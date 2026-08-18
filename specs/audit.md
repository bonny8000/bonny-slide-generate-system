# Drift audit — run before delivery

The "mandated audit" step. A sub-agent checks the finished slide/deck against the specs and reports
issues with a severity. Fix **blocker** + **major** before delivery.

## Run the machine checks first
Two gates are mechanical — run them before the human-judgement checks below, and fix what they
report. They exist because these rules used to be prose only, and prose degrades first.

```bash
python scripts/compile_system.py --check          # tokens + routing drift
python scripts/validate_layout.py DECK.html       # rendered balance + density
```

- `compile_system.py --check` fails on routing drift: a stable layout with no `content-map.md` row,
  an orphan component, an unresolvable `depends_on`, a duplicate trigger, or **any Korean in a
  routing trigger**. — blocker
- `validate_layout.py` renders each slide and fails on a blank/unstyled render, a dead band inside
  the content, an empty top or bottom band, a dead quadrant, or extreme density. Add `--strict-hex`
  to also scan `<style>` blocks for hardcoded colour. — blocker on a failure it reports
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

## Severity
- **blocker** — breaks the system identity (mixed theme, 2nd accent, Korean). Must fix.
- **major** — visibly off-system (raw colors, tiny text, unbalanced, mixed icon styles). Fix.
- **minor** — polish (a decorative icon, a stray dep). Fix if time.

## Output format
`severity · slide · check · what's wrong · suggested fix`
