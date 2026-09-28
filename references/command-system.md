# Paper-gogo command system

Execute only the requested command. If no command is supplied, default to `/建立档案`.

## Intake and diagnosis

### `/建立档案`

Extract research field, target journal, research problem, core method, data, experiments, conclusions, claimed contributions, and major risks. Do not rewrite the manuscript.

### `/审稿人诊断`

Simulate three perspectives:

- Reviewer A: novelty and scientific importance;
- Reviewer B: methods, experiments, statistics, and reproducibility;
- Reviewer C: argument, writing, figures, and journal fit.

Return public author comments, confidential editor-only concerns when appropriate, and a recommendation: reject, major revision, minor revision, or accept. Never invent misconduct; describe only observable warning signs and required verification.

### `/评分`

Apply the 100-point rubric in `SKILL.md`. Explain deductions and list the five highest-value repairs. Do not translate the score into an acceptance probability.

### `/目标期刊`

Assess scope, article type, expected contribution, evidence depth, and presentation requirements using supplied or verified journal guidance. If current guidance has not been supplied, mark it `VERIFY`.

## Problem and novelty

### `/提炼问题`

Use `现象 -> 机制 -> 条件` to produce one main research question and two alternatives. Distinguish the scientific question from the engineering task.

### `/检查创新`

Classify each claimed contribution as:

- domain/scientific innovation;
- methodological or engineering improvement;
- generic technique application;
- presentation-only contribution.

Rewrite viable contributions as `existing failure -> missing domain insight -> proposed design -> verified benefit`. Flag unsupported words such as “first”, “novel”, “SOTA”, and “robust”.

### `/领域偏置`

Identify domain-specific structures, physics, causal relations, temporal cycles, topology, constraints, or operational rules. Map each to a possible inductive bias and a discriminating experiment. Reject generic attention, residual connections, positional encoding, or model replacement as standalone cross-domain novelty.

## Evidence and experiments

### `/修改实验`

Audit data splits, leakage, baselines, fairness, hyperparameters, reproducibility, repeated runs, uncertainty, robustness, efficiency, generalization, and failure analysis. Separate conclusions already supported from those still missing evidence.

### `/设计消融`

For each central claim, specify the ablation, control variables, expected observation, and how each possible outcome changes the claim. Prefer the smallest set of high-discrimination experiments.

### `/分析难例`

Create a domain-appropriate error taxonomy. Test whether multiple representative models fail repeatedly under the same condition. Recommend scenario-based or device/batch/time-based splits to prevent leakage.

### `/证据审计`

Build a table with columns: claim, manuscript location, supporting figure/table/experiment, evidence state, alternative explanation, missing test, and permitted wording.

### `/检查公式`

Check definitions, dimensions, indices, numbering, symbol consistency, assumptions, and derivation completeness. Mark uncertain mathematical validity for verification instead of pretending certainty.

## Section revision

### `/修改标题`

Provide five bounded titles emphasizing scientific problem, method, domain mechanism, application, and a concise conservative option. Recommend one.

### `/修改摘要`

Use: context/problem -> unresolved difficulty -> method and domain rationale -> quantitative results -> bounded contribution. Insert `【请补充】` where required evidence is absent.

### `/修改引言`

Use: puzzle or real-world contradiction -> importance -> current explanations -> unresolved conflict -> proposed perspective -> contributions. Avoid gap-only openings and generic claims of limited prior work.

### `/修改相关工作`

Organize literature as dialogue: dominant explanation -> limitation -> alternative view -> conflict/complementarity -> manuscript position. Preserve citation identifiers.

### `/修改方法`

For every module state: problem, rationale, domain basis, implementation, relationship to other modules, expected effect, and validating experiment. Flag module stacking.

### `/修改结果`

Write: observed result -> relation to hypothesis -> supported explanation -> applicable condition -> anomaly/failure. Do not merely repeat tables.

### `/修改讨论`

Address mechanism, relation to prior work, implications, scope, failure conditions, alternative explanations, and unsupported extrapolations.

### `/修改局限`

State concrete limitations, their effect on current conclusions, and a feasible validation path. Avoid empty future-work language.

### `/修改结论`

Summarize only supported findings. Do not introduce new results or inflate impact.

### `/逐段修改`

Return: original problems, replacement paragraph, key changes, and missing author information.

### `/学术润色`

Improve accuracy, concision, cohesion, and discipline-appropriate style without changing technical meaning or optimizing for AI-detector evasion.

### `/压缩`, `/中译英`, `/英译中`

Preserve terminology, numbers, formulas, citations, and logical strength. Report material omissions made during compression.

## Review and submission

### `/模拟拒稿`

List up to ten likely rejection reasons grouped as fatal, major, and minor. Mark which can be repaired in prose and which require evidence.

### `/投稿前检查`

Check consistency across title, abstract, highlights, graphical abstract, contributions, methods, results, figures, supplements, citations, declarations, and conclusions.

### `/回复审稿人`

For each comment use: appreciation -> interpretation -> action -> evidence -> exact location. If a requested experiment was not performed, state that honestly and offer a bounded alternative analysis or explanation.

## Artifact and execution commands

### `/生成汇报PPT`

Invoke `nature-paper2ppt` after the paper or source-grounded reading notes are available. Produce a real PPTX when tooling is available, not only an outline.

### `/补充引用`

Invoke `nature-citation`. Segment claims, grade support conservatively, verify metadata, and export the requested reference-manager format.

### `/数据可用性`

Invoke `nature-data` to inventory datasets, select access routes, draft the statement, and flag missing repository identifiers.

### `/生成结果图`

Invoke `nature-figure`. If the user has not chosen Python or R, ask that one question and stop.

### `/生成图文摘要`

Generate at most one manuscript-level Graphical Abstract when the target journal requests or permits it. Base it on the verified problem, method, main finding, and boundary; do not treat each正文图说明 as a Graphical Abstract and do not invent unsupported effects.

### `/生成框架图`

Invoke `paper-framework-figure-studio-pro`. Execute only the explicitly requested S0-S7 step and never advance automatically. Use `framework-concept` for Phase 5/9 and a separate `framework-final` state for Phase 13.

### `/代码实现`

Invoke `codebase-design`, then conditionally `tdd`, `python-expert`, and `karpathy-guidelines` according to the implementation task.

### `/诊断实验错误`

Invoke `diagnosing-bugs`; build a red-capable feedback loop before forming a root-cause theory.

## Shared output format

For revision commands, always return:

1. 诊断
2. 修改稿
3. 修改依据
4. 证据边界
5. 下一步
