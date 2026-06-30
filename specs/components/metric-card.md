---
id: metric-card
kind: component
tier: molecule
status: stable        # example built + render-validated
intent: state one outcome so the number is the hero and the topic is labeled quietly
triggers: [one result + a one-line reason, an outcome with a topic, a card in a results-grid]
depends_on: [tokens]
tokens_used: [surface, ink, muted, accent]
icon_use: optional
learned_from: Img13
example: examples/light-metric-cards.html
---
# metric-card

## Purpose
A single outcome on a card: a claim title with the **key metric phrase in `--accent`**, a muted
supporting line, and an optional **right-anchored topic icon**.

## Intention & rationale
The card must make one result land. **Why the parts are arranged this way:**
- **Emphasis carries the claim:** the metric/outcome phrase is `--accent`, the rest of the title `--ink`.
  The eye lands on the proof first (intention → emphasis). The accent is a *phrase* (e.g. "平均 2 小時",
  "+34%"), not necessarily one word — it's whatever words carry the number.
- **Icon labels, doesn't lead:** the topic glyph sits **right-anchored and vertically centered** while the
  text fills the left ~75%. Text leads (we read left-first); the icon is a quiet topic marker on the
  right, so it supports without stealing the number's attention (`foundations/iconography.md`).
- **Muted support recedes:** the explanation is `--muted` so it's available but never competes with the
  title — honoring the 4-color discipline.

## When to use / When NOT
Use as a column card in `results-grid`, or anywhere one outcome needs a topic + a one-liner. **Not** for a
bare number with no context (use `metric`) or for evidence trios (use `evidence-card`).

## Structure
`--surface` card. Left text block: **title** (`--ink`, metric phrase `--accent`) → small gap → **body**
(`--muted`, 1–2 lines). Optional **icon** on the right, vertically centered, card-anchor size (40–56px),
`--accent`, one style. Title→body gap tight; eyebrow→title (if any) tighter than title→body.

## Tokens used
surface (card), ink (title base), accent (metric phrase + icon), muted (body).

## Icon use
Optional, single, right-anchored, `--accent`, one deck-wide style. Drop it if the title already names the
topic clearly (don't repeat meaning).

## Content rules
One outcome per card. Accent exactly one phrase — the metric/result. 繁中 primary + short EN handle; body
in 繁中 (optional muted EN second line). Keep sibling cards equal height.

## Do / Don't
- **Do** accent only the metric phrase; keep the icon quiet and on the right.
- **Don't** accent the whole title, place the icon left of the text, or mix icon styles across cards.

## Example
"1 年以上契約維持率 **+34%**" + muted reason + a right-anchored people icon (learned from Img13, structure only).
