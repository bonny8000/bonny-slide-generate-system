---
id: terminology-card
kind: component
tier: molecule
status: stable
depends_on: [tokens]
tokens_used: [surface, ink, muted, accent]
icon_use: required
learned_from: Img12
example: examples/dark-06-terminology.html
---
# terminology-card
## Purpose
Define one term with a supporting illustration.
## When to use / When NOT
Use inside `terminology-cards`. Not for data (use a chart).
## Structure
`--surface` card: illustration (top) + small keyword label (`--muted`) + term (`--accent`) +
definition (`--ink`/`--muted`). Optional paired EXAMPLE card below.
## Tokens used
surface, ink, muted, accent.
## Icon use
**Required** — one illustration, theme-colored 2-tone, one style across all cards.
## Content rules
Term in accent; definition ≤ 2 lines; example concrete. 繁中 primary.
## Do / Don't
Do keep illustration style + size identical across cards. Don't use full-color art.
## Example
Keyword 1 → TO-BE 自我 → definition → EXAMPLE card (Img12).
