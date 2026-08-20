---
id: painpoint-evidence
kind: layout
tier: organism
status: stable        # example built + render-validated
intent: present a pain point backed by evidence — qualitative quotes and/or spatial/quant data
triggers: ["painpoint N", a problem + participant quotes, geographic concentration, evidence for a problem, 痛點佐證, 一個痛點加引述, 問題的證據, 使用者困擾與數據]
material: quote
arrangement: split
item_count: one
depends_on: [quote-bubble, geo-map, tokens]
tokens_used: [canvas, surface, ink, muted, muted-soft, accent, band-fill]
icon_use: optional
learned_from: Img23
example: examples/light-painpoint-evidence.html
---
# painpoint-evidence

## Purpose
A pain point split into sub-problems, each backed by concrete evidence (user quotes and/or a data/map).

## Intention & rationale
The job is to **make a pain point believable, not asserted**. Why this form:
- **A claimed problem is weak; evidence earns it.** Participant **quote-avatars** make it human; a **map or
  count** makes it factual — pairing qual + quant is more convincing than either alone.
- **Numbered "문제점 N" badges** chunk one pain point into its distinct causes.

## When to use / When NOT
Use for a research pain-point slide with supporting evidence. **Not** for the solution (use
`problem-solution`) or a single quote (use `quote-bubble`).

## Structure
Top band: pain-point label + title + muted sub. Two problem panels, each: a **"문제點 N" badge** + a
one-line finding + **evidence**, one of:
- a **row of participant quote-avatars** (`quote-bubble` + avatar + label), or
- a **`geo-map`** with leader-line annotations + counts.

## Tokens used
canvas, surface, ink (findings), muted/muted-soft (sub, map silhouette, quiet text), accent (focus region /
key phrase), band-fill (badges + top band).

## Icon use
Optional avatars (recolored toward palette, one style). Map markers are leader lines, not icons.

## Content rules
≤ 4 quote-avatars per row; ≤ 3 map annotations with counts; one finding per panel; quotes terse.

## Do / Don't
- **Do** back each sub-problem with concrete evidence.
- **Don't** use off-palette full-color stock art (recolor illustrated avatars; real photos are fine as content).

## Example
"Painpoint 3": panel 1 = 4 participant quote-avatars; panel 2 = a region map ("24 of 35 stores in the
capital area") (learned from Img23, structure only).
