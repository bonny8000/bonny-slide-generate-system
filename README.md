# Bonny Slide System

An intention-first agent skill for building bilingual **繁體中文 + English** UX and product decks —
as per-slide HTML, one scrolling HTML file, PDF, or PPTX.

You give it an audience and a source. It names what each page must **do**, looks that job up in a
compiled router instead of inventing a layout, builds from one shared stylesheet, and has to pass a
set of checks before it may hand anything over.

> **The detail is not here.** [`SKILL.md`](SKILL.md) is the operating manual, `specs/` holds the rules,
> and [`CHANGELOG.md`](CHANGELOG.md) holds the history. This file is the map.

---

## The pieces

```text
bonnyt/
|-- SKILL.md      # the operating manual the agent reads
|-- specs/        # THE DECISION LAYER — one file per rule, component, layout
|   |-- foundations/     # 14 rules: story, typography, colour, balance, imagery...
|   |-- components/      # 19 reusable parts
|   |-- layouts/         # 25 whole-slide structures
|   |-- content-map.md   # intention -> layout + components
|   |-- generated-*.md   # compiled — never hand-edited
|   `-- preferences.md   # 50 judged A/B rounds
|-- system/       # THE MACHINE LAYER — tokens, hypertokens, recipes, compiled router
|-- assets/       # THE BUILD LAYER — base.css + generated theme files
|-- scripts/      # the compiler + 12 checks
|-- examples/     # render-validated slides; reference only, never definitions
`-- pptx/         # python-pptx bridge from the same tokens
```

`specs/` decides. `system/` is the machine-readable truth. `assets/` builds. Generated files are
overwritten by the compiler — `--check` fails first if anything drifted.

---

## How a deck gets built

![Decide what the page must do before what it looks like](assets/readme/02-build-pipeline.svg)

1. **Frame** — audience, one theme, the source, and any **real** assets. A missing screenshot changes
   which layouts are eligible.
2. **Plan** — one claim and one intention per page. No components yet.
3. **Route** — write the normalised line, then look it up.
4. **Build** — `assets/base.css` classes and one theme file. Token names only, never a raw colour.
5. **Gate** — render, measure, look, fix the weakest page, repeat.

### One page, end to end

```text
意圖: let the room meet the real users and what stops them
形狀: quote+illustration / grid / few
```

That line resolves in `system/router.json` to `persona-cards` → components `persona`,
`level-slider`, `chip`, `quote-bubble` → built with `.pcard` / `.pavatar` / `.qbubble` / `.hbar` →
rendered and measured. The spec says *why* that anatomy works, so the arrangement is not a guess.

![The rendered persona page](examples/case-study/_preview/04.png)

---

## Two modes

![The skill does two different things](assets/readme/01-modes.svg)

Asking for a deck **reads** the router. Saying **"training / 訓練"** with reference slides **writes**
to it. If an image arrives with no instruction, the agent asks which is meant.

![A pattern the planner cannot reach does not exist](assets/readme/10-learning-loop.svg)

A training run changes `specs/` and never outputs a slide. Taste is learned the same way — two
defensible variants, judged by a person, distilled into principles.

---

## Routing

![Routing is a lookup, not a guess](assets/readme/03-router.svg)

Every spec declares what it is FOR (`intent`), what the slide holds
(`material` / `arrangement` / `item_count`), and what phrasing should summon it (`triggers`). The
compiler turns all of it into one index. A pattern that falls out of the index fails the build.

![Two questions choose the layout](assets/readme/08-two-axes.svg)

Triggers are multilingual (繁中, English, Korean) because intention does not change with the language
it is written in. Output language is separate, enforced at render time.

When more than one candidate survives, [`layout-choice.md`](specs/foundations/layout-choice.md)
decides in a fixed order: **availability → fit → variety → intent proximity.**

---

## The layer stack

![Only the top layer gets to choose anything](assets/readme/09-layer-stack.svg)

Intention picks the form. Nothing below it gets a vote.

`base.css` is the one deliberate exception — hand-written, because it is a usage contract, not
codegen. Examples carry the shipped stylesheet rather than a copy, so they cannot drift behind the
specs they demonstrate.

---

## Illustration decisions

![Native evidence and generated editorial explainer routes](assets/readme/07-illustration-routing.svg)

Every page records an explicit decision. Tables, data and detailed UI evidence stay native and
inspectable. Dialogue, workshops, workflows and scattered-input transformations route to a freshly
generated explainer in one of four compositions:

| Variant | For |
|---|---|
| `agenda-dialogue` | Workshop timing, rules, grouping, voting |
| `guided-dialogue` | Human/assistant worked examples, approval loops |
| `workflow-transform` | People, roles or tools converging into one outcome |
| `ui-qa` | A real supplied interface explained in conversation |

Reuse, tracing and CSS recreation all fail. If generation is unavailable, the build stops.

---

## Checks

![Measured by a machine, then looked at by a person](assets/readme/06-gates.svg)

| Command | Catches |
|---|---|
| `validate_layout.py` | unstyled render, dead bands, stretched container, wrong language, deck with no visual moment |
| `validate_editorial_explainer_plan.py` | a page that skipped its explainer; missing provenance |
| `validate_generated_illustration.py` | wrong ratio or grayscale output |
| `compile_system.py --check` | token and routing drift; a pattern with no route |
| `sync_examples.py --check` | an example carrying stale CSS |
| `verify_rebuild.py` | a pattern not rebuildable from `base.css` |
| `visual_baseline.py diff` | visual change nobody intended |
| `validate_routing.py` | a request that no longer reaches the right layout |
| `check_antipatterns.py` | a known-bad slide that started passing |
| `check_style_rules.py` · `calibrate_gate.py` | taste drift — **advisory** |

Routing scores **30/30** on the fixture it was tuned against and **8/10** on the held-out one. The
second is the real one.

**A pass is a floor, not a verdict.** Three times a change cleared every gate and looked worse. The
gates cannot tell you whether a slide is good — look at the render.

---

## Getting started

The repository root *is* the skill; `SKILL.md` carries the frontmatter.

```bash
git clone https://github.com/bonny8000/bonny-slide-generate-system.git ~/.claude/skills/bonny-slide-system
```

Needs **Python 3.9+** (standard library only) and a **Chromium browser** for the render gates.
`pptx/` additionally needs **python-pptx**; generated explainers need an image-generation tool.

Then just ask — it will come back for the audience, the theme and any real assets before starting.

```bash
python scripts/validate_layout.py DECK.html
```

```bash
python scripts/compile_system.py --check
```

For linked HTML use `assets/base.css`. For self-contained HTML inline
`assets/generated/base-bundle.css` plus **exactly one** `assets/tokens-*.css` theme.

---

## At a glance

| | |
|---|---:|
| Foundation rules · components · layouts | 14 · 19 · 25 |
| Routable patterns · indexed triggers | 44 · 313 |
| Themes (one per deck, one accent) | 2 |
| Example files | 172 |
| Judged A/B rounds | 50 |
| Hypertokens · recipes · explainer variants | 5 · 3 · 4 |
| Scripts | 13 |

---

## Glossary

| Term | Meaning |
|---|---|
| **Intention** | What a page must DO to the room. The only thing that selects a form. |
| **Shape** | `material / arrangement / item_count` — what the slide actually holds. The decisive routing axis. |
| **Trigger** | A phrase, in any of three languages, that summons a pattern. |
| **Router** | `system/router.json` — the compiled index. A pattern not in it does not exist. |
| **Recipe · hypertoken · token** | Slots → implementation fragment → the active theme's value. |
| **Hard candidate** | A page whose content presumptively needs a generated explainer. |
| **Gate** | A command that can fail a build. |

---

**v12.18 · August 2026** — routing keys on intention *and* content shape; triggers are multilingual
because intention is language-independent; layout choice, asset policy and illustration triggering are
declared data rather than judgement.
