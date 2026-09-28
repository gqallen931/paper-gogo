# S3 To S5 Candidate Module

S3 selects the strongest direction from S2 and defines the local-refinement target.

At the end of S3, the next-step prompt for S4 must be split into a shared part and two user-facing branches:

- Shared part: use the S3-selected direction(s), paper facts, registered artifacts, current aspect ratio, and constraints; enter only S4-CANDIDATE-BRIEF; do not generate images or enter S5.
- Branch A: keep the subsequent reference images hand-drawn / sketch-like / low-fidelity in character. If chosen, S4 candidate contracts and S5 prompts must preserve that hand-drawn reference-image direction.
- Branch B: make the subsequent reference images clean, formal, paper-faithful, and figure-caption symbiotic, using clear geometry, semantically relevant icons, clean connectors, short labels, and a style-aware caption plan. This is the default branch. Ease of later SVG/PPT redrawing is only a secondary editability consideration.

If the user does not explicitly choose branch A, treat branch B as selected. The selected branch must affect the second-round candidate text, prompt contracts, visual treatments, caption style, and later S5 image-generation prompts.

S4 prepares formal S5 candidate contracts. The default matrix is 6 candidates: `2 selected directions x 3 visual communication treatments`. The total must not exceed 8.

S4 must list for every candidate:

- candidate_id;
- figure_title;
- figure_sentence;
- pre_image_explanation;
- symbol_visual_legend;
- in_image_text_budget;
- kept_out_of_image;
- visible math symbols or simple formulas;
- symbol/formula necessity proof;
- image_required_core_steps;
- image_core_step_visibility_plan;
- claimed improvement visual anchor;
- arrow/color/icon semantic contract;
- style-aware caption plan;
- paper evidence anchor;
- paper-faithfulness and editability risks.

S5 generates separate formal raster candidate images. It does not generate SVG or PPT artifacts.

Default S5 style is a regular, clean publication schematic image reference. It should use stable module geometry, precise connectors, restrained and meaningful color, paper-relevant icons, short labels, and a caption plan that completes the visual meaning. Do not choose icons or symbols because they are easy to redraw; choose them because they better express the target paper.

Do not default to hand-drawn, whiteboard, sketch-note, comic, painterly, photorealistic, or poster-like rendering. A story-like or metaphorical candidate is optional only when explicitly requested or justified in S4, and must remain paper-faithful, close to the method, based on common concepts, and bridged by caption text.

Do not add unnecessary symbols or formulas. A visible symbol/formula is allowed only when S4 records why the paper's core idea or claimed improvement cannot be expressed precisely without it. Conversely, any heavily described, formula-backed, or explicitly improved core innovation must have a visual anchor in the candidate.

Hard raster image gate for S5/S6: every S5 formal candidate is a target-paper image artifact and must be generated through Image Gen, ChatGPT Create Image, or another approved image-generation API. The accepted file must be `.png`, `.jpg`, `.jpeg`, or `.webp`. S6-FINAL-SELECT must select one of the generated S5 raster images as `s6.selected_reference_final`.

Do not execute S6 in the same reply after S5 image generation.
