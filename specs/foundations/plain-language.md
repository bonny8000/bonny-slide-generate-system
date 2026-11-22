---
id: plain-language
kind: foundation
status: stable
---
# Plain-language layer (白話層) — run on every title & caption

Decks are read by managers, PMs, and engineers — not only UX people — and often re-presented by
someone else. Copy must land on first read.

1. **One-read test.** If a reader can't say what the slide claims after reading the title once, rewrite.
2. **No stacked modifiers in titles.** A process sentence isn't a title: 「按任務目標串起跨階段的執行路徑」
   → label 「任務模式」 + plain sub 「一個任務,從頭到尾會用到哪些 skill」.
3. **Concrete over abstract — name names.** Replace category labels with real examples (#chips). Real
   artifact names also signal progress: 「已經開始做的:#元件庫 #CMS 介面審查」.
4. **Who / what / what-they-get**, not the internal mechanism.
5. **Cross-team = collaboration, not replacement.**
6. **Cut behind-the-scenes for exec rooms, or show ONE worked example.**
7. **Frame provisional content as a range, not a closed list** — no 「枚舉/all/最終」; say 範圍/方向 + a
   「先盡量涵蓋,之後再收斂」 note.
8. **Bilingual handles for skimmable lists:** `#English Handle (中文說明)` (English accent, Chinese muted).

Wording stays the author's voice — the layer enforces plainness, it doesn't rename things.

## Taiwanese Traditional Chinese

When drafting or reviewing zh-TW slides, look for the installed skill named `zh-tw-writing`.
Use its registered path, a path the user supplied, or the sibling `../zh-tw-writing/SKILL.md`
relative to the slide system's root. Read its `SKILL.md` and the 簡報 section of its
`references/formats.md` once per deck. Consult 介面文案 in that file when the slide proposes
button labels, field hints or error messages. If the companion is unavailable, use the following
checks and continue with the deck. Layout, theme and output language follow the slide brief.

- **Research finding.** Name the observed action and the step where it happened. Draft a short
  headline that reads aloud in one phrase. Move a second result into a caption. For example, given
  eight test participants and three who needed a hint to find export, try「8 人中有 3 人需要提示才找到匯出功能」.
  A shorter title can leave the sample size in a visible chart or caption on the same slide.
  Keep units, conditions and uncertainty when shortening or adding English.
- **Product change.** Lead with what someone can now do. If a screenshot helps them find a control,
  start its caption with the location or the action that reveals it. Copy visible labels verbatim.
- **Proposed UI.** Use the product's terms and pair each message with an action the product supports.
  For a short title, button or one-line hint, try phrasing that needs no comma or final period.
  Longer explanations can use punctuation where a pause helps.
