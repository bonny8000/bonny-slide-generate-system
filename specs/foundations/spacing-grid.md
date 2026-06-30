---
id: spacing-grid
kind: foundation
status: stable
---
# Spacing & grid

- **8px scale:** `--s0:4 --s1:8 --s2:16 --s3:24 --s4:32 --s5:40 --s6:48 --s7:64 --s8:80 --s9:96`.
  Defaults: pad-y 80 · pad-x 96 · gutter 32 · section gap 48 · card pad 48 (overridable, on-scale).
- **12-column grid** (`.grid12` + `.col-N`). Common splits: 6+6 · 7+5 · 8+4 · 4+4+4. Equal sets → `.cards.two/.three`.
- **Equal four-side margins.** `.slide` is a centered flex column → content sits in the optical middle.
- **Fill, don't leave dead space.** Give light slides presence (card `min-height`, generous gaps); aim ≥30% whitespace but no large empty voids.
- **Vertical rhythm inside a card/title block:** group tightly, separate loosely. eyebrow→title gap is
  **tight** (`--s0/--s1`), title→body is **looser** (`--s2/--s3`), and the chart/icon gets the remaining
  space. The proximity tells the eye what belongs together — a tight eyebrow reads as a label *on* the
  title, not a separate line (Img13).
- **Margins scale with role:** generous card padding (card pad 48) + a steady gutter (32) keep cards
  breathing; equal gutters and equal sibling-card heights are what make an asymmetric grid still read as
  ordered.
- Canvas: `.slide.deck` 1920×1080 · `.slide.poster` 1080×auto.
