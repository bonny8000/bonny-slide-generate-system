---
id: feature-grid
kind: layout
tier: organism
status: stable        # example built + render-validated
intent: present a small set of features as equal, scannable cards
triggers: [3–4 features, "what's included", a 2×2 of capabilities each with an icon + blurb, 功能一覽, 幾個功能平均排開, 功能卡片並列, 包含哪些功能]
material: icon
arrangement: grid
item_count: few
alternates: [feature-showcase]
depends_on: [feature-card, tokens]
tokens_used: [canvas, surface, ink, muted, accent, accent-soft]
icon_use: optional
learned_from: Img11
example: examples/light-feature-grid.html
---
# feature-grid

## Purpose
A 2×2 (or 2×N) grid of `feature-card`s — each an icon/illustration + title + short description.

## Intention & rationale
The job is to **show a coherent set of features as peers**. The grid signals "these go together and are
equally part of the offer"; each card's icon gives quick recognition, the blurb gives just enough detail.

## When to use / When NOT
Use for a feature/capability set (3–4). **Not** for a ranked or sequential set (use `numbered-rows` /
`stepflow`) or a single hero feature.

## Structure
Header. Body (`.grow`): a 2×2 grid of `feature-card`s (icon in an `--accent-soft` tile + title + desc).

## Tokens used
canvas, surface (cards), ink (titles), muted (descriptions), accent + accent-soft (icon tiles).

## Icon use
One monochrome icon per card from a single set (accent on `--accent-soft`).

## Content rules
3–4 cards, parallel; one icon + title + one-line desc each.

## Do / Don't
- **Do** keep cards equal and the icon style consistent.
- **Don't** mix icon sets or let one card carry far more text.

## Example
照片日記 / 無痕記錄 / 成就回饋 / 彈性提醒 as a 2×2 (learned from Img11).
