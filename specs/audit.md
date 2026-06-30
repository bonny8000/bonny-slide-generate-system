# Drift audit — run before delivery

The "mandated audit" step. A sub-agent checks the finished slide/deck against the specs and reports
issues with a severity. Fix **blocker** + **major** before delivery.

## Checks
### Theme & color  (foundations/color-discipline.md, themes-and-modes.md)
- [ ] **One theme across the whole deck** (same mode + same accent on every slide). — blocker if mixed
- [ ] **≤ 4 color roles**; accent is the only chromatic color. — blocker on a 2nd accent
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
- [ ] Density comfortable (~30–45% whitespace): not 太擠, not 很空. — major
- [ ] Text/title/icon/number sized to role + container; content fills its box; icon never out-weighs its title. — major

### Reference match & self-critique  (foundations/self-critique.md)
- [ ] **Screenshotted** and reviewed visually at deck size — not critiqued from source, not "passed" on structural checks alone. — blocker
- [ ] Built HTML is self-contained (tokens + base.css inlined); no broken/unstyled render from unresolved links. — major
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

### Component / layout conformance
- [ ] Each slide maps to a real layout in `layouts/`; components used per their spec. — major
- [ ] `depends_on` respected (no upward/hidden deps). — minor

## Severity
- **blocker** — breaks the system identity (mixed theme, 2nd accent, Korean). Must fix.
- **major** — visibly off-system (raw colors, tiny text, unbalanced, mixed icon styles). Fix.
- **minor** — polish (a decorative icon, a stray dep). Fix if time.

## Output format
`severity · slide · check · what's wrong · suggested fix`
