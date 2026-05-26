# Foundations

Use this file for every Bonny Slide System V2 task.

## Canvas

- HTML slide: fixed `1920 x 1080`.
- PPTX slide: widescreen `13.333 x 7.5 in`.
- Safe margin: `104px` left/right and `72px` top/bottom by default.
- Dense report margin: `88px` left/right and `64px` top/bottom.
- Sparse cover margin: `128px` left/right and `96px` top/bottom.
- Use a visible design grid: 12 columns, `28px` gutters, with content usually spanning 10-12 columns.

## Layout Zones

- Header zone: `72-210px`; eyebrow, slide title, subtitle.
- Evidence zone: `240-900px`; cards, charts, mockups, quotes, maps.
- Footer zone: `920-1008px`; source, method, page marker, next-step band.
- Do not place primary evidence below `900px` unless the slide is a full-height flow or timeline.

## Spacing Scale

- Micro: `8px`, `12px`, `16px`.
- Component internal: `20px`, `24px`, `32px`.
- Card gaps: `28px`, `32px`, `40px`.
- Section gaps: `48px`, `64px`, `80px`.
- Title-to-content gap: `48-72px`.
- Dense dashboard gap: `20-28px`.

## Typography

Use separate spans or language attributes when mixing CJK and Latin.

- CJK font stack: `Noto Sans TC`, `Microsoft JhengHei`, `PingFang TC`, system sans-serif.
- Latin font stack: `Inter`, `Helvetica Neue`, `Arial`, system sans-serif.
- CJK letter spacing: `0.05em`.
- Latin, numbers, dates, and product names: `0`.
- Default line height: `1.5`.
- Dense chart labels can use line height `1.25-1.35`.

## Type Scale On 1920 x 1080

- Cover title: `72-92px`, weight `700`.
- Section title: `60-76px`, weight `700`.
- Main slide title: `44-60px`, weight `700`.
- Secondary title: `34-42px`, weight `650-700`.
- Card title: `24-32px`, weight `650-700`.
- Body: `20-26px`, weight `400-500`.
- Quote text: `28-40px`, weight `500-650`.
- Annotation: `18-22px`, weight `500-650`.
- Caption/source: `14-18px`, weight `400`.
- Large metric: `68-112px`, weight `700`.

## Text Rules

- One headline per slide. The headline states the argument, not the topic label.
- Use the accent color on one phrase, metric, or status word per headline.
- Keep the English line subordinate: usually 50-70% of the Chinese title size.
- Use body paragraphs only for context. Convert lists into cards, rows, chips, timelines, or callouts.
- Use 3 as the default count for parallel evidence. Use 2 for comparisons and 4-5 for process stages.
- Avoid more than 28 CJK characters in a single card title.
- Avoid more than 2 body lines in a compact evidence card.

## Color System

Use one accent family per slide unless showing categories or actors.

### Neutrals

- Light canvas: `#FFFFFF`, `#F6F8FB`, `#F2F5F9`.
- Light surface: `#FFFFFF`.
- Light border: `#E3E8F0`, `#D8DEE8`.
- Primary text: `#111827`.
- Secondary text: `#344054`.
- Muted text: `#667085`.
- Quiet metadata: `#98A2B3`.

### Dark Neutrals

- Dark canvas: `#101418`, `#151B22`, `#1B2430`.
- Dark surface: `#1F2732`, `#27313D`.
- Dark border: `#3A4553`.
- Dark primary text: `#FFFFFF`.
- Dark secondary text: `#E5E7EB`.
- Dark muted text: `#A8B0BD`.

### Semantic Accents

- Research/data: blue `#2F80ED`, `#4C83F1`, soft `#EAF2FF`.
- Product/system clarity: cobalt `#2854FF`, soft `#EEF2FF`.
- Improvement/success: green `#20C781`, `#16B364`, soft `#E7F8EF`.
- Social/motivation/friendly AI: purple `#6B6FF2`, soft `#F0EFFF`.
- Attention/study/warm service: orange `#FF9F1C`, yellow `#FFD84D`, soft `#FFF5DA`.
- Pain/warning/friction: red `#E74C3C`, pink `#FF5C8A`, soft `#FFE8EF`.
- Inactive/baseline: gray `#98A2B3`, soft `#F2F4F7`.

## Mode Selection

Use light mode for:

- Context, background, desk research, survey data, market analysis, normal feature explanation, comparison tables, and appendix slides.

Use dark mode for:

- Emotional interviews, high-level insights, solution reveal, product walkthrough, status map, result dashboard, and dramatic before/after.

Use mixed mode only when:

- A light slide needs one dark focus panel for the future state, selected user segment, or final result.
- A dark slide needs white product UI cards or phone mockups for readability.

## Surfaces And Shapes

- Standard evidence card radius: `24px`.
- Dense dashboard card radius: `16px`.
- Report/table card radius: `10-12px`.
- Pill radius: `999px`.
- Soft shadow: `0 16px 40px rgba(15, 23, 42, 0.08)`.
- Dark shadow: `0 18px 50px rgba(0, 0, 0, 0.28)`.
- Use borders more than shadows on dense report slides.
- Avoid nested cards unless the inner object is a screenshot, chart, form, or quote.

## Chart Rules

- Always include axis, baseline, period, or source when showing quantified claims.
- Use one active accent and gray inactive bars/lines.
- Use chart cards for evidence; use metric cards for results.
- Do not make pie/donut charts unless one dominant proportion is the message.
- Use annotations to explain the change, not to restate the label.

## Asset Rules

- Use real product screens, screenshots, or clear image references when the slide is about a product.
- Use simple custom diagrams when explaining a process, service, or workflow.
- Use avatar or character elements only on approachable portfolio/empathy slides.
- Do not use decorative gradient blobs, stock-style abstract visuals, or purely atmospheric images.
