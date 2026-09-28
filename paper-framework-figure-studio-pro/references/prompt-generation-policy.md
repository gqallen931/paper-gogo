# Prompt Generation Policy

S2 and S5 image prompts must be grounded in the preceding text-step candidate contracts.

S2 prompts:

- generate separate raster sketches;
- explore broad reader hooks and layout grammars;
- use sparse text and simple symbols;
- use story/metaphor only when it is close to the paper and easy to connect back through caption text;
- avoid inventing paper facts.

S5 prompts:

- generate separate formal raster candidates;
- default to clean publication schematic image references;
- use paper-relevant icons, precise connectors, meaningful color, short labels, and a style-aware caption plan;
- include symbols/formulas only when S4 records why the core idea cannot be expressed without them;
- avoid default hand-drawn, whiteboard, sketch-note, comic, decorative cartoon, painterly, photorealistic, or poster-like rendering;
- include the `image_core_step_visibility_plan`, `claimed_improvement_visual_anchor`, `symbol_formula_necessity_proof`, and arrow/color/icon semantic contract.

Hard gate: do not enter S2 without complete S1 sketch cards. Do not enter S5 without complete S4 formal candidate contracts.

Prompt-only manifests are not a substitute for generated raster images.
