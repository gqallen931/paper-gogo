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
