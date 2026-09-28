# Architecture Governance Contract

This contract turns the skill architecture principles into operational rules. Read it before changing workflow steps, state schema, artifact roles, scripts, or release packaging.

Principles:

- **Pipeline:** S0-S7 is a linear workflow with explicit handoffs. Handoffs are copyable prompts, not automatic execution.
- **Loose coupling:** keep workflow constants, state construction, artifact indexing, image-output registration, cleanup, validation, and release checks in separate modules.
- **High cohesion:** each script owns one responsibility. Shared Python state helpers live under `scripts/figure_studio_core/`.
- **Layered on-demand calls:** load only the reference needed for the current step.
- **Transformation isolation:** S0 reports, S2 sketches, S5 candidates, S6 final selection/text outputs, and S7 final audit outputs use distinct output roots and artifact roles.
- **Memory:** after interruption, use `project-state.json` as source of truth.
- **Vulnerability checks:** run validate, doctor, architecture audit, compile checks, JSON validation, and release path scan before packaging.

Before release, run:

```bash
python scripts/figure_studio_architecture_audit.py --target . --fail-on-issue
python -m compileall -q scripts
python scripts/figure_studio_release_check_paths.py scan --target . --fail-on-match
```
