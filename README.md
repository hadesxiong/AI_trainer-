# 人工智能训练师（三级）备考资料 / AI Trainer Level 3 Study Materials

## 项目简介 / Overview

本项目整理了“人工智能训练师”（职业编码：4-04-05-05）三级职业技能等级认定的备考资料，包括理论题库、在线刷题系统、参考答案和操作技能资料。

This repository collects study materials for the Level 3 certification of “Artificial Intelligence Trainer” (occupation code: 4-04-05-05), including theory question banks, an offline quiz system, reference answers, and practical-skill materials.

级别信息参考：`国家职业技能标准4-04-05-05.pdf`。资料来源：https://gjzs.sjtu.edu.cn （上海交通大学终身教育学院）。

Reference standard: `国家职业技能标准4-04-05-05.pdf`. Source materials are from https://gjzs.sjtu.edu.cn (School of Lifelong Education, Shanghai Jiao Tong University).

**注意：官方未提供答案，本项目中的答案均为个人理解整理，仅供学习交流参考。**

**Note: Official answers are not provided. The answers in this repository are personal study notes and are for learning and discussion only.**

## 文件说明 / Files

| 文件/文件夹 | 中文说明 | English Description |
|-------------|----------|---------------------|
| `4-04-05-05_3_20250701.zip` | 人工智能训练师（三级）职业技能等级认定指导手册 | Official guidance package for the Level 3 certification |
| `人工智能训练师三级题库/` | 指导手册解压后的题库文件（第0-6部分） | Extracted question-bank files from the guidance package |
| `人工智能训练师三级题库-v1.md` | 理论知识题库 Markdown 版本（判断300题 + 单选300题 + 多选300题） | Markdown version of the theory question bank: 300 true/false, 300 single-choice, and 300 multiple-choice questions |
| `人工智能训练师三级刷题系统_v1.html` | 理论知识在线刷题系统，详见下方说明 | Offline browser-based quiz system for theory practice |
| `人工智能训练师三级理论答案.xlsx` | 理论知识参考答案（3个 sheet：判断/单选/多选） | Reference answers for theory questions, with separate sheets for true/false, single-choice, and multiple-choice |
| `人工智能训练师三级素材/` | 操作技能考试所需上网素材、模拟界面及操作题答案 | Practical-skill exam materials, mock interfaces, and reference answers |
| `人工智能训练师三级素材/操作题答案/` | 40道操作技能题的参考答案与解析 | Reference answers and explanations for 40 practical-skill tasks |
| `个人承诺书.zip` | 报名所需的个人承诺书模板 | Personal commitment letter template for registration |
| `国家职业技能标准4-04-05-05.pdf` | 人工智能训练师国家职业技能标准全文 | Full national occupational skill standard |

## 刷题系统 / Quiz System

主文件：`人工智能训练师三级刷题系统_v1.html`

Main file: `人工智能训练师三级刷题系统_v1.html`

### 打开方式 / How To Open

直接用浏览器打开该 HTML 文件即可，推荐 Chrome 或 Edge。无需安装、无需联网、无需登录。

Open the HTML file directly in a browser. Chrome or Edge is recommended. No installation, internet connection, or login is required.

### 功能模块 / Features

1. **题库刷题**：包含判断题300题、单选题300题、多选题300题。支持按题型浏览、翻页、实时判对错并显示正确答案。

   **Question-bank practice**: Includes 300 true/false, 300 single-choice, and 300 multiple-choice questions. Supports browsing by type, page navigation, instant grading, and answer display.

2. **模拟考试**：包含官方模拟试卷和随机组卷两种模式。题型分布为判断40题 + 单选140题 + 多选10题，限时90分钟，满分100分，60分及格。

   **Mock exams**: Includes official mock-paper mode and random-paper mode. The paper structure is 40 true/false + 140 single-choice + 10 multiple-choice questions, with a 90-minute time limit, 100 total points, and 60 points to pass.

3. **错题本**：自动收录做错的题目，支持按题型和反复错筛选，也支持针对筛选结果专项练习。错题练习状态按题目本身存储，避免移除错题后串题。

   **Wrong-question notebook**: Automatically records incorrect answers, supports filtering by question type and repeated mistakes, and allows focused practice. Practice state is stored by question key to avoid state carry-over after removing a wrong question.

4. **本地存档**：支持把做题进度、错题本和考试记录导出为 JSON 存档，也支持之后导入恢复。

   **Local save files**: Supports exporting progress, wrong questions, and exam records as a JSON save file, and importing it later for recovery or migration.

### 数据存储 / Data Storage

所有做题进度、考试记录和错题本数据都保存在浏览器本地存储（localStorage）中：

All progress, exam records, and wrong-question data are stored in the browser’s localStorage:

- 同一浏览器下次打开会自动恢复进度。  
  Progress is restored automatically when the same browser opens the file again.
- 清除浏览器数据会导致记录丢失。  
  Clearing browser data will remove saved records.
- 不同浏览器之间数据默认不互通。  
  Different browsers do not share data by default.

主要 localStorage 键 / Main localStorage keys:

- `ai3_bankAnswered`：题库页每题是否已答及用户答案 / Per-question answer state in practice mode
- `ai3_bankStats`：题库页每题的作答次数与正确次数 / Attempt and correctness statistics
- `ai3_wrong`：错题本条目、累计错题次数、连续答对次数等 / Wrong-question entries and review counters
- `ai3_examResults`：模拟考试记录与可选的整卷回顾数据 / Mock-exam records and optional full-paper review data
- `ai3_wrongSettings`：错题移除规则 / Wrong-question removal settings

若需跨浏览器或跨设备保存，请使用刷题系统内的“导出存档 / 导入存档”按钮。

To move data across browsers or devices, use the “Export Save / Import Save” buttons in the quiz system.

### 进度管理 / Progress Management

- 题库页支持“重置本页进度”和“重置本题型进度”。  
  The practice page supports resetting the current page or the current question type.
- 考试记录支持逐条删除和完整试卷回顾。  
  Exam records can be deleted individually and reviewed as full papers.

## 手机友好版社区贡献 / Mobile-Friendly Community Contribution

感谢 @hughware 提交的手机友好版尝试：PR #2 “添加了一个适合手机小屏幕使用的版本”。

Thanks to @hughware for proposing a mobile-friendly version in PR #2, “添加了一个适合手机小屏幕使用的版本”.

该版本目前没有合入主线。主要原因是本项目当前以电脑端刷题和电脑考试场景为主，现有主线版本已经覆盖判断、单选、多选和完整模拟考试流程。手机友好版对小屏幕体验很有帮助，但目前功能覆盖和主线版本并不完全一致。

This version has not been merged into the main branch. The current project focuses on desktop-based practice and exam preparation, and the main quiz system already covers true/false, single-choice, multiple-choice, and the full mock-exam workflow. The mobile-friendly version is useful for small screens, but its feature coverage is not fully aligned with the main version yet.

有手机端需求的用户仍可查看该贡献：  
Users who need a mobile-oriented version can still find the contribution here:

https://github.com/xxiao1127/AI_trainer-/pull/2

## 操作技能参考答案 / Practical-Skill Reference Answers

`人工智能训练师三级素材/操作题答案/` 中包含 40 道操作技能题的参考答案，覆盖全部 4 大类 8 小类。

The folder `人工智能训练师三级素材/操作题答案/` contains reference answers for 40 practical-skill tasks, covering all 4 major categories and 8 subcategories.

| 类别 | 题型 | 答案内容 |
|------|------|----------|
| 1.1.x（5题） | 数据采集与处理（Python） | 完整代码 + 填空速查 + 解析 |
| 1.2.x（5题） | 业务模块效果优化 | 问题分析 + 优化方案 |
| 2.1.x（5题） | 数据清洗与标注（Python） | 完整代码 + 解析 |
| 2.2.x（5题） | 模型开发与测试（sklearn） | 完整代码 + 测试报告模板 |
| 3.1.x（5题） | 产品数据分析与优化 | 基于真实数据的分析报告 + 优化方案 |
| 3.2.x（5题） | AI模型推理（ONNX） | 完整代码 + 交互流程设计 |
| 4.1.x（5题） | 培训大纲编写 | 学习目标填空答案 |
| 4.2.x（5题） | 数据采集处理方案 | 填空答案 + 方案设计 |

## 本 Fork 更新说明 / Fork Updates

本 Fork 在上游（xxiao1127/AI_trainer-）基础上补充了以下内容，**上游原有文件与目录结构未做任何改动**。

This fork adds the following on top of the upstream repository (xxiao1127/AI_trainer-). **All original upstream files and directory structure remain untouched.**

### 新增内容 / What's New

| 新增内容 | 说明 | Description |
|----------|------|-------------|
| `*_answer.ipynb`（20 个） | 1.1.x / 2.1.x / 2.2.x / 3.2.x 各 5 题的**答题 ipynb**，基于原始题目文档（试题单 + 评分表 M1~Mn）逐项核对填写 | Answered notebooks for the 20 coding tasks (5 each of 1.1.x / 2.1.x / 2.2.x / 3.2.x), filled and verified item-by-item against the original exam papers and scoring rubrics |
| `实操考前冲刺行动指南.md` | 考前 1 小时冲刺指南：全局考场铁律 + 8 大题型区间（概要 / 答题要点 / 产出自检） | A pre-exam sprint guide: global exam rules + 8 task-type sections (overview / key points / deliverable checklist) |
| `extract_mock_exam.py` | 模拟操作测试抽题脚本，按考试抽题规则随机组卷并生成 `考题.md` | Mock-exam extractor: randomly draws one question per exam rule and generates a `考题.md` question sheet |
| `mock_exam/` | 抽题脚本的输出目录（每次运行生成一个带时间戳的会话文件夹），已被 `.gitignore` 忽略 | Output folder of the extractor (one timestamped session folder per run); ignored via `.gitignore` |

### 目录速览 / Repository Layout

```
AI_trainer-/
├── 人工智能训练师三级题库/        # 原始题库（理论 + 操作技能原题文档）
├── 人工智能训练师三级素材/        # 操作技能素材（上网素材 + 参考答案）
│   └── 人工智能训练师三级上网素材/  #   40 个题目文件夹（含 *_answer.ipynb）
├── mock_exam/                    # 模拟考产物（git 忽略）
├── extract_mock_exam.py          # 模拟考抽题脚本
├── 实操考前冲刺行动指南.md        # 考前冲刺指南
└── （根目录其余文件为上游原有内容）
```

### 模拟考抽题脚本用法 / Mock-Exam Extractor Usage

```bash
python extract_mock_exam.py              # 随机抽一套模拟题
python extract_mock_exam.py --seed 42    # 固定随机种子，复现同一套题
python extract_mock_exam.py --keep-docx  # 额外保留 doc/docx 答题卷（默认排除）
```

抽题规则与真实考试一致：题目1（1.1.x + 1.2.x 抽 1）、题目2~5（2.1.x / 2.2.x / 3.1.x / 3.2.x 各抽 1）、题目6（4.1.x + 4.2.x 抽 1），共 6 题；排除 `*_answer.ipynb` 与 doc/docx，其余文件保留原目录结构。

The draw mirrors the real exam: 6 questions total — one from (1.1.x + 1.2.x), one each from 2.1.x / 2.2.x / 3.1.x / 3.2.x, and one from (4.1.x + 4.2.x). `*_answer.ipynb` and doc/docx files are excluded; all other files keep their original structure.

## 贡献与致谢 / Contributors and Acknowledgements

感谢所有为本项目提供帮助的人。GitHub 的 Contributors 页面会根据提交作者账号和邮箱自动统计；OpenAI Codex 作为 AI 协作助手没有独立的 GitHub 账号，因此不会出现在自动统计列表中，但它参与了本项目的代码审查、错题本修复、PR 处理和 README 中英双语整理。

Thanks to everyone who has helped improve this project. GitHub's Contributors page is generated automatically from commit authors and linked accounts. OpenAI Codex does not have an independent GitHub account, so it does not appear in that automatic list, but it assisted with code review, wrong-question notebook fixes, PR handling, and bilingual README updates.

- @xxiao1127：项目整理、维护与答案校对 / Project organization, maintenance, and answer review
- @hughware：错题本修复与手机友好版尝试 / Wrong-question notebook fix and mobile-friendly version proposal
- Claude：早期辅助整理 / Early assistant-supported organization
- OpenAI Codex：代码审查、维护修复、PR 处理与文档整理 / Code review, maintenance fixes, PR handling, and documentation updates
## 声明 / Notice

- 来源 / Source: https://github.com/xxiao1127
- 本资料全部开源免费，答案仅为个人理解，仅供学习交流参考。  
  These materials are open and free. Answers reflect personal understanding and are for learning and discussion only.
- 禁止任何形式的商用、倒卖或未经授权的转载。  
  Commercial resale or unauthorized redistribution is not allowed.
- 联系作者 / Contact: shellyx060@gmail.com