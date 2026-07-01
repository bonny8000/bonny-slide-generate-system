---
id: source-sync
kind: foundation
status: stable
---
# Source sync — keeping specs and implementation in step

This closes the diagram's last arrow ("update specs with regular source sync"). Without it, a
spec-driven system slowly drifts back to the traditional one-time-styleguide failure mode.

## Canonical sources (who wins on a conflict)
- **Token values** → `system/tokens.json`. `assets/tokens-*.css`,
  `assets/generated/foundations.css`, `assets/generated/base-bundle.css`, and
  `pptx/generated_tokens.py` are generated outputs.
- **Hypertoken fragments + compatibility selectors** → `system/hypertokens.json`.
- **Pilot component recipes** → `system/recipes.json`. Recipe migration status is engineering metadata and
  has **zero selection weight**; `specs/content-map.md` remains intention-first.
- **Component / layout implementation not yet migrated** → `assets/base.css` classes.
- **Rules, usage, decision logic** → `specs/` (foundations, content-map, component/layout specs, audit).
- **Index of what exists + status** → `specs/_catalog.md`.

## Three sync directions
1. **canonical data → generated outputs.** Edit only `system/*.json`, then run
   `python scripts/compile_system.py`. Never patch generated CSS, Python, or reference Markdown by hand.
2. **spec ↔ implementation.** When you add or change a non-migrated class in `base.css`, update its spec
   (and the reverse). A spec that references a missing class/token, or a `stable` class with no spec, is drift.
3. **real decks → system.** When you build an actual deck and either invent a new pattern or hit a
   recurring content shape with no home, capture it back into the system: add a spec (via
   `spec-template.md`), add a `base.css` class, update `_catalog.md` and `content-map.md`. This is how
   the system *learns* (the v1 catalog itself was mined from 12 real decks).

## Cadence (lightweight — sync at the moment of change)
- **Per deck:** before finishing, ask "did I improvise anything not in the system?" → if yes, fold it back.
- **Per change to tokens/hypertokens/recipes:** edit `system/*.json`, compile, then run `--check`.
- **Per change to non-generated `assets/`:** update the matching spec + `last_synced` in its front-matter.
- **Every ~N decks (or monthly):** run `audit.md` across the library; clear stale `todo`s; bump
  `SKILL.md` version + changelog when the system changes.

## Reconcile checklist
- [ ] Every spec's `tokens_used` / `depends_on` exist.
- [ ] `python scripts/compile_system.py --check` passes; generated files are current.
- [ ] Hypertoken and recipe `migrationStatus` does not affect layout/component selection.
- [ ] Existing catalog entries remain usable whether migrated or not.
- [ ] Every `stable` component/layout has both a spec and a (still-rendering) example.
- [ ] No raw colors crept into `base.css`; token names only.
- [ ] `_catalog.md` status matches reality (no `stable` that's missing, no `todo` already built).
- [ ] `last_synced` updated on anything that changed.
