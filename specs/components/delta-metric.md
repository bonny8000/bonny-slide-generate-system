---
id: delta-metric
kind: component
tier: molecule
status: stable
intent: prove a change by pairing a big +/-% with its before/after bars
triggers: [before to after, "improvement %", 改善前/改善後, result over a period, impact metric]
depends_on: [barchart, tokens]
tokens_used: [ink, muted, muted-soft, accent]
icon_use: none
learned_from: Img1
example: examples/dark-07-kpi-results.html
---
# delta-metric
## Purpose
Headline a change: a big ±% with a before/after bar chart.
## When to use / When NOT
Use for a result/impact metric over a period. Not for a static single number (use metric).
## Structure
Header: `[label --ink] [big ±% --accent]` + a mini legend (改善前 = muted, 改善後 = accent).
Below: a `barchart` where the "after" bars are `.active` (accent), the "before" bars muted.
## Tokens used
ink (label), accent (% + active bars), muted/muted-soft (before bars + legend).
## Icon use
None.
## Content rules
One % per block. Keep the accent on the improved series only. Both "good up" and "good down" use accent
(it's the deck's single highlight) — don't introduce a second color.
## Do / Don't
Do label what the % is vs. Don't color before and after with two different hues.
## Variant — delta pill
`learned_from: Ref-delta-pill-2026-09-03` · `example: examples/light-delta-pill.html`

State the change **at** the bar instead of in the header. A dashed `.was` line marks where the value
used to be and a `.dpill` on that line names the gap. Put `.delta` on the "after" `.barcol` and set
`--rise` to how far the previous value sat above this bar's top. `--lead` is how far left the line
runs, as a percentage of the bar's width — reach it back to the bar being quoted, so the line is a
connection between two heights rather than a floating rule.

Why it is a separate rendering and not just a smaller header: with only two bars, a header ±% asks the
audience to hold a number while they look for the two heights it came from. The dashed line gives the
comparison a mark on the canvas, so the drop is measured against something visible rather than against
the neighbouring bar's height. Use it for exactly two periods; with a series, the header form reads
better because there is no single "before" to draw a line at.

**The pill takes `accent`, not `pos`** — even when the change is good news, and even though the source
figure was green. The rule below holds: one highlight colour per deck. A green pill here would make
this slide's good news a different colour from every other slide's emphasis.

## Example
"每月申請件數 +25%" with 6 monthly bars, last 3 active (Img1).
