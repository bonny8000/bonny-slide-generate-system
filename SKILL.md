---
name: bonny-slide-system
description: Generate, critique, or convert bilingual UX research and product case-study slides in Bonny's editorial slide style. Use when Codex needs to create Chinese/English slide decks, UX portfolio slides, research/problem/insight/solution slides, light-mode or dark-mode variants, HTML/PPTX slide templates, or when asked to apply Bonny slide typography, component choices, colors, layout patterns, or visual storytelling.
---

# Bonny Slide System

## Purpose

Create polished bilingual UX/product slides that feel like Bonny's portfolio and research decks: quiet editorial structure, strong hierarchy, clean data cards, intentional accent color, and clear light/dark mode control.

This is not a model fine-tune. Treat the source material as design references and use these rules to choose layout, component, mode, and color for future slide work.

## Default Output

- Use 16:9 slides. For HTML use a fixed `1920 x 1080` canvas; for PPTX use widescreen `13.333 x 7.5 in`.
- Use Traditional Chinese and English by default. Translate non-English reference content into Chinese/English output unless the user requests another language.
- Apply typography exactly: Chinese letter spacing `0.05em`, English letter spacing `0`, and line-height `1.5`.
- Prefer light mode unless the user asks for dark mode or the content is an insight/result/user-test/emphasis section that benefits from stronger contrast.
- Build the actual slide surface, not a marketing landing page.

## Workflow

1. Identify the slide intent before designing: background, desk research, user research, problem, pain point, insight, solution, workflow, comparison, product feature, MVP, result, or portfolio cover.
2. Choose the mode. Use light mode for evidence, survey, analysis, and product explanation. Use dark mode for interviews, high-emphasis insights, before/after outcomes, result dashboards, emotional pain, and cinematic product walkthroughs.
3. Choose components using `references/component-decision-rules.md`.
4. Apply typography from `references/typography.md` before tuning layout.
5. Apply color and mode rules from `references/color-and-mode.md`.
6. Use `references/layout-patterns.md` to structure the slide.
7. Check the result: no text overflow, no accidental overlap, visible hierarchy, consistent accent semantics, readable charts, and enough whitespace.

## Reference Loading

Always read:

- `references/typography.md`
- `references/component-decision-rules.md`

Read when relevant:

- `references/color-and-mode.md` for light/dark mode and accent decisions.
- `references/layout-patterns.md` for concrete slide structures.
- `references/source-observations.md` when matching the uploaded Pinterest/Korean/portfolio references or the legacy Bonny v1 source.

## Assets

- `assets/bonny-slide-tokens.css` contains reusable CSS variables and utility classes for HTML slide work.
- `assets/templates/slide-template.html` is a minimal 1920 x 1080 HTML slide starting point.
- `assets/legacy-v1/` stores selected files from the previous `bonny_slide_skill` as source material. Use it as reference, not as the primary rule source.

## Validation

Before final delivery, verify the slide against these checks:

- Chinese text has `letter-spacing: 0.05em`; English and numbers have `letter-spacing: 0`.
- Body and caption text use `line-height: 1.5`.
- Each slide has one dominant message, one primary visual structure, and no more than one strong accent color family.
- Light slides remain white or pale-gray first; dark slides use deep neutral surfaces with bright accents only for meaning.
- Components match the content intent. Do not use decorative cards, bubbles, or gradients when a chart, flow, or comparison is the clearer showing way.
- For HTML output, run `scripts/check_slide_html.py <html-file>` when practical.
