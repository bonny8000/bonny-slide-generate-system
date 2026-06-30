---
id: geo-map
kind: component
tier: molecule
status: stable        # example built + render-validated
intent: show where things cluster geographically
triggers: [region/country map, "X of Y in the capital area", spatial concentration, store/region counts]
depends_on: [tokens]
tokens_used: [surface, muted, muted-soft, ink, accent]
icon_use: none
learned_from: Img23
example: examples/light-painpoint-evidence.html
---
# geo-map

## Purpose
A simplified region map with the focus area highlighted and leader-line annotations + counts.

## Intention & rationale
The job is to **make concentration spatial and obvious** — "most are *here*" is felt on a map far faster
than in a sentence. The focus region in `--accent` carries the point; **leader lines tie counts to places**
so the numbers are grounded.

## When to use / When NOT
Use for geographic concentration / coverage. **Not** for non-spatial counts (use a chart).

## Structure
A simplified region silhouette (`--muted-soft`); the **focus region filled `--accent`** (or `--ink`);
**leader-line annotations** each with a label + count. Keep 2–3 annotations.

## Tokens used
muted-soft (silhouette), accent (focus region), ink (labels/counts), muted (leader lines).

## Icon use
None — leader lines and labels carry it.

## Content rules
≤ 3 annotations, each a place + count. One focus region in accent; rest neutral.

## Do / Don't
- **Do** keep it a simple silhouette with ≤ 3 annotations.
- **Don't** use a full-color cartographic map or introduce new hues.

## Example
A region silhouette with "首都圈 24 / 其他 11" leader-line annotations, capital area in accent (learned from Img23).
