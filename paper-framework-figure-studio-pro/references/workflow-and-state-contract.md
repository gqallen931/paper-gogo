# Workflow And State Contract

The workflow is fixed:

```text
S0-PAPER-FOUNDATION -> S1-FIGURE-STRATEGY -> S2-SKETCH-EXPLORE -> S3-DIRECTION-SELECT -> S4-CANDIDATE-BRIEF -> S5-CANDIDATE-IMAGE -> S6-FINAL-SELECT -> S7-FINAL-JOINT-AUDIT
```

Phase semantics:

- Foundation: `S0-PAPER-FOUNDATION`.
- Global exploration: `S1-FIGURE-STRATEGY -> S2-SKETCH-EXPLORE -> S3-DIRECTION-SELECT`.
- Local refinement, selection, and final audit: `S4-CANDIDATE-BRIEF -> S5-CANDIDATE-IMAGE -> S6-FINAL-SELECT -> S7-FINAL-JOINT-AUDIT`.

Default next-step table:

| Step | Default next |
|---|---|
| S0-PAPER-FOUNDATION | S1-FIGURE-STRATEGY |
| S1-FIGURE-STRATEGY | S2-SKETCH-EXPLORE |
| S2-SKETCH-EXPLORE | S3-DIRECTION-SELECT |
| S3-DIRECTION-SELECT | S4-CANDIDATE-BRIEF |
| S4-CANDIDATE-BRIEF | S5-CANDIDATE-IMAGE |
| S5-CANDIDATE-IMAGE | S6-FINAL-SELECT |
| S6-FINAL-SELECT | S7-FINAL-JOINT-AUDIT |
| S7-FINAL-JOINT-AUDIT | done |

`S7-FINAL-JOINT-AUDIT` is the final workflow step. S6 selects the final raster image and drafts figure text. S7 evaluates the selected image plus title/caption/legend/body-reference text together and then either passes the bundle or routes a bounded repair. Agents must not propose or execute the old foreground extraction, SVG/PPT construction, or post-S6 delivery chain.

S2 sketches, S5 candidates, and the S6 selected final reference are target-paper image artifacts. They must be generated raster images (`.png`, `.jpg`, `.jpeg`, or `.webp`) produced by Image Gen, ChatGPT Create Image, or another approved image-generation API.

SVG/HTML/Mermaid/canvas/PPT/PDF/code-drawn substitutes are invalid for those target-image roles. SVG/PPT editability is only a downstream consideration, not a primary design target and not a change in output modality.

S6-FINAL-SELECT must select one final S5 raster candidate, provide the selected final image path and display it when the runtime supports local image display, then draft the figure title, style-aware caption, legend, body-reference text, and manuscript note. S6 must explicitly close the stage and hand off to S7.

S7-FINAL-JOINT-AUDIT is terminal. It must run a bounded joint audit of the selected image and figure text, including paper fidelity, model/algorithm/process/math correctness, arrow semantics, color semantics, icon relevance, symbol/formula necessity, figure-caption symbiosis, story fidelity when applicable, and reviewer readiness.
