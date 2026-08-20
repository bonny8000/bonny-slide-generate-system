---
id: positioning-matrix
kind: layout
tier: organism
status: stable        # example built + render-validated
intent: show competitive/strategic standing in a space and the target position to move toward
triggers: [perceptual map, positioning map, 2 dimensions low↔high, option/brand markers, a "target"/goal point, 目標定位, 競品分析, 市場定位, 兩軸象限, 競品分布, 목표 지점, 포지셔닝]
material: text-only
arrangement: matrix
item_count: many
alternates: []
depends_on: [logo-row, tokens]
tokens_used: [canvas, surface, ink, muted, muted-soft, accent]
icon_use: optional
learned_from: Img15
example: examples/light-positioning-matrix.html
---
# positioning-matrix

## Purpose
A perceptual map: options/brands plotted on two axes, with the own/focus position and a target point
called out.

## Intention & rationale
The job is to **show standing and direction** — where everyone sits, and where we're going. Why this form:
- **Spatial position argues better than a list** — quadrant and distance are read instantly, so the
  audience *sees* who leads on which dimension.
- **The accented target + a beam/arrow from current → target turns analysis into a goal**, the single
  most important takeaway, so it gets the accent.
- **Pairs with a `comparison-table`** on the same slide: the table is the detail, the map is the synthesis
  (this is the competitive-analysis pattern — Img15).

## When to use / When NOT
Use for competitive positioning, prioritization (impact×effort), or any 2-dimension trade-off with a
goal. **Not** for a categorical 2×2 framework with fixed quadrant labels (use `matrix`).

## Structure
A `--surface` card: two axis lines crossing into 4 quadrants; **bilingual end-labels** on each axis
(`--muted`, low ↔ high); markers (dots or brand logos) placed by position; the **own/focus marker and the
target point in `--accent`** — target as a dashed accent ring, optionally with a soft beam/arrow from the
current position.

## Tokens used
canvas, surface (card), ink (marker labels), muted/muted-soft (axes, end-labels, other markers), accent
(own marker + target ring/beam).

## Icon use
Optional brand logos as markers. **Brand/competitor logos keep their real colors** — the one sanctioned
exception to monochrome (you can't recolor a logo); everything non-logo stays on-palette
(`foundations/iconography.md`).

## Content rules
Exactly 2 axes, both ends labeled bilingually; ≤ ~6 markers; exactly one target point. Own + target in
accent; all other markers muted/ink.

## Do / Don't
- **Do** reserve accent for the own-position + target; label both axis ends.
- **Don't** plot more than ~6 markers or add chromatic color beyond logos + the one accent.

## Example
A quality×awareness map with competitor logos placed, MUJI circled, and a dashed "目標位置" target with a
beam (learned from Img15, structure only).
