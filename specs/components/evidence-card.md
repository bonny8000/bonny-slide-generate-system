---
id: evidence-card
kind: component
tier: molecule
status: stable
depends_on: [tokens, logo-row, barchart]
tokens_used: [surface, ink, muted, accent, accent-soft]
icon_use: optional
learned_from: Img8
example: examples/light-08-evidence-trio.html
---
# evidence-card
## Purpose
One card carrying a single piece of evidence — an icon-stat, a chart, or a logo-row.
## When to use / When NOT
Use 2–3 in a row to back a framing question (`centered-question-evidence`). Not as a generic content card.
## Structure
`--surface` card, centered: one of {icon-stat (figic + stat number) · a small chart · a logo-row} + a
one-line caption (`--muted`). Equal width and min-height across the row.
## Tokens used
surface, ink (stat), muted (caption), accent + accent-soft (icon).
## Icon use
Optional: a single figure icon for the stat variant (theme-colored, one style).
## Content rules
One figure/visual + one caption per card. Keep the three cards parallel.
## Do / Don't
Do keep all three the same height. Don't mix three of the same evidence type.
## Example
276,499 member stat · participation bar · app logo-row (Img8).
