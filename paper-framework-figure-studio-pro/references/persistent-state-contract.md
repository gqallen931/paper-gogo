# Persistent State Contract

The project state is the source of truth for the S0-PAPER-FOUNDATION to S7-FINAL-JOINT-AUDIT workflow.

Required top-level state groups include workflow plan, step runs, artifact role registry, active artifact roles, artifacts, pending outputs, runtime environment, user preference status, image generation events, cleanup policy, S6 final selection policy, and S7 final joint audit policy.

The active step sequence is:

```text
S0-PAPER-FOUNDATION -> S1-FIGURE-STRATEGY -> S2-SKETCH-EXPLORE -> S3-DIRECTION-SELECT -> S4-CANDIDATE-BRIEF -> S5-CANDIDATE-IMAGE -> S6-FINAL-SELECT -> S7-FINAL-JOINT-AUDIT
```

Canonical artifact roles:

- `s0.paper_foundation_report`
- `s1.figure_strategy`
- `s2.primary_sketch`
- `s3.direction_selection`
- `s4.candidate_brief`
- `s5.primary_candidate`
- `s6.final_selection`
- `s6.selected_reference_final`
- `s6.figure_text`
- `s7.final_joint_audit`

S6 is complete only when the selected final S5 raster candidate is recorded and the final-selection report includes title, style-aware caption, legend, body-reference text, manuscript note, and S7 handoff. S7 is complete only when the bounded joint audit passes and records `s7.final_joint_audit`.

State validation must reject path traversal, local absolute paths in state fields, non-raster target-paper image substitutes for S2/S5/S6 selected reference roles, and secret-like keys.
