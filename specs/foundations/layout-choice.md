# Choosing between candidate layouts

The router narrows a page to one layout most of the time. When it narrows to two or more, this is how
to choose — and the order of the rules matters more than any single rule.

Machine form: `selectionPolicy.tieBreak` in `system/router.json`, compiled from here.

## The order

### 1. Availability — can this layout's material exist at all?
Every layout declares `material`, and from it an `assetNeed` and an `assetPolicy`.

| assetPolicy | meaning |
|---|---|
| `none` | text, charts, stats, quotes — build it from content you already have |
| `generate` | needs an **illustration**, and one may be generated if the user did not supply it |
| `must-supply` | needs a **ui-screen**, and it may **never** be generated |

**A `ui-screen` cannot be invented.** A fabricated screenshot of a real product is a false record of
that product, which `generated-editorial-explainer.md` forbids outright and which no deadline
justifies. If the user has not supplied the screen, this candidate is **disqualified** — drop it and
take the next one. Do not substitute a CSS mockup, a traced redraw, or a generated image.

An `illustration` is the opposite case: a missing one is not a blocker, it is a job. See
*Missing illustrations trigger generation* below.

### 2. Fit — does the content actually fill this layout?
Prefer the candidate whose `itemCount` matches how many items you really have.

- `one` · `pair` · `few` (2–4) · `many` (5+)
- Three items in a `many` layout **starves** the slide: thin content stretched over a wide frame.
- Seven items in a `pair` layout **overflows** it, or shrinks type past the floor to fit.

This is not a matter of taste. It is the same defect `validate_layout.py` measures after the
fact — dead bands, stretched empty surface, quadrant imbalance. Choosing for fit is how you avoid
failing that gate rather than fighting it afterwards.

### 3. Variety — has this deck already used it?
Among candidates that survived 1 and 2, prefer one this deck has not used yet. Two identical layouts
back to back read as a template rather than an argument, and a deck that runs one pattern eight times
teaches the audience to stop looking.

**Variety never outranks fit.** A repeated layout that fits the content beats a fresh one that
starves it. Reaching for novelty at the cost of a well-filled page is the more common mistake and the
more visible one — the audience sees a thin slide immediately and never notices that the layout also
appeared four pages ago. Rule 2 is a quality floor; rule 3 is a preference above it.

Deck-wide rhythm still matters (`foundations/storytelling.md`): alternate dense and open pages so the
deck breathes. That is served by rule 3, not by overriding rule 2.

### 4. Intent proximity
If two candidates still tie, take the one whose `intent` line is closest to the page's job. This is
the last rule, not the first, because intent alone identifies only 13 of 25 layouts — the twins
(`keyword-cards` vs `terminology-cards`) are exactly the cases that reach this far.

## Missing illustrations trigger generation

When the chosen layout's `assetPolicy` is `generate` and the user supplied no artwork, that is a
**decision the router has already made for you**: the page needs an illustration, so raise it as a
`gate: yes` record in `illustration-plan.json` with the trigger noted as `material:illustration`, and
follow the generator workflow in `foundations/generated-editorial-explainer.md`.

Do not quietly downgrade the page to a text-only layout to avoid generating. That converts a routing
decision into a silent visual compromise, and it is how decks end up uniformly flat.

**Pages that never need one**, regardless of material: covers, section covers, bridges, agenda pages,
and closing/appreciation pages. Their job is punctuation, not explanation, and an illustration on
them competes with the one thing they exist to say. Record them as `gate: no` with the reason
`structural-page` — an omitted decision is still a build error.

## Falling back

Each layout carries `alternates`: the other layouts that share its `arrangement`. They lay the page
out the same way and differ in the material they need, which makes them the right fallback when
rule 1 disqualifies your first choice.

- No screenshots? `as-is-to-be` → `problem-solution` (both `opposed`).
- No illustrations and generating is not wanted? `use-case-cards` → `feature-grid` or
  `keyword-cards` (all `grid`).

Some layouts have no alternates — `product-hero` is the only `hero` arrangement in the library. When
its material is unavailable there is nothing to fall back to, so **ask the user for the screenshot**
rather than inventing one or forcing an unrelated layout.
