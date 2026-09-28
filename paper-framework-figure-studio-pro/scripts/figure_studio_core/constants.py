"""Stable public constants and schema values."""

from __future__ import annotations

from pathlib import Path
import re

SKILL_NAME = "paper-framework-figure-studio-pro"
SKILL_VERSION = "3.1.4a"
SCHEMA_VERSION = 1
DEFAULT_ROOT = "figure-studio-runs"
STATE_RELATIVE_PATH = Path("state") / "project-state.json"

PREFERENCE_REFERENCE_ROOT = "inputs/preference-reference-images"
PREFERENCE_ANALYSIS_PATH = "outputs/S0-paper-foundation/preference-reference-analysis.md"

SAFE_PROJECT_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,79}$")
SECRET_KEY_RE = re.compile(r"(api[_-]?key|token|secret|password|credential)", re.I)

REFERENCE_IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".webp"}
TARGET_RASTER_IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".webp"}
TARGET_RASTER_IMAGE_STEPS = {
    "S2-SKETCH-EXPLORE",
    "S5-CANDIDATE-IMAGE",
}
TARGET_RASTER_REFERENCE_ROLES = {
    "s2.primary_sketch",
    "s5.primary_candidate",
    "s6.selected_reference_final",
}
FORBIDDEN_TARGET_IMAGE_KINDS = {
    "svg",
    "html",
    "mermaid",
    "canvas",
    "pptx",
    "pdf",
}
FORBIDDEN_TARGET_IMAGE_EXTS = {
    ".svg",
    ".html",
    ".htm",
    ".mmd",
    ".pptx",
    ".pdf",
}
RUNTIME_ENVIRONMENTS = {"unknown", "chatgpt_web", "codex", "claude_code", "other"}
IMAGE_GENERATION_ROUTES = {
    "unknown",
    "chatgpt_create_image",
    "codex_imagegen",
    "approved_image_api",
    "user_supplied_api_required",
    "prompt_only",
}

WORKFLOW_STEPS = [
    (
        "S0-PAPER-FOUNDATION",
        "TEXT_ONLY",
        "Build the paper/source foundation, runtime state, canvas defaults, and optional preference-reference scope.",
        "outputs/S0-paper-foundation",
    ),
    (
        "S1-FIGURE-STRATEGY",
        "TEXT_ONLY",
        "Diagnose reader question, figure role, narrative structure, and candidate visual directions from the paper foundation.",
        "outputs/S1-figure-strategy",
    ),
    (
        "S2-SKETCH-EXPLORE",
        "IMAGE_ONLY_PLUS_PROMPT",
        "Generate 6-8 low-fidelity exploration sketches as separate raster images; include at least two paper-close story-driven/storyboard sketches by default, and use them for broad direction discovery.",
        "outputs/S2-sketch-explore",
    ),
    (
        "S3-DIRECTION-SELECT",
        "TEXT_ONLY",
        "Select the strongest direction from S2 and define the local refinement target without contradicting source evidence.",
        "outputs/S3-direction-selection",
    ),
    (
        "S4-CANDIDATE-BRIEF",
        "TEXT_ONLY",
        "Prepare the formal candidate matrix: per-candidate title, logic, style-aware caption plan, visible core anchors, arrow/color/icon semantics, and image prompt contract.",
        "outputs/S4-candidate-brief",
    ),
    (
        "S5-CANDIDATE-IMAGE",
        "IMAGE_ONLY_PLUS_PROMPT",
        "Generate formal paper-framework raster candidate images, defaulting to clean publication schematic style with paper-relevant icons, precise arrows/colors, and figure-caption symbiosis.",
        "outputs/S5-candidate-images",
    ),
    (
        "S6-FINAL-SELECT",
        "TEXT_ONLY",
        "Select and display the final image, draft the figure title, caption, legend, body-reference text, and manuscript note, then hand off to S7 for joint audit.",
        "outputs/S6-final-selection",
    ),
    (
        "S7-FINAL-JOINT-AUDIT",
        "TEXT_ONLY",
        "Terminal joint audit: evaluate the selected figure and caption/legend/body text together for paper fidelity, model/algorithm/process/math correctness, arrow semantics, color semantics, icon relevance, and final submission readiness.",
        "outputs/S7-final-joint-audit",
    ),
]

STEP_OUTPUT_DIRS = {step: output_dir for step, _, _, output_dir in WORKFLOW_STEPS}
STEP_SEQUENCE = tuple(step for step, _, _, _ in WORKFLOW_STEPS)
DEFAULT_NEXT_STEP_BY_STEP = {
    step: STEP_SEQUENCE[index + 1] if index + 1 < len(STEP_SEQUENCE) else None
    for index, step in enumerate(STEP_SEQUENCE)
}
TEXT_REPLY_STEP_BANNER_TEMPLATE = (
    "当前流程位置\n"
    "全流程：S0-PAPER-FOUNDATION -> S1-FIGURE-STRATEGY -> S2-SKETCH-EXPLORE -> "
    "S3-DIRECTION-SELECT -> S4-CANDIDATE-BRIEF -> S5-CANDIDATE-IMAGE -> "
    "S6-FINAL-SELECT -> S7-FINAL-JOINT-AUDIT\n"
    "当前 step：{current_step}\n"
    "默认下一步：{default_next_step}"
)
STEP_CLEANUP_EXTRA_DIRS = {}
STEP_CLEANUP_EXTRA_FILES = {}

ARTIFACT_ROLES = {
    "s0.paper_foundation_report": {
        "step": "S0-PAPER-FOUNDATION",
        "kind": "markdown",
        "relative_path": "outputs/S0-paper-foundation/paper-foundation-report.md",
    },
    "s1.figure_strategy": {
        "step": "S1-FIGURE-STRATEGY",
        "kind": "markdown",
        "relative_path": "outputs/S1-figure-strategy/figure-strategy-brief.md",
    },
    "s2.primary_sketch": {
        "step": "S2-SKETCH-EXPLORE",
        "kind": "image",
        "relative_path": "outputs/S2-sketch-explore/sketch-01.png",
    },
    "s3.direction_selection": {
        "step": "S3-DIRECTION-SELECT",
        "kind": "markdown",
        "relative_path": "outputs/S3-direction-selection/direction-selection.md",
    },
    "s4.candidate_brief": {
        "step": "S4-CANDIDATE-BRIEF",
        "kind": "markdown",
        "relative_path": "outputs/S4-candidate-brief/candidate-board-brief.md",
    },
    "s5.primary_candidate": {
        "step": "S5-CANDIDATE-IMAGE",
        "kind": "image",
        "relative_path": "outputs/S5-candidate-images/candidate-01.png",
    },
    "s6.final_selection": {
        "step": "S6-FINAL-SELECT",
        "kind": "markdown",
        "relative_path": "outputs/S6-final-selection/final-selection-report.md",
    },
    "s6.selected_reference_final": {
        "step": "S6-FINAL-SELECT",
        "kind": "image",
        "relative_path": "outputs/S5-candidate-images/candidate-01.png",
    },
    "s6.figure_text": {
        "step": "S6-FINAL-SELECT",
        "kind": "markdown",
        "relative_path": "outputs/S6-final-selection/figure-text.md",
    },
    "s7.final_joint_audit": {
        "step": "S7-FINAL-JOINT-AUDIT",
        "kind": "markdown",
        "relative_path": "outputs/S7-final-joint-audit/final-joint-audit.md",
    },
}

PRIMARY_ARTIFACT_ROLE_BY_STEP = {
    "S0-PAPER-FOUNDATION": "s0.paper_foundation_report",
    "S1-FIGURE-STRATEGY": "s1.figure_strategy",
    "S2-SKETCH-EXPLORE": "s2.primary_sketch",
    "S3-DIRECTION-SELECT": "s3.direction_selection",
    "S4-CANDIDATE-BRIEF": "s4.candidate_brief",
    "S5-CANDIDATE-IMAGE": "s5.primary_candidate",
    "S6-FINAL-SELECT": "s6.final_selection",
    "S7-FINAL-JOINT-AUDIT": "s7.final_joint_audit",
}

CANONICAL_OUTPUTS = {
    step: ARTIFACT_ROLES[role]["relative_path"] for step, role in PRIMARY_ARTIFACT_ROLE_BY_STEP.items()
}


def _pending_row(role_id: str) -> dict[str, str]:
    role = ARTIFACT_ROLES[role_id]
    return {"step": role["step"], "relative_path": role["relative_path"], "artifact_role": role_id}


PENDING_CANONICAL_OUTPUTS = []
for _step, _, _, _ in WORKFLOW_STEPS:
    _role_id = PRIMARY_ARTIFACT_ROLE_BY_STEP[_step]
    PENDING_CANONICAL_OUTPUTS.append(_pending_row(_role_id))

TEXT_ONLY_STEPS = {step for step, mode, _, _ in WORKFLOW_STEPS if mode.startswith("TEXT_ONLY")}
IMAGE_ONLY_STEPS = {step for step, mode, _, _ in WORKFLOW_STEPS if mode.startswith("IMAGE_ONLY")}

ATLAS_BOARD_ROOT = "assets/subtype-atlas/boards"
ATLAS_THUMBNAIL_ROOT = "assets/subtype-atlas/thumbnails"
ATLAS_MANIFEST_PATH = "assets/subtype-atlas/manifest.json"
ATLAS_BOARD_IDS = (
    "subtype-overview",
    "visual-grammar-layout",
    "reader-role-detail",
    "visual-communication-styles",
)
ATLAS_DISPLAY_POLICY = (
    "Whenever a reply mentions subtype/category atlas boards, layout grammar, visual communication styles, "
    "reader-role detail, or subtype overview, embed the corresponding saved PNG board with Markdown. "
    "Do not build generated web pages in any environment, including Codex."
)
