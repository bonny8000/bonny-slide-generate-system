---
id: timeline
kind: layout
tier: organism
status: stable        # example built + render-validated
intent: set expectations over time — show the project/roadmap phases and their deliverables
triggers: [timeline, roadmap, Gantt, phases over dates, "journey", project plan, 時程, 專案階段, 各階段產出, 時間軸, 專案規劃]
material: text-only
arrangement: sequence-dated
item_count: few
alternates: []
depends_on: [logo-row, tokens]
tokens_used: [canvas, surface, ink, muted, muted-soft, accent, band-fill]
icon_use: optional
learned_from: Img24
example: examples/light-timeline.html
---
# timeline

## Purpose
A Gantt-style timeline: phases as staggered bars over a dated axis, with deliverables under each phase.

## Intention & rationale
The job is to **set expectations over time**. Why this form:
- **Staggered bars show sequence *and* overlap over real dates** — a flat list can't show duration or that
  phases overlap.
- **Deliverables under each phase** ground the plan in concrete outputs.
- **One accent marks the current/active phase**, so "where we are" is instantly clear.

## When to use / When NOT
Use for a roadmap, project plan, or process journey with dates. **Not** for a non-temporal sequence (use
`flow`) or a single milestone.

## Structure
Eyebrow + title; optional header **tools logo-row** + page number. A **dated axis** (vertical gridlines =
date columns, `--muted-soft`). **Staggered phase bars** (rounded, `--band-fill`/`--ink`) cascading across
their date span. Under each phase, a **bullet list of deliverables** aligned to its column.

## Tokens used
canvas, surface, ink (phase labels, bullets), muted/muted-soft (axis, gridlines), accent (active phase),
band-fill (phase bars).

## Icon use
Optional header logo-row (tools); brand logos keep real color (`foundations/imagery.md`).

## Content rules
4–6 phases; terse deliverable bullets aligned under their phase; dates on the axis.

## Do / Don't
- **Do** align deliverables under their phase column; accent only the active phase.
- **Don't** give each phase a different hue (use one band-fill + one accent).

## Example
"Timeline" — Research→Define→Ideate→Design→Test as staggered bars over Dec–Feb, deliverables listed under
each (learned from Img24).
