---
id: numbered-rows
kind: layout
tier: organism
status: stable
intent: explain 2-4 sequenced points, each backed by its own chart
triggers: [1/2/3 points each with data, multi-point findings, numbered explainer rows, background points with charts]
depends_on: [numbered-row, line-chart, barchart, pie-donut, tokens]
tokens_used: [canvas, surface, ink, muted, accent]
icon_use: optional
learned_from: Img10
example: examples/light-07-numbered-rows.html
---
# numbered-rows

## Purpose
Explain 2–4 points in sequence, each backed by its own chart.

## When to use / When NOT
Use for a multi-point background/findings slide where each point has a data visual. **Not** for a flat
list (use cards) or a single point (use metric/statement).

## Structure
Optional eyebrow + intro (bilingual). Then 2–4 **numbered-rows**, each:
`[number badge] [bilingual headline + description, ~55%] [chart, ~45%]`.
Keep a consistent left-text / right-chart rhythm so the column edge stays clean.

## Tokens used
canvas, surface (chart cards), ink (headlines), muted (descriptions/captions), accent (number badge + one active series).

## Icon use
Optional: numeric badges (accent). No other icons needed.

## Content rules
2–4 rows. Headline = the point (繁中); description 繁中 with optional EN second line (muted). One chart
per row, beside its text.

## Do / Don't
Do keep one chart type per row and aligned chart widths. Don't exceed 4 rows; don't split a point's
chart from its text.

## Example
3 numbered rows (line / bar / pie), each with 繁中 + EN description (Img10).
