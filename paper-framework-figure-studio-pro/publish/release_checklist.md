# Release Checklist

- [ ] Version is `3.1.4a`.
- [ ] Workflow is `S0-PAPER-FOUNDATION -> S1-FIGURE-STRATEGY -> S2-SKETCH-EXPLORE -> S3-DIRECTION-SELECT -> S4-CANDIDATE-BRIEF -> S5-CANDIDATE-IMAGE -> S6-FINAL-SELECT -> S7-FINAL-JOINT-AUDIT`.
- [ ] Strict human-in-the-loop alternation is enforced.
- [ ] Multi-choice text stages provide both default-choice and user-placeholder prompts.
- [ ] Initial bootstrap gate is enforced.
- [ ] S0 paper-foundation behavior is input-depth-sensitive.
- [ ] S2 generates 6-8 raster exploration sketches.
- [ ] S4 provides complete candidate text contracts before S5.
- [ ] S5 defaults to formal clean publication schematic raster candidates with paper-relevant icons, precise arrows/colors, and style-aware caption plans.
- [ ] S6 selects one final S5 image and provides title, caption, legend, body-reference text, and manuscript note.
- [ ] S7 performs bounded joint audit and returns PASS/TEXT-REPAIR/IMAGE-REPAIR/DIRECTION-REPAIR.
- [ ] Re-entering S7 cleans prior S7 outputs/records and records cleanup before rerun.
- [ ] `python scripts/figure_studio_architecture_audit.py --target . --fail-on-issue` passes.
- [ ] `python -m compileall -q scripts` passes.
- [ ] JSON templates validate.
- [ ] State init/validate/doctor smoke tests pass.
- [ ] Release path scanner reports no local absolute paths.
- [ ] Package zip name is `paper-framework-figure-studio-pro-v3.1.4a-skill.zip`.
