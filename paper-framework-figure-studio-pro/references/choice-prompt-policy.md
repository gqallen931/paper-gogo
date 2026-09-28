# Choice Prompt Policy

Every default prompt, fallback prompt, and option prompt for Chinese users must begin with:

```text
请按照 paper-framework-figure-studio-pro skill 的要求，根据当前状态和已登记产物，
```

Each text reply must end with:

```text
如果不知道如何提问，请说：请使用 paper-framework-figure-studio-pro 根据当前状态只建议下一步提示词，不要自动执行下一步。
```

Prompts are suggestions only. They never authorize automatic execution of the next step.

When a text-only stage offers multiple user-facing choices, it must provide:

- a default-choice copyable prompt using the recommended/default option;
- a placeholder-choice copyable prompt that lets the user fill in their preferred option, for example `我选择：<填写心仪方案ID或描述>` and `请按这个选择进入下一步：<填写下一步stage>`。

The placeholder prompt is required even when a default is clearly recommended.

Default prompt targets:

- S0-PAPER-FOUNDATION: initialize state and paper/source foundation.
- S1-FIGURE-STRATEGY: diagnose figure strategy and S2 sketch cards.
- S2-SKETCH-EXPLORE: generate separate raster exploration sketches.
- S3-DIRECTION-SELECT: choose the strongest direction.
- S4-CANDIDATE-BRIEF: prepare formal candidate contracts.
- S5-CANDIDATE-IMAGE: generate separate formal raster candidate images.
- S6-FINAL-SELECT: select the final image and draft style-aware figure text.
- S7-FINAL-JOINT-AUDIT: run bounded joint audit of the selected image and figure text.

S3-DIRECTION-SELECT special next-prompt rule: when S3 ends, the S4 prompt must contain one shared part and two branches. The shared part must preserve S3 choices, paper facts, registered artifacts, aspect ratio, and constraints while entering only S4. Branch A means the later reference figures keep hand-drawn / sketch-like character. Branch B means the later reference figures prefer clean formal paper-figure design, precise semantics, paper-relevant icons, and style-aware caption planning. Branch B is the default if the user does not choose, and the chosen branch must affect S4 candidate contracts, S5 image prompts, and S6/S7 figure-caption evaluation.

Every step response must state that the current stage has ended and that the next stage has not been executed. After S6, offer the S7-FINAL-JOINT-AUDIT prompt. After S7, offer completion only if verdict is PASS; otherwise offer the selected repair route.
