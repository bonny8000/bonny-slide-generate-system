---
id: quote-bubble
kind: component
tier: molecule
status: stable        # example built + render-validated
intent: carry a user's voice (a qual quote) with attribution
triggers: [a user quote, testimonial, participant voice, interview snippet, several voices as evidence]
depends_on: [tokens]
tokens_used: [surface, ink, muted, accent]
icon_use: optional
learned_from: Img4, Img7, Img23
example: examples/light-painpoint-evidence.html
---
# quote-bubble

## Purpose
A speech bubble carrying a short user quote, with an avatar + attribution.

## Intention & rationale
The job is to **add a real voice** — credibility a paraphrase can't give. The **accent on the emotional
crux** makes the point land; the **avatar humanizes** the data. Used singly for one voice, or as a **row of
several** to show a pattern across participants (evidence).

## Structure
A `--surface` speech bubble: the **quote** (`--ink`, accent the key phrase) + an **avatar** (illustration or
photo) + a small **label** (name/role, `--muted`). For evidence, place 3–4 in a row, parallel.

## Tokens used
surface (bubble), ink (quote), muted (attribution), accent (key phrase).

## Icon use
Optional avatar; illustrated avatars recolored toward palette (one style); real photos kept as content.

## Content rules
Keep the quote short (one breath); accent one phrase. Attribution = name/role or "참가자 A". In a row, keep
all bubbles the same size.

## Do / Don't
- **Do** accent only the emotional/key phrase; keep quotes terse.
- **Don't** recolor a real photo; don't let a quote run to a paragraph.

## Example
Four participant quote-avatars in a row as painpoint evidence (Img23); a quote beside a persona (Img4, Img7).
