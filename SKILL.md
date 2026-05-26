---
name: bonny-slide-design
description: Use this skill to generate well-branded interfaces and assets for Bonny Slide System V2 — bilingual UX/product case-study slides with Traditional Chinese as the primary voice and English as supporting labels. Contains essential design guidelines, color and typography tokens, fonts, slide-template assets, ready-to-copy component HTML, and a JSX UI kit for prototyping. Use whenever Claude needs to create a 16:9 slide deck, redesign or critique an existing deck, build a design-system doc, or output agent instructions for choosing slide components, modes, typography, and layouts.
---

# Bonny Slide Design System — Skill

Read `README.md` in this skill first to understand the design direction (voice, visual foundations, iconography). Then explore the other files based on what you're being asked to make.

## Content → Component Decision Matrix

This is the **most important table in the skill**. Read the situation, find the row that matches, use those components. Never pick a layout for decoration; pick it for the content's job.

| If the content is… | Situation example | Primary component | Support components | Mode | Accent |
|---|---|---|---|---|---|
| **A project intro** | First slide of a deck — project name, role, year | Title block (centered or editorial-left) | Hero visual or product mockup, metadata chips | Light for research, dark for product/tech reveal | Blue (default) |
| **A section change** | "Now we move from research to solution" | Centered title block on full-bleed panel | Phase chip, progress line | Dark for climax, light for normal | Match next section's accent |
| **Background / context** | Why does this problem matter? Market size, trend | 3 evidence cards | Eyebrow + headline, source footer, small key band | Light | Blue |
| **Desk research** | External reports, market data | 3 evidence cards (one may be `card-accent-blue`) | Chart card, source labels | Light | Blue |
| **Survey numbers** | "52% find X confusing" | Chart card (left) + interpretation card (right) | Metric card, count chip | Light | Blue |
| **Interview voices** | What users said — patterns across people | 3 quote cards (`quote-card`) | Participant tags, `.highlight` on repeated phrase | Light for report, dark for emotional climax | Blue (light) / Green (dark) |
| **Pain points** | What blocks the user, with cause | 3 pain cards (`pain-card`) | Severity chip, avatar marker, quote snippet | Light with pink accent, or dark for emotional | Pink / red |
| **Synthesized finding** | "Users aren't unwilling — they lack confidence" | Insight panel (`insight-panel`) | Evidence note, implication line | **Dark** (preferred) | Green on dark, blue on light |
| **Problem → opportunity** | Bridge from research to solution direction | Problem-to-opportunity bridge | Key band, connector arrows, HMW chip | Light or mixed | Pink (pain) → Blue (opp) |
| **Current vs improved** | Before/after process, As-Is / To-Be | Comparison grid (`comparison-grid`) | State header, takeaway band | Light | Gray (as-is) + Green (to-be) |
| **Sequence / journey** | 3–5 steps in order | Workflow timeline (`timeline`) | Actor chips, stage cards | Light for ops, dark for product process | Blue or Green |
| **A product screen** | App feature walkthrough | Phone mockup + 2–3 annotations (`annotation-list`) | Feature stack, before/after mini-screen | Light for function, dark for walkthrough | Purple / Blue |
| **Feature set / MVP** | What gets built first — 3 pillars | Feature stack (`feature-stack`) | Priority chips, scope note | Light | Blue (one row highlighted) |
| **Outcome data** | What improved after launch | Metric card grid (result dashboard) | Before/after bars, quote proof, next-step band | **Dark** for executive, light for client report | Green (improvement) |
| **Market / segment map** | Positioning, who you're targeting | Positioning map (2×2 / scatter / venn) | Highlighted target segment, interpretation list | Light | Blue + Gray |
| **One memorable line** | Final takeaway, design principle, HMW | Key band (`key-band`) | Source/method tag | Light or dark | Blue (default) |
| **An appendix detail** | Raw table, source list, reference grid | Dense table or screenshot grid | Small title block, page marker | Light | Gray |

### Quick decider (when the matrix is overkill)

Apply this one-line test:

- Main evidence is a **number** → `metric-card`
- Main evidence is a user's **words** → `quote-card`
- Content is **wrong / blocked / painful** → `pain-card`
- Content is a **synthesized finding** → `insight-panel`
- Content shows **how something changes** → `comparison-grid`
- Content shows **steps in order** → `timeline`
- Content shows a **product screen** → `phone` + `annotation-list`
- Content lists **what will be built** → `feature-stack`
- Content shows **what improved** → `metric-card` grid (result dashboard)
- None of the above → `card card-pad` inside `grid grid-3` with `card-title` + `card-body`

Default to **3 cards in light mode** when uncertain. Always safer than inventing a new layout.

### Mode rule (light vs dark)

- **Light** = evidence, context, comparison, normal explanation, appendix. *Anything that needs to be calmly examined.*
- **Dark** = insight, emotional interview, solution reveal, product walkthrough, status map, executive result dashboard. *Anything that should feel like the climax of the story.*
- **Mixed** = one dark insight panel inside an otherwise light evidence slide, or one bright product UI card on an otherwise dark walkthrough slide. Use sparingly.

### Accent rule (one family per slide)

One semantic accent per slide unless you are explicitly comparing categories or actors. **Highlight only one phrase per headline.**

| Accent | Meaning | Example use |
|---|---|---|
| Blue (`--blue`) | Research, data, product clarity | Default for desk research, survey, feature explanation |
| Green (`--green`) | Improvement, success, service simplification | Result dashboards, to-be state, dark-mode eyebrow |
| Purple (`--purple`) | Social, motivation, friendly AI | Community features, AI agents |
| Orange / Yellow | Attention, study, warm service | Education, onboarding, attention slides |
| Pink / Red | Pain, friction, warning | Pain cards, current state in as-is |
| Gray | Baseline, inactive, current state | As-is in a comparison; inactive bars in a chart |

## When to load what

Always load:

- `README.md` — high-level direction, sources, caveats.
- `references/foundations.md` — canvas, grid, type, spacing, color, mode rules.
- `references/component-system.md` — every component's anatomy + when to use it.
- `references/component-html.md` — **required for any HTML output.** Copy-paste HTML snippets for every component. Never invent class names.

Load when relevant:

- `references/slide-recipes.md` — when building a multi-slide deck or mapping source material into slides.
- `references/agent-playbook.md` — when deciding how to classify content and report design choices.
- `references/source-analysis.md` — when explaining why the system looks the way it does.

## Workflow

1. **Classify** the request: single slide, full deck, redesign, template, or critique. Identify story type (UX research, product redesign, strategy report, portfolio case study, result report).
2. **Outline** each slide with intent label, one-sentence message, primary component, support components, mode (light/dark), accent color, required evidence.
3. **Choose components by intent** using `references/agent-playbook.md` Step 3 decision tree — evidence → evidence card; user voice → quote card; blocker → pain card; synthesis → insight panel; sequence → timeline; before/after → comparison grid; product behavior → phone + annotations; outcome → result dashboard.
4. **Compose** by copying the matching snippet from `references/component-html.md` into the `assets/templates/slide-template.html` shell. Link `assets/bonny-slide-v2-tokens.css`. Set `data-mode="light"` or `"dark"` on `.slide`.
5. **Mark languages.** Add `class="cjk"` to Traditional Chinese spans (思源黑體 / Noto Sans TC) and `class="latin"` to English / numbers / product names (Arial). CJK gets `letter-spacing: 0.10em`; Latin gets `0`. Do not mix in one span.
6. **Validate.** One dominant message per slide. Every claim has source/method/baseline. Highlight only ONE phrase per headline. No inline styles for color/font-size/font-weight/letter-spacing.

## When asked for visual artifacts (slides, mocks, prototypes)

- Copy assets out of this skill into the output directory; do not reference them with relative paths that escape the project.
- Default output: a single HTML file per slide, linked to `bonny-slide-v2-tokens.css`. Multiple slides → use `<deck-stage>` starter component to host them.
- Use real product screenshots for feature slides. If unavailable, leave a labeled placeholder rectangle — never hand-draw UI with SVG.
- Use Lucide icons via CDN when an icon is genuinely informational.

## When asked for production code

Copy `colors_and_type.css` for base tokens. The full slide-component classes in `assets/bonny-slide-v2-tokens.css` are slide-specific — adapt them, don't blindly ship them into a product app.

## If invoked without guidance

Ask the user:

1. Single slide, full deck, or design-system update?
2. Source material — research notes, transcript, PRD, screenshots, or existing deck?
3. Story type (research, redesign, strategy, portfolio, result)?
4. Primary language: Traditional Chinese is the default — confirm.
5. Output: HTML, PPTX, or Markdown spec?

Then act as an expert slide designer and produce the artifact following the workflow above.

## Hard rules

- Never use inline `style=""` for colors, font-size, font-weight, or letter-spacing. Only for per-slide layout overrides (`gap`, `padding-block-start`, `max-inline-size`).
- Never invent CSS class names. If a class is not in `assets/bonny-slide-v2-tokens.css`, do not use it.
- Never apply `data-mode="dark"` to `.frame` or inner elements — it goes on `.slide` only.
- Never use more than one accent family per slide unless comparing categories or actors.
- Never use `.highlight` on random words. Only on phrases repeated across multiple quotes or cards.
- Never omit `.footer-bar` on evidence, chart, or quote slides.
- Never write component HTML from scratch. Start from `references/component-html.md`.
