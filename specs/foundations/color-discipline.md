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

## Emphasis — colored by intention
Color follows **intention**: the accent marks the **one phrase that carries the slide's claim** — and
nothing else. Decide *what the page is trying to prove*, then accent the words that prove it; the rest of
the title stays `--ink`, supporting text `--muted`.
- It's **one phrase per title, not necessarily one word.** On a results slide the claim is the number, so
  the whole metric phrase is accent: "對應時間降到 **平均 2 小時**", "維持率 **+34%**" (Img13). On a
  conceptual title it's a single keyword. Either way: exactly one accented span.
- **Importance, not category, earns color.** Don't accent every label or repeat the accent across a card;
  if two things are accented, the eye lands on neither. The muted layer holds everything that supports
  but isn't the point.
Bands and section-covers use `--band-fill` (the text color as a fill) so they read as structure, not as a
new color.

## Categories & semantic contrast (without breaking the rule)
The temptation is to reach for a second/third hue to code categories or "good vs bad." Don't — solve it
with **surface and tone**, keeping the single accent:
- **Categorical grouping** (flowchart swimlanes, regions, segments): differentiate with **neutral surface
  tints** — variations in lightness of `--surface` / `--accent-soft` / `--muted-soft` — not multiple
  chromatic hues. Keep `--accent` for the primary/active path or the one focus group (Img14).
- **Semantic contrast** (problem vs solution, as-is vs to-be): carry it with **surface tone** — a
  recessed/muted panel vs a bright/raised one — not a second color (Img17).
- **Exception — brand/competitor logos** keep their real brand colors (you can't recolor a logo); place
  them small and let everything non-logo stay on-palette (Img9, Img15).
