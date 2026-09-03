---
id: system-anatomy
kind: layout
tier: organism
status: stable        # example built + render-validated
intent: show what a system is made of — which parts are peers, which part lives inside another, and what passes between them
triggers: [what are the pieces of this system and how do they fit together, what this is built from, which piece is hosted inside another, which component lives inside which, the stack a feature runs on, an architecture overview, the anatomy of the thing we built, what sits between the app and the server, 系統結構, 架構圖, 這個東西由哪些元件組成, 哪一層包在哪一層裡面, 跑在哪一層裡面, 各元件之間傳遞什麼, 구조, 아키텍처]
material: text-only
arrangement: nested-blocks
item_count: few
alternates: [service-flow, event-sequence, linked-circles]
depends_on: [tokens]
tokens_used: [canvas, chip, surface, ink, muted, muted-soft, accent, accent-soft]
icon_use: none
learned_from: Ref-system-anatomy-2026-09-03
example: examples/light-system-anatomy.html
---
# system-anatomy

## Purpose
The parts of a system laid out as peers on one rail, with the part that hosts a subsystem holding it
visibly inside, and numbered connectors naming what passes between each pair.

## Intention & rationale
The job is to **establish the cast and the boundaries before anyone explains behaviour**. Why this form:
- **Containment is shown by nesting, never claimed by a label.** "The bridge runs inside the webview"
  is a sentence the audience has to take on trust; a bridge drawn inside the webview is a fact they can
  see. Every later explanation can then point at the picture instead of re-establishing the boundary.
- **Peers sit at equal width so the eye does not rank them.** The one exception is the host, which is
  wider — not because it matters more, but because it has to hold a subsystem legibly. It keeps the
  same surface as the other peers: tinting it too would claim the containment a second time, and the
  nesting has already said it.
- **Connectors are their own cells, not borders.** A request and its response are two numbered steps
  between the same pair; drawing one arrow between two blocks loses the round trip.
- **The numbers give an order without making the layout about time.** This is a map, and the numbering
  is an overlay on it — which is exactly the division of labour with `event-sequence`, where order is
  the axis itself.

## When to use / When NOT
Use when the question is **what the thing is made of**: an architecture overview, a "which layer lives
inside which" explanation, the components a feature is assembled from.

**Not** when the question is what happened in what order between named parties — that is
`event-sequence`, which has a time axis this deliberately does not. **Not** for a process with
decisions and branches — that is `service-flow`. **Not** for one hub with satellites around it — that
is `linked-circles`. If nothing nests inside anything, this layout's whole argument is unused; a plain
row of cards says the same thing with less apparatus.

## Shape
`arrangement: nested-blocks`. The distinguishing feature is not that items sit in a row — many layouts
do — but that one of them **contains** another level. That containment is what the shape has to carry,
otherwise the router cannot tell this from any other row of peers.

## Structure
- `.anat` — the panel: `.cap` then `.rail`.
- `.anat .cap` — `.n` names the system, `.d` says how to read the diagram (e.g. what the numbers mean).
- `.anat .rail` — alternating `.blk` and `.link` cells, in reading order.
- `.anat .blk` — one part: `.n` its name, `.d` its one-line job. Add `.host` to the one that nests a
  subsystem.
- `.anat .blk.host > .grp` — the contained subsystem: `.gn` labels it, then `.mem` members, with
  `.bidi` between two members that talk both ways.
- `.anat .link` — a connector between the two blocks it sits between. It holds one or more `.step`,
  each with `.num`, a `.t` label and a `.dir` arrow, so opposite-travelling steps stay separate.

## Asset policy
`none` — blocks, nesting and connectors are drawn from tokens and CSS. No artwork is requested.
