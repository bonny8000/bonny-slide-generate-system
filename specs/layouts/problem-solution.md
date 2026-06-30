---
id: problem-solution
kind: layout
tier: organism
status: stable        # example built + render-validated
intent: contrast the problem with the solution so the solution lands as the answer
triggers: [problem/solution, 문제/해결, as-is vs to-be, two opposing states, pain → fix]
depends_on: [tokens]
tokens_used: [canvas, surface, ink, muted, muted-soft, accent, band-fill]
icon_use: optional
learned_from: Img17
example: examples/light-problem-solution.html
---
# problem-solution

## Purpose
Two mirrored panels side by side — the problem on the left, the solution on the right.

## Intention & rationale
The job is to **make the solution feel like the answer** by contrasting it with the problem. Why this form:
- **The contrast is carried by surface *tone*, not a new color:** the problem panel is muted/recessed, the
  solution panel is bright/raised — so "bad → good" is *felt* before it's read, while the single `--accent`
  stays free for the key marks. This is how to show semantic contrast under the 4-color rule
  (`foundations/color-discipline.md`).
- **Mirrored structure makes the two directly comparable** — same badge, same title shape, same number of
  lines, so the eye maps problem-point → solution-point.

## When to use / When NOT
Use for problem→solution, as-is→to-be, current→proposed. **Not** for a multi-step process (use `flow`) or
a single statement (use `statement`).

## Structure
Eyebrow + centered title + muted sub-line. Two equal panels:
- **Left — problem:** recessed/muted surface; a badge pill (`--band-fill`); a 2-line title (`--ink`/light
  on the muted panel); 2–3 supporting lines, each marked with a small `--accent` dot.
- **Right — solution:** bright/raised `--surface`; same badge + title + lines structure.

## Tokens used
canvas, surface (solution panel), muted/muted-soft (problem panel), ink (titles/text), accent (the point
dots / one keyword), band-fill (badge pills).

## Icon use
Optional; usually none — the panel tone does the work. If used, one style, theme-colored.

## Content rules
Parallel structure on both sides; ≤ 3 points each; one claim per panel title; accent only the dots or one
keyword. Works in light or dark mode (the problem panel is simply the quieter surface of the theme).

## Do / Don't
- **Do** make the solution panel visibly brighter/raised than the problem panel.
- **Don't** introduce a second hue for "good vs bad" — use surface tone, not color.

## Example
"問題定義" (muted panel, 3 pain points with accent dots) vs "解決方案" (bright panel, 3 mirrored lines)
(learned from Img17, structure only).
