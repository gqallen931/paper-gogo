# Prompt Template

All default prompts, option prompts, and fallback prompts must begin with the skill prefix for Chinese users:

```text
请按照 paper-framework-figure-studio-pro skill 的要求，根据当前状态和已登记产物，
```

Every text reply must end with this exact standalone line:

```text
如果不知道如何提问，请说：请使用 paper-framework-figure-studio-pro 根据当前状态只建议下一步提示词，不要自动执行下一步。
```

When a text-only stage presents multiple choices, provide both:

```text
【默认方案提示词】请按照 paper-framework-figure-studio-pro skill 的要求，根据当前状态和已登记产物，<使用默认推荐方案进入下一步...>
```

```text
【自填方案提示词】请按照 paper-framework-figure-studio-pro skill 的要求，根据当前状态和已登记产物，我选择：<填写心仪方案ID或描述>。请按这个选择进入：<填写下一步stage>。不要执行其他未指定 stage。
```

## S2-SKETCH-EXPLORE Image Prompt

Generate low-fidelity global-exploration sketches for the target paper framework figure. Use the environment image route: Image Gen in Codex, Create Image / ChatGPT Images 2.0 in ChatGPT web, or another approved image API only if neither is available. Generate each sketch as a separate image call and save/register it separately.

Hard modality gate: every S2 sketch must be a generated raster image file (`.png`, `.jpg`, `.jpeg`, or `.webp`). Do not output SVG code, vector diagrams, HTML, Mermaid, canvas, PPT/PPTX shapes, PDF, or prompt-only placeholders as sketches. Editability means only that the raster sketch stays readable and not fused; it does not permit drawing the sketch directly as SVG.

Default canvas aspect ratio is 16:9 unless changed by the user. Default and minimum count is 6 diverse sketches; maximum is 8. Keep the sketches broad and eye-catching across different reader hooks, visual metaphors, layout grammars, reader paths, density/detail levels, visual communication styles, and first-glance emphasis. The first low-fidelity hand-drawn exploration batch must include story-driven/storyboard sketches by default: at least 2 of the 6-8 sketches should have a clear paper-close story arc unless the user explicitly forbids story-like sketches or the paper is genuinely unsuitable. They may be more divergent than later steps, but they must not invent paper facts.

Use the paper reading to distill the big framework, not to draw every paper detail. Use large clear icons, module silhouettes, rough grouping, simple data-flow symbols, and at most short module/step titles. Avoid dense labels, long text, unnecessary symbols/formulas, tiny icons, and tangled connectors. Only include a symbol or formula if the paper's core idea cannot be expressed without that anchor.

For each story/metaphor sketch, keep the story close to the target paper's actual mechanism and use common concepts that readers can easily connect back to the method. Record the caption bridge; do not use a distant story just for visual novelty.

Hard gate: if the preceding S1 output does not contain complete S2 candidate cards with `candidate_id`, `figure_title`, `pre_image_explanation_draft`, `symbol_visual_legend`, `in_image_text_budget`, `caption_support_note`, and `reader_understanding_test` for every planned sketch, stop before writing prompts or generating images and repair S1 first.

After the images, print only a compact candidate-ID/filename list, state that S2 has ended and S3 has not been executed, the S3 next-step prompt, and the unsure-user fallback. Do not execute S3 in the same reply.

## S5-CANDIDATE-IMAGE Prompt

Generate formal paper-framework candidates for local refinement. Use the environment image route and generate every candidate separately. Do not create a contact sheet or stitched candidate board.

Hard modality gate: every S5 candidate must be a generated raster image file (`.png`, `.jpg`, `.jpeg`, or `.webp`). Do not output SVG code, vector diagrams, HTML, Mermaid, canvas, PPT/PPTX shapes, PDF, or prompt-only placeholders as candidates. The S6 selected final reference must be one of these generated raster image candidates.

Default canvas aspect ratio is 16:9 unless changed by the user. Default count is 6 candidates as a `2 selected directions x 3 visual communication treatments` matrix unless the user changed the matrix.

All default S5 formal candidates should be generated raster images in a clean publication-ready schematic style. Use stable modular geometry, consistent stroke weights, clear module bodies, clean connector grammar, restrained meaningful color coding, paper-relevant icons, short labels, and predictable reading order. They should look like serious research-paper diagram references whose caption completes the meaning. Do not generate SVG in S5, and do not choose icons merely because they are easy to redraw.

Do not use hand-drawn, whiteboard, paper-sketch, sketch-note, comic, sticky-note, or storyboard rendering as the default S5 style. A plain-language story-like candidate may appear only when the user explicitly requests it or S4 records it as an intentional optional candidate; even then it should stay close to the paper's own logic, use common concepts, and include a caption bridge, not a decorative cartoon or SVG output.

Keep paper meaning fixed across all candidates, but do not mechanically mirror the manuscript draft's current organization. Vary visual grammar, focal hierarchy, panel rhythm, label density, local-detail display, style treatment, callout strategy, reader path, and non-contradictory organization.

Design with semantic clarity in mind: prefer paper-relevant icons, module cards, swimlanes, panel groups, clean insets, short editable-looking labels, and controlled data-flow relations. SVG/PPT approximation is secondary. Avoid painterly textures, photo-realism, complex translucency, tiny decorative details, elaborate backgrounds, exaggerated cartoon rendering, wobbly strokes, and fused shapes.

Every S5 prompt must include the S4 `image_core_step_visibility_plan`, `claimed_improvement_visual_anchor`, `symbol_formula_necessity_proof`, and arrow/color/icon semantic contract. Name the visual carrier for each image-required core step, for example a three-token mini-chain inside a module, a connected inset, a small loop, or a mechanism panel. If S4 lacks `image_required_core_steps` or `image_core_step_visibility_plan`, stop and repair S4 before generating images.

After the images, print only a compact candidate-ID/filename list, state that S5 has ended and S6 has not been executed, the S6 next-step prompt, and the unsure-user fallback. Do not execute S6-FINAL-SELECT in the same reply.

## S6-FINAL-SELECT Prompt

Use only after S5-CANDIDATE-IMAGE has generated and registered the formal raster candidates.

S6-FINAL-SELECT selects the final image and drafts the figure text package. It is not terminal in v3.1.4a. It must not execute S7, but it must hand off to S7-FINAL-JOINT-AUDIT. It must not print or execute any old post-S6 foreground/SVG/PPT handoff prompt.

Required S6 output:

1. Review all S5 candidates as bundles: S4 contract plus generated image.
2. Recheck the paper foundation report and highest-quality paper/source material for terminology, modules, arrow relations, method constraints, core contributions, and non-contradictory reorganization.
3. Rank candidates with explicit reasons, including paper fidelity, core-submodule detail visibility, image-required core-step coverage, readability, figure-vs-caption split, style-aware caption readiness, stable focal hierarchy, target-size readability, icon relevance, arrow/color semantics, and symbol/formula necessity.
4. Select one final S5 raster candidate as the final figure reference and provide its project-relative path.
5. Display the selected final image when the runtime supports local image display; the final selected image must be visible in the S6 response or explicitly unavailable with reason.
6. Provide final figure text: title, style-aware caption, legend/symbol notes, and body-reference sentence(s).
7. Provide manuscript revision suggestions when the selected figure uses a clearer organization than the draft paper text.
8. Mark `S6-FINAL-SELECT complete`; state that S6 has ended and S7 has not been executed; default next step is `S7-FINAL-JOINT-AUDIT`.

## S7-FINAL-JOINT-AUDIT Prompt

Use only after S6-FINAL-SELECT has selected the final raster image and drafted title/caption/legend/body-reference text.

If entering S7 again, first delete prior S7 outputs and remove prior S7 records from state, preserve S0-S6 inputs, write a cleanup event to `state/project-state.json`, and only then execute S7.

Run one bounded best-practice joint audit. Evaluate the selected image plus caption/legend/body-reference text together. Do not run an endless review loop.

Required S7 output:

1. Show the selected bundle: image path/display, title, caption, legend, body-reference sentence.
2. Audit paper fidelity, model/algorithm/process/math correctness, core innovation anchors, arrow semantics, color semantics, icon relevance, symbol/formula necessity, figure-caption symbiosis, story fidelity if applicable, and reviewer readiness.
3. For each audit pass, mark `OK`, `MINOR-TEXT-FIX`, `MAJOR-FIGURE-FIX`, or `BLOCKER` with one source-grounded evidence note.
4. Give one verdict: `PASS`, `TEXT-REPAIR`, `IMAGE-REPAIR`, or `DIRECTION-REPAIR`.
5. Mark `S7-FINAL-JOINT-AUDIT complete` and whole workflow complete only when verdict is `PASS`.
