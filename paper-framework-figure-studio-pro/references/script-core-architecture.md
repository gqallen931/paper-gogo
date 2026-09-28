# Script Core Architecture

CLI entry:

- `scripts/figure_studio_state.py`: persistent state helper CLI.
- `scripts/figure_studio_architecture_audit.py`: package architecture and release hygiene audit.
- `scripts/figure_studio_release_check_paths.py`: absolute path and cache scanner.

Core helpers:

- `constants.py`: workflow sequence, artifact roles, generation gates, stable paths.
- `state_schema.py`: initial project-state schema and step-run helpers.
- `state_commands.py`: CLI command implementations and cleanup.
- `artifacts.py`: artifact indexing and target raster validation.
- `image_outputs.py`: image generation event and batch registration helpers.
- `validation.py`: state validation and security checks.
- `paths.py`: path normalization and relative-path enforcement.
- `preferences.py`: user preference reference registration.
- `runtime_config.py`: runtime image-route policy.

S5 remains a raster image generation step. Any SVG/PPT language in prompts must mean optional later human approximation, not direct SVG/PPT output and not the primary design target.

S7 is a text-only bounded audit step. It may clean prior S7 outputs on rerun, but it must preserve S0-S6 inputs because they are the audit source.
