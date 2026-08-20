---
name: bonny-slide-system
description: Build, critique, and iterate bilingual 繁中 + English UX/product slides and decks (HTML per-slide, single-scroll HTML, PDF, or PPTX). The agent READS specs/ and BUILDS with assets/. Use for UX/product storytelling, workshop and workflow slides, design-system decks, reference-image learning, and intention-routed generated editorial explainers. Every deck must record a per-slide illustration decision; human/agent workflows, conversational worked examples, workshop facilitation, and scattered-input transformations require a fresh built-in image-generation call unless precise data must stay native. Never silently substitute reused artwork, CSS, SVG, or a hand-built diagram. Also runs in training mode: when the user says "training"/"訓練" or sends reference slides or images to learn from, do not build a deck - read the references for intention, trigger, layout logic and component craft, and register the pattern into specs/ so the planner can route to it next time.
metadata:
  version: 12.9.0
---

# Bonny Slide System — agent skill

## When to use
Any time the user wants to make, fix, or critique slides/decks for UX or product work, bilingual
繁中 (primary) + English (supporting) — **or** wants to *train* the system by sending reference slides
and images to learn from. Check which mode you are in before doing anything (next section).

## How this skill is organized
- **`specs/`** — the LLM-readable design system you READ each run. Source of truth for *rules*:
  `foundations/` (color-discipline, themes-and-modes, typography, spacing-grid, layout-balance,
  iconography, **imagery**, **generated-editorial-explainer**, plain-language, storytelling,
  **self-critique**, source-sync, **learn-from-image**) · `themes/` · `tokens/` ·
  `components/` · `layouts/` · **`slide-plan.md`** · `content-map.md` · `audit.md` · `spec-template.md` · `_catalog.md` · **`preferences.md`** (taste from A/B rounds).
- **`specs/generated-router.md`** — the **complete intention→pattern index**, compiled from every spec's
  `intent` + `triggers` frontmatter (machine form: `system/router.json`). This is the authoritative list of
  what exists; `content-map.md` is the narrative layer that adds detection heuristics and component
  pairings. Both are kept in sync by the compiler's `--check`, which fails on routing drift.
- **`system/`** — canonical machine-readable tokens, hypertokens, pilot recipes, and JSON schemas.
  `migrationStatus` is engineering metadata only and never affects component/layout selection.
- **`scripts/compile_system.py`** — the deterministic compiler. It generates CSS, the PPTX bridge, the
  router, and a Markdown reference; generated files are never edited by hand. `--check` fails on token
  **and routing** drift.
- **`specs/generated-class-coverage.md`** — which catalogued patterns can actually be built from
  `assets/base.css`, and which need classes that exist only inside their own example (machine form:
  `system/class-manifest.json`). A pattern with gaps has to be reinvented on every build, so treat its
  gaps as the implementation backlog. **`base.css` stays hand-written — this is a usage contract,
  never codegen.**
- **`scripts/sync_examples.py`** — will make `examples/` pure REFERENCE, with implementation only in
  `assets/base.css`. Built and verified, but not yet applied: `base.css` first needs its 17 bare
  generic selectors scoped to their owning pattern (see CHANGELOG), or patterns collide once they
  share one stylesheet.
- **`scripts/validate_layout.py`** — the layout gate. Renders a built slide and measures balance,
  distribution, and density against `foundations/layout-balance.md`, so those rules are enforced rather
  than merely described.
- **`assets/`** — the CSS you BUILD with. `base.css` is the compatibility/component layer and imports the
  generated foundations + five pilot hypertokens; load ONE generated theme file
  (`tokens-light.css` / `tokens-dark.css`). For self-contained HTML, inline the import-free generated
  `assets/generated/base-bundle.css` plus one theme.
- **`examples/`** — rendered reference slides; **`examples/deck-demo/`** + `deck-demo-scroll.html` = a full short deck showing how layouts chain (pacing, bridges, dividers). **`pptx/`** — token-mirrored python bridge for .pptx.

## Two modes — read the request before building anything
This skill runs in one of two modes. Decide which **before** doing any work.

| The user says | Mode | What it means |
|---|---|---|
| "make a slide/deck", a topic, a source file | **build** | Produce slides. Follow the operating procedure below. |
| **"training"** / **"訓練"**, or sends reference images or slides to learn from | **training** | Do **not** build a deck. Grow the library from what they sent. |

**Training mode is not slide-making.** The user is teaching the system, so the output is a change to
`specs/`, not a deck. Never answer a training request with a slide; never silently fold a sent image
into a build. If the intent is ambiguous — an image arrives with no instruction — **ask which one**,
because the two produce completely different artifacts.

### Training mode procedure
1. **Read each reference for all five things** in `specs/foundations/learn-from-image.md` — intention,
   trigger, layout logic, component craft, and the intention↔component rationale. Structure only:
   colours are recorded as **token roles**, never hex. A reference in any language teaches STRUCTURE
   only — the deck's output language is a separate, declared decision (default 繁中 + English).
2. **Dedupe against `specs/_catalog.md`** → existing (add to `learned_from`) · variant (extend the
   spec) · new (create one from `specs/spec-template.md`).
3. **Register it so it is actually reachable.** A pattern the planner cannot find does not exist:
   - `intent` + `triggers` frontmatter on the spec — the router is compiled from these
   - a row in `specs/_catalog.md` and a row in `specs/content-map.md`, keyed on **intention**
   - a render-validated example, referenced by `example:`
4. **Close the loop — run the gates.** `python scripts/compile_system.py --check` must pass: it fails
   on a stable layout with no `content-map.md` row, an unresolvable `depends_on`, a duplicate trigger,
   or a trigger in a language the router does not match on. Then
   `python scripts/validate_layout.py <example>`.
5. **Report what the system learned** — the new/updated pattern, its intention, its triggers, and what
   will now route to it. The point of training is that the *next* deck reaches for it automatically.

**Implementation debt is part of training.** If the new pattern needs CSS, add it to `assets/base.css`
— not only to the example. `specs/generated-class-coverage.md` tracks patterns whose CSS lives only in
their example; those cannot be rebuilt by the agent and must be reinvented every time, which is how
consistency drifts.

## Operating procedure (every deck)
1. **Inputs:** audience/room; **one theme** (mode + accent) — ask if unstated; the content/source. **Ask
   the user for any real assets** the deck needs — screenshots, logos, photos, data (`specs/foundations/imagery.md`).
2. **Load rules:** read `specs/foundations/*` + the chosen `specs/themes/<theme>.md`. Lock the theme deck-wide.
3. **Outline — structure first:** turn the file into a page-by-page plan with `specs/slide-plan.md`
   (one claim per slide; order method → range → relationships → conclusion per
   `specs/foundations/storytelling.md`; place covers/section-covers/bridges). Run the editorial-explainer
   suitability gate after naming each intention. Save every yes/no decision in the deck's
   `illustration-plan.json`; each record includes `trigger`, `hard_candidate`, `gate`, and `reason`.
   **A routed layout whose `assetPolicy` is `generate` and whose artwork the user did not supply is
   itself a `gate: yes` trigger** — record it as `material:illustration` and generate. Do not dodge it
   by swapping to a text-only layout; that turns a routing decision into a silent visual compromise.
   Covers, section covers, bridges, agenda and closing pages are always `gate: no`, reason
   `structural-page` — their job is punctuation, not explanation.
   A hard candidate may use `gate: no` only with an explicit precision override. An omitted decision is a
   build error. **No components or layouts yet.**
4. **Map — visuals second:** for each planned page, **write one normalised line before you look
   anything up**, in this exact form:

   > `意圖: <what this page must DO>  ·  形狀: <material> / <arrangement> / <count>`

   Material is `chart · quote · stat · ui-screen · illustration · icon · text-only` (or a `+` pair);
   arrangement and count come from the same controlled vocabulary as the router. Derive the shape
   from **the content you actually have**, never from the layout you are hoping to use.

   Then look that line up in `specs/generated-router.md`. **Shape is the decisive axis, not
   intention.** Measured on this library: intention alone identifies 13 of 25 layouts, because pairs
   like `idea-evidence`/`painpoint-evidence` share a job and differ only in material — a chart versus
   participant quotes. The shape triple alone identifies 24 of 25. Match the shape, then use
   intention to break the one remaining tie. On held-out requests this took routing from 4/10 to
   8/10; skipping the normalised line is the single biggest cause of picking the wrong layout.

   Then read that row's `content-map.md` entry for the
   detection heuristic and component pairing.

   **When the router leaves two or more candidates, apply `foundations/layout-choice.md` in order:**
   availability → fit → variety → intent proximity. Availability is a hard filter, not a preference —
   but only `must-supply` disqualifies. **`assetPolicy: build` means draw the screen yourself**: a
   `ui-mockup` is schematic, made from `.phone` / `.mock` / `.appframe` / `.sk` in `base.css` per
   `components/ui-mockup.md`, so never ask the user for it and never drop a layout for lacking one.
   Only a real `ui-screen` (the `ui-qa` route) may never be produced; there, fall back to the
   layout's declared `alternates` or ask the user. Fit outranks variety: a repeated layout that fills
   the page beats a fresh one that starves it. The router is the complete list — if you are about to invent
   a layout, you have missed one. Then find its shape in `specs/content-map.md` → layout + components.
   Human/agent workflows, conversational worked examples, workshop instructions, and scattered-input
   transformations are hard candidates: choose the generated route unless exact data/table/UI evidence must
   stay inspectable. When the map selects `editorial-explainer-stage`, read
   `specs/foundations/generated-editorial-explainer.md` and choose its composition variant by intention.
5. **Build:** write HTML with `assets/base.css` classes + the theme token file. Check the pattern in
   `specs/generated-class-coverage.md` first — if it lists missing classes, that CSS does not exist yet
   and you must add it to `base.css` rather than inventing a one-off in the page. **Layout varies by
   intention; vocabulary never varies** (`foundations/layout-balance.md`). Hypertokens are
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
7. **Audit & self-critique:** run the three mechanical gates first — they fail loudly and name the fix:
   ```bash
   python scripts/compile_system.py --check                                  # tokens + routing drift
   python scripts/validate_editorial_explainer_plan.py illustration-plan.json DECK.html
   python scripts/validate_layout.py DECK.html                               # rendered balance
   python scripts/validate_layout.py slides/ --deck                          # + deck pacing
   ```
   Then **render at deck size and look** — run `specs/audit.md`, then self-critique
   per `specs/foundations/self-critique.md`: score whole-page balance, density (不空不擠), proportional
   sizing, and (if a reference was given) whether the build is **≥ the reference**. Fix the worst, re-render,
   repeat until every dimension passes.
8. **Output:** per-slide HTML, single-scroll HTML, PDF, or PPTX (`pptx/`). Deliver only after the build clears the gate.

## Golden rules (never break)
- **One theme per deck** — color is a separate layer; layouts/components stay theme-agnostic.
- **4-color discipline** — accent is the only chromatic color.
- **繁中 primary + English supporting by default** — a deck in another language is fine when the
  user asks for one; declare it (`validate_layout --lang`). That is an **output** constraint, enforced
  at render time. Routing *triggers* are deliberately multilingual — 繁中, English and Korean —
  because intention does not change with the language it is written in, and much of this library was
  learned from Korean reference decks. Deleting that vocabulary deleted recognition, not risk.
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
Version history lives in `CHANGELOG.md` — it is not needed at build time.
