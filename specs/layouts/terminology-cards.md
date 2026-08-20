---
id: terminology-cards
kind: layout
tier: organism
status: stable
intent: establish shared vocabulary so a mixed room means the same thing
triggers: [glossary, what we mean by X, X means..., key terms, definitions, 3 terms, 名詞解釋, 統一名詞, 術語定義, 講的是同一件事]
depends_on: [terminology-card, tokens]
tokens_used: [canvas, surface, ink, muted, accent]
icon_use: required
learned_from: Img12
example: examples/dark-06-terminology.html
---
# terminology-cards

## Purpose
Define a small set of key terms visually, so a mixed room shares the same vocabulary.

## When to use / When NOT
Use for a glossary / "what we mean by X" slide (3 terms ideal). **Not** for more than ~4 terms (split or
use a list).

## Structure
Eyebrow + centered title. A row of 3 **terminology-cards**, each:
`[illustration] [Keyword n label] [term] [definition]`. Optionally a paired **EXAMPLE card** beneath each.

## Tokens used
canvas, surface (cards), ink (definition), muted (keyword label / example), accent (the term).

## Icon use
**Required** — one illustration per term, one consistent illustration style, limited to theme colors
(2-tone: neutral + accent). See `foundations/iconography.md`.

## Content rules
3 terms. Term in `--accent`; definition ≤ 2 lines; example concrete and short. 繁中 primary.

## Do / Don't
Do keep all illustrations in one style + size. Don't use full-color stock art; don't write paragraphs.

## Example
3 columns: illustration + term + definition, each with an EXAMPLE card below (Img12).
