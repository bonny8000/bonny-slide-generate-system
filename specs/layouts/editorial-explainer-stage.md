---
id: editorial-explainer-stage
kind: layout
tier: layout
status: stable
intent: humanize workshop instructions, workflow transformation, or real-UI interpretation
triggers: [workshop timing and rules, facilitator dialogue, human-agent worked example, assistant-led workflow, scattered inputs to shared intent, real UI with Q&A, 工作坊怎麼進行, 有人味的說明, 引導流程說明, 實際畫面加問答]
material: illustration+ui-screen
arrangement: narrative-stage
item_count: one
alternates: []
depends_on: [shot, stage-backdrop, tokens]
tokens_used: [canvas, surface, ink, muted, muted-soft, accent, accent-soft, shadow-img]
icon_use: generated-only
learned_from: Img39, Img40, Img41, Img42, Img43
example: examples/editorial-explainer-stage.html
last_synced: 2026-07-15
---
# Editorial explainer stage

Use one generated image as the dominant full-block stage. Select `agenda-dialogue`, `workflow-transform`, or
`ui-qa` through `generated-editorial-explainer.md`; do not blend variants on one page.

- Generate at the stage's exact ratio and fill it completely; no contain-fit gutters.
- Keep exact titles/body copy native in intentionally empty zones whenever possible.
- For `ui-qa`, preserve the real screenshot and generate only the surrounding editorial explanation.
- Save the fresh generated asset inside the deck and apply no grayscale/desaturation filter.

This layout is invalid without a fresh built-in image-generation call. The references may guide generation
but may never become delivered output. HTML/CSS/SVG recreation is not a fallback; choose a native layout.
