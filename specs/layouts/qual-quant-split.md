---
id: qual-quant-split
kind: layout
tier: organism
status: stable        # example built + render-validated
intent: make a finding both felt and proven — user voices beside the matching numbers
triggers: [quotes AND stats together, "what users said + how many", a hypothesis backed by both, 原話配數據, 質化量化並排, 使用者說什麼加多少人]
depends_on: [quote-bubble, stat-bar, tokens]
tokens_used: [canvas, surface, ink, muted, muted-soft, accent]
icon_use: optional
learned_from: Img4
example: examples/light-qual-quant-split.html
---
# qual-quant-split

## Purpose
Two columns — qualitative quotes on one side, quantitative stat-bars on the other — landing on a hypothesis.

## Intention & rationale
The job is to **make it both felt and proven**. A quote alone is anecdote; a number alone is cold.
Side-by-side, the **voice gives the number meaning** and the **number gives the voice weight**. The
hypothesis band at the bottom turns the paired evidence into a direction.

## When to use / When NOT
Use when a finding has both human quotes and supporting percentages. **Not** for pure data (use `data`) or
pure quotes (use `quote-bubble`).

## Structure
Header. Body (`.grow`): left = 2–3 `quote-bubble`s; right = `stat-bar`s (labeled tracks with the % filled
in `--accent`). A **hypothesis `callout`** pinned at the bottom.

## Tokens used
canvas, surface (bubbles), ink (quotes/labels), muted (attribution), muted-soft (bar tracks), accent (bar
fills + hypothesis keyword).

## Icon use
Optional avatars on the quotes; one style.

## Content rules
≤ 3 quotes, ≤ 4 stat-bars; accent the one key phrase in the hypothesis. Keep quotes terse.

## Do / Don't
- **Do** pair each side so they reinforce; end on a hypothesis.
- **Don't** add a second chromatic color to the bars.

## Example
2 user quotes + 3 stat-bars (72% / 58% / 64%) + a hypothesis band (learned from Img4).
