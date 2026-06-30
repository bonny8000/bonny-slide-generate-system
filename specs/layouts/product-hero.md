---
id: product-hero
kind: layout
tier: organism
status: stable        # example built + render-validated
intent: present the product itself — what it is and what it does — like a landing hero
triggers: [product intro, landing/hero, value proposition + CTAs, a product UI to show off, proof stats]
depends_on: [cta-buttons, ui-mockup, metric, tokens]
tokens_used: [canvas, surface, ink, muted, muted-soft, accent]
icon_use: optional
learned_from: Img19
example: examples/light-product-hero.html
---
# product-hero

## Purpose
A landing-style hero: a value-prop headline + CTAs + proof stats, with the real product UI as the visual.

## Intention & rationale
The job is to **make "what this is" tangible**. Why this form:
- **The product shot is the hero** — showing the actual UI proves the thing exists and looks usable, which
  a description can't.
- **A few proof stats** (50+, 70%, AI) give instant credibility beside the pitch.
- **The headline carries the value prop** with one accent phrase; a **primary + secondary CTA** gives one
  obvious next step plus a quieter alternative.

## When to use / When NOT
Use for a product/landing intro or a "here's the product" slide. **Not** for a single metric (use `metric`)
or a feature deep-dive (use `feature-showcase`).

## Structure
Optional top nav (logo + menu + login pill). Hero: **headline** (value prop, one `--accent` phrase) + muted
sub; **`cta-buttons`** (primary + secondary); an inline **stat trio** (`metric` ×3 — small caption over big
value) top-right. Below: a **`ui-mockup`** (dashboard/skeleton) as the hero visual. Optional bottom
**tab/stepper row** (3–4 captions; active = `--accent`, bold + underline).

## Color
Secondary-category cards (e.g. an HR panel) use **neutral / `--accent-soft` tints**, not a second hue.
Playful floating icons are a landing-tone option only — keep "purposeful, one style" (`foundations/iconography.md`).

## Tokens used
canvas, surface (mockup + cards), ink (headline), muted/muted-soft (sub, captions, skeleton), accent
(headline keyword, active tab, active UI element).

## Icon use
Optional; nav/CTA icons one style. Avoid scattering decorative glyphs.

## Content rules
One value-prop headline (accent one phrase); ≤ 3 stats; exactly one primary CTA + one secondary.

## Do / Don't
- **Do** let the product shot lead; keep one primary CTA.
- **Don't** add a 2nd chromatic color for category cards or scatter decorative icons.

## Example
"易用的 ERP SaaS" hero: headline + 2 CTAs + 50+/70%/AI stats + a dashboard mockup + a 4-item tab row
(learned from Img19, structure only).
