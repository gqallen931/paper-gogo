# State Banner Template

Every text reply must start with this visible banner before any analysis, table, report, or prompt:

```text
全流程：S0-PAPER-FOUNDATION -> S1-FIGURE-STRATEGY -> S2-SKETCH-EXPLORE -> S3-DIRECTION-SELECT -> S4-CANDIDATE-BRIEF -> S5-CANDIDATE-IMAGE -> S6-FINAL-SELECT -> S7-FINAL-JOINT-AUDIT
当前 step：<current_step>
默认下一步：<default_next_step 或 已完成>
```

If state is not loaded, write `unknown` as the current step and initialize or load `figure-studio-runs/<project_id>/state/project-state.json`.

After the main body, print key reports and decision prompts inline. Do not only save reports to files.

Every step must explicitly state that the current stage has ended. For S0-S6, also state that the next stage has not been executed. For S7, state that the whole workflow is complete only after the bounded joint audit passes.
