#!/usr/bin/env python3
"""Audit package structure, workflow contracts, and release hygiene."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path


EXPECTED_SEQUENCE = [
    "S0-PAPER-FOUNDATION",
    "S1-FIGURE-STRATEGY",
    "S2-SKETCH-EXPLORE",
    "S3-DIRECTION-SELECT",
    "S4-CANDIDATE-BRIEF",
    "S5-CANDIDATE-IMAGE",
    "S6-FINAL-SELECT",
    "S7-FINAL-JOINT-AUDIT",
]

REQUIRED_FILES = [
    "SKILL.md",
    "metadata.json",
    "VERSION",
    "scripts/figure_studio_state.py",
    "scripts/figure_studio_release_check_paths.py",
    "references/architecture-governance-contract.md",
    "references/module-orchestration-contract.md",
    "references/security-and-portability-policy.md",
    "references/step-rewind-cleanup-contract.md",
    "templates/project-state-template.json",
]

FORBIDDEN_FILE_NAMES = {
    "editable_renderer.html": "Generated browser renderer output is not part of the skill contract.",
    "renderer_core.js": "Generated browser renderer output is not part of the skill contract.",
}


@dataclass
class Finding:
    severity: str
    check_id: str
    path: str
    message: str


def text_files(root: Path) -> list[Path]:
    suffixes = {".md", ".py", ".js", ".json", ".yaml", ".yml", ".txt"}
    return [
        path
        for path in sorted(root.rglob("*"))
        if path.is_file() and path.suffix.lower() in suffixes and ".git" not in path.parts
    ]


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def is_mirrored_vector_library_path(rel_path: str) -> bool:
    return rel_path.startswith("assets/vector-library/") or rel_path.startswith("references/vector-library/")


def add(finds: list[Finding], severity: str, check_id: str, path: str, message: str) -> None:
    finds.append(Finding(severity, check_id, path, message))


def check_required_files(root: Path, finds: list[Finding]) -> None:
    for rel in REQUIRED_FILES:
        if not (root / rel).exists():
            add(finds, "error", "required-file", rel, "Required package file is missing.")


def check_versions(root: Path, finds: list[Finding]) -> None:
    version_file = (root / "VERSION").read_text(encoding="utf-8").strip()
    metadata = json.loads((root / "metadata.json").read_text(encoding="utf-8"))
    constants_text = read_text(root / "scripts/figure_studio_core/constants.py")
    match = re.search(r'SKILL_VERSION\s*=\s*"([^"]+)"', constants_text)
    constant_version = match.group(1) if match else None
    if metadata.get("version") != version_file:
        add(finds, "error", "version-sync", "metadata.json", "metadata.json version does not match VERSION.")
    if constant_version != version_file:
        add(finds, "error", "version-sync", "scripts/figure_studio_core/constants.py", "SKILL_VERSION does not match VERSION.")


def check_step_sequence(root: Path, finds: list[Finding]) -> None:
    state = json.loads((root / "templates/project-state-template.json").read_text(encoding="utf-8"))
    if state.get("step_sequence") != EXPECTED_SEQUENCE:
        add(finds, "error", "step-sequence", "templates/project-state-template.json", "step_sequence does not match the canonical workflow.")
    for index, step in enumerate(EXPECTED_SEQUENCE[:-1]):
        expected_next = EXPECTED_SEQUENCE[index + 1]
        actual_next = state.get("default_next_step_by_step", {}).get(step)
        if actual_next != expected_next:
            add(finds, "error", "next-step", "templates/project-state-template.json", f"{step} default next is {actual_next!r}, expected {expected_next!r}.")
    if state.get("default_next_step_by_step", {}).get(EXPECTED_SEQUENCE[-1]) is not None:
        add(finds, "error", "next-step", "templates/project-state-template.json", "Final step must not have a default next step.")


def check_reference_links(root: Path, finds: list[Finding]) -> None:
    for path in text_files(root):
        rel_path = path.relative_to(root).as_posix()
        if is_mirrored_vector_library_path(rel_path):
            continue
        text = read_text(path)
        for raw_rel in re.findall(r"references/[A-Za-z0-9_.\-/]+", text):
            rel = raw_rel.rstrip(".,);`]")
            if not (root / rel).exists():
                add(finds, "error", "broken-reference", rel_path, f"Referenced file does not exist: {rel}")
        for raw_rel in re.findall(r"scripts/[A-Za-z0-9_.\-/]+", text):
            rel = raw_rel.rstrip(".,);`]")
            if rel.endswith(".py") or rel.endswith(".js"):
                if not (root / rel).exists():
                    add(finds, "error", "broken-script-reference", rel_path, f"Referenced script does not exist: {rel}")


def legacy_tokens() -> list[str]:
    old = []
    for number in [0, 1, 2, 3, 4, 5, 6, 7, 9]:
        old.append("Sta" + f"ge{number}")
    old.extend(["Sta" + "ge8a", "Sta" + "ge8b", "sta" + "ge8a", "sta" + "ge8b", "sta" + "ge_"])
    return old


def check_text_hygiene(root: Path, finds: list[Finding]) -> None:
    current_script = Path(__file__).name
    for path in text_files(root):
        rel_path = path.relative_to(root).as_posix()
        if is_mirrored_vector_library_path(rel_path):
            continue
        text = read_text(path)
        if rel_path.endswith(current_script):
            continue
        for token in legacy_tokens():
            if token in text:
                add(finds, "error", "legacy-step-name", rel_path, f"Legacy workflow token remains: {token}")


def check_cache_and_outputs(root: Path, finds: list[Finding]) -> None:
    for path in sorted(root.rglob("*")):
        rel_path = path.relative_to(root).as_posix()
        if path.name == "__pycache__" or path.suffix == ".pyc":
            add(finds, "error", "python-cache", rel_path, "Python cache artifacts must not be released.")
        if path.name in FORBIDDEN_FILE_NAMES:
            add(finds, "error", "forbidden-output", rel_path, FORBIDDEN_FILE_NAMES[path.name])
        if ".skill_test_runs" in path.parts:
            add(finds, "error", "test-output", rel_path, "Temporary smoke-test output must not be released.")


def check_architecture_contract(root: Path, finds: list[Finding]) -> None:
    state = json.loads((root / "templates/project-state-template.json").read_text(encoding="utf-8"))
    policy = state.get("architecture_governance_policy", {})
    if policy.get("contract") != "references/architecture-governance-contract.md":
        add(finds, "error", "architecture-policy", "templates/project-state-template.json", "architecture_governance_policy contract is missing or incorrect.")
    required_keys = [
        "loose_coupling",
        "high_cohesion",
        "layered_on_demand_calls",
        "transformation_isolation",
        "failure_resume",
        "abstraction",
        "memory",
        "retrievability",
        "vulnerability_checks",
    ]
    missing = [key for key in required_keys if key not in policy]
    if missing:
        add(finds, "error", "architecture-policy", "templates/project-state-template.json", "Missing architecture policy keys: " + ", ".join(missing))


def run(root: Path) -> list[Finding]:
    finds: list[Finding] = []
    check_required_files(root, finds)
    if not finds:
        check_versions(root, finds)
        check_step_sequence(root, finds)
        check_reference_links(root, finds)
        check_text_hygiene(root, finds)
        check_cache_and_outputs(root, finds)
        check_architecture_contract(root, finds)
    return finds


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", default=".", help="Skill package directory to audit.")
    parser.add_argument("--json-output")
    parser.add_argument("--fail-on-issue", action="store_true")
    args = parser.parse_args(argv)
    root = Path(args.target).resolve()
    findings = run(root)
    payload = {
        "target": str(root),
        "ok": not findings,
        "finding_count": len(findings),
        "findings": [asdict(finding) for finding in findings],
    }
    if args.json_output:
        Path(args.json_output).parent.mkdir(parents=True, exist_ok=True)
        Path(args.json_output).write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2, ensure_ascii=False))
    if findings and args.fail_on_issue:
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
