# Package manifest

Package line: `Paper-gogo-v2-public`

Published as a public repository: <https://github.com/gqallen931/paper-gogo>

## Workflow integrity hashes

| File | SHA-256 |
|---|---|
| `paper-workflow-v5.md` | `E0D5462B50D6BFEE115A9D6C67E30F83A84EA31831F097E55DB9DEDC2476AA9D` |
| `paper-workflow-v6.md` | `D82371E10E54663769DBF6866119572379F4FA8FE90CA64C8FFA4B84FEF023FC` |

The v5 hash is included as the historical-baseline integrity marker. The active entry point is root `SKILL.md`; the active workflow is `paper-workflow-v6.md`. ASCII-only workflow filenames avoid ZIP and console encoding ambiguity while preserving the Chinese document content.

## Bundled skills

This package bundles **57 skills** that the workflow routes to, plus skills that complement it. `SKILLS_INDEX.md` is generated from the content actually present.

| Location | Content | Skills |
|---|---|---|
| `nature-skills/` | search, reading, writing, polishing, citation, data, figures, PPT, reviewer response | 9 |
| `code-understanding/` | code understanding, diff analysis, bug diagnosis | 9 |
| `architecture-engineering/` | domain modeling, module design, TDD | 8 |
| `world-model-method/` | planning, decision and review | 1 |
| `paper-framework-figure-studio-pro/` | turn-by-turn S0-S7 framework figures | 1 |
| `karpathy-guidelines/` | coding guardrails | 1 |
| `python-expert/` | Python experiment implementation | 1 |
| `extra-skills/` | additional third-party collections (licenses differ — see below) | 27 |

> The workflow rule is that only a skill unpacked as a directory with a readable `SKILL.md` may be routed to. Every skill listed above satisfies that condition.

**License note:** `extra-skills/academic-research-skills/` is **CC BY-NC 4.0 (non-commercial)**, unlike the rest of the package. See `THIRD_PARTY_NOTICES.md` and `extra-skills/THIRD_PARTY_NOTICES.extras.md`.

## Consumed by

The DSH plugin [`dsh-paper-gogo-plugin`](https://github.com/gqallen931/paper-gogo-plugin) vendors this workflow into its own `workflow/` directory so that installing the plugin needs no separate copy of this package. The plugin also supports reading this package directly via `preferBundled: false` plus `config.root`.

The plugin project is the build source of truth for the bundled content and carries the maintenance tooling:

| Script | Purpose |
|---|---|
| `scripts/sync-to-package.py` | Mirrors bundled content into this package's layout; `--check` reports drift |
| `scripts/check-consistency.py` | Cross-checks both trees: UTF-8 validity, skill counts, workflow hashes, relative links |
| `scripts/build-skills-index.mjs` | Regenerates `SKILLS_INDEX.md` for either layout |

## Intentionally excluded from the archive

- `.git/`, `.codex/`, `.agents/`
- `work/`, cache, logs, results, and `.understand-anything/`
- existing ZIP files, Python caches, local environment files, and private-key file patterns
