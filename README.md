# Bonny Slide System

An intention-first agent skill for building bilingual **繁體中文 + English** UX and product decks —
as per-slide HTML, one scrolling HTML file, PDF, or PPTX.

> **The detail is not here.** [`SKILL.md`](SKILL.md) is the operating manual, `specs/` holds the rules,
> [`CHANGELOG.md`](CHANGELOG.md) holds the history. This file is the map.

---

## Why it exists

Ask two people to lay out the same research finding and you get two slides. Ask the same person twice,
a month apart, and you still get two slides. The layout gets chosen by whatever felt right that day,
so a deck drifts away from itself page by page.

This system takes that decision away from the moment. Each page has to state **what it must do** before
anything is drawn, and that statement is looked up in a compiled index. Same job, same layout — every
time, in any deck.

---

## How it works

![From an ask to a deck, in five moves](assets/readme/fig-01-architecture.svg)

*You bring the content; the planner names the job; the router — not the agent's taste — returns the
layout. The gate can send it back. All three middle stages read from one compiled source, so none of
them can quietly invent something.*

---

## One slide's life

![What actually gets passed around](assets/readme/fig-02-lifecycle.svg)

*The routing moment is the whole design: a page arrives as an intention plus a shape, and leaves as a
named layout. Everything before it is planning, everything after is construction. The failure at the
bottom is the normal case, not the exception — the gate measures rendered pixels, so a starved page
comes back before anyone sees it.*

---

## What it builds

![Every part of this page was chosen, not styled](assets/readme/fig-03-anatomy.png)

*One page of a ten-page case study. The layout, its components and every colour trace back to a
decision recorded somewhere in `specs/` — which is why the other nine pages look like they belong to
it. The full deck is in [`examples/case-study/`](examples/case-study).*

---

## How a layout gets chosen

![Two questions choose the layout](assets/readme/08-two-axes.svg)

*Both questions are asked, but the content question does most of the work. Two layouts can share a job
and differ only in whether the evidence is a chart or a quote — so the job alone cannot separate them.*

When more than one candidate survives both questions,
[`layout-choice.md`](specs/foundations/layout-choice.md) decides in a fixed order:
**availability → fit → variety → intent proximity.** A layout needing a screenshot nobody supplied is
dropped rather than faked; a repeated layout that fills the page beats a fresh one that starves it.

Triggers are multilingual — 繁中, English, Korean — because an intention does not change with the
language it is written in. What language the deck comes out in is a separate decision, enforced when
it renders.

---

## Why every deck looks like the same system

![Only the top layer gets to choose anything](assets/readme/09-layer-stack.svg)

*Selection happens once, at the top. Below it, nothing has an opinion — a component cannot decide it
wants a different colour, because the only colour it knows is the name of a token.*

---

## When a page needs a picture

![Native evidence and generated explainer routes](assets/readme/07-illustration-routing.svg)

*Tables, data and real UI stay native and inspectable. Dialogue, workshops and workflows become a
freshly generated illustration — never reused artwork, never a diagram traced in CSS.*

| Variant | For |
|---|---|
| `agenda-dialogue` | Workshop timing, rules, grouping, voting |
| `guided-dialogue` | Human/assistant worked examples, approval loops |
| `workflow-transform` | People, roles or tools converging into one outcome |
| `ui-qa` | A real supplied interface explained in conversation |

If generation is required but unavailable, the build stops. It does not quietly fall back to text.

The same rule applies to product UI shown inside a device or app frame: the frame is only the chrome;
the **screen interior** has to read as a real screen. [`examples/light-screen-interiors.html`](examples/light-screen-interiors.html)
is the reference page for this vocabulary — app bars, list rows, toggles, sheets and popups are built
from the system tokens and scaled with the mock device, rather than pasted in as arbitrary screenshots.

![Light mobile and website frames using the same token-scaled screen interior](https://raw.githubusercontent.com/bonny8000/bonny-slide-generate-system/4dd9e81/assets/readme/fig-04-screen-interior-light.svg)

*The frame tells you what contains the UI; the interior tells you what product screen the audience is
looking at. The interior is made from the same vocabulary as the deck — app bar, list rows, toggles,
popups and sheets — so it remains legible and coherent when the mockup changes size.*

---

## What changed recently

The latest work tightened the system in two places that are easy to miss in a static README:

- **Reference UI interiors.** A new self-contained example shows how the inside of a phone or app mockup
  is constructed, including device-relative type and spacing. It keeps the product surface legible while
  preserving the slide system's own theme and rounded, lightly lifted image treatment.
- **A trustworthy antipattern gate.** `check_antipatterns.py` now uses validator exit codes instead of
  scraping console text: `0` means every known-bad fixture is still rejected, `1` means a fixture leaked,
  and `2` means the checker could not run. Browser/render crashes and timeouts are therefore reported as
  **cannot run**, not mistaken for either a passing gate or a leaked layout. Chrome discovery now covers
  macOS app bundles as well as Linux paths.

  The frozen fixtures and their maintenance rules live in [`specs/gate-antipatterns/README.md`](specs/gate-antipatterns/README.md).

---

## What it refuses to ship

![Measured by a machine, then looked at by a person](assets/readme/06-gates.svg)

*The machine catches what it can measure. It cannot tell you a slide is good — three times a change
passed every check and still looked worse.*

| Checks | Catch |
|---|---|
| `validate_layout.py` | an unstyled render, dead bands, a stretched container, the wrong language, a long deck with no visual moment |
| `validate_editorial_explainer_plan.py` · `validate_generated_illustration.py` | a page that skipped its illustration, missing provenance, the wrong ratio |
| `compile_system.py --check` · `sync_examples.py --check` | token or routing drift, a pattern with no route, an example carrying stale CSS |
| `validate_routing.py` · `verify_rebuild.py` · `visual_baseline.py` | a request that stopped reaching the right layout, a pattern that cannot be rebuilt, a visual change nobody intended |
| `check_antipatterns.py` | a known-bad slide that started passing, or a gate that could not run |

Routing scores **30/30** on the fixture it was tuned against and **8/10** on a held-out one written
afterwards. The second is the real number.

---

## How it gets better

![A pattern the planner cannot reach does not exist](assets/readme/10-learning-loop.svg)

*Send reference slides with **"training / 訓練"** and the system grows instead of producing a deck. It
reads a reference for structure, never colour, so a learned pattern works under any theme. Taste is
learned the same way — two defensible variants, judged by a person, distilled into a principle.*

---

## The repository

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
overwritten by the compiler, and `--check` fails first if anything drifted.

---

## Getting started

The repository root *is* the skill; `SKILL.md` carries the frontmatter.

```bash
git clone https://github.com/bonny8000/bonny-slide-generate-system.git ~/.claude/skills/bonny-slide-system
```

Needs **Python 3.9+** (standard library only) and a **Chromium browser** for the render checks.
`pptx/` also needs **python-pptx**; generated illustrations need an image-generation tool.

Then just ask for a deck — it will come back for the audience, the theme and any real assets before it
starts, because those decide which layouts are even eligible.

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

| | | | |
|---|---:|---|---:|
| Foundation rules | 14 | Routable patterns | 44 |
| Components | 19 | Indexed triggers | 313 |
| Layouts | 25 | Themes | 2 |
| Example files | 173 | Judged A/B rounds | 50 |
| Hypertokens · recipes | 5 · 3 | Illustration variants | 4 |

**Intention** — what a page must DO; the only thing that selects a form. **Shape** — material,
arrangement and count; what the page actually holds. **Router** — the compiled index; a pattern not in
it does not exist. **Token** — a colour's name, resolved by the one active theme.

---

**v12.18 + unreleased gate portability fix · August 2026** — routing keys on intention *and* content shape; triggers are multilingual
because intention is language-independent; layout choice, asset policy and illustration triggering are
declared data rather than judgement. Screen interiors now have a token-scaled reference; antipattern
checks distinguish rejected, leaked and unrunnable results.
