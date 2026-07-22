---
name: bonny-slide-system
description: Build, critique, and iterate bilingual 繁中 + English UX/product slides and decks (HTML per-slide, single-scroll HTML, PDF, or PPTX). The agent READS specs/ and BUILDS with assets/. Use for UX/product storytelling, workshop and workflow slides, design-system decks, reference-image learning, and intention-routed generated editorial explainers. Every deck must record a per-slide illustration decision; human/agent workflows, conversational worked examples, workshop facilitation, and scattered-input transformations require a fresh built-in image-generation call unless precise data must stay native. Never silently substitute reused artwork, CSS, SVG, or a hand-built diagram.
metadata:
  version: 12.8.0
---

# Bonny Slide System — agent skill

## When to use
Any time the user wants to make, fix, or critique slides/decks for UX or product work, bilingual
繁中 (primary) + English (supporting).

## How this skill is organized
- **`specs/`** — the LLM-readable design system you READ each run. Source of truth for *rules*:
  `foundations/` (color-discipline, themes-and-modes, typography, spacing-grid, layout-balance,
  iconography, **imagery**, **generated-editorial-explainer**, plain-language, storytelling,
  **self-critique**, source-sync, **learn-from-image**) · `themes/` · `tokens/` ·
  `components/` · `layouts/` · **`slide-plan.md`** · `content-map.md` · `audit.md` · `spec-template.md` · `_catalog.md` · **`preferences.md`** (taste from A/B rounds).
- **`system/`** — canonical machine-readable tokens, hypertokens, pilot recipes, and JSON schemas.
  `migrationStatus` is engineering metadata only and never affects component/layout selection.
- **`scripts/compile_system.py`** — the deterministic compiler. It generates CSS, the PPTX bridge, and a
  Markdown reference; generated files are never edited by hand.
- **`assets/`** — the CSS you BUILD with. `base.css` is the compatibility/component layer and imports the
  generated foundations + five pilot hypertokens; load ONE generated theme file
  (`tokens-light.css` / `tokens-dark.css`). For self-contained HTML, inline the import-free generated
  `assets/generated/base-bundle.css` plus one theme.
- **`examples/`** — rendered reference slides; **`examples/deck-demo/`** + `deck-demo-scroll.html` = a full short deck showing how layouts chain (pacing, bridges, dividers). **`pptx/`** — token-mirrored python bridge for .pptx.

## Operating procedure (every deck)
1. **Inputs:** audience/room; **one theme** (mode + accent) — ask if unstated; the content/source. **Ask
   the user for any real assets** the deck needs — screenshots, logos, photos, data (`specs/foundations/imagery.md`).
2. **Load rules:** read `specs/foundations/*` + the chosen `specs/themes/<theme>.md`. Lock the theme deck-wide.
3. **Outline — structure first:** turn the file into a page-by-page plan with `specs/slide-plan.md`
   (one claim per slide; order method → range → relationships → conclusion per
   `specs/foundations/storytelling.md`; place covers/section-covers/bridges). Run the editorial-explainer
   suitability gate after naming each intention. Save every yes/no decision in the deck's
   `illustration-plan.json`; each record includes `trigger`, `hard_candidate`, `gate`, and `reason`.
   A hard candidate may use `gate: no` only with an explicit precision override. An omitted decision is a
   build error. **No components or layouts yet.**
4. **Map — visuals second:** for each planned page, find its shape in `specs/content-map.md` → layout + components.
   Human/agent workflows, conversational worked examples, workshop instructions, and scattered-input
   transformations are hard candidates: choose the generated route unless exact data/table/UI evidence must
   stay inspectable. When the map selects `editorial-explainer-stage`, read
   `specs/foundations/generated-editorial-explainer.md` and choose its composition variant by intention.
5. **Build:** write HTML with `assets/base.css` classes + the theme token file. Hypertokens are
   implementation fragments, **not a component whitelist**: choose through `content-map.md`, then let the
   component recipe resolve fragments. **Token names only — never hardcode color.** Icons per
   `specs/foundations/iconography.md`; images per `specs/foundations/imagery.md`. For
   `editorial-explainer-stage`, **invoke the `imagegen` skill and built-in image-generation tool** with the
   matching files under `assets/illustration-style/` as style references. Generate a fresh asset at the
   target block's exact aspect ratio. Never reuse a reference as output, trace it with CSS/SVG, or replace
   generation with a hand-built diagram. If the generator is unavailable, stop and report the blocker; never
   downgrade silently. Save the asset locally, record generator provenance in `illustration-plan.json`, validate,
   then place the generated image full-block with `data-editorial-explainer="<variant>"`.
6. **Write plainly:** every title/caption passes `specs/foundations/plain-language.md`.
7. **Audit & self-critique:** first run
   `python scripts/validate_editorial_explainer_plan.py illustration-plan.json DECK.html`; then **render at deck
   size and look** — run `specs/audit.md`, then self-critique
   per `specs/foundations/self-critique.md`: score whole-page balance, density (不空不擠), proportional
   sizing, and (if a reference was given) whether the build is **≥ the reference**. Fix the worst, re-render,
   repeat until every dimension passes.
8. **Output:** per-slide HTML, single-scroll HTML, PDF, or PPTX (`pptx/`). Deliver only after the build clears the gate.

## Golden rules (never break)
- **One theme per deck** — color is a separate layer; layouts/components stay theme-agnostic.
- **4-color discipline** — accent is the only chromatic color.
- **繁中 primary + English supporting; no Korean.**
- **One claim per slide; plain-language titles; purposeful icons, one style.**
- **A generated editorial explainer must be genuinely generated.** Canonical images are style
  reference only; CSS/SVG recreation, reference reuse, grayscale filtering, and contain-fit gutters fail.
- **No silent illustration bypass.** Every slide appears in `illustration-plan.json`; any `gate: yes` page
  must have a local fresh asset, built-in generator provenance, a valid variant, and matching HTML placement.
- **Hard candidates are machine-checked.** A hard candidate cannot use `gate: no` without an allowed precision
  override. Split mixed workflow + table pages into a generated overview and a native evidence slide.
- For a system/decision, **show the reasoning before the conclusion.**

## Learning loop (gets smarter from the user's slides)
The user keeps sending **reference slide images**. Each one grows the library — follow
`specs/foundations/learn-from-image.md`:
1. **Read the intention, not just the look.** For each image extract five things: its **intention** (the
   job it does to the audience), the **trigger** (what content should summon this layout next time), the
   **layout logic**, the **component craft** (how each component is shown), and the **intention↔component
   rationale** (*why* those components achieve the job).
2. **Learn structure, not color.** Color is a separate theme layer, so record colors only as **token
   roles** — never hex/px. Every learned pattern stays theme-agnostic and reusable under any theme.
3. **Dedupe vs `specs/_catalog.md`** → existing (add to `learned_from`) · `todo` (write it now) ·
   variant (extend the spec) · new (create one via `spec-template.md`, filling `intent`, `triggers`, and
   the *Intention & rationale* section).
4. **Register & reach it:** update `_catalog.md` (`learned_from: ImgN`) and add/refresh a
   `content-map.md` row keyed on **intention** so the planner reaches for it when that intention recurs.
5. **Audit + sync** the new spec/example (`audit.md`, `foundations/source-sync.md`). More images →
   denser intention→layout map + rationale library → better autonomous planning and building.

## Extending the system
- New component/layout → copy `specs/spec-template.md`, fill it, add a class to `assets/base.css`
  (or include inline CSS in the spec example), update `specs/_catalog.md`. `todo` items in the catalog
  are built by composing existing `base.css` primitives per their spec until a class exists.
- New theme → copy a `specs/themes/*.md`, keep the role names, **one accent**. Run `audit.md`.

## Changelog
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
