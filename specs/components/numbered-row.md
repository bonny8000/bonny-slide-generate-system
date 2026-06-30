---
id: numbered-row
kind: component
tier: molecule
status: stable
depends_on: [tokens]
tokens_used: [ink, muted, accent, surface]
icon_use: optional
learned_from: Img10
example: examples/light-07-numbered-rows.html
---
# numbered-row
## Purpose
One numbered point with bilingual text and a chart beside it.
## When to use / When NOT
Use inside `numbered-rows`. Not standalone if there's no sequence.
## Structure
`[number badge, --accent] [headline --ink + description --muted (繁中 [+ EN])] [chart slot, --surface]`.
Grid: ~55% text / ~45% chart.
## Tokens used
accent (badge + active series), ink (headline), muted (description/caption), surface (chart card).
## Icon use
Optional numeric badge only.
## Content rules
Headline = the point; description 繁中 with optional EN second line. One chart.
## Do / Don't
Do align chart widths across rows. Don't separate the chart from its text.
## Example
"② 보청기 구매율 증가 → 助聽器購買率上升" + bar chart (Img10).
