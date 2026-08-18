---
id: icon-label-row
kind: component
tier: atom
status: stable
intent: list items with a quick visual anchor per row
triggers: [categories, audiences, capabilities, benefit list, short labelled items, 6 one-liners]
depends_on: [tokens]
tokens_used: [ink, muted, accent, surface]
icon_use: required
learned_from: Img6
example: examples/dark-02-target-group.html
---
# icon-label-row

## Purpose
A list where each item is an icon + a label — for categories, audiences, capabilities.

## When to use / When NOT
Use when items benefit from a quick visual anchor (Img6 audience/benefit lists). **Not** when items are
long phrases (use plain rows) or when the icons would just repeat the labels.

## Structure
Vertical stack of rows; each row = `[icon 20–24px] [label]`. Optional container card (`--surface`).
Rows share alignment and spacing from the `--sN` scale.

## Tokens used
ink (label), muted (default icon), accent (one emphasized row's icon/label), surface (optional card).

## Icon use
**Required.** One style across all rows (all line or all filled), monochrome from theme tokens; the one
emphasized row may use `--accent`.

## Variants
Plain list · carded list · two-column (audience vs benefits, as Img6).

## Content rules
≤ 7 rows. Labels short (≤ ~10 CJK chars). 繁中 labels; Latin terms allowed.

## Do / Don't
Do keep one icon style + size. Don't mix icon weights; don't add an icon that just restates the label.

## Example
Two side cards (오디언스 / 기업 → 受眾 / 企業) each a 5–6 row icon-label list (Img6).
