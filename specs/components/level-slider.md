---
id: level-slider
kind: component
tier: atom
status: stable        # example built + render-validated
intent: show a trait/level at a glance (low ↔ high)
triggers: [persona behavior traits, ratings, "敏感度/能力/連結性", a 0–100 level, comparable attributes, 민감도, 능력, 연결성]
depends_on: [tokens]
tokens_used: [muted-soft, accent, ink, muted]
icon_use: none
learned_from: Img22
example: examples/light-persona-cards.html
---
# level-slider

## Purpose
A labeled track with a marker showing where a trait sits on a low↔high scale.

## Intention & rationale
The job is to **convey "how much" instantly and comparably**. Position on a track reads faster than a
number; the accent marker draws the eye to the value; **aligned tracks** let several traits be compared at
a glance.

## Structure
A **label** (`--ink`/`--muted`) + a horizontal **track** (`--muted-soft`) with a filled portion or **dot**
(`--accent`) at the level. Stack several with labels and tracks aligned in a column.

## Tokens used
muted-soft (track), accent (fill/dot), ink (label), muted (optional scale ends).

## Icon use
None.

## Content rules
Align all tracks. Omit exact numbers unless they carry meaning. 2–5 traits read best together.

## Do / Don't
- **Do** align tracks so traits are comparable.
- **Don't** color different traits differently — one accent only.

## Example
"壓力敏感度 / 情緒表達能力 / 社會連結性" as three aligned sliders with accent dots (learned from Img22).
