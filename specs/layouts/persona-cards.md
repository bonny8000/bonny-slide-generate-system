---
id: persona-cards
kind: layout
tier: organism
status: stable        # example built + render-validated
intent: anchor design in real users and surface their pain points
triggers: [persona(s), user archetype, "two personas", behavior traits + pain points, a quote + profile, 使用者輪廓, 人物誌, 主要使用者與他們的困擾, 使用者樣貌]
material: quote+illustration
arrangement: grid
item_count: few
alternates: [use-case-cards]
depends_on: [persona, level-slider, chip, quote-bubble, tokens]
tokens_used: [canvas, surface, ink, muted, muted-soft, accent]
icon_use: required
learned_from: Img22
example: examples/light-persona-cards.html
---
# persona-cards

## Purpose
1–3 parallel persona cards: avatar + a defining quote + traits + pain points.

## Intention & rationale
The job is to **make the user real and surface the pain that fuels design**. Why this anatomy:
- **Avatar + a first-person quote** make the persona feel human, not a spec.
- **The quote accents the emotional crux** (intention → emphasis) so empathy lands on the right phrase.
- **Behavior `level-slider`s quantify traits at a glance**; **pain points** (accent-dot bullets) are the
  design fuel — they're why this persona is on the slide.

## When to use / When NOT
Use for research personas. **Not** for a single quote (use `quote-bubble`) or a stats dump.

## Structure
Eyebrow "Persona" + title (accent the discovered theme). 1–2 `--surface` persona cards, each:
**avatar** (illustration) + identity (name/age/role, `--muted`) + a big **quote** (accent the key phrase) +
**tag chips** + **"Story"** muted paragraph (bold accent on key phrases) + **"Behavior"** labeled
`level-slider`s + **"Pain point"** accent-dot bullets.

## Tokens used
canvas, surface (cards), ink (quote/headers), muted/muted-soft (story, identity, slider tracks), accent
(quote keyword, slider dot, pain-point dots, chips).

## Icon use
Required: one avatar per persona (illustration recolored toward palette, one style). Tag chips optional.

## Content rules
1–3 personas, parallel structure. One quote each (accent one phrase); 2–4 behavior sliders; ≤ 3 pain
points. Keep Story to ~3 short lines.

## Do / Don't
- **Do** keep cards parallel and the quote short.
- **Don't** let Story become a wall of text or use full-color stock avatars off-palette.

## Example
Two personas (student / office worker), each with a 3D avatar, an accented quote, behavior sliders, and
pain-point bullets (learned from Img22, structure only).
