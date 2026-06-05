---
name: bonny-slide-system
kind: agent-skill
version: 9.0.0
description: Build, critique, and iterate bilingual 繁中 + English UX/product slides and decks (HTML per-slide, single-scroll HTML, PDF, or PPTX). The agent READS specs/ (the LLM-readable design system) each run and BUILDS with assets/ (the real CSS). Color is a separate, deck-wide theme layer; layouts/components are theme-agnostic. Strict 4-color discipline, Noto Sans TC + Arial, 12-col grid, plain-language titles, a disciplined icon/illustration layer, and a content→layout map so naked text becomes a good slide. Korean is never produced.
---

# Bonny Slide System — agent skill

## When to use
Any time the user wants to make, fix, or critique slides/decks for UX or product work, bilingual
繁中 (primary) + English (supporting).

## How this skill is organized
- **`specs/`** — the LLM-readable design system you READ each run. Source of truth for *rules*:
  `foundations/` (color-discipline, themes-and-modes, typography, spacing-grid, layout-balance,
  iconography, plain-language, storytelling) · `themes/` · `tokens/` · `components/` · `layouts/` ·
  `content-map.md` · `audit.md` · `spec-template.md` · `_catalog.md`.
- **`assets/`** — the real CSS you BUILD with. `base.css` (theme-independent: type, spacing, grid,
  components) + ONE theme file (`tokens-light.css` / `tokens-dark.css`). Source of truth for *token values*.
- **`examples/`** — rendered reference slides; **`examples/deck-demo/`** + `deck-demo-scroll.html` = a full short deck showing how layouts chain (pacing, bridges, dividers). **`pptx/`** — token-mirrored python bridge for .pptx.

## Operating procedure (every deck)
1. **Inputs:** audience/room; **one theme** (mode + accent) — ask if unstated; the content/source.
2. **Load rules:** read `specs/foundations/*` + the chosen `specs/themes/<theme>.md`. Lock the theme deck-wide.
3. **Plan slides:** for each content chunk, find its shape in `specs/content-map.md` → layout + components.
   For a system/decision, order it method → range → relationships → conclusion (`specs/foundations/storytelling.md`).
4. **Build:** write HTML with `assets/base.css` classes + the theme token file. **Token names only —
   never hardcode color.** Icons per `specs/foundations/iconography.md`.
5. **Write plainly:** every title/caption passes `specs/foundations/plain-language.md`.
6. **Audit:** run `specs/audit.md`; fix blockers + majors.
7. **Output:** per-slide HTML, single-scroll HTML, PDF, or PPTX (`pptx/`). Render-check before delivering.

## Golden rules (never break)
- **One theme per deck** — color is a separate layer; layouts/components stay theme-agnostic.
- **4-color discipline** — accent is the only chromatic color.
- **繁中 primary + English supporting; no Korean.**
- **One claim per slide; plain-language titles; purposeful icons, one style.**
- For a system/decision, **show the reasoning before the conclusion.**

## Extending the system
- New component/layout → copy `specs/spec-template.md`, fill it, add a class to `assets/base.css`
  (or include inline CSS in the spec example), update `specs/_catalog.md`. `todo` items in the catalog
  are built by composing existing `base.css` primitives per their spec until a class exists.
- New theme → copy a `specs/themes/*.md`, keep the role names, **one accent**. Run `audit.md`.

## Changelog
- **v9** — unified into an agent skill: LLM-readable `specs/` library (color-as-separate-theme-layer,
  first-class iconography, content→layout map, drift audit, spec template, catalog mined from 12 real
  decks) + the real `assets/` implementation + pptx bridge.
- **v8** — show-the-reasoning pattern, section cover (扉頁), bilingual tags, range-framing.
- **v6–v7** — plain-language layer, full component library, spacing/grid, two locked modes, PPTX bridge.
