# Response Prompt Options Policy

Each text reply should show the current workflow position:

```text
全流程：S0-PAPER-FOUNDATION -> S1-FIGURE-STRATEGY -> S2-SKETCH-EXPLORE -> S3-DIRECTION-SELECT -> S4-CANDIDATE-BRIEF -> S5-CANDIDATE-IMAGE -> S6-FINAL-SELECT -> S7-FINAL-JOINT-AUDIT
当前 step：<current_step>
默认下一步：<default_next_step 或 已完成>
```

The next-step prompt is copyable guidance only. It must not auto-run the next step.

When a text stage provides multiple choices, show both a default-choice prompt and a placeholder prompt where the user can fill in the preferred option. The placeholder prompt must include explicit fields such as `<填写心仪方案ID或描述>` and `<填写下一步stage>`.

When the current step is `S3-DIRECTION-SELECT`, the next-step prompt for `S4-CANDIDATE-BRIEF` must include a shared part plus two explicit branches:

- Branch A: continue the second-round reference images with hand-drawn / sketch-like character.
- Branch B: prefer clean formal paper-figure references with precise semantics, paper-relevant icons, and style-aware caption plans. SVG/PPT editability is secondary.

Branch B is the default if the user does not choose. The branch selection must carry into S4 candidate wording and S5 image prompts.

Target-paper images must follow the environment image route. Every sketch and candidate is generated separately.

Every stage response must state that the current stage has ended and that the next stage has not been executed. After S6, provide the S7-FINAL-JOINT-AUDIT next prompt. After S7, provide completion status only if the bounded joint audit passes; otherwise provide the repair route.
