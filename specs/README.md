# Bonny Slide Design System — Spec Library (v1)

An **LLM-readable** slide design system: the agent reads these specs *every time* it builds a deck,
instead of reading one styleguide once and then drifting.

## The one big idea: color is a separate layer
A deck picks **one theme** (color + mode). **Every slide in that deck uses it.** Layout and component
specs are **theme-agnostic** — they reference token *names*, never hex/px. So the same layout renders
in any theme without editing the layout. Pick color once at the deck level; never per slide or per
component.

## How the agent uses this library
1. Read `foundations/` (the non-negotiable rules) + the chosen `themes/<theme>.md`.
2. **Structure first:** use `slide-plan.md` to turn the file into a page-by-page plan (one claim per slide).
3. **Visuals second:** for each planned page, use `content-map.md` to pick a **layout** and **components**.
4. Build using `components/*` and `layouts/*` specs (token names only).
5. Run `audit.md` on the result; fix blockers/majors before delivery.
6. **Learn:** when the user sends a reference slide image, run `foundations/learn-from-image.md` to fold
   its pattern back into the library (theme-agnostic — color stays a separate layer).

## Folders
- `foundations/` — rules that never change per deck: color discipline, themes/modes, typography, spacing+grid, layout balance, **iconography**.
- `themes/` — the swappable color layer. One per deck.
- `tokens/` — token name reference (the contract components depend on).
- `components/` — atoms/molecules. One spec each. Theme-agnostic.
- `layouts/` — full-slide patterns (organisms), mined from real decks.
- `slide-plan.md` — raw file → page-by-page plan (structure first). Stage 1 of the "make a slide" engine.
- `content-map.md` — naked content shape → layout + components (visuals second). Stage 2 of the engine.
- `audit.md` — drift checks + severities.
- `spec-template.md` — the shape every component/layout spec follows.
- `_catalog.md` — full inventory + what each pattern was learned from.
- `foundations/learn-from-image.md` — the loop that learns new theme-agnostic patterns from slide images.

## Status
Foundations, themes, content-map, audit, template = written. **Every component/layout spec is `stable`
with a render-validated example** (built from `assets/`, screenshot-checked per `foundations/self-critique.md`).
7 patterns remain `todo` in `_catalog.md` (catalogued, awaiting a source slide).
