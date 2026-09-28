# paper-framework-figure-studio-pro v3.1.4a

Publication-oriented framework-figure workflow for computer-science papers.

Core route:

```text
S0-PAPER-FOUNDATION -> S1-FIGURE-STRATEGY -> S2-SKETCH-EXPLORE -> S3-DIRECTION-SELECT -> S4-CANDIDATE-BRIEF -> S5-CANDIDATE-IMAGE -> S6-FINAL-SELECT -> S7-FINAL-JOINT-AUDIT
```

Highlights:

- Strict human-in-the-loop alternation: one user turn executes at most one explicitly requested workflow step, then stops.
- Every step explicitly states that the current stage has ended; S0-S6 also state that the next stage has not been executed.
- Multi-choice text stages provide both the default-choice prompt and a placeholder prompt for user-selected options.
- S2 generates 6-8 broad low-fidelity raster sketches; story/metaphor sketches must stay close to the paper and use common concepts.
- S3 completion offers two S4 prompt branches: preserve hand-drawn reference-image character, or default to clean formal figure-caption co-design.
- S4 prepares per-candidate figure title, explanation, legend, text budget, visible core-step plans, claimed improvement anchors, symbol/formula necessity proof, and arrow/color/icon semantic contracts before S5.
- S5 formal candidates default to clean publication schematic raster images with paper-relevant icons, precise arrows/colors, and style-aware caption plans.
- S6 selects the final S5 candidate and drafts the figure title, style-aware caption, legend, body-reference text, and manuscript note.
- S7 performs a bounded joint audit of the selected image and text package, returning PASS/TEXT-REPAIR/IMAGE-REPAIR/DIRECTION-REPAIR.
- Re-entering S7 cleans prior S7 products and records a cleanup event while preserving S0-S6 inputs.
