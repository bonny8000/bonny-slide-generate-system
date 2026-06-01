# Bonny Slide System v8

Bilingual **繁中 + English** UX/product slides in **two locked modes** (LIGHT / DARK), one mode per
deck, under a strict **4-color discipline**. Outputs per-slide HTML, a single scroll-through HTML, or
PPTX. Carries a **Plain-Language Layer** and patterns for **presenting a system or decision — show the
reasoning, not just the conclusion.**

## Consistency is structural
`assets/base.css` (spacing scale, 12-col grid, type, components — no color) + **one** of
`tokens-light.css` / `tokens-dark.css`. Same variable names in both, so swapping the token file flips
the whole set. The `pptx/` bridge mirrors the same tokens.

## What v8 added (from an end-to-end build + 3 rounds of stakeholder feedback)
- **Show the reasoning, not just the result** — method slide (① enumerate → ② relate → ③ package) →
  detail slides → conclusion. Senior reviewers keep asking for the *thinking*, not the conclusion alone.
- **Section cover (扉頁)** `.slide.section-cover` — dark announce-page between major parts. Rule: nav
  strip + "NEXT" label stay small; the section title is the hero. Dark inside a light deck is allowed.
- **Bilingual tag list** `.taglist` — `#Handle (中文說明)` for mixed CJK+English rooms.
- **Frame provisional content as a range, not a closed list** — no 「枚舉/all」; say 範圍/方向 + 收斂 note.
- **Numbered step flow**, **labeled split rows** (設計線/程式線, 上線前/上線後), **worked example +
  enlarged takeaway**, **relationship triplet** (前後 / 相依 / 並行).
- **Candidate comparison** delivery — offer 2–3 versions when layout is subjective.
- **Iteration-heuristics** table mapping common feedback → response.

## Modes
| | LIGHT | DARK |
|---|---|---|
| canvas | `#FBFBFE` | `#1B1B20` |
| accent | `#7077FB` | `#4D77FF` |

## Files
`SKILL.md` (full spec) · `assets/` (source of truth) · `examples/` · `pptx/` (token bridge + samples).

## Known scope
WCAG contrast not enforced (light muted ≈ 3.6:1) — raise `--muted` if AA required. PPTX covers core
templates (title, ranked-bars, feature-rows).

— v8 · 2026.06
