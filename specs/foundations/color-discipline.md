---
id: color-discipline
kind: foundation
status: stable
---
# Color discipline — the Iron Rule (theme-independent)

> **4 colors maximum: 1 background + 1 text + 1 muted + 1 accent.**
> `--accent` is the ONLY chromatic color on a slide.

This holds in **every theme**. A theme changes the hues; it never adds a 5th role or a 2nd accent.

## The four roles
- **background** — `--canvas` (whole slide) and `--surface` (cards/panels). Background can be light or
  dark; that's a theme/mode choice, not an extra color.
- **text** — `--ink`.
- **muted** — `--muted` / `--muted-soft` for secondary text, inactive data, hairlines.
- **accent** — `--accent` / `--accent-soft` for the ONE thing to look at: emphasis keyword, active chart
  series, a highlighted column, a badge.

## Charts
Inactive series = `--muted` / `--muted-soft`. The one series that matters = `--accent`. Never two
chromatic colors in a chart. (Semantic `--pos`/`--neg` may co-occur **only** inside a KPI/delta chart.)

## Emphasis
Emphasize **one** keyword per title in `--accent`. Bands and section-covers use `--band-fill` (the text
color as a fill) so they read as structure, not as a new color.
