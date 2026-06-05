---
id: how-themes-work
kind: theme-guide
status: stable
---
# How themes work

A theme is **one token set for one mode**. The deck loads exactly one. Components/layouts reference the
token names below; the theme supplies the values. See `foundations/themes-and-modes.md` for the rule.

## Required token roles (a theme must define all)
`--canvas --surface --ink --muted --muted-soft --accent --accent-soft --band-fill --pos --neg --warn`

## Shipped themes
- `light-periwinkle` — near-white canvas, periwinkle accent. Editorial deck feel.
- `dark-periwinkle` — near-black canvas, brighter blue accent. Premium poster feel.

## Adding a theme (keep the discipline)
1. Choose **one** accent hue + its soft tint.
2. Set neutrals for the mode (canvas, surface, ink, muted, muted-soft).
3. `band-fill` = the text color (light mode) or a near-canvas dark (dark mode).
4. Keep semantic pos/neg/warn legible on the canvas.
5. Do **not** add a second accent. Validate with `audit.md`.

Valid accents seen in references (each used alone, deck-wide): green, orange, yellow, navy, blue, purple.
