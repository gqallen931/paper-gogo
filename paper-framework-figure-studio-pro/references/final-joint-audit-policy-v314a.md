# Final Joint Audit Policy v3.1.4a

S7-FINAL-JOINT-AUDIT is the terminal quality gate. It is not the old SVG/PPT delivery stage. It is a text-only semantic audit of the selected S6 image plus figure title, caption, legend, body-reference sentence, and manuscript note.

S7 is a bounded best-practice review, not an endless checking loop. "Multiple checks" means one structured audit with fixed passes, explicit evidence, and a clear verdict. Do not repeatedly re-audit without new input or a changed artifact.

## Required Inputs

- S6 selected final raster image path/display;
- S6 final-selection report;
- S6 draft figure title, caption, legend, body-reference text, and manuscript note;
- S4 candidate contract for the selected image;
- S0 paper foundation report and highest-quality source material;
- any S1/S3 direction-selection notes and recorded user constraints.

## Required Audit Passes

S7 must run all passes and print a compact result table. A pass cannot be marked OK unless the image and caption are evaluated together.

1. Paper fidelity: terminology, contribution claims, module names, input/output semantics, training/inference scope, and constraints do not contradict the paper.
2. Model and algorithm: all non-droppable model blocks, algorithm steps, update/generation/evaluation stages, and core submodule internals are represented by visible anchors plus caption support.
3. Process and arrow semantics: each arrow type has a precise meaning such as data flow, control flow, optimization/update, feedback, retrieval, comparison, or dependency. Arrow direction, multiplicity, and loop meaning must match the paper.
4. Mathematics and symbols: every visible formula, variable, symbol token, operator, score, loss, or metric is supported by the paper and explained either by nearby compact labels or the caption/legend.
5. Color and visual coding: every color, shade, line style, marker, icon family, or region code has a defined meaning. Decorative color with no semantic contract should not be treated as evidence.
6. Icon relevance: entity icons must be tied to the paper's domain and method meaning, not generic filler. Borrowed icon style is allowed; borrowed paper facts are not.
7. Figure-caption symbiosis: caption wording matches the selected visual style, explains the reader path and visual grammar, and carries appropriate details removed from the image.
8. Story fidelity, when applicable: any low-fidelity story or metaphor remains close to the paper, uses common concepts, and has an explicit caption bridge back to the method.
9. Reviewer readiness: a reviewer can understand the paper idea by viewing the image and then reading the caption, without being misled by omitted or invented details.

## Bounded Audit Procedure

Use this fixed procedure:

1. If S7 is being entered again and prior S7 outputs or active records exist, delete only the previous S7 output directory/files and remove prior S7 active artifact/pending-output records; preserve S0-S6 inputs.
2. Record the S7 cleanup event in `state/project-state.json` before executing the new audit.
3. Load the selected S6 bundle and source evidence.
4. Run the nine required audit passes exactly once, unless a file is unreadable or missing.
5. For each pass, record `OK`, `MINOR-TEXT-FIX`, `MAJOR-FIGURE-FIX`, or `BLOCKER`, plus one evidence note.
6. Decide one verdict from the table below.
7. Stop. Do not start another audit cycle unless the user asks to rerun S7 after a repair or provides new evidence.

Do not inflate S7 into an open-ended quality meditation. The audit should be strict, source-grounded, and finite.

## Verdict Rules

- `PASS`: all required passes are OK; mark `S7-FINAL-JOINT-AUDIT complete`; workflow is complete.
- `TEXT-REPAIR`: the image is semantically acceptable but title/caption/legend/body-reference text needs repair; return to S6.
- `IMAGE-REPAIR`: the selected image has fixable but material semantic errors; return to S4/S5/S6.
- `DIRECTION-REPAIR`: the selected direction itself contradicts or badly misses the paper logic; return to S1/S3.

S7 must not approve a figure with unresolved arrow, color, model, algorithm, mathematical, or caption-claim errors.
