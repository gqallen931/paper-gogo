# Skill Architecture Review Guidelines

Review architecture changes against these checks:

- Workflow constants, state schema, artifact roles, image generation gates, cleanup helpers, and release checks remain separate.
- S0-S7 is the active step sequence, with S7 as a bounded final joint audit.
- S2/S5 target images remain generated raster images.
- S5 formal candidates are schematic raster references with paper-relevant icons, precise arrows/colors, visible core anchors, and style-aware caption plans; they are not SVG outputs.
- S6 includes final image selection plus figure text; S7 is terminal and audits the selected image plus text package.
- State files store relative paths only.
- Release packages contain no caches, temporary test outputs, or host-specific absolute paths.
