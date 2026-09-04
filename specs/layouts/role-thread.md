---
id: role-thread
kind: layout
tier: organism
status: stable        # example built + render-validated
intent: show how one problem travelled across roles until it was understood, with each turn attributed to who said it
triggers: [how we found the cause, an incident walked through end to end, what each team saw, the handoff from monitoring to QA to the fix, a bug from detection to cause, who noticed it and who confirmed it, 我們是怎麼找到原因的, 這個問題怎麼一路查下去, 各角色分別看到什麼, 從偵測到修好的過程, 事故回顧, 크래시 재현 경로]
material: text-only
arrangement: rows
item_count: few
alternates: [event-sequence, painpoint-evidence, idea-evidence]
depends_on: [tokens]
tokens_used: [canvas, chip, surface, ink, muted, muted-soft, accent, accent-soft, warn, warn-soft, pos, pos-soft, neg, neg-soft]
icon_use: none
learned_from: Ref-role-thread-2026-09-03
example: examples/light-role-thread.html
---
# role-thread

## Purpose
A short thread in which each turn is attributed to the role that produced it, and one turn expands
into the evidence the thread was working towards.

## Intention & rationale
The job is to **make a cross-functional diagnosis legible as one story**. Why this form:
- **Attribution is the content, not decoration.** "The crash was reproducible" is a claim; "QA
  reproduced it by following that path" is a finding with an owner. Putting the role in a chip beside
  every turn means the audience reads the *handoff* — who noticed, who narrowed it, who confirmed —
  rather than a wall of undifferentiated quotes.
- **One turn is an artifact, not a sentence.** The moment a thread produces evidence — a reproduction
  path, a stack trace, a query — the evidence *is* that turn. Expanding it into a card and leaving the
  others as bubbles marks where the investigation actually turned, without a label saying so.
- **The failure is the only `neg` on the slide.** The reproduction path is a row of neutral steps
  ending in one terminal chip. Colouring the steps too would make the whole path look like the
  problem, when the point is that every step before the last one was ordinary.
- **Four role tints, and no more.** A fifth voice has to reuse a colour, which is the signal that the
  thread has more participants than one slide can attribute legibly — split it or summarise it.

## When to use / When NOT
Use for an incident or investigation retold across roles: detection → analysis → confirmation → fix,
a bug's life, a support escalation, any story whose point is that different people saw different parts.

**Not** for message passing between *systems* — that is `event-sequence`, where the parties are
components and the axis is order rather than authorship. **Not** for a complaint plus its supporting
data — that is `painpoint-evidence`. If nobody in the thread is a distinct role, the attribution
column is empty apparatus; use a plain list.

## Structure
- `.thr` — column of `.turn` rows.
- `.thr .turn` — `.who` chip then `.say`.
- `.thr .who` — the role. Add `.a` / `.w` / `.p` / `.n` to take the accent, warn, pos or neg role
  colour; unmodified it is muted. Assign them by *role*, consistently down the thread, never by mood.
- `.thr .say` — `.lbl` names the source (a tool, a channel, a person's function), then either a `.bub`
  for something said or a `.rcard` for evidence produced.
- `.thr .rcard` — `.rh` its title, `.rd` what it shows, `.rl` labelling the path, then `.path`.
- `.thr .path` — `.pstep` chips separated by `.sep`, with `.pstep.end` as the terminal state.

## Asset policy
`none` — chips, bubbles and the evidence card are drawn from tokens. No artwork is requested.
