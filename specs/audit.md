# Drift audit — run before delivery

The "mandated audit" step. A sub-agent checks the finished slide/deck against the specs and reports
issues with a severity. Fix **blocker** + **major** before delivery.

## Run the machine checks first
Two gates are mechanical — run them before the human-judgement checks below, and fix what they
report. They exist because these rules used to be prose only, and prose degrades first.

```bash
python scripts/compile_system.py --check          # tokens + routing drift
python scripts/validate_layout.py DECK.html       # rendered balance + density
python scripts/validate_layout.py slides/ --deck  # ...plus deck-level visual pacing
```

- `compile_system.py --check` fails on routing drift: a stable layout with no `content-map.md` row,
  an orphan component, an unresolvable `depends_on`, a duplicate trigger, or **any Korean in a
  routing trigger**. — blocker
- `validate_layout.py` renders each slide and fails on a blank/unstyled render, a dead band inside
  the content, a band of surface carrying no text (relocated emptiness), an empty top or bottom band,
  a dead quadrant, extreme density, or **copy in a script the declared output language does not
  imply** (default 繁中 + English; pass `--lang ja,en` and a Japanese deck passes). Add `--strict-hex` to also scan
  `<style>` blocks for hardcoded colour. — blocker on a failure it reports
- `sync_examples.py` is the tool that will make examples pure reference — implementation only in
  `assets/base.css`. It is NOT yet part of the gate: applying it first needs the 17 bare generic
  selectors in `base.css` (`.track`, `.card`, `.panel`, `.sub`, …) scoped to their owning pattern,
  or they collide across patterns once examples share one stylesheet.
- `--deck` additionally enforces the v12.7 anti-dryness rule across a deck of 8+ slides: at least one
  page must carry a genuine visual moment (real screenshot, logo-row, device mockup, or generated
  explainer). Icons and chips do not count. — major
- Neither gate replaces looking at the screenshot. They catch what is measurable; you still judge
  intention, hierarchy, and craft.

## Checks
### Theme & color  (foundations/color-discipline.md, themes-and-modes.md)
- [ ] **One theme across the whole deck** (same mode + same accent on every slide). — blocker if mixed
- [ ] **≤ 4 color roles**; accent is the only chromatic color. — blocker on a 2nd accent
- [ ] Editorial-explainer bitmap exception is confined to sparse avatar/highlight hues inside the image; native
      components still use one accent. — blocker if supporting hues leak into the slide system
- [ ] **No raw colors** in markup; token names only. — major
- [ ] Charts: inactive = muted, active = accent. — major

### Typography  (foundations/typography.md)
- [ ] CJK Noto Sans TC 0.05em; Latin/numbers Arial 0; line-height 1.5. — major
- [ ] No meaningful text below 16px. — major
- [ ] 繁中 primary, English supporting; no Korean. — blocker on Korean
- [ ] No terminal 句號/full stop on titles, statements, captions; complete clauses not orphaned across lines. — minor

### Layout & balance  (foundations/spacing-grid.md, layout-balance.md)
- [ ] Spacing on the 8px scale; equal four-side margins; content vertically centered, fills the canvas. — major
- [ ] One claim per slide; visual sits next to the text it supports. — major
- [ ] Whole-page weight balanced; no heavy quadrant against an empty one. — major
      *(machine-checked: `validate_layout.py` dead-quadrant check)*
- [ ] Density comfortable (~30–45% whitespace): not 太擠, not 很空. — major
- [ ] **No dead band inside the content** — an even top/bottom margin can still hide an empty
      lower half. — major *(machine-checked: `validate_layout.py` interior-gap check)*
- [ ] Text/title/icon/number sized to role + container; content fills its box; icon never out-weighs its title. — major

### Reference match & self-critique  (foundations/self-critique.md)
- [ ] **Screenshotted** and reviewed visually at deck size — not critiqued from source, not "passed" on structural checks alone. — blocker
- [ ] Built HTML is self-contained (tokens + base.css inlined); no broken/unstyled render from unresolved links. — major
- [ ] Self-contained HTML uses generated `assets/generated/base-bundle.css`; no unresolved `@import`. — major
- [ ] If a reference was given: build delivers the intention **≥** the reference (composition, density, hierarchy, craft). — major
- [ ] Build does NOT copy the reference's off-system choices (extra hues, off-palette art). — major

### Plain language  (foundations/ + plain-language)
- [ ] Title passes one-read test; no stacked modifiers; emphasis on ONE keyword. — major

### Icons / illustration  (foundations/iconography.md)
- [ ] One icon style across the deck (all line OR all filled). — major
- [ ] Icons monochrome from theme tokens; illustrations limited to theme colors. — major
- [ ] Every icon earns its place (no decorative-only icons). — minor

### Imagery  (foundations/imagery.md)
- [ ] Non-photo/logo imagery recolored to palette; one illustration style deck-wide. — major
- [ ] Images seated on a surface, not floating on bare canvas. — minor
- [ ] No fabricated screenshot or fake-precise data presented as real. — blocker
- [ ] Asked the user for assets (screenshots/logos/photos/data) that would materially improve a page. — minor

### Generated editorial explainer
- [ ] `illustration-plan.json` exists and contains a decision for every slide. — blocker
- [ ] `python scripts/validate_editorial_explainer_plan.py illustration-plan.json DECK.html` passes. — blocker
- [ ] Stage-1 intention gate is `yes`; the explainer communicates the human process better than a native layout. — major
- [ ] A built-in image-generator call created a **fresh** output using the matching canonical variant references. — blocker
- [ ] The result is not a reference image, crop/trace, CSS/SVG recreation, or hand-built diagram. — blocker
- [ ] Generated dimensions match the target block ratio; image fills the block with no contain-fit gutters. — major
- [ ] No grayscale/desaturation filter; colour is visibly preserved and supporting hues stay inside the bitmap. — major
- [ ] Exact copy is native/editable, or every baked word was verified; no Korean, logo, watermark, or random text. — blocker
- [ ] `ui-qa` uses a real supplied screenshot; no generated/fabricated product UI. — blocker
- [ ] Generated file is saved inside the deck and visibly placed. — blocker
- [ ] A selected generated route was not silently downgraded because the generator was unavailable. — blocker

### Component / layout conformance
- [ ] Each slide maps to a real layout in `layouts/`; components used per their spec. — major
- [ ] `depends_on` respected (no upward/hidden deps). — minor

### Hypertoken pipeline
- [ ] `python scripts/compile_system.py --check` passes. — blocker
- [ ] Generated CSS/Python/Markdown was not edited by hand. — major
- [ ] Component/layout choice still follows `content-map.md`; migration status carries zero selection weight. — blocker
- [ ] Unmigrated catalog components remain available; pilot hypertokens are not a whitelist. — blocker
- [ ] Managed properties have one canonical owner in `system/*.json`. — major

## Reading the examples: three things that look like defects and are not

Reviewers keep flagging these. Check here before opening one as a finding.

**A slide-specific `<style data-slide>` block is by design.** Every example ships one. Stripping it
and re-rendering will differ — that is the block doing its job, not a pattern that failed to adopt
the shared system. `scripts/verify_rebuild.py` reports this as *local reliance*, a magnitude to read,
not a pass/fail. High reliance is worth investigating; any reliance is not.

**Not every hex in an example is a violation.** The zero-raw-hex rule is absolute for
`assets/base.css`, which is clean. In examples it applies to *theme* colour. Three files still carry
literals, and they are not all the same thing: `#fff` inside `color-mix()` (`r45A`) is a blend
operand, not a colour choice, and `rgba()` in a shadow or a radial-gradient stop is opacity work.
What **is** a real finding is `editorial-explainer-stage`'s `.tag{color:#16899b}` — a teal that is a
second accent, which this document rates a blocker. It is open, not blessed.

(A Claude-brand deck — `claude-code-ccv1`, `ccv2`, `how-to-use-claude-code` — used to sit here with a
warm off-token palette. It was deleted rather than tokenised: off-system reference can only teach
off-system colour.)

**A larger value than base.css is often deliberate.** `.mc .t` is 33px in `light-metric-cards` and
22px in base. That is per-slide sizing tuned to a three-card row, not a stale copy. Do not
bulk-revert example values to base values; check what the slide actually needs.

## Severity
- **blocker** — breaks the system identity (mixed theme, 2nd accent, Korean). Must fix.
- **major** — visibly off-system (raw colors, tiny text, unbalanced, mixed icon styles). Fix.
- **minor** — polish (a decorative icon, a stray dep). Fix if time.

## Output format
`severity · slide · check · what's wrong · suggested fix`
