---
id: iconography
kind: foundation
status: stable
note: replaces the old "no iconography" stance
---
# Iconography & illustration

Icons and illustration are **first-class** in this system — most strong decks use them to make a point
land faster (see Img6, Img8, Img11, Img12). The rule is **disciplined, purposeful** use, not decoration.

## Principles
1. **Purposeful only.** An icon must do a job: anchor a card, mark a persona, label a category, show a
   data source, or define a concept. If the label already says it, drop the icon.
2. **One style per deck.** Pick line **or** filled; keep one stroke weight, corner radius, and grid
   size. Never mix icon sets. (Illustrations: one illustration style per deck too.)
3. **Theme-colored.** Icons are **monochrome from theme tokens** — `--muted` or `--ink` by default,
   `--accent` only for the single emphasized/active one. Illustrations are limited to theme colors
   (e.g. 2-tone: a neutral + accent), so they still obey the 4-color discipline. No full-color stock
   art that introduces new hues. **One exception: brand/competitor logos** keep their real brand colors
   (you can't recolor a logo) — keep them small and let everything else stay on-palette (Img9, Img15).
4. **Supportive, not load-bearing.** Pair icons with text; never rely on an icon alone to carry meaning.

## Icon + text placement (how they share a row)
- **Text leads, icon supports.** We read left-first, so the text block sits left and the icon is
  **right-anchored and vertically centered** on a card; the icon is a quiet topic marker, never the
  headline (Img13). Don't put the icon left of a metric — it would compete with the number.
- **The emphasized number keeps the accent; the icon is the same accent but smaller and quieter** — one
  accent role, two quiet uses, so the 4-color rule holds.
- **One icon per card**, sized from the scale below (card-anchor on metric/result cards), all icons in a
  group identical in size, style, and weight.

## Size scale
inline `1em` · label `20–24px` · card-anchor `40–56px` · hero illustration sized per layout.

## Where icons/illustration earn their place (patterns)
| pattern | use | ref |
|---|---|---|
| icon + label row | category / audience lists | Img6 |
| icon-topped card | feature / terminology cards | Img11, Img12 |
| avatar | persona header / quote attribution | Img4, Img7 |
| logo row | data sources, tools, competitors | Img8, Img9 |
| stat icon | anchor a single headline metric | Img8 |
| right-anchored card icon | quiet topic glyph on a metric/result card (icon right, text left, accent) | Img13 |
| keyword illustration | define a concept visually | Img12 |

## Don't
Decorative icon beside every bullet · mixing line + filled · full-color illustrations that break the
palette · an icon that repeats the label's meaning · different icon sizes in the same row.

## Audit
One icon style deck-wide (major) · monochrome from theme tokens (major) · every icon earns its place (minor).


## Icon & illustration sources (open-source)
Pick **one** icon set and **one** illustration source per deck — consistency beats variety.

**Line-icon sets** (all MIT, SVG, recolorable):
- **Lucide** — clean 24×24 / 2px line, the Feather successor. Ubiquitous (the AI/template default) → fast, but less distinctive.
- **Tabler** — 5,900+ icons, 24×24 / 2px, MIT, no attribution. Best breadth.
- **Phosphor** — six weights (thin → fill → duotone); choose one weight per deck. Most distinctive feel.
- **Iconoir / Heroicons** — also clean; Iconoir reads a touch more distinctive, Heroicons pairs with Tailwind.

**How to use them (theme-colored, on-system):**
1. Get the icon's SVG (from the set's site, or its npm/CDN — e.g. `unpkg.com/lucide-static/icons/<name>.svg`).
2. Inline the `<svg>`; set `stroke="currentColor"` (or `fill="currentColor"`).
3. Color via token: `.icon{color:var(--muted)}`; the one emphasized icon → `var(--accent)`. One stroke width throughout.
This keeps icons monochrome and inside the 4-color rule. Use the `.icon` helper in `assets/base.css`.

**Illustrations** (terminology / hero):
- **unDraw** — open license, **no attribution**; set a **single color by hex on the site** → use your deck `--accent` so it matches and obeys the palette. Best default.
- **Storyset** — richer + optional animation, color/layer editor; free **with attribution** (paid removes it).
- **Humaaans / Open Peeps** — CC0 character builders.
Rule: one illustration style per deck; recolor to a single theme color so it never breaks the 4-color discipline.
