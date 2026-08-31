---
id: results-grid
kind: layout
tier: organism
status: stable         # example built + validated: examples/light-results-grid.html (Round-1 open layout)
intent: prove impact across several outcomes / show what the work achieved
triggers: [results, 成果, "before → after", 2–4 outcome metrics each with a one-line reason, an achievements recap, 成效數字, 專案成果, 帶來的改變, 成效指標]
material: stat
arrangement: grid
item_count: few
alternates: []
depends_on: [metric-card, delta-metric, tokens]
tokens_used: [canvas, surface, ink, muted, muted-soft, accent]
icon_use: optional
learned_from: Img13
example: examples/light-results-grid.html
---
# results-grid

## Purpose
A results / achievements slide: one hero outcome shown with a before→after chart, plus a stacked column
of secondary outcome cards.

## Intention & rationale
The job is to **prove impact** — make the audience believe the work moved real numbers. So:
- The **metric phrase is the hero**: in every title the number/outcome sits in `--accent` while the rest
  stays `--ink`, pulling the eye straight to the proof (intention → emphasis, see `foundations/color-discipline.md`).
- The hero card carries a **before→after bar** (`delta-metric`) so the improvement is *felt visually*, not
  just read — a single number alone is weaker than a number you can see shrink/grow.
- Secondary outcomes become **`metric-card`s** with a **quiet right-anchored topic icon**, so each result
  is scannable and labeled by topic without the icon competing with the number.
This is why the components are arranged this way: hero = depth (one proof, fully shown); column = breadth
(more proofs, compactly). Asymmetry signals "one headline result + supporting wins."

> **Preference-validated layout (A/B Round 1 — see `preferences.md`):** the strongest form is a **giant
> hero number** (the headline metric) with a small before→after bar, the **secondary stats as an OPEN list
> with hairline dividers** (not boxed `metric-card`s), and a **quote/takeaway band pinned at the bottom** —
> the body uses `.vspread` so it fills top→bottom. Keep the hero number and the supporting stats close (no
> dead center gap). The carded variant still works, but open beat carded with the user.

## When to use / When NOT
Use to recap measurable outcomes (a "what we achieved" / KPI results slide), especially with a flagship
before/after metric. **Not** for a single number (use `metric`/`delta-metric` alone) or non-quantified
claims (use `statement`/`conclusion`).

## Structure
1. **Eyebrow** (`Achieved` / `成果`, small) top-left + **plain-language section title** below it.
2. **12-col grid**, asymmetric: **hero card ~6–7 cols** (taller) + **stacked column ~5–6 cols** holding
   2 `metric-card`s of equal height.
   - Hero card: title (accent metric phrase) + muted supporting lines + a `delta-metric` before→after bar.
   - Column cards: `metric-card` each (title + muted line + right-anchored topic icon).
All cards on `--surface`, rounded; card pad 48, gutter 32 (`foundations/spacing-grid.md`).

## Tokens used
canvas (slide), surface (cards), ink (titles), muted/muted-soft (body + "before" bar + chart labels),
accent (the metric phrase, the "after" bar, the topic icons).

## Icon use
Optional: one topic glyph per column card, **right-anchored, vertically centered, `--accent`, one style**
(`foundations/iconography.md`). The hero card usually needs no icon — its chart is the visual.

## Content rules
One claim per card; the accented phrase is the metric/outcome only. 繁中 primary + short EN handle.
Keep column cards equal height and parallel in shape. 2–3 outcomes total reads best.

## Do / Don't
- **Do** make every card's metric phrase the one accent; align the column cards' edges and heights.
- **Do** give the flagship outcome the hero card + the before/after chart.
- **Don't** accent a whole title, add a second chromatic color, or let a topic icon outweigh its number.
- **Don't** mix icon styles between the cards.

## Example
Eyebrow "Achieved" + title; hero card "response time → 平均 2 小時" with a 16h→2h before/after bar; two
column cards "+34% retention" (people icon) and "revision requests → 4/mo" (pencil icon) (learned from Img13).

> Note: Img13 is a Korean reference; this spec captures its **structure only**. The system reproduces in
> 繁中 + English — never Korean.

## Human preference refinement
R52 A (2026-08-31): lead supporting metric uses an accent-soft surface; numeric values in all rows keep the same horizontal inset. The fill is not an alignment anchor.
