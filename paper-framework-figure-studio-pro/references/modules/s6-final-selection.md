# S6 Final Selection Module

S6-FINAL-SELECT selects the final image and drafts the figure text package. It is not terminal in v3.1.4a; S7-FINAL-JOINT-AUDIT follows as the bounded final audit. There is no old post-S6 foreground extraction or SVG/PPT handoff.

Inputs:

- S5 candidate image paths;
- S4 candidate contracts;
- S0 paper foundation report and highest-quality source material;
- any S3 direction-selection criteria.

S6 must:

1. Rank the S5 candidate bundles as image-plus-caption-contract units.
2. Recheck paper terminology, modules, arrows, colors, icons, constraints, contribution claims, and core mechanism visibility.
3. Select one S5 raster candidate as the final image.
4. Provide the selected final image path and display the selected final image when the runtime supports local image display.
5. Provide draft final figure title, style-aware caption, legend/symbol notes, body-reference sentence, and manuscript revision note.
6. Record the figure-caption split: what is visible in the image, what is intentionally explained by the caption/legend, and what is omitted.
7. Mark `S6-FINAL-SELECT complete`, explicitly state that S6 has ended and S7 has not been executed, and set default next step `S7-FINAL-JOINT-AUDIT`.

If the final result is not acceptable, recommend returning to S4, S5, or S6 for refinement. Do not offer the old post-S6 SVG/PPT workflow.
