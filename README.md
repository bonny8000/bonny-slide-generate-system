# Bonny Slide System v7

Bilingual **繁中 + English** UX/product slides in **two locked modes** (LIGHT / DARK), one mode per
deck, under a strict **4-color discipline**. Outputs per-slide HTML, a single scroll-through HTML, or
PPTX. v7 adds a **Plain-Language Layer** so titles and captions land on first read for mixed
manager / PM / engineer rooms.

## Consistency is structural
`assets/base.css` (spacing scale, 12-col grid, type, components — no color) + **one** of
`tokens-light.css` / `tokens-dark.css`. Same variable names in both, so swapping the token file flips
the whole set. The `pptx/` bridge mirrors the same tokens.

## What v7 added (from a live review of a real deck)
The feedback was not about visuals — it was that titles read as too abstract for a non-UX room. So:
- **Plain-Language Layer** — one-read test; no stacked-modifier titles; turn process sentences into a
  short label + plain sub; name real examples instead of categories; every code (L0–L4, 3A/3B) carries
  a plain label; cross-team framed as collaboration; cut behind-the-scenes pages or show one worked example.
- **`.skill-chip` / `.chipcloud`** — show real skill names as #tags (concrete > abstract, and signals volume).
- **Narrative continuity** check — bridge from an overview into a deep-dive; no unbridged jumps.
- **Audience-first** parser step; **16px readability floor** on decks.
- Documented **single-scroll** and **TOC** as delivery patterns.

## Modes
| | LIGHT | DARK |
|---|---|---|
| canvas | `#FBFBFE` | `#1B1B20` |
| accent | `#7077FB` | `#4D77FF` |

## Files
`SKILL.md` (full spec) · `assets/` (source of truth) · `examples/` (layouts in both modes) ·
`pptx/` (token bridge + sample decks).

## Known scope
WCAG contrast is not enforced (light muted text ≈ 3.6:1) — intentional per the reference; raise
`--muted` if AA is required. PPTX covers core templates (title, ranked-bars, feature-rows).

— v7 · 2026.05
