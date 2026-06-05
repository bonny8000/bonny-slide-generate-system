---
id: themes-and-modes
kind: foundation
status: stable
---
# Themes & modes — color is a separate layer

**The rule:** a deck chooses **one theme**, and **every slide uses it**. Color does **not** depend on
the component or the content. Layout and component specs are **theme-agnostic** — they reference token
*names* (`--accent`, `--surface`…), never hex/px. Swapping the theme re-skins the whole deck without
touching a single layout.

## Why
Consistency is a **per-deck** property, not a per-slide one. If color lived inside components, two
slides using different components would look like different decks. Keeping color in one theme file,
applied deck-wide, is what makes a deck feel like one document.

## Discipline is fixed; hues are swappable
The **4-color discipline never changes**: 1 background + 1 text + 1 muted + 1 accent (accent = the only
chromatic color). A *theme* only supplies the actual values for those roles. The 12 reference decks
prove this — accents range across green, orange, yellow, navy, blue, purple, but **each deck is
internally one consistent style.** That is exactly the target behavior.

## A theme = a token set
A theme file fills every token role for one mode:
`canvas, surface, ink, muted, muted-soft, accent, accent-soft, band-fill, pos, neg, warn`.
**Mode** (light vs dark background) is part of the theme. One mode per deck.

## How to pick / add a theme
- Pick **one** accent. Set neutrals (canvas/surface/ink/muted) for the chosen mode. Keep `accent-soft`
  as a tint of the accent; `band-fill` as the text color (so bands/section-covers add no new color).
- To add a theme: copy an existing theme file, change the values, keep the role names. **Never add a
  second accent.**
- Choosing a theme is a **deck-level decision made once**, before building slides. Never choose color
  per slide or per component.

## What the audit enforces
One theme across the deck (blocker if mixed) · no raw colors in markup (token names only) · one accent.
