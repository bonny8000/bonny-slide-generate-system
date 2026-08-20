---
id: interview-affinity
kind: layout
tier: organism
status: stable        # example built + render-validated
intent: converge several interview groups into one shared insight
triggers: [interview groups/segments, affinity mapping, "across N groups we heard…", persona columns + insight, 訪談收斂, 幾組訪談的共同洞察, 親和圖, 分組訪談結果彙整]
depends_on: [tokens]
tokens_used: [canvas, surface, ink, muted, muted-soft, accent, accent-soft]
icon_use: optional
learned_from: Img7
example: examples/light-interview-affinity.html
---
# interview-affinity

## Purpose
Parallel interview-group columns (avatar + reasons), converging into a shared insight band.

## Intention & rationale
The job is to **show that different groups land on the same problem**. The parallel columns let the
audience compare segments; the **single insight band underneath does the affinity-mapping move** —
"despite different contexts, here's the common thread." Convergence is the point.

## When to use / When NOT
Use to synthesize across user groups. **Not** for one persona (use `persona-cards`) or unrelated lists.

## Structure
Header. Body (`.grow`): 2–4 `--surface` group columns (avatar + name + 2–3 reason bullets), then one
**insight band** (`--accent-soft`) stating the shared finding.

## Tokens used
canvas, surface (columns), ink (names), muted (reasons), accent + accent-soft (avatars, insight band, keyword).

## Icon use
Optional avatar per column (one style, recolored to palette).

## Content rules
2–4 parallel columns, ≤ 3 reasons each; one insight band with the key phrase accented.

## Do / Don't
- **Do** keep columns parallel and end on the converged insight.
- **Don't** let any one column dominate.

## Example
學生 / 上班族 / 海外人士 columns → "見面前的不確定感是阻礙開口的關鍵" insight (learned from Img7).
