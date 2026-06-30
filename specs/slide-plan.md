---
id: slide-plan
kind: process
status: stable
---
# Slide plan — decide each page's structure FIRST (the outline stage)

The make-a-slide engine has **two stages, in order**:
1. **`slide-plan.md` (this file)** — turn the raw file into a page-by-page plan. *Structure first.*
2. **`content-map.md`** — for each planned page, pick the layout + components. *Visuals second.*

Never pick a component before the page's job is decided. Structure first stops the AI from decorating
text it hasn't understood.

## Input → output
- **Input:** the raw content/source (a doc, notes, findings, a transcript).
- **Output:** an ordered **page plan** — one row per slide, no visuals chosen yet:

| # | The ONE claim (繁中 + EN handle) | Intention (the job) | Narrative slot | Content shape (hint) | Source ref |
|---|---|---|---|---|---|
| 1 | … | what this page must DO to the audience (persuade / teach / compare / prove / orient …) | cover / context / method / range / relationships / conclusion / section-cover | (a guess; `content-map` decides) | … |

## How to build the plan
1. **Segment.** Split the file into slides. One slide = **one claim** (golden rule). If a chunk carries
   two claims, split it; if three chunks repeat one claim, merge them.
2. **State each claim.** Write the single sentence each page must land, 繁中 primary + a short English
   handle. This becomes the plain-language title later (`foundations/plain-language.md`).
3. **Name the intention.** For each page, say what it must *do* to the audience — persuade, teach,
   compare, prove, orient, provoke, re-orient. **Intention is the primary key** `content-map.md` selects
   on, so naming it here is what lets stage 2 pick the right layout (not just a plausible-looking one).
4. **Order the narrative.** For a system/decision, sequence **method → range → relationships →
   conclusion** — reasoning before the result (`foundations/storytelling.md`). Never lead with the
   final model.
5. **Place the scaffolding.** Add `cover`, `toc`, a `section-cover` (扉頁) between major parts, and a
   one-line **bridge** opening each deep-dive. Mark these as their own rows.
6. **Hint the shape, don't bind it.** Note a likely content shape per row, but leave layout/component
   selection to `content-map.md` — the hint is a guess, not a decision.

## Ask for assets
While planning, flag any page whose intention needs a **real asset** — a product screenshot, a logo, a
photo, a data export — and **ask the user to provide it** before building (`foundations/imagery.md`). Name
exactly what you need and why; offer a fallback (skeleton mockup / recolored placeholder, labeled
representative) if they don't have it. Don't fabricate screenshots or precise data.

## Hand-off
Each finished row is passed to `content-map.md` (shape → layout + components). The plan also gives the
deck its **pacing** (how layouts chain — see `examples/deck-demo/`).

## Do / Don't
- **Do** decide the whole deck's structure before building any single slide.
- **Do** keep the plan theme-agnostic — color is decided once at the deck level, not here.
- **Don't** name components, charts, or layouts in this stage.
- **Don't** let a page hold more than one claim.
