---
id: typography
kind: foundation
status: stable
---
# Typography

- **CJK** → Noto Sans TC, `letter-spacing: 0.05em`. **Latin / numbers** → Arial, `0`. Line-height `1.5`.
- Wrap CJK in `.cjk`, Latin/numbers in `.latin`.
- **Bilingual:** 繁中 is primary voice; English is supporting (smaller, muted, or a second line). No Korean.
- **Scale (px):** h1 50 · metric 56 · section 30 · eyebrow 22 · Q 20 · pill 18 · body 17 · caption 14.
- **Readability floor:** no meaningful text below **16px** on a 1920-wide deck.
- A key takeaway line may enlarge to **32–36px** as the slide's punchline.
- **Emphasis:** one keyword per title in `--accent` (color from theme). Don't bold whole sentences.


## Punctuation & line breaks (slides)
- **No terminal 句號 / full stop** on titles, headlines, statements, captions, or short labels. Mid-line
  marks (、 , : ——) are fine; just don't end with 。 or `.`. (Long body paragraphs may keep periods.)
- **Keep a complete clause on one line.** Never let a sentence wrap so a fragment orphans (e.g. 「去。」
  alone on line 2). Break only at a natural separator (—— , :) and wrap each clause so it can't split
  mid-phrase: `white-space:nowrap` per clause, or `text-wrap:balance` on the line. Widen `max-width` or
  drop one font-size step before allowing an ugly wrap. (See the `.statement` / `.nowrap` helpers.)
