# Spec template — every component & layout spec follows this

Front-matter (machine-readable) + fixed sections (so the agent parses reliably).

```
---
id: comparison-table            # kebab-case, == filename
kind: component                 # component | layout
tier: molecule                  # token | atom | molecule | organism | layout
status: stable                  # draft | stable | deprecated
depends_on: [card, tokens]      # lower-tier specs it composes/needs
tokens_used: [surface, ink, muted, accent, muted-soft]
icon_use: optional              # none | optional | required  (see foundations/iconography.md)
learned_from: Img9              # which real slide this pattern came from (if any)
example: examples/comparison-table.html
---
```

## Sections (in this order)
1. **Purpose** — one line: what this is for.
2. **When to use / When NOT** — the content shape it fits; what to use instead.
3. **Structure** — the slots/classes and how they nest (no colors here).
4. **Tokens used** — by name only. (Color comes from the deck theme.)
5. **Icon use** — if/how icons or illustration appear (style, size, color token).
6. **Variants** — sanctioned variations.
7. **Content rules** — length limits, bilingual handling, emphasis (accent on ONE keyword).
8. **Do / Don't.**
9. **Example** — link to a rendered HTML.

## Rule: specs are theme-agnostic
Never write a hex or a px color in a component/layout spec. Reference a token name; the theme supplies
the value. The audit rejects raw colors.
