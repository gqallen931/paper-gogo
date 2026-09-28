#!/usr/bin/env python3
"""Persistent state helper CLI for paper-framework-figure-studio-pro."""

from __future__ import annotations

import argparse
import sys

from figure_studio_core.constants import (
    ARTIFACT_ROLES,
    DEFAULT_ROOT,
    IMAGE_GENERATION_ROUTES,
    PREFERENCE_REFERENCE_ROOT,
    RUNTIME_ENVIRONMENTS,
    WORKFLOW_STEPS,
)
from figure_studio_core.errors import StateError
from figure_studio_core.state_commands import (
    cmd_delete,
    cmd_doctor,
    cmd_init,
    cmd_overwrite,
    cmd_record_image_generation,
    cmd_register,
    cmd_register_image_batch,
    cmd_register_reference_images,
    cmd_rewind_step,
    cmd_resume_cleanup,
    cmd_resume,
    cmd_set_runtime_config,
    cmd_update_step,
    cmd_validate,
)

def add_common(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--root", default=DEFAULT_ROOT)
    parser.add_argument("--allow-custom-root", action="store_true")
    parser.add_argument("--project-id", required=True)

def add_artifact_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--artifact-id", required=True)
    parser.add_argument("--step", required=True, choices=[step for step, _, _, _ in WORKFLOW_STEPS])
    parser.add_argument("--kind", required=True)
    parser.add_argument("--path", required=True)
    parser.add_argument("--summary", default="")
    parser.add_argument("--tag", action="append", default=[])
    parser.add_argument("--status", default="active")
    parser.add_argument("--artifact-role", choices=sorted(ARTIFACT_ROLES))
    parser.add_argument("--source-artifact-role", action="append", default=[], choices=sorted(ARTIFACT_ROLES))
    parser.add_argument("--source-user-request", default="")

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    p_init = sub.add_parser("init")
    add_common(p_init)
    p_init.add_argument("--title")
    p_init.add_argument("--source-material")
    p_init.add_argument("--force", action="store_true")
    p_init.set_defaults(func=cmd_init)

    p_register = sub.add_parser("register")
    add_common(p_register)
    add_artifact_args(p_register)
    p_register.set_defaults(func=cmd_register)

    p_update = sub.add_parser("update-step")
    add_common(p_update)
    p_update.add_argument("--current-step", required=True, choices=[step for step, _, _, _ in WORKFLOW_STEPS])
    p_update.add_argument("--resume-instructions")
    p_update.add_argument("--source-user-request")
    p_update.add_argument(
        "--allow-step-skip",
        action="store_true",
        help="Explicit override for unusual documented reroutes.",
    )
    p_update.set_defaults(func=cmd_update_step)

    p_rewind = sub.add_parser("rewind-step")
    add_common(p_rewind)
    p_rewind.add_argument("--target-step", required=True, choices=[step for step, _, _, _ in WORKFLOW_STEPS])
    p_rewind.add_argument("--reason", default="")
    p_rewind.add_argument("--source-user-request", default="")
    p_rewind.add_argument("--dry-run", action="store_true")
    p_rewind.set_defaults(func=cmd_rewind_step)

    p_resume_cleanup = sub.add_parser("resume-cleanup")
    add_common(p_resume_cleanup)
    p_resume_cleanup.add_argument("--event-id")
    p_resume_cleanup.set_defaults(func=cmd_resume_cleanup)

    p_overwrite = sub.add_parser("overwrite")
    add_common(p_overwrite)
    add_artifact_args(p_overwrite)
    p_overwrite.set_defaults(func=cmd_overwrite)

    p_delete = sub.add_parser("delete")
    add_common(p_delete)
    p_delete.add_argument("--artifact-id", required=True)
    p_delete.set_defaults(func=cmd_delete)

    p_image_batch = sub.add_parser("register-image-batch")
    add_common(p_image_batch)
    p_image_batch.add_argument("--batch-id", required=True)
    p_image_batch.add_argument("--step", required=True, choices=[step for step, _, _, _ in WORKFLOW_STEPS])
    p_image_batch.add_argument("--source", action="append", required=True)
    p_image_batch.add_argument("--output-dir", required=True)
    p_image_batch.add_argument("--filename-pattern", default="{step}-{index:02d}.png")
    p_image_batch.add_argument("--start-index", type=int, default=1)
    p_image_batch.add_argument("--kind", default="image")
    p_image_batch.add_argument("--summary", default="")
    p_image_batch.add_argument("--tag", action="append", default=[])
    p_image_batch.add_argument("--status", default="active")
    p_image_batch.add_argument("--source-user-request", default="")
    p_image_batch.add_argument("--replace", action="store_true")
    p_image_batch.set_defaults(func=cmd_register_image_batch)

    p_record_generation = sub.add_parser("record-image-generation")
    add_common(p_record_generation)
    p_record_generation.add_argument("--event-id", required=True)
    p_record_generation.add_argument("--batch-id", required=True)
    p_record_generation.add_argument("--step", required=True, choices=[step for step, _, _, _ in WORKFLOW_STEPS])
    p_record_generation.add_argument("--generator", required=True, choices=["imagegen", "create-image", "approved-api"])
    p_record_generation.add_argument("--generated-path", action="append", default=[])
    p_record_generation.add_argument("--summary", default="")
    p_record_generation.add_argument("--source-user-request", default="")
    p_record_generation.add_argument("--require-exists", action="store_true")
    p_record_generation.set_defaults(func=cmd_record_image_generation)

    p_reference = sub.add_parser("register-reference-images")
    add_common(p_reference)
    p_reference.add_argument("--source", action="append", required=True)
    p_reference.add_argument("--output-dir", default=PREFERENCE_REFERENCE_ROOT)
    p_reference.add_argument("--reference-id-prefix", default="preference-reference")
    p_reference.add_argument("--start-index", type=int, default=1)
    p_reference.add_argument("--summary", default="")
    p_reference.add_argument("--tag", action="append", default=[])
    p_reference.add_argument("--source-user-request", default="")
    p_reference.add_argument("--replace", action="store_true")
    p_reference.set_defaults(func=cmd_register_reference_images)

    p_runtime = sub.add_parser("set-runtime-config")
    add_common(p_runtime)
    p_runtime.add_argument("--environment", required=True, choices=sorted(RUNTIME_ENVIRONMENTS))
    p_runtime.add_argument("--image-generation-route", choices=sorted(IMAGE_GENERATION_ROUTES))
    p_runtime.add_argument("--image-generation-note")
    p_runtime.add_argument("--source-user-request", default="")
    p_runtime.set_defaults(func=cmd_set_runtime_config)

    p_resume = sub.add_parser("resume")
    add_common(p_resume)
    p_resume.add_argument("--json", action="store_true")
    p_resume.set_defaults(func=cmd_resume)

    p_validate = sub.add_parser("validate")
    add_common(p_validate)
    p_validate.set_defaults(func=cmd_validate)

    p_doctor = sub.add_parser("doctor")
    add_common(p_doctor)
    p_doctor.add_argument("--json", action="store_true")
    p_doctor.add_argument("--fail-on-issue", action="store_true")
    p_doctor.set_defaults(func=cmd_doctor)

    return parser

def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return args.func(args)
    except StateError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

if __name__ == "__main__":
    raise SystemExit(main())


