# Figure-Caption Symbiosis Policy v3.1.4a

Use this policy whenever S1-S7 plan, generate, select, or audit a paper framework figure.

## Core Rule

The figure and caption are one explanatory unit. The image should carry the visual cognition path; the caption, legend, and body-reference sentence should complete the meaning without forcing the image to carry every definition, formula explanation, numeric detail, dataset fact, or caveat.

Do not evaluate the image alone when judging final quality. Evaluate the selected image plus title, caption, legend, and body-reference text together.

## Style-Aware Captioning

Caption wording must match the visual style and layout grammar actually used:

- For a mechanism-first schematic, the caption should explain the mechanism path, internal module logic, and why the reader should follow the main flow first.
- For a pipeline or system-flow figure, the caption should name the input/output semantics, stage transitions, and what each arrow class means.
- For a split train/inference or before/after figure, the caption should explicitly distinguish phases and state what changes between panels.
- For an evidence-panel or small-multiple style, the caption may carry target-paper numbers, datasets, metrics, and claim support when putting them in the image body would distract from the method.
- For a story-like or metaphorical sketch, the caption must bridge the story back to the paper mechanism using common concepts that are close to the paper, not a distant analogy.

Generic captions are invalid when the figure has a specific visual rhetoric. The caption must explain the adopted visual grammar well enough that a reader can understand the design choice, arrow meanings, color meanings, symbol roles, and evidence/caveat layer.

## Caption-Only Evidence Anchor

The vector-library builder's `caption_only_evidence_anchor` pattern contributes this transferable rule:

- Keep paper-specific facts, numbers, datasets, metrics, claim support, and caveats in the caption when they would overload or distract from the core method drawing.
- Borrow only layout grammar, grouping rhythm, reader path, connector treatment, and caption strategy from references.
- Never transfer source-reference paper facts, labels, claims, metrics, datasets, symbols, equations, or numeric results into the target-paper caption.
- Use target-paper evidence to support caption claims; if evidence is unavailable, mark the uncertainty instead of inventing a claim.

## Image Text Reduction

Move these items out of image pixels by default:

- long prose definitions;
- equation derivations and formula meanings;
- dataset names, exact numbers, metrics, and implementation caveats unless visually essential;
- detailed symbol explanations;
- reviewer-facing claim support.

Keep these items visible in the image when they are necessary visual anchors:

- main modules and core mechanism steps;
- input/output roles;
- short labels or tokens that make arrows and groups readable;
- one or two compact symbols/formulas only when they are essential to understanding the mechanism;
- color/shape distinctions that the caption can then explain.

Caption cannot hide a non-droppable core step that must be visible. If the paper contribution depends on a step, the figure needs a visual anchor for it, and the caption can explain that anchor.

## S7 Joint Evaluation Questions

S7 must ask and answer:

1. Does the caption describe the actual selected figure style and reader path, not a generic diagram?
2. Do the caption and legend explain arrow, color, icon, symbol, and formula semantics precisely?
3. Are any image omissions intentionally covered by caption text, and are those omissions safe?
4. Are all caption claims supported by the target paper rather than by borrowed reference examples?
5. Does the figure-caption bundle preserve the paper's model, algorithm, process, and mathematical meaning?
6. Would a reviewer understand the figure better by reading the caption after looking at the image?
