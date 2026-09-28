---
name: paper-gogo
description: This skill should be used when the user asks to "修改我的论文", "按审稿人视角诊断论文", "启动论文工作流", "检查创新性或实验充分性", "设计消融实验", "润色SCI论文", or prepare a manuscript, submission package, or reviewer response through a staged evidence-first workflow.
---

# Paper-gogo v6.0

## Goal

Orchestrate an evidence-first academic-paper workflow from problem diagnosis to reviewer response. Work backward from reviewer expectations while preserving the truth of the research.

## Boundaries

- Do not fabricate experiments, data, citations, novelty, author contributions, or completed revisions.
- Do not turn correlation into causation or expand conclusions beyond the evidence.
- Do not promise acceptance or assign pseudo-precise acceptance probabilities.
- Do not optimize for detector evasion. Improve clarity, specificity, and authorial voice instead.
- Do not treat replacing one generic model with another as cross-domain innovation.
- Do not rewrite the entire manuscript when a scoped command was requested.

## Default behavior

1. Read the manuscript and supplied project materials.
2. If the user gives a slash command, execute only that command.
3. If no command is given, run `/建立档案` and stop after producing the project card.
4. Separate every issue into:
   - `表达问题`: can be fixed directly in prose;
   - `论证问题`: needs restructuring or explanation;
   - `证据问题`: needs analysis, experiments, data, or source verification.
5. Label substantive claims with one evidence state:
   - `SUPPORTED`: supported by supplied evidence;
   - `INFERRED`: plausible interpretation, explicitly marked;
   - `VERIFY`: requires author or source verification;
   - `MISSING`: required evidence is absent.
6. End each task with no more than five prioritized next actions.

## Reviewer-first workflow

Use the detailed 18-phase workflow in `paper-workflow-v6.md`. The major quality gates are:

| Gate | Reviewer question | Required result |
|---|---|---|
| G0 Scope | Is this in scope and ethically reviewable? | project card and target-journal fit |
| G1 Problem | Is the problem important and non-trivial? | phenomenon-mechanism-condition problem statement |
| G2 Novelty | Is novelty domain-driven and literature-grounded? | claim map and novelty verdict |
| G3 Design | Can the study test its central claims? | claim-to-experiment matrix |
| G4 Evidence | Do results support every major claim? | evidence audit and failure analysis |
| G5 Manuscript | Is the argument coherent and reproducible? | reviewer audit and revision ledger |
| G6 Submission | Are journal fit, files, citations, and disclosures ready? | submission checklist |

A gate may be `PASS`, `PASS WITH CONDITIONS`, or `FAIL`. A failed gate must produce a repair plan; prose polishing cannot override it.

Before executing any Phase, load `references/phase-skill-routing.md`. Route to one primary bundled skill; load auxiliary skills only when their trigger condition is met. Record the invoked skill and produced artifact in the phase log.

Instruction precedence is: this file's boundaries, then `paper-workflow-v6.md` gates, then phase routing, then inherited v5 wording. Never use a legacy phase sentence to bypass truth, evidence, ethics, or journal-policy verification.

## Command routing

Load `references/command-system.md` whenever the user gives a slash command or asks what commands are available.

Common routes:

- Intake: `/建立档案`, `/目标期刊`, `/评分`
- Problem and novelty: `/提炼问题`, `/检查创新`, `/领域偏置`
- Evidence: `/修改实验`, `/设计消融`, `/分析难例`, `/证据审计`
- Writing: `/修改标题`, `/修改摘要`, `/修改引言`, `/修改相关工作`, `/修改方法`, `/修改结果`, `/修改讨论`, `/修改结论`, `/逐段修改`
- Review and submission: `/审稿人诊断`, `/模拟拒稿`, `/投稿前检查`, `/回复审稿人`

## Core review model

Use this default 100-point diagnostic rubric. Scores are decision aids, not publication predictions.

| Dimension | Weight | Test |
|---|---:|---|
| Novelty | 30 | new problem, mechanism, constraint, method, or evidence |
| Evidence sufficiency | 30 | controls, baselines, ablations, uncertainty, generalization, failure cases |
| Scientific and practical importance | 20 | meaningful problem and credible impact |
| Writing and presentation | 10 | coherent argument, precise language, readable figures |
| Journal fit | 10 | scope, depth, article type, and workload |

For interdisciplinary AI papers, test whether the inductive bias comes from the domain. Map each contribution as:

`real-world failure -> domain mechanism/constraint -> model or study design -> discriminating evidence -> bounded conclusion`

## Output contract for revision commands

1. `诊断`: problems and severity.
2. `修改稿`: complete replacement text for the requested scope.
3. `修改依据`: what each major change fixes.
4. `证据边界`: SUPPORTED / INFERRED / VERIFY / MISSING.
5. `下一步`: three to five prioritized actions.

Preserve citation identifiers, formulas, variables, numerical values, and terminology unless the user explicitly authorizes changes. Mark unverifiable citations as `VERIFY`; never guess their content.

## Bundled resources

- `paper-workflow-v6.md`: authoritative workflow and phase gates.
- `references/command-system.md`: slash-command definitions and output rules.
- `references/reviewer-checklist.md`: reviewer checks, decision logic, and evidence audit.
- `references/phase-skill-routing.md`: executable Phase-to-skill mapping, entry gates, and fallbacks.
- `nature-skills/`: bundled reading, writing, polishing, citation, data, and response skills.
- `code-understanding/`: bundled code-understanding skills.
- `architecture-engineering/`: bundled design, testing, and review skills.
- `paper-framework-figure-studio-pro/`: bundled paper-framework figure workflow.
- `code_assets/`: reusable experiment and project templates.

Use optional external skills only after verifying they are installed as directories with a readable `SKILL.md`. A ZIP archive alone is not an installed skill.
