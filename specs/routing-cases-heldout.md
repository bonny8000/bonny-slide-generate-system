# Routing cases — former held-out set, now regression

This set was originally held out: lexical routing scored 4/10, then shape normalization scored 8/10.
On 2026-08-31 its failures were inspected and repaired. It is now a regression fixture, **not** an
independent benchmark. Keep the original requests and expected layouts unchanged. A future blind
benchmark must be authored and withheld independently; no generalization claim follows from 10/10.
The filename is retained for command compatibility.

Run: `python scripts/validate_routing.py --cases specs/routing-cases-heldout.md`

| request | shape declared from the request | expect |
| --- | --- | --- |
| 這一季要交付什麼，分成幾個階段 | text-only / sequence-dated / few | timeline |
| 我們的客戶大致分成哪幾類 | text-only / grid / few | use-case-cards |
| 使用者的抱怨原句，旁邊放同意的比例 | quote+stat / split / few | qual-quant-split |
| 上線後留存率跟客訴量的變化 | stat / grid / few | results-grid |
| 把三個設計原則列出來，份量一樣 | text-only / grid / few | keyword-cards |
| 這個功能長什麼樣子，畫面上標重點 | ui-screen / split / pair | feature-showcase |
| 我們在市場上的位置跟主要對手 | text-only / matrix / many | positioning-matrix |
| 使用者從註冊到完成訂單會經過哪些步驟 | text-only / sequence / many | service-flow |
| 先問一個問題，再用三個數據回答 | stat+chart+logo / question-then-proof / few | centered-question-evidence |
| 為什麼要選我們，三個理由各有證據 | text-only / rows / few | value-points |

## What the failures teach

**Generic words become attractors.** `persona-cards` won two unrelated requests outright because its
triggers `使用者輪廓` / `使用者樣貌` put the bigram 使用者 in the index — and 使用者 appears in
almost every request this system will ever see. `as-is-to-be` had the identical problem before
(改版), swallowing three cases that belonged elsewhere. A trigger built from common vocabulary does
not route *to* a layout, it routes *everything* to that layout.

So: **triggers must be distinctive, not merely relevant.** Prefer 人物誌 over 使用者輪廓, 留存率 over
數據. Before adding one, ask whether it appears in requests that should land somewhere else.

**Precision beats coverage.** Adding 繁中 triggers to 17 layouts moved blind performance from 30% to
roughly 40%, not to 100%. The remaining gap is not fixable by adding more triggers of the same kind.

**IDF weighting fixed the attractors and did not move the score.** Matches are now weighted by how
distinctive the token is in real deck copy, so `persona-cards` fell from 1.0 to 0.5 on the 抱怨原句
case and stopped winning it by accident. Held-out stayed at 4/10 — because in those cases the
*correct* layout has no distinctive token in the request either, and no reweighting can score a match
that does not exist. Precision was the fixable half. What remains is coverage, and lexical matching
has no answer to it: the request says 留存率, the layout's triggers say 成效指標, and nothing links
them without understanding what the words mean.

That is the ceiling of a lookup table, and the reason the next step is **query normalisation** — have
the agent restate the request as a canonical intention line *before* lookup, so the table is matched
against controlled vocabulary rather than against however the user happened to phrase it.
