# S7 Final Joint Audit Module

S7-FINAL-JOINT-AUDIT is terminal. It audits the selected final figure and its text package together before final submission. It is bounded: run the fixed audit once, give one verdict, then stop.

Inputs:

- S6 selected image path/display;
- S6 final-selection report;
- S6 title, caption, legend, body-reference sentence, and manuscript note;
- S4 selected candidate contract;
- S0 paper foundation report and highest-quality source material.

S7 must:

1. If entering S7 again, delete prior S7 outputs/records, preserve S0-S6 inputs, and record a cleanup event in state before auditing.
2. Re-read the paper foundation and the selected S6 bundle.
3. Evaluate the image and caption/legend/body text together, not image-only.
4. Check model, algorithm, process, mathematical symbols, formula anchors, module boundaries, data/control/update arrows, colors, icons, and labels against the paper.
5. Confirm that the caption matches the selected figure style and explains the actual visual grammar, reader path, arrows, colors, symbol roles, and any intentionally omitted details.
6. Confirm that caption-only facts, values, datasets, metrics, and claims are target-paper supported and not borrowed from reference figures.
7. For story-like sketches or candidates, confirm the story is close to the paper and uses common concepts that readers can easily associate with the method.
8. Print one verdict: `PASS`, `TEXT-REPAIR`, `IMAGE-REPAIR`, or `DIRECTION-REPAIR`.
9. If and only if all checks pass, mark `S7-FINAL-JOINT-AUDIT complete` and default next step `done` / `完成`.

If S7 fails, do not submit the figure. Give the exact return step and the concrete repair reason.
