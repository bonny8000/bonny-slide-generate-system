---
id: comparison-table
kind: component
tier: molecule
status: stable
depends_on: [tokens, logo-row]
tokens_used: [surface, ink, muted, muted-soft, accent, accent-soft]
icon_use: optional
learned_from: Img9
example: examples/comparison-table.html
---
# comparison-table

## Purpose
Compare several options across several criteria at a glance, with one option highlighted.

## When to use / When NOT
Use for competitive analysis, vs-alternatives, feature matrices. **Not** for a single option (use cards)
or for time-series (use a chart).

## Structure
- Left column = **criteria** (rows), top-aligned, `--ink`.
- Top row = **options** (columns); optional logo/icon per option (see logo-row).
- Cells = `O` / `X`, a short value, or a stat. Keep cells terse.
- **One highlighted column** = the winning/focus option: `--surface` raised + a subtle `--accent` border;
  its key numbers in `--accent`. All other columns neutral.
- Optional side panel: a ranked-needs list derived from the table (1/2/3).

## Tokens used
surface (highlighted col), ink (criteria + values), muted (secondary cells), muted-soft (gridlines),
accent (focus column emphasis), accent-soft (focus column fill).

## Icon use
Optional option logos/icons in the header row — monochrome or brand marks kept small; one style.

## Variants
O/X matrix · value matrix · mixed (value + O/X).

## Content rules
≤ 6 criteria rows, ≤ 5 option columns on one slide. Highlight exactly one column. Bilingual: criteria
in 繁中, option/value labels may be Latin.

## Do / Don't
Do highlight one column only. Don't color multiple columns; don't pack long sentences into cells.

## Example
A 4-option × 6-criteria O/X table with column 1 highlighted + a 3-item ranked-needs panel (Img9).
