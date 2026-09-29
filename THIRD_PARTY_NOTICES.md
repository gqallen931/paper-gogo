# Third-party notices

This repository bundles third-party skills and assets alongside the Paper-gogo workflow. Each bundled component is listed below with the license evidence that could be verified from the files in this repository.

**This file records evidence, not conclusions.** Where no license file or license declaration exists, redistribution permission has not been established. Those entries are marked `UNVERIFIED` and need upstream confirmation before this repository is relied upon as a redistribution point.

## Verified in-tree

| Component | License | Evidence |
|---|---|---|
| `world-model-method/` | MIT | `world-model-method/LICENSE` — "Copyright (c) 2026 王多鱼AI (Wang Duoyu)"; includes a note attributing the underlying world-model/JEPA ideas to Yann LeCun's *A Path Towards Autonomous Machine Intelligence* (2022) |
| `karpathy-guidelines/` | MIT | `karpathy-guidelines/SKILL.md` frontmatter: `license: MIT`; derived from Andrej Karpathy's published observations (link cited in the file) |
| `paper-workflow-v5.md`, `paper-workflow-v6.md`, `SKILL.md`, `references/`, `code_assets/` | Original to this package | No third-party license file present; authored as part of Paper-gogo |

## UNVERIFIED — no license file or declaration found

| Component | Contents | Status |
|---|---|---|
| `nature-skills/` | 9 skills: `nature-academic-search`, `nature-citation`, `nature-data`, `nature-figure`, `nature-paper2ppt`, `nature-polishing`, `nature-reader`, `nature-response`, `nature-writing` | No LICENSE file, no `license:` frontmatter, no upstream attribution |
| `code-understanding/` | 9 skills: `diagnosing-bugs`, `understand`, `understand-chat`, `understand-dashboard`, `understand-diff`, `understand-domain`, `understand-explain`, `understand-knowledge`, `understand-onboard` | No LICENSE file, no `license:` frontmatter, no upstream attribution |
| `architecture-engineering/` | 8 skills: `codebase-design`, `domain-modeling`, `grill-me`, `grill-with-docs`, `grilling`, `improve-codebase-architecture`, `resolving-merge-conflicts`, `tdd` | No LICENSE file, no `license:` frontmatter, no upstream attribution |
| `python-expert/` | `SKILL.md` | No LICENSE file, no `license:` frontmatter |
| `paper-framework-figure-studio-pro/` | Skill plus `assets/` vector library, examples, templates, scripts | No LICENSE file, no `license:` frontmatter |

## Required action before redistributing

1. Identify the upstream source of each `UNVERIFIED` component.
2. Determine its license and whether redistribution and modification are permitted.
3. Add the upstream license text to a `LICENSES/` directory, or add a `license:` field to the component's `SKILL.md` frontmatter.
4. Record the source URL and license in this file.
5. If redistribution is not permitted, remove the component or replace it with an original implementation.

## Referenced upstream works (not reproduced)

Several bundled documents discuss third-party research, tools, or standards. Ideas, paper titles, journal policies, and citation metadata are referenced for scholarly use and remain the property of their respective authors. No third-party article, video, or dataset is reproduced in this repository.

## Bundled extra skill collections (`extra-skills/`)

`extra-skills/` holds four additional third-party collections that complement the workflow. **Their licenses differ from the workflow's own components.**

| Collection | License | Evidence |
|---|---|---|
| `extra-skills/academic-research-skills/` | **CC BY-NC 4.0** | `LICENSE` (Copyright © 2026 Cheng-I Wu), `NOTICE.md`, `CITATION.cff` |
| `extra-skills/claude-scholar/` | **MIT** | `LICENSE` (Copyright © 2026 Gaorui Zhang) |
| `extra-skills/paper-craft-skills/` | **MIT** | Stated in upstream `README.upstream.md`; no separate LICENSE file in the upstream archive |
| `extra-skills/scipilot-figure-skill/` | **MIT** | `LICENSE` bundled with the skill |

### ⚠️ Non-commercial restriction

`extra-skills/academic-research-skills/` is licensed **CC BY-NC 4.0 — NonCommercial**: redistribution with attribution is permitted, **commercial use is not**. This is the only non-commercial component in this repository. Remove that directory if commercial use is required.

Full details, the list of skills per collection, and what was deliberately excluded are in [`extra-skills/THIRD_PARTY_NOTICES.extras.md`](extra-skills/THIRD_PARTY_NOTICES.extras.md).

## Bundled skill inventory

[`SKILLS_INDEX.md`](SKILLS_INDEX.md) is generated from the content actually present and lists every bundled skill with its description. It is regenerated with `npm run build:index` in the plugin project and copied here, so it cannot silently drift from reality.
