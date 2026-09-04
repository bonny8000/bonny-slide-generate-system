---
id: practice-hero
kind: layout
tier: organism
status: stable        # example built + render-validated
intent: make a recurring practice feel real — show the people doing it, then the steps it runs through
triggers: [the ritual we put in place, a standing review and what happens in each round, our monthly cadence, the routine that stops it recurring, a recurring meeting and its agenda, the working agreement we now run, 我們建立了什麼樣的例行做法, 每個月的協同機制, 例行會議實際上在做什麼, 固定的檢視節奏, 정기 협의체]
material: illustration
arrangement: hero
item_count: few
alternates: [value-points, use-case-cards, service-flow]
depends_on: [tokens]
tokens_used: [canvas, chip, ink, muted, muted-soft, accent, accent-soft]
icon_use: none
learned_from: Ref-practice-hero-2026-09-03
example: examples/light-practice-hero.html
---
# practice-hero

## Purpose
One illustration of the practice as the anchor, a caption naming it, and the steps it runs beneath.

## Intention & rationale
The job is to **make a routine credible before explaining it**. Why this form:
- **A process described in three bullets sounds like a plan; a picture of people doing it looks like a
  habit.** The illustration is not decoration here — it is the claim that this actually happens, and
  the steps below are the evidence of what happens in it.
- **The role tags belong on the drawing, not in the steps.** Naming who is in the room at the moment
  the audience first looks at it settles the "is the right team involved" question silently, so the
  steps can be about the work rather than about attendance.
- **Steps are numbered and equal-width.** A recurring practice has no climax; each pass through it
  does all three. Weighting one would suggest the others are optional.
- **The caption sits between picture and steps** so the anchor is named before it is unpacked. Without
  it the illustration is a mood and the steps are an orphaned list.

## When to use / When NOT
Use for a ritual, cadence or working agreement the audience has to believe in: a standing review, a
triage rota, a monthly retro, a quality gate someone actually runs.

**Not** for a one-off process — that is `service-flow`. **Not** for selling capabilities, where each
point needs its own supporting evidence — that is `value-points`. **Not** for audience segments — that
is `use-case-cards`. If there is no practice, only a diagram, the illustration is decoration and this
layout is the wrong argument.

## Structure
- `.phero` — centred column: `.anchor` then `.steps`.
- `.phero .anchor` — the drawing and its caption together. They are wrapped because the column
  distributes its children: left loose, the caption drifts into the middle of the gap instead of
  staying under the picture it names.
- `.phero .stage` — the drawing plus its role tags. `.art` holds the SVG; each `.tag` is placed with
  `--x` / `--y` as percentages of the stage.
- `.phero .cap` — `.n` names the practice, `.d` gives its cadence in one line.
- `.phero .steps` — three `.stp` cards: `.k` the number, `.t` the step, `.d` what it produces.

## Asset policy
`generate` — this layout declares `material: illustration`, so an illustration is expected and may be
generated when the user supplies none. The shipped example draws it as inline SVG in `currentColor`
with `accent-soft` fills, per `foundations/imagery.md`: line art built from tokens is on-palette in
both themes, where a supplied raster is not. A supplied illustration drops into `.art` in its place.
The source figure used a full-colour 3D render; that palette is deliberately not carried over.
