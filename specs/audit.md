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

### Plain language  (foundations/ + plain-language)
- [ ] Title passes one-read test; no stacked modifiers; emphasis on ONE keyword. — major

### Icons / illustration  (foundations/iconography.md)
- [ ] One icon style across the deck (all line OR all filled). — major
- [ ] Icons monochrome from theme tokens; illustrations limited to theme colors. — major
- [ ] Every icon earns its place (no decorative-only icons). — minor

### Component / layout conformance
- [ ] Each slide maps to a real layout in `layouts/`; components used per their spec. — major
- [ ] `depends_on` respected (no upward/hidden deps). — minor

## Severity
- **blocker** — breaks the system identity (mixed theme, 2nd accent, Korean). Must fix.
- **major** — visibly off-system (raw colors, tiny text, unbalanced, mixed icon styles). Fix.
- **minor** — polish (a decorative icon, a stray dep). Fix if time.

## Output format
`severity · slide · check · what's wrong · suggested fix`
