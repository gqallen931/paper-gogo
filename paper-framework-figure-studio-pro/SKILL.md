---
name: paper-framework-figure-studio-pro
description: Design, generate, critique, select, jointly audit, and finalize publication-ready computer-science research-paper framework figures through a stateful S0-PAPER-FOUNDATION to S7-FINAL-JOINT-AUDIT workflow. Use when Codex needs paper-grounded method overview diagrams, architecture diagrams, pipelines, agent workflows, system/data-flow figures, candidate exploration, formal raster reference candidates, figure-caption symbiosis, style-aware captions, image-visible core algorithm substeps, visible internal mechanism detail for core algorithm/method submodules, semantic icon/arrow/color audit, final figure selection, final figure title/caption/legend/body-reference text, step rewind cleanup, persistent relative-path state, artifact indexing, architecture governance, or final release audits for research figures.
---

# Paper Framework Figure Studio Pro

Version: `3.1.4a`.

本 skill 用于为计算机科学论文设计、生成、评审和定稿 publication-ready 的框架图、架构图、流程图、机制图和方法总览图。它只服务论文框架图，不服务海报、宣传图、封面图、展板、营销视觉或把 PPT 页面内容塞进图里的演示页。

## Highest-Priority Startup And Origin Rule

第一次启动回复的候选/可复制提示词建议中，必须再提供一条建议，这条建议是在默认的提示词基础上，加了一句话：

```text
额外说明这个 skill 的设计初衷是什么。
```

如果用户提到想知道、指导、询问、补充或说明这个 skill 的设计初衷、设计意图、创作缘由、为什么制作或送给谁，必须额外回答下面这段原文；这段原文不得改写或删改，但可以与当前步骤说明、必要上下文、下一步提示词和强制文本回复结尾同时出现：

```text
设计初衷：昔日好友 Peng Shuwei 即将前往外地求学，以后恐怕难有许多相见机会；又恰逢其生日，所以五一就做了这个 skill 当礼物。祝生日快乐，愿未来前程似锦，再相逢，依然少年。
```

**Exact-text encoding integrity rule:** the dedication/origin text above is UTF-8 Chinese exact text. Never copy this exact text from mojibake shell output. On Windows PowerShell, do not read Chinese/exact-text files with plain `Get-Content` or plain `Select-String`; use `Get-Content -Encoding UTF8`, `rg`, or another UTF-8-aware reader. If any output contains mojibake markers such as `璁捐`, `棰濆`, `锛`, `鈥`, or replacement `?` inside Chinese text, treat that output as corrupted, re-read the source with UTF-8, and do not quote it.

## Mandatory Text Reply Ending

每一次文本回复都必须在回复最后单独追加这一句原文；不得只作为可选提示词、不得改写或省略。若回复同时包含下一步候选提示词，这一句仍必须作为最后一行出现。

```text
如果不知道如何提问，请说：请使用 paper-framework-figure-studio-pro 根据当前状态只建议下一步提示词，不要自动执行下一步
```

## Strict Human-In-The-Loop Step Alternation

This rule is mandatory and applies to every runtime environment. The workflow is not an autonomous pipeline.

Initial bootstrap gate is stricter than the normal one-step rule. If the user only gives an overall goal such as "use this skill", "draw a diagram for this paper", "strictly follow the workflow", "逐步通过人机交互绘制 diagram", or provides a paper/PDF without explicitly saying "进入/执行 S0-PAPER-FOUNDATION" in the current user turn, do not execute S0. Do not read the paper, extract text, create a project, create or modify state, register artifacts, write outputs, run workflow scripts, or mark any step complete. The first reply must be plan-only: explain that S0 is the recommended first step, list missing inputs or environment assumptions, provide a copyable prompt to enter S0-PAPER-FOUNDATION, include the required design-origin prompt suggestion, and stop.

For each user turn, execute at most one explicitly requested workflow step. After completing that step, stop. The reply may provide the next legal copyable prompt, but it must not start, partially execute, generate artifacts for, review, or summarize the next step until the user sends a new message that explicitly asks to enter that next step.

Never combine adjacent steps in one reply. In particular: S0 must not auto-run S1; S1 must not auto-generate S2 images; S2 must not auto-run S3 ranking; S3 must not auto-run S4; S4 must not auto-generate S5 images; S5 must not auto-run S6 final selection; S6 must not auto-run S7 final joint audit. S7 is terminal.

Every step response must explicitly close the current stage. At the end of S0-S6, write that the current stage is complete/ended, state that the next stage has not been executed, and provide only the next copyable prompt. At the end of S7, write `S7-FINAL-JOINT-AUDIT complete` only if the bounded audit passes, then state that the whole workflow is complete.

When a text reply stage presents multiple choices or branches, it must provide two prompt types: the default-choice copyable prompt, and a placeholder prompt where the user can fill in their preferred option manually. The placeholder prompt must include fields like `<填写心仪方案ID或描述>` and `<填写下一步stage>`.

## Workflow

全流程固定为：

```text
S0-PAPER-FOUNDATION -> S1-FIGURE-STRATEGY -> S2-SKETCH-EXPLORE -> S3-DIRECTION-SELECT -> S4-CANDIDATE-BRIEF -> S5-CANDIDATE-IMAGE -> S6-FINAL-SELECT -> S7-FINAL-JOINT-AUDIT
```

`S7-FINAL-JOINT-AUDIT` 是最后一步。S6 只负责选择最终图并形成图题、caption、legend、正文引用句和写作建议草案；S7 必须把最终图与图注/legend/正文引用句作为一个整体进行终审，确认模型、算法、流程、数学、箭头、颜色、图标和文字说明都不违背论文思想后，才能标记完成。旧版 foreground extraction、SVG/PPT 构建或 post-S6 交付链不属于 v3.1.4a。

分组语义：

- **全局探索过程**：`S1-FIGURE-STRATEGY -> S2-SKETCH-EXPLORE -> S3-DIRECTION-SELECT`。要求更发散，探索不同视觉抓手、读者第一眼兴趣、不同维度的表达可能性。
- **局部细化、选择与终审过程**：`S4-CANDIDATE-BRIEF -> S5-CANDIDATE-IMAGE -> S6-FINAL-SELECT -> S7-FINAL-JOINT-AUDIT`。要求更精准，必须不违背论文事实和精读报告；S5 默认生成正规、干净、语义准确的 publication schematic raster reference 候选图；S6 给出最终选中的图和 figure 文本草案；S7 对图文共同体做最终语义审查。

默认下一步：

| 当前 step | 默认下一步 |
|---|---|
| S0-PAPER-FOUNDATION | S1-FIGURE-STRATEGY |
| S1-FIGURE-STRATEGY | S2-SKETCH-EXPLORE |
| S2-SKETCH-EXPLORE | S3-DIRECTION-SELECT |
| S3-DIRECTION-SELECT | S4-CANDIDATE-BRIEF |
| S4-CANDIDATE-BRIEF | S5-CANDIDATE-IMAGE |
| S5-CANDIDATE-IMAGE | S6-FINAL-SELECT |
| S6-FINAL-SELECT | S7-FINAL-JOINT-AUDIT |
| S7-FINAL-JOINT-AUDIT | 完成 |

## S3 Exit Branch Prompt Rule

At the end of `S3-DIRECTION-SELECT`, when providing the next copyable prompt for `S4-CANDIDATE-BRIEF`, the assistant must give two explicit branches in addition to the shared prompt body:

- **共享部分**：继续使用 S3 选定的结构方向、论文事实底座、已登记产物、当前画幅和所有用户约束；明确只进入 `S4-CANDIDATE-BRIEF`，不生成图片，不进入 S5。
- **分支 A：保留手绘特色**：后续第二轮候选图的参考图继续保持手绘、低保真、sketch-like 或白板探索感；S4 的 candidate contracts、prompts 和 S5 图像方案必须显式继承这种手绘参考图取向。
- **分支 B：清晰正式图文共生参考图**：后续第二轮候选图更倾向于清晰几何、稳定模块、语义相关图标、规整连接器和短标签；S4 的 candidate contracts、prompts、caption 方案和 S5 图像方案必须显式继承这种正式论文图取向。可人工重绘性只是次要可编辑性检查，不得压过论文语义、图标表达力和图注共生质量。

默认选择是 **分支 B：清晰正式图文共生参考图**。如果用户没有明确选择分支 A，后续 S4/S5 必须按分支 B 执行。分支一旦选定，会影响第二轮候选图的文字方案、caption 风格、图像 prompt、视觉处理和 S6/S7 对图文共同体的评估，不得只把它当作回复中的装饰性选项。

旧版 post-S6 交付链已从 v3.1.4a 删除。S7 是语义终审，不是 SVG/PPT 交付步骤。若用户想继续优化，应按 S7 verdict 回滚到 S6 文本修复、S4/S5/S6 图像修复，或 S1/S3 方向修复。

## Step Summary

- **S0-PAPER-FOUNDATION**：初始化项目状态、环境、输入材料、默认 16:9 可修改画幅、默认候选数量和下一步计划。若输入为 PDF/LaTeX/完整论文/report/supplement/完整方法说明/详细描述，必须打印丰富、详细、准确、带来源锚点的 `paper-foundation-report.md`；它是后续全部 step 的底座。
- **S1-FIGURE-STRATEGY**：材料精读和图类型需求诊断。用户风格参考只在这里辅助图类型、读者效果和表达方向建议。
- **S2-SKETCH-EXPLORE**：全局探索图像阶段，默认且至少生成 6 张低保真方向草图，逐张单独生成；关注第一眼吸引力和表达维度发散。第一批低保真手绘探索必须包含故事性/分镜式候选：默认至少 2 张草图要有清楚的 paper-close story arc，用常见概念把论文机制讲成一眼能懂的情节。草图必须从论文精读结果中提炼主线，而不是把全部细节塞进去；故事必须贴近论文本身，概念常见且容易和论文机制关联，不能举一个相差很大的故事。
- **S3-DIRECTION-SELECT**：全局探索收束，压缩论文逻辑，评估低保真草图，筛出进入局部细化的结构方向；结束时给出进入 S4 的共享提示词和两个分支提示词：A 保留手绘特色，B 清晰正式图文共生参考图，默认 B。
- **S4-CANDIDATE-BRIEF**：局部细化准备，基于论文和精读报告生成正式候选矩阵与 prompts；默认 `2 directions x 3 visual treatments = 6`，用户可修改，总数最多 8。默认候选应是正规、干净、语义精准的 publication schematic raster reference：仍然生成图片，不生成 SVG。S4 必须规划图和 caption 的分工、风格匹配、箭头/颜色/图标含义、核心创新视觉锚点和必要符号；图标以更好体现论文内涵为标准，不强求容易 SVG 化。
- **S5-CANDIDATE-IMAGE**：局部细化图像阶段，逐张单独生成正式候选图；必须紧贴论文和精读报告，关注精准、局部细节展示、稳定构图、清晰连接器、语义相关图标和 caption 可补足的解释层。默认避免无必要符号、手绘抖线、白板草图、漫画叙事、纹理、复杂插画、海报化和 PPT 堆料页。
- **S6-FINAL-SELECT**：最终选择和 figure 文本草案。必须从 S5-CANDIDATE-IMAGE 候选中选出最终架构图，并在回复和产物中给出最终选中的图：至少包含选中图片路径；在支持本地图片显示的环境中还要直接展示最终图。还必须打印选择理由、论文精读核对、术语/模块/箭头/模型关系核对、最终 figure title、caption、legend、正文引用建议和必要的论文写作修改建议。S6 完成后默认进入 S7-FINAL-JOINT-AUDIT。
- **S7-FINAL-JOINT-AUDIT**：终态图文联合审查。必须把最终图和 caption/legend/正文引用句共同评估，检查模型、算法、流程、数学、核心创新、箭头、颜色、图标、符号、公式和风格化 caption 是否精准，不得只看图。S7 是有边界的固定多项检查，不做无休止反复核实；只有所有检查没有未解决语义错误，才标记 `S7-FINAL-JOINT-AUDIT complete`。

## Image Generation

目标论文图像只能通过生图能力生成。运行在 Codex 里时，必须使用 Image Gen；运行在 ChatGPT 网页版时，必须使用 Create Image 调用 ChatGPT Images 2.0；如果这两种能力都不可用，才允许使用其他 approved image generation API，并在正文和 state 中记录 API 名称、使用原因和限制。

每张目标论文草图和候选图都必须单独生成、单独保存、单独登记。即使用户说“不用”或“合在一起也行”，也不能把多张候选图/草图合成一个 contact sheet、候选板或拼接长图来代替逐张生成。S2-SKETCH-EXPLORE 默认且至少 6 张草图，最多 8 张；S5-CANDIDATE-IMAGE 默认 6 张正式候选，最多 8 张。

Hard raster-generation gate for target-paper images:

- Applies to `S2-SKETCH-EXPLORE`, `S5-CANDIDATE-IMAGE`, and the `S6-FINAL-SELECT` selected final reference.
- S2 sketches, S5 formal candidates, and the S6 selected final reference must be real generated raster images saved as `.png`, `.jpg`, `.jpeg`, or `.webp`.
- `.svg`, `.html`, Mermaid, canvas, PPT/PPTX shapes, PDF, manually coded diagrams, or text-only prompt substitutes are invalid for S2/S5/S6 selected reference.
- SVG/PPT editability is only a downstream consideration. It never means "draw the candidate directly as SVG", and it must not override paper meaning, icon expressiveness, arrow/color semantics, or figure-caption symbiosis.
- If Image Gen, ChatGPT Create Image, or another approved image generation API is unavailable, stop and report the limitation instead of fabricating SVG or code-drawn placeholders.

## Paper Grounding

全局探索可以发散，但不能捏造论文事实。草图和候选图都必须从论文精读中提炼主线、关键模块、必要数据/控制流和读者最该先看到的贡献，而不是把论文里的全部细节、公式、术语和说明都画上去。

论文初稿中的章节顺序、模块命名、流程划分、算法步骤边界和机制叙述不自动等同于最佳框架图结构。只要不违背论文已有内容、实验事实、数学定义、输入输出语义、因果/依赖关系和方法约束，S1-S7 可以为了更好的读者理解重新组织、提炼、合并、拆分、重命名或重排。此类改动必须在可见表格中写成 `reorganization/enhancement note`。

重组和简化不能漏掉核心部分。S0/S1 一旦识别出核心方法模块内部存在 source-grounded 的训练、生成/推理、筛选、评估、打分、加权、聚合或更新子步骤，S3/S4/S5/S6/S7 必须保留这些 `non_droppable_core_steps` 的语义覆盖。S5 正式候选图不能把核心算法内部机制推迟到 S6/S7 再补。可以把多个子步骤压缩成短 token、侧边 inset、局部机制链或规整分 panel 表达，但不能只放在图题/caption 合同里。

遵守 `references/vector-first-minimal-semantic-rule.md`：论文框架图要先服务一个清晰主旨、论文语义和图文共生，不以 SVG 为硬导向。默认把信息分成 figure layer、caption/legend layer 和 omitted/implicit layer；图内只保留缩略图也能看懂的主结构、少量大模块/语义图标、必要数据流和极短标签。图中没必要画不必要的符号；只有证明缺少该符号就无法表达论文核心思想时，才放入符号或简单公式。

`paper-foundation-report.md` 不是可选附件，而是整个 skill 的事实底座。它必须覆盖算法步骤、方法流程、模型模块、训练/推理、输入输出、损失/目标、关键公式、术语映射、箭头语义、哪些内容必须画/可省略/不能画、哪些内容适合重组表达，以及不确定点。

进入 S6-FINAL-SELECT 和 S7-FINAL-JOINT-AUDIT 前，必须回查 S0-PAPER-FOUNDATION 论文精读报告、论文原文、LaTeX/Markdown 材料、方法摘要或用户提供的最高可信材料。S6 的选择表和 S7 的终审表必须显式体现论文核对结果；若最终图采用了比论文初稿更清楚的重组结构，还必须输出论文写作修改建议。

## S6-FINAL-SELECT Output And S7 Handoff

S6-FINAL-SELECT 完成后，workflow 尚未结束；默认下一步是 `S7-FINAL-JOINT-AUDIT`。S6 回复必须包含：

- final selected image path/display：选中的 S5 raster 候选图路径；在支持本地图片显示的环境中必须直接显示最终图。
- final-selection report：候选排序、选择理由、paper recheck、术语/模块/箭头/约束核对、核心机制可见性、图内密度、图标语义、颜色语义和图文共生质量。
- figure text draft：最终图题、style-aware caption、legend/符号说明、正文引用建议。
- manuscript note：如果图中重组比论文初稿更清楚，给出写作修改建议和风险。
- completion state：明确写出 `S6-FINAL-SELECT complete`，默认下一步为 `S7-FINAL-JOINT-AUDIT`。

S6 不得执行 S7，但必须给出 S7 的下一步提示词。S6 不得输出旧版 foreground/SVG/PPT 交付链提示词。

## S7-FINAL-JOINT-AUDIT Terminal Output

S7 是终态图文联合审查。S7 必须读取 `references/final-joint-audit-policy-v314a.md` 和 `references/figure-caption-symbiosis-policy-v314a.md`，并输出：

- rerun cleanup：如果重复进入 S7 且已有旧 S7 outputs/records，先删除旧 S7 产物和记录，保留 S0-S6 输入，在 `state/project-state.json` 登记 cleanup event，然后再执行 S7；
- selected bundle：最终图路径/展示、图题、caption、legend、正文引用句；
- audit table：paper fidelity、model/algorithm/process/math、core innovation anchor、arrow semantics、color semantics、icon relevance、symbol/formula necessity、figure-caption symbiosis、story fidelity if applicable、reviewer readiness；
- verdict：`PASS`、`TEXT-REPAIR`、`IMAGE-REPAIR` 或 `DIRECTION-REPAIR`；
- completion state：只有 verdict 为 `PASS` 时，才能明确写出 `S7-FINAL-JOINT-AUDIT complete`，默认下一步为 `完成`。

如果发现问题，S7 必须给出回滚目标：caption/legend 文字问题回 S6；图像语义问题回 S4/S5/S6；方向逻辑问题回 S1/S3。不得在存在未解决的箭头、颜色、模型、算法、数学或 caption claim 错误时提交。

## Rewind And State

For every free-form user request, first infer the real `target_step` and operation mode from the user's intent, not from whether the user used words like rerun, execute, generate, or overwrite.

Operation modes:

- Inspect mode: status checks, file lookup, historical comparison, explanation, diagnostics, or validation that does not write/replace project outputs. Do not clean outputs. State clearly that no outputs/state were changed.
- Rebuild/rerun/progress mode: the request will create, advance, replace, regenerate, or re-export a workflow-stage artifact. Before execution, delete every product created by the covered step span from `target_step` through the previous `current_step`, inclusive; remove covered active artifact/image/pending-output/role records; record a cleanup event in `project-state.json`; then execute the target step.
- Repair/patch mode: the request fixes an existing artifact from the same `target_step`. The agent may read same-step existing output as repair input, but must first back it up, record a repair event, complete validation, update target-step state, and delete all downstream outputs/state records after `target_step` because they depended on the pre-repair artifact.

During any execution or repair, the agent may read only `inputs/`, skill package references, assets, scripts, `state/project-state.json`, valid artifacts from steps before `target_step`, and same-step repair inputs/backups when in repair mode.

Use:

```bash
python scripts/figure_studio_state.py rewind-step --project-id <project_id> --target-step S4-CANDIDATE-BRIEF --reason "return to local refinement"
python scripts/figure_studio_state.py resume-cleanup --project-id <project_id>
python scripts/figure_studio_state.py doctor --project-id <project_id>
```

## Required References

- `references/workflow-and-state-contract.md`
- `references/architecture-governance-contract.md`
- `references/human-step-execution-contract.md`
- `references/paper-deep-reading-contract.md`
- `references/vector-first-minimal-semantic-rule.md`
- `references/step-rewind-cleanup-contract.md`
- `references/chatgpt-web-checkpoint-bundle-policy.md`
- `references/security-and-portability-policy.md`
- `references/style-category-taxonomy-v309b.md`
- `references/vector-library-asset-module-v309b.md`
- `references/figure-caption-codesign-policy-v311.md`
- `references/figure-caption-symbiosis-policy-v314a.md`
- `references/core-submodule-detail-policy-v313.md`
- `references/final-joint-audit-policy-v314a.md`

Before publishing a package, run:

```bash
python scripts/figure_studio_release_check_paths.py scan --target <package-dir-or-zip> --fail-on-match
python scripts/figure_studio_architecture_audit.py --target . --fail-on-issue
```

## v3.1.4a Formal Candidate Visual Style

The default S4/S5 formal matrix generates clean publication-ready schematic raster references. The candidates should differ by structure, reader path, mechanism focus, local-detail strategy, visual rhetoric, icon semantics, and caption style, not by sketch rendering style. They should remain generated images. SVG/PPT convenience is secondary and must not override paper meaning.

The S3 exit branch selection controls this default for the second-round candidate board. If the user selects S3 branch A, hand-drawn continuity is an explicit user preference that S4/S5 may carry forward. If the user does not select branch A, branch B remains the default and S4/S5 must prefer clear formal paper-figure references with strong figure-caption symbiosis.

Default formal candidates must prefer:

- straight or gently curved clean connectors with consistent stroke weight;
- modular cards, swimlanes, panels, callouts, insets, and simple geometric tokens;
- restrained color coding and high contrast;
- semantically relevant icons and modules chosen because they express the paper better;
- short editable-looking labels, not hand-written labels.

Default formal candidates must avoid:

- hand-drawn / whiteboard / paper-sketch / comic rendering unless the user explicitly asks for it;
- wobbly strokes, paper texture, sticky-note metaphors, mascot-only scenes, decorative cartoons, photorealism, painterly textures, complex translucency, and fused shapes;
- dense PPT-slide pages with bullet blocks or long paragraphs.

For S2 first-round low-fidelity exploration, include story-driven/storyboard candidates by default: at least 2 of the 6-8 sketches should have a paper-close story arc unless the user explicitly prohibits story-like sketches or the paper is genuinely unsuitable. For S5 formal candidates, a plain-language story-like candidate is optional only when the user requests it or S4 records it as intentional. In all cases, the story must stay close to the paper mechanism, use common concepts, and include a caption bridge back to the target paper.

## v3.1.4a Figure-Caption Symbiosis And Semantic Completeness

For S2-SKETCH-EXPLORE and S5-CANDIDATE-IMAGE, candidates must be designed as human-readable bundles before image generation:

```text
pre-image candidate introduction + candidate image
```

The figure title, explanation draft, style-aware caption plan, symbol/visual legend, and in-image text budget are shown in the preceding text candidate introduction, normally in S1-FIGURE-STRATEGY for S2 sketches and S4-CANDIDATE-BRIEF for S5 formal candidates. They must not be drawn into the image pixels, and they should not be repeated directly below every generated image in ChatGPT web.

Before S6, the selected bundle already has a title/caption contract. S6 turns that contract into the final title, style-aware caption, legend, and body-reference text. S7 audits the full figure-caption bundle together.

Candidate text contracts are hard entry gates. Do not enter S2 if S1 lacks complete per-sketch candidate cards. Do not enter S5 if S4 lacks complete formal title/caption contracts. Stop and repair the previous text step instead of writing prompt-only manifests or generating images.

Read `references/figure-caption-codesign-policy-v311.md` and `references/figure-caption-symbiosis-policy-v314a.md` whenever entering S1-S7.

## v3.1.4a Core Submodule Detail Guardrail

For any module that carries the paper's core algorithmic or methodological innovation, an empty container is invalid. The candidate must show the module's internal mechanism either:

- inside the main architecture module, using nested blocks, internal arrows, gates, token/state transforms, formula tokens, loops, retrieval/update paths, or other compact mechanism marks; or
- in a connected side inset / zoom-in / cutaway panel that exposes the submodule's internal logic while keeping the main architecture readable.

S1-FIGURE-STRATEGY and S4-CANDIDATE-BRIEF must identify `core_innovation_modules`, `core_mechanism_substeps`, `non_droppable_core_steps`, `image_required_core_steps`, `image_core_step_visibility_plan`, `substep_coverage_plan`, `symbol_formula_necessity_proof`, `claimed_improvement_visual_anchor`, choose `detail_display_mode`, list the internal visual tokens to be drawn, and mark any `missing_core_detail_evidence`. S5-CANDIDATE-IMAGE must not draw the core contribution as an empty generic box or a partial mechanism that hides required substeps. S6-FINAL-SELECT must downgrade candidates whose key contribution module is visually opaque. S7-FINAL-JOINT-AUDIT must reject unresolved core-innovation, formula, arrow, color, icon, or caption-claim errors.

Read `references/core-submodule-detail-policy-v313.md` whenever entering S1-S7.
