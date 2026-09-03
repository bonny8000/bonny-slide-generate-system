---
id: hidden-majority
kind: layout
tier: organism
status: stable        # example built + render-validated
intent: stop a small number being dismissed by showing the larger part it hides
triggers: [only a small percent so far, the rest have not got it yet, partial rollout risk, what this number hides, the visible part is not the whole, staged release exposure, tip of the iceberg, 只是冰山一角, 目前只有一小部分, 其餘的還沒拿到, 看不見的那一部分更大, 分批推送的風險, 아직 받지 못한 사용자]
material: stat
arrangement: opposed
item_count: pair
alternates: [pie-donut, delta-metric]
depends_on: [tokens]
tokens_used: [canvas, surface, muted, muted-soft, ink, accent, accent-soft, warn, warn-soft]
icon_use: none
learned_from: Ref-hidden-majority-2026-09-02
example: examples/light-hidden-majority.html
---
# hidden-majority

## Purpose
One whole split across a waterline: the small part that is already visible, and the larger part it is
still hiding.

## Intention & rationale
The job is to **stop the room dismissing a small number**. Why this form:
- **A donut or a single stat bar makes "1%" look trivial** — which is the correct reading only if the
  number is finished. When the remainder has simply not arrived yet, that reading is dangerous.
- **Splitting the whole across a waterline inverts the conclusion.** The same 1% becomes the leading
  edge of something larger instead of a rounding error.
- **The small part carries `warn`, the submerged part keeps the dominant surface.** Emphasis follows
  the argument, not the size: the visible sliver is what you must act on, the mass is what is at stake.
- **The waterline is labelled with what "so far" means** (how much is deployed, how far adoption has
  reached). Without that label the picture is just a proportion; with it, it is a forecast.

## When to use / When NOT
Use when a proportion's **unseen remainder is the point**: a staged rollout where few have the build, an
early incident, partial adoption.

**Not** for a settled proportion where the split is simply the fact — that is `pie-donut`. **Not** for a
before/after change over time — that is `delta-metric`. **Not** when the remainder is genuinely
irrelevant; this layout argues that it is not, and using it where the argument does not hold is a lie
told with a shape.

## Structure
- `.hm` — column: `.above`, `.water`, `.below`.
- `.hm .above` — the visible sliver: a `.tip` wedge in `warn-soft` with a `.fig` (number + label) beside it.
- `.hm .water` — the dashed waterline; `.cap` is right-aligned and names what has been reached so far.
- `.hm .below` — the submerged panel on `accent-soft`, holding the `.mass` silhouette and its `.fig`.
- `.hm .fig` — `.n` for the number, `.l` for the label. Both take their colour from the role of the side
  they sit on, never a literal.

## Asset policy
`none` — the whole thing is drawn from tokens and CSS shapes. No artwork is required or requested.
