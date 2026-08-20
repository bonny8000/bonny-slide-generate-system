---
id: hero-radial
kind: layout
tier: organism
status: stable        # example built + render-validated
intent: put one central concept at the middle with its facets radiating around it
triggers: [a core concept + surrounding facets, a center-out model, "X connects A/B/C/D", a framework hub, 核心概念放中間, 中心加周邊面向, 一個主軸展開幾個面向, 放射狀架構]
depends_on: [tokens]
tokens_used: [canvas, surface, ink, muted, muted-soft, accent, accent-soft]
icon_use: optional
learned_from: Img6
example: examples/light-hero-radial.html
---
# hero-radial

## Purpose
A central accent node with facet labels radiating around it, flanked by two supporting list-cards.

## Intention & rationale
The job is to **show one thing at the center of many**. The **central accent circle is the subject**; the
radial labels read as facets *of* it (not a sequence); the two side cards carry the inputs/outputs. The
geometry itself communicates "everything orbits this core."

## When to use / When NOT
Use for a center-out concept model / framework. **Not** for a sequence (use `flow`) or a continuum (use
`linked-circles`).

## Structure
Header. Body (`.grow`): 3 columns — left list-card, a **radial** (center `--accent` circle + 4 labels
positioned top/right/bottom/left), right list-card.

## Tokens used
canvas, surface (side cards), accent (core circle + labels accent), ink/muted (card text), muted-soft (label chips).

## Icon use
Optional; the core may hold an icon. Keep one style.

## Content rules
1 core + 3–5 radial facets; 2 side cards with ≤ 3 items each.

## Do / Don't
- **Do** make the center clearly dominant (size + accent).
- **Don't** let radial labels imply an order.

## Example
"使用者體驗核心" center + 情境/連結/成長/協助 radials + 輸入/輸出 side cards (learned from Img6).
