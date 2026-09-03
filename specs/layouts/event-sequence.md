---
id: event-sequence
kind: layout
tier: organism
status: stable        # example built + render-validated
intent: show the ordered exchange between several components, and mark the stretch of it that carries the argument
triggers: [who calls whom and in what order, the order these components talk to each other, the calls between services in the order they fire, a handshake, a protocol exchange, an event lifecycle, message passing between components, 呼叫順序, 服務之間互相呼叫, 元件之間互相影響的順序, 事件依序觸發, 訊息往返, 誰先呼叫誰, 시퀀스, 주고받는 이벤트]
material: text-only
arrangement: sequence-actors
item_count: many
alternates: [service-flow, numbered-rows, timeline]
depends_on: [tokens]
tokens_used: [canvas, chip, surface, ink, muted, muted-soft, accent, accent-soft]
icon_use: none
learned_from: Ref-event-sequence-2026-09-03
example: examples/light-event-sequence.html
---
# event-sequence

## Purpose
Several named actors across the top, time running down, and one row per message between them — with
one stretch of that order banded as the part that matters.

## Intention & rationale
The job is to **make an invisible exchange auditable**. Why this form:
- **Actors are columns, so the cast is fixed before the story starts.** The audience learns who is in
  the system once, at the top, and never has to re-parse it while following the order.
- **Time is the vertical axis, so order is read, not inferred.** A flowchart shows that A can reach B;
  this shows that A reached B *third*. When the question is "what happened, in what order", that
  difference is the whole answer.
- **Direction is carried by the arrowhead, not by position.** A reply travelling right-to-left is the
  same weight of line as the call that provoked it, so a round trip reads as one exchange rather than
  as two unrelated steps.
- **An internal action is a chip on its own lifeline, never an arrow.** Something an actor does to
  itself is not a message; drawing it as one would invent a party that was never involved.
- **The phase band is the argument.** A sequence with every step equally weighted is a transcript, not
  a point. Banding the stretch that matters — the moment the ad renders, the window where the crash is
  reproducible — says which part of the order the audience is meant to leave with.

## When to use / When NOT
Use when the content **is** an ordered exchange between named parties: a protocol, a handshake, an
event lifecycle, a request travelling through several services, a bug reproduced across components.

**Not** for a process with branches and decisions — that is `service-flow`, which can show a diamond
this cannot. **Not** for a small linear list of stages with no senders and receivers — that is
`numbered-rows`. **Not** for work scheduled against dates — that is `timeline`. If the exchange has fewer
than about four messages, the cast row costs more than the ordering earns; use `numbered-rows`.

## Shape
`arrangement: sequence-actors`, not plain `sequence`. `service-flow` already owns
`text-only / sequence / many`, and a shape collision is not a tie the router can break: with the
same three tags a user-journey request resolved to both at once. The axis here is *who*, not just
*when*, which is the same reason `timeline` declares `sequence-dated`.

## Structure
- `.seq` — column: `.cast` then `.track`. Set `--seq-cols` to the number of actors on `.seq`; every
  layer reads it, so one number keeps the whole diagram aligned.
- `.seq .cast` — one `.actor` per column: `.n` for the name, `.r` for its one-line role.
- `.seq .track` — the message area. It distributes its rows over the remaining height, so the diagram
  fills the canvas rather than bunching under the cast.
- `.seq .lanes` — the dashed lifelines, one `.lane` per actor, in a layer behind the messages.
- `.seq .msg` — one message. `--from` is its starting column and `--span` how many columns it crosses;
  `.t` is the label and `.a` the arrow. Add `.back` for one travelling right-to-left.
- `.seq .self` — an internal action, placed on a single lifeline with the same `--from` / `--span`.
- `.seq .pband` — the banded stretch, spanning the full width with `.pl` as its label. Messages inside
  it take the band's accent colour so the phase reads as one passage. Repeat `.lanes` inside it: the
  band paints over the track's lifelines, and a sequence whose lifelines stop at the band reads as
  though the actors left the diagram for its duration.

## Asset policy
`none` — lifelines, arrowheads and the band are drawn from tokens and CSS. No artwork is requested.
