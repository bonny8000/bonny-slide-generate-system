---
id: value-points
kind: layout
tier: organism
status: stable        # example built + render-validated
intent: justify "why us" with a few value points, each backed by a concrete supporting card
triggers: ["why X?", 2–3 value points each with a paragraph + a backing visual/tag cluster, a sell slide, 為什麼選我們, 價值主張加佐證, 我們的優勢]
material: illustration
shape_variants: ["text-only / rows / few"]
arrangement: rows
item_count: few
alternates: []
depends_on: [taglist, tokens]
tokens_used: [canvas, surface, ink, muted, muted-soft, accent]
icon_use: optional
learned_from: Img25
example: examples/light-value-points.html
---
# value-points

## Purpose
2–3 value points side by side, each a short claim plus a supporting card (often a tag cluster).

## Intention & rationale
The job is to **make "why us" concrete**. Why this form:
- **A claim like "we cover everything" is abstract** — a **`taglist` cluster makes breadth visible and
  scannable**, so the reader sees the coverage instead of being told about it.
- **The accent count/keyword** in the card title ("9,000+") is the proof phrase (intention → emphasis).

## When to use / When NOT
Use for a "why us" / differentiator slide. **Not** for equal values with no backing (use `keyword-cards`)
or a single point (use `statement`).

## Structure
Eyebrow-with-rule ("Why VDOT? ———"). 2–3 points side by side, each: a **"Point N ."** label (accent dot) +
a muted paragraph + a **supporting card** (a `taglist` cluster, accent count/keyword in its title).

## Tokens used
canvas, surface (cards), ink (labels), muted/muted-soft (paragraphs, chips), accent (point dot + count/keyword).

## Icon use
Optional; usually none beyond the accent point dot.

## Content rules
2–3 points, parallel; paragraph short; one backing card each; accent the count/keyword only.

## Do / Don't
- **Do** back each point with a concrete card.
- **Don't** let paragraphs run long or accent the whole title.

## Example
"Why VDOT?" with Point 1 (Video Categories tag cluster) + Point 2 ("9,000+" Influencers tag cluster)
(learned from Img25).

## Text evidence variant
`text-only / rows / few` uses native supporting text in each evidence card when the brief contains
no illustration. Declare it before asset selection; policy `none`. The illustration variant keeps
its `generate` policy and must not be silently downgraded.

## Human preference refinement
R55 A (2026-08-31): equal peer labels and supporting chips may all use the same accent hue; do not arbitrarily demote later peers.
