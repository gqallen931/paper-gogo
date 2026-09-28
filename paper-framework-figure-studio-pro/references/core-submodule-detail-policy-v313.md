# Core Submodule Detail Policy v3.1.3

This policy refines S1-S7 below the existing origin rule, paper-grounding rule, non-poster rule, minimal semantic rule, and figure-caption symbiosis rule.

## Core Rule

A module that carries the paper's core algorithmic or methodological innovation must not be an empty generic box. It needs a visible internal mechanism.

The figure may stay readable, but the visual must show how the core contribution works at a submodule level. If the main architecture diagram cannot hold this detail cleanly, use a side inset, zoom-in panel, cutaway, mini-mechanism strip, or split-panel detail view connected back to the main module.

If the paper spends substantial method prose on an idea, provides formulas for it, or explicitly frames it as an improvement over a prior method/baseline, that idea is a core-innovation candidate until S0/S1 proves otherwise. It must have a clear visual anchor in the image. Caption text may explain the anchor, but cannot be the only place where the innovation appears.

## Non-Droppable Core Substeps

Reorganization and simplification may change layout, grouping, names, and visual order, but they must not delete source-grounded core substeps. When S0/S1 identifies a core module with an internal sequence, split it into non-droppable substeps before S2/S4 planning.

Examples of non-droppable substeps include:

- training/fitting a model before it is used for generation, inference, retrieval, scoring, control, or update;
- sampling/generation/inference after a model has been trained;
- validation/evaluation that produces a score, reward, confidence, or weight;
- update/aggregation/optimization that uses the score or generated output;
- filtering, selection, routing, or thresholding that changes which data or states continue downstream.

A generated-output token alone does not cover the training/fitting substep that produces the generator. An update arrow alone does not cover the training, scoring, or validation substep that justifies the update. A module label such as "diffusion generator", "retriever", "planner", "optimizer", or "aggregator" is not sufficient when the paper's contribution depends on how that module is trained, constructed, evaluated, or connected.

For example, if a paper states that a diffusion model is trained on labeled plus pseudo-labeled data, then sampled to generate data, and later consensus-updated, a faithful figure/candidate contract must preserve all three ideas at the appropriate level: train `psi_i` on `Y_i/P_i`, generate `D_i`, and update/aggregate `psi_i`. These can be shown as a compact mini-chain, an inset, or a small storyboard panel, but they cannot be silently collapsed into only "diffusion produces `D_i`" or only "update `psi_i`".

## First-Round Image Visibility Gate

Formal first-round S5 candidates are not allowed to postpone the paper's core mechanism to a later optimization round. S6 selects and captions an already generated candidate; S7 audits it. Neither S6 nor S7 is a hidden second round for adding missing algorithm semantics.

For every S5 formal candidate, each source-grounded `non_droppable_core_step` must be recoverable from the image pixels themselves through compact labels, symbols, arrows, icons, mechanism chains, panel order, or a connected inset. The pre-image explanation, figure title, caption, and legend may define symbols and explain why the chain matters, but they cannot be the only place where a non-droppable core step appears.

If a step is essential but would clutter the main architecture, S4 must choose a visual containment strategy before S5: mini-chain, side inset, zoom-in, cutaway, local loop, storyboard panel, or a small equation/symbol anchor. If none of those can make the step visible, S4 must mark the candidate incomplete and repair the design instead of generating an image.

## Two Valid Display Modes

For every core innovation submodule, choose one of these modes before image generation:

1. `in_place_internal_detail`: show the internal mechanism inside the main architecture module. Use nested blocks, micro-flow arrows, gates, token/object transforms, loop markers, retrieval/update paths, or formula tokens when essential.
2. `side_inset_detail`: keep the main module compact, then draw a side inset or zoom-in detail panel that exposes the internal mechanism. Connect it to the main module with a clean callout line or numbered anchor.

A candidate may combine both modes only when the result stays readable.

## Mathematical Symbols And Simple Formulas

Internal mechanism detail may include mathematical symbols or a small number of simple formulas when they help reveal the contribution. Use them only when all of these are true:

- the symbol or formula is central to the visible mechanism;
- without this symbol/formula anchor, the figure cannot express the paper's core idea or claimed improvement precisely;
- it is simple enough to understand without reading the full method section;
- it is likely introduced before the architecture figure, or the candidate title/caption/legend can explain it briefly;
- it replaces a long prose explanation rather than adding clutter.

Do not put derivations, multi-line equations, proof fragments, or dense formula explanations into the figure. Put those in the pre-image candidate explanation, caption, legend, or body text.

For symbols such as \(w_i\), prefer visual self-explanation first: place the token near the producing module, connect it with an arrow to the receiving module, and keep the token readable. The caption may add one concise phrase such as "the generated weights \(w_i\) are passed into the aggregation module"; avoid longer explanatory paragraphs unless the user explicitly wants a dense technical figure.

## Required Planning Fields

S1-FIGURE-STRATEGY and S4-CANDIDATE-BRIEF must identify:

- `core_innovation_modules`: the modules that carry the paper's main contribution;
- `core_mechanism_substeps`: the source-grounded internal sequence for each core module;
- `non_droppable_core_steps`: the subset that must remain visible in the S5 image itself when source evidence exists;
- `image_required_core_steps`: the non-droppable steps that must be visible as pixels in every formal candidate;
- `image_core_step_visibility_plan`: for each image-required step, the concrete visual carrier: in-module mini-chain, side inset, zoom-in, cutaway, storyboard panel, symbol/arrow relation, or simple formula token;
- `substep_coverage_plan`: for each non-droppable substep, whether it appears in the main image, side inset, or storyboard panel, plus any caption text that only explains it;
- `internal_mechanism_summary`: what happens inside each module;
- `detail_display_mode`: `in_place_internal_detail` or `side_inset_detail`;
- `detail_visual_tokens`: internal blocks, arrows, formula tokens, simple formulas, gates, state transitions, memory/retrieval paths, optimization loops, or other visual atoms;
- `visible_math_symbols_or_simple_formulas`: which mathematical tokens are visible and why they are understandable before the full method section;
- `symbol_formula_necessity_proof`: a short reason why each visible symbol/formula is necessary; if no such reason exists, do not draw it;
- `claimed_improvement_visual_anchor`: how any explicitly claimed improvement, formula-backed mechanism, or heavily described innovation appears in the image;
- `empty_box_risk`: whether the candidate risks hiding the core contribution in a blank container;
- `caption_support`: which definitions stay in the pre-image explanation/caption rather than inside pixels;
- `caption_only_core_step_forbidden`: true for S5 formal candidates unless source evidence is missing and the risk is recorded.

## What Must Be Visible

When source evidence exists, show at least one of the following for each core innovation module:

- internal data/control flow;
- algorithm step sequence;
- model subcomponent relation;
- token/feature/state transformation;
- optimization, matching, retrieval, selection, or update loop;
- loss/objective signal or formula token if it is part of the mechanism;
- interaction between two or more internal entities.

Do not replace these with a decorative icon, a single unlabeled rectangle, or a generic label such as "Core Module" when the paper provides more detail.

Do not add symbols, variables, equations, or formula-like tokens merely to make the figure look technical. They are valid only when they are necessary anchors for the paper's core idea or improvement and are explained by the caption/legend.

If a core module has multiple non-droppable substeps, at least the sequence relation must remain recoverable in the S5 image itself. The image can use short tokens such as `train -> sample`, `score -> weight`, or `fit -> retrieve`, and the pre-image/caption contract can explain the words. However, the plan must not count a later output token as coverage for an earlier training/fitting/selection substep.

## Review Rule

S3, S6, and S7 must downgrade or reject candidates when a paper's central contribution is represented as an empty or opaque box. A candidate can still be clean and sparse, but the core innovation must have visible internal logic either inside the architecture or in a connected side inset.

S3, S4, S6, and S7 must also run a substep coverage check. Compare the candidate against `non_droppable_core_steps` from S0/S1. If a formal S5 candidate omits one of those substeps from the image body, connected inset, or storyboard panel, it must be marked as a paper-faithfulness failure and repaired or rejected, even if the missing substep is mentioned in the pre-image explanation or caption/legend contract.

If the paper/source material does not contain enough information to draw the internal mechanism, the step must record `missing_core_detail_evidence` and ask for source material or mark the risk. Do not fabricate internal details.
