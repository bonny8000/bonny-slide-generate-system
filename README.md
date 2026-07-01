# Bonny Slide System v12.5 — agent skill

Bilingual 繁中 + English UX/product slides. The agent **reads `specs/`** (the LLM-readable design
system) and **builds with `assets/`** (the real CSS), then runs the **drift audit**.

## The core ideas
- **Color is a separate layer.** A deck picks one theme; every slide uses it; layouts/components are
  theme-agnostic (token names only). The 4-color discipline is fixed; hues are swappable per deck.
- **Icons are first-class but disciplined** — one style per deck, theme-colored, purposeful.
- **A content→layout map** turns naked text into the right slide instead of guessing.
- **A mandated audit** catches drift (mixed theme, 2nd accent, raw colors, tiny text, mixed icon styles).

## Layout
```
SKILL.md          # agent operating manual (read this first)
specs/            # foundations · themes · tokens · components · layouts · content-map · audit · spec-template · _catalog
system/           # canonical tokens + hypertokens + recipes + JSON schemas
scripts/          # deterministic compiler for CSS / PPTX / generated reference docs
assets/           # linked base.css + generated import-free base bundle + theme outputs
examples/         # rendered reference slides (single layouts) + deck-demo/ & deck-demo-scroll.html = a full short deck (chaining, bridges, dividers)
pptx/             # python-pptx bridge (same tokens)
```

## Source of truth
`system/*.json` = canonical token values, hypertoken fragments, and pilot recipes. Run:

```powershell
python scripts/compile_system.py
python scripts/compile_system.py --check
```

Generated CSS/Python/Markdown must not be edited by hand. `specs/*` remains canonical for design rules,
intention, and component/layout selection. Migration status never affects selection, so the pilot does not
restrict the existing catalog.

Use `assets/base.css` for linked HTML. For self-contained HTML, inline
`assets/generated/base-bundle.css` plus exactly one `assets/tokens-*.css` theme.

— v12.5 · 2026.06 · hypertoken pilot + intention-first component library

## Tier mapping (vs the atomic-design diagram)
`components/` = **atoms + molecules** · `layouts/` = **organisms** (whole-slide, product-specific). Same tiering and one-way dependency as foundations → tokens → components → layouts; named for slides rather than a UI library.
