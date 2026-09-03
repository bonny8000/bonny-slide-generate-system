---
id: annotated-screen
kind: layout
tier: organism
status: stable        # example built + render-validated
intent: explain one screen part by part, anchoring each note to the place it applies
triggers: [explain each part of one screen, what every element on this screen does, callouts pinned to a screen, point at the parts of the interface, which rule applies where, walk through one screen element by element, node-level annotation of a UI, 逐一說明畫面各部位, 畫面元件逐項標註, 指出介面上的位置, 一個畫面拆開解說, 한 화면을 부분별로 설명]
material: ui-mockup
arrangement: centre-satellite
item_count: few
alternates: [feature-showcase, ui-mockup]
depends_on: [ui-mockup, tokens]
tokens_used: [canvas, surface, muted, muted-soft, ink, accent, on-accent, shadow-card]
icon_use: optional
learned_from: Ref-annotated-screen-2026-08-31
example: examples/light-annotated-screen.html
---
# annotated-screen

## Purpose
**One** screen, with several notes pinned to the exact parts they describe, plus a numbered legend that
carries the detail the pins are too small to hold.

## Intention & rationale
The job is to **make a mechanism legible by anchoring it to a concrete artefact**. Why this form:
- **A list of rules beside a screenshot forces the audience to map text onto location themselves.**
  Pinning each note where it applies removes that work, so the audience learns the mapping instead of
  decoding it.
- **The screen stays the subject.** Pins are `surface` on a hairline `muted-soft` border, so they read as
  annotation over the artefact rather than as competing cards.
- **Exactly one pin takes `accent`** — the part the page is actually claiming something about. More than
  one accent and the eye has nowhere to land.
- **The legend absorbs the detail.** Pins carry a label; anything longer (an identifier, a rule number,
  a reason) belongs in the numbered legend beside the stage, so the leader lines stay short.

## When to use / When NOT
Use when the content is **one** interface and **several** things to say about **specific locations in it**
— an engine explaining where it acted, a component audit, a spec walkthrough.

**Not** for two or more separate feature areas each with one caption — that is `feature-showcase`, whose
annotations sit *below* each screen rather than pinned inside one. **Not** for a screen shown whole with
no part-level claim — that is `ui-mockup` inside whatever layout owns the page. **Not** for a real
supplied screenshot that must be interpreted in conversation — that is the `ui-qa` explainer route.

## Structure
- `.ascr` — flex row: the stage, then the legend.
- `.ascr .stage` — positioning context; holds the built screen (`ui-mockup` primitives: `.phone` /
  `.appframe` / `.sk`). Pins and leaders are absolutely positioned against it.
- `.ascr .pin` — a pinned note: `.t` label, optional `.d` detail. `.accent` marks the one being claimed.
- `.ascr .leader` — a dashed rule from pin toward its anchor; the author sets `width` and
  `transform:rotate()` inline, the same way `.anno-pin` takes inline offsets.
- `.ascr .legend` — numbered rows (`.lnum` / `.ltext`) carrying the longer explanation.

## Asset policy
`build` — the screen is schematic, assembled from `base.css` primitives per `components/ui-mockup.md`.
Never ask the user for artwork, and never drop the layout for lacking a screenshot. A page that must
show a *real* product screen is a different route.
