---
id: feature-card
kind: component
tier: molecule
status: stable        # example built + render-validated
intent: present one feature with an icon, a title, and a short description
triggers: [a single feature/capability, an icon + title + blurb card, a cell of a feature-grid]
depends_on: [tokens]
tokens_used: [surface, ink, muted, accent, accent-soft]
icon_use: required
learned_from: Img11
example: examples/light-feature-grid.html
---
# feature-card

## Purpose
A card for one feature: an icon tile + a title + a one-line description.

## Intention & rationale
The job is to **make one feature recognizable fast**. The icon gives instant recognition, the title names
it, the muted blurb adds just enough. Used in a `feature-grid` so several read as peers.

## Structure
A `--surface` card: an **icon tile** (`--accent-soft` background, `--accent` monochrome icon) + **title**
(`--ink`) + **description** (`--muted`, one line). Icon may sit left of or above the text.

## Tokens used
surface (card), accent + accent-soft (icon tile), ink (title), muted (description).

## Icon use
Required: one monochrome icon from the deck's single set.

## Content rules
One icon + title + one-line desc. Keep titles parallel in length across a grid.

## Do / Don't
- **Do** match icon style to the rest of the deck.
- **Don't** let the description run to a paragraph.

## Example
"照片日記 — 先選一張照片，系統幫你帶出書寫的起點" (learned from Img11).
