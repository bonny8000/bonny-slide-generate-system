# README visuals

The main README uses current HTML screenshots for examples and inline Mermaid for architecture.
The old static explanation figures have been retired: they mixed stale counts, intention-first
routing claims, and an outdated recipe example with actual output. Diagram source now lives beside
the explanation it describes in [README.md](../../README.md).

## Screenshots

| Image | HTML source |
|---|---|
| `metrics-light.png` | [Light metric cards](../../examples/light-metric-cards.html) |
| `persona-light.png` | [Case-study personas](../../examples/case-study/04.html) |
| `kpi-dark.png` | [Dark KPI results](../../examples/dark-07-kpi-results.html) |
| `screen-interiors-light.png` | [Schematic screen interiors](../../examples/light-screen-interiors.html) |

These are full Chromium screenshots at 1920 × 1080 and device scale 1. They retain the browser's
actual text, shadows, clipping, and colors rather than approximating the DOM with vector primitives.
The sample content illustrates layouts; it is not verified research or real product performance.

## Refresh

From the repository root, with Python 3.10+ and Chromium installed:

```bash
python3 scripts/check_system.py
python3 scripts/render_readme.py
```

If auto-discovery cannot find the browser, pass its executable with `--browser`.
After CSS/token edits, run the compiler and example sync before these commands.
Inspect all four images at full size and in the rendered README. Do not retouch screenshots to
conceal a problem in a slide; fix the HTML/CSS and render again.

[`manifest.json`](manifest.json) records the source paths, viewport, and source/image SHA-256 hashes
for the last refresh. The sources currently embed their shipped styles. Hashes make those inputs
traceable; they do not automatically refresh images or certify their visual quality. Browser and font
differences can change the pixels. This helper is not part of the core CI checks.
