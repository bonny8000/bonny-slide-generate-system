# Maintenance and verified boundaries

## Source and generation
- Edit canonical tokens in `system/tokens.json`, implementation fragments in `system/hypertokens.json`,
  slot bindings in `system/recipes.json`, selection metadata in spec frontmatter, and shared layout
  styles in `assets/base.css`. All 44 patterns have connected recipes; see [the contract](tokens/recipes.md).
- Run `python scripts/compile_system.py`, then `python scripts/sync_examples.py`.
- The generated bundle already contains base.css. Inline one theme and one bundle, never base twice.
- `<style data-slide>` is the supported place for authored slide-specific overrides. Sync preserves it;
  reusable component styles belong in scoped shared selectors.
- Explicit `data-theme="dark"` prevents a dark example from silently receiving the light theme.
- When promoting styles out of an example, check whether the shared rule already exists before
  pasting it. Each `/* ===== … promoted from examples/… ===== */` block re-pasted its own copy of the
  common card rules, which left `.card` defined nine times, `.foot` four and `.kicker` three — all
  byte-identical. Those 20 redundant lines were removed (keeping the last occurrence of each, so the
  rule that already won the cascade stays in place); a promotion that re-pastes them puts the drift
  risk straight back.
- Default sync excludes any `_ab`/`_audit` example folder. Their 115 existing HTML files are frozen
  historical evidence, not stale files to bulk update. `--include-archives` is an explicit opt-in.

## Repeatable checks
```bash
python scripts/check_system.py
python scripts/check_system.py --render
python scripts/validate_editorial_explainer_plan.py examples/case-study/illustration-plan.json examples/case-study
python scripts/verify_rebuild.py light-feature-showcase light-screen-interiors light-idea-evidence
python scripts/calibrate_gate.py --json work/calibration.json
python scripts/visual_baseline.py diff
```
Core CI runs compiler freshness, current-example sync, regression tests and both routing fixtures on
Python 3.10/3.12. Browser tests run locally with installed Chromium and fonts; they are not claimed
as completed by the core CI job. `--render` reports skipped non-slide artifacts explicitly.

There are **58 current HTML files**: 54 individual 1920×1080 slides, two 1080px-wide long posters,
one editorial reference gallery, and one eight-slide scroll viewer. Do not count a viewer as a single
validated slide or a poster's first viewport as its full page.

For the two survey posters, measure full height in the browser, then render at that height and review
all content. The August 2026 content is approximately 1406px tall before font/environment variation:
```bash
python scripts/validate_layout.py examples/dark-01-survey-stack.html --poster-height 1450
```
Poster checks cover blank output, language and inline color violations, not 16:9 density thresholds.
A supplied height is not automatic proof that no content is cropped; inspect the full render.

Gate exit codes: layout/check suite `0` passed applicable checks, `1` a quality/regression failure,
`2` could not run. A viewer/poster/reference-only invocation without an applicable render cannot
claim success. Illustration-plan violations use `1`.

## A/B evidence
R1–R50 contain 37 available A/B file pairs. R51–R55 were judged by the user on 2026-08-31:
**B, A (with numeric alignment correction), A, B, A**. Their portable frozen variants, shown PNGs,
and hashes live under `specs/ab-reviewed/2026-08-31/`.

`ab_round.py` creates a separate review directory and never overwrites frozen historical variants.
Already-rendered or judged pairs require a new experiment/output folder. The calibration script
reads both judgement sources, excludes pending rounds, checks the saved hashes and reports missing
historical pairs. It refuses to quietly omit new judged rounds when their manifest is unavailable.
A/B agreement is a diagnostic on the given browser/fonts, not an automatic taste score.

## PDF and PowerPoint
```bash
python -m pip install -r requirements-export.txt
python scripts/export_pdf.py examples/case-study --out work/case-study.pdf
```
PDF export prints each ordered individual slide with Chromium, verifies exactly one PDF page per
input, then merges with pypdf. It preserves native text where the browser supports it and retains
relative asset resolution without changing the source HTML. An existing output requires `--force`.
Print pages are 16:9 (1440×810 PDF points). This exporter deliberately rejects multi-slide viewers;
export the individual slide files. Review the exported PDF, especially fonts, before delivery.

`pptx/slidegen.py` is an existing native PowerPoint bridge with **three** template methods: `title`,
`hbars`, `features`. It does not cover all 25 layouts and does not convert arbitrary HTML to editable
PowerPoint. Expanding native PPTX coverage is separate implementation work, not a completed feature.

## Remaining limits
- This is an agent skill and tool library, not a hosted app or autonomous generation service.
- All 40 routing requests are regression fixtures now; there is no fresh independent accuracy score.
- All 44 patterns have fragment-level recipes, not complete JSON representations of every CSS rule.
  Structural geometry and contextual overrides remain hand-written; recipes never choose a layout.
- The plan validator checks real slide coverage and local per-slide asset placement. Generator names
  and reference lists are declarations; fresh-call provenance still needs external tool-call evidence.
- The structural reader handles ordinary omitted-head HTML and explicit hidden states. It is not a
  full browser DOM/CSS implementation, and cannot prove an external CSS rule did not hide an asset.
- Pixel balance heuristics cannot judge evidence quality, aesthetics, all overflow, or factual accuracy.
  The existing example data has not been independently verified as product/research results.

Visual baselines target the 54 current 16:9 slides by default. Capture updates only selected entries,
preserving historical fingerprints. Missing baseline entries fail the diff. Re-capture only after
reviewing an intentional change, with comparable Chromium/fonts; a new baseline is not independent
evidence of visual correctness. The committed capture was refreshed after this review on macOS.

## Cascade experiments retained from the consistency pass

**Before the bound-value migration, the hypertoken layer retained only `image.floating`.** It once
  held five. Four of them (`surface.card`, `text.heading`, `text.supporting`, `layout.stack.card`)
  restated rules `assets/base.css` already had, and were removed after measurement showed they could
  never take effect. Deleting the whole layer moved only 2 of 54 rendered slides, both traceable to
  `image.floating`'s shadow; the other four were inert. `metric-card` and `evidence-card` went with
  them, since every slot referenced a removed fragment. Adding a fragment that restates a base.css
  rule re-creates the same dead duplication.

**Making the hypertoken layer authoritative was attempted, measured and rejected. Do not retry it
  without reading this.** Generated fragments are `:where(...)` (zero specificity) inside
  `@layer hypertokens`; base.css is unlayered, and unlayered CSS beats every layered rule regardless
  of specificity. The layer is therefore designed to lose, which is correct for a fallback and fatal
  for a source of truth. Two routes were tried against a render baseline, and both regressed:
  - *Wrapping base.css in `@layer components`* moved 6 slides. A slide's own `<style data-slide>`
    stays unlayered, so it went from winning on source order to winning unconditionally — defeating
    the more specific `.mcrow.roomy .mc{min-height:430px}` (0,3,0) with a plain `.mc` (0,1,0). That
    430px is recorded preference **R53 A**, so the cascade silently reverted a human A/B decision.
  - *Deleting the shadowed base.css rules so the fragments drove them* moved 47 of 54 slides. The
    values were byte-identical; only cascade position changed. `.card` sits at the end of base.css
    and wins same-specificity contests by source order, so `class="card metric"` took `.card`'s
    `gap:var(--s4)` over `.metric`'s `gap:var(--s1)` (line 122). Demoted to a zero-specificity
    layered rule, it lost that contest and the gap collapsed.

  The blocker is not the selector grammar. `SELECTOR_RE` does admit only a single bare class
  (`^\.[a-z][a-z0-9_-]*$`), which puts 439 of 699 base.css rules (62%) outside it — but widening it
  would not help, because the demotion is what breaks. base.css currently encodes real design
  decisions as **implicit source-order dependencies**. Any migration has to make those dependencies
  explicit first; that audit is the prerequisite, not the schema.

The subsequent migration preserves those dependencies: recipes assign custom-property values, while
the consuming CSS declarations keep their exact selector, source order and layer. The de-duplicated
base.css remains unlayered; no former base-class aliases are restored. This avoids both rejected
routes above. The scoped showcase mockup now resolves its actual `shadow-card`, not the overridden
`image.floating` fallback. Existing `image.floating` aliases and their rendering behavior stay intact.
