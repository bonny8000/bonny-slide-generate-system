---
id: ranked-list
kind: component
tier: molecule
status: stable        # example built + render-validated
intent: show prioritized needs/requirements in explicit rank order
triggers: ["第一優先/第二優先", priority list, ranked needs, top-N requirements, "what matters most" panel]
depends_on: [tokens]
tokens_used: [surface, ink, muted, accent, band-fill]
icon_use: optional
learned_from: Img9, Img16
example: examples/light-positioning-matrix.html
---
# ranked-list

## Purpose
A vertical stack of ranked items — each a rank badge + the item — usually a side panel derived from a
`comparison-table`.

## Intention & rationale
The job is to **make priority unmistakable**. Why this form:
- **The rank order itself is the message** — the badge (1순위 / #1) turns a list into a ranking, so the
  audience absorbs "what matters most" at a glance.
- **One line per item** keeps the priority *sequence* readable; detail lives in the table it's derived from.

## When to use / When NOT
Use beside a `comparison-table` (the `comparison` layout) or wherever needs are prioritized. **Not** for an
unordered list (use chips/cards) or a process (use `stepflow`).

## Structure
3–5 stacked cards/rows on `--surface`, each: a **rank badge** (`--band-fill` or `--accent`) + the item
(`--ink`, 繁中, one line). Order top→down by priority.

## Tokens used
surface (cards), ink (item text), muted (optional sub-note), accent / band-fill (rank badge).

## Icon use
Optional; the rank badge usually suffices.

## Content rules
3–5 items, one line each, ordered by priority. Bilingual: item in 繁中, optional EN handle.

## Do / Don't
- **Do** order strictly top→down by rank; keep items one line.
- **Don't** mix unranked items in, or let an item wrap to a paragraph.

## Example
A 3-item "習慣形成所需功能" panel (1순위/2순위/3순위) beside a competitor comparison table (Img9, Img16).
