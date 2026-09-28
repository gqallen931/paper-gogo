"""State schema defaults and workflow state construction."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .constants import (
    ARTIFACT_ROLES,
    CANONICAL_OUTPUTS,
    DEFAULT_ROOT,
    DEFAULT_NEXT_STEP_BY_STEP,
    FORBIDDEN_TARGET_IMAGE_EXTS,
    FORBIDDEN_TARGET_IMAGE_KINDS,
    PENDING_CANONICAL_OUTPUTS,
    PREFERENCE_ANALYSIS_PATH,
    PREFERENCE_REFERENCE_ROOT,
    SCHEMA_VERSION,
    SKILL_NAME,
    SKILL_VERSION,
    STATE_RELATIVE_PATH,
    STEP_CLEANUP_EXTRA_DIRS,
    STEP_SEQUENCE,
    TARGET_RASTER_IMAGE_EXTS,
    TARGET_RASTER_IMAGE_STEPS,
    TARGET_RASTER_REFERENCE_ROLES,
    TEXT_REPLY_STEP_BANNER_TEMPLATE,
    WORKFLOW_STEPS,
    ATLAS_DISPLAY_POLICY,
    ATLAS_MANIFEST_PATH,
    ATLAS_BOARD_ROOT,
    ATLAS_BOARD_IDS,
)
from .paths import normalize_relative_path, safe_join, utc_now


def workflow_state(current_step: str = "S0-PAPER-FOUNDATION") -> list[dict[str, Any]]:
    rows = []
    step_order = [step for step, _, _, _ in WORKFLOW_STEPS]
    current_index = step_order.index(current_step)
    for index, (step, mode, purpose, output_dir) in enumerate(WORKFLOW_STEPS):
        if step == current_step:
            status = "in_progress"
        elif index < current_index:
            status = "completed"
        else:
            status = "pending"
        rows.append(
            {
                "step": step,
                "mode": mode,
                "purpose": purpose,
                "output_dir": output_dir,
                "canonical_output": CANONICAL_OUTPUTS[step],
                "default_next_step": DEFAULT_NEXT_STEP_BY_STEP[step],
                "status": status,
            }
        )
    return rows


def step_attempt_id(step: str, epoch: int) -> str:
    normalized_step = step.lower().replace("-", "_")
    return f"{normalized_step}-e{epoch:04d}"


def initial_step_runs(current_step: str, now: str) -> dict[str, dict[str, Any]]:
    current_index = [step for step, _, _, _ in WORKFLOW_STEPS].index(current_step)
    rows: dict[str, dict[str, Any]] = {}
    for index, (step, _, _, output_dir) in enumerate(WORKFLOW_STEPS):
        epoch = 1 if step == current_step else 0
        if step == current_step:
            status = "in_progress"
        elif index < current_index:
            status = "completed"
        else:
            status = "pending"
        rows[step] = {
            "step": step,
            "epoch": epoch,
            "attempt_id": step_attempt_id(step, epoch),
            "status": status,
            "output_dir": output_dir,
            "started_at": now if status == "in_progress" else None,
            "updated_at": now,
        }
    return rows


def ensure_step_runs(state: dict[str, Any]) -> dict[str, dict[str, Any]]:
    now = utc_now()
    current_step = state.get("current_step", "S0-PAPER-FOUNDATION")
    step_runs = state.setdefault("step_runs", {})
    for step, _, _, output_dir in WORKFLOW_STEPS:
        row = step_runs.setdefault(step, {})
        row.setdefault("step", step)
        row.setdefault("output_dir", output_dir)
        row.setdefault("epoch", 1 if step == current_step else 0)
        row.setdefault("attempt_id", step_attempt_id(step, int(row.get("epoch") or 0)))
        row.setdefault("status", "in_progress" if step == current_step else "pending")
        row.setdefault("started_at", now if step == current_step else None)
        row.setdefault("updated_at", now)
    for stale_step in list(step_runs):
        if stale_step not in STEP_SEQUENCE:
            step_runs.pop(stale_step, None)
    return step_runs


def current_step_epoch(state: dict[str, Any], step: str) -> int:
    step_runs = ensure_step_runs(state)
    return int(step_runs.get(step, {}).get("epoch") or 0)


def mark_step_run_in_progress(state: dict[str, Any], step: str, bump_if_zero: bool = True) -> dict[str, Any]:
    step_runs = ensure_step_runs(state)
    row = step_runs[step]
    epoch = int(row.get("epoch") or 0)
    now = utc_now()
    if bump_if_zero and epoch == 0:
        epoch = 1
        row["epoch"] = epoch
        row["attempt_id"] = step_attempt_id(step, epoch)
        row["started_at"] = now
    row["status"] = "in_progress"
    row["updated_at"] = now
    step_order = [name for name, _, _, _ in WORKFLOW_STEPS]
    current_index = step_order.index(step)
    for other_step, other_row in step_runs.items():
        if other_step == step or other_step not in step_order:
            continue
        other_index = step_order.index(other_step)
        other_epoch = int(other_row.get("epoch") or 0)
        other_row["status"] = "completed" if other_index < current_index and other_epoch > 0 else "pending"
        other_row["updated_at"] = now
    return row


def bump_step_epoch(state: dict[str, Any], step: str, status: str) -> dict[str, Any]:
    step_runs = ensure_step_runs(state)
    row = step_runs[step]
    now = utc_now()
    old_epoch = int(row.get("epoch") or 0)
    new_epoch = old_epoch + 1
    row.update(
        {
            "epoch": new_epoch,
            "attempt_id": step_attempt_id(step, new_epoch),
            "status": status,
            "started_at": now if status == "in_progress" else None,
            "updated_at": now,
        }
    )
    return {
        "step": step,
        "old_epoch": old_epoch,
        "new_epoch": new_epoch,
        "attempt_id": row["attempt_id"],
        "status": status,
    }


def ensure_output_dirs(run_dir: Path) -> None:
    safe_join(run_dir, "state").mkdir(parents=True, exist_ok=True)
    safe_join(run_dir, PREFERENCE_REFERENCE_ROOT).mkdir(parents=True, exist_ok=True)
    for _, _, _, output_dir in WORKFLOW_STEPS:
        safe_join(run_dir, output_dir).mkdir(parents=True, exist_ok=True)
    for extra_dirs in STEP_CLEANUP_EXTRA_DIRS.values():
        for output_dir in extra_dirs:
            safe_join(run_dir, output_dir).mkdir(parents=True, exist_ok=True)


def initial_state(project_id: str, run_dir: Path, title: str | None) -> dict[str, Any]:
    now = utc_now()
    return {
        "project_state_schema_version": SCHEMA_VERSION,
        "skill_name": SKILL_NAME,
        "skill_version": SKILL_VERSION,
        "project_id": project_id,
        "project_title": title or project_id,
        "created_at": now,
        "updated_at": now,
        "current_step": "S0-PAPER-FOUNDATION",
        "workflow_plan": workflow_state("S0-PAPER-FOUNDATION"),
        "step_sequence": list(STEP_SEQUENCE),
        "default_next_step_by_step": DEFAULT_NEXT_STEP_BY_STEP,
        "step_runs": initial_step_runs("S0-PAPER-FOUNDATION", now),
        "output_root": normalize_relative_path(Path(DEFAULT_ROOT) / project_id),
        "state_file": normalize_relative_path(STATE_RELATIVE_PATH),
        "path_storage_policy": "all stored paths are project-run relative; host-specific absolute paths are not persisted",
        "removed_steps_policy": {
            "status": "active",
            "removed_after_v3_1_3": "old post-S6 extraction and SVG/PPT delivery steps",
            "terminal_step": "S7-FINAL-JOINT-AUDIT",
            "no_old_delivery_chain": True,
            "rule": "S6 selects/provides the final image and drafts figure text; S7 jointly audits the selected figure plus caption/legend/body text before final submission. The old foreground extraction, SVG/PPT construction, and separate delivery chain are not active.",
        },
        "target_raster_image_generation_policy": {
            "status": "hard_required",
            "rule": "Target-paper sketches and formal candidates must be generated raster images. SVG/HTML/Mermaid/canvas/PPT/PDF/code-drawn substitutes are invalid for S2/S5 target images.",
            "raster_generation_steps": sorted(TARGET_RASTER_IMAGE_STEPS),
            "raster_reference_roles": sorted(TARGET_RASTER_REFERENCE_ROLES),
            "allowed_generated_image_extensions": sorted(TARGET_RASTER_IMAGE_EXTS),
            "forbidden_target_image_kinds": sorted(FORBIDDEN_TARGET_IMAGE_KINDS),
            "forbidden_target_image_extensions": sorted(FORBIDDEN_TARGET_IMAGE_EXTS),
            "s6_selected_reference_policy": "S6-FINAL-SELECT must select one S5 generated raster image candidate as the final reference and provide its path/display.",
            "no_fallback_substitute": "If Image Gen, ChatGPT Create Image, or an approved image API is unavailable, stop and report the limitation instead of fabricating SVG or code-drawn placeholders.",
        },
        "paper_framework_non_poster_policy": (
            "This skill is only for research-paper framework/architecture/pipeline/mechanism figures. "
            "It must not produce posters, marketing visuals, cover art, decorative exhibition boards, or PPT-slide content pages."
        ),
        "default_canvas_policy": {
            "default_aspect_ratio": "16:9",
            "user_editable": True,
            "first_reply_disclosure_required": True,
            "applies_to_steps": ["S2-SKETCH-EXPLORE", "S5-CANDIDATE-IMAGE"],
            "user_adjustment_examples": ["4:3", "1:1", "3:2", "double-column landscape", "journal-specified size"],
            "state_recording_policy": "If the user changes the aspect ratio, record the requested ratio in project state and carry it through later image prompts.",
        },
        "default_density_policy": (
            "Default figure density is readable and not crowded. Use the image as a cognitive map; "
            "move definitions, caveats, dense equations, symbol meanings, and long explanations to the caption/legend/body text that S7 audits together with the figure."
        ),
        "vector_first_minimal_semantic_policy": {
            "status": "active",
            "contract": "references/vector-first-minimal-semantic-rule.md",
            "one_visual_sentence": True,
            "default_main_module_range": "3-6",
            "default_dominant_flow_count": 1,
            "default_secondary_flow_range": "0-3",
            "default_formula_policy": "usually 0 visible formulas; include a symbol/formula only with a necessity proof that the core idea cannot be expressed without it",
            "style_policy": "S5 defaults to clean publication-ready schematic raster references; SVG/PPT approximation is a downstream editability check, not the primary design target, and S5 does not generate SVG.",
            "figure_caption_split": "Figure and caption are co-designed as one explanatory bundle: the figure carries the cognitive map, while title/caption/legend/body text carries definitions, equation meaning, symbol explanations, constraints, caveats, and long explanations.",
        },
        "core_submodule_detail_policy": {
            "status": "active",
            "contract": "references/core-submodule-detail-policy-v313.md",
            "rule": "Core innovation modules must not be empty generic boxes when source evidence provides internal mechanism detail.",
            "display_modes": ["in_place_internal_detail", "side_inset_detail"],
            "review_policy": "S3, S6, and S7 downgrade or reject candidates whose core contribution module is visually opaque, whose non-droppable core substeps are absent from the figure-caption bundle, or whose caption is hiding a step that must be visibly anchored in the image.",
        },
        "math_symbol_anchor_policy": {
            "status": "active",
            "rule": "A few mathematical symbols or simple formulas may be visible only when they are necessary self-contained anchors for the core idea or claimed improvement.",
            "visual_preference": "Prefer arrows, placement, grouping, and compact legends over derivations or dense notation inside the figure; if a symbol is not necessary, omit it.",
        },
        "figure_caption_codesign_policy": {
            "status": "active",
            "contract": "references/figure-caption-codesign-policy-v311.md",
            "candidate_bundle": "pre-image candidate introduction + candidate image",
            "pixel_policy": "Title, explanation, legend, method prose, and symbol definitions stay outside image pixels unless a short label is needed for readability.",
            "s2_card_policy": "Each S2 sketch candidate is introduced before image generation with candidate ID, short figure title, 2-3 sentence explanation draft, symbol/visual legend, a 3-5 short-label image text budget, and story-paper closeness note for story-driven candidates.",
            "s2_storyboard_requirement": "The first S2 low-fidelity hand-drawn exploration batch must include at least two paper-close story-driven/storyboard candidates by default, unless the user explicitly forbids story-like sketches or the paper is genuinely unsuitable.",
            "s5_card_policy": "Each S5 formal candidate is introduced in S4 before image generation with figure title, 4-6 sentence explanation draft, style-aware caption plan, symbol/visual legend, in-image text budget, kept-out-of-image notes, claimed improvement visual anchor, symbol/formula necessity proof, and arrow/color/icon semantic contract.",
            "candidate_text_contract_gate": "hard_required_before_image_generation",
            "s6_policy": "S6-FINAL-SELECT must provide final image selection plus draft title, caption, legend, body-reference text, and manuscript note; S7 then audits the figure-caption bundle jointly.",
            "s7_policy": "S7-FINAL-JOINT-AUDIT evaluates the selected image and caption/legend/body text together, not image-only, and may pass, require caption repair, or send the workflow back to S4/S5/S6.",
        },
        "artifact_role_registry": ARTIFACT_ROLES,
        "active_artifact_roles": {},
        "s0_paper_foundation_policy": {
            "status": "input_depth_sensitive",
            "contract": "references/paper-deep-reading-contract.md",
            "output_artifact": "outputs/S0-paper-foundation/paper-foundation-report.md",
            "must_print_in_reply_body": True,
            "foundation_status": "required_foundation_for_all_later_steps when source material is available",
            "simple_description_policy": "If the user only provides a short/simple description, do lightweight scoping and record deep_reading_status as not_triggered_simple_description.",
        },
        "figure_direction_and_candidate_policy": {
            "S2": "Generate 6-8 broad low-fidelity sketches, including at least two paper-close story-driven/storyboard sketches by default.",
            "S5": "Generate up to 8 formal raster candidates, default 6 in a 2x3 matrix; second-round candidates should be formal, clean, paper-faithful, icon-semantically relevant, and readable as figure-caption bundles.",
            "hand_drawn_boundary": "Hand-drawn/sketch-note/storyboard style is expected in the first S2 low-fidelity exploration batch; at least two story-driven/storyboard sketches are required by default. Any story/metaphor must be close to the paper's own logic and use common concepts that readers can associate with the paper. S5 remains formal unless the user explicitly asks otherwise.",
        },
        "s6_final_selection_output_policy": {
            "status": "active",
            "final_image_required": True,
            "final_image_source": "one selected S5-CANDIDATE-IMAGE raster candidate",
            "final_image_path_or_display_required": True,
            "default_next_step": "S7-FINAL-JOINT-AUDIT",
            "required_text_sections": [
                "figure_title",
                "caption",
                "legend",
                "body_reference_sentence",
                "manuscript_revision_note",
            ],
            "completion_rule": "After S6-FINAL-SELECT, proceed to S7-FINAL-JOINT-AUDIT for final figure-caption audit.",
        },
        "s7_final_joint_audit_policy": {
            "status": "active",
            "terminal_step": True,
            "joint_evaluation_required": True,
            "minimum_passes": [
                "paper_fidelity_and_non_contradiction",
                "model_algorithm_process_math_check",
                "visual_semantics_check_for_arrows_colors_icons_symbols",
                "figure_caption_symbiosis_check",
                "reader_readiness_and_submission_check",
            ],
            "pass_rule": "Only mark S7 complete when the selected image plus caption/legend/body-reference text jointly pass all checks with no unresolved semantic error.",
            "failure_route": "If a problem is found, state whether to repair S6 text, regenerate S5 candidates through S4/S5, or revisit S1/S3 direction logic; do not silently submit a flawed figure.",
        },
        "preference_reference_root": PREFERENCE_REFERENCE_ROOT,
        "startup_questions": {
            "runtime_environment": {
                "status": "pending",
                "question": "Which runtime will generate images: Codex Image Gen, ChatGPT web Create Image, or another approved image API?",
            },
            "preference_reference_diagrams": {
                "status": "optional",
                "question": "Do you have reference diagrams for style/category preference? If so, register them before S1 when possible.",
            },
        },
        "user_preference_reference_images": [],
        "user_preference_profile": {
            "status": "none",
            "analysis_artifact": PREFERENCE_ANALYSIS_PATH,
            "default_s2_sketch_count": 6,
            "default_s5_candidate_count": 6,
            "max_total_candidate_count": 8,
            "style_preference_scope_policy": "Preference references inform S1 figure-type/reader-effect suggestions and do not automatically force S2-S7 style.",
        },
        "runtime_environment": {
            "environment": "unknown",
            "image_generation_route": "unknown",
            "image_generation_note": "Resolve the image route before image steps.",
            "runtime_environment_note": "Use text replies plus direct Markdown image embeds for saved atlas boards; generated web pages are not produced.",
        },
        "atlas_display_policy": {
            "status": "active",
            "manifest": ATLAS_MANIFEST_PATH,
            "board_root": ATLAS_BOARD_ROOT,
            "board_ids": list(ATLAS_BOARD_IDS),
            "policy": ATLAS_DISPLAY_POLICY,
        },
        "architecture_governance_policy": {
            "status": "active",
            "contract": "references/architecture-governance-contract.md",
            "loose_coupling": "Each stage reads registered artifacts and writes its own output root.",
            "high_cohesion": "Shared Python helpers live under scripts/figure_studio_core and each command owns one narrow state task.",
            "layered_on_demand_calls": "Load references only when needed; S0/S1 grounding, S2/S5 image generation, S6 final selection, and S7 final audit stay separate.",
            "transformation_isolation": "S0 reports, S2 sketches, S5 candidates, S6 selected outputs, and S7 final audit outputs use distinct output roots and artifact roles.",
            "failure_resume": "state/project-state.json is the resume anchor and is preserved by rewind cleanup.",
            "abstraction": "Stable constants define workflow, artifact roles, and validation rules.",
            "memory": "Artifacts, image generation events, cleanup events, and preference references are stored in project state.",
            "retrievability": "Canonical outputs and artifact roles make generated material discoverable after resume.",
            "vulnerability_checks": "State validation rejects path traversal, host absolute paths, forbidden target-image substitutes, and secret-like keys.",
        },
        "step_rewind_cleanup_policy": {
            "status": "active",
            "contract": "references/step-rewind-cleanup-contract.md",
            "backjump_decision_policy": "If a user returns to an earlier or current step and that step will be executed again, cleanup is mandatory.",
            "delete_target_and_later_step_outputs": "hard_cleanup_for_target_to_from_step_span",
            "history_reference_policy": "Pure historical questions may be answered without cleanup; execution backjumps clean covered active outputs.",
            "cleanup_required_when": [
                "current_step moves back to an earlier step for execution",
                "the current step is rerun",
                "S7-FINAL-JOINT-AUDIT is entered again after prior S7 outputs or records exist",
            ],
            "hard_cleanup_required_for": "all steps when returning/rerunning for execution",
            "s7_rerun_cleanup_scope": "delete prior S7 outputs and S7 records only; preserve S0-S6 selected figure and text inputs; record cleanup event before rerunning S7",
            "state_file_deleted": False,
            "artifact_record_policy": "remove covered output records from artifacts/image_generation_events/active roles/pending state; keep cleanup_events as the audit record",
            "cleanup_events": [],
        },
        "pending_outputs": list(PENDING_CANONICAL_OUTPUTS),
        "artifacts": [],
        "previous_image_only_output_recording_status": "not_applicable",
        "previous_image_only_plus_prompt_output_recording_status": "not_applicable",
        "generated_image_default_locations_to_register": [],
        "image_generation_state_update_status": "not_applicable",
        "image_output_registration_status": "not_applicable",
        "image_generation_events": [],
        "choice_prompt_policy": {
            "mandatory_after_every_text_reply": True,
            "required_section_title": "下一步可复制提示词",
            "must_include_fallback_for_unsure_user": True,
            "must_end_every_text_reply_with_exact_sentence": True,
            "final_line_text": "如果不知道如何提问，请说：请使用 paper-framework-figure-studio-pro 根据当前状态只建议下一步提示词，不要自动执行下一步。",
            "must_show_unsure_user_reminder_in_every_pure_text_reply": True,
            "choice_prompt_policy_applied": False,
            "default_option_id": None,
            "available_option_ids": [],
            "alternative_prompt_count": 0,
            "copyable_prompts_provided_for_options": [],
            "multi_choice_placeholder_prompt_required": True,
            "placeholder_prompt_template": "请按照 paper-framework-figure-studio-pro skill 的要求，根据当前状态和已登记产物，我选择：<填写心仪方案ID或描述>。请按这个选择进入：<填写下一步stage>。不要执行其他未指定 stage。",
            "language_policy": "Use Chinese for docs and prompts when the user's main input is Chinese; use English when the user's main input is mainly English.",
        },
        "text_reply_step_banner_template": TEXT_REPLY_STEP_BANNER_TEMPLATE,
        "last_user_request": None,
        "notes": [],
    }
