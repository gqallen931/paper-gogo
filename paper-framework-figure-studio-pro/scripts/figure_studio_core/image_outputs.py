"""Image generation and canonical image batch registration helpers."""

from __future__ import annotations

import argparse
from pathlib import Path
import shutil
from typing import Any

from .artifacts import artifact_record, find_artifact
from .errors import StateError
from .paths import generated_path_to_relative, normalize_relative_path, safe_join, utc_now


def image_batch_records(args: argparse.Namespace, run_dir: Path, state: dict[str, Any]) -> list[dict[str, Any]]:
    output_dir_rel = normalize_relative_path(args.output_dir)
    output_dir = safe_join(run_dir, output_dir_rel)
    output_dir.mkdir(parents=True, exist_ok=True)
    if args.step == "S2-SKETCH-EXPLORE":
        count = len(args.source)
        if count < 6 or count > 8:
            raise StateError(
                "S2-SKETCH-EXPLORE low-fidelity sketch batches must contain 6-8 images. "
                "Default and minimum is 6; uploaded style references do not create automatic preference-informed extras."
            )
    if args.step == "S5-CANDIDATE-IMAGE" and args.start_index + len(args.source) - 1 > 8:
        raise StateError(
            "S5-CANDIDATE-IMAGE formal candidate images must not exceed 8; default is 6 as an adjustable 2x3 matrix."
        )

    created: list[dict[str, Any]] = []
    for offset, source in enumerate(args.source):
        src = Path(source).expanduser().resolve()
        if not src.exists() or not src.is_file():
            raise StateError(f"source image does not exist or is not a file: {source}")
        ext = src.suffix.lower()
        if ext not in {".png", ".jpg", ".jpeg", ".webp"}:
            raise StateError(f"unsupported image extension for source: {source}")
        index = args.start_index + offset
        file_name = args.filename_pattern.format(index=index, step=args.step.lower().replace("-", "_"))
        if Path(file_name).name != file_name:
            raise StateError("filename pattern must produce a file name, not a path")
        if not Path(file_name).suffix:
            file_name += ext
        dest_rel = normalize_relative_path(Path(output_dir_rel) / file_name)
        dest = safe_join(run_dir, dest_rel)
        if dest.exists() and not args.replace:
            raise StateError(f"destination exists; use --replace to overwrite: {dest_rel}")
        shutil.copy2(src, dest)
        artifact_id = f"{args.batch_id}-{index:02d}"
        record_args = argparse.Namespace(
            artifact_id=artifact_id,
            step=args.step,
            kind=args.kind,
            path=dest_rel,
            summary=args.summary or f"{args.batch_id} image {index:02d}",
            tag=sorted(set((args.tag or []) + [args.batch_id, args.step])),
            status=args.status,
            source_user_request=args.source_user_request or "",
        )
        existing = find_artifact(state, artifact_id)
        record = artifact_record(record_args, run_dir, existing, state=state)
        if existing is None:
            state.setdefault("artifacts", []).append(record)
        else:
            existing.clear()
            existing.update(record)
        created.append(record)
    return created


def image_generation_event(args: argparse.Namespace, run_dir: Path) -> dict[str, Any]:
    now = utc_now()
    if args.step == "S2-SKETCH-EXPLORE" and args.generated_path and not (6 <= len(args.generated_path) <= 8):
        raise StateError(
            "S2-SKETCH-EXPLORE image generation events should record 6-8 generated sketch paths. "
            "Default and minimum is 6; uploaded style references do not create automatic preference-informed extras."
        )
    if args.step == "S5-CANDIDATE-IMAGE" and len(args.generated_path or []) > 8:
        raise StateError(
            "S5-CANDIDATE-IMAGE formal image generation events must not record more than 8 generated paths; "
            "default is 6 as an adjustable 2x3 matrix."
        )
    generated_paths: list[str] = []
    omitted_count = 0
    for source in args.generated_path or []:
        rel_path = generated_path_to_relative(run_dir, source, args.require_exists)
        if rel_path is None:
            omitted_count += 1
        else:
            generated_paths.append(rel_path)
    if args.generated_path and omitted_count == 0:
        path_status = "relative_paths_recorded"
    elif args.generated_path:
        path_status = "external_or_unsafe_paths_omitted"
    else:
        path_status = "no_generated_paths_provided"
    return {
        "event_id": args.event_id,
        "batch_id": args.batch_id,
        "step": args.step,
        "generator": args.generator,
        "status": "generation_succeeded",
        "state_update_mode": "auto_project_state_json_only",
        "generated_paths": generated_paths,
        "generated_path_mode": "project_run_relative",
        "generated_path_recording_status": path_status,
        "omitted_generated_path_count": omitted_count,
        "canonical_copy_status": "pending_explicit_copy",
        "summary": args.summary or "",
        "source_user_request": args.source_user_request or "",
        "created_at": now,
        "updated_at": now,
    }
