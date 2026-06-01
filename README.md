# Bonny Slide System

Bonny Slide System is a bilingual slide design and production system for UX, product, strategy, and progress-report storytelling.

It is not a one-off slide template. It gives people and AI agents a shared way to turn messy work into clear slides: choose a story structure, apply a consistent visual mode, write in plain language, and export to HTML or PPTX.

Traditional Chinese is the primary voice. English is used for supporting labels, tags, metrics, and section handles.

## What this system helps with

- Explain UX research, product decisions, system thinking, or project progress.
- Turn abstract work into slides that managers, PMs, designers, and engineers can understand on first read.
- Keep AI-generated slides visually consistent without hand-tuning every page.
- Support both human presentation and AI handoff: the rules are explicit enough for another agent to continue the work.
- Produce either per-slide HTML, a single scroll-through HTML page, or PPTX through the included Python bridge.

## How the system works

### 1. One mode per deck

Each deck uses one visual mode:

| Mode | Best for | Feel |
|---|---|---|
| LIGHT | research, explanation, documentation, progress reports | clean editorial deck |
| DARK | executive summary, system reveal, product strategy, high-impact story | premium infographic poster |

A deck should not mix LIGHT and DARK as normal pages. Section covers may use a dark full-bleed background inside a light deck when they act as a divider, not as a new mode.

### 2. Shared structure, swappable color tokens

The system separates structure from color:

- `assets/base.css` defines layout, grid, spacing, typography, and components.
- `assets/tokens-light.css` defines the LIGHT color mode.
- `assets/tokens-dark.css` defines the DARK color mode.

Because both token files use the same variable names, a deck can switch modes by changing one CSS file.

### 3. Four-color discipline

Every slide should stay within a strict color model:

**1 background + 1 text + 1 muted + 1 highlight.**

The highlight color is the only chromatic color. Charts and diagrams should use muted states plus one active accent, unless they are showing a specific positive/negative KPI comparison.

### 4. Plain-language layer

The system is designed for mixed rooms, not only UX specialists. Every title and caption should pass a one-read test:

- Say the slide's message directly.
- Avoid stacked abstract modifiers.
- Use concrete examples instead of vague categories.
- Add plain labels to internal codes or framework names.
- Show who can use the work, what they use it for, and what they get.

### 5. Show the reasoning, not only the result

When presenting a system, method, or decision, the slide flow should show the thinking:

1. What was collected or compared.
2. How the relationships were identified.
3. How the final structure or recommendation was formed.

This keeps the deck from jumping straight to a conclusion and makes the reasoning easier for another person or AI agent to review.

## What is included

```text
bonny-slide-system/
├─ SKILL.md
├─ README.md
├─ assets/
│  ├─ base.css
│  ├─ tokens-light.css
│  └─ tokens-dark.css
├─ examples/
│  ├─ light-*.html
│  └─ dark-*.html
└─ pptx/
   ├─ tokens.py
   ├─ slidegen.py
   ├─ build_sample.py
   ├─ sample-light.pptx
   └─ sample-dark.pptx
```

## How to use it

For people:

1. Start from the story: research finding, product decision, progress update, system explanation, or outcome.
2. Choose LIGHT or DARK for the whole deck.
3. Copy the closest HTML example from `examples/`.
4. Keep the title plain and specific.
5. Use `assets/base.css` plus one token file.
6. Export or rebuild as HTML/PPTX.

For AI agents:

1. Read `SKILL.md` first.
2. Classify the slide job before choosing a layout.
3. Use existing components and examples instead of inventing a new visual style.
4. Keep Traditional Chinese primary and English supporting.
5. Validate that the slide has one clear message, one mode, and a readable structure.

## Good fit

- UX case studies
- Product strategy decks
- Research synthesis
- Design-system or agent-system explanation
- CMS / internal-system progress reports
- Handoff materials for PM, design, engineering, or another AI agent
- Bilingual executive summaries

## Known scope

This system provides slide structure, visual rules, examples, and a PPTX bridge. It does not automatically guarantee WCAG contrast compliance in every custom slide. If accessibility compliance is required, adjust muted text contrast and validate the final output.

— Bonny Slide System v8.0.1
