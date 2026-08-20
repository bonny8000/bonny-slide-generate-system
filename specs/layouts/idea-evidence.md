---
id: idea-evidence
kind: layout
tier: organism
status: stable        # example built + render-validated
intent: pair a design idea with the evidence that backs it
triggers: [an idea/claim + a supporting chart or stat, "we think X — here's why", two-column idea vs proof, 想法配證據, 一個主張加佐證, 設計想法與支持數據, 設計想法, 想法與佐證]
material: chart
arrangement: split
item_count: one
alternates: []
depends_on: [barchart, tokens]
tokens_used: [canvas, surface, ink, muted, muted-soft, accent]
icon_use: none
learned_from: Img5
example: examples/light-idea-evidence.html
---
# idea-evidence

## Purpose
Two panels: the design idea (with a small chart) on one side, the survey stat + reasoning on the other.

## Intention & rationale
The job is to **make a claim credible on the same slide**. Putting the idea and its proof side by side
stops the audience asking "says who?" — the **evidence answers the idea immediately**. The accent marks
the idea's key phrase and the proof number, so the eye links cause and support.

## When to use / When NOT
Use for one idea + one piece of evidence. **Not** for many findings (use `numbered-rows`) or a metrics
recap (use `results-grid`).

## Structure
Header. Body (`.grow`): two equal `--surface` panels. **Idea panel** = a claim (accent keyword) + a small
`barchart` + a one-line note. **Evidence panel** = a big stat (`--accent`) + reasoning text.

## Tokens used
canvas, surface (panels), ink (claim), muted/muted-soft (note, inactive bars), accent (keyword, active bar, stat).

## Icon use
None — let the chart and number carry it.

## Content rules
One idea + one stat per slide. Accent the idea keyword and the stat only.

## Do / Don't
- **Do** keep the two panels balanced and directly related.
- **Don't** crowd in a second idea.

## Example
"先看到共同點，再決定參加" + an ascending bar chart | "68%" + reasoning (learned from Img5).
