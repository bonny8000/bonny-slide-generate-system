---
id: typography
kind: foundation
status: stable
---
# Typography

- **CJK** → Noto Sans TC, `letter-spacing: 0.05em`. **Latin / numbers** → Arial, `0`. Line-height `1.5`.
- Wrap CJK in `.cjk`, Latin/numbers in `.latin`.
- **Bilingual:** 繁中 is primary voice; English is supporting (smaller, muted, or a second line).
  Output stays 繁中 + English unless the user asks otherwise and declares it (`validate_layout --lang`).
  This is an **output** rule; routing triggers are deliberately multilingual (see `generated-router.md`).
- **Scale (px):** h1 50 · metric 56 · section 30 · eyebrow 22 · Q 20 · pill 18 · body 17 · caption 14.
- **Readability floor:** no meaningful text below **16px** on a 1920-wide deck.
- A key takeaway line may enlarge to **32–36px** as the slide's punchline.
- **Emphasis:** one keyword per title in `--accent` (color from theme). Don't bold whole sentences.


## Bilingual pairs expand — leave room before you need it

繁中 is the most compact writing this system produces and English is among the least, so a 繁中 line
and its English partner are **not** the same length. The shorter the 繁中, the worse the ratio:

| 繁中 source | expect the English to run |
|---|---|
| ≤ 10 characters | **150–250%** of the width |
| 11–20 | 130–150% |
| 21–30 | 110–130% |
| 31–50 | 90–110% |
| 51+ | 80–90% |

(Ratios from [seed-design's international-design guidance](https://github.com/daangn/seed-design),
which measures the same effect from Korean; 繁中 behaves the same way, and the underlying source is
[W3C on text size in translation](https://www.w3.org/International/articles/article-text-size.en).)

**What this means on a slide.** A four-character 繁中 headline with an English subtitle beneath it is
the worst case in the table — the English can be two and a half times wider. Fixed-width furniture is
where it breaks: a `.band` tag, a `.btn` label, a card title in a three-up grid, an `.appbar` title in
a mockup. The failure is not subtle but it is late: the English wraps to two lines, the card grows,
the row loses its alignment, and the layout gate reports an imbalance whose cause is a translation
you wrote three steps earlier.

- **Size the container for the English, not the 繁中.** Set the width from the longer line.
- **Never let a bilingual pair sit in a fixed-width box that fits only the 繁中.**
- **Let it wrap, deliberately.** A two-line English subtitle set on purpose reads fine; the same two
  lines arriving by accident push everything below them out of place.
- **Shorten the English rather than shrink it.** Supporting text that drops below the type floor to
  fit is a worse outcome than a tighter phrase.

## Punctuation & line breaks (slides)
- **No terminal 句號 / full stop** on titles, headlines, statements, captions, or short labels. Mid-line
  marks (、 , : ——) are fine; just don't end with 。 or `.`. (Long body paragraphs may keep periods.)
- **Keep a complete clause on one line.** Never let a sentence wrap so a fragment orphans (e.g. 「去。」
  alone on line 2). Break only at a natural separator (—— , :) and wrap each clause so it can't split
  mid-phrase: `white-space:nowrap` per clause, or `text-wrap:balance` on the line. Widen `max-width` or
  drop one font-size step before allowing an ugly wrap. (See the `.statement` / `.nowrap` helpers.)
