---
id: pie-donut
kind: component
tier: atom
status: stable
intent: show one proportion that matters
triggers: [single share, "one key %", yes/no split, proportion of a whole, 佔比]
depends_on: [tokens]
tokens_used: [muted, muted-soft, accent, ink]
icon_use: none
learned_from: Img2, Img3, Img10
example: examples/light-03-survey-stack.html
---
# pie-donut
## Purpose
Show one share/proportion that matters.
## When to use / When NOT
Use for a single dominant proportion (a yes/no split, one key %). Not for many categories (use hbar).
## Structure
Pie or donut. **Focus segment = `--accent`; all others `--muted` / `--muted-soft`.** Big % or center
number in `--accent` (or `--ink`); label beside.
## Tokens used
accent (focus), muted/muted-soft (rest), ink (center number/label).
## Icon use
None.
## Content rules
Highlight exactly one segment. Show the figure that matters large. ≤ 4 segments.
## Do / Don't
Do keep non-focus segments neutral. Don't color every slice; don't use a legend if labels fit inline.
## Example
Donut 73.0 center, rest muted, "상담 방문한 적 없다" (Img3); 65% yes/no pie (Img2).
