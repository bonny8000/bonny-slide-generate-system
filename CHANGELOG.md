# Changelog — Bonny Slide System

Version history for the skill. The agent does **not** need this at build time; it lives here so
`SKILL.md` stays a working operating manual. Current version is in `SKILL.md` frontmatter.

## v12.15 — the gate cannot learn taste, so it learns to remember; and builds read 58% less
Acting on the four-step plan, with one step abandoned on evidence.

- **Abandoned: more pixel metrics.** Nine geometric measures were scored against the 37 labelled A/B
  pairs — coverage, interior gap, text gap, band ratio, margin ratio, quadrant spread, ink ratio and
  fill-vs-ink share. **None separated a preferred slide from a rejected one**; the best was 60% on
  n=20, which is noise. The plan had been to add a per-surface hollowness check. The measurement says
  the differences a person decides on are not geometric, so that check would have added cost and
  complexity for nothing.
- **Static features carry the signal instead.** The same test over markup and CSS found `accent_ink`
  — accent carried on *type* rather than a filled surface — agreeing with the user on 14 of 19 rounds
  (74%). That is the empirical form of principle 7, **emphasis-by-ink > emphasis-by-fill**. Round 34
  is the worked case: the rejected variant striped its table with
  `tr:nth-child(odd){background:var(--surface)}`, the chosen one used `border-bottom`. Identical
  geometry, identical gate score, opposite verdicts.
- **New `scripts/check_style_rules.py`** reads the stylesheet, not the pixels, and flags zebra fill,
  accent carried by fill rather than ink, and accent spread across too many regions. It separates R34
  correctly and raises **zero notes across all 41 shipped examples**, so it is precise rather than
  noisy. **Advisory only** — 74% confidence would be wrong once in four, and the slide's intent can
  overrule any of it.
- **New `scripts/check_antipatterns.py` + `specs/gate-antipatterns/`.** Two frozen slides that must
  keep failing, including the layout that went FAIL → pass at 34% whitespace. A gate can only be made
  so clever; it can be made to remember. Now a blocker in `audit.md`, alongside a check that
  `calibrate_gate.py` was run and did not get worse.
- **`self-critique.md` gains the six named render questions** the gate provably cannot answer, in the
  order the failures actually occurred.
- **Builds read 58% less.** The read-before-building set was 170 KB, most of it inapplicable to the
  slide in hand. The seven core foundations are now named (~25 KB) and the other seven are behind
  explicit triggers — `layout-choice` only when the router leaves two candidates, `learn-from-image`
  never during a build. Taste comes from a compiled
  `specs/generated-preferences-digest.md` (3.6 KB) rather than the 51 KB `preferences.md`, generated
  so the two cannot drift. **170 KB → 71 KB.**

## v12.17 — a panel title that reads as one, and numbers that stop implying rank
- **New `.panel-title` role.** A title above a list sat at 16px against 15px body — bold, but not
  senior, so the group had no head. This is the role between `.eyebrow` and `.headline`.
- **A numbered badge is a claim about order.** `1 2 3` says first, second, third. Used on peers —
  three features, three reasons, three supporting facts — it invents a hierarchy the content does not
  have, and the reader spends a moment working out why item 1 outranks item 3 before finding there is
  no answer. `foundations/iconography.md` now draws the line: numbers for a sequence, a ranking, or a
  count the audience refers back to; **an icon for peers**, since it costs the same space and carries
  meaning rather than rank. New `.rankrow .ic` marker alongside the existing `.rn`.
  The icon has to say something about its own item — three copies of one generic dot are a bullet
  with extra steps.
- **Distribute, don't inflate.** Making the supporting list span the table's height by stretching each
  row gave one line of text a 275px container — the hollow-container failure, reintroduced while
  fixing an alignment one. The rows stay compact and the list distributes them instead.
- Both rules are in `audit.md`. Verified by rendering at full size, not by the gate.

## v12.16 — paired panels match; a neutralisation revert had been shrinking a table
Design review of two A/B bases turned up three real defects, one of them a bug of mine.

- **`neutralise()` had stripped `width:100%` from a comparison table.** The sync reverts every
  property a shipped rule declares that a slide rule does not, so `.ctable{font-size:17px}` also
  reverted `width` and `border-collapse` — the table collapsed to content width and read as a huge
  gap in the middle of the slide. Refinement and collision are indistinguishable from inside the
  sync, so this is documented with the way around it rather than patched with a heuristic: **to
  refine a shared component from a slide, use a selector `base.css` does not own** —
  `.ranklist>.rankrow` rather than `.rankrow`, which has nothing to collide with.
- **Paired panels are now the same size and aligned**, whatever they contain. `.vp` laid each column
  out independently, so the two grey rectangles ended at different heights — an accident, not a
  decision. The row stretches, the description is held to two lines so both panels start level, and
  the panel takes the leftover height so they end level. Item count stops deciding geometry.
- **One alignment axis inside a panel.** A centred heading over left-aligned chips gave the two no
  common axis, so the panel's margins stopped looking equal even though the padding was symmetric.
  Everything left-aligns now, which also lands a wrapped orphan chip under the first one instead of
  floating it mid-row.
- **Paired columns run the same length** — the supporting list beside the comparison table now
  stretches to match it instead of leaving a short column beside a long one.
- All three rules recorded in `foundations/layout-balance.md`. Balance gate **7 → 5** as a
  side effect, and R54 was re-posed: its first form was withdrawn because the variants were barely
  different, the CSS having landed on the list while the table itself was broken. A round run on a
  broken base measures the breakage, not the axis.

## v12.14 — measure whether the gate has taste, using the A/B rounds as labelled data
Every other check measures the gate against itself: it passes when its own thresholds are satisfied.
That says nothing about whether a passing slide is good, which is why three changes have now passed
every gate while looking worse.

- **New `scripts/calibrate_gate.py`.** `preferences.md` records each A/B round's winner and both
  variants are on disk, so 37 pairs are **human-labelled**. Run the gate on both, see which it
  prefers, compare with the person who chose.
- **First measurement: the gate had no opinion on 20 of 37 pairs** — identical scores, so it cannot
  distinguish a preferred slide from a rejected one at all. Of the 17 it did rank it agreed 7 and
  disagreed 10, or 41%. The ties are the headline; 17 decided pairs is far too small to claim 41% is
  meaningfully worse than a coin flip, and the honest reading is that the gate carries **no useful
  taste signal today** rather than an inverted one.
- This is now the number to move. Any change to the gate should be scored here before it is believed,
  and it is the first metric in the system that measures the checker rather than the work.

## v12.13 — compose starved slides as a centred group; 15 balance failures → 7
The user's read of a failing render turned out to be the fix the previous session had given up on.

- **The footer was being measured as content.** `.foot` is pinned 42px off the canvas bottom on every
  slide, and the gate measured the content extent down to it. That made the bottom margin ~20px
  everywhere and charged every slide for the gap above its own page furniture — a slide whose content
  ended at 70% height was reported as a 25% dead band it could only "fix" by stretching something into
  the footer's lap. `trim_page_chrome()` now excludes a thin run pinned to the canvas bottom before
  measuring both the interior gap and the top/bottom balance, recognised structurally (≤2 cell-rows,
  bottom 12%, separated) because the gate works from pixels and cannot read class names.
- **The composition rule, and it came from looking at the render.** Pinning the header to the top and
  letting the body row `.grow` into the leftover space opens *two* holes — one under the header, one
  above the footer — and the eye reads two fragments instead of one statement. Bringing the header
  down against its content so they read as a single block, and letting the leftover become even margin,
  fixes both at once. Applied across the library: **15 failures → 7.** `feature-grid`,
  `idea-evidence`, `interview-affinity`, `keyword-cards`, `linked-circles`, `metric-cards`,
  `product-hero` and `service-flow` are now balanced compositions rather than starved ones, each
  verified by rendering it.
- `.grow` is for content that genuinely has the mass to fill the body. It is not a way to make a short
  slide look tall — that is now written into `foundations/layout-balance.md` alongside the four
  reverted attempts that prove it.
- **README rewritten** for the two-axis router, multilingual triggers, the tie-break order, the
  routing gate and its held-out score, and an honest note that three separate changes have now passed
  every gate while looking worse.

## v12.12.2 — the gate stops measuring a deck viewer as a slide
- **`deck-demo-scroll.html` was never a slide.** It holds eight `.frame`/`.slide` elements — a
  scroll-through viewer. Rendering it at 1920×1080 measured a wall of frames and reported "太擠, 100%
  coverage": a real number about the wrong object. `validate_layout.py` now detects a page with more
  than one slide and skips it, saying why. The slides inside are gated individually, where the answer
  means something. **16 failures → 15.**
- **Four attempted fixes for the remaining 15, all reverted, all recorded in
  `foundations/layout-balance.md`.** Growing every figure primitive changed 162 renders and fixed
  zero slides. Stretching a grown row's cards moved the dead band inside the cards. Distributing a
  stretched card's content *passed the gate* and looked clearly worse — content flung to the card's
  extremes. Re-anchoring turned one failure into three.
- The conclusion is worth more than the fixes would have been: **a slide short on content cannot be
  fixed by geometry** — every lever only moves where the emptiness sits. The remaining 15 need
  material that earns the space, a cut, or an explicit sparse classification. That is a content
  decision, not a CSS one.

## v12.12.1 — phone mocks measured in iOS points; a sync bug that reverted base.css
Three fixes from user review, one of which was quietly undoing every stylesheet change.

- **`sync_examples.py` was promoting stale shipped rules back into the slide block.** It read
  *every* `<style>` block as "the slide's existing CSS", including the previous `data-shipped` block.
  So on any `base.css` change, last build's shipped rules differed from this build's, `slide_specific`
  read them as deliberate differences, and promoted them into the slide block — where, being second
  and unlayered, they **overrode the very improvement just made**. It resurrected the old
  `.phone .notch` over the new one, and would have silently reverted every future `base.css` fix
  across all 162 examples. Now only non-shipped blocks count. 26 already-promoted rules removed.
- **A phone mock is a scaled device, so its interior is now measured in points.** `--uis` is one iOS
  point at that mock's size (`width / 390`), so Apple specs convert straight across: frame 390×844,
  nav bar 44pt over a 59pt status inset, dynamic island 125×36pt, switch 51×31pt, list row 44pt, body
  17pt. Absolute px inside a phone is what made the old mock look wrong at a glance and hard to name:
  shrink the frame to fit a slide and the type does not shrink with it, so proportions stop reading as
  a real screen even though each element looks fine on its own.
- **Dynamic island, not a notch** — a floating pill inset 11pt from the top, and the app bar reserves
  the status inset so it can never land on a title. The old notch dated a mockup instantly.
- **A UI text scale, separate from slide type.** `--fs-ui-1..5` (11/12/13/14/16px) paired with
  `--lh-ui-1..5`, plus `--fw-regular/medium/bold`; size and line-height travel together and weight
  stays independent. Slide type runs 14–150px because it is read across a room; text inside a mock
  screen is read as an *image* of an interface. `fontWeight` is now an allowed token type.
  `.appframe` / `.mock` use the absolute scale at 1:1; `.phone` scales it by the device ratio.

## v12.12 — app-screen anatomy for ui-mockup, and a bilingual expansion rule
Surveyed an external mobile design system for ideas worth having. Took two, declined a third; nothing
is ported, everything is built from this system's own tokens.

- **App-screen furniture for `ui-mockup`.** A census of what a real mobile screen actually contains,
  against a system that had only `.phone` / `.appframe` / `.listrow` / `.mock`. `base.css` gains `.appbar`, `.tabbar`, `.segbar`, `.sheet`, `.banner` (+`warn`/`neg`/`pos`),
  `.fab` and `.badge` — 8 primitives, all token-driven, zero raw hex. A schematic screen reads as a
  real app when its **chrome** is right, not when its content is detailed, so the rule stays: label
  the app bar and the tabs, skeleton bars everywhere else, never invent rows of plausible data.
- **Three new `ui-mockup` variants** — `list-screen`, `tab-screen`, `sheet-screen` — with a
  render-validated example, `examples/light-app-screen-mockup.html`. Built, screenshotted, looked at,
  and revised three times: captions were running as one cramped line, and two of the three screens
  emptied out below the fold, which no check would have caught.
- **Bilingual pairs expand, and now `typography.md` says by how much** (source: W3C). 繁中 is the most compact
  writing this system produces and English among the least, so a ≤10-character 繁中 line pairs with
  English running **150–250%** wider. That is the worst case and it is also the most common one — a
  four-character headline with an English subtitle. The failure arrives late: the English wraps, the
  card grows, the row loses alignment, and the layout gate reports an imbalance whose real cause was a
  translation written three steps earlier. Size the container for the English, not the 繁中.
- **Declined: semantic spacing tokens** — naming spacing by relationship (`global-gutter`,
  `nav-to-title`, `component-default`) rather than by size. It is the better idea in the abstract, but
  this system already has a working scale plus `--gutter`, and renaming it would churn every example
  and the visual baseline to fix a problem nothing has measured. Recorded here so it is a decision
  rather than an oversight.
- Also: `ui-mockup` gains 繁中 and Korean triggers, now that triggers are multilingual.

## v12.11.1 — a schematic mockup is not a screenshot; alternates stop being guessed
Two corrections to v12.11, both from user review, both cases of a distinction I had collapsed.

- **`ui-mockup` split from `ui-screen`.** v12.11 tagged `as-is-to-be`, `feature-showcase` and
  `product-hero` as needing a real screenshot and disqualified them when the user had none. That was
  wrong: the system already ships schematic UI primitives — `.phone`, `.mock`, `.appframe`, `.sk`
  skeleton bars — and a `components/ui-mockup.md` spec whose rule is *skeleton bars, never invented
  data*. A schematic screen costs nothing, always matches the theme because it is drawn from tokens,
  and is exactly what makes an as-is/to-be vivid. New policy `build`: draw it, never ask for it,
  never drop a layout for lacking one. `must-supply` now applies only to the `ui-qa` route, where the
  claim really is about the actual product UI. Three layouts moved from blocked to buildable.
- **`alternates` are hand-declared now.** Deriving them from a shared `arrangement` produced
  substitutes that were structurally similar and semantically absurd — `keyword-cards` offered as a
  stand-in for `use-case-cards` because both are grids of a few cards, when one states design
  principles and the other shows who the product serves. Laying a page out the same way does not make
  two layouts interchangeable. 12 of 25 now declare a real substitute (`as-is-to-be` ↔
  `problem-solution`, `qual-quant-split` ↔ `painpoint-evidence`, `use-case-cards` ↔ `persona-cards`);
  the other 13 are empty on purpose, and an empty list means go back to the user rather than force a
  layout that does a different job.
- `--check` now validates that every declared alternate is a real spec.

## v12.11 — a standard for choosing between candidates, and illustration as a routed decision
Two follow-ons from the shape axis. Both were only buildable once `material` existed as data.

- **New `specs/foundations/layout-choice.md`** — the ordered comparison method for when the router
  narrows to two or more, compiled into `selectionPolicy.tieBreak` in `router.json`:
  **availability → fit → variety → intent proximity.**
- **Fit outranks variety, deliberately.** Reaching for a fresh layout at the cost of a well-filled
  page is the more common mistake and the more visible one: the audience sees a thin slide
  immediately and never notices the layout also appeared four pages ago. Variety is a preference
  above a quality floor, not a rule that can override it. Fit is not taste either — a `few` content
  set stretched across a `many` layout is the same starvation `validate_layout.py` measures after the
  fact, so choosing for fit is how you stop fighting that gate.
- **Every layout now carries `assetNeed`, `assetPolicy` and `alternates`,** derived from `material`.
  18 of 25 need no asset, 3 auto-trigger illustration generation, 4 need a real screenshot.
- **Missing illustration is now a routed decision, not a judgement call.** A layout with
  `assetPolicy: generate` and no supplied artwork is itself a `gate: yes` trigger, recorded as
  `material:illustration`. Silently swapping to a text-only layout to dodge generation is called out
  as what it is — turning a routing decision into a visual compromise. Covers, section covers,
  bridges, agenda and closing pages stay `gate: no` with reason `structural-page`.
- **A ui-screen may never be generated, and that is now enforced by the routing itself.** Material
  `ui-screen` compiles to `assetPolicy: must-supply`, which the tie-break treats as a hard
  disqualification rather than a preference — a fabricated screenshot of a real product is a false
  record of it. `alternates` gives the fallback: no screenshots turns `as-is-to-be` into
  `problem-solution`, both `opposed`. `product-hero` and `editorial-explainer-stage` have no
  alternate, so they force a question to the user instead of a substitution.
- `audit.md` gains four checks, two of them blockers: no generated stand-in for a required
  screenshot, and no silent swap away from a generate-policy layout.

## v12.10 — routing gets a second axis, and the Korean ban comes off
The user's reframe: intention is language-independent, so neither the input language nor the router's
own language should change which layout a page needs. Both changes follow from that.

- **The Hangul trigger ban is lifted, and the deleted Korean vocabulary is restored.** v12.9 rejected
  Korean in triggers. That aimed at the right goal from the wrong layer — the real constraint is that
  decks must be *generated* in 繁中 + English, which `validate_layout.py` already enforces at render
  time against the declared output language. A trigger is internal routing vocabulary and is never
  rendered, so the ban protected nothing; it only deleted recognition ability learned from the Korean
  reference decks this library was trained on. Restored from `d036c34`. The length floor also treated
  Hangul as ASCII and rejected 연결 as "too short" — 2 characters of Han or Hangul is a whole word,
  and the rule now says so.
- **Layouts route on two axes.** New `material` / `arrangement` / `item_count` frontmatter on all 25,
  compiled into `router.json` and the generated index, and required by `--check`. The measurement
  that forced this: **intent lines alone identify only 13 of 25 layouts.** The collisions are real
  conceptual twins — `idea-evidence`/`painpoint-evidence` both back a claim with evidence and differ
  only in whether the material is a chart or participant quotes; `hero-radial`/`linked-circles` both
  arrange concepts, one as a centre with satellites and one as a continuum. **The shape triple alone
  identifies 24 of 25**, with `keyword-cards`/`terminology-cards` the single legitimate collision,
  separated by intent.
- **Shape had to be structured, not prose.** The first attempt wrote content shape as a sentence and
  made things *worse* — 13/25 down to 11/25 — because every shape sentence shares filler vocabulary
  ("one X and its Y") and fuzzy matching drowned in it. Discrete tags either match or they do not.
- **Held-out routing went 4/10 → 8/10**, with each shape derived from the request's own words rather
  than from the expected layout. The one remaining misroute is honest: "我們的客戶大致分成哪幾類"
  names no illustration, so it reads as `text-only` while `use-case-cards` wants `illustration`. The
  other is now reported as **narrowed but tied** rather than unresolved — shape cut it to exactly the
  two known twins. Unresolved cases are down to zero.
- **`SKILL.md` requires the normalised line before any lookup** — `意圖: … · 形狀: material /
  arrangement / count` — derived from the content actually in hand, never from the hoped-for layout.

## v12.9.2 — the router was blind to 繁中, and now there is a test that says so
The first measurement of whether intention routing actually *works*, rather than whether it is
structurally well-formed.
- **New `scripts/validate_routing.py`.** `compile --check` proved every layout was *reachable*; it
  never asked whether a request phrased the way a person phrases it lands on the right entry. This
  replays a fixture of realistic 繁中/English requests through the router and reports HIT / WRONG /
  MISS, where MISS means the table gave the agent nothing and it free-picks — the exact mechanism
  behind "it keeps choosing the same layout".
- **The cause, measured:** only **10 of 122 triggers contained any 繁中**, while 繁中 is the primary
  output language. **17 of 25 layouts had zero.** Those 17 were invisible to Chinese input, and the 8
  that were visible swallowed everything — `as-is-to-be` alone won three requests that belonged to
  other layouts, purely because 改版 was in its trigger list. First run: 9/30.
- **繁中 triggers added to all 17**, plus 8 thin ones rounded out. The working fixture now scores
  30/30 — but that number is over-fitted and is labelled as such.
- **The honest number is 4/10**, from `specs/routing-cases-heldout.md`, written afterwards without
  consulting any trigger list and never tuned against. Blind performance went from ~30% to ~40%. Real
  and worth having; nowhere near solved.
- **What the held-out failures teach, recorded in that file:** generic words become attractors.
  `persona-cards` won two unrelated requests because `使用者輪廓` puts 使用者 in the index, and 使用者
  appears in nearly every request this system will see — the same pathology as 改版. Triggers must be
  *distinctive*, not merely relevant. More triggers of the same kind will not close the gap.

## v12.9.1 — dead example CSS removed; a review tool that was reading the architecture wrong
Prompted by an outside review that reported "adoption is only partially consistent" across patterns.
The headline finding did not hold, but chasing it turned up a real defect underneath.
- **586 dead rules deleted from the examples** (1523 → 937, 39%). Examples were originally built by
  inlining a snapshot of `base.css`, so every rule the sheet has since improved survived in the slide
  block as a "deliberate difference" — including rules for components the slide does not contain.
  `light-metric-cards` carried `.ctable` and `.hbar .track` while holding neither a table nor a bar
  chart, at values `base.css` had already superseded. Inert to render, but these files exist to be
  read as reference, so they were teaching values the system no longer uses. `sync_examples.py` now
  drops a rule when none of its classes appear in the markup. Proven safe rather than argued safe:
  all 164 slides match the visual baseline exactly, and the layout gate is unchanged at 16 of 41.
- **`verify_rebuild.py` was calling a designed feature a failure.** It strips `<style data-slide>`
  and re-renders, which asked a fair question when examples inlined the whole sheet and had no slide
  block. After the sync every example carries one deliberately, so any gap now measures "this slide
  has per-slide CSS" — true by design. It now reports **local reliance** as a magnitude to read
  rather than a pass/fail verdict, and says so in its own docstring so the old reading is not
  restored.
- **The raw-hex "violations" in six examples are mostly legitimate**, and `audit.md` now records why,
  since this is the second review to flag them. `.appwin .sb{background:#1b1b20}` paints a mockup of
  a dark application sidebar inside a light slide — a token would repaint it to the slide's own
  background and destroy the depiction. `#fff` inside `color-mix()` is a blend operand. Exactly one
  literal was a real violation and is now `var(--accent)`. `base.css` remains at zero.
- **The three Claude-brand examples are deleted** (`claude-code-ccv1`, `ccv2`,
  `how-to-use-claude-code`, plus their `.png` siblings). Their warm palette — `#d97757`, `#ece6dd` —
  was never in the token set, so they were off-system reference that could only teach off-system
  colour. Removing them beats inventing a brand theme for three files. 164 examples → 161.
- Also recorded in `audit.md`: a slide value larger than the `base.css` value is often deliberate
  per-slide sizing, not staleness. Do not bulk-revert examples to base values.

## v12.9 — the router + the balance gate
Two structural fixes aimed at a long-standing failure: the system knew a great deal but could enforce
almost none of it, so layout quality degraded first under context pressure.
- **Intention routing became a lookup.** Every spec now carries `intent` + `triggers` frontmatter
  (backfilled into 14 that lacked it). `scripts/compile_system.py` compiles all of it into
  `system/router.json` + `specs/generated-router.md` — the complete, drift-proof index of every
  routable pattern. `content-map.md` stays the hand-written narrative layer.
- **Routing drift now fails the build.** `--check` rejects a stable layout with no `content-map.md`
  row, an orphan component, an unresolvable `depends_on`, a duplicate trigger, and **any Korean in a
  trigger**. This caught 5 layouts that had specs but were unreachable by the planner
  (`feature-grid`, `hero-radial`, `idea-evidence`, `interview-affinity`,
  `centered-question-evidence` — the last via an id mismatch with `content-map.md`), plus 7 specs
  whose routing triggers were still Korean and so could never match 繁中 input.
- **Layout balance became a gate, not advice.** New `scripts/validate_layout.py` renders a built slide
  and measures what the rules only described: whitespace ratio (不空不擠), quadrant mass balance,
  safe-area overflow, empty top/bottom bands, and hardcoded hex. Wired into `audit.md` and
  `self-critique.md` so it gates delivery the way the illustration validator already does.
- **Two more prose rules became checks.** `validate_layout.py` now fails on copy in an undeclared
  language (see below) and, with `--deck`, on the v12.7 anti-dryness rule: a deck of
  8+ slides carrying no genuine visual moment. It also fails on a band of surface holding no text —
  the relocated-emptiness failure, which matters because without it a slide can be "fixed" into
  passing the gate while getting visibly worse.
- **Training is now an explicit mode.** Saying "training" / 訓練, or sending reference slides to learn
  from, routes to the learning loop instead of the build loop — the two produce different artifacts and
  were previously distinguishable only by tone. A training run is unfinished until the pattern is
  actually routable: `intent` + `triggers` frontmatter, catalog and content-map rows, a validated
  example, and a passing `--check`.
- **Recipes became usage contracts, not codegen.** `system/class-manifest.json` +
  `specs/generated-class-coverage.md` record which CSS classes each pattern is built from. This
  surfaced the deepest issue found so far: **only 13 of 44 catalogued patterns can be built from
  `assets/base.css`** — the other 31 need classes that exist only inside their own example, so the
  agent has to reinvent them on every build. That is a direct cause of visual inconsistency even when
  intention routing is correct. `base.css` stays hand-written; measuring the gap is the point.
- **The consistency rule replaced the "no new content" constraint.** A slide may add an existing
  catalogued component to earn its height; what it may never add is new design vocabulary — a new
  class, an untokenised colour, a type size off the scale. Layout varies by intention, vocabulary
  never varies.
- **Examples became pure reference; implementation lives only in `base.css`.** Each example had
  carried its own hand-maintained copy of the stylesheet, and those copies drifted three separate
  times across versions — which matters more than ordinary drift, because the agent learns layout by
  imitating examples, so a stale one actively teaches a superseded rule. `scripts/sync_examples.py`
  now rewrites every example as a regenerated `<style data-shipped>` plus a small `<style data-slide>`
  for what is genuinely specific to that slide (1360 such rules across 164 files, ~8 each), and
  `--check` makes staleness a build error.

  Applying it exposed a defect the promotion work had introduced earlier in v12.9, and fixing it
  properly turned out to be one invariant rather than a rename of 29 colliding class names. Both
  style blocks are unlayered and the slide block comes second, so a slide rule already wins for every
  property it SETS; the leak is the properties it does not set. That is how the v12 flow primitive's
  bare `.track{display:flex;flex:1}` flattened a bar chart, and how feature-showcase's
  `.fs{align-items:start}` collapsed an unrelated A/B slide to content width. The sync now
  **auto-neutralises**: any property a colliding shipped rule declares and the slide rule does not is
  explicitly reverted. `.hbar .track` was also made self-sufficient in `base.css`, which is a real
  component fix independent of the sync.

  Measured after: 18 of 48 slides fail the layout gate, down from 23 — five fixed, none newly broken.
  Both regressions were found by rendering the slide and looking, not by any check.

- **Output language is declared, not hardcoded.** The "no Korean" check is replaced by a check that
  the copy uses no script the deck's declared language implies — default 繁中 + English, taken from
  `<html lang>`, overridable with `--lang`. A Japanese or Korean deck now passes when it is asked
  for, and an accidental leak still fails. Routing *triggers* keep the constraint for a different
  reason, now stated as such: they are matched against the plan's intention naming, so a trigger in
  a language the router does not read can never fire.
- **A starved content slide now points at the right two remedies.** Instead of only reporting low
  density, the gate says to re-open that page's illustration decision — a thin content page is
  usually an intention that was always visual and got routed to native cards, or a page that should
  be merged or cut. It deliberately does NOT auto-generate an image: filling a hole with artwork is
  decoration, and illustration is chosen by intention. `toc`, `agenda`, `context`, `thanks`,
  `appreciation` and `closing` joined the whitespace exception, alongside cover and statement.
- **`SKILL.md` slimmed.** The changelog moved here, reclaiming ~63% of the entry-point file for the
  operating procedure the agent actually needs.
- **The illustration gate can actually run.** `validate_generated_illustration.py` imported Pillow at
  module scope, so on any machine without it the v12.8 "no silent illustration bypass" rule was
  unenforceable — the gate crashed before checking anything. It now falls back to a stdlib PNG decoder
  and only requires Pillow for non-PNG assets.
- **Token discipline repaired in `base.css`.** Six hardcoded colours were replaced with tokens. Five
  were exact-equivalent to the existing `--on-accent`. The sixth, the page backdrop, was a fixed
  light grey that stayed light behind a **dark** deck; it is now a themed `--backdrop` token.

- **v12.7** — **Deck-level visual pacing** (learned from a real all-text governance deck): new
  anti-dryness rule in `layout-balance.md` — a deck of 8+ pages needs ≥1–2 genuine visual moments (real
  screenshot, logo-row, mockup, or generated explainer; icons/chips don't count), and when nothing trips a
  trigger, the planner elevates the best candidate page instead of shipping a document-like deck. Broadened
  `workflow-transform` triggers in `content-map.md` to cover tool-pipeline / role-handoff / governance-flow
  convergence (not just workshop viewpoints), while keeping data-precise pipelines native.
- **v12.8** — Made editorial illustration selection enforceable. Every deck now carries a per-slide
  `illustration-plan.json`; human/agent toolchains, conversational worked examples, workshop facilitation,
  and scattered-input transformations are hard candidates. Added `guided-dialogue`, a plan validator,
  generator-provenance checks, HTML placement checks, and an explicit fail-closed rule when image generation
  is unavailable. This prevents a renderer from quietly falling back to native cards after selecting imagery.
- **v12.6** — Added a reference-driven **editorial explainer image generator** learned from Img39–Img43.
  It selects among workshop agenda + Q&A, scattered-input workflow transformation, and real-UI + Q&A
  compositions while keeping one visual language. Every route requires a fresh built-in image-generation
  call, exact target ratio, full-block placement, preserved colour, native editable copy zones, prompt
  builder, and validator. References are never reused as outputs; CSS/SVG imitation is prohibited.
- **v12.5** — Added the hypertoken pilot without narrowing the library: canonical `system/tokens.json`,
  five reusable style fragments, three pilot recipes, strict schemas, and a deterministic compiler that
  generates layered low-specificity CSS, the PPTX token bridge, and an LLM-readable reference. Component
  selection remains intention-first; migration status has zero selection weight; all legacy components
  stay available. Added `--check` plus governance/audit rules against generated-file drift.
- **v12.4** — A/B pick confirmed: **annotated-screenshot (callout pins on the UI) is now the DEFAULT for
  how-to / onboarding slides** (beat steps-beside-hero). Added a `content-map.md` intention row "Teach how to
  use / onboard → `annotated-screenshot`" and strengthened the `preferences.md` showcase rule (default +
  place pins clear of UI text, re-screenshot). Final slide: `examples/claude-code-ccv2`.
- **v12.3** — **Showcase self-review** (built the Claude Code intro slide, compared it to reference decks
  idx 24/26). New `preferences.md` rule "Product/feature showcase — anchor the hero, fill the frame,
  annotate to teach": (1) a *hero* mockup must be **anchored on a soft stage/backdrop** (floating-with-shadow
  is only for secondary/inline images — refined in `imagery.md`); (2) fill the frame with balanced zones,
  match the supporting column to the hero's height; (3) give the headline a **sub-line**; (4) to explain a
  UI, **annotate it with callout pins** rather than a detached step list. Produced two render-validated
  versions (`examples/claude-code-ccv1` steps+anchored-hero, `ccv2` annotated-hero).
- **v12.2** — **Image-presentation rule** (learned + validated from the reference decks, per user): every
  screenshot / photo / UI-mockup gets **rounded corners + a subtle LIGHT shadow** — new `--shadow-img` token
  (soft two-layer lift, tight contact + gentle ambient; never dark/heavy) in both light & dark themes, a
  unified `base.css` rule (`.shot` wraps raw `<img>`; `.phone`/`.appframe`/`.ui-mockup`/`.mock*` carry it
  automatically), and reconciled `imagery.md` (a soft-shadowed image may now **float on the canvas** — the
  shadow seats it — instead of always needing a surface card). Render-validated against the attached
  reference look (`examples/case-study/_audit/AIMG`).
- **v12.1** — Copy & layout refinements per user: removed the "codes carry a plain label" rule from
  `plain-language.md`; enforced an **equal four-side margin** — `.slide` now uses uniform padding
  (`var(--pad-y)`, top=bottom=left=right) instead of 80×96, and `layout-balance.md` elevates the rule
  ("uniform content safe-area" + "allocate in balance inside that box"). Verified by render.
- **v12.0** — **Reference capability audit (38 real slides).** Audited whether the system can reproduce each
  reference's *layout* by intention (color out of scope): **2 FULL / 36 PARTIAL / 0 NONE** — the system built
  the bulk of every slide but hit one specific missing layout mechanic on most. Clustered the gaps into 13
  themes and added a **v12 primitive library** to `base.css` + `_catalog.md`: an export-safe SVG **leader/
  connector** layer (tether/elbow/curve/converge), **decor/bleed/hero-cutout** off-grid layer, **tbubble**
  tails + **anno-pin** + **collage/qcascade** scatter, bounded **panel/splitpanel/ab-panel/split-2**, **funnel-
  merge** + **tracks** column connectors, **barline** combo chart + chart-annot, horizontal **babars** before/
  after + **bubble-delta**, **phone/appframe/device-stack** mockups + listrow/toggle/popup, **cards.four/flat/
  stagger** + **qstack**, **dash-link/node--dotted/thread**, **splitbar/formula/needsrow**, **radialmap** dual-
  hub map, and flow **dead-state/toplabel**. Added 4 narrow **exception rules** to `preferences.md` (one off-
  canvas hero illustration; non-uniform collage bubbles; composite flow+reveal frame; anchor-top whitespace).
  **Render-validated** via 10 composite slides in `examples/case-study/_audit/` (caught + fixed a stale
  inlined-CSS head and a `--bg`→`--chip` token mismatch along the way). Net: the 36 PARTIAL intentions are now
  reproducible. Bilingual-only discipline held — Korean references taught *structure*, output stays 繁中+English.
- **v11.0** — **A/B taste loop complete: 50 rounds.** Final rules (`preferences.md` R46–50): two-series →
  **lines for a crossover**, grouped bars for exact values; single stat vs benchmark → **big number + gap
  pill**; in-body emphasis → **bold ink for many, accent for the one**; counted list → **numerals** (checks
  only for completion); section divider → **omit the progress indicator** by default. Added a **⭐ Principles
  digest** at the top of `preferences.md` distilling all 50 rounds into 12 transferable meta-principles
  (fill-the-canvas, size-container-to-content, content-density-gates-form, sequence-vs-parallel, match-form-
  to-intent, accent-scarcity, emphasis-by-ink, in-flow-emphasis, number-leads-chart-supports, real-assets-
  only, don't-double-encode, always-screenshot). The taste layer is now a navigable principles-first
  reference backed by 50 traceable, render-validated rounds.
- **v10.8** — A/B taste loop reached **45 rounds**. New taste rules (`preferences.md` R41–45): table row →
  **tint when sparse, ink when dense**; step numbering → **plain numerals** (badges only for left-column
  mass); timeline → **vertical rail** (horizontal only for a wide stage; confirms R5); icon → **soft same-hue
  chip** for sparse cards (bare glyph when dense); categorization → **flat accent for peers, tint ramp only
  for ranked** (the one sanctioned widening of the single-accent rule). Plus the **emphasis-by-fill vs
  emphasis-by-ink** meta-rule (R26·R31·R34·R41·R42·R44·R45): paint a surface only when it also supplies mass
  or encodes ranking — otherwise accent the type.
- **v10.7** — A/B taste loop reached **40 rounds**. New taste rules (`preferences.md` R36–40): headline accent
  → **pinpoint the one keyword**; content-slide header → **left-align to the body grid**; 6 cards → **icon-left
  rows** for one-liners (tall cards only for real depth); hero stats → **round the headline, footnote the
  decimals**; system diagram → **orientation follows the message** (horizontal flow for a pipeline, vertical
  bands for a stack, top→bottom in narrative order). Plus the **size-the-container-to-its-content** meta-rule
  consolidating the loop's most repeated balance failure (R9·R14·R24·R38·R40).
- **v10.6** — A/B taste loop reached **35 rounds**. New taste rules (`preferences.md` R31–35): pricing →
  **elevate the recommended card** (built in-flow, not a fragile badge); funnel → **horizontal bars on a
  shared track + step %** (trapezoid only for evocative mode); trade-offs → **two-column 優點|風險 split**;
  dense table → **hairline rows** by default, zebra only at ≈≥8–10 rows; closing → **minimal centered 謝謝**,
  contact block only to hand off a next step. Plus the **emphasis-must-be-in-flow** meta-rule (badges/labels
  built fragile — white-on-white, clipped, fixed-width overflow — fail; encode with structure) extending the
  absolute-positioning rule. R31's badge bug and R35's contact row are the concrete cautionary cases.
- **v10.5** — A/B taste loop reached **30 rounds**. New taste rules (`preferences.md` R26–30): co-equal KPI
  row → **open numbers on hairline dividers** by default, flat cards only to carry the lower canvas; before→
  after → **side-by-side on one eye-line** for a single hero metric, stacked only for lists; text-heavy prose
  → **one column, capped measure** (two columns only for parallel volume); single headline stat + trend →
  **number leads, chart supports** (no absolute pills, fill with `.vspread`); flat capability set → **pill
  row** for short curated labels, checklist for export-safety. R29 unified the chart/number family
  (R1·R8·R11·R16·R25) and re-confirmed the no-absolute-positioning + fill-the-canvas rules.
- **v10.4** — A/B taste loop reached **25 rounds**. New taste rules (`preferences.md` R21–25): title slide →
  **editorial-left** (full-height accent rule + two-line title + metadata footer) by default, centered only
  for a content-light cinematic hero; testimonial → portrait panel **only with a real photo** (else avatar +
  centered quote); single insight → **full-width callout band** by default, oversized inline only as a
  high-impact exception; single-feature → **size the element by meaning, not space** (mockup gets hero weight
  only when the screenshot is rich/legible); single KPI → **annotate the delta** (badge + sparkline +
  context) when movement matters. Plus the **real-assets-earn-dominant-space** meta-rule — the empirical
  *why* behind `imagery.md`'s ask-for-assets step: never promote a placeholder glyph/mock to focal weight.
- **v10.3** — A/B taste loop reached **20 rounds**. New taste rules (`preferences.md` R16–20): single
  proportion → **ring/donut gauge** for a composed slide, big typographic number only for a one-glance
  punchline; section dividers → **hero the 繁中 keyword, demote the number** to a small `NN / NN` index;
  problem framing → **annotated product mockup with numbered pins** when pain is spatial (else numbered
  cards); two-option compare → **criteria-as-rows table** for 3+ criteria, VS-cards only for a binary
  "pick a side"; short agenda → **2-column card grid** (+ full-width tinted lead) over a wide numbered list.
  Plus the **absolute-positioning-is-export-fragile** meta-rule (prefer grid/flow + transform-centering;
  re-screenshot any floated element) — reinforcing the modern-web-guidance review step.
- **v10.2** — A/B taste loop reached **15 rounds**; integrated **modern-web-guidance** as a per-slide
  code-quality review step (`self-critique.md`) and added `text-wrap: balance/pretty` to `base.css`. New
  taste rules (`preferences.md` R11–15): short single-series trend with a headline end-value → **bar with
  the final bar accent-highlighted + value on-chart** (line only when path-shape is the message);
  comparison cells → **icon check/cross, accent only on "yes"**, negatives stay muted even in a tinted
  winner column; closing/CTA → **recap 3 stats above the buttons** by default; persona → **one hero by
  default**, two only when contrasting AND each card is content-filled; step/feature icons → **filled glyph
  on a solid accent chip for focal rows**, line icons only for secondary rows. Plus the **content-density-
  gates-the-form** meta-rule (never stretch thin content to fill a container).
- **v10.1** — A/B taste loop reached **10 rounds**, now run via deterministic **Workflow** panels (3 judges
  → tally → synthesize). New taste rules in `preferences.md`: testimonial = quote-as-hero (+ the statement
  whitespace *exception* to the fill rule); dashboards = one lead metric + real multi-point hero chart
  (sparklines need ≥3–4 pts); benefit sets keep a disciplined icon layer; **theme matched to job** (dark =
  spotlight a single stat, light = dense reading). Plus the **sequence-vs-parallel** meta-rule.
- **v10.0** — **full library complete.** Specced + render-validated the last 7 `todo` patterns
  (qual-quant-split, idea-evidence, hero-radial, interview-affinity, feature-grid + stat-bar, feature-card).
  Catalog is now **62 stable / 0 draft / 0 todo** — every catalogued component & layout has a spec *and* a
  screenshot-validated example, with zero raw-hex drift.
- **v9.9** — **backlog cleared.** All 20 draft component/layout specs are now render-validated `stable` —
  built a self-contained example slide for each, screenshotted and checked every one (fixing floats /
  stretched-empty cards before promotion). Also repaired 8 pre-existing stale `example:` refs. Now: every
  spec resolves to a real example, **0 drafts, 0 raw-hex drift**; 7 `todo` patterns remain catalogued
  (awaiting a source slide). Catalog: 55 stable / 7 todo.
- **v9.8** — A/B rounds 2–3 (self-judged panels). Process slides favor a clean **vertical list** over tall
  horizontal step-cards (which top-load + leave empty card-bottoms). Research findings favor **inline
  numbers for a 2-value contrast** over a 2-bar chart, **quotes as wide breathing cards**, and accent kept
  as a precise highlight (not a big filled block). Corrected the fill rule: `.grow` fills the body *region*
  but its content must **distribute** too — added **`.vspread`** (fill + space-between) so a short block
  doesn't float with empty top/bottom. `preferences.md` updated each round.
- **v9.7** — started the **A/B preference loop** (subagent writes a requirement → build 2 variants →
  user picks → fold the winner's lesson back in). Round 1 added `specs/preferences.md` (the taste layer),
  a **`.grow`** helper, and rewrote the vertical-placement rule: **fill the full canvas top→bottom** —
  empty top *and* empty bottom both read unfinished (header → growing body → footer pinned bottom).
- **v9.6** — improvements mined from generating a full 10-slide deck (`examples/case-study/`) through the
  render→screenshot→critique loop: subtle elevation tokens **`--shadow-card` / `--shadow-pop`** + an
  elevation rule (shadows are depth, not drama); **`.slide.top`** modifier + a vertical-placement rule so
  thin header-led slides (agenda, tables) pin the title to the top instead of floating with an empty top
  band. Confirmed leaning on existing `base.css` components is the reliable generation path.
- **v9.5** — closed the **output-quality loop**: expanded `foundations/layout-balance.md` with whole-page
  composition, a density rule (不空不擠, ~30–45% whitespace), and proportional sizing (title/body/icon/number
  scaled to their container); added `foundations/self-critique.md` — **render → score vs the rules and the
  reference → fix until ≥ the reference**. Audit gained Layout-balance and Reference-match checks.
- **v9.4** — added `foundations/imagery.md`: the agent now **asks the user for real assets** (screenshots,
  logos, photos, data) at planning time, and a taxonomy for keeping imagery on-system (device mockups,
  background tints, one recolored illustration style, stock-person illustrations, annotated screens, the
  logo/photo full-color exceptions). New patterns mined from real slides: `timeline`, `value-points`,
  `use-case-cards`, `as-is-to-be`, `taglist`. Audit gained an Imagery section.
- **v9.3** — **intention** is now a first-class dimension: `slide-plan.md` names each page's job,
  `content-map.md` selects layout/components by intention (not just surface shape), `spec-template.md`
  records each pattern's `intent`/`triggers` + an *Intention & rationale* section, and
  `learn-from-image.md` learns the **intention↔component-usage relationship** (and the reverse trigger:
  "what content should use this layout") from each slide image.
- **v9.2** — make-a-slide engine is now an explicit **two-stage pipeline**: `slide-plan.md` (decide each
  page's structure first) → `content-map.md` (then pick layout + components); added
  `foundations/learn-from-image.md` — a harness loop that learns new theme-agnostic components/layouts
  from user-supplied slide images (color stays a separate layer, so learned patterns are reusable).
- **v9.1** — added `foundations/source-sync.md` (closes the spec → audit → enforce → **sync** loop); tier-naming map (components/layouts ↔ atoms/molecules/organisms) in README.
- **v9** — unified into an agent skill: LLM-readable `specs/` library (color-as-separate-theme-layer,
  first-class iconography, content→layout map, drift audit, spec template, catalog mined from 12 real
  decks) + the real `assets/` implementation + pptx bridge.
- **v8** — show-the-reasoning pattern, section cover (扉頁), bilingual tags, range-framing.
- **v6–v7** — plain-language layer, full component library, spacing/grid, two locked modes, PPTX bridge.
