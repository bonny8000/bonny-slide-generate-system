# Slides UI Kit

A JSX recreation of every Bonny Slide System V2 component, mirroring the same class names defined in `assets/bonny-slide-v2-tokens.css`. Use these components when you want to compose slides programmatically (React) instead of writing the HTML by hand. The visual rules are identical — anatomy, mode, accent, validation — only the syntax differs.

## Files

- `index.html` — interactive demo: navigate through every slide intent (cover, desk research, interview, pain, insight, comparison, phone walkthrough, result dashboard). Acts as the visual reference for the kit.
- `Slide.jsx` — the slide shell. Wraps `<main class="slide">` + `<section class="frame">` and handles `data-mode` switching.
- `TitleBlock.jsx` — eyebrow + headline + subtitle, with `.accent-*` highlight injection.
- `EvidenceCard.jsx` — 3-column evidence card grid.
- `QuoteCard.jsx` — interview quote cluster with participant + highlighted phrase.
- `PainCard.jsx` — pain-point card with label, quote, root cause, severity.
- `MetricCard.jsx` — large metric + label + baseline.
- `InsightPanel.jsx` — dark cinematic insight panel.
- `ComparisonGrid.jsx` — As-Is / To-Be two-column with state divider.
- `Timeline.jsx` — workflow timeline with 3–5 stages.
- `PhoneWalkthrough.jsx` — phone mockup + annotation list.
- `FeatureStack.jsx` — MVP / pillar feature rows.
- `KeyBand.jsx` — bottom takeaway / next-step band.
- `Footer.jsx` — page footer with source + page marker.

## Usage

```jsx
<Slide mode="light">
  <TitleBlock
    eyebrow="DESK RESEARCH"
    headline={<>外部數據驗證了<span className="accent-blue">核心問題假設</span></>}
    subtitle="3 independent sources · 2023–2024"
  />
  <EvidenceCard.Grid>
    <EvidenceCard pill="01" title="日均使用者上升" body="2025 達 24 萬 6 千人 +12%" source="KTX 2025" />
    <EvidenceCard pill="02" title="線上預訂為主流" body="88.2% 透過線上購票" source="Annual Survey" />
    <EvidenceCard pill="KEY" title="App 下載量第一" body="1,600 萬下載" source="MOI Brief" accent="blue" />
  </EvidenceCard.Grid>
  <Footer source="Source: KTX Annual Report 2024" page="04 / 08" />
</Slide>
```

## Rules (same as the rest of the design system)

- One dominant message per slide.
- Pick the component by **content intent**, not decoration. See `SKILL.md` Content → Component matrix.
- Light mode for evidence / context / comparison. Dark mode for insight / walkthrough / result.
- One accent family per slide unless comparing categories.
- Mark CJK and Latin runs separately. Never mix in one span.
- Highlight only one phrase per headline.
- Every evidence/chart/quote slide gets a `<Footer>`.

The components are intentionally thin — they're cosmetic wrappers around the CSS classes, not state machines. If you need behavior, drop into the underlying div.
