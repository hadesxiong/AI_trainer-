# -*- coding: utf-8 -*-
"""
模拟操作测试抽题脚本

功能：
  1. 在 mock_exam/ 下创建会话文件夹：YYYY_MM_DD_HHMMSS_<uuid8>
  2. 按考试抽题规则从素材中随机抽取 6 题，复制素材文件（保留原目录结构），
     排除 *_answer.ipynb、*.doc、*.docx
  3. 在会话文件夹内生成"考题.md"（题目序号 + 题号 + 试题名称 + 抽中文件清单）

用法：
  python extract_mock_exam.py            # 随机抽题
  python extract_mock_exam.py --seed 42  # 固定随机种子（复盘同一套题）
  python extract_mock_exam.py --keep-docx  # 额外保留 doc/docx 答题卷（默认排除）
"""

import argparse
import shutil
import time
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC_DIR = ROOT / "人工智能训练师三级素材" / "人工智能训练师三级上网素材"
MOCK_DIR = ROOT / "mock_exam"

# 题目1：1.1.x 全部 + 1.2.x 全部（共 10 题，与"总共10题"一致）
POOL_1 = [f"1.1.{i}" for i in range(1, 6)] + [f"1.2.{i}" for i in range(1, 6)]
POOL_2 = [f"2.1.{i}" for i in range(1, 6)]
POOL_3 = [f"2.2.{i}" for i in range(1, 6)]
POOL_4 = [f"3.1.{i}" for i in range(1, 6)]
POOL_5 = [f"3.2.{i}" for i in range(1, 6)]
# 题目6：4.1.x + 4.2.x（共 10 题）
POOL_6 = [f"4.1.{i}" for i in range(1, 6)] + [f"4.2.{i}" for i in range(1, 6)]

POOLS = [
    ("题目1", POOL_1),
    ("题目2", POOL_2),
    ("题目3", POOL_3),
    ("题目4", POOL_4),
    ("题目5", POOL_5),
    ("题目6", POOL_6),
]

# 40 题试题名称（源自《第4部分_人工智能训练师_3级_操作技能复习题》）
TITLES = {
    "1.1.1": "智能医疗系统中的业务数据处理流程设计",
    "1.1.2": "智能农业系统中的业务数据采集和处理流程设计",
    "1.1.3": "金融机构信用评估系统中的业务数据审核流程设计",
    "1.1.4": "电商平台用户行为分析系统的数据采集与处理流程设计",
    "1.1.5": "智能交通系统的数据采集、处理和审核流程设计",
    "1.2.1": "顾客评价情感识别业务模块效果优化",
    "1.2.2": "老年人健康监测与管理服务业务模块效果优化",
    "1.2.3": "智慧金融服务业务模块效果优化",
    "1.2.4": "智能卖点生成系统业务模块效果优化",
    "1.2.5": "腾讯云智能数智人系统业务模块效果优化",
    "2.1.1": "智慧交通中燃油效率模型的数据清洗和标注流程设计",
    "2.1.2": "低碳生活行为影响因素数据清洗和标注流程设计",
    "2.1.3": "信用评分模型数据清洗和标注流程设计",
    "2.1.4": "医疗研究数据清洗和标注设计",
    "2.1.5": "健康与营养咨询数据预处理与数据规范设计",
    "2.2.1": "智能信用评分Logistic回归模型开发与测试",
    "2.2.2": "智慧交通中燃油效率随机森林模型开发与测试",
    "2.2.3": "日常运动量随机森林预测模型开发与测试",
    "2.2.4": "低碳生活行为影响因素预测线性回归模型开发与测试",
    "2.2.5": "智能步数预测模型开发与测试",
    "3.1.1": "智能音箱产品的数据分析与优化",
    "3.1.2": "智能照明系统的数据分析与优化",
    "3.1.3": "智能健康手环的数据分析与优化",
    "3.1.4": "智能健康监测系统的数据分析与优化",
    "3.1.5": "智能家居环境控制系统的数据分析与优化",
    "3.2.1": "图像识别评估系统交互流程设计",
    "3.2.2": "手写数字识别系统交互流程设计",
    "3.2.3": "面部表情识别系统交互流程设计",
    "3.2.4": "花朵智能识别系统交互流程设计",
    "3.2.5": "人脸AI智能检测系统交互流程设计",
    "4.1.1": "Label studio培训大纲编写",
    "4.1.2": "爬虫培训大纲编写",
    "4.1.3": "数据清洗培训大纲编写",
    "4.1.4": "Pandas数据清洗培训大纲编写",
    "4.1.5": "Python数据可视化培训大纲编写",
    "4.2.1": "智能零售分析系统数据采集和处理指导",
    "4.2.2": "AI辅助的医疗影像诊断系统数据采集和处理指导",
    "4.2.3": "AI智能安防监控系统采集和处理指导",
    "4.2.4": "自动驾驶汽车感知系统数据采集与标注指导",
    "4.2.5": "智能化数据标注在文化遗产数字化保护中的应用指导",
}


def is_excluded(name: str) -> bool:
    """排除 _answer.ipynb 与 doc/docx（大小写不敏感）"""
    lower = name.lower()
    if lower.endswith("_answer.ipynb"):
        return True
    if lower.endswith((".doc", ".docx")):
        return True
    return False


def make_ignore(keep_docx: bool):
    def _ignore(_dir: str, files: list[str]) -> list[str]:
        if keep_docx:
            return [f for f in files if f.lower().endswith("_answer.ipynb")]
        return [f for f in files if is_excluded(f)]
    return _ignore


def copy_question(qid: str, dst_root: Path, keep_docx: bool) -> list[str]:
    """复制单题素材，返回复制后的相对文件路径列表"""
    src = SRC_DIR / qid
    dst = dst_root / qid
    if not src.is_dir():
        raise FileNotFoundError(f"素材目录不存在: {src}")
    shutil.copytree(src, dst, ignore=make_ignore(keep_docx))

    copied = sorted(
        str(p.relative_to(dst_root)) for p in dst.rglob("*") if p.is_file()
    )
    return copied


def build_exam_md(records: list[dict], session_name: str, timestamp: str) -> str:
    lines = [
        "# 模拟操作测试考题",
        "",
        f"- 抽取时间：{timestamp}",
        f"- 会话目录：`mock_exam/{session_name}`",
        "",
        "---",
        "",
    ]
    for rec in records:
        qid = rec["qid"]
        lines.append(f"## {rec['label']}：{qid} —— {TITLES.get(qid, '（未知试题名称）')}")
        lines.append("")
        if rec["files"]:
            lines.append("素材文件：")
            lines.append("")
            for f in rec["files"]:
                lines.append(f"- `{f}`")
        else:
            lines.append(
                "> ⚠️ 该题素材目录中除 doc/docx 外无其他文件（文档题的答题卷为 docx，"
                "按默认排除规则未复制）。如需答题卷，请加 `--keep-docx` 重新抽取。"
            )
        lines.append("")
        lines.append("---")
        lines.append("")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="模拟操作测试抽题脚本")
    parser.add_argument("--seed", type=int, default=None, help="随机种子（复现同一套题）")
    parser.add_argument(
        "--keep-docx",
        action="store_true",
        help="额外保留 doc/docx 文件（默认排除）",
    )
    args = parser.parse_args()

    import random

    if args.seed is not None:
        random.seed(args.seed)

    if not SRC_DIR.is_dir():
        raise SystemExit(f"未找到素材目录: {SRC_DIR}")

    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    session_name = f"{time.strftime('%Y_%m_%d_%H%M%S')}_{uuid.uuid4().hex[:8]}"
    session_dir = MOCK_DIR / session_name
    session_dir.mkdir(parents=True, exist_ok=True)

    records = []
    for label, pool in POOLS:
        qid = random.choice(pool)
        files = copy_question(qid, session_dir, keep_docx=args.keep_docx)
        records.append({"label": label, "qid": qid, "files": files})

    md_path = session_dir / "考题.md"
    md_path.write_text(
        build_exam_md(records, session_name, timestamp), encoding="utf-8"
    )

    print(f"[完成] 模拟考题已生成: {md_path}")
    for rec in records:
        title = TITLES.get(rec["qid"], "")
        print(f"  {rec['label']}：{rec['qid']}  {title}  ({len(rec['files'])} 个文件)")


if __name__ == "__main__":
    main()
