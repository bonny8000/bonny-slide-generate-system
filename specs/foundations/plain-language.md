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
   → label 「任務模式」 + plain sub 「一個任務從頭到尾會用到哪些 skill」.
3. **Concrete over abstract — name names.** Replace category labels with real examples (#chips). Real
   artifact names also signal progress: 「已經開始做的：#元件庫 #CMS 介面審查」.
4. **Who / what / what-they-get**, not the internal mechanism.
5. **Cross-team = collaboration, not replacement.**
6. **Cut behind-the-scenes for exec rooms, or show ONE worked example.**
7. **Frame provisional content as a range, not a closed list** — no 「枚舉/all/最終」; say 範圍/方向 + a
   「先盡量涵蓋，之後再收斂」 note.
8. **Bilingual handles for skimmable lists:** `#English Handle（中文說明）` (English accent, Chinese muted).

Wording stays the author's voice — the layer enforces plainness, it doesn't rename things.

## Writing the words (繁中)

The full rules live in `specs/writing/`, organised by what the writer is deciding — intent, wording,
sentence, title, translation, usage — and not by where a rule was first observed. A rule about how a
condition sits in a sentence governs a caption exactly as it governs any other text. This section is
the always-read layer: four passes, the checks every slide must pass, and when to open a file.

### Four passes, every deck

1. **Read the page's job.** Who reads it, where the text sits (headline, caption, label, quote,
   mock screen), and what the reader must know or decide after reading.
2. **Draft from the source.** Use only what the source gives. Reasons, numbers and promises it does
   not contain stay out. A figure the source lets you compute is fair (4 of 12 could not find the entry,
   so 8 did). A reading of the numbers may be the slide's claim when the numbers it rests on are on the
   same slide; when the data cannot prove it, word it as the team's judgement (「我們判斷」), not as fact.
3. **Scan for drafting habits.** After the deck is drafted, run `specs/writing/drafting-habits.md`
   over it. For each hit ask what the word adds here; keep it if it adds something.
4. **Check the meaning against the source.** Fluent rewrites are where facts change quietly. Go slide
   by slide: numbers and units, where a time span starts, conditions and scope, certainty, who does
   which step, one name per thing, and that the English says no more than the Chinese.

### Checks every slide must pass

- **No comma after the topic; a short headline reads to the end.** A Chinese topic sentence does not
  need a comma after its topic: 「改版後結帳完成率提高 6%」, not 「改版後，結帳完成率提高 6%」. A contrast of
  two clauses keeps its comma (「8 個人找到 Entry Point，但只有 7 個人走完整段流程」). For any other pause,
  break the line or move the second half to the subhead. No final 。; a question keeps its ？.
- **Say it the way the team says it.** Work terms the team says in English stay in English (Entry
  Point, RD 估計, IT team 估計); people are counted as 「8 個人」; a gap is told with 「…，但只有…」; a
  percentage change is 「提高 6%」. The list is in `writing/slide-copy.md` → 團隊的說法, and it wins over
  the general rules in the dimension files.
- **The verb is what happened.** 「回收率分析」 states nothing; write the finding, the change or the
  decision to make.
- **Shortening never widens the claim.** 平均、部分、預計、首次…以來 stay with the number or event they
  qualify. If two findings bear on the decision, the headline does not report only the good one.
- **Research finding.** Name the observed action and the step where it happened. Draft a short
  headline that reads aloud in one phrase and move a second result into a caption. Given eight
  participants and three who needed a hint to find export, try 「8 個人裡有 3 個人需要提示才找到匯出功能」. A
  shorter title can leave the sample size in a visible chart or caption on the same slide.
- **Product change.** Lead with what someone can now do. If a screenshot helps them find a control,
  start its caption with the location or the action that reveals it. Copy visible labels verbatim.
- **Proposed UI.** Use the product's terms and pair each message with an action the product
  supports. Say which text is quoted from the screen and which is proposed. A short title, button or
  one-line hint needs no comma or final period; longer explanations use punctuation where a pause helps.
- **Numbers carry their name, unit and base.** 增加 is not 增至; 人 is not 人次. When a headline says
  「提高 6%」, the start and end values (62% → 68%) are on the same slide, along with the denominator
  and the period.
- **Certainty matches the evidence.** 預計、可望、將、已 are four different claims. Say who judged
  「最難」「最好」. Write 「改版後」 unless the data supports 「因為改版」.
- **One name per thing, deck-wide.** A 「方案」 on slide 3 is not a 「計畫」 on slide 9. When the state
  changes, the word changes with it (草稿 → 已送出).
- **One sentence form per group.** Cards, bullets and labels in a set are all nouns or all
  verb-first phrases.
- **Each step says who acts.** Start steps with the verb; name the actor again when it changes.
- **Taiwan usage and full-width punctuation.** 影片、設定、登入、螢幕, not 視頻、設置、登錄、屏幕.
  Chinese text uses ，、：？「」; half-width `,` `:` `?` belong to English and numbers.
- **The English line says no more than the Chinese.** Same numbers, same conditions, same certainty;
  shorten the phrase rather than shrink the type.

### Open the dimension file when

`writing/slide-copy.md` settles most decks on its own. Open a dimension file when its row applies
and the matching section of `slide-copy.md` leaves the question open. `drafting-habits.md` is the
exception: pass 3 always reads it.

| read this | when |
|---|---|
| `writing/slide-copy.md` | once per deck, before writing final copy — it maps every kind of slide text to its rules and holds the recorded selection preferences |
| `writing/wording.md` | a slide carries numbers, counts, limits or percentages; or a verb or small adverb (才、就、只、還) could change what is promised |
| `writing/sentences.md` | steps, timelines, eligibility or anything with dates, conditions or more than one actor |
| `writing/intent.md` | the slide commits to something, asks for a decision, or reports how sure a finding is |
| `writing/titles-and-body.md` | section covers, openings and endings, chart titles, or a headline that will not settle |
| `writing/translation.md` | the source, or part of it, is in another language and must become Chinese (the English line itself is covered by `slide-copy.md` → 中英並列) |
| `writing/taiwan-usage.md` | a term might be a mainland usage, or the register (spoken → formal) must be chosen |
| `writing/ui-components.md` | the slide shows a mock screen or proposes buttons, messages, empty states or settings |
| `writing/drafting-habits.md` | pass 3, once the deck is drafted |
| `writing/revision-*.md` | a rule needs a worked before/after sentence |
