---
id: as-is-to-be
kind: layout
tier: organism
status: stable         # example built + validated: examples/dark-as-is-to-be.html
intent: contrast the current experience with the improved one using real screens
triggers: ["as-is / to-be", before/after of a UI, "기능 추가 후", screen 改善, annotated current vs improved]
depends_on: [ui-mockup, tokens]
tokens_used: [canvas, surface, ink, muted, muted-soft, accent, band-fill]
icon_use: optional
learned_from: Img28
example: examples/dark-as-is-to-be.html
---
# as-is-to-be

## Purpose
Two large screen mockups — As-is vs To-be — each annotated with what's wrong / what improved.

## Intention & rationale
The job is to **prove the improvement on the real product**. Why this form:
- **Showing the actual screens makes the change credible** — not a claim, a visible before/after.
- **Annotations name exactly what changed**, tying each callout to a screen element.
- **Tone carries the verdict:** As-is is muted/quiet, To-be is bright + accent; problems are muted,
  improvements accent — so "before → better" reads without a second hue.
- Cousin of `problem-solution` (that contrasts *text* panels; this contrasts *annotated screens*).

## When to use / When NOT
Use to show a UI before/after with reasons. **Not** for a conceptual problem/solution (use
`problem-solution`) or a single screen (use `feature-showcase`).

## Structure
Title (accent the improvement phrase). Two large **`ui-mockup`** screens side by side: **As-is**
(muted/grey badge + quiet screen) and **To-be** (accent badge + bright screen). Around each, **annotation
callouts with leader lines** — As-is = problems (`--muted`), To-be = improvements (`--accent`).

## Tokens used
canvas, surface (screens), ink (annotation titles), muted/muted-soft (as-is + problem callouts), accent
(to-be + improvement callouts), band-fill (As-is/To-be badges).

## Icon use
Optional; callout markers are leader-line dots, one style.

## Content rules
2–3 annotations per side; terse; one screen each side. As-is muted, To-be accent.

## Do / Don't
- **Do** mark improvements in accent and problems in muted.
- **Don't** use two hues for as-is vs to-be — use tone + the single accent.

## Example
"功能新增後更便利的流程" — As-is screen (3 problem callouts) vs To-be screen (3 improvement callouts)
(learned from Img28, structure only).
