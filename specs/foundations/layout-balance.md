---
id: layout-balance
kind: foundation
status: stable
---
# Layout & balance

- **One claim per slide.** If a slide makes two points, split it.
- **Headline = a full claim**, with one keyword emphasized in `--accent`. Not a topic label, not a
  stacked-modifier phrase. (Plain-language: passes the one-read test.)
- **Visual sits next to the text it supports** — chart beside its sentence, not on a separate slide.
- **Balance the quadrants.** Avoid a heavy top with an empty bottom; use a bottom band, a caption row,
  or card min-heights to settle the composition (Img1, Img3 do this with a bottom panel / band).
- **Eyebrow** (section tag like `Background`, `Target Audience`) top-left or centered, small, muted/accent.
- **Bridges:** a deep-dive slide opens with a one-line handoff from the prior slide; major parts are
  separated by a `section-cover` (扉頁).

## Whole-page composition (visual weight)
Read the page as **masses**, not text: the title block, the hero visual, supporting text, and whitespace
each have weight. Balance them so no quadrant is heavy while another sits empty.
- **Anchor, then counterbalance.** Pick one dominant element (the hero visual or the claim); balance it
  with the secondary masses. A lone heavy element on one side reads lopsided — recenter it or add a
  counterweight (caption, second card, bottom band).
- **Equal four-side margin (uniform safe-area).** On a single slide, the overall content is inset by the
  **same margin on all four sides** — top = bottom = left = right (enforced by `.slide`'s equal padding).
  All content lives inside this box; nothing touches the slide edge except an *intentional* full-bleed
  decor / `bleed-shape`.
- **Inside that content box, allocate in balance.** Align to the 12-col grid, fill top→bottom
  (`.grow` / `.vspread`), give equal siblings **equal size + equal gaps**, and sit the composition in the
  **optical middle** — so the allowed area is filled evenly, not heavy on one side / one quadrant.
- Settle a top-heavy page with a **bottom band, caption row, or equal card min-heights** (Img1, Img3).

## Density — not 很空, not 太擠 (the breathing-room rule)
Aim for a comfortable fill: **~30–45% whitespace**. Below ~25% reads **太擠** (cramped); above ~55% reads
**很空** (empty / unfinished).
- **太擠 → remove, don't shrink:** cut to one claim, fewer items, fewer words; widen gaps/padding; split
  into two slides. **Never** drop text below the 16px floor just to fit.
- **很空 → grow the content, not the padding:** enlarge the hero number/visual, add a supporting
  chart/caption/illustration, raise card min-heights, or step the type scale up. Empty space must be
  *intentional margin*, never a void the eye reads as "unfinished."
- Equal siblings get **equal size + equal gaps**; uneven gaps read as accidental.

## Proportional sizing (text / title / icon scaled to their space)
Size by **role + container**, from the scale in `typography.md`. The bigger the box or the more important
the element, the larger its content — **content should fill its box, not float tiny inside it.**
- **Title ↔ body:** a title clearly out-sizes its body (e.g. section 30 / body 17). In a large card, step
  the title up (toward 32–36) so it isn't lost.
- **Number / metric:** on a metric/result slide the hero number is the **largest** thing (metric 56) — it
  must dominate or the proof doesn't land.
- **Icon ↔ text:** an icon *supports* text, so size it to the text beside it (inline 1em · label 20–24 ·
  card-anchor 40–56). An icon must **never out-weigh the title** it accompanies; a card-anchor icon pairs
  with a title, not a caption.
- **Fill the container:** if content looks tiny in its card, the card is too big or the content too small
  — grow the content or shrink the card; don't leave a halo of dead space around it.

## Vertical placement — FILL the full canvas (top to bottom)
**An empty top OR an empty bottom both read as unfinished.** Don't center thin content (empty top), and
don't pin everything to the top either (empty bottom). On a 1920×1080 deck, content should reach the
**full height**.
- **Header + body (+ footer) slides:** header at the top, the **body grows to fill** (`.grow` →
  `flex:1`), and any footer (quote band, source line) sits at the **bottom**. So content spans top→bottom
  with no dead band at either end.
- **Growing isn't enough — distribute the body's content too.** If the body holds a short block, *centering*
  it inside `.grow` just re-creates an empty top + empty bottom *within* the body. Use **`.vspread`** (fill +
  `space-between`) so sub-blocks reach the body's top and bottom, or grow the sub-blocks. *(Round 3 — both
  A/B variants floated a short block in a grown body.)*
- **Fill the body with *meaningful* content, not stretched empty boxes.** If a card stretches tall and
  floats a tiny number inside, that's just relocated emptiness — instead add vertical mass that earns its
  space: a before/after **chart**, more stat rows, a supporting visual (per the density rule).
- **Centered (`.slide` default)** is only for genuinely single-element slides — cover, a statement, a
  centered question. `.slide.top` alone is rarely enough; pair it with a growing body + bottom footer.
- **The one exception (statement / hero-quote / section-divider):** these *may* breathe with generous
  emptiness — but only if the whitespace is **intentional**: block optically centered, symmetric margins,
  one strong axis. The moment content clusters to one side and leaves dead quadrants, the exception is
  void and it reads unfinished. (A/B round 7 — see `preferences.md`.)
*(Learned from A/B round 1: a header-heavy slide with an empty lower half was rejected — "nothing is at
the bottom.")*

## Deck-level visual pacing (the anti-dryness rule)
Per-slide intention mapping alone can produce a technically-correct deck that is **all text-and-boxes** —
every page routed to native cards because nothing triggered the imagery layer. Judge visual pacing at the
**deck level** too, at the outline stage (`slide-plan.md`) and again in self-critique:
- **In a deck of 8+ pages, at least 1–2 pages should carry a genuine visual moment** — a real
  screenshot/photo (`.shot`), a `logo-row`, a device mockup, or a generated editorial explainer. Icons and
  chips alone do not count; they are seasoning, not a visual moment.
- **If no page trips a trigger, elevate the best candidate** instead of shipping a dry deck: the page whose
  intention is closest to a visual route (a tool pipeline → logos or `workflow-transform`; a real product
  or tool being described → ask for its real screenshot per `imagery.md`; a conversation/how-to →
  `agenda-dialogue`). Name the elevated page in the slide plan.
- **This never overrides the gates.** Precise data, dense comparisons, and evidence stay native
  (`content-map.md`); the editorial route still requires a genuine image-generation call — if the generator
  is unavailable, use real assets (`imagery.md`) or a `logo-row`/mockup, never a CSS/SVG imitation.
- Symptom to catch in self-critique: flipping through the rendered deck feels like reading a document.
  That is a **fix**, not a pass, even when every individual page passes.

## Elevation (shadows)
Shadows convey **depth, not drama**. Use the subtle `--shadow-card` / `--shadow-pop` tokens — never a
heavy, dark, far-spread shadow. Most flat cards need **no** shadow at all; reserve elevation for things
that genuinely float (popups, device mockups, overlays), and keep even those soft.
