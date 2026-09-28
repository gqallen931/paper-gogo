# Style Category Taxonomy v3.0.9b

This reference merges the style/category systems extracted from:

- `paper-vector-library-builder-final-library.zip`
- `paper-vector-figure-skills-v0.6-deepread-reference-index.zip`

Use it when S1-S4 need richer style choices and when S4 builds the formal candidate matrix. It is a design taxonomy, not a source-paper fact base.

## Source A: Final Vector Library Taxonomy

The final library is grounded in 541 audited papers, 3239 figure-story-architecture links, 2805 final reference rows, 691 canonical icons, 2313 icon aliases, 501 PPT primitives, 31 design patterns, 31 layout patterns, and 100 paper-derived motif records.

### Figure Subtypes

- `evidence_chart`
- `graph_or_network`
- `retrieval_flow`
- `data_or_embedding_map`
- `qualitative_example`
- `method_architecture`

### Layout Grammars

- `small_multiples_or_chart_panel`
- `node_edge_graph_layout`
- `query_context_retrieval_answer_flow`
- `map_or_distribution_panel`
- `example_grid_or_before_after_panel`
- `left_to_right_modular_pipeline`

### Architecture Topologies

- `graph_network`
- `retrieval_augmented_flow`
- `train_infer_split`
- `loop_or_feedback`
- `pipeline_or_modular_system`
- `unknown_caption_only`

### Figure Roles

- `support_empirical_claim_or_ablation`
- `explain_graph_structure_or_dependency_flow`
- `explain_retrieval_augmented_reasoning_flow`
- `explain_dataset_distribution_or_representation_space`
- `show_qualitative_behavior_or_case`
- `explain_method_or_system_architecture`

### Density And Symbol Levels

- Density: `low`, `medium`, `high`
- Formula/symbol burden: `none_or_caption_only`, `low`, `medium`
- Vector buildability scores present in the source index: `0.82`, `0.52`, `0.4`

### Borrowable Design Pattern Families

- reviewer-first grouping and reading order
- caption anchors that separate visual strategy from paper-specific facts
- small-multiple comparison rhythm
- claim-to-chart captioning
- evidence placement
- module grouping
- stage-output chips
- typed arrows for data/control flow
- distribution overview
- semantic grouping
- legend strategy

### Style Token

`iclr_clean_flat_modular_v1` is the starter token. It means:

- vector-first rebuild;
- reviewer-first information grouping;
- clean academic figure language;
- caption carries paper-specific claims;
- do not transfer source-paper facts, exact numbers, or unsupported labels.

## Source B: v0.6 Deep-Read Reference Index Taxonomy

The v0.6 package contributes a deep-read-backed retrieval and transfer system. Its main point is that style selection should not be surface-only: it should consider paper story, architecture topology, claim-evidence logic, reader path, and vector buildability.

### Paper Story Signature Axes

- `reader_question`
- `problem_type`
- `gap_type`
- `core_insight`
- `contribution_type`
- `story_arc`: `problem_to_method`, `mechanism_first`, `example_first`, `architecture_first`, `evidence_first`, `failure_to_guardrail`, `comparison_first`
- `desired_reviewer_effect`
- `main_claims`
- `evidence_roles`
- `caption_burden`
- `allowed_reorganization`

### Model Architecture Signature Axes

- `model_family`
- `modality`
- `topology_family`
- `module_roles`
- `training_flow`
- `inference_flow`
- `data_flow_pattern`
- `control_flow_pattern`
- `feedback_loops`
- `loss_or_objective_signals`
- `memory_retrieval_tool_use`
- `main stage outputs`
- `expected_module_count`
- `complexity_level`

### Figure Signature Axes

- `figure_subtype`
- `paper_slot`
- `reader_path`
- `layout_grammar`
- `panel_rhythm`
- `module_grouping_strategy`
- `stage-output visibility`
- `icon_landmarks`
- `arrow_grammar`
- `evidence_treatment`
- `symbol_density`
- `text_density`
- `style_family`
- `vector_buildability`
- `ppt_editability`

### Preference Style Dimensions

- palette;
- layout rhythm;
- shape language;
- icon style;
- arrow grammar;
- typography;
- dimensionality;
- abstraction level;
- density;
- evidence treatment;
- tone;
- positive and negative preferences;
- vector risk;
- transfer strength: `weak`, `medium`, `strong`, `locked`.

### Reference Retrieval Groups

- `direct_story_architecture_match`
- `architecture_match_style_different`
- `story_match_architecture_different`
- `visual_style_match_only`
- `evidence_treatment_reference`
- `do_not_use_due_to_mismatch`

## v3.0.9b Merged Style Lenses

Use these lenses to make the first formal candidate matrix less single-track. A default `2 directions x 3 styles` matrix still produces six candidates, but the three style slots should be selected from this menu according to paper need.

| Lens ID | Style Lens | Best For | Typical Layout/Asset Hints |
|---|---|---|---|
| `schematic_precision` | Schematic precision / formal architecture | methods, systems, architecture boundaries | modular pipeline, typed arrows, exact interfaces |
| `editorial_clarity` | Clean editorial flat / minimal line-art | intro or method overview needing fast comprehension | sparse modules, strong hierarchy, low text density |
| `mechanism_snapshot` | Mechanism intuition snapshot | explaining why the core idea works | central mechanism, zoom callout, cause-effect arrows |
| `evidence_infographic` | Mini-evidence infographic | linking method to result or ablation | side evidence card, metric badge, small-multiple cue |
| `graph_reasoning` | Graph/network reasoning | GNNs, dependency graphs, causal/relational logic | node-edge graph layout, edge semantics, compact legend |
| `retrieval_flow` | Retrieval/RAG/query-context-answer flow | RAG, agents, tool use, memory, search | query-context-retrieval-answer grammar |
| `data_embedding_map` | Data/embedding/distribution map | representations, manifolds, latent spaces, datasets | map/distribution panel, clusters, arrows, legend |
| `qualitative_walkthrough` | Example or before/after walkthrough | showing one case through the method | grid, storyboard, before/after strip |
| `train_infer_split` | Training vs inference split | papers with different optimization/deployment paths | split lanes, shared model core, output chips |
| `loop_feedback` | Loop/feedback/self-improvement cycle | agents, RL, iterative refinement, self-training | cyclic path, feedback port, iteration marker |
| `taxonomy_matrix` | Taxonomy/matrix overview | high-density survey or category map when explicitly requested | matrix grid, grouped cells, caption-heavy support |
| `premium_scientific` | Premium scientific illustration, vector-safe | high first-glance appeal without posterization | restrained color, landmark icons, separable foreground |
| `plain_language_hand_drawn_storyboard` | Hand-drawn whiteboard / lightly narrative everyday-example storyboard | making a complex method understandable by analogizing the algorithm/model category into a faithful everyday example | 3-5 sketch panels, hand-drawn arrows, simple characters/objects, sticky-note labels, model-detail mini-chain, story-to-method mapping |

## Selection Rule

For S2, sample broad directions across subtype, layout grammar, reader path, and first-glance hook.

For S4, choose style lenses by paper need:

1. Pick the active structural directions from S3.
2. For each direction, choose style lenses that differ in visual rhetoric, density, reader path, and evidence treatment.
3. Prefer at least one reviewer-first low-density option.
4. Include one mechanism/evidence option only when the target paper has a mechanism or evidence anchor worth showing.
5. Keep the default first formal S5 matrix in clean publication schematic raster style. Hand-drawn, whiteboard, sketch-note, comic, or story-like treatments are optional only when the user explicitly requests them or S4 explicitly justifies them.
6. Record `style_lens_id`, `source_taxonomy_refs`, `icon_family_hints`, and `transfer_boundary` in the candidate brief.

For any optional story-like candidate, S4 must provide the story-to-method mapping and explain why it helps the reader. The image must remain a generated raster candidate grounded in paper modules, symbols, sample types, weights, arrows, and update relations.

Do not use style lenses to import facts from reference papers. Only borrow layout skeletons, reader paths, panel rhythm, abstraction level, stage-output visualization, callout strategy, evidence placement, icon style, arrow grammar, density discipline, and style family.
