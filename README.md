# Bonny Slide System

An intention-first agent skill for building bilingual **Traditional Chinese + English** UX and product decks.

Think of `specs/` as the decision engine, `system/` as the machine-readable design logic, and `assets/`
as the build layer. The agent names what each page must DO, looks that intention up in a compiled router,
builds the page from the shared stylesheet, and has to clear four blocking checks before delivery.

![The skill does two different things](assets/readme/01-modes.svg)

Asking for a deck **reads** the router. Saying **“training / 訓練”** and sending reference slides **writes**
to it — a learned pattern is not finished until the planner can actually reach it.

![Decide what the page must do before what it looks like](assets/readme/02-build-pipeline.svg)

## What This Repository Contains

- `SKILL.md` is the agent operating manual and release history.
- `specs/` contains the foundations, themes, components, layouts, intention map, audit, and learned preferences.
- `system/` contains canonical tokens, hypertokens, recipes, and strict JSON schemas.
- `assets/` contains the component CSS, generated bundles, theme outputs, and illustration references.
- `scripts/` contains the deterministic compiler, prompt builder, and validation tools.
- `examples/` contains render-validated slides and short deck sequences. They are **reference only** —
  every one carries the shipped stylesheet, never its own copy, so an example can never teach a rule
  the specs have already superseded.
- `pptx/` contains the python-pptx bridge built from the same token source.

The core rule is simple: **decide what the slide must do before deciding what it should look like**.

## Current Shape

| Area | Current count | Notes |
|---|---:|---|
| Foundation rules | 13 | Story, typography, imagery, colour, balance, audit, learning, and source sync |
| Stable components | 19 | Reusable evidence, metric, comparison, UI, quote, and support patterns |
| Stable layouts | 25 | Whole-slide structures selected by communicative intention |
| HTML examples | 162 | Individual examples, audit builds, and short deck sequences |
| Preference rounds | 50 | Render-tested A/B choices distilled into transferable principles |
| Hypertokens | 5 | Reusable surface, type, layout, and image implementation fragments |
| Pilot recipes | 3 | Slot mappings for metric cards, evidence cards, and feature showcases |
| Editorial variants | 4 | Workshop, guided dialogue, workflow transformation, and real-UI Q&A |
| Routable patterns | 44 | Compiled from spec frontmatter into `system/router.json` + `specs/generated-router.md` |
| Enforcement gates | 6 | Token/routing drift, example staleness, illustration provenance, rendered layout balance, render fingerprints, and intention routing |

## Routing

![Routing is a lookup, not a guess](assets/readme/03-router.svg)

Each spec declares what it is FOR (`intent`), what material the slide holds (`material` /
`arrangement` / `item_count`) and what phrasing should summon it (`triggers`). The compiler turns all
of it into a single index, so choosing a layout is a lookup rather than a judgement call made afresh
each time — and a pattern that falls out of the index fails the build rather than going quietly missing.

**Routing keys on two axes, and the second is the decisive one.** Measured on this library, the
`intent` lines alone identify **13 of 25** layouts: several pairs share a job and separate only on the
material they need. `idea-evidence` and `painpoint-evidence` both back a claim with evidence, one with
a chart and one with participant quotes; `hero-radial` and `linked-circles` both arrange concepts, one
as a centre with satellites and one as a continuum. The shape triple alone identifies **24 of 25**, so
shape decides and intent breaks the remaining tie.

Before any lookup the planner writes one normalised line — `意圖: … · 形狀: material / arrangement /
count` — derived from the content actually in hand rather than the layout being hoped for. On held-out
requests that took routing from 4/10 to 8/10, with nothing left unresolved.

Triggers are deliberately multilingual (繁中, English, Korean). **Intention does not change with the
language it is written in**, and much of this library was learned from Korean reference decks, so
deleting that vocabulary deleted recognition rather than risk. Output language is a separate concern,
enforced at render time by `validate_layout.py --lang`.

Where the router leaves more than one candidate, `specs/foundations/layout-choice.md` decides in a
fixed order — **availability → fit → variety → intent proximity**. Availability is a hard filter: a
layout needing a real screenshot the user has not supplied is disqualified rather than faked, while a
missing *illustration* is a routed decision to generate one. Fit outranks variety, because a repeated
layout that fills the page beats a fresh one that starves it.

## What Is Enforced

![Rules that are only prose degrade first](assets/readme/06-gates.svg)

Rules that exist only as prose degrade first, so the ones that can be measured are checked by a
command rather than by good intentions:

```bash
python scripts/compile_system.py --check    # token + routing drift; a pattern with no route fails
python scripts/sync_examples.py --check     # an example carrying its own stale copy of the CSS fails
python scripts/validate_layout.py DECK.html # renders the slide and measures balance and density
python scripts/verify_rebuild.py            # can each pattern be rebuilt from base.css alone?
python scripts/visual_baseline.py diff      # did anything change visually that was not meant to?
python scripts/validate_routing.py          # does a real request reach the right layout?
```

**What they catch:** a layout with no route, a trigger the planner can never match, a blank or
unstyled render, a dead band inside the content, a stretched container, copy in a language the deck
did not declare, raw colour outside the token layer, and a deck of 8+ slides with no visual moment.

`validate_routing.py` runs two fixtures and the gap between them is the point. The working set scores
30/30 because triggers were sharpened against it, which makes that number nearly meaningless; the
held-out set was written afterwards without consulting any trigger list and scores **8/10**. Trust the
held-out one, and if you ever tune against it, it is spent — write a new one.

**What they do not catch:** whether the slide is any good. Three times now a change has passed every
gate and looked worse — most recently a card layout that went FAIL to pass at 34% whitespace with its
label, title and body flung to the card's extremes. A pass bought that way is worth less than the
failure. Both blind spots are documented: the emptiness checks scan rows across the whole canvas, so a
card inflated in one column can hide behind a neighbouring column's text; and the routing score is a
lexical lower bound, since the agent matches semantically and will do better. Treat a pass as a floor,
not a verdict, and look at the render.

Where content genuinely does not fill the canvas, no gate setting fixes it and neither does geometry —
growing figures, stretching rows and re-anchoring the page were all measured and all reverted. What
works is composition: bring the header down against its content so the two read as one block and let
the leftover become even margin. That took the balance gate from 15 failures to 7.

## System Structure

![Hand-write one column, compile the rest](assets/readme/04-source-of-truth.svg)

Only the left column is written by hand; the router, the class manifest and every CSS output are compiled
from it.

![Examples demonstrate patterns, they never define them](assets/readme/05-examples-are-reference.svg)

`examples/` carries the shipped stylesheet rather than a copy of it, so an example can no longer drift
behind the specs it is supposed to demonstrate. The layers have different responsibilities:

- **Decision layer:** `slide-plan.md` names one claim and one intention per page; `content-map.md` selects
  the layout and components.
- **Design layer:** foundations, themes, components, layouts, and the preference library define what
  good work means.
- **Implementation layer:** recipes connect component slots to hypertokens; hypertokens resolve semantic
  token values into reusable CSS fragments.
- **Output layer:** the compiler produces CSS, a PPTX token bridge, and an LLM-readable reference.

Hypertoken migration status has no selection weight. The full component and layout catalogue remains
available, and intention continues to choose the form.

## How the Workflow Works

1. Confirm the audience, room, source, theme, and required real assets.
2. Turn the source into a complete page plan with one claim and one intention per slide.
3. Order the reasoning before the conclusion and place covers, section breaks, and bridges.
4. Record every slide in `illustration-plan.json`, including the trigger, gate, reason, and any precision override.
5. Use `content-map.md` to select the visual route, layout, and components.
6. Build with `assets/base.css`, one theme, semantic tokens, recipes, and hypertokens.
7. Generate a fresh editorial explainer when the gate requires one.
8. Render the deck, inspect balance and density, correct the weakest page, and repeat until the audit passes.

The same source can produce a different slide when the audience job changes:

| Intention | Typical signal | Selected form |
|---|---|---|
| Teach how to use a product | A real screen with spatial steps | Annotated screenshot |
| Explain a people-and-tool hand-off | Roles and tools converge into one outcome | Generated workflow transformation |
| Prove impact | A precise metric, table, chart, or evidence | Native, inspectable data layout |
| Help the room choose | Options compared against shared criteria | Comparison table |
| Re-orient the audience | A new chapter or major change of topic | Section cover |

## Illustration Routing

![Native evidence and generated editorial explainer routes](assets/readme/07-illustration-routing.svg)

Every page receives an explicit illustration decision. Human/assistant dialogue, workshop facilitation,
multi-tool hand-offs, and scattered inputs becoming shared intent are hard candidates for a newly generated
editorial explainer. Tables, code, dense comparisons, data, and detailed UI evidence stay native and inspectable.

Generated explainers are not CSS diagrams or reused reference artwork. The system requires:

- a fresh built-in image-generation call;
- one sanctioned composition variant;
- the exact target aspect ratio;
- a local asset with generator provenance;
- native, editable copy zones; and
- plan and HTML validation before delivery.

| Variant | Best used for |
|---|---|
| `agenda-dialogue` | Workshop timing, rules, prompts, grouping, voting, and discussion |
| `guided-dialogue` | Human/assistant worked examples, approval loops, and agent-assisted operations |
| `workflow-transform` | Scattered viewpoints, people, roles, or tools converging into one shared outcome |
| `ui-qa` | A real supplied interface explained through participant/assistant conversation |

If generation is required but unavailable, the build stops instead of quietly falling back to native cards.

## Hypertokens

Tokens carry semantic values. Hypertokens turn those values into reusable implementation fragments such as
`surface.card`, `text.heading`, and `image.floating`. Recipes attach the fragments to component slots:

```json
"metric-card": {
  "slots": {
    "root": ["surface.card", "layout.stack.card"],
    "supporting": ["text.supporting"]
  }
}
```

The separation is deliberate:

- intention selects the layout or component;
- recipes describe its slots;
- hypertokens provide reusable visual behaviour;
- tokens resolve the active theme; and
- the compiler generates consistent implementation outputs.

## Quality Gate

A deck is complete only when the rendered pages pass the system:

- one theme and one chromatic accent;
- Traditional Chinese primary, with supporting English;
- one claim per slide;
- a complete illustration plan with valid provenance;
- no silent downgrade of hard candidates;
- balanced whole-page composition and readable density, measured on the rendered pixels;
- no visual drift against the recorded render fingerprints;
- at least one or two genuine visual moments in decks of eight or more pages; and
- re-rendered evidence that the weakest page has been corrected.

## Directory Map

```text
bonnyt/
|-- SKILL.md              # agent operating manual
|-- README.md             # GitHub-facing system overview
|-- specs/                # rules, themes, components, layouts, intention map, audit and preferences
|-- system/               # canonical tokens, hypertokens, recipes and JSON schemas
|-- scripts/              # compiler, prompt builder and validators
|-- assets/               # component CSS, generated bundles, themes and illustration references
|-- examples/             # render-validated slides and complete short-deck examples
`-- pptx/                 # python-pptx bridge using the same token system
```

`specs/` is the source of truth for design rules and selection logic. `system/*.json` is the source of
truth for machine-readable tokens, hypertokens, and recipes. Generated files must not be edited by hand.

## Compile and Validate

```powershell
python scripts/compile_system.py
python scripts/compile_system.py --check
```

For a deck that uses editorial explainers:

```powershell
python scripts/validate_editorial_explainer_plan.py illustration-plan.json DECK.html
```

Use `assets/base.css` for linked HTML. For self-contained HTML, inline
`assets/generated/base-bundle.css` plus exactly one `assets/tokens-*.css` theme.

---

**v12.12 · August 2026** — routing now keys on intention *and* content shape, measured rather than
assumed; triggers are multilingual because intention is language-independent; layout choice, asset
policy and illustration triggering are declared data rather than judgement; UI mockups are measured in
device points; and every claim in this file is backed by a number some check produced.
