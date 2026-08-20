---
id: use-case-cards
kind: layout
tier: organism
status: stable         # example built + validated: examples/light-use-case-cards.html
intent: show who the product serves — audience segments / use cases
triggers: ["use cases", audience segments, "serving every X", 3 customer types each with an illustration, 服務哪些客群, 應用情境, 目標客群分類, 使用情境]
depends_on: [ui-mockup, tokens]
tokens_used: [canvas, surface, muted, muted-soft, ink, accent, band-fill]
icon_use: optional
learned_from: Img26
example: examples/light-use-case-cards.html
---
# use-case-cards

## Purpose
3 cards, each an audience/use-case with a badge, an illustration, and a caption.

## Intention & rationale
The job is to **show breadth of who it serves**. Why this form:
- **One card per audience makes coverage explicit** — "we serve all of these."
- **A consistent recolored illustration per card** gives each segment identity without breaking the
  palette (`foundations/imagery.md`).
- **A dark pill badge** names the segment crisply at the top of its card.

## When to use / When NOT
Use for audience segments / use cases. **Not** for feature walkthroughs (use `feature-showcase`) or values
(use `keyword-cards`).

## Structure
**Split header** (big title left + supporting paragraph right) + eyebrow. 3 cards, each: a **dark pill
badge + icon** (top-left), a **recolored line-illustration / `ui-mockup`** filling the card (one style,
accent-toned), and a **caption paragraph** below.

## Tokens used
canvas, surface (cards), muted/muted-soft (illustration neutrals, caption), ink (title), accent
(illustration highlight), band-fill (badges).

## Icon use
Optional badge icon, one style; illustrations recolored to one accent + neutrals.

## Content rules
2–4 cards, parallel; one badge + one illustration + one caption each. One illustration style across cards.

## Do / Don't
- **Do** keep one illustration style deck-wide.
- **Don't** use full-color stock art that adds hues.

## Example
"Serving every player in the renovation industry" — Installers / Assessors / Energy providers cards, each a
badge + a blue line-illustration + a caption (learned from Img26).
