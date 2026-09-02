# Content → slide map (the "make a slide" engine, stage 2)

Stage 1 (`slide-plan.md`) already named each page's **intention** (its communicative job) and **one claim**.
Here in stage 2, for each planned page: match it to a **shape**, then use the mapped layout + components.
**Shape is the index key; intention decides between the candidates it returns** — this mirrors
`selectionPolicy.primaryKey` in `system/router.json`, which is `shape`. Intention still carries the
design weight: the same raw text can become a different slide depending on what the page is trying to
*do*. Shape narrows the choice; intention picks the winner.

| Intention (the job) | Content shape | How to detect it | Layout | Key components | Icon/illustration |
|---|---|---|---|---|---|
| Make one idea land / commit the room | Single big claim / thesis | one sentence meant to land | `statement` | enlarged headline (32–36px) + 1 keyword in accent | none |
| Establish shared vocabulary / teach a term | Definition / concept set | "X means…", a few terms | `terminology-cards` | terminology-card (illustration + term + def) [+ example card] | keyword illustration |
| Help the audience choose / justify a pick | Comparison of options | N options × criteria, vs, "better than" | `comparison` | comparison-table (criteria×options, O/X or value, 1 column highlighted) | option logos/icons in header |
| Show coverage / breadth of what exists | Flat list of items | bullets, tags, "we have…" | `card-grid` or inline | chip / taglist / feature-card | optional icon per item |
| Show how it works / movement over steps | Process / sequence / before→after | arrows, "first…then", "as-is/to-be" | `flow` | stepflow (①→②→③) / flow-row | small step icons |
| Orient to how it works / walk the logic | Service flow / flowchart | decision diamonds, branches, swimlanes by user type | `service-flow` | flow nodes + connectors + region tints + callouts | small wayfinding icons |
| Contrast the problem with the solution | Problem ↔ solution (as-is/to-be) | two opposing states, pain → fix | `problem-solution` | two mirrored panels (muted vs bright) + badge + accent-dot lines | optional |
| Show standing + the target to move to | Positioning / perceptual map | 2 dimensions low↔high, option markers, a goal point | `positioning-matrix` | 2×2 axis cross + logo/dot markers + target (accent dashed ring) | brand logos as markers |
| Show parts connect into one whole | Connected concepts / continuum | overlapping circles, "connected", TX/total-X | `linked-circles` | enclosing container + 3–5 overlapping circles + accent labels | none |
| Prove impact with one number | Single metric / KPI | one number that matters | `metric` or evidence card | metric / delta-metric (±% + before/after bars) | optional stat icon |
| Prove several outcomes / show what was achieved | Results / achievement board | "results"/"成果", a flagship before→after + 2–3 outcome metrics each w/ a one-line reason | `results-grid` | metric-card ×N + delta-metric (before/after bar) | right-anchored topic icon per card |
| Let the data argue / show distribution | Several data points | charts, %, counts | `data` | barchart / hbar / pie-donut / line / bubble-cluster | none (let data speak) |
| Summarize what users said, at scale | Survey / Q&A results | repeated questions + answers | `survey-stack` | q-card (question + chart + 1-line insight); left rail = sample stats | Q badges |
| Earn the conclusion (problem → insight) | Research story | background → problem → insight | `research-flow` | data cards → callout-band (HMW) → citation-card | none |
| Make it both felt and proven | Qual + quant together | quotes AND numbers | `qual-quant-split` | quote-bubble (+avatar) \| stat bars | avatar icons |
| Teach how to run a workshop activity in a human way | Timing rail + facilitator/assistant Q&A + rules/output | agenda, duration, rounds, breaks, prompts, voting, grouping, discussion rules | `editorial-explainer-stage` · `agenda-dialogue` | freshly generated full-block editorial explainer + native copy zones | **required:** image generator with workshop references; never reuse/trace them |
| Humanize a worked example or assistant-led operating flow | Human prompt(s) → assistant action → governed outcome | “say these lines”, chat-driven workflow, owner asks an assistant, assistant opens PR/updates status, human approval checkpoints | `editorial-explainer-stage` · `guided-dialogue` | freshly generated dialogue stage + native editable prompts/outcomes | **required:** image generator with workshop/dialogue references; never rebuild as speech-card CSS |
| Turn scattered inputs into one shared outcome (viewpoints→intent, or tools/roles→one pipeline) | Inputs → central transformation workflow → shared direction/output | problems, observations, limits, expectations, multiple voices, alignment, co-creation, explicit next step; **also** several tools/roles/steps converging into one process, a handoff chain, "X does A → Y does B → everyone gets C" governance flows | `editorial-explainer-stage` · `workflow-transform` | freshly generated full-block editorial explainer + native copy zones | **required:** image generator with workflow reference; never reuse/trace it. Data-precise pipelines (exact states, inspectable nodes) stay native `flow` |
| Explain a real UI through a participant/assistant conversation | Real supplied screenshot + interpretive Q&A | user tries to understand screen, steps, locked states, hierarchy, or likely action | `editorial-explainer-stage` · `ui-qa` | real screenshot on left + generated conversational explainer on right | **required:** real screenshot + image generator with UI-Q&A reference; never fabricate UI |
| Set expectations over time | Timeline / roadmap | phases over time | `timeline` | numbered-row / phase markers | phase markers |
| Reveal structure / how parts nest | Hierarchy / IA / structure | tree, nesting, sitemap | `hierarchy` | indented nodes / tree | node icons |
| Add a human voice / credibility | Quote / testimonial | attributed sentence | `quote` | quote-bubble + avatar | avatar |
| Anchor design in a real user | Persona | a user archetype (1 or several) | `persona-cards` | persona card(s): avatar + quote + chips + behavior sliders + pain points | avatar/illustration |
| Show how things connect / constrain | Relationships / dependency | "depends on", "in parallel" | `relations` | relationship triplet (前後 / 相依 / 並行) | small flow icons |
| Back a claim with sources / build trust | Citations / evidence | findings + sources | `citations` | citation-card (finding + source) | none |
| Converge multiple proofs on one point | 3 parallel evidence types | a stat + a chart + logos | `evidence-trio` | evidence-card ×3 (icon-stat / chart / logo-row) | stat icon + logos |
| Open a section / provoke thinking | Centered framing question | a question to anchor a section | `centered-question-evidence` | big centered question + 3 `evidence-card`s (icon-stat · chart · logo-row) | optional |
| Explain a few points, each with proof | Numbered explainer rows | 1/2/3 points, each w/ a chart | `numbered-rows` | numbered-row (badge + bilingual text + chart) | number badges |
| Present the product itself | Product hero / landing | a product to introduce, value prop + CTAs + a UI to show | `product-hero` | cta-buttons + metric ×3 + ui-mockup + tab row | optional landing icons |
| Present a few parallel values | Value / keyword cards | 3–4 principles/keywords each w/ a short blurb | `keyword-cards` | numbered value cards | optional |
| Show features via real UI | Feature showcase | app screens to walk through, annotated UI | `feature-showcase` | ui-mockup (phone) + header bands + annotation callouts | annotation badges |
| Explain one screen part by part | Annotated single screen | several notes about specific places in ONE interface; "what does each part do", rule/spec walkthrough | `annotated-screen` | ui-mockup (phone) + pinned notes + dashed leaders + numbered legend | optional |
| Stop a small number being dismissed | Proportion whose remainder is hidden | "only 1% so far", staged rollout, the rest have not received it yet | `hidden-majority` | waterline + warn-tinted visible tip + submerged mass on accent-soft | none |
| Teach how to use / onboard | Product UI + how-to | "how to use", "getting started", first-run | `annotated-screenshot` | hero ui-mockup **anchored on a soft stage** + 3 numbered callout pins (`.callp`/`.anno-pin`) placed ON the relevant UI regions; reserve a detached step list only when steps aren't tied to one screen | numbered callout pins |
| Back a pain point with evidence | Painpoint evidence | "painpoint", problem + user quotes / geographic concentration | `painpoint-evidence` | quote-bubble row + geo-map | participant avatars |
| Justify "why us" with backed points | Value / why-us points | "why X?", 2–3 points each w/ a backing card | `value-points` | accent-dot label + paragraph + taglist | optional |
| Show who it serves (use cases) | Use-case cards | "use cases", audience segments each w/ an illustration | `use-case-cards` | badge + illustration/mockup + caption | one illustration style |
| Contrast current vs improved screens | As-is → To-be (screens) | before/after of a UI + annotations | `as-is-to-be` | ui-mockup ×2 (muted vs accent) + annotation callouts | optional |
| Say which screen the audience is looking at | Screen interior | a mock whose *type* carries the argument — an overview, a checkout, settings, an empty state, a component sheet | any layout taking `ui-mockup` | ui-mockup chrome + one C17 interior (`overview` · `form-summary` · `rail-rows` · `table` · `empty` · `specimen`), one accent per frame | optional |
| Re-orient / mark a new part | Section transition | "now part 2 of 3" | `section-cover` (扉頁) | section-cover (small nav + hero title) | none |
| Set the map up front | Agenda | the outline | `toc` | numbered outline | none |
| Present a small set of features as equals | Feature set / capability grid | 3–4 features, "what's included", capabilities each w/ an icon + blurb | `feature-grid` | feature-card ×3–4 in a 2×2 / 2×N grid | one icon or illustration per card |
| Put one concept at the centre with its facets around it | Core concept + radiating facets | a center-out model, "X connects A/B/C/D", a framework hub | `hero-radial` | central accent node + radial facet labels + two side list-cards | optional facet icons |
| Pair a design idea with the evidence backing it | Idea ↔ proof (two column) | "we think X — here's why", an idea/claim + a supporting chart or stat | `idea-evidence` | idea panel (+ small chart) \| survey stat + reasoning panel | none (let the chart speak) |
| Converge several interview groups into one insight | Interview / affinity synthesis | interview groups or segments, affinity mapping, "across N groups we heard…" | `interview-affinity` | persona//group columns (avatar + reasons) → shared insight band | participant avatars |
| Rank what matters most | Prioritized needs / requirements | priority list, ranked needs, top-N requirements, 第一優先/第二優先 | `comparison` or a side panel | `ranked-list` (explicit rank order) | none |
| List short items each with a visual anchor | Icon + label list | categories, audiences, capabilities, 6 one-liners | `card-grid` or a side rail | `icon-label-row` (icon 20–24px + label) | required — one icon per row |

**Selection rule:** start from the page's **intention** (from `slide-plan.md`), then match the shape.
Prefer the most specific shape. If two fit, pick the one whose **intention matches the page's job** — and
between equals, the one with a concrete visual (chart/table/illustration) usually wins over plain cards,
because it carries more meaning per slide.

`editorial-explainer-stage` wins when the stage-1 gate is `yes`. The hard-candidate triggers above must not be
silently downgraded to `flow`, `numbered-rows`, or native speech cards merely because those are easier to build.
It requires a fresh image-generator
call and is not a synonym for drawing with HTML, CSS, SVG, or native cards. `ui-qa` additionally requires a
real screenshot. Use native layouts when exact nodes/data must remain inspectable; use the generated route
when the human explanation is the point.

**Reverse use (imagining content for a layout):** every learned layout records the intention it serves
and the triggers that should summon it (see `foundations/learn-from-image.md`). So when new content shows
that intention, the planner can reach straight for the layout — this table is read both directions.
