# Case study deck — source content & slide plan

A 10-slide bilingual (繁中 + English) UX case-study deck, generated through the full pipeline
(`slide-plan` → `content-map` → build → screenshot → self-critique) and used as the test harness for the
v9.6 system improvements. Theme: **light-periwinkle**. All slides self-contained (tokens + base.css inlined).

**Topic:** 校園語言交換 App — 讓語言交換聚會不再讓人卻步 (a campus language-exchange app: lowering the
barrier to the first conversation).

| # | Intention (the job) | Layout / components | base.css used |
|---|---|---|---|
| 01 | Open the deck | cover (centered head) | headline/eyebrow/sub/meta |
| 02 | Set the map | agenda — **`.slide.top`** single column + descriptions | head + custom list |
| 03 | Explain the situation with data | numbered-rows ×3 + charts | numrow · linechart · barchart · donut |
| 04 | Anchor in real users | persona-cards ×2 | card · qbubble · chipcloud · hbars |
| 05 | Contrast problem → solution | problem-solution (muted vs accent-soft panels) | grid12 + custom panels |
| 06 | Compare options | comparison-table — **`.slide.top`** | ctable (focus column) |
| 07 | Land the insight | statement/callout (centered pause) | callout |
| 08 | Show what we built | feature-rows (headline + 3) | feature-rows + monochrome SVG icons |
| 09 | Prove impact | results: KPI before/after + 2 metrics | kpibars · delta · metric |
| 10 | Summarize & close | conclusion: 3 takeaways + callout band | cards.three · callout |

## What this deck taught the system (v9.6)
1. **Thin header-led slides floated** with an empty band above the title (02, 06). → added **`.slide.top`**
   (pin header to top) + a rule in `layout-balance.md`. Empty *top* reads worse than empty *bottom*.
2. **Shadows were too strong** on device mockups. → added subtle **`--shadow-card` / `--shadow-pop`** tokens
   + an elevation rule; softened the `as-is-to-be` example.
3. **Leaning on existing `base.css` components** (ctable, numrow, kpibars, feature-rows, hbars…) makes most
   slides robust and self-contained with little custom CSS — the reliable path for generation.

> Validation: every page was rendered headlessly (Edge `--headless --screenshot`) at 1920×1080 and reviewed
> visually, per `foundations/self-critique.md` — not signed off on structural checks alone.
