# 内置技能清单

本文件由 `scripts/build-skills-index.mjs` 自动生成，请勿手改。它列出插件 `workflow/` 目录中实际内置的技能。

Paper-gogo 的规则是：**只有解压为目录且存在可读取 `SKILL.md` 的技能才能被路由调用**。下面每一项都满足该条件。

## 工作流技能（`workflow/skills/`）

### nature-skills（9 个）

| 技能 | 说明 |
|---|---|
| `nature-academic-search` | Multi-source literature search, citation verification, MeSH search strategy, citation file management (.nbib/.ris/.bib conversion), and reference management (BibTeX, related articles, ID conversion) via MCP tools (PubMed, CrossRef, arXiv). Use when the user needs coordinated multi-step literature workflows beyond a single MCP call. |
| `nature-citation` | Add strict Nature/CNS citations to manuscript text by splitting long passages into citable segments, searching only accepted flagship and subjournal titles from Nature Portfolio, the AAAS Science family, and Cell Press, filtering by publication time range, and exporting one reference-manager-ready output by default. Use this skill whenever the user asks to input text and automatically get references, add citations to a paragraph/manuscript, find Nature-series or CNS support for statements, create text-to-reference correspondence, "分段引用", "自动给出引用", "Nature系列引用", "CNS及子刊", "支撑文献", "补引用", "找引用", or export EndNote/RIS/ENW/Zotero RDF. |
| `nature-data` | Prepare, audit, or revise Nature-ready Data Availability statements, data repository plans, dataset citations, and FAIR metadata checklists for manuscripts. Use when the user asks about Nature data availability, research data sharing, repository selection, accession numbers, restricted or sensitive data, source data, supplementary datasets, DataCite-style dataset references, FAIR metadata for academic publication, or Chinese-to-English data availability wording for Chinese-speaking authors preparing Nature-family submissions. |
| `nature-figure` | Submission-grade Nature/high-impact journal figure workflow for Python or R. Use whenever the user asks to create, revise, audit, or polish manuscript figures, multi-panel scientific plots, figures4papers-style matplotlib plots, or journal-ready SVG/PDF/TIFF outputs, especially for Nature-family or other high-impact journals. Before plotting, define the figure's conclusion, evidence logic, export needs, and review risks. If the user has not chosen Python or R, ask "Python or R?" and stop. Use only the selected backend for figure generation, previewing, exporting, and QA. Supports matplotlib/seaborn and ggplot2/patchwork/ComplexHeatmap. Not for dashboards or Illustrator/Figma-first infographics. |
| `nature-paper2ppt` | Build a complete but efficient Nature-style Chinese PPTX presentation from a scientific paper, preprint, PDF, article text, abstract, figure legends, or reading notes. Use this skill whenever the user asks to make slides/PPT/PPTX for journal club, group meeting, paper sharing, thesis seminar, lab meeting, department report, or academic presentation from a research paper, not only medical papers. It identifies the paper type and argument, selects only the figures needed for the story, writes Chinese slide content and speaker notes, creates the actual .pptx deck, and performs lightweight verification with cross-platform Python tooling by default. |
| `nature-polishing` | Polish, restructure, or translate academic prose into Nature-leaning English using writing-strategy principles, curated Nature/Nature Communications article patterns, and phrase-level support from Academic Phrasebank. Use whenever the user asks to polish a manuscript paragraph, abstract, introduction, results, discussion, conclusion, title, methods section, or Chinese academic draft for publication-quality English. |
| `nature-reader` | Build full-paper Chinese-English side-by-side, figure/table-aware, source-grounded Markdown readers for journal or conference papers from PDF, DOI, arXiv, publisher HTML, or pasted text. Use whenever the user asks to translate or read a paper, make 中英文对照/原文对照/全文翻译解读, extract figures or tables into the right positions, preserve figure/table placement near relevant prose, or keep exact source anchors for every block. This skill must not degrade into a summary-only output unless the user explicitly asks for a summary. |
| `nature-response` | Draft, audit, or revise point-by-point reviewer response letters for Nature-family manuscript revisions. Use when the user provides reviewer comments, editor decision letters, revision notes, response drafts, or asks how to respond to major/minor revision requests, rebuttal letters, response to reviewers, peer-review reports, 审稿意见回复, 逐点回复, 修回信, 大修回复, 小修回复, or 如何回复 reviewer. |
| `nature-writing` | Draft, restructure, or plan Nature-style manuscript sections from author-provided claims, results, figures, notes, or Chinese drafts. Use when the user wants to write or rebuild an abstract, introduction, results narrative, discussion, conclusion, title, or full manuscript argument rather than only polish finished prose. |

### code-understanding（9 个）

| 技能 | 说明 |
|---|---|
| `diagnosing-bugs` | Diagnosis loop for hard bugs and performance regressions. Use when the user says "diagnose"/"debug this", or reports something broken/throwing/failing/slow. |
| `understand` | Analyze a codebase to produce an interactive knowledge graph for understanding architecture, components, and relationships |
| `understand-chat` | Use when you need to ask questions about a codebase or understand code using a knowledge graph |
| `understand-dashboard` | Launch the interactive web dashboard to visualize a codebase's knowledge graph |
| `understand-diff` | Use when you need to analyze git diffs or pull requests to understand what changed, affected components, and risks |
| `understand-domain` | （未声明 description） |
| `understand-explain` | （未声明 description） |
| `understand-knowledge` | （未声明 description） |
| `understand-onboard` | （未声明 description） |

### architecture-engineering（8 个）

| 技能 | 说明 |
|---|---|
| `codebase-design` | Shared vocabulary for designing deep modules. Use when the user wants to design or improve a module's interface, find deepening opportunities, decide where a seam goes, make code more testable or AI-navigable, or when another skill needs the deep-module vocabulary. |
| `domain-modeling` | Build and sharpen a project's domain model. Use when the user wants to pin down domain terminology or a ubiquitous language, record an architectural decision, or when another skill needs to maintain the domain model. |
| `grill-me` | A relentless interview to sharpen a plan or design. |
| `grill-with-docs` | A relentless interview to sharpen a plan or design, which also creates docs (ADR's and glossary) as we go. |
| `grilling` | Interview the user relentlessly about a plan or design. Use when the user wants to stress-test a plan before building, or uses any 'grill' trigger phrases. |
| `improve-codebase-architecture` | Scan a codebase for deepening opportunities, present them as a visual HTML report, then grill through whichever one you pick. |
| `resolving-merge-conflicts` | Use when you need to resolve an in-progress git merge/rebase conflict. |
| `tdd` | Test-driven development. Use when the user wants to build features or fix bugs test-first, mentions "red-green-refactor", or wants integration tests. |

### world-model-method（1 个）

| 技能 | 说明 |
|---|---|
| `world-model-method` | A general-purpose working mode that makes the assistant produce output the "world-model way" — define an explicit goal and cost, build an abstract model of the situation, predict the consequences of several candidate approaches, search/optimize for the best full plan, and only then render the concrete output — instead of generating it token-by-token off the top. This operationalizes Yann LeCun's objective-driven / world-model / planning ideas (JEPA, "A Path Towards Autonomous Machine Intelligence") as a reusable prompt-level method for ANY non-trivial task: important writing, decisions, strategy, problem-solving, system design, planning. Trigger when the user says "用世界模型工作法 / 按 LeCun 那套来做 / 别顺嘴生成，给我规划出来的 / 想清楚再答 / objective-driven / plan it, don't just write it", or when a task is complex enough that deliberation and comparing alternatives clearly beats a first-draft answer. |

### paper-framework-figure-studio-pro（1 个）

| 技能 | 说明 |
|---|---|
| `paper-framework-figure-studio-pro` | Design, generate, critique, select, jointly audit, and finalize publication-ready computer-science research-paper framework figures through a stateful S0-PAPER-FOUNDATION to S7-FINAL-JOINT-AUDIT workflow. Use when Codex needs paper-grounded method overview diagrams, architecture diagrams, pipelines, agent workflows, system/data-flow figures, candidate exploration, formal raster reference candidates, figure-caption symbiosis, style-aware captions, image-visible core algorithm substeps, visible internal mechanism detail for core algorithm/method submodules, semantic icon/arrow/color audit, final figure selection, final figure title/caption/legend/body-reference text, step rewind cleanup, persistent relative-path state, artifact indexing, architecture governance, or final release audits for research figures. |

### karpathy-guidelines（1 个）

| 技能 | 说明 |
|---|---|
| `karpathy-guidelines` | Behavioral guidelines to reduce common LLM coding mistakes. Use when writing, reviewing, or refactoring code to avoid overcomplication, make surgical changes, surface assumptions, and define verifiable success criteria. |

### python-expert（1 个）

| 技能 | 说明 |
|---|---|
| `python-expert` | This skill should be used when the user asks to implement, debug, profile, or optimize Python code for scientific computing, data pipelines, ML models, training loops, evaluation, or reproducible experiments in Paper-gogo Phases 4, 6, 7, or 8. |

## 附加技能合集（`extra-skills/`）

这些是补充的第三方技能合集。**许可证与工作流技能不同**，见 [extra-skills/THIRD_PARTY_NOTICES.extras.md](extra-skills/THIRD_PARTY_NOTICES.extras.md)。

| 技能 | 所属合集 | 说明 |
|---|---|---|
| `academic-paper` | `academic-research-skills` | 12-agent academic paper writing pipeline. 11 modes (full/plan/outline/revision/revision-coach/abstract/lit-review/format-convert/citation-check/disclosure/rebuttal-audit). 6 paper types, 5 citation formats, bilingual abstracts, LaTeX/DOCX-via-Pandoc/PDF output. Style Calibration + Writing Quality Check + Anti-Patterns with IRON RULE markers. Triggers: write paper, academic paper, guide my paper, parse reviews, audit my rebuttal, check my response draft, AI disclosure, 寫論文, 學術論文, 引導我寫論文, 審查意見, 評估回覆. |
| `academic-paper-reviewer` | `academic-research-skills` | Multi-perspective academic paper review with dynamic reviewer personas. Simulates 5 independent reviewers (EIC + 3 peer reviewers + Devil's Advocate) with field-specific expertise. Supports full review, re-review (verification), quick assessment, methodology focus, Socratic guided, and calibration modes. Triggers on: review paper, peer review, manuscript review, referee report, review my paper, critique paper, simulate review, editorial review, calibrate reviewer, reviewer calibration, measure reviewer accuracy. |
| `academic-pipeline` | `academic-research-skills` | Orchestrator for the full academic research pipeline: research -> write -> integrity check -> review -> revise -> re-review -> re-revise -> final integrity check -> finalize. Coordinates deep-research, academic-paper, and academic-paper-reviewer into a seamless 10-stage workflow with mandatory integrity verification, two-stage peer review, and reproducible quality gates. Triggers on: academic pipeline, research to paper, full paper workflow, paper pipeline, end-to-end paper, research-to-publication, complete paper workflow. |
| `deep-research` | `academic-research-skills` | Universal deep research agent team. 13-agent pipeline for rigorous academic research on any topic. 8 modes: full research, quick brief, paper review, lit-review, fact-check, three-way literature scan, Socratic guided research dialogue, and systematic review with optional meta-analysis. Covers research question formulation, Socratic mentoring, methodology design, systematic literature search, source verification, cross-source synthesis, risk of bias assessment, meta-analysis, APA 7.0 report compilation, editorial review, devil's advocate challenges, ethics review, and post-research literature monitoring. Triggers on: research, deep research, literature review, systematic review, meta-analysis, PRISMA, evidence synthesis, fact-check, WHY HOW WHAT papers, 3W literature scan, guide my research, help me think through, 研究, 深度研究, 文獻回顧, 文獻探討, 系統性回顧, 後設分析, 事實查核, 三段式文獻掃描, 引導我的研究, 幫我釐清, 幫我想想, 我不確定要研究什麼, 研究方向, 研究主題. |
| `agent-identifier` | `claude-scholar` | Use when creating or configuring Claude Code agents and their frontmatter. |
| `bug-detective` | `claude-scholar` | This skill should be used when the user asks to "debug this", "fix this error", "investigate this bug", "troubleshoot this issue", "find the problem", "something is broken", "this isn't working", "why is this failing", or reports errors/exceptions/bugs. Provides systematic debugging workflow and common error patterns. |
| `citation-verification` | `claude-scholar` | This skill provides reference guidance for citation verification in academic writing. Use when the user asks about "citation verification best practices", "how to verify references", "preventing fake citations", or needs guidance on citation accuracy. This skill supports ml-paper-writing by providing detailed verification principles and common error patterns. |
| `code-review-excellence` | `claude-scholar` | This skill should be used when the user asks to review a diff or pull request, write review comments, audit code quality, establish review standards, or improve how a team performs code review. |
| `daily-paper-generator` | `claude-scholar` | Use when the user asks to generate daily paper digests on a general topic. This skill supports both arXiv and bioRxiv (or either one), then produces structured Chinese/English summaries for selected papers. |
| `doc-coauthoring` | `claude-scholar` | This skill should be used when the user asks to co-author documentation, draft a proposal, write a technical spec, create a decision doc or RFC, or structure a substantial document through iterative collaboration and reader testing. |
| `git-workflow` | `claude-scholar` | This skill should be used when the user asks to "create git commit", "manage branches", "follow git workflow", "use Conventional Commits", "handle merge conflicts", or asks about git branching strategies, version control best practices, pull request workflows. Provides comprehensive Git workflow guidance for team collaboration. |
| `latex-conference-template-organizer` | `claude-scholar` | Organize messy conference LaTeX template .zip files into clean Overleaf-ready structure. Use when the user asks to "organize LaTeX template", "clean up .zip template", or "prepare Overleaf submission template". |
| `ml-paper-writing` | `claude-scholar` | Write publication-ready ML/AI papers for NeurIPS, ICML, ICLR, ACL, AAAI, COLM. Use when drafting papers from research repos, conducting literature reviews, finding related work, verifying citations, or preparing camera-ready submissions. Includes LaTeX templates, citation verification workflows, and paper discovery/evaluation criteria. |
| `obsidian-literature-workflow` | `claude-scholar` | Use this skill for project-scoped literature review built on Sources/Papers, with synthesis landing in Knowledge, writing handoff in Writing, and the default literature canvas under Maps/literature.canvas. |
| `paper-self-review` | `claude-scholar` | This skill should be used when the user asks to "review paper quality", "check paper completeness", "validate paper structure", "self-review before submission", "audit claims", "check overclaiming", "verify whether results support claims", or mentions systematic paper quality checking. Provides comprehensive quality assurance checklist for academic papers. |
| `publication-chart-skill` | `claude-scholar` | This skill should be used when the user asks for a publication-quality scientific figure or table, wants help choosing the right chart for results, needs a paper-ready pubfig or pubtab workflow, wants a figure + companion table for a results section, wants an Excel sheet turned into publication-ready LaTeX, or wants an existing scientific figure/table reviewed and upgraded. |
| `research-ideation` | `claude-scholar` | This skill should be used when the user asks to "brainstorm research ideas", "use 5W1H framework", "identify research gaps", "conduct gap analysis", "start research project", "conduct literature review", "define research question", "select research method", "plan research", or mentions research project initiation phase. Provides comprehensive guidance for research startup workflow from idea generation to planning. |
| `results-analysis` | `claude-scholar` | This skill should be used when the user asks to "analyze experimental results", "run strict statistical analysis", "compare model performance", "generate scientific figures", "check significance", "do ablation analysis", or mentions interpreting experiment data with rigorous statistics and visualization. It focuses on strict analysis bundles, not Results-section prose. |
| `results-report` | `claude-scholar` | This skill should be used when the user asks to "write an experiment report", "summarize experimental results", "do experiment retrospection", "write a results report", "写实验总结报告", "写实验复盘", or mentions turning completed experiment artifacts into a structured, decision-oriented research report. It assumes strict analysis should come from `results-analysis` first. |
| `review-response` | `claude-scholar` | Systematic review response workflow from comment analysis to professional rebuttal writing. Use when the user asks to "write rebuttal", "respond to reviewers", "draft review response", or "analyze review comments". Improves paper acceptance rates. |
| `verification-loop` | `claude-scholar` | This skill should be used when the user asks to "verify code", "run verification", "check quality", "validate changes", or before creating a PR. Provides comprehensive verification including build, type check, lint, tests, security scan, and diff review. |
| `writing-anti-ai` | `claude-scholar` | This skill should be used when the user asks to "remove AI writing patterns", "humanize this text", "make this sound more natural", "remove AI-generated traces", "fix robotic writing", or needs to eliminate AI writing patterns from prose. Supports both English and Chinese text. Based on Wikipedia's "Signs of AI writing" guide, detects and fixes inflated symbolism, promotional language, superficial -ing analyses, vague attributions, AI vocabulary, negative parallelisms, and excessive conjunctive phrases. |
| `zotero-obsidian-bridge` | `claude-scholar` | Use this skill when Zotero is the literature source of truth and the project KB should receive source notes under Sources/Papers plus project-linked synthesis in Knowledge and Writing. |
| `paper-analyzer` | `paper-craft-skills` | 将学术论文转化为深度HTML长文。6轮强制工作流、代码仓库搜索、公式渲染、Mermaid图表。 3种写作风格，输出可直接分享的精美HTML页面。 |
| `paper-comic` | `paper-craft-skills` | 论文方法图解——用视觉图解彻底讲清楚一篇论文到底做了什么、怎么做的。 自动分析论文核心方法，先推荐封面/概述图/机制细节图的生成方案，必须由用户确认范围、张数、语言、风格后再生成。 支持温暖笔记风和论文框架图风。 |
| `paper-deck` | `paper-craft-skills` | 将论文、技术文章或知识内容制作成高真实感的 AIGC 幻灯片。先做叙事结构和逐页视觉导演，再调用生图模型生成每一页 16:9 slide image，最后合成为 PPTX/PDF。适合论文汇报、组会、公开课、技术分享、商业化研究展示；当用户提到“论文PPT”“AI生成PPT”“不像AI的PPT”“高质感幻灯片”“逐页生图PPT”时使用。 |
| `scipilot-figure-skill` | `scipilot-figure-skill` | SciPilot Skills 家族成员，负责科研数据可视化——但定位不是"画图工具"， 而是"可视化顾问"。先做数据剖析（列类型/样本量/分布/异常值/分组结构/相关性）， 再结合用户的论证目标推荐图型，主动拦截科研画图的经典错误（小样本画均值柱掩盖 分布、双 Y 轴、饼图、Y 轴不当截断、rainbow 色图、把分类点连成折线等），最后 产出 Nature / Science / IEEE / Elsevier / PNAS / 中文核心期刊级别的成图。 覆盖纯数据图：折线、柱状、散点、箱线 / 小提琴、热力图、误差棒、分布图（直方 图 / KDE）、相关性矩阵 / 散点矩阵、多面板组合。技术栈 matplotlib + seaborn + SciencePlots（静态）+ plotly（交互）。中英文双语，中文模式自动配置 Noto Sans CJK / Source Han Sans / SimHei 并修复负号方框，支持中文期刊"宋体正文 + Times New Roman 数字"混排。默认色盲安全配色 + 冗余编码 + 灰度预览。出图后做 "视觉自检闭环"：渲染 PNG 预览→程序自检缺字/文字裁切/刻度重叠→AI 读图复核遮盖 与子图对齐→回改重渲，直到通过。 当用户的任务涉及以下任何情况时主动触发：论文配图、科研画图、数据可视化、 不知道用什么图、怎么展示数据、用什么图好、期刊投稿图、figure、出版级图表、 matplotlib、seaborn、plotly、误差棒、显著性标注、色盲安全配色、矢量图导出、 中文论文图表、多面板。**即使用户只是给一批数据问"这个怎么画"或"用什么图 好"，也应使用本技能——本技能首要能力是"判断该用什么图"，其次才是绘制。** 不做示意图、流程图、架构图。 |

## 汇总

- 内置技能总数：**57**
- 工作流技能组：7
- 附加合集：academic-research-skills、claude-scholar、paper-craft-skills、scipilot-figure-skill

## 未内置的内容

- 图片/PDF 等媒体资产已从内置副本中剥离以控制体积。依赖内置图片的技能（如 `paper-comic`、`paper-deck`）保真度会下降。
- 与工作流无关的技能合集（动画、股票分析、代码图工具、无人值守自动化等）未纳入。
