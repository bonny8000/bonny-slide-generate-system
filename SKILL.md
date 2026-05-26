---
name: bonny-slide-system
description: Generate, critique, redesign, or systematize bilingual UX/product case-study slides in Bonny's detailed editorial slide style. Use when Codex needs to create Chinese/English slide decks, UX portfolio slides, research reports, product strategy decks, case-study pages, HTML/PPTX slide templates, design-system rules for slides, or agent instructions for choosing slide components, modes, typography, layouts, and storytelling patterns.
---

# Bonny Slide System V2

## Purpose

Create clear bilingual UX/product slides with a stricter design system than the previous Bonny slide skill. The system is optimized for agents: each slide is selected by content intent, then built from defined components, variants, tokens, and validation checks.

Use this skill for 16:9 slide surfaces, usually `1920 x 1080` HTML or widescreen PPTX. Default language is Traditional Chinese as the main voice with English as supporting labels, subtitles, captions, and metrics.

## Core Workflow

1. Identify the slide job: cover, context, research evidence, interview, pain point, insight, opportunity, solution, workflow, comparison, product feature, result, or appendix.
2. Read `references/agent-playbook.md` first when the user asks for a deck, redesign, or system-level output.
3. Read `references/foundations.md` for typography, grid, spacing, color, modes, and writing rules.
4. Read `references/component-system.md` before composing slides. Choose components by intent, not by decoration.
5. Read `references/component-html.md` to get the exact HTML structure for each component before writing any markup. Never invent class names or inline styles — copy from this file and fill in real content.
6. Read `references/slide-recipes.md` when mapping source material into a multi-slide deck.
7. Use `assets/bonny-slide-v2-tokens.css` and `assets/templates/slide-template.html` for HTML slides.
8. Validate with `scripts/check_slide_html.py <html-file>` for HTML output when practical.

## Default Design Position

- Prefer clean light-mode editorial slides for context, evidence, comparison, MVP explanation, and normal report pages.
- Switch to dark mode for emotional interview findings, high-level insights, solution reveal, product walkthroughs, process/status maps, and result dashboards.
- Use one main message per slide. Supporting components exist to prove or explain that message.
- Use cards only when grouping evidence, quotes, metrics, steps, or screenshots. Do not make every section a card.
- Keep CJK and Latin typography separate: CJK gets `letter-spacing: 0.05em`; English, numbers, and product names get `letter-spacing: 0`.
- Use source notes, method labels, participant counts, or baseline labels whenever claims depend on evidence.

## Reference Loading Guide

Always load:

- `references/foundations.md`
- `references/component-system.md`
- `references/component-html.md` — **required for any HTML output.** This file has ready-to-use HTML snippets for every component. Copy and adapt; do not write component HTML from scratch.

Load when relevant:

- `references/slide-recipes.md` for deck structure, slide-by-slide recipes, and situation mapping.
- `references/agent-playbook.md` for how an agent should decide what to build and how to report choices.
- `references/source-analysis.md` when matching the Pinterest/Korean UX portfolio references or explaining why v2 differs from `bonny8000/bonnyt`.

## Output Contract

For a deck or slide system output, provide:

- A slide outline with intent labels, such as `Research Evidence`, `Pain Point`, `Insight`, or `Feature Walkthrough`.
- A component map listing the primary component and supporting components for each slide.
- Mode and accent choices with short reasons.
- Final slide files or templates when requested.
- A validation note covering text overflow, hierarchy, source traceability, and component fit.

## CSS Discipline Rule

When writing HTML slides, always follow this rule without exception:

- **Copy component HTML from `references/component-html.md`.** Do not write component structure from scratch.
- **Use only class names that exist in `assets/bonny-slide-v2-tokens.css`.** Do not invent new class names.
- **Never use `style=""` for colors, font-size, font-weight, or letter-spacing.** Only use inline style for layout overrides that are specific to one slide (such as `gap`, `padding-block-start`, `max-inline-size`, or `min-inline-size`).
- **Never import external fonts or libraries.** All tokens are already in `bonny-slide-v2-tokens.css`.
- **Never use `!important`.** If a style isn't applying, the class is either wrong or not in the token file.

Consistency comes from always starting from the same component snippets, not from trying to remember rules.

## Quality Bar

Before final delivery:

- Confirm every slide has one dominant message and one primary visual structure.
- Confirm component choice matches content intent, using `references/slide-recipes.md` as the decision guide.
- Confirm no text sits below 18px on a 1920 x 1080 slide unless it is source metadata.
- Confirm charts have baseline/context labels, not just numbers.
- Confirm quote slides use `.highlight` to mark repeated patterns, not isolated quotes.
- Confirm phone mockup slides have exactly 2–3 `.annotation-item` entries explaining user value.
- Confirm dark slides use `data-mode="dark"` on `.slide`, not on `.frame` or inner elements.
- Confirm HTML slides link `bonny-slide-v2-tokens.css` and use no other stylesheet.
- Confirm every evidence slide has a `.footer-bar` with source and page marker.
