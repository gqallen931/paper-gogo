# Paper-gogo v2 release notes

This package preserves `paper-workflow-v5.md` as the historical baseline and repairs the executable v6 workflow.

## Main repairs

- Added explicit instruction precedence and non-skippable truth/evidence/ethics gates.
- Replaced unavailable ZIP-only skill references with bundled, readable skills.
- Changed literature work from a fixed 30-paper quota to a core/extended evidence corpus.
- Made experiments task-adaptive; cross-dataset, robustness, and ablation tests are required only when the claim and available data make them relevant.
- Excluded stubs, simulations, and incomplete runs from evidence, rankings, figures, and manuscript claims.
- Separated the Phase 5/9 concept-framework state from the Phase 13 final-framework state.
- Replaced per-figure “Graphical Abstracts” with figure briefs and one optional manuscript-level Graphical Abstract.
- Replaced imitation-oriented writing with author-confirmed claims and non-copying argument-structure analysis.
- Replaced “AI-removal rate” with language quality and authorial voice checks.
- Replaced acceptance probabilities with qualitative, evidence-based submission risk.
- Added GitHub setup guidance and repository hygiene defaults; updated for public release.

## Compatibility

- `paper-workflow-v5.md` remains available for historical reference.
- `paper-workflow-v6.md` is the active workflow.
- Both workflow files retain Chinese content but use ASCII-only filenames for cross-platform compatibility.
- Root `SKILL.md` is the package entry point.
