# Spec template — every component & layout spec follows this

Front-matter (machine-readable) + fixed sections (so the agent parses reliably).

```
---
id: comparison-table            # kebab-case, == filename
kind: component                 # component | layout
tier: molecule                  # token | atom | molecule | organism | layout
status: stable                  # draft | stable | deprecated
intent: help the audience choose / justify a pick   # the communicative JOB this pattern does
triggers: [N options × criteria, "vs", "better than", a decision to defend]  # content that should summon it
depends_on: [card, tokens]      # lower-tier specs it composes/needs
tokens_used: [surface, ink, muted, accent, muted-soft]
icon_use: optional              # none | optional | required  (see foundations/iconography.md)
learned_from: Img9              # which real slide this pattern came from (if any)
example: examples/comparison-table.html
---
```

## Sections (in this order)
1. **Purpose** — one line: what this is for.
2. **Intention & rationale** — the communicative *job* this pattern does, and **why these components in
   this arrangement achieve it** (the component-usage ↔ intention link). This is the reasoning the system
   reuses; without it a spec is just decoration. See `foundations/learn-from-image.md`.
3. **When to use / When NOT** — the intention + content shape it fits (the `triggers`); what to use instead.
4. **Structure** — the slots/classes and how they nest (no colors here).
5. **Tokens used** — by name only. (Color comes from the deck theme.)
6. **Icon use** — if/how icons or illustration appear (style, size, color token).
7. **Variants** — sanctioned variations.
8. **Content rules** — length limits, bilingual handling, emphasis (accent on ONE keyword).
9. **Do / Don't.**
10. **Example** — link to a rendered HTML.

## Rule: specs are theme-agnostic
Never write a hex or a px color in a component/layout spec. Reference a token name; the theme supplies
the value. The audit rejects raw colors.
