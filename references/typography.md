# Typography

Use this file for every Bonny slide task.

## Language Defaults

- Primary output language: Traditional Chinese.
- Secondary output language: English.
- If source references are Korean or another language, translate the design intent into Traditional Chinese plus English support text.
- Keep Chinese and English visually distinct. Chinese usually carries the headline and main decision; English is often a smaller subtitle, label, or explanatory line.

## Font Stacks

- Chinese: `Noto Sans TC`, `Microsoft JhengHei`, `PingFang TC`, system sans-serif.
- English: `Inter`, `Helvetica Neue`, `Arial`, system sans-serif.
- Avoid serif fonts unless the user explicitly asks for a more editorial magazine tone.

## Required Spacing

- Chinese letter spacing: `0.05em`.
- English letter spacing: `0`.
- Numbers, percentages, dates, and product labels: `0`.
- Default line-height: `1.5` for Chinese and English.
- For mixed text, wrap CJK and Latin spans separately when possible so English and numbers do not inherit CJK letter spacing.

Example:

```html
<h1><span class="cjk">會員留存率提升</span> <span class="latin">34%</span></h1>
```

## Type Scale On 1920 x 1080 Canvas

- Cover title: `64-88px`, weight `700`.
- Section title: `48-64px`, weight `700`.
- Main slide title: `42-56px`, weight `700`.
- Supporting subtitle: `22-30px`, weight `400-500`, muted color.
- Card title: `24-34px`, weight `600-700`.
- Body: `20-26px`, weight `400-500`.
- Caption/source: `14-18px`, weight `400`.
- Tiny metadata/chapter labels: `14-18px`, weight `500-700`, often accent colored.
- Large numeric result: `56-88px`, weight `700`.

## Hierarchy Rules

- Use one main headline per slide. Do not split attention between multiple large headings.
- Highlight only the decisive phrase or metric in accent color.
- Keep English support text at 50-75% of the Chinese visual weight.
- In research and evidence slides, keep captions/source text visible but quiet.
- In dark mode, use white headlines, muted gray body, and accent only for the core finding.

## Text Density

- Prefer 3 cards, 3 bullets, or 3 evidence points when summarizing.
- Use 2 columns when comparing.
- Use 4 steps only when showing a process or timeline.
- Avoid more than 3 nested text levels on one slide.
