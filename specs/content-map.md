# Content → slide map (the "make a slide" engine)

Given a chunk of naked content, detect its **shape**, then use the mapped layout + components.
This is what turns raw text into a good slide reliably (instead of the AI guessing).

| Content shape | How to detect it | Layout | Key components | Icon/illustration |
|---|---|---|---|---|
| Single big claim / thesis | one sentence meant to land | `statement` | enlarged headline (32–36px) + 1 keyword in accent | none |
| Definition / concept set | "X means…", a few terms | `terminology-cards` | terminology-card (illustration + term + def) [+ example card] | keyword illustration |
| Comparison of options | N options × criteria, vs, "better than" | `comparison` | comparison-table (criteria×options, O/X or value, 1 column highlighted) | option logos/icons in header |
| Flat list of items | bullets, tags, "we have…" | `card-grid` or inline | chip / taglist / feature-card | optional icon per item |
| Process / sequence / before→after | arrows, "first…then", "as-is/to-be" | `flow` | stepflow (①→②→③) / flow-row | small step icons |
| Single metric / KPI | one number that matters | `metric` or evidence card | metric / delta-metric (±% + before/after bars) | optional stat icon |
| Several data points | charts, %, counts | `data` | barchart / hbar / pie-donut / line / bubble-cluster | none (let data speak) |
| Survey / Q&A results | repeated questions + answers | `survey-stack` | q-card (question + chart + 1-line insight); left rail = sample stats | Q badges |
| Research story | background → problem → insight | `research-flow` | data cards → callout-band (HMW) → citation-card | none |
| Qual + quant together | quotes AND numbers | `qual-quant-split` | quote-bubble (+avatar) | stat bars | avatar icons |
| Timeline / roadmap | phases over time | `timeline` | numbered-row / phase markers | phase markers |
| Hierarchy / IA / structure | tree, nesting, sitemap | `hierarchy` | indented nodes / tree | node icons |
| Quote / testimonial | attributed sentence | `quote` | quote-bubble + avatar | avatar |
| Persona | a user archetype | `persona` | persona card + avatar | avatar/illustration |
| Relationships / dependency | "depends on", "in parallel" | `relations` | relationship triplet (前後 / 相依 / 並行) | small flow icons |
| Citations / evidence | findings + sources | `citations` | citation-card (finding + source) | none |
| 3 parallel evidence types | a stat + a chart + logos | `evidence-trio` | evidence-card ×3 (icon-stat / chart / logo-row) | stat icon + logos |
| Centered framing question | a question to anchor a section | `centered-question` | big centered question + 3 evidence cards | optional |
| Numbered explainer rows | 1/2/3 points, each w/ a chart | `numbered-rows` | numbered-row (badge + bilingual text + chart) | number badges |
| Section transition | "now part 2 of 3" | `section-cover` (扉頁) | section-cover (small nav + hero title) | none |
| Agenda | the outline | `toc` | numbered outline | none |

**Selection rule:** prefer the most specific shape. If two fit, the one with a concrete visual
(chart/table/illustration) usually wins over plain cards — it carries more meaning per slide.
