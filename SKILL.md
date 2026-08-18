---
name: bonny-slide-system
description: Build, critique, and iterate bilingual 繁中 + English UX/product slides and decks (HTML per-slide, single-scroll HTML, PDF, or PPTX). The agent READS specs/ and BUILDS with assets/. Use for UX/product storytelling, workshop and workflow slides, design-system decks, reference-image learning, and intention-routed generated editorial explainers. Every deck must record a per-slide illustration decision; human/agent workflows, conversational worked examples, workshop facilitation, and scattered-input transformations require a fresh built-in image-generation call unless precise data must stay native. Never silently substitute reused artwork, CSS, SVG, or a hand-built diagram.
metadata:
  version: 12.9.0
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
- **`specs/generated-router.md`** — the **complete intention→pattern index**, compiled from every spec's
  `intent` + `triggers` frontmatter (machine form: `system/router.json`). This is the authoritative list of
  what exists; `content-map.md` is the narrative layer that adds detection heuristics and component
  pairings. Both are kept in sync by the compiler's `--check`, which fails on routing drift.
- **`system/`** — canonical machine-readable tokens, hypertokens, pilot recipes, and JSON schemas.
  `migrationStatus` is engineering metadata only and never affects component/layout selection.
- **`scripts/compile_system.py`** — the deterministic compiler. It generates CSS, the PPTX bridge, the
  router, and a Markdown reference; generated files are never edited by hand. `--check` fails on token
  **and routing** drift.
- **`scripts/validate_layout.py`** — the layout gate. Renders a built slide and measures balance,
  distribution, and density against `foundations/layout-balance.md`, so those rules are enforced rather
  than merely described.
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
4. **Map — visuals second:** for each planned page, **look its intention up in `specs/generated-router.md`**
   (match `intent` first, confirm with `triggers`), then read that row's `content-map.md` entry for the
   detection heuristic and component pairing. The router is the complete list — if you are about to invent
   a layout, you have missed one. Then find its shape in `specs/content-map.md` → layout + components.
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
Version history lives in `CHANGELOG.md` — it is not needed at build time.
