# Figure Caption Co-Design Policy

Candidates are planned as bundles:

```text
pre-image candidate introduction + generated raster candidate image
```

In v3.1.4a, the stronger rule is figure-caption symbiosis: the figure and caption are one explanatory unit. The caption is not a generic afterthought. It must match the adopted figure style, reader path, visual grammar, arrow/color/icon/symbol semantics, and any evidence layer intentionally kept out of the image.

S1 must introduce every planned S2 sketch candidate before image generation. S4 must introduce every planned S5 formal candidate before image generation.

Required S2 fields:

- candidate_id
- figure_title
- pre_image_explanation_draft
- symbol_visual_legend
- in_image_text_budget
- caption_support_note
- reader_understanding_test

Required S5 fields:

- candidate_id
- figure_title
- figure_sentence
- pre_image_explanation
- symbol_visual_legend
- in_image_text_budget
- visible_math_symbols_or_simple_formulas
- kept_out_of_image
- reader_understanding_test
- caption_risk_or_missing_context
- image_required_core_steps
- image_core_step_visibility_plan

The title, explanation, legend, method prose, and symbol definitions normally stay outside image pixels. The image should carry the cognitive map; S6 figure text carries definitions, caveats, equation meanings, and long explanations.

Caption wording must be style-aware. A mechanism-first schematic caption should describe the mechanism path; a pipeline caption should describe stage transitions and arrow classes; a split train/inference caption should separate phases; an evidence-panel caption may carry target-paper facts, metrics, and caveats that would distract inside the image; a story-like caption must bridge the story back to the paper's own method with close, common concepts.

Borrowed reference layouts can contribute caption strategy, grouping rhythm, reader path, and evidence placement, but their paper-specific facts, numbers, labels, symbols, claims, datasets, and metrics must not transfer into the target-paper caption.

For S5 formal candidates, caption/legend text cannot be the only carrier of a non-droppable core algorithm step. If a step is required to understand the paper contribution, it must appear in the image body, a connected inset, zoom/cutaway, compact mechanism panel, or another visible carrier. The caption may explain the visible step, but it may not replace it.

S5 defaults to clean publication schematic raster references. These are images, not SVGs. SVG/PPT approximation is only a downstream editability consideration; semantic fidelity, style-caption fit, and paper-grounded icon/arrow/color meaning are more important than forcing a vector-oriented look.

S6-FINAL-SELECT drafts the selected bundle into final figure title, caption, legend, body-reference text, and manuscript note. S7-FINAL-JOINT-AUDIT then evaluates that full bundle together and decides whether it is ready, needs text repair, needs image repair, or needs direction repair.
