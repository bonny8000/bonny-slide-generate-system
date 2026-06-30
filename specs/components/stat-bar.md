---
id: stat-bar
kind: component
tier: atom
status: stable        # example built + render-validated
intent: show a single labeled percentage as a horizontal bar
triggers: [labeled % values, survey results, "N% of users …", a row of comparable proportions]
depends_on: [tokens]
tokens_used: [muted-soft, accent, on-accent, ink]
icon_use: none
learned_from: Img4
example: examples/light-qual-quant-split.html
---
# stat-bar

## Purpose
A labeled horizontal bar: a caption above a track whose fill length encodes a percentage.

## Intention & rationale
The job is to **make a proportion instantly comparable**. Bar length reads faster than a bare number, and
stacking several with aligned tracks lets the audience compare survey answers at a glance. The % sits on
the fill so value and length are read together.

## Structure
A **label** (`--ink`) + a **track** (`--muted-soft`) with a **fill** (`--accent`) sized to the % and the
value (`--on-accent`) right-aligned inside the fill. Stack several with aligned tracks.

## Tokens used
muted-soft (track), accent (fill), on-accent (value text), ink (label).

## Icon use
None.

## Content rules
Align all tracks; 2–5 bars read best. One accent — don't color bars differently.

## Do / Don't
- **Do** keep tracks the same width and order meaningfully.
- **Don't** use a second hue to distinguish bars.

## Example
"覺得不知道寫什麼 72% / 曾因中斷而放棄 58% / 想要成就感 64%" (learned from Img4).
