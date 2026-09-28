# Changelog

## 3.1.4a

- Added terminal `S7-FINAL-JOINT-AUDIT` as a bounded final figure-caption audit, not an SVG/PPT delivery step.
- Reframed S6 as final image selection plus style-aware title/caption/legend/body-reference drafting, followed by S7.
- Made figure-caption symbiosis explicit: caption and image are evaluated together, and captions must match the selected visual style, reader path, arrow/color/icon semantics, and evidence layer.
- Extracted caption-only evidence-anchor knowledge from `paper-vector-library-builder-final-library.zip`: target-paper facts, numbers, datasets, metrics, and caveats can live in the caption when they would distract inside the figure; reference-paper facts must not transfer.
- Demoted SVG/PPT approximation from default design driver to secondary editability consideration.
- Required semantically relevant icons chosen for paper meaning rather than ease of SVG redrawing.
- Tightened symbol/formula use: do not draw unnecessary symbols unless the core idea cannot be expressed without them.
- Required clear visual anchors for heavily described, formula-backed, or explicitly improved core innovations.
- Added a default requirement that the first S2 low-fidelity hand-drawn batch include paper-close story-driven/storyboard candidates, with close-to-paper constraints for every story/metaphor sketch.
- Added S7 rerun cleanup: delete prior S7 outputs/records, preserve S0-S6 inputs, record cleanup in state, then rerun S7.
- Required every stage response to explicitly state that the stage has ended and that the next stage has not been executed.
- Required multi-choice text stages to provide both a default-choice prompt and a placeholder prompt where users can fill in their preferred option.

## 3.1.4

- Promoted the v3.1.3 package to version 3.1.4.
- Shortened the active workflow to S0-PAPER-FOUNDATION through terminal S6-FINAL-SELECT.
- Moved final figure text into S6-FINAL-SELECT: title, caption, legend, body-reference text, and manuscript note.
- Clarified that S6-FINAL-SELECT must output the final selected image path/display and that the workflow ends there with no S7 step.
- Changed S5 formal candidate defaults from hand-drawn/sketch-note/storyboard to clean publication schematic raster references that are easier to approximate later with SVG/PPT primitives.
- Added an in-place S3 exit prompt rule while keeping version `3.1.4`: after S3, the S4 next prompt must include a shared section plus two branches, hand-drawn continuity or default SVG/PPT-approximable refinement, and the selected branch must affect S4/S5 text and image plans.
- Removed post-S6 delivery scripts, templates, and prompt handoffs from the active package.
