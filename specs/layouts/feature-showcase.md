---
id: feature-showcase
kind: layout
tier: organism
status: stable        # example built + render-validated
intent: show how specific UI features deliver value / resolve user anxieties
triggers: [feature areas, app screens to show, "this screen does X", annotated UI, a detail page walkthrough, 功能畫面解說, 這個畫面能做什麼, 標註過的介面, 功能如何化解不安]
material: ui-mockup
arrangement: split
item_count: pair
alternates: [feature-grid]
depends_on: [ui-mockup, quote-bubble, tokens]
tokens_used: [canvas, surface, muted, muted-soft, ink, accent, band-fill]
icon_use: optional
learned_from: Img21
example: examples/light-feature-showcase.html
---
# feature-showcase

## Purpose
Two (or more) feature areas, each shown with real UI mockups and annotations tying screens to value.

## Intention & rationale
The job is to **make a feature concrete and show what it's for**. Why this form:
- **Real UI (device mockups) makes the feature tangible** — the audience sees it, not a description.
- **Annotations tie a specific UI element to the value it delivers** (e.g. a "verified" badge → "removes
  pre-meeting anxiety").
- **Header bands chunk the screen** into scannable feature areas so two ideas don't blur together.

## When to use / When NOT
Use to walk through key screens / features of a product. **Not** for a single hero shot (use
`product-hero`) or non-UI content.

## Structure
Eyebrow + title. 2 feature areas, each under a **header pill band** (`--band-fill`); inside: **`ui-mockup`**
(phone/screen) + a small heading + muted desc + **annotation callouts** (badge/bubble) pointing at UI
elements. Separate the two areas by **surface tone** (a bright area vs a muted/quiet one).

## Tokens used
canvas, surface (mockups), muted/muted-soft (descriptions, quiet panel), ink (headings), accent (one
highlighted UI element / annotation), band-fill (header bands).

## Icon use
Optional; annotation badges one style, theme-colored.

## Content rules
≤ 2–3 feature areas; each mockup paired with a one-line value; annotations terse. Separate areas by tone,
not by a new hue.

## Do / Don't
- **Do** annotate the specific UI element that delivers the value.
- **Don't** crowd more than ~2 device mockups per area.

## Example
"聚會詳情頁" with a language-level area (phone + donut card) and a profile area (dark panel, profile
screens + a "verified" badge callout) (learned from Img21, structure only).
