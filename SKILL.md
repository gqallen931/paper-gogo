---
name: paper-gogo
description: AI-orchestrated paper production workflow. 18-phase pipeline (0-17) in 4 stages from project kickoff to journal submission and reviewer response. Covers 10+ ML domains. Framework-agnostic, integrates 30+ sub-skills for architecture, code understanding, Nature-grade publishing, and academic review simulation.
model: sonnet
---

# Paper-gogo v5.0 · 论文工作流编排器

> AI 协作的学术论文全流程工作流。18 Phase (0-17) 覆盖从项目启动到审稿回复的完整生命周期。

## 一句话

从 idea 到 accepted paper 的 AI 协作工作流。

## 适用范围

**10 大领域**：CV / NLP / LLM / KG / Medical AI / PHM / Time Series / RL / Speech / Tabular ML

**框架无关**：PyTorch / TensorFlow / JAX / NumPy 均可

## 激活方式

在 Claude Code 或 Codex 对话中输入：

```
/paper-gogo
```

或直接说"启动 Phase N"（N = 0-17）。

## 工作流架构

```
准备阶段 (0-5)  →  实现阶段 (6-8)  →  写作阶段 (9-10)  →  投稿阶段 (11-17)

Phase 0  项目检查              understand → 知识图谱
Phase 1  必需要素采集            方向+创新=硬性必须
Phase 2  文献检索入库            30+ PDF→md (全文+图表+参考文献)
Phase 3  全文阅读+综述           可发表级学术综述
Phase 4  创新点+四标准审查        模块堆砌检测/真实创新/二区水准/实验可行性
Phase 5  方案设计+框架图S0-S3     期刊→baseline→协议→RQ→框架图草图
Phase 6  项目代码构建            工程架构+smoke test
Phase 7  实验执行                9子阶段+双路径+防烧token+缓存+回溯
Phase 8  结果审查                完整性+代码扫描+公平性+checklist
Phase 9  可视化+GraphicalAbstract 任务自适应图+框架图S4-S7+图画摘要
Phase 10 论文撰写                摘抄·仿写·改写+图表布局+编号管理
Phase 11 内容审查+引用校验        四维审查+术语锁定+引用校验+期刊checklist
Phase 12 引用插入+终稿润色        SCI引用插入+[1]起编号+定稿
Phase 13 框架图+模块图绘制        基于定稿+代码→最终框架图+模块详图
Phase 14 全文整合+终稿审查        10项全面审查→投稿包
Phase 15 二次润色+去AI率          AI痕迹检测+人工化改写
Phase 16 期刊匹配+审稿模拟        编辑审查→审稿人模拟→桌拒/录用概率
Phase 17 审稿意见回复            逐点回复→修改→回复信→提交
```

## 全局规则

1. **对话式，非流水线**：Phase 松耦合，用户可任意跳转、回溯。AI 提问引导，不强制执行门禁。
2. **每 Phase 结束自动工作记录**：保存到 `docs/项目工作阶段记录/Phase{N}_{name}.md`。
3. **技能按需调用**：每个 Phase 列出推荐技能，AI 根据实际选用，不堆砌。
4. **用户确认关键节点**：创新点确认、实验范围、投稿决策必须经用户确认。
5. **Stubs 优于中断**：缺失依赖自动 fallback，不中断。
6. **目录约束**：所有产物在 `docs/` 子目录下。

## 技能依赖

本技能包包含以下子技能目录，通过 `/paper-gogo` 调用时自动可用：

| 技能目录 | 技能等级 | 用途 |
|---------|---------|------|
| `nature-skills/` | L9 | Nature 出版工具（读写/检索/写作/绘图/润色/引用/数据/PPT/审稿） |
| `code-understanding/` | L9 | 代码深度理解（知识图谱/问答/差异/解释/领域/入门） |
| `architecture-engineering/` | L8 | 代码质量把控（设计/建模/审查/测试/TDD/冲突） |
| `world-model-method/` | — | 全局统筹/决策/审查 |
| `paper-framework-figure-studio-pro/` | — | 论文总体框架图 v3.1.4a |
| `karpathy-guidelines/` | — | Karpathy 代码质量准则（全局注入） |
| `python-expert/` | — | Python 专家支持 |

### 外部技能（需单独安装，路径见下文）

| 技能 | 路径 | 用途 |
|------|------|------|
| paper-craft-skills | `D:\Skills\paper-craft-skills-main.zip` | 论文工艺（摘抄/仿写/改写/术语/AI检测） |
| academic-research-skills | `D:\Skills\academic-research-skills-main.zip` | 学术研究（内容审查/期刊匹配/审稿模拟） |
| scipilot-figure-skill | `D:\Skills\scipilot-figure-skill-main.zip` | 科学图表辅助（模块图/配色/布局） |
| codegraph | `D:\Skills\codegraph-main.zip` | 代码结构可视化 |
| codex-plusplus | `D:\Skills\codex-plusplus-main.zip` | 代码增强 |

### 技能 × Phase 矩阵

| Phase | nature | understand | arch-eng | world-model | paper-fig | paper-craft | academic-res | scipilot |
|-------|:------:|:----------:|:--------:|:-----------:|:---------:|:-----------:|:------------:|:--------:|
| 0 | | ● | | | | | | |
| 1 | | | | | | | | |
| 2 | ● | ● | | | | | | |
| 3 | ● | | | ○ | | | | |
| 4 | ● | | ○ | ● | | | ● | |
| 5 | ● | | | ● | ●(S0-S3) | | | |
| 6 | | ● | ● | ○ | | | | |
| 7 | | | | ● | | | | |
| 8 | | ● | ● | ● | | | | |
| 9 | ● | | | ○ | ●(S4-S7) | | ○ | ● |
| 10 | ● | | | ○ | | ● | | |
| 11 | ● | | | ● | | ● | ● | |
| 12 | ● | | | | ○ | ● | | |
| 13 | ● | ● | | ○ | ● | ○ | | ● |
| 14 | ● | | | ● | ○ | ● | ● | |
| 15 | ● | | | | | ● | | |
| 16 | ● | | | ● | | ○ | ● | |
| 17 | ● | | | ○ | | ● | ● | |

> ● = 主要使用  ○ = 辅助使用

## 安装

### Claude Code

```bash
# 方式 1：直接复制
cp -r D:/Skills/Paper-gogo ~/.claude/skills/paper-gogo

# 方式 2：从 GitHub 安装
# (push 到 GitHub 后在 Claude Code 中)
/install paper-gogo
```

然后在任意项目中：`/paper-gogo`

### Codex (OpenAI)

```bash
# 复制技能包到 Codex skills 目录
cp -r D:/Skills/Paper-gogo ~/.codex/skills/paper-gogo
```

然后在 Codex 对话中：`/paper-gogo`

## 文档

| 文件 | 内容 |
|------|------|
| `论文工作流_v5.md` | 完整 18 Phase 工作流（含 Mermaid 图 + 控制台规范 + 缓存机制） |
| `论文工作流.md` | 同上（主文档入口） |
| `工作流问题记录.md` | 全量实测+假设测试记录（~38 条问题→设计迭代） |
| `code_assets/` | 可复用代码模板（Trainer/实验/指标/配置/脚手架） |
| `README.md` | 技能清单 + 安装指南 |
