# Bundled extra skill collections — third-party notices

This plugin bundles four third-party skill collections under `workflow/extras/`, in addition to the Paper-gogo workflow itself (`workflow/`, documented in `../THIRD_PARTY_NOTICES.md`).

**This file records evidence, not conclusions.** Where no license file exists, redistribution permission has not been established.

## Verified in-tree

| Collection | License | Evidence |
|---|---|---|
| `academic-research-skills/` | **CC BY-NC 4.0** | `LICENSE` (Copyright © 2026 Cheng-I Wu), `NOTICE.md`, `CITATION.cff` |
| `claude-scholar/` | **MIT** | `LICENSE` (Copyright © 2026 Gaorui Zhang) |
| `paper-craft-skills/` | **MIT** | Stated in the upstream `README.upstream.md`; no separate LICENSE file in the source archive |
| `scipilot-figure-skill/` | **MIT** | `LICENSE` bundled with the skill |

### ⚠️ Non-commercial restriction

`academic-research-skills/` is licensed **CC BY-NC 4.0 — NonCommercial**. Redistribution is permitted with attribution, but **commercial use is not**. This is a different license from the rest of this plugin (MIT) and from the Paper-gogo workflow package. If you intend commercial use, remove `workflow/extras/academic-research-skills/` and update this file.

## Bundled skills per collection

| Collection | Skills |
|---|---|
| `academic-research-skills/` | `academic-paper`, `academic-paper-reviewer`, `academic-pipeline`, `deep-research` |
| `claude-scholar/` | `citation-verification`, `ml-paper-writing`, `paper-self-review`, `review-response`, `publication-chart-skill`, `latex-conference-template-organizer`, `research-ideation`, `results-analysis`, `results-report`, `daily-paper-generator`, `writing-anti-ai`, `obsidian-literature-workflow`, `zotero-obsidian-bridge`, `doc-coauthoring`, `bug-detective`, `code-review-excellence`, `verification-loop`, `git-workflow`, `agent-identifier` |
| `paper-craft-skills/` | `paper-analyzer`, `paper-comic`, `paper-deck` |
| `scipilot-figure-skill/` | `scipilot-figure-skill` |

## What was deliberately excluded

- **Media assets** (PNG/JPG/PDF/ZIP) were stripped from every vendored collection to keep the plugin small. Skills whose upstream behaviour depends on bundled images (notably `paper-comic` and `paper-deck`) will have reduced fidelity. All instructions, references and scripts are preserved.
- **claude-scholar's `nature-*` skills** were excluded because they are byte-identical to the copies already vendored under `workflow/skills/nature-skills/`. Verified by SHA-256 comparison of every file.
- **`skills-main`** (Matt Pocock engineering skills) — already fully represented by `workflow/skills/architecture-engineering/` and `workflow/skills/code-understanding/`.
- **Unrelated collections** — `gsap-skills`, `stock-analysis`, `ponytail`, `codex-plusplus`, `agency-agents`, `shushu-internship-tool`, `Auto-claude-code-research-in-sleep` (181 skills, dominated by unattended overnight-loop automation that conflicts with this workflow's user-confirmation gates), and `codegraph` (developer tooling for its own project, no license file).

## Required action

1. Confirm the upstream source and license of `paper-craft-skills` (MIT stated in README only).
2. If this plugin will be used commercially, remove the CC BY-NC collection listed above.
3. Keep the bundled `LICENSE` files alongside their collections — they are the attribution mechanism.
