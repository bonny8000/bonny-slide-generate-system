---
name: bonny-slide-system
description: Generate bilingual 繁中 + English UX/product slides in two locked visual modes — LIGHT and DARK — under a strict 4-color discipline. Each deck is one mode only, never mixed; mode is a single token-file swap over a shared base.css. Outputs HTML (deck or poster), a single scroll-through HTML, or PPTX (python-pptx bridge sharing the same tokens). Carries a Plain-Language Layer so titles and captions land on first read for mixed manager/PM/engineer audiences. Full component library (charts, flows, features, personas, KPI, #skill-chips), 12-col grid, spacing scale, tone modifiers. Korean is never produced — Traditional Chinese is primary, English supporting.
---

# Bonny Slide System v7

Bilingual 繁中 + English slides in **two locked modes**, output as **HTML / single-scroll HTML / PPTX**.
Korean appears only in source material; it is translated, never quoted.

Consistency is **structural**. `base.css` holds everything mode-independent (spacing scale, grid,
type, components). Color lives only in `tokens-light.css` / `tokens-dark.css`, which expose the
**same variable names**. A deck loads `base.css` + **one** token file. Swap the file → the whole set
flips mode. Mixing light and dark inside a set is impossible by construction.

```
bonny-slide-system/
├─ SKILL.md
├─ assets/  base.css · tokens-light.css · tokens-dark.css
├─ examples/  flagship layouts in both modes + supporting layouts
└─ pptx/  tokens.py · slidegen.py · build_sample.py · sample-light.pptx · sample-dark.pptx
```

---

## Rule 0 · One mode per set (ASK if unsure)

A set is all LIGHT or all DARK. Never mixed. If the user hasn't named a mode, ask.

| | LIGHT (ref. img 1) | DARK (ref. img 2) |
|---|---|---|
| feel | clean editorial deck | premium infographic poster |
| canvas | near-white `#FBFBFE` | near-black `#1B1B20` |
| accent | `#7077FB` | `#4D77FF` |

---

## The Iron Rule (color) — 4 colors absolute max

> **1 background + 1 text + 1 muted + 1 highlight.** `--accent` is the ONLY chromatic color.
> Charts: inactive `--muted-soft`, active `--accent` — never two chromatic colors.

Background can be anything (a dark full-bleed page inside a light deck is a background choice, not a
mode switch). The insight band is the text color used as a fill (`--band-fill`), so it adds no color.

### Locked tokens

| role | LIGHT | DARK |
|---|---|---|
| `--canvas` / `--surface` | `#FBFBFE` / `#F1F4F9` | `#1B1B20` / `#2C2C33` |
| `--ink` | `#2B3040` | `#FFFFFF` |
| `--muted` / `--muted-soft` | `#7C7E92` / `#DCE0EB` | `#9A9CA8` / `#454652` |
| `--accent` / `--accent-soft` | `#7077FB` / `#E7E8FC` | `#4D77FF` / `#2A3358` |
| `--band-fill` | `#2B3040` | `#23242C` |
| semantic `--pos`/`--neg`/`--warn` | `#2FB67A`/`#E5556E`/`#E08A1E` | `#34D399`/`#F26D82`/`#F2B04E` |

---

## Typography (locked)

- CJK → **Noto Sans TC**, `letter-spacing: 0.05em`. Latin/numbers → **Arial**, `0`. Line-height **1.5**.
- Wrap CJK in `.cjk`, Latin/numbers in `.latin`.
- Scale: h1 50 · metric 56 · section 30 · eyebrow 22 · Q 20 · pill 18 · body 17 · caption 14 (px).
- **Readability floor:** on a 1920-wide deck, never set descriptive text below **16px**. Captions/labels
  16–17px, not 13–14px, when they carry meaning the room must read.

---

## Plain-Language Layer (白話層) — run on every title and caption

Decks are read by **managers, PMs, and engineers, not only UX people**, and are often re-presented by
someone else. Copy has to land on first read. (Real review failures: 「可彈性配置的模組化技能系統」、
「按任務目標串起跨階段的執行路徑」 — read three times, still unclear.)

1. **One-read test.** If a reader can't say what the slide claims after reading the title once, rewrite.
2. **No stacked modifiers in titles.** Drop chains like 「可彈性配置的／模組化／技能系統」. Say the plain
   thing. A process sentence is not a title: 「按任務目標串起跨階段的執行路徑」 → short label 「任務模式」
   + plain sub 「一個任務,從頭到尾會用到哪些 skill」.
3. **Concrete over abstract — name names.** Replace category labels with real examples as `.skill-chip`
   clouds: 「我們已經有這些 skill:#洞察整合 #元件庫 #樣式檢查…」 beats 「一套可重複使用的技能模組」.
   Showing real names also signals volume of work done.
4. **Who / what / what-they-get.** Frame capability copy as 誰可以用、用在哪、會得到什麼 — not the
   internal mechanism. 「PM、設計、RD 都能用」 over 「把技能打包發給對應團隊」.
5. **Codes always carry a plain label.** Never ship a bare code. `L0–L4` → 「L0 法規」「L1 系統與狀態」…
   and state the ordering in words (由廣到細). `3A/3B` → 「設計線／程式線」.
6. **Cross-team = collaboration, not replacement.** Touching another team's turf (RD/前端) → frame as
   help: 「交付可用的程式、讓串接更順」, not 「取代 RD」.
7. **Cut behind-the-scenes pages for exec rooms, or show ONE worked example.** A "how the metadata maps
   skills to roles" page is for the builder, not the room. Drop it, or replace the abstract diagram with
   one concrete walk-through (以一個 skill 為例 → 有人帶需求進來 → 系統配對到它).

Title *wording* stays the author's voice — the layer enforces plainness, it doesn't take over naming.

---

## Narrative continuity

Slides must connect. When a deep-dive follows an overview (e.g. 審查 L0–L5 after the 六階段 overview),
add a one-line **bridge** that hands off from the previous slide:「六階段裡的『審查』再往下拆,就是這套
分層檢查」. Never jump from an overview straight into a sub-topic with no transition. (A section-divider
/ 扉頁 page is one optional way to bridge.)

---

## Spacing scale & grid & balance

- 8px scale: `--s0:4 … --s9:96`. Roles: `--pad-y:80 --pad-x:96 --gutter:32 --gap-section:48 --pad-card:48`.
- **12-column grid** (`.grid12` + `.col-N`). Splits: 6+6 · 7+5 · 8+4 · 4+4+4. Equal splits → `.cards.two/.three`.
- Equal four-side margins; `.slide` is a centered flex column → content sits in the optical middle.
- **Fill, don't leave dead space.** Give light slides presence (card `min-height`, generous gaps) so a
  short content block doesn't float in a sea of white. Four-quadrant test: weight in ≥3 quadrants.
- Canvas: `.slide.deck` 1920×1080 · `.slide.poster` 1080×auto.

---

## Component library (all in base.css)

| component | class | notes |
|---|---|---|
| vertical bar chart | `.barchart`/`.barcol` | height via `--h`; one `.active`. |
| horizontal ranked bars | `.hbars`/`.hbar.active` | transparent track; length = value. |
| donut | `.donut` | conic-gradient, `--p1/--p2`; hole blends with surface. |
| line chart | `.linechart`+`.ln-*` | geometry = data; styling tokenized. |
| twin-bar / KPI result | `.kpibars`/`.kpibar.up/.down`+`.delta` | uses `--pos`/`--neg`. |
| metric | `.metric` | big number + unit + caption. |
| persona / quote | `.persona`, `.qbubble` | centered persona, or attributed quote. |
| finding→opportunity | `.insightcol` | L8 column. |
| flow / node-chain | `.flow`/`.flow-node.active`, `.flow-row` | AS-IS muted, TO-BE accent. |
| feature rows | `.feature-rows`/`.feature-row.headline` | one row filled = headline. |
| insight band | `.card.has-band`+`.band` | dark text-color fill; correct in both modes. |
| bubble cluster | `.bubbles`/`.bubble` | one accent circle, rest muted. |
| section divider | `.section-divider`+`.pill` | accent pill + headline. |
| **#skill chips** | **`.chipcloud`/`.skill-chip`** | concrete skill names as #tags; `.on` = highlighted. Plain-language layer's main tool. |

Useful deck patterns (compose from the above): TOC/目錄 (left title + right numbered outline),
single-scroll export (stack `.slide`s, auto-scale to viewport width — see "Delivery").

---

## Tone modifiers (semantic color)

`.slide.tone-pos/neg/warn` swap the single accent per slide intent (still one chromatic color).
`--pos` + `--neg` may co-occur only inside a KPI/result chart.

---

## Delivery formats

- **Per-slide HTML** — the native unit (`assets/` + one token file; examples are pre-inlined for portability).
- **Single-scroll HTML** — stack every `.slide` in one document; a small script scales each 1920 frame to
  the viewport width so the whole deck scrolls top-to-bottom. Good for review links / GitHub Pages.
- **PDF** — render each slide to image, combine.
- **PPTX** — `pptx/` mirrors the tokens (`tokens.py`) and emits real `.pptx` (`slidegen.py`):
  1920×1080 px → 13.333″×7.5″ (`Inches(px/144)`), `pt = px/2`. Shapes ship with shadow stripped
  (empty `effectLst` + removed style block) for the flat look. Core templates: title, ranked-bars,
  feature-rows; extend `slidegen.py` for more.

---

## The 7-Step Parser (doc → slides)

1. **Name the room first**, then the intent. Who watches, who re-presents? Exec/mixed rooms → maximize
   plain language + concrete examples, minimize internal-mechanism pages.
2. Chunk into atomic claims `A1…`.
3. Classify each → component.
4. Group into slides (≤3 primary cards; a synthesized finding gets its own slide).
5. Pick layout.
6. Confirm mode (ask if unstated) → load one token file. Tone only for result/pain/warn.
7. Validate; fix one item at a time.

## Validation gate

1. One mode, one token file across the set?
2. One chromatic color per slide (KPI `--pos`+`--neg` the only exception)?
3. Charts: inactive muted, active accent?
4. CJK `0.05em`, Latin `0`, line-height `1.5`; no meaningful text below 16px on a deck?
5. Spacing on the `--sN` scale; four-side margins similar; content centered, not floating?
6. **One-read test passed; no stacked-modifier titles; process sentences turned into label + plain sub?**
7. **Every code/level carries a plain label; abstract capabilities shown as concrete #chips where possible?**
8. **Each slide bridges from the previous (no unbridged overview→deep-dive jump)?**
9. **Cross-team content framed as collaboration; behind-the-scenes pages cut or reduced to one example for exec rooms?**
10. No Korean; numbers/dates/products in `.latin`?

## Hard Rules

1. One mode per set. Ask when unsure.
2. One highlight color per slide (KPI `--pos`+`--neg` excepted).
3. No Korean in output.
4. Gradients only as background; never inside a card.
5. Inactive data muted, active accent.
6. Each slide claims one sentence; if two, split.
7. Fonts fixed: Noto Sans TC + Arial. Spacing only from `--sN`.
8. **Titles and captions pass the Plain-Language Layer before delivery.**

## Changelog

- **v7** — Plain-Language Layer (one-read test, no stacked modifiers, concrete #chips, plain labels for
  codes, collaboration framing, cut behind-the-scenes for exec rooms); narrative-continuity rule;
  audience-first parser step; `.skill-chip`/`.chipcloud` component; 16px readability floor; single-scroll
  + TOC documented as delivery/patterns. *(From a live review: titles read as too abstract for a mixed
  manager/PM/RD room; fix is plainer copy + concrete examples, not more visual polish.)*
- **v6** — spacing scale + 12-col grid; band fixed in dark; full component library; semantic tone modifiers;
  real PPTX bridge; both flagships in both modes.
- **v5** — two locked modes via shared base + one token file; insight band; bubble cluster.
- **v4** — 4-color discipline, 7-step parser, layout/card libraries.
