# Bonny Slide System v9 — agent skill

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
assets/           # base.css + tokens-light.css / tokens-dark.css   (real implementation)
examples/         # rendered reference slides (single layouts) + deck-demo/ & deck-demo-scroll.html = a full short deck (chaining, bridges, dividers)
pptx/             # python-pptx bridge (same tokens)
```

## Source of truth
`assets/tokens-*.css` = canonical token **values**; `specs/themes/*.md` document them. `specs/*` =
canonical **rules**. Components/layouts never hardcode color.

— v9 · 2026.06 · patterns mined from 12 reference decks
