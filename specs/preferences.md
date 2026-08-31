# Learned preferences — the taste layer (built from A/B rounds)

Foundations are *rules*; this file is *taste* — design choices the user revealed by picking between
variants. Apply it alongside the foundations and `self-critique.md`. Each entry notes the round it came
from so it's traceable (and revisable if a later round contradicts it).

## ⭐ Principles digest (read this first)
Fifty A/B rounds distilled to a dozen transferable principles. Reach for these first; the per-component
sections below are the worked detail. When two principles tension, the slide's **intent** breaks the tie.

1. **Compose to the amount of meaningful content.** A substantial header/body page may fill vertically;
   compact content keeps its header and body together as one centred group. Do not pin a tiny header
   far from its cards merely to touch the canvas edges. This reconciles the later composition rule in
   `layout-balance.md`; R51 B confirms this for the tested keyword-card page. *(R1, R3, R7)*
2. **Size the container to its content.** Match peer-panel heights and alignment, but keep content grouped
   with controlled gaps. Shrink a hollow container or add real evidence; do not spread a few labels
   across an oversized box just to pass a density check. *(R9, R14, R24, R38, R40)*
3. **Content-density gates the form.** Pick the form to match how much real content you have; never stretch
   thin content (a 2-pt "trend", a one-line persona, an empty mock) to fill a shape built for more. *(R8,
   R11, R14, R38)*
4. **Sequence → vertical; parallel peers → columns/grid.** Steps & timelines run vertical; co-equal sections
   /options/agenda items get full-height lanes. *(R2, R5, R6, R20)*
5. **Match form to intent & audience.** verdict-led to convince / table to let a skeptic verify (R4);
   minimal for emotion / substantiated for proof (R7, R13); analytical bars+% / evocative trapezoid (R32);
   pipeline horizontal / stack vertical (R40).
6. **Accent is a scarce, precise highlight.** One chromatic accent; pinpoint the single load-bearing keyword,
   don't flood the clause or many body phrases (bold ink carries the rest). A single-hue tint *ramp* is the
   only sanctioned widening — and only to encode ranking. *(R36, R45, R48)*
7. **Emphasis-by-ink > emphasis-by-fill** — unless the fill *also* supplies mass to a sparse composition or
   encodes a genuine ranking. Accent the type (label, numeral, key cell) by default; paint a surface only
   when it earns its keep. *(R26, R31, R34, R41, R42, R44, R45)*
8. **Build emphasis & labels from robust in-flow layout** — card fill/height/weight, outside-the-shape label
   gutters, wrapping text. Never a floating badge, a reversed-out fill that can vanish, a fixed-width column
   that overflows, or text trapped in a resizing container. Re-screenshot anything floated. *(R16, R18, R31,
   R35, R50)*
9. **Number leads, chart supports.** Round the hero number to a memorable shape and footnote the decimals;
   annotate the delta when movement matters; a chart earns dominance only when its *trajectory's shape* is
   the message (≥6–8 pts / a crossover). *(R1, R8, R11, R16, R25, R29, R39, R46, R47)*
10. **Real assets earn dominant space; placeholders never.** A real photo/screenshot earns a hero half/top
    and adds credibility; a placeholder given that weight steals focus and reads unfinished — so **ask the
    user for the asset** (`imagery.md`) or fall back to a text-led layout. *(R22, R24)*
11. **Don't encode the same thing twice.** If the index already shows deck position, the progress dots are
    redundant; if a column is tinted as the winner, don't also re-color its negatives. *(R12, R50)*
12. **Always render → screenshot → self-critique; keep shadows subtle.** Structural checks never substitute
    for seeing the pixels; run modern-web-guidance on the HTML. *(`self-critique.md`, every round)*

## Recorded refinements (2026-08-31)
- R51 B: centre the compact keyword composition as a group.
- R52 A: use an accent-soft surface for the lead supporting metric. Keep all numeric values on
  a shared alignment axis; the surface boundary must not shift the first value inward.
- R53 A: the tested three metric cards benefit from intentional height (430px), with centred content.
  This is a contextual exception to shrinking every container to its text, not permission for hollow panels.
- R54 B: prefer hairline row separators to zebra fill in the tested comparison table.
- R55 A: parallel value points may share the accent on labels/chips. Keep one hue, not one arbitrary
  winner among peers. This qualifies the earlier "single highlighted point" default.

## Vertical fill
Historical round notes below describe their original examples; the current composition rule is the digest above.
- **Fill the full canvas, top → bottom.** An empty top AND an empty bottom both read unfinished. Pattern:
  header at top → body grows (`.grow` = `flex:1`) → footer (quote / source line) pinned at the bottom.
  *(Round 1 — a top-clustered slide with an empty lower half was rejected.)* Also in `layout-balance.md`.

## Results / metric slides
- **Prefer a dominant hero number + open supporting stats** (hairline dividers) over a grid of fully-boxed
  metric cards. The airier, editorial treatment beat the boxed "dashboard" for a results slide.
  *(Round 1 — variant A > variant B.)*
- **Keep the hero and its supporting stats close.** Size the hero column to its content; don't leave a dead
  horizontal gap in the middle between the big number and the supporting numbers. *(Round 1.)*

## Process / steps slides  (Round 2 — B > A, 2–1 judge panel)
- **Prefer a clean vertical stacked list** (one top-to-bottom 1→N scan path) over horizontal tall
  step-cards. Horizontal step-cards top-load their content and leave empty card-bottoms; the vertical list
  fills the canvas and reads faster for an exec skim.
- **Stretching a box to fill height just relocates emptiness.** Give each stretched row meaningful content
  that spans its width — e.g. a **right-anchored step icon / mini-visual** — so there's no empty right side
  or empty bottom. Keep row height comfortable, not exaggerated.
- **Crescendo the critical path:** give the payoff step a subtle accent (fill/border) so 1→3 builds; mark
  optional steps lighter (dashed/muted). Both treatments read clearly.

## Research-finding / quant + qual slides  (Round 3 — A > B, 2–1 judge panel)
- **For a 2-value contrast, show the two numbers inline** (e.g. `48s → 9s`) rather than a 2-bar chart. A
  tiny bar chart that needs a written caption to explain its own ratio isn't earning its space — inline
  numbers read as one instant eye-stop.
- **Give quotes room to breathe as wide, equal cards** — not crammed into a narrow stacked column.
- **Don't over-weight the single accent with a large filled block** (e.g. a big periwinkle bar). Accent is
  a precise highlight, not a mass.
- **Rank co-equal stats:** when one number is the finding (62%) and another is the mechanism (48s→9s),
  let the finding lead (larger / labelled) — don't give them identical weight.

## Filling a grown body — distribute, don't center  (Round 3 — both variants floated)
- **`.grow` fills the body *region*, but its *content* must fill too.** Centering a short block inside a
  grown body re-creates an empty top + empty bottom *within* the body. Use **`.vspread`** (fill +
  `space-between`) to push sub-blocks to the body's top and bottom, or grow the sub-blocks themselves.

## Decision / recommendation slides  (Round 4 — B > A, 2–1 judge panel)
- **When the recommendation is already made, lead with the verdict.** Winner as a hero card + 3
  pre-digested reasons; show the also-rans small, each with its one disqualifier. Verdict-led beats a
  neutral comparison table — it lands the call in a second, and the asymmetry signals confidence.
- **But keep the decisive trade-off visible.** The cost/timeline that justifies the call ("6 weeks is
  acceptable") is load-bearing for buy-in — promote it (e.g. a cost chip), don't bury it in fine print.
- **Match framing to intent** (the real lesson): **verdict-led to *convince*** (decision made, exec buy-in)
  vs **a full comparison table to let a skeptic *verify*** (decision still open / analytical audience).
  When using the table, give cells a light encoding (check/X or tint) so the winning row pops.

## Roadmap / timeline slides  (Round 5 — B > A, 3–0 unanimous)
- **Prefer a vertical time-rail over a horizontal cascade.** Top→bottom matches reading order and is a
  stronger "time passing" cue; it marks the current phase unambiguously (colored title + inline badge +
  enlarged node on one line); and it **fills the canvas top→bottom**. A staggered horizontal cascade
  strands content in the upper half (empty bottom) and its "current" marker floats and competes with the stagger.
- **Make the rail a progress bar:** accent from the top down to the current node, gray below — the rail
  itself shows how far along the plan is.
- **Don't hug the left:** widen each phase to a near-full-width row (date → title → deliverables) so the
  right side isn't a dead zone.

## Hierarchy / IA slides  (Round 6 — B > A, 3–0 unanimous panel)
- For a hierarchy of **parallel peer sections**, a **column-per-section sitemap** beats a vertical indented
  tree: equal columns read instantly as "N parallel sections," containment shows section→child, and the
  accent can cascade the full column height. An indented tree hugs the left (dead right side), makes the
  last section read as "and finally…", and confines emphasis to one chip.
- **To mark "the bet," cascade the accent down the whole column** (header + tinted sub-cards / a
  column-wide panel) — a single header chip dissipates the emphasis.

## Cross-round meta-rule — sequence vs parallel  (Rounds 2, 5, 6)
The rule is NOT "vertical always wins." **Match orientation to the data's structure:**
- **Sequential** items (process steps, timeline phases) → **vertical** rail/list — a horizontal cascade
  strands content with an empty bottom (R2: vertical list > horizontal step-cards; R5: vertical rail >
  horizontal cascade).
- **Parallel peers** (sections, values, options, use-cases) → **column grid** — each peer gets a full-height
  lane and the canvas fills (R6: sitemap columns > indented tree; also keyword-cards / use-case-cards).

## Testimonial / quote slides  (Round 7 — A > B, 2–1 Workflow panel)
- **The quote is the hero:** set the human voice as one large, optically-centered statement and let it
  stand alone. Proof stats, avatars, eyebrow titles, takeaway labels are credibility props that *compete*
  with the voice — add them only when a skeptical B2B buyer needs verifiable magnitude (the credibility
  dissent). Match to audience: **minimal for emotional impact / memorability; substantiated for proof.**
- **Never restate the quote's punchline as a title** — it spoils the line before it lands.
- **One accent inside the quote** (the highlighted before→after number), not a separate stats column.
- Constrain the hero quote to **~60–70% width** (not edge-to-edge) for a tighter, poster-like shape.

## Fill-the-canvas EXCEPTION — statement / quote slides  (Round 7)
The fill rule has **one legitimate exception**: a **statement / hero-quote / section-divider** slide may
breathe with generous emptiness — **but only when the whitespace is *intentional***: the block optically
centered, symmetric top/bottom + left/right margins, a single strong vertical axis. The exception is
**forfeited the moment content clusters to one side and leaves dead quadrants** (that reads unfinished, not
composed). Empty space must *frame* the hero, not orbit it.

## Multi-metric / dashboard slides  (Round 8 — B > A, 3–0)
- **Give one metric the lead; the rest recede.** An equal-weight 2×2 grid has no focal point and forces
  scanning. Promote the lead indicator to a **hero element with a real multi-point chart** (axis labels,
  baseline, integrated value+delta) and stack the others as compact supporting callouts.
- **A sparkline needs ≥3–4 points** — a 2-point "trend" is a content-free stub that breaks the trend the
  title promises. If you only have before/after, use inline numbers, not a mini-line.
- **Title asserts the takeaway** ("啟用率帶頭走高…"), not the category ("…的季度走勢"); layout hierarchy must
  enact the claim. Chart x-axis chronological (oldest left), label all points.

## Benefit / feature "set" slides — icons earn their place  (Round 9 — A > B, 2–1)
- **Keep the icons.** A disciplined monochrome icon family makes a benefits set scannable and instantly
  categorized, and ships more polished than a purely typographic (number-only) version. A 01/02/03 index
  reads as a *sequence* — wrong signal for parallel benefits.
- **But icons don't fix fill:** size the cards to fill the body top→bottom **and anchor/distribute** their
  content (icon-top / title+desc / optional accent-bottom). Short centered cards leave dead top/bottom
  bands; over-tall cards leave content center-stranded (hollow). Solve fill first — the icon is a bonus.

## Theme / mode — match to the slide's job  (Round 10 — DARK > LIGHT, 3–0, hero-stat statement)
- **A single hero stat in negative space is the canonical DARK-theme case:** figure-ground contrast makes
  the accent numeral + white statement *glow* off near-black; the same on white reads soft and merely calm.
- **Match theme to emotional job, not a default:** **dark = spotlight on one number / dramatic statement
  (impact); light = dense, reading-heavy layouts where airy white aids scanning (legibility).**
- On dark, lighten small muted captions one step so methodology/source lines stay legible.

## Chart type — bar vs line for a trend  (Round 11 — B > A, 3–0 unanimous)
- **Short single-series trend where the *ending value* is the headline → bar chart, not line.** Discrete
  bars fill the card edge-to-edge, the final bar can be **accent-highlighted as a hero with its value
  labelled on-chart** (e.g. `28k`), and a flex/height layout is screenshot-stable. A thin polyline strands
  its mass in the lower-right, leaves a dead whitespace triangle, and pushes the actual number to a footnote.
- **Reach for a line chart only when the *shape of the path* is the message** — many points (≳8),
  volatility / inflections to trace, or multiple series to compare. Then the trajectory itself carries the
  insight and bars would be too busy. (Cohabits with the dashboard sparkline rule, R8: ≥3–4 points or use
  inline numbers.)

## Comparison-table cell encoding — icon + semantic color  (Round 12 — B > A, 3–0 unanimous)
- **Encode have/have-not with form AND color: accent check for "yes", muted-gray cross for "no".** Icons let
  the eye parse the matrix in one sweep; the absent mark must **recede everywhere — including inside the
  tinted winner column.** Plain O/X *text* forces glyph-by-glyph decoding.
- **Never tint a negative mark in the accent.** Round 12's losing variant painted a Pro-column `X` the same
  accent purple as the positive marks, so the tinted winner column *inverted* its own message (a "no" read
  as a triumphant "yes"). Accent lands only on present/winning marks. (Extends the decision-table encoding
  note in R4.)

## Closing / CTA slide — recap the proof before the ask  (Round 13 — B > A, 2–1)
- **Default: headline + a 3-stat recap (the proof) above the CTA buttons.** The stat trio
  (`−89% / 4.6 / +38%`) gives an instant, memorable reason to click and fills the canvas as a balanced
  centered column — it won clarity *and* balance-fill.
- **Drop to a bare headline + 2 buttons only when** the proof already lives on the prior slide, the labels
  risk wrapping / export breakage (the dissent — minimal is the most overflow-proof), or a deliberately
  quiet, high-confidence close is wanted. *Recap by default for a standalone closer; minimal when robustness
  or restraint outranks recap.*

## Persona slide — one hero by default, gated by content density  (Round 14 — A > B, 2–1)
- **Default to ONE detailed full-width hero persona:** a single face + name + resonant quote gives one
  unambiguous "who is this for", and goals/pains columns add depth without splitting attention. It reads as
  a complete, content-sized card.
- **Use two side-by-side personas ONLY when the slide's job is contrast** (distinct segments / ICPs) **AND
  each card carries equal, card-filling depth** (≥2 goals + ≥2 pains) so neither runs more than ~25% empty.
  Round 14's losing variant stretched thin content (one quote + one pain) to full height → both cards ~60%
  empty, which reads as a layout *defect* on export. **One rich persona beats two hollow ones.**

## Icon style — filled for focal rows, line for secondary  (Round 15 — B > A, 2–tie–1)
- **Step/process/feature rows that are a *focal* element → filled glyph on a solid accent chip.** The
  saturated chips become three equal-weight anchors that set the 1-2-3 rhythm with near-zero decoding effort
  and make the single accent read decisively — and they survive headless-Chrome export where pale tints
  muddy. **Reserve stroked line icons on soft-tinted chips for *secondary* rows meant to recede.**
- **The balance lens is blind to this choice** — fill style changes glyph *weight*, not canvas composition.
  Decide on focal intent + export robustness, not layout. (Refines R9: icons earn their place — now *which*
  icon weight, by role.)

## Cross-round meta-rule — content density gates the form  (Rounds 11, 14; cf. 8)
Several rounds converge on one principle: **pick the form to match how much real content you have, and never
stretch thin content to fill a container.**
- A 2-point "trend" isn't a line/sparkline (R8); a ≤8-point trend with a headline value is bars, not a line
  (R11); one fleshed-out persona beats two hollow stretched cards (R14).
- The failure mode is always the same — *a container sized for content you don't have reads as a defect, not
  as breathing room.* (This is the disciplined inverse of the statement-slide whitespace exception in R7:
  emptiness is only "composed" when it's intentional and symmetric, never when content was stretched thin.)

## Single-proportion viz — gauge for composure, big number for punch  (Round 16 — mixed, A 1 / B 2)
- **Default to a ring / donut gauge** for one proportion (e.g. 73%): the accent arc over a muted track
  encodes part-of-whole so the proportion is *felt*, it fills the canvas as two balanced columns (gauge
  anchoring the left, headline + context on the right), and it reads more on-brand (accent confined to the
  arc + one highlighted phrase; the numeral itself stays neutral ink).
- **Switch to a BIG typographic number (no chart)** only when the stat *is* the headline and must land in
  one glance — a punchline/hero moment with one focal point and zero eye travel. *Its risk:* a lone centered
  number strands dead whitespace above and below (cf. the fill rule). **Never pair a gauge with a number so
  large the arc is redundant** — the arc then just shrinks the number and splits focus. (Cf. results hero
  number, R1.)

## Section dividers — the biggest element must carry meaning  (Round 17 — B > A, 3–0 unanimous)
- **Hero the 繁中 keyword, demote the number to a small `NN / NN` index.** A giant section *number* wins the
  eye with a glyph that carries no meaning, forcing a second hop to the title; a giant *keyword* makes the
  topic itself the focal point and lands instantly. Center the lockup on the grid so the whitespace reads as
  the intentional statement-slide kind (R7), not a lopsided left-edge cluster.
- **Flip to a giant numeral only when oversized numbers are a deliberate, recurring deck motif** (a
  navigational through-line) — and even then anchor it on the grid, never the bleed edge.

## Problem framing — annotated mockup when pain is spatial  (Round 18 — mixed, B 2 / A 1)
- **When pain points map to specific regions of a real UI, show an annotated product mockup** (browser-window
  mock + numbered callout pins matched to side-notes) instead of a text-card list. The pins anchor each pain
  to *where* it lives, creating cause-and-effect, and fill the canvas in two columns. This is the imagery
  lever from `imagery.md` made concrete.
- **Fall back to numbered text cards** when the pains are abstract / non-spatial, OR when export fidelity
  must be guaranteed. **Pin placement must be grid/flow-anchored, never hard-coded absolute px** — the
  brand-code judge flagged absolutely-positioned pins as drifting on panel edges under headless-Chrome export
  (see the code-quality meta-rule below). Always re-screenshot to verify pin positions.

## Two-option comparison — table for substance, VS-cards for a binary  (Round 19 — B > A, 3–0 unanimous)
- **When two options differ on 3+ comparable criteria (most real build-vs-buy calls), use a criteria-as-rows
  comparison table** with the recommended column tinted and winning cells in the accent. The eye scans each
  head-to-head via the tinted column, it fills the canvas evenly off the headline, it earns credibility by
  honestly showing the loser's one win, and it survives export. (Cell encoding per R12; verdict-vs-table
  framing per R4.)
- **Reserve side-by-side VS-cards for a near-binary, emotional "pick a side" reveal** (1–2 dimensions, the
  rivalry *is* the message). Two cards strand content in a mid-page stripe and force the eye to jump the VS
  gap to pair unaligned bullets — they read as decoration the moment the comparison gets substantive.

## Agenda / section overview — grid over wide list  (Round 20 — B > A, 2–1)
- **For a short agenda (≤6 sections), prefer a 2-column card grid** with number + 繁中 title + English
  stacked as one tight unit per card, and the **final item as a full-width accent-tinted lead card** for a
  deliberate focal endpoint. Each item parses in a single fixation and both halves of the canvas fill evenly.
- **A numbered full-width vertical list wins only on austerity / render-safety** (the brand-code dissent: no
  fills, zero positioning risk) — but across a wide row it strands the English label at the opposite edge and
  leaves a dead center band. (This is the *parallel-peers → grid* meta-rule, R6/cross-round, applied to an
  agenda: sections are parallel peers, not a sequence to walk.)

## Cross-round meta-rule — absolute positioning is export-fragile  (Rounds 16, 18; cf. modern-web-guidance)
The brand-code lens repeatedly rewarded **grid/flow layout** and penalized **hard-coded absolute coordinates**
under headless-Chrome screenshot export. SVG arcs with centered text (R16) and callout pins (R18) are the
high-risk cases: they render pixel-correct *only* when the geometry is anchored to the element box, not to
guessed `top/left` px that drift if the container resizes. **Prefer `grid`/`flex` placement, percentage- or
anchor-based offsets, and `transform`-centering; if you must position absolutely, re-screenshot and verify
every floated element sits where intended.** (Aligns with the modern-web-guidance code-quality review step in
`self-critique.md`.)

## Opening / title slide — editorial-left by default, centered for a cinematic hero  (Round 21 — mixed, A 1 / B 2)
- **Default to a left-aligned editorial title:** a full-height accent rule down the left edge, a **two-line
  stacked** bilingual title, subtitle, and a **metadata footer** (提案 / 日期 / 對象). It fills the canvas
  top→bottom (no marooned-middle dead bands), carries context, and stacking the two-color title on separate
  lines removes mid-string wrap risk under export.
- **Reserve the centered, symmetric single-line title for a content-light cinematic opener** — when the
  title alone is the whole payload and you want a deliberate "statement" feel. It wins raw glance-impact but
  strands a thin mid-canvas stripe unless the frame is wide enough to avoid wrapping. (This is the
  statement-slide whitespace exception, R7, applied to openers.)

## Testimonial — portrait panel only with a REAL photo  (Round 22 — mixed, A 2 / B 1)
- **Default: small avatar glyph + centered hero quote** (the R7 quote-as-hero, pure flexbox, accent on one
  phrase). It survives any quote length and keeps strict color discipline. Its only weakness — empty
  top/bottom bands — is fixed by **enlarging the quote / tightening vertical rhythm, never by bolting on a
  fake panel.**
- **A large full-height portrait panel earns its half of the canvas ONLY when a genuine photo exists.** With
  a real face it balances mass and adds human credibility; with a placeholder glyph it is decorative weight
  that steals focus from the quote, and the absolutely-positioned badge + single-line quote are export-
  fragile. → When you want this layout, **ask the user for the real portrait** (`imagery.md`); don't ship a
  placeholder in hero position.

## Single key insight — callout band by default, oversized inline for max impact  (Round 23 — A > B, 2–1)
- **Default: a full-width accent-tinted callout band** (icon + a short "the one thing" label + the sentence),
  with a context paragraph above. The band spreads mass edge-to-edge so the lower third doesn't strand dead
  space, wraps safely under export, and frames the line as the deliberate payload.
- **Drop the box for a large inline highlighted sentence only as an intentional high-impact exception** — and
  only if you commit to making it *genuinely oversized* (~2× the boxed size) and fill the right third.
  Unboxed, it tends to under-fill, pool weight in the left column, and tempt fragile hand-tuning (manual line
  breaks, dangling em-dashes, **underlined CJK** glyphs — avoid all three).

## Single-feature showcase — size the element by meaning, not by space  (Round 24 — A > B, 2–1)
- **Side-by-side (text + mockup) is the default** when the mockup is a placeholder or low-information: title +
  3 bullets stay paired with the visual in a scannable F-pattern, accent discipline and footer margin hold.
- **Give a mockup hero/dominant (stacked-on-top, wide) weight only when the screenshot is rich, legible, and
  IS the message worth seeing large.** Round 24's losing variant gave the most visual weight to three empty
  lavender panels that said the least, flooded ~60% of the canvas with accent-tint (breaking one-accent
  discipline), and crushed the real text into a thin bottom strip. **Never let a content-empty element become
  the focal point just to fill space.**

## Single KPI — annotate the delta when movement matters  (Round 25 — B > A, 2–1)
- **When a single KPI's *movement* is the point, pair the big number with a delta badge (`▲ +12pt`) + a tiny
  sparkline + a one-line context sentence** so the direction and the "so what?" read in one glance. The bare
  number alone shows magnitude but not meaning.
- **Keep it a bare number only for a trendless constant / target**, or when headless-export robustness is the
  explicit priority. (Sparkline still needs ≥3–4 points per R8; results-hero sizing per R1.)

## Cross-round meta-rule — real assets earn dominant space; placeholders never do  (Rounds 22, 24; cf. 14, 18)
A recurring verdict: **an element's visual weight must be justified by the meaning it carries, not the space
it fills.** A real portrait or a rich, legible product screenshot earns a hero half/top of the canvas and adds
credibility; a *placeholder* glyph or empty mock given the same weight steals focus, breaks one-accent
discipline (large tinted panels), and reads as an unfinished asset. This is the empirical *why* behind the
ask-for-assets rule in `imagery.md`: **before composing a layout around an image/mockup as the hero, get the
real asset from the user** — otherwise fall back to a text-led layout (centered hero quote, side-by-side
feature, callout band) that fills the canvas on its own. (Generalizes the content-density-gates-the-form rule
above: thin/absent content must never be stretched to fill, and absent *visual* content must never be
promoted to focal.)

## Co-equal KPI row — open numbers by default, boxes only to carry the canvas  (Round 26 — mixed, A 2 / B 1)
- **For 3 co-equal KPIs (no single hero), default to open numbers on hairline dividers** — no boxes, no
  shadows. The colored numbers pop straight off the white field, nothing competes, and the three read as one
  unified result (extends the open-editorial treatment from R1). It also keeps strictest 4-color discipline.
- **Switch to flat cards only when the stat row must fill the lower canvas alone** (no chart/body/footer to
  give the bottom mass) — the card fills add vertical footprint. If you box them, **keep fills flat (skip the
  drop shadow — it bands under export) and center the content** so they read as one story, not three
  detached widgets. (The bare row's weakness — a thin floating stripe — is fixed by `.vspread`/surrounding
  content, per the fill rule, not by adding chrome.)

## Before → after — side-by-side for one hero, stacked for a list  (Round 27 — A > B, 3–0 unanimous)
- **For a single hero before→after metric (48 min → 5 min), put both values side-by-side on one eye-line
  with a horizontal arrow between.** The brain reads the shrink in one horizontal sweep, the two tall cards
  give vertical mass and fill the width, and wide vertical CJK columns tolerate long 繁中 bullets without
  truncation. (改版前 neutral card → 改版後 accent-soft card reinforces the direction.)
- **Reserve the stacked (vertical) layout for *lists* of multiple before/after pairs or short-label rows** —
  there the vertical rhythm reads as a scannable table; for one hero comparison it spreads the two numbers
  apart and leaves each thin full-width row half-empty (and forces CJK truncation in the cramped slots).

## Text-heavy prose — one column for flow, two only for parallel volume  (Round 28 — A > B, 3–0 unanimous)
- **Flow continuous prose (sequential / cause-effect paragraphs) into ONE column with a capped measure.** It
  preserves one top-to-bottom reading path, lets the subhead anchor all the text, breaks CJK lines cleanly,
  and is export-robust. **If a single column feels too wide, cap its measure (`max-width`) — don't split it.**
- **Two columns only earn their keep when the text is long enough to fill both to near-equal depth AND the
  content is genuinely parallel/independent.** Otherwise they fragment the narrative, orphan a short right
  column into a lopsided sliver, and (on CJK) strand orphan characters via fragile column-balancing.

## Single headline stat + trend — number leads, chart supports  (Round 29 — A > B, 2–1)
- **When the payload is ONE headline stat, lead with the big number; make the chart small supporting proof**
  (a lone-accent final bar, full unabbreviated CJK, flow-anchored — **no absolute-positioned callout pill
  over live bar geometry**, per the absolute-positioning meta-rule). A dominant chart of near-identical bars
  becomes decoration the eye must decode before hunting for the takeaway, and it forces CJK truncation.
- **Number-led must still FILL top→bottom** — anchor the number at top and distribute the mini-chart +
  context with `.vspread` so it doesn't strand a mid-canvas stripe (the balance dissent).
- **Flip to a dominant chart only when the *shape of the trajectory* is itself the message** (≥6–8 real
  points, inflections worth tracing); then the stat rides as the accent. This unifies the chart/number
  family: **R1** keep-hero-close · **R8** give-the-chart-real-points · **R11** bars-when-ending-value-is-headline
  · **R16** big-number-for-punch · **R25** annotate-the-delta.

## Flat capability set — pill row for impact, checklist for safety  (Round 30 — B > A, 2–1)
- **For a flat set of ~6 *short* capabilities, default to a single full-width pill / tag row with 1–2 accented
  pills.** It reads as one scannable horizontal "capability bar," spans the canvas with balanced margins, and
  the accented pills create instant focal hierarchy.
- **Switch to a 2-column checkmark list only when CJK label lengths are unpredictable or export-safety is the
  binding constraint** (flow layout, overflow-proof) — and **even then, accent one item so the list doesn't
  read inert.** (Note: a 6-pill row still needs vertical fill — distribute it, don't float it as a lone
  mid-canvas line.)

## Pricing tiers — elevate the recommended card  (Round 31 — B > A, 2–1)
- **When one of several plan/option cards is recommended, elevate it** — accent fill, greater height, and
  **name the pick in the title** ("Pro 最適合成長團隊"). Equal cards force a flat scan and leave the call
  unstated; the elevated card both guides the eye and activates dead lower-center space. Use three equal
  cards only when you genuinely have no recommendation (a neutral feature comparison).
- **Realize the emphasis through robust in-flow styling (fill / height / weight), not a floating badge.**
  Round 31's "最受歡迎" badge shipped *broken* — white-on-white and clipped at the card's top edge. If you
  add a "most popular" badge, **give it its own non-reversing background and seat it INSIDE the card box** so
  it can never render invisibly or clip. (Concrete case of the absolute-positioning meta-rule.)

## Funnel — horizontal bars on a shared track, not a trapezoid  (Round 32 — B > A, 3–0 unanimous)
- **For an analytical conversion funnel, use horizontal diminishing bars on a shared baseline track**, each
  labelled with count **and step-conversion %**, labels in fixed outside gutters. The common baseline makes
  drop-off severity instantly comparable (付費 reads as a tiny stub vs a full 認知 bar), the % surface the
  "where's the biggest leak" thesis, and one solid accent holds (no tint ramp), filling the canvas edge-to-
  edge.
- **Reserve the centered trapezoid silhouette for an evocative, presentation-mode "funnel" feel** for a
  non-analytical audience where exact comparison and per-step rates don't matter. The trapezoid dilutes the
  accent into a tint ramp, crowds text inside shrinking bands, and strands a lopsided right margin.

## Trade-offs (pros/cons) — two-column split by default  (Round 33 — A > B, 2–1)
- **Default to a two-column 優點 | 風險 split** (accent vs muted). The spatial left/right divide lets a
  UX/product audience grasp the balance in one saccade and is structurally robust with plain bullet lists.
- **Switch to an interleaved tagged list only when the pro/con counts are uneven** (an unbalanced split
  strands one short column with dead canvas) **or when each item needs a full sentence** — then the list
  fills evenly, but **size the CJK tag chips generously (fixed width)** so labels never clip or misalign and
  flatten the contrast.

## Dense table — hairline rows by default, zebra only when long  (Round 34 — B > A, 2–1)
- **For a small dense table (≈5 rows), use hairline rows** (thin bottom rules, no fills). Less ink lets the
  one accent figure (the `+24%` the title calls out) and the bold row labels pop, keeps strict color
  discipline, and is export-robust (full-width row fills can band/clip near the slide margin).
- **Reach for zebra striping only at higher row counts (≈≥8–10)** where the eye loses its place across wide
  rows, OR when the table must single-handedly carry the lower canvas (its fills add mass). Below that, zebra
  is decoration. **Fix a floating thin-stripe table with `.vspread` / surrounding content, not by painting
  rows** (the fill rule again).

## Closing / thank-you slide — minimal centered by default  (Round 35 — A > B, 3–0 unanimous)
- **Default to a big centered 謝謝 + one subtitle line** — zero overflow/wrap/clip risk, renders identically
  under export, and the intentional symmetric whitespace is the legitimate statement-slide breathing (R7).
- **Add a left-aligned contact block only when the closer must hand off a concrete next step** (Owner /
  Email / Next). **Never trust a fixed-width 3-column row of email/name values to survive export** — long
  fields overflow or wrap; if you must, let it wrap/flow rather than locking column widths.

## Cross-round meta-rule — emphasis & labels must be built from robust in-flow layout  (Rounds 31, 32, 35; extends the absolute-positioning rule)
A repeated failure mode across these rounds: **decoration that carries meaning but is built fragile.** The
white-on-white/clipped "most popular" badge (R31), text crammed *inside* shrinking funnel bands (R32), and a
fixed-width contact row that overflows (R35) all lost the brand-code lens. The rule: **encode emphasis and
labels with in-flow structure — card fill/height/weight, outside-the-shape label gutters, wrapping/flowing
text — never with a floating badge, a reversed-out fill that can vanish, a fixed-width column that can
overflow, or text trapped in a resizing container.** When a highlight *must* float, give it a self-contained
non-reversing background and re-screenshot to confirm it neither clips nor disappears.

## Headline accent dosage — pinpoint the one keyword  (Round 36 — A > B, 2–1)
- **Accent only the single load-bearing keyword in a headline**, not the whole clause. One tight pinpoint
  gives the eye one place to land and maximizes recall; flooding the trailing phrase (incl. connective verbs
  like 花在) dilutes the highlight into a colored run and softens the punch on the word that matters. Upholds
  the accent-as-precise-highlight discipline.
- **Widen to the whole phrase only when no single word dominates, or when a centered headline reads lopsided**
  and needs the colored mass to counterweight a long dark run (balance, not focus, is then the failure mode).

## Content-slide header — left-align to the body grid  (Round 37 — A > B, 3–0 unanimous)
- **Align the eyebrow + headline to the LEFT edge of the body grid** (top-left header). Sharing the grid
  origin with the card row gives one continuous scan line, a single focal anchor, and a robust home for a
  variable-length bilingual headline — with zero centering math to break.
- **Reserve a centered header only for bodies that are themselves centered/symmetric** (a single hero
  statement, a centered logo wall, an odd card count visually centered). Centering a header over a left-
  anchored grid strands empty flanks and splits the anchor.

## 6 feature cards — icon-left rows for one-liners, tall cards only for real depth  (Round 38 — B > A, 3–0)
- **For ~6 cards holding one-line captions, use icon-left rows (2 cols × 3 rows).** It binds icon + title +
  caption into one compact horizontal reading unit, gives bilingual captions horizontal room, and forms a
  strong left-edge scan rail.
- **Reach for icon-on-top tall cards (3 × 2) only when each card carries real vertical content** — a
  multi-line body, a stat, or a sub-list — that genuinely fills the lower half and earns the height.
  Otherwise the icon strands mid-card above a hollow void. (Content-density-gates-the-form again.)

## Hero stat precision — round the headline, footnote the decimals  (Round 39 — A > B, 3–0 unanimous)
- **Round the big hero number to its most memorable shape** (−89% / 4.6 / +38%) and **push exact decimals
  into the gray subcaption** (約 48 分 → 5 分). Rounded reads as a single memorable shape, sits with even
  gutters, and survives export; precise decimals widen each token, crowd the dividers/margin, and dilute the
  punch — and nothing is lost because the fine print carries the nuance.
- **Use precise decimals only when the exact figure is itself the claim** — regulatory / scientific /
  financial reporting, A/B deltas where 38.2 vs 38 changes the decision, or audiences who'd distrust a round
  number as hand-waved.

## System diagram — orientation follows the message  (Round 40 — mixed, A 1 / B 2)
- **Directional pipeline (a journey, "from X to Y") → horizontal boxes-and-arrows.** Arrows make the flow
  explicit and ride left-to-right reading. **Size the container tight to the row** — a flow dumped into a
  tall card leaves a cavernous hollow band (the balance trap that cost A here).
- **Layered stack (tiers where altitude itself is the meaning, no temporal flow) → vertical full-width
  bands**, ordered **top→bottom in narrative order** (never reversed — putting the source at the bottom
  silently reverses the story). Bands fill the canvas evenly and wrap descriptions in their own column with
  no equal-width tiles to misalign on export.

## Cross-round meta-rule — size the container to its content  (Rounds 38, 40; cf. 9, 14, 24)
The single most repeated balance failure across the loop: **a container (tall card, big diagram panel, hero
mockup/portrait) sized larger than the content it holds reads as a hollow void or an unfinished asset, not as
breathing room.** Fixes, in order of preference: (1) shrink the container to its content (icon-left rows vs
tall cards R38; tight flow row vs cavernous card R40); (2) add real content to earn the height (multi-line
body, stat, sub-list); (3) distribute with `.vspread` so sub-blocks span top→bottom. This is the disciplined
inverse of the statement-slide whitespace exception (R7): emptiness only reads as composed when it is
intentional and symmetric — never when a box was drawn bigger than its contents.

## Comparison-table row emphasis — tint the row when sparse, ink it when dense  (Round 41 — A > B, 2–1)
- **Tint the whole recommended row** (an `--accent-soft` band, rounded ends, accent label + key cells) **when
  the table is short and the canvas is sparse** — the band registers preattentively as one "found-it" object
  *and* gives the small table real visual mass / a center of gravity.
- **Drop the fill for a 建議 pill tag + accent key cells on hairline rows when the table is long/dense
  (≈≥8 rows), sits among other content, or export-robustness / strict one-accent discipline binds.** (Row
  twin of R34 dense-table hairlines and R31 elevate-the-card.)

## Step numbering — plain numerals by default, badges for left-column mass  (Round 42 — B > A, 2–1)
- **Use large plain accent numerals by default.** Stronger size-contrast hierarchy reads as sequence faster,
  tinting only the type honors one-accent restraint, and there's zero export risk (no fixed-diameter badge or
  absolutely-centered numeral to clip/distort).
- **Reach for filled accent circle badges only when rows are sparse and left-heavy** — a short title over a
  tall empty band leaves the left column void, and the solid disc supplies anchoring mass.

## Timeline — vertical rail by default, horizontal only for a wide stage  (Round 43 — B > A, 2–1; confirms R5)
- **Default to a vertical rail.** It double-codes the current phase with an accent label (far louder than a
  hollow ring that a solid "done" dot out-shouts), and left-aligned rows give labels unlimited horizontal
  room (nothing wraps/collides on export).
- **Use a horizontal milestone line only when the canvas is genuinely wide, quarter labels are short, AND
  full-bleed fill is the priority** — its sole edge is even left-to-right fill; otherwise it strands a thin
  mid-canvas stripe (R5's horizontal-cascade failure).

## Icon container — soft same-hue chip for sparse cards, bare glyph for dense  (Round 44 — A > B, 2–1; refines R15)
- **Wrap each icon in a soft rounded chip that is a low-opacity tint of the *same* accent** (chip = tint,
  glyph = full saturation). It anchors the glyph, fills cavernous cards, keeps the single-hue ramp intact, and
  the fixed flex-centered box survives export without baseline drift.
- **Drop the chip for a larger bare glyph only when cards are content-dense and impact beats containment.**
  Keep the glyph fully saturated either way so the chip never dilutes it.

## Categorization color — flat accent for peers, tint ramp only for ranked  (Round 45 — A 2 / B 1; sharpens the 4-color rule)
- **For 3+ *peer* categories, use neutral cards + one flat accent reused identically** (accent top-border +
  accent index numeral) and **lean on numerals, not color, for any sequence.** This is the strict, export-safe,
  on-brand default.
- **Use an accent-TINT ramp (one hue, descending shades) ONLY when the categories carry an inherent priority
  order AND your accent is dark enough that even the lightest shade keeps legible header-text contrast.** A
  ramp reads as several colored masses — great for ranked grouping, but a strict reader sees several colors,
  the palest tint risks white-on-light contrast failure, and full-bleed bands must clip to rounded corners.
  *A single-hue tint ramp is the only sanctioned widening of the one-accent rule, and only for ranking.*

## Cross-round meta-rule — emphasis-by-fill vs emphasis-by-ink  (Rounds 41, 42, 44, 45; cf. 26, 31, 34)
The loop converged hard on one principle for highlighting: **a chromatic fill (row band, circle badge, icon
chip, tinted header) earns its keep mainly when it ALSO solves fill — supplying mass to a sparse card/table —
or encodes a genuine ranking. When the canvas is already full, or strict one-accent discipline / headless-
export robustness is the binding constraint, prefer emphasis-by-ink: accent the *type* (label, numeral, key
cell), reuse one flat accent, and let numerals carry sequence.** Default to ink; reach for fill when the
composition needs the weight or the data is ranked. (This is the highlight-level companion to the
size-the-container-to-its-content rule: don't paint a surface to do a job that structure or ink already does.)

## Two-series comparison — lines for a crossover, grouped bars for exact values  (Round 46 — mixed, B 2 / A 1)
- **When the message is one series *overtaking* another, use two overlaid lines** — the flip renders as a
  single literal X read in under a second, and accent-stroke-vs-grey-hairline is the most on-brand minimal-ink
  expression.
- **Reserve grouped bars for reading exact per-month values, series that never actually cross, or when you
  need the baseline-anchored bars to fill the frame** (two thin lines float in a mid-canvas band — distribute
  with `.vspread`).

## Single stat vs benchmark — big number + gap pill, not two bars  (Round 47 — B > A, 2–1)
- **For one headline stat against a benchmark, lead with the oversized number centered and state the gap
  explicitly in a small benchmark pill** ("業界平均 41% ▲ +32pt"). One figure is an instant focal point and
  the "+32pt" means the "near-double" claim is *read*, not estimated from bar heights.
- **Reserve side-by-side bars for when the visual ratio itself is the message, or when comparing 3+ values.**
  (If the hero glyph + multi-token pill risks export fragility, shorten the pill / test glyph sizing rather
  than defaulting to bars.)

## In-body emphasis — bold ink for many, accent for the one  (Round 48 — mixed, A 2 / B 1; ties to R36)
- **Neither blanket treatment is right.** Accenting *multiple* phrases in a paragraph scatters the highlight
  into 4+ chromatic fragments and breaks the "accent is a scarce precise highlight" discipline.
- **Carry multi-phrase emphasis with bold ink; reserve accent color for the ONE load-bearing phrase per body
  block** (the single payoff, e.g. 減少近九成), demoting supporting phrases to bold ink. This is R36's
  headline rule extended to body copy.

## List marker — numerals for counted takeaways, checks only for completion  (Round 49 — B > A, 2–tie–1)
- **When the title counts or sequences the items ("三個重點", "key takeaways"), lead each with a bold accent
  numeral (01/02/03) as live text.** It echoes the count, gives an ordinal scan path, stays emphasis-by-ink,
  and exports cleanly.
- **Reserve check icons for content genuinely about completion / confirmation / requirements-met** — a
  check-disc on neutral takeaways reads as a generic done-list and adds a fragile SVG glyph for no semantic
  gain. (Balance is unaffected — the marker lives inside the card — so decide purely on meaning.)

## Section-divider progress indicator — omit by default  (Round 50 — B > A, 2–1)
- **The numeric index ("02 / 05") already encodes deck position, so omit the progress-dot row by default.**
  A 5-dot row is redundant *and* spends the accent a second time, creating a blue cluster that competes with
  the two-tone hero keyword and dilutes the single focal path; it's also a more fragile 5-child flex row vs.
  three centered text lines.
- **Add a progress indicator only for long, wayfinding-heavy decks** (training / reference) — and then
  **render the active dot in ink, not accent**, so it doesn't duplicate the accent already on the index +
  keyword. (Don't encode the same thing — deck position — twice in the same color.)

<!-- next rounds append here -->

## Product / feature showcase — anchor the hero, fill the frame, annotate to teach  (self-review vs reference decks)
Comparing a built "how to use Claude Code" slide against the reference showcases (idx 24/26) surfaced four
fixes — a floating bare mockup opposite an empty column read under-filled and lopsided:
- **Anchor the hero mockup — never float it bare in a void.** A *hero* screenshot/mockup sits on a soft
  backdrop (an `--accent-soft` / `--surface` rounded **stage**, or a circle/panel behind it) or near-bleeds,
  so the opposite side isn't an empty column. (Floating-with-soft-shadow stays for **secondary / inline**
  images; the hero earns a stage. Refines `imagery.md`.)
- **Fill the frame with balanced zones.** References span content edge-to-edge (e.g. left list · center
  hero · right stats). Match the supporting column's vertical extent to the hero's — don't strand a short
  centered list beside a tall mockup.
- **Give the headline a sub-line** on a showcase / section slide, so the top mass has weight (a lone
  headline over a big gap reads thin).
- **To explain a UI ("how to use" / onboarding), annotate it — this is the DEFAULT.** Numbered callout
  pins (`.anno-pin` / a `.callp` card) placed ON the relevant UI regions teach faster than a detached step
  list — the reference annotated-UI technique (idx 21/26/32). *(Confirmed by an A/B pick: the annotated-hero
  version beat steps-beside-hero for a "how to use Claude Code" slide.)* Reserve a detached step list only
  when the steps aren't tied to one screen. **Place pins in the stage margin / empty regions, clear of any
  UI text they'd obscure, and re-screenshot to confirm no occlusion.**

<!-- next rounds append here -->

## Capability / exception rules (from the 38-slide reference audit — layout only)
The audit (2 FULL / 36 PARTIAL / 0 NONE) added the v12 primitives in `base.css` + `_catalog.md`. It also
surfaced four **exceptions** to standing rules — each narrow, intentional, and re-screenshot-gated:
- **One sanctioned off-canvas / overlapping hero-or-decor illustration.** `imagery.md` + layout-balance say
  illustrations sit on a surface, on-grid. *Exception:* a single recolored hero illustration (or an ambient
  `.decor-layer` of rotated props) **may overlap content and bleed off-canvas** when it's clearly decorative
  and the content stays legible above it (`.above`). Still one illustration style; still real assets for
  product imagery. *(refs 3, 11, 13, 24, 36)*
- **Quote bubbles need not be uniform in a collage/cascade.** The testimonial rule "same size in a row" holds
  for tidy rows, but `.qcascade` / `.collage` voice-of-customer scatters **may vary bubble size, offset, and
  tail direction** — the controlled irregularity is the point. *(refs 7, 35)*
- **A composite "flow-region + section-reveal" may share one frame.** One-claim-per-slide normally splits
  these, but a problem→synthesis→reveal sequence (e.g. pain points converging into a solution hero) **may
  live on one taller frame** when the convergence *is* the narrative. *(ref 9)*
- **Anchor-top with intentional bottom whitespace is allowed** (reuse `.slide.top`) — overriding the fill
  rule — when a dense table/chart genuinely ends mid-canvas and stretching it would distort the data. Prefer
  `.vspread` first; fall back to anchor-top only when distribution would lie about the data. *(ref 34)*

These exceptions never loosen the **core**: one accent, plain-language bilingual (繁中+English, never Korean
even when a reference is Korean — learn the *structure* only), subtle shadows, and the principles digest above.
