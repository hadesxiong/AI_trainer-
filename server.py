#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
人工智能训练师三级刷题系统 — 云同步服务端（单文件 / 零依赖）

- 托管刷题系统 HTML 页面（浏览器直接通过 URL 访问）
- 使用 SQLite 存储刷题状态，实现多终端数据共享
- 仅使用 Python 标准库，无需 pip install 任何东西

用法:
    python3 server.py                     # 0.0.0.0:8787
    python3 server.py --port 9000
    python3 server.py --host 127.0.0.1 --port 8787

数据库文件: same directory `ai3_sync.db`（首次运行自动创建）
"""

import argparse
import json
import os
import sqlite3
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 按优先级查找要托管的页面
HTML_CANDIDATES = [
    "人工智能训练师三级刷题系统_v2.html",
    "人工智能训练师三级刷题系统_v1.html",
]

DB_FILE = os.path.join(BASE_DIR, "ai3_sync.db")
MAX_BODY = 64 * 1024 * 1024  # 64MB 足够覆盖任何含完整试卷的存档

_db_lock = threading.Lock()


def get_db():
    con = sqlite3.connect(DB_FILE)
    con.row_factory = sqlite3.Row
    return con


def init_db():
    con = get_db()
    try:
        con.execute(
            """
            CREATE TABLE IF NOT EXISTS sync_state (
                id INTEGER PRIMARY KEY CHECK (id = 1),
                data_json TEXT,
                revision INTEGER NOT NULL DEFAULT 0,
                updated_at INTEGER NOT NULL DEFAULT 0
            )
            """
        )
        row = con.execute("SELECT id FROM sync_state WHERE id = 1").fetchone()
        if row is None:
            con.execute(
                "INSERT INTO sync_state (id, data_json, revision, updated_at) VALUES (1, NULL, 0, 0)"
            )
        con.commit()
    finally:
        con.close()


def load_state():
    con = get_db()
    try:
        row = con.execute(
            "SELECT data_json, revision, updated_at FROM sync_state WHERE id = 1"
        ).fetchone()
        data = json.loads(row["data_json"]) if row["data_json"] else None
        return data, int(row["revision"]), int(row["updated_at"])
    finally:
        con.close()


def save_state(data, client_revision):
    """带乐观并发校验的写入。client_revision 为 None 视为强制覆盖。"""
    with _db_lock:
        con = get_db()
        try:
            row = con.execute(
                "SELECT revision, data_json FROM sync_state WHERE id = 1"
            ).fetchone()
            server_rev = int(row["revision"])
            if client_revision is not None and int(client_revision) != server_rev:
                server_data = json.loads(row["data_json"]) if row["data_json"] else None
                con.close()
                return False, server_data, server_rev  # 409 冲突
            now = int(time.time() * 1000)
            con.execute(
                "UPDATE sync_state SET data_json = ?, revision = ?, updated_at = ? WHERE id = 1",
                (json.dumps(data, ensure_ascii=False), server_rev + 1, now),
            )
            con.commit()
            return True, None, server_rev + 1
        finally:
            con.close()


class Handler(BaseHTTPRequestHandler):
    server_version = "AI3Sync/1.0"
    protocol_version = "HTTP/1.1"

    # ---- 基础工具 ----

    def _cors(self):
        # 允许 file:// 直接打开的页面也能连接本服务（可选用法）
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")

    def _send_json(self, payload, status=200):
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self._cors()
        self.end_headers()
        self.wfile.write(body)

    def _send_file(self, path, ctype):
        try:
            with open(path, "rb") as f:
                body = f.read()
        except OSError:
            self._send_json({"error": "not found"}, 404)
            return
        self.send_response(200)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self._cors()
        self.end_headers()
        self.wfile.write(body)

    def _read_body(self):
        length = int(self.headers.get("Content-Length") or 0)
        if length <= 0 or length > MAX_BODY:
            return None
        return self.rfile.read(length)

    def log_message(self, fmt, *args):  # 精简日志
        print("[%s] %s" % (time.strftime("%H:%M:%S"), fmt % args))

    # ---- 路由 ----

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Content-Length", "0")
        self._cors()
        self.end_headers()

    def do_GET(self):
        path = self.path.split("?")[0].split("#")[0]
        if path == "/api/state":
            data, revision, updated_at = load_state()
            self._send_json(
                {
                    "data": data,
                    "revision": revision,
                    "updatedAt": updated_at,
                }
            )
            return
        if path in ("/", "/index.html"):
            for name in HTML_CANDIDATES:
                p = os.path.join(BASE_DIR, name)
                if os.path.isfile(p):
                    self._send_file(p, "text/html; charset=utf-8")
                    return
            self._send_json({"error": "HTML file not found"}, 404)
            return
        self._send_json({"error": "not found"}, 404)

    def do_POST(self):
        path = self.path.split("?")[0].split("#")[0]
        if path != "/api/state":
            self._send_json({"error": "not found"}, 404)
            return
        raw = self._read_body()
        if raw is None:
            self._send_json({"error": "invalid body"}, 400)
            return
        try:
            payload = json.loads(raw.decode("utf-8"))
        except (ValueError, UnicodeDecodeError):
            self._send_json({"error": "invalid json"}, 400)
            return
        data = payload.get("data") if isinstance(payload, dict) else None
        client_revision = payload.get("revision") if isinstance(payload, dict) else None
        if client_revision is None:
            client_revision = 0  # 从未拉取过的客户端按 revision 0 校验
        if not isinstance(data, dict):
            self._send_json({"error": "'data' must be an object"}, 400)
            return
        try:
            int(client_revision)
        except (TypeError, ValueError):
            self._send_json({"error": "invalid revision"}, 400)
            return

        ok, server_data, server_rev = save_state(data, int(client_revision))
        if ok:
            print(f"       状态已保存 (revision -> {server_rev})")
            self._send_json({"ok": True, "revision": server_rev})
        else:
            self._send_json({"ok": False, "data": server_data, "revision": server_rev}, 409)


def main():
    parser = argparse.ArgumentParser(description="AI三级刷题系统 云同步服务端")
    parser.add_argument("--host", default="0.0.0.0", help="监听地址（默认 0.0.0.0）")
    parser.add_argument("--port", type=int, default=8787, help="监听端口（默认 8787）")
    args = parser.parse_args()

    init_db()
    data, _, _ = load_state()
    print("=" * 52)
    print("  人工智能训练师三级刷题系统 · 云同步服务端")
    print("=" * 52)
    print(f"  数据库: {DB_FILE}")
    print(f"  云端状态: {'已有数据' if data else '空（等待首次同步）'}")
    print(f"  访问地址: http://<本机IP>:{args.port}/")
    print("=" * 52)

    server = ThreadingHTTPServer((args.host, args.port), Handler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n服务已停止")
        server.server_close()


if __name__ == "__main__":
    main()
