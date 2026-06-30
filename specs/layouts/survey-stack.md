---
id: survey-stack
kind: layout
tier: organism
status: stable
depends_on: [pie-donut, barchart, hbar, tokens]
tokens_used: [canvas, surface, ink, muted, accent]
icon_use: optional
learned_from: Img2
example: examples/light-03-survey-stack.html
---
# survey-stack

## Purpose
Present survey / Q&A results as a scannable stack — one row per question, each with its chart and a
one-line takeaway.

## When to use / When NOT
Use for user-survey result sets (3–6 questions). **Not** for a single stat (use metric) or open-ended
qual (use qual-quant-split / quotes).

## Structure
- **Left rail:** section eyebrow + title + sample stats (N, demographics) in muted.
- **Right:** vertical stack of **q-cards**, each = `[Q-badge] [question, 1 keyword in accent] [1-line
  insight, muted] [chart on the right: pie / bar / hbar]`.
- Equal card rhythm; charts right-aligned for a clean vertical edge.

## Tokens used
canvas, surface (q-cards), ink (questions), muted (insight + sample stats), accent (active chart slice/bar + keyword).

## Icon use
Optional small Q-badge / insight bullet icon; one style.

## Content rules
One question + one chart + one insight sentence per card. Highlight the answer that matters in `--accent`.
繁中 questions; numbers Latin.

## Do / Don't
Do keep one chart type per card and a consistent card height. Don't put two charts in one card; don't
let questions exceed two lines.

## Example
5 stacked q-cards (pie / bar / pie / pie / hbar) + a left rail with sample = 95, demographics (Img2).
