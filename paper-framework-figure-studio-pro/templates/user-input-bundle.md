# User Input Bundle Template

Use this bundle to normalize the user's request before each step.

## Source Inputs

- paper/source files:
- LaTeX/Markdown/report/supplement files:
- simple description only:
- target figure type:
- aspect ratio or journal size:
- user preference reference images:

Before explicit S0 entry, normalize only the startup request and return a plan-only reply with a copyable S0 prompt.

After the user explicitly asks to enter/run/execute/start/continue S0-PAPER-FOUNDATION: if the input is only a simple short description, keep S0 lightweight; if the input includes a PDF, LaTeX, full paper text, detailed method/model description, report, or supplement, run paper-only deep reading and print a rich, detailed, accurate paper foundation report.

## Current State

```text
全流程：S0-PAPER-FOUNDATION -> S1-FIGURE-STRATEGY -> S2-SKETCH-EXPLORE -> S3-DIRECTION-SELECT -> S4-CANDIDATE-BRIEF -> S5-CANDIDATE-IMAGE -> S6-FINAL-SELECT
当前 step：<current_step>
默认下一步：<default_next_step 或 已完成>
```

## Step-Specific Inputs

- S1-FIGURE-STRATEGY/S3-DIRECTION-SELECT global exploration: selected sketch directions, reader hook, visual divergence goals.
- S4-CANDIDATE-BRIEF/S5-CANDIDATE-IMAGE local refinement: paper-grounded candidate matrix, method/algorithm/model anchors, required modules and terminology.
- S6-FINAL-SELECT final selection: S5-CANDIDATE-IMAGE candidate paths, paper recheck notes, final selection criteria, and figure text.

## Cleanup Rule

If the user returns to an earlier/current step and that step will be executed, run covered-step cleanup first for every step from `target_step` through the previous `current_step`. Remove covered outputs and active state records. Never delete `state/project-state.json`, `state/`, `inputs/`, user source files, or the skill package.

If the user only asks a historical question, inspect state/history without cleanup.
