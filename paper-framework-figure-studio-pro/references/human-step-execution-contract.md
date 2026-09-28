# Human Step Execution Contract

The workflow is human-in-the-loop. Execute at most one explicitly requested step per user turn.

Active workflow:

```text
S0-PAPER-FOUNDATION -> S1-FIGURE-STRATEGY -> S2-SKETCH-EXPLORE -> S3-DIRECTION-SELECT -> S4-CANDIDATE-BRIEF -> S5-CANDIDATE-IMAGE -> S6-FINAL-SELECT
-> S7-FINAL-JOINT-AUDIT
```

Initial bootstrap gate: if the user only gives an overall diagram goal or provides a paper/PDF without explicitly asking to enter S0, do not execute S0. Provide a plan-only reply and a copyable S0 prompt.

Do not combine adjacent steps in one reply. S0 cannot auto-run S1; S1 cannot auto-run S2; S2 cannot auto-run S3; S3 cannot auto-run S4; S4 cannot auto-run S5; S5 cannot auto-run S6; S6 cannot auto-run S7. S7 is terminal.

Every step response must explicitly close the current stage. Write the completed step name, state that this stage has ended, and state that the next stage has not been executed. Then provide only the next copyable prompt. For S7, write that `S7-FINAL-JOINT-AUDIT complete` only when the bounded audit passes, and state that the whole workflow is complete.

Target-paper sketches and candidates must use the environment image route: Image Gen in Codex, Create Image in ChatGPT web, or another approved API only if neither is available. Generate each image separately.

Every default prompt, fallback prompt, and option prompt must begin with `请按照 paper-framework-figure-studio-pro skill 的要求，根据当前状态和已登记产物，`.
