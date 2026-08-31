# Catalog recipes

All **25 layouts and 19 components** have connected recipes: **165 slots** composed from
25 reusable hypertokens. Recipe coverage means that each slot has a real selector, a matching
element in its spec's example, and an authored CSS declaration that consumes the generated value.
It does not mean that all CSS or all PowerPoint layouts have been implemented in JSON.

## Find and use a recipe

Choose the pattern through the shape/intent router first. Then inspect its recipe:

```bash
python scripts/resolve_recipe.py metric-card --theme dark
```

The output includes the spec, example, slot selectors, fragment references, CSS properties, and
theme-resolved values. Hex colors in `resolved` omit `#` for the existing Python bridge. Read the
spec and compose its existing classes; no additional wrapper or `data-recipe` attribute is needed.
Use `assets/base.css` plus one theme for linked HTML, or one theme plus `base-bundle.css` inline.

For example, the `metric-card` root binds `.mc` to `surface.panel` and `layout.column`. The generated
bindings assign the surface/radius and column values on `.mc`; its authored CSS consumes them:

```css
.mc {
  background: var(--recipe-surface-panel-background);
  border-radius: var(--recipe-surface-panel-border-radius);
  display: var(--recipe-layout-column-display);
  flex-direction: var(--recipe-layout-column-flex-direction);
  /* Padding, height and composition-specific overrides stay in base.css. */
}
```

Bindings supply **custom properties**, not a second set of competing structural declarations.
The original declaration order and specificity stay intact. This preserves scoped overrides such as
R52's aligned numeric columns, R53's roomy metric cards and R55's equal accent labels.

`pptx/generated_tokens.py` also exposes `recipe(name, slot, mode)` for managed fragment values.
This is a token resolver; the PowerPoint renderer still only has three template methods.

## Source ownership and checks

1. Edit fragment values in `system/hypertokens.json`; theme values live in `system/tokens.json`.
2. Edit slot composition and selector bindings in `system/recipes.json`.
3. Keep layout geometry and contextual overrides in the hand-written `assets/base.css`.
4. Run `python scripts/compile_system.py`, then `python scripts/sync_examples.py`.
5. Run `python scripts/check_system.py` and `python scripts/visual_baseline.py diff`.

The compiler generates `assets/generated/recipes.css`, `system/resolved-recipes.json`, the
self-contained bundle, the Python bridge, and the reference table. Do not edit these outputs.
Adding a stable catalog pattern also requires a connected recipe; migration never influences routing.

Compilation fails on missing/orphaned recipes, a recipe pointing at another spec, missing slot
bindings, unknown or conflicting fragments, a selector absent from its example, an unbound variable,
or CSS that no longer consumes its recipe value. Bindings deliberately accept only tag/class
compounds and descendant spaces; pseudo-selectors and other advanced behavior remain in CSS.

This is **fragment-level migration**, with the complete pattern catalog covered. Responsive behavior,
pseudo-elements, content geometry, per-slide tuning and data-driven chart dimensions remain CSS
responsibilities. Render checks remain necessary: selector presence alone cannot establish appearance.
