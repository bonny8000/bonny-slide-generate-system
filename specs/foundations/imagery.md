---
id: imagery
kind: foundation
status: stable
learned_from: Img19, Img21, Img22, Img23, Img24, Img26, Img28
---
# Imagery — ask for it, then keep it on-system

Images make a slide land. The discipline has two halves: **(1) get the *right* image** (often by asking the
user), and **(2) make every image obey the 4-color system.**

## 1. Ask for assets (don't fabricate)
A page's intention is frequently best served by a *real* asset. During `slide-plan.md`, when a page would
be materially stronger with one, **ask the user to provide it** instead of inventing:
- **Product / feature pages → real screenshots** (then frame with `ui-mockup`).
- **Brand / competitor / tool pages → logos** (the user has them; logos keep real color).
- **Persona / quote / team pages → photos, or a chosen illustration set.**
- **Results / data pages → the real numbers or a data export.**
Ask **early** (at planning), name **exactly** what you need and **why**, and offer a fallback if they don't
have it. A representative placeholder is fine *if labeled as such*; a fabricated screenshot or fake-precise
data presented as real is not.

## 2. How references handle imagery (pick the technique that fits the intention)
| technique | when to use | how to keep it on-system | ref |
|---|---|---|---|
| **Device / UI mockup** | show a product or feature screen | screenshot in a browser/phone frame (`ui-mockup`); no shot yet → skeleton bars | Img19, Img21, Img28 |
| **Background fill / tint** | seat a mockup or illustration so it doesn't float | a soft `--surface` / `--accent-soft` block behind it — never a new hue | Img19, Img26 |
| **Consistent illustration set** | give cards/sections identity | ONE illustration style deck-wide, recolored to a single theme color (accent) + neutrals | Img26 |
| **Stock / 3D person illustration** | humanize a persona or quote | one character set, toned toward palette; always paired with text | Img22, Img23 |
| **Annotated screen** | point at what changed / what a feature does | leader-line callouts; problems muted, improvements/active in accent | Img21, Img28 |
| **Brand / tool logos** | sources, tools, competitors | the one exception — keep real brand colors, small and contained | Img15, Img24 |
| **Real photo as content** | the photo *is* the content (e.g. UGC, reviews) | keep un-recolored; seat on a `--surface` card; don't tint | Img21 |
| **Generated editorial explainer** | workshop instructions, workflow transformation, or real-UI interpretation through human/assistant dialogue | invoke the built-in image generator with the matching canonical references; generate a new exact-ratio image and fill the whole block | Img39–Img43 |

### Generated editorial-explainer route
When `content-map.md` selects `editorial-explainer-stage`, follow
`generated-editorial-explainer.md`. Reference assets teach style only. Never place one as the
new slide, crop it into a derivative, or imitate it with CSS/SVG. Generate a fresh image, save it under the
deck, validate its ratio and colour, and place it edge-to-edge in the intended image block.

## 3. The discipline that ties them together
- **Every screenshot / photo / UI-mockup gets ROUNDED CORNERS + a SUBTLE LIGHT shadow.** Use the
  `--r-card` radius (or the device bezel radius for phones) and the **`--shadow-img`** token — a soft,
  lifted, *light* shadow (tight contact + gentle ambient), **never dark or heavy**. In HTML, wrap a raw
  `<img>` in **`.shot`**; the device/mockup frames (`.phone` / `.appframe` / `.ui-mockup` / `.mock*`) carry
  it automatically. *(Validated against the reference decks — every screenshot there is rounded + softly
  shadowed.)*
- **A SECONDARY / inline image may float directly on the canvas** with that treatment — the soft shadow
  seats it, so it needs no surface card. But a **HERO mockup (the slide's main visual) must be ANCHORED** —
  seat it on a soft `--accent-soft` / `--surface` rounded **stage** (or a circle/panel behind it) or let it
  near-bleed — so it never floats in a void opposite an empty column. (Pick floating-with-shadow for
  secondary, stage/anchor for hero; never a hard unshadowed image on bare canvas, never a dark shadow.)
- Every **non-photo, non-logo** image is **recolored / toned to the theme** — one accent + neutrals — so it
  obeys the 4-color rule (`color-discipline.md`).
- The narrow editorial-explainer exception may keep sparse reference-style avatar/highlight hues inside the
  bitmap only; do not propagate those hues into native slide components.
- **One illustration style per deck**, one icon style; never mix sets (`iconography.md`).
- Differentiate grouped images by **surface tone**, not new hues.
- **Photos and logos are the only full-color elements** — keep them small and contained.

## 4. Open-source sources (license-checked, June 2026)
**Prefer code-native assets** (CSS / inline SVG) over raster — they recolor to your tokens, so they obey the
4-color rule automatically. Recolor every illustration to **one accent + neutrals**; keep **one style per
deck**. Photos and logos are the only full-color elements.

| Need | Source | License | Keep on-system |
|---|---|---|---|
| **Device / browser frames** | **devices.css** (marvelapp) — pure-CSS phones/tablets/laptop | MIT | recolor the frame to `--ink`/`--muted`; put the screenshot or `ui-mockup` inside. Ideal for HTML decks (no image) |
| **Flat 2D illustrations** | **unDraw** | free, **no attribution** | recolor to `--accent` on the site → download **SVG**, inline it. Best default |
| **Flat 2D (richer / animated)** | **Storyset** (Freepik) | free **with attribution** | set a single brand color; SVG/Lottie |
| **Person / avatar illustrations** | **Open Peeps** (CC0), **Humaaans** (free) — Pablo Stanley | CC0 / free | mix-and-match SVG; tone toward palette. For personas/quotes (Img22, Img23) |
| **3D illustrations / icons** | **3dicons.co** (realvjy) — the 3D-object look | **CC0** | use the monochrome/“colorful” PNG that sits closest to your accent; keep one style; place small |
| **Background patterns / texture** | **Hero Patterns** (Steve Schoger) — repeatable SVG | free | set foreground = `--accent`/`--muted`, low opacity; seat content above it |
| **Stock photos** | **Unsplash**, **Pexels** | free, no attribution, commercial OK | photos stay full-color *as content*; seat on a `--surface` card; don't tint |
| **Icons** | Lucide · Tabler · Phosphor · Heroicons · Iconoir | MIT | see `foundations/iconography.md` — `currentColor` + token; one set per deck |

Caveats: don't redistribute unDraw as a pack or use it to build a competing library; **photos carry no
model release** (Unsplash/Pexels don't verify consent — check before using a recognizable face); brand/tool
logos keep their real colors but you still need the right to use them.

## 5. Fallback when no asset exists
Use a skeleton `ui-mockup` or a recolored illustration placeholder, and **label it representative**. Never
present a placeholder as a real screenshot or invent precise data.

## Audit
Non-photo/logo imagery recolored to palette; one illustration style deck-wide (major) · **every screenshot/
photo/mockup has rounded corners + the soft `--shadow-img` (never a hard-edged or dark-shadowed image)**
(major) · image either floats with the soft shadow OR sits on a surface — never bare/unshadowed on canvas
(minor) · no fabricated screenshot or fake-precise data presented as real (blocker) · asked the user for
assets that would materially improve a page (minor).
