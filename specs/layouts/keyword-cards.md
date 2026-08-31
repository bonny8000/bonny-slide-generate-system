---
id: keyword-cards
kind: layout
tier: organism
status: stable        # example built + render-validated
intent: present a few parallel values / keywords / principles as equal cards
triggers: [3–4 values or principles, "our keywords", parallel ideas each with a short explanation, 核心理念, 幾個關鍵字等重呈現, 我們的準則, 設計原則, 理念並列呈現]
material: text-only
arrangement: grid
item_count: few
alternates: [terminology-cards]
depends_on: [tokens]
tokens_used: [canvas, surface, ink, muted, accent]
icon_use: optional
learned_from: Img20
example: examples/light-keyword-cards.html
---
# keyword-cards

## Purpose
3–4 equal cards, each a numbered keyword/value with a title and a short description.

## Intention & rationale
The job is to **present parallel ideas as equally important**. Why this form:
- **Equal cards signal equal weight** — these are values, not a ranking.
- **The numbered label** ("01 | Keyword") gives order and scannability without implying priority.
- **Restraint** (text-only, generous whitespace) keeps each value readable; a busy card would dilute it.

## When to use / When NOT
Use for values, principles, or themed keywords. **Not** for a ranked list (use `ranked-list`) or items
that each need a chart (use `numbered-rows`).

## Structure
Centered eyebrow (e.g. `{ GROWTH }`). 3–4 equal `--surface` cards, each: **numbered label header**
("01 | Keyword", number in `--accent`) → bold 2-line **title** (`--ink`) → muted **paragraph**. Optional
footer deck-chrome (logo / copyright / page number, `--muted`).

## Tokens used
canvas, surface (cards), ink (titles), muted (descriptions + footer), accent (the number/label).

## Icon use
Optional; usually none — restraint is the point.

## Content rules
3–4 cards, parallel structure, equal height. Title = the value (one claim); description muted; accent only
the number/label.

## Do / Don't
- **Do** keep cards equal and parallel.
- **Don't** exceed 4 cards or accent the whole title.

## Example
"{ GROWTH }" + three "0N | Keyword" value cards with bold titles + muted paragraphs (learned from Img20).

## Human preference refinement
R51 B (2026-08-31): compose the header and compact card group together at the centre; avoid a detached top-pinned header.
