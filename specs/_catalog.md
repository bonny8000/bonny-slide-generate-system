# Catalog — components & layouts (and what each was learned from)

Mined from real reference decks (Img1–Img43). **Every entry is now `stable`** — has a spec *and* a render-validated example (`examples/`). All are **theme-agnostic** (color comes from the deck theme, with the narrow generated-editorial bitmap exception documented in `color-discipline.md`).

> **Growing this catalog:** when the user sends a new reference slide image, follow
> `foundations/learn-from-image.md`. New images continue the `ImgN` convention (Img13, Img14, …) in
> `learned_from`, so every learned pattern stays traceable to the slide it came from.

## Layouts (organisms)
| id | what it is | learned_from | status |
|---|---|---|---|
| cover | title slide | — | stable |
| toc | agenda / 目錄 | — | stable |
| section-cover | 扉頁 transition (small nav + hero title) | — | stable |
| context | 40/60 overview | — | stable |
| statement | one enlarged claim, 1 keyword accent | — | stable |
| kpi-results | headline + before/after delta charts + bottom plan panel | Img1 | stable |
| survey-stack | repeated Q (question + chart + 1-line insight) + sample rail | Img2 | stable |
| research-flow | data cards → HMW callout band → citation cards | Img3 | stable |
| qual-quant-split | speech-bubble quotes + stat bars + hypothesis | Img4 | stable |
| editorial-explainer-stage | generated agenda-dialogue / workflow-transform / real-UI-Q&A variants in one visual system | Img39–Img43 | stable |
| idea-evidence | statement + chart \| survey stat + reasoning (two col) | Img5 | stable |
| hero-radial | center illustration + radial labels + two side list-cards | Img6 | stable |
| interview-affinity | design rail + persona columns (avatar + reasons) + insight boxes | Img7 | stable |
| centered-question | centered framing question + 3 evidence cards | Img8 | stable |
| comparison | comparison table + ranked-needs panel | Img9, Img16 | stable (see component) |
| service-flow | swimlane flowchart: start → decisions → ends, regions by segment + callouts | Img14 | stable |
| positioning-matrix | 2×2 perceptual map: axis cross + markers + accent target point | Img15 | stable |
| problem-solution | two mirrored panels (muted problem vs bright solution) | Img17 | stable |
| linked-circles | overlapping translucent circles in one container (continuum) | Img18 | stable |
| product-hero | landing hero: nav + headline + CTA pair + stat trio + product UI mockup + tab row | Img19 | stable |
| keyword-cards | 3–4 numbered value cards (number·label + title + desc) | Img20 | stable |
| feature-showcase | feature areas under header bands, shown with annotated device mockups | Img21 | stable |
| annotated-screen | one built screen with notes pinned to the parts they describe + numbered legend | Ref-annotated-screen-2026-08-31 | stable |
| hidden-majority | one whole split across a waterline: the visible sliver above, the mass it hides below | Ref-hidden-majority-2026-09-02 | stable |
| event-sequence | actors as columns, time down, one row per message, with the decisive stretch banded | Ref-event-sequence-2026-09-03 | stable |
| system-anatomy | peer blocks on a rail, one hosting a nested subsystem, with numbered connectors between | Ref-system-anatomy-2026-09-03 | stable |
| role-thread | a thread whose turns are attributed to roles, with one turn expanded into evidence | Ref-role-thread-2026-09-03 | stable |
| practice-hero | an illustration of the practice, captioned, over the numbered steps it runs | Ref-practice-hero-2026-09-03 | stable |
| persona-cards | 1–2 persona cards: avatar + quote + tags + story + behavior sliders + pain points | Img22 | stable |
| painpoint-evidence | two problem panels: participant quote-avatar row + annotated geo map | Img23 | stable |
| timeline | Gantt: staggered phase bars over a dated axis + deliverables | Img24 | stable |
| value-points | 2–3 "why us" points, each paragraph + a backing card (tag cluster) | Img25 | stable |
| use-case-cards | 3 audience/use-case cards: badge + recolored illustration + caption | Img26 | stable |
| as-is-to-be | two annotated screen mockups (muted As-is vs accent To-be) | Img28 | stable |
| numbered-rows | 1/2/3 rows: badge + bilingual text + chart | Img10 | stable |
| feature-grid | 2×2 cards, illustration + title + desc | Img11 | stable |
| terminology-cards | keyword illustration + term + def + example card | Img12 | stable |
| results-grid | hero metric + open supporting stats + quote band (A/B-validated open layout) | Img13 | stable |
| matrix | 2×2 framework | — | stable |
| case-study | card + timeline | — | stable |
| conclusion | 3 takeaway cards + band | — | stable |

## Components (atoms / molecules)
| id | what it is | learned_from | status |
|---|---|---|---|
| metric | big number + unit + caption | many | stable |
| metric-card | result card: title (accent metric phrase) + muted line + right-anchored topic icon | Img13 | stable |
| delta-metric | ±% headline + before/after grouped bars + legend; *delta pill* variant states the change at the bar on a dashed was-line | Img1, Ref-delta-pill-2026-09-03 | stable |
| barchart / hbar | vertical / ranked horizontal bars (1 active accent) | Img1,2,5,8,10 | stable |
| pie-donut | pie / donut with big % or center number | Img2,3,10 | stable |
| bubble-cluster | circles sized by magnitude | Img3 | stable |
| line-chart | trend over time | Img10 | stable |
| quote-bubble | speech bubble + avatar (qual quote) | Img4, Img7, Img23 | stable |
| cta-buttons | primary (filled) + secondary (outline) action pair | Img19 | stable |
| ui-mockup | product UI / device-screen mockup (browser · phone · skeleton) + six screen **interiors** (overview · form-summary · rail-rows · table · empty · specimen) | Img19, Img21, screen-interiors | stable |
| shot | rounded + soft-shadowed wrapper for any raw screenshot/photo | Img21, Img26 | stable |
| level-slider | labeled trait track with a level dot | Img22 | stable |
| geo-map | region map with leader-line annotations + counts | Img23 | stable |
| stat-bar | labeled before/after % bars | Img4 | stable |
| callout-band | highlighted band (HMW / key note) | Img3 | stable (insight band) |
| citation-card | finding + source | Img3 | stable |
| comparison-table | criteria × options, O/X or value, 1 col highlighted | Img9 | stable |
| ranked-list | 1순위/2순위/3순위 priority list | Img9, Img16 | stable |
| evidence-card | icon-stat / chart / logo-row variants | Img8 | stable |
| logo-row | source/tool/competitor logos | Img8,9 | stable |
| numbered-row | number badge + text (bilingual) + chart | Img10 | stable |
| feature-card | illustration-top + title + desc | Img11 | stable |
| terminology-card | illustration + term + def (+ example) | Img12 | stable |
| icon-label-row | icon + label list rows | Img6 | stable |
| chip / taglist | #tags / #Handle (中文) cluster — breadth as a shape | Img25 | stable |
| stepflow | ①→②→③ numbered flow | — | stable |
| lrow | labeled rows w/ optional 2-track split | — | stable |
| section-cover | dark announce page | — | stable |
| persona | persona card + avatar | — | stable |

## v12 — Reference-audit primitives (from a 38-slide capability audit; 2 FULL / 36 PARTIAL / 0 NONE)
CSS lives in `assets/base.css` ("v12 — Reference-audit primitives"). Added to close the recurring **layout** gaps (color was out of scope). Validated by composite render tests under `examples/case-study/_audit/`.
| id | what it is | closes (ref idx) | status |
|---|---|---|---|
| leader / leader-svg | export-safe SVG-overlay connector (%-anchored): vertical tether, elbow fan-out, curved growth arc, converge | 1,3,5,9,17,23,26,27,33,34,36 | stable |
| vtether | pure-CSS dashed vertical card→caption tether | 3,17,33 | stable |
| decor-layer / hero-cutout / bleed-shape / stage-backdrop / sticker | off-grid + edge-bleed decorative/hero layer (one sanctioned overlapping illustration) | 3,9,11,13,16,24,32,35,36 | stable |
| tbubble (tail-up/down/left/right) + react | speech bubble with directional CSS tail + emoji reaction slot | 1,7,32,35 | stable |
| qcascade / collage / overhang | staggered/zig-zag & free-scatter quote arrangements; avatar overhang | 7,16,35,37 | stable |
| anno-pin | positioned annotation pill/popup (over a mockup/chart) | 22,32 | stable |
| panel / splitpanel / ab-panel / statrail / split-2 + vrule | bounded panel wrapping a sub-composition; tonal split; equal-height as-is/to-be; hairline-split card | 4,9,21,26,28,32,37,38 | stable |
| funnel-merge / mergenode | many-peers→one-outcome converging wedge + seam merge node | 1,5,9 | stable |
| tracks / track (+connector-down) | N parallel columns each = card → vertical connector → band (1:1 paired ladder) | 9,10,17,38 | stable |
| barline + chart-annot + ln-area / ln-path.alt / ln-drop | bars + overlaid trend line in one plot; area fill; 2nd series; drop-line; in-chart floating callout | 1,27,28,33,34,36 | stable |
| babars (horizontal before/after) + deltametric.overline / axis-mid / slope / bubble-delta | horizontal before→after bars w/ trailing captions; centered delta; midline; proportional-circle delta | 25,29,30,31,34,36 | stable |
| phone / appframe / notch / screen / device-stack / popup / listrow / toggle | phone & app-frame device mockups, overlapping multi-device stage, in-screen UI kit | 7,11,12,23,24,26,32 | stable |
| ui-body / ui-split / ui-panel / ui-field / ui-cta / ui-metric / ui-bars / ui-tr / ui-rail / ui-empty / ui-matrix | screen **interiors** — the arrangement inside a frame that says which screen it is, not just which product | screen-interiors | stable |
| cards.four / col-3 / card.flat / cards.stagger / qstack / qcard | 4-up grid, flat/ghost dense cards, staggered row, nested quote-stack cards | 8,11,16,19,37,38 | stable |
| dash-link / node--dotted / thread | dashed "broken-path" connector, dotted circle node, decorative bleed thread | 1,5,10,19,24 | stable |
| splitbar / formula / needsrow | 2-segment 100% split bar; circle×circle=value arithmetic; overlapping mini-circle needs row | 3,4,37 | stable |
| psubhead / reaction / statbox / bilingual-lead | underlined sub-head; emoji+paragraph reaction; dotted mini-stat box; zh/en two-col intro caption | 6,17,28,38 | stable |
| radialmap / hub-circle / hub-mark / orbit-card | symmetric dual-hub ecosystem mind-map (text-bearing circle hubs + orbiting cards + curved dashed arcs) | 2 | stable |
| flow-node.dead / .toplabel | terminal/dead-end flow state + label-above-node slot | 10 | stable |
