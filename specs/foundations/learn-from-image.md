---
id: learn-from-image
kind: foundation
status: stable
---
# Learn from a slide image — the harness loop that makes the system smarter

The user keeps sending **reference slide images**. Each one is a chance to grow the library. Because
**color is a separate theme layer** (`foundations/color-discipline.md`, `foundations/themes-and-modes.md`),
a slide's *structure* and its *color* are independent — so you can learn the **layout + components**
from any image and they stay **theme-agnostic and reusable** under every theme. This is the front-end
of the same learn loop as `foundations/source-sync.md` (real decks → system), now extended to
**real slide images → system.**

## Entering this loop — training mode
The user triggers this deliberately by saying **"training"** (or 訓練), or by sending reference slides
with the intent to teach rather than to get a deck. `SKILL.md` routes that to here. The output of a
training run is a **change to `specs/`**, never a slide.

A learned pattern only counts once the planner can reach it, so a training run is not finished until:
- the spec carries `intent` + `triggers` frontmatter (the router in `system/router.json` is compiled
  from these — a spec without them is invisible to routing)
- `specs/_catalog.md` and `specs/content-map.md` both have a row, keyed on **intention**
- `example:` points at a render-validated file
- any CSS the pattern needs is in **`assets/base.css`**, not only in the example — otherwise it lands
  in `specs/generated-class-coverage.md` as a gap and has to be reinvented on every future build
- `python scripts/compile_system.py --check` passes

## The one discipline: learn STRUCTURE, not COLOR
When you read an image, extract the skeleton — slots, nesting, grid, spacing rhythm, type roles,
emphasis, icon use. **Record colors only as token *roles*** (accent / ink / muted / surface), never as
hex or px. The audit rejects raw color in a spec. A pattern that bakes in a specific color is not
reusable; a pattern expressed in token names renders in any theme.

## What to extract from each image (don't stop at "what it looks like")
The goal is to learn *why the slide works*, so the system can reuse the thinking — not just the pixels.
For every image, read out all five:
1. **Intention — the job.** What is this slide trying to *do* to its audience? (persuade, teach, compare,
   prove impact, build trust, orient, provoke, re-orient.) This is the most important thing to capture.
2. **Trigger — the reverse map.** What raw content or situation *should make you reach for this layout
   next time*? Imagine the input that this pattern is the right answer to. This becomes/updates the
   `triggers` in the spec and a row's detection in `content-map.md`.
3. **Layout logic.** How the layout organizes the page to serve the intention: the reading path, what's
   emphasized, the hierarchy, how it paces against neighboring slides.
4. **Component craft.** For each component, *how it's shown* — the rendering technique (e.g. one active
   bar in accent while the rest are muted; a donut with the number in the hole; before/after as paired
   bars) — expressed in token roles, not colors.
5. **Intention ↔ component rationale.** **Why these components, in this arrangement, achieve that
   intention.** (e.g. "one accent bar = the eye lands on the single number that proves impact"; "O/X grid
   = lets the audience compare at a glance so they can choose.") This rationale is the learning that makes
   the system smarter — record it in the spec's *Intention & rationale* section.
6. **Imagery handling.** How does the slide treat images — device/UI mockup, background fill, a recolored
   illustration set, a stock-person illustration, an annotated screen, a brand logo, or a real photo?
   Record the technique and how it stays on-palette (`foundations/imagery.md`). Note whether the page
   relies on a real asset you'd ask the user to supply.

## The loop (run on every image)
1. **Name the shape.** What content shape is this? Cross-check `content-map.md`. If it's a shape with
   no row there, that's a signal you may be learning something new.
2. **Decompose.** Separate the **layout** (organism: the full-slide pattern) from the **components**
   (atoms/molecules inside it). List each slot and how it nests — colors excluded.
3. **Dedupe against `_catalog.md`.** Decide which case this is:
   - **Already `stable`** → just add the image to its `learned_from`. Nothing to build.
   - **A `todo`** → this image is your source; write the spec now (`spec-template.md`) and flip it to
     `stable`.
   - **A variant** of an existing pattern → add a *Variant* to that spec, don't create a new one.
   - **Genuinely new** → create a new spec via `spec-template.md`.
4. **Write it theme-agnostic, with the reasoning.** New spec uses **token names only**; fill `intent`
   and `triggers` in the front-matter and write the **Intention & rationale** section (why these
   components achieve the job — extraction #5). Add a class to `assets/base.css` (or inline CSS in the
   spec example) and a rendered `examples/*.html`. Map every observed color to a token role.
5. **Register & make it reachable.** Update `_catalog.md` (id, what it is, `learned_from: ImgN`, status).
   Add/refresh a `content-map.md` row keyed on the **intention** (job) and **triggers**, so next time
   content with that intention appears, the planner reaches straight for this layout.
6. **Audit + sync.** Run `specs/audit.md` on the new spec/example (no raw color, tokens exist, example
   renders). This closes the loop per `foundations/source-sync.md`.

## Naming learned sources
Continue the `ImgN` convention used in `_catalog.md` (`Img1`–`Img12` mined the v1 library). New images
become `Img13`, `Img14`, … in `learned_from`, so every pattern stays traceable to the slide it came from.

## Why it compounds
Each pass adds one reusable, theme-agnostic pattern **plus the reasoning that selects it** — the planner
(`slide-plan.md`) names an intention, the mapper (`content-map.md`) matches that intention to a layout,
and the spec explains why its components do the job. More images → a denser intention→layout map and a
richer rationale library → the system recognizes what a slide is *for* and builds better slides on its
own. That is the harness loop: not memorizing pictures, but learning the relationship between intention
and the components that serve it.
