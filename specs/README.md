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
2. For each chunk of content, use `content-map.md` to pick a **layout** and **components**.
3. Build using `components/*` and `layouts/*` specs (token names only).
4. Run `audit.md` on the result; fix blockers/majors before delivery.

## Folders
- `foundations/` — rules that never change per deck: color discipline, themes/modes, typography, spacing+grid, layout balance, **iconography**.
- `themes/` — the swappable color layer. One per deck.
- `tokens/` — token name reference (the contract components depend on).
- `components/` — atoms/molecules. One spec each. Theme-agnostic.
- `layouts/` — full-slide patterns (organisms), mined from real decks.
- `content-map.md` — naked content shape → layout + components. The "make a slide" engine.
- `audit.md` — drift checks + severities.
- `spec-template.md` — the shape every component/layout spec follows.
- `_catalog.md` — full inventory + what each pattern was learned from.

## Status
Foundations, themes, content-map, audit, template = written. Components/layouts = core + new ones
written as gold standard; the rest catalogued in `_catalog.md` as `todo` to fill from real slides.
