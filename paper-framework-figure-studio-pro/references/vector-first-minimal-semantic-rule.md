# Vector-First Minimal Semantic Rule

Use this rule whenever S1-S7 decide what a research-paper framework figure should show.

Vector-first is no longer the dominant design objective in v3.1.4a. S2/S5 output generated raster images, not SVG. The useful part of vector-first is only this: avoid fused, unreadable geometry when a clean paper figure would benefit from separable modules, icons, and connectors. Do not force a candidate to look SVG-oriented when another paper-faithful style communicates the paper better.

Default figure shape:

- one clear visual sentence;
- 3-6 main modules;
- one dominant flow and 0-3 secondary flows;
- few large landmark icons;
- short labels;
- usually no formulas or symbols unless the designer can state why the paper's core idea cannot be expressed without them.
- caption/legend/body text that completes the image instead of forcing all explanations into pixels.

Minimal does not permit deleting non-droppable core substeps. If the source-grounded method depends on a sequence such as train -> generate, filter -> use, score -> weight, or evaluate -> update, S5 formal candidates must preserve that sequence in the generated image body, connected inset, zoom/cutaway, or compact mechanism panel. Captions may explain visible steps, but they must not be the only carrier.

If the paper presents a core innovation through substantial method prose, formulas, or explicit "improvement" language, the figure must include a clear visual anchor for that innovation. The anchor may be a module-internal mechanism, a formula token, a comparison/gating mark, an update loop, a before/after contrast, or a highlighted transformation, but it cannot be absent from the image.

Entity icons must be chosen for paper meaning and explanatory power. Generic icon style is allowed, but the icon's semantic role must match the paper's domain entities, model modules, algorithm operations, data objects, or evaluation concepts. Ease of SVG redrawing is secondary and must not override semantic clarity.

S6 absorbs important details removed from the pixels into title, caption, legend, body-reference text, and manuscript note. S7 audits whether the figure-caption bundle is complete, paper-faithful, and precise.
