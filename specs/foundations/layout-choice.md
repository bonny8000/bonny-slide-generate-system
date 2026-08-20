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
| `build` | needs a **ui-mockup**: draw it in-system, no asset required and none to ask for |
| `generate` | needs an **illustration**, and one may be generated if the user did not supply it |
| `must-supply` | needs a real **ui-screen**, and it may **never** be produced |

**Three cases, and the middle one is the one that gets collapsed by mistake.**

A **`ui-mockup` is not a screenshot.** It is a schematic screen drawn from the primitives `base.css`
already ships — `.phone`, `.mock`, `.appframe`, and `.sk` skeleton bars — following
`components/ui-mockup.md`: real labels only on headers that matter, skeleton bars everywhere else,
one `--accent` on the single active element, no invented data. It costs nothing, always matches the
theme because it is drawn from tokens, and it is what makes an as-is/to-be or a feature walkthrough
vivid instead of abstract. **Never disqualify a layout for lacking one, and never ask the user to
supply one.** Build it.

An **`illustration`** the user did not supply is not a blocker either, it is a job — see *Missing
illustrations trigger generation* below.

A **real `ui-screen`** is the one thing that may never be produced. A fabricated screenshot of a real
product is a false record of that product, which `generated-editorial-explainer.md`'s `ui-qa` route
forbids outright. This applies only where the deck's claim is about *the actual product UI*. If the
user has not supplied it, the candidate is **disqualified** — and note that a schematic `ui-mockup`
is not a substitute here, because the whole point of that route is that the screen is real.

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

Each layout declares `alternates`: layouts that do the **same job** and differ in the material or
emphasis they need. 12 of 25 have one; the rest are empty on purpose.

- `as-is-to-be` ↔ `problem-solution` — both contrast two states; one shows it in screens, the other
  in words.
- `qual-quant-split` ↔ `painpoint-evidence` — both prove a finding; one needs numbers beside the
  quotes, the other runs on quotes alone.
- `use-case-cards` ↔ `persona-cards` — both answer "who is this for", at different resolution.

**Alternates are hand-declared, and the reason is worth keeping.** They were first derived
automatically from a shared `arrangement`, which produced substitutes that were structurally similar
and semantically absurd: `keyword-cards` was offered as a stand-in for `use-case-cards` because both
are grids of a few cards — one states design principles, the other shows who the product serves.
Laying a page out the same way does not make two layouts interchangeable.

**An empty list is an answer, not a gap.** Where nothing genuinely substitutes, the correct move is
to go back to the user — ask for the missing screenshot, or ask whether to cut the page — rather than
force a layout that does a different job and hope the content bends to fit.
