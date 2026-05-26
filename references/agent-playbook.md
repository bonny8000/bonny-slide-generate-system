# Agent Playbook

Use this file when an agent is using Bonny Slide System V2 to create, critique, or redesign slides.

## Operating Principle

Do not start by picking a pretty layout. Start by classifying the content intent, then select the component that explains that intent with the least ambiguity.

## Step 1: Classify The Request

Identify:

- Output type: single slide, deck, template, design-system doc, or critique.
- Source type: transcript, research notes, raw images, PRD, metrics, screenshots, or existing deck.
- Story type: UX research, product redesign, strategy report, product pitch, result report, or portfolio case study.
- Language: default to Traditional Chinese primary + English support unless the user specifies otherwise.
- Format: HTML, PPTX, Markdown spec, or Figma-style design instructions.

## Step 2: Build A Slide Outline

For each slide, assign:

- Intent label.
- One-sentence message.
- Primary component.
- Supporting components.
- Mode.
- Accent color.
- Required source/evidence.

Example outline row:

```text
Slide 4 | Pain Point | Users cannot connect intent to action after discovery | Pain Point Card Triad | Quote cards + key band | Light | Pink/blue | Interview notes
```

## Step 3: Choose Components

Use this decision order:

1. Is the content evidence? Use `Evidence Card` or `Chart Card`.
2. Is it user voice? Use `Quote Card`.
3. Is it a blocker? Use `Pain Point Card`.
4. Is it a synthesized meaning? Use `Insight Module`.
5. Is it a transition from problem to design direction? Use `Problem-To-Opportunity Bridge`.
6. Is it a before/after or current/future change? Use `As-Is / To-Be`.
7. Is it a sequence? Use `Workflow Timeline`.
8. Is it a product behavior? Use `Phone Mockup Walkthrough`.
9. Is it a feature set? Use `Feature Stack`.
10. Is it outcome data? Use `Result Dashboard`.

## Step 4: Choose Mode And Accent

Mode:

- Light for evidence, context, comparison, and normal explanation.
- Dark for insight, emotional interview, product reveal, walkthrough, or result.
- Mixed for one emphasized panel inside an otherwise light report slide.

Accent:

- Blue for research, data, product structure.
- Green for improvement, success, service simplification.
- Purple for social, motivation, friendly AI.
- Orange/yellow for attention, study, warm service.
- Pink/red for pain, warning, friction.
- Gray for baseline, inactive, current state.

## Step 5: Draft Content

Convert raw source into slide text:

- Headline: argument, not topic.
- Subtitle: method/context.
- Cards: one idea each.
- Captions: evidence source.
- Key band: implication or next action.

Use this compression rule:

- Raw paragraph -> headline + 2 cards.
- Five quotes -> 3 quote patterns.
- Feature list -> 3 feature outcomes.
- Complex workflow -> 4-stage timeline.
- Dense metrics -> one hero metric + two supporting metrics.

## Step 6: Compose The Slide

For HTML:

1. Open `references/component-html.md` and find the snippet for the primary component you chose in Step 3.
2. Copy that snippet into the slide shell from `assets/templates/slide-template.html`.
3. Replace placeholder text with real content. Do not change class names.
4. Set `data-mode="light"` or `data-mode="dark"` on `.slide` based on Step 4 mode choice.
5. Add `.footer-bar` with source and page marker for any evidence slide.
6. Use `lang="zh-TW"` on CJK text containers and `.latin` on English/number spans.
7. Never add inline styles for color, font-size, font-weight, or letter-spacing. Only use inline style for per-slide layout overrides (gap, padding-block-start, max-inline-size).

For PPTX:

- Use the same canvas logic: 16:9, generous margin, component hierarchy.
- Preserve font roles, spacing, and accent semantics.
- Treat each component as a grouped object.

## Step 7: Validate

Run checks:

- Does the slide have one dominant message?
- Does the chosen component match the intent?
- Does every claim have source, method, or baseline where needed?
- Does text fit without overflow?
- Are CJK and English spacing handled separately?
- Is the primary accent used semantically?
- Are charts readable from a presentation distance?
- Are phone mockup callouts limited to 2-3?

For HTML:

```bash
python scripts/check_slide_html.py path/to/slide.html
```

## How To Respond To The User

When finishing a design-system or deck task, report:

- What was created.
- Where the files are.
- The strongest design-system improvements.
- What was validated.

Keep the report short unless the user asks for full rationale.

## Agent Anti-Patterns

- Do not copy Pinterest layouts directly. Extract structure and translate it into the user's content.
- Do not use a card grid when the content is a flow, comparison, or insight.
- Do not make every slide light; use dark mode at narrative turning points.
- Do not show product screenshots without annotations.
- Do not use decorative icons when data, quote, or workflow structure is the real evidence.
- Do not bury the main message inside body text.
- Do not invent statistics. Use placeholders if source data is missing.
- Do not write component HTML from scratch. Always start from `references/component-html.md`.
- Do not invent CSS class names. If a class does not exist in `bonny-slide-v2-tokens.css`, do not use it.
- Do not use inline `style=""` for colors or typography. Token classes handle those.
- Do not apply `data-mode="dark"` to `.frame` or inner elements. It goes on `.slide` only.
- Do not use more than one accent family per slide unless showing multiple categories.
- Do not omit `.footer-bar` on evidence, chart, or quote slides.
- Do not write `.highlight` spans on random words. Only highlight repeated terms that appear across multiple quotes or cards.

## When You Are Unsure

If you are unsure which component to use, apply this test:

- If the main evidence is a number → `metric-card`
- If the main evidence is a user's words → `quote-card`
- If the content is wrong, blocked, or painful → `pain-card`
- If the content is a synthesized finding → `insight-panel`
- If the content shows how something changes → `comparison-grid`
- If the content shows steps in order → `timeline`
- If the content shows a product screen → `phone` + `annotation-list`
- If the content lists what will be built → `feature-stack`
- If the content shows what improved → `metric-card` grid (result dashboard)
- If none of the above → `card card-pad` inside `grid grid-3` with `card-title` + `card-body`

Default to 3 cards in light mode when uncertain. That is always a safer choice than inventing a new layout.
