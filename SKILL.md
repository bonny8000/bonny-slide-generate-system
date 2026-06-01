---
name: bonny-slide-system
description: >-
  Generate bilingual 繁中 + English UX/product slides in two locked visual modes: LIGHT and DARK. Use when Codex needs to create HTML decks, single-scroll HTML, PPTX slides, UX/product case-study slides, progress reports, system or decision presentations, bilingual tag lists, numbered step flows, section covers, KPI/result slides, charts, flows, features, personas, and manager/PM/engineer-readable slide narratives. Traditional Chinese is primary and English is supporting; Korean is never produced.
metadata:
  version: "8.0.0"
  strategy: "Two locked modes · shared base + one token file · plain-language + show-the-reasoning · validation-gated"
---

# Bonny Slide System v8

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
├─ examples/  flagship + supporting layouts in both modes
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

**Exception — section covers (扉頁) may invert.** A full-bleed dark page inside a LIGHT deck is a
*background choice*, not a mode switch (the Iron Rule allows any background). Use it to announce a
new section; content still obeys 4 colors. See the `.section-cover` component.

---

## The Iron Rule (color) — 4 colors absolute max

> **1 background + 1 text + 1 muted + 1 highlight.** `--accent` is the ONLY chromatic color.
> Charts: inactive `--muted-soft`, active `--accent` — never two chromatic colors.

The insight band / section cover use the text color as a fill (`--band-fill`), so they add no color.

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
- **Readability floor:** on a 1920-wide deck, never set descriptive text below **16px**. A key takeaway
  line may be *enlarged* to ~32–36px as the slide's punchline (see worked-example pattern).

---

## Plain-Language Layer (白話層) — run on every title and caption

Decks are read by **managers, PMs, and engineers, not only UX people**, and are often re-presented by
someone else. Copy has to land on first read. (Real failures: 「可彈性配置的模組化技能系統」、
「按任務目標串起跨階段的執行路徑」 — read three times, still unclear.)

1. **One-read test.** If a reader can't say what the slide claims after reading the title once, rewrite.
2. **No stacked modifiers in titles.** A process sentence is not a title: 「按任務目標串起跨階段的執行路徑」
   → short label 「任務模式」 + plain sub 「一個任務,從頭到尾會用到哪些 skill」.
3. **Concrete over abstract — name names.** Replace category labels with real examples as chips. Showing
   real artifact names also signals progress: 「我們已經開始做的:#元件庫 #CMS 介面審查 …」.
4. **Who / what / what-they-get**, not the internal mechanism. 「PM、設計、RD 都能用」 over 「把技能打包發給對應團隊」.
5. **Codes always carry a plain label.** `L0–L4` → 「L0 法規」「L1 系統與狀態」…, state ordering in words (由廣到細).
6. **Cross-team = collaboration, not replacement** (RD/前端): 「交付可用的程式、讓串接更順」.
7. **Cut behind-the-scenes pages for exec rooms, or show ONE worked example.**
8. **Frame provisional content as a range, not a closed list.** When the set is still evolving, do **not**
   say 「枚舉 / all / 最終」. Say 「範圍 / 涵蓋的方向 / range」, show representative examples, and add a
   「先盡量涵蓋,之後再收斂」 note. (Lesson: a stakeholder read "list all skills" as over-committing.)
9. **Bilingual handles for skimmability.** Listing items for a mixed CJK+English room → give each an
   English handle + a short Chinese gloss: `#English Handle (中文說明)`, separated by ·. The handle is
   scannable/quotable; the gloss is understood. (See `.taglist`.)

Title *wording* stays the author's voice — the layer enforces plainness, it doesn't take over naming.

---

## Presenting a system or decision — show the reasoning, not just the result

The single most common senior feedback: *"you jumped to the conclusion; the thinking isn't shown."*
Make the reasoning its own slides, in order, **before** the conclusion:

1. **Method slide** — the numbered steps you actually followed, as a left-to-right `.stepflow`
   (e.g. ① 列出所有 skill → ② 找出關係 → ③ 才決定打包). One line of plain explanation per step.
2. **Detail slides** for the steps that carry weight:
   - the **range/enumeration** (what you listed) — framed as range, bilingual handles;
   - the **relationships** — show 前後(sequence) / 相依(dependency) / 並行(parallel) explicitly.
3. **Then** the conclusion / packaging. Never put the "three ways / final model" before the reasoning.

For a *mechanism*, show **one concrete worked example** as a left-to-right flow (thing → trigger →
result), and end on an **enlarged one-line takeaway** (~32–36px). One real example beats an abstract diagram.

---

## Narrative continuity

Slides must connect. When a deep-dive follows an overview, add a one-line **bridge** that hands off
from the previous slide. Never jump from an overview straight into a sub-topic with no transition. A
**section cover (扉頁)** is the cleanest bridge between major parts.

---

## Spacing, grid & balance

- 8px scale: `--s0:4 … --s9:96`. Roles: `--pad-y:80 --pad-x:96 --gutter:32 --gap-section:48 --pad-card:48`.
- **12-column grid** (`.grid12` + `.col-N`). Splits 6+6 · 7+5 · 8+4 · 4+4+4; equal → `.cards.two/.three`.
- Equal four-side margins; `.slide` is a centered flex column → content sits in the optical middle.
- **Fill, don't leave dead space.** Give light slides presence (card `min-height`, generous gaps).
- Canvas: `.slide.deck` 1920×1080 · `.slide.poster` 1080×auto.

---

## Component library (all in base.css)

| component | class | notes |
|---|---|---|
| vertical / ranked bars | `.barchart`, `.hbars` | inactive muted, one `.active` accent. |
| donut / line / KPI | `.donut`, `.linechart`, `.kpibars` | geometry = data; `--pos`/`--neg` only inside KPI. |
| metric · persona · quote | `.metric`, `.persona`, `.qbubble` | |
| finding→opportunity | `.insightcol` | |
| flow / node-chain | `.flow`, `.flow-row` | AS-IS muted, TO-BE accent. |
| feature rows | `.feature-rows` | one row filled = headline. |
| insight band | `.card.has-band`+`.band` | text-color fill; correct in both modes. |
| #skill chips | `.chipcloud`/`.skill-chip` | concrete names as #tags; `.on` = highlighted. |
| **bilingual tag list** | **`.taglist`** | `#Handle (中文)` · `#Handle (中文)`; for mixed rooms / provisional sets. |
| **numbered step flow** | **`.stepflow`/`.step`** | ①→②→③ method / process / before→after. |
| **section cover (扉頁)** | **`.slide.section-cover`** | dark announce-page; small nav strip + hero title. |
| **labeled split rows** | **`.lrow`** (+`.split`/`.track`) | left badge + content; a row may split into 2 labeled tracks (設計線/程式線, 上線前/上線後). |
| section divider (pill) | `.section-divider`+`.pill` | lighter in-deck divider. |

**Section-cover rule:** the progress **nav strip and "NEXT/接下來" label stay small (~14–18px)**; the
**section title is the hero (~54px)**. (We oversized these once — the page read as shouting.)

Patterns to compose: TOC/目錄 (left title + right numbered outline); worked-example flow (`.stepflow`
+ enlarged takeaway); relationship triplet (three small cards: 前後 / 相依 / 並行).

---

## Tone modifiers (semantic color)

`.slide.tone-pos/neg/warn` swap the single accent per slide intent. `--pos`+`--neg` co-occur only inside a KPI chart.

---

## Delivery formats

- **Per-slide HTML** — native unit (`assets/` + one token file).
- **Single-scroll HTML** — stack every `.slide`; a small script scales each 1920 frame to viewport width
  so the deck scrolls top-to-bottom (right-edge dot nav). Best for review links / GitHub Pages.
- **PDF** — render each slide to image, combine.
- **PPTX** — `pptx/` mirrors tokens (`tokens.py`) → real `.pptx` (`slidegen.py`): px/144 = inches, pt = px/2,
  shadows stripped for the flat look.
- **Candidate comparison** — when a layout choice is subjective, render **2–3 full versions stacked** and
  let the person pick, rather than guessing. (Used this for a stage-table layout; it saved rework.)

---

## The 7-Step Parser (doc → slides)

1. **Name the room first**, then the intent. Exec/mixed rooms → maximize plain language + examples;
   show the *reasoning*, not just results; minimize internal-mechanism pages.
2. Chunk into atomic claims `A1…`.
3. Classify each → component.
4. Group into slides (≤3 primary cards; a synthesized finding gets its own slide).
5. Pick layout. For a system/decision: method → range → relationships → conclusion → packaging.
6. Confirm mode (ask if unstated) → load one token file. Tone only for result/pain/warn.
7. Validate; fix one item at a time.

## Validation gate

1. One mode, one token file (section covers may invert dark — allowed)?
2. One chromatic color per slide (KPI `--pos`+`--neg` excepted)?
3. Charts: inactive muted, active accent?
4. CJK `0.05em`, Latin `0`, line-height `1.5`; no meaningful text below 16px?
5. Spacing on the `--sN` scale; four-side margins similar; content centered, not floating?
6. One-read test; no stacked-modifier titles; process sentences → label + plain sub?
7. **Does the deck show the method/reasoning, or jump straight to conclusions?**
8. **Provisional lists framed as range (not "all/枚舉"), with examples + a收斂 note?**
9. Codes/lifecycle items carry plain (and bilingual, for mixed rooms) handles?
10. Each slide bridges from the previous; section covers used between major parts?
11. Cross-team framed as collaboration; behind-the-scenes cut or reduced to one example for exec rooms?
12. Section covers: nav small, title hero? No Korean; numbers/dates/products in `.latin`?

## Hard Rules

1. One mode per set (section covers may invert). Ask when unsure.
2. One highlight color per slide (KPI `--pos`+`--neg` excepted).
3. No Korean in output.
4. Gradients only as background; never inside a card.
5. Inactive data muted, active accent.
6. Each slide claims one sentence; if two, split.
7. Fonts fixed: Noto Sans TC + Arial. Spacing only from `--sN`.
8. Titles and captions pass the Plain-Language Layer before delivery.
9. For a system/decision, show the reasoning before the conclusion.

## Iteration heuristics (from live reviews)

| feedback | response |
|---|---|
| 看不懂 / 太抽象 | Plain-Language Layer: plain titles, real examples. |
| 跳太快 / 中間沒講到 | add a method slide + bridges (enumerate → relate → decide). |
| 這做了嗎 / 太空泛 | name real artifacts as chips. |
| 太細 / 資訊太多 | consolidate to names + labels; push full descriptions to appendix / Notion. |
| 講太死 / 像最終版 | frame as range; "先盡量涵蓋,之後再收斂". |
| 排版見仁見智 | offer 2–3 versions to pick (candidate comparison). |

## Changelog

- **v8** — "Show the reasoning, not just the result" pattern (method slide → range → relationships →
  conclusion); section cover (扉頁) component with small-nav / hero-title rule + dark-invert exception;
  bilingual tag list `#Handle (中文)`; "frame as range, not a closed list" copy rule; numbered step flow,
  labeled split rows, worked-example + enlarged-takeaway, relationship triplet (前後/相依/並行);
  candidate-comparison delivery; iteration-heuristics table. *(From an end-to-end deck build + three
  rounds of stakeholder feedback.)*
- **v7** — Plain-Language Layer; narrative-continuity; audience-first parser; `.skill-chip`; 16px floor.
- **v6** — spacing scale + 12-col grid; band fixed in dark; full component library; tone modifiers; PPTX bridge.
- **v5** — two locked modes via shared base + one token file; insight band; bubble cluster.
- **v4** — 4-color discipline, 7-step parser, layout/card libraries.
