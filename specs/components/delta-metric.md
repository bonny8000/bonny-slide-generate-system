---
id: delta-metric
kind: component
tier: molecule
status: stable
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
## Example
"每月申請件數 +25%" with 6 monthly bars, last 3 active (Img1).
