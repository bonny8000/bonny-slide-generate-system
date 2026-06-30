---
id: cta-buttons
kind: component
tier: atom
status: stable        # example built + render-validated
intent: offer one clear primary action plus a quieter secondary
triggers: [CTAs, landing actions, "buttons", a next step + an alternative]
depends_on: [tokens]
tokens_used: [ink, canvas, surface, muted, accent]
icon_use: optional
learned_from: Img19
example: examples/light-product-hero.html
---
# cta-buttons

## Purpose
A primary + secondary action pair.

## Intention & rationale
The job is to **make the next step obvious without two competing weights**: one filled primary (the action
you want) and one quiet secondary (the alternative). Two filled buttons would compete; an unstyled link
would be missed.

## Structure
Side by side, primary first. **Primary** = filled (`--ink` or `--accent`) with contrasting label + optional
trailing chevron. **Secondary** = outline/ghost (`--muted` border, `--ink` label) + optional send/arrow icon.

## Tokens used
ink / accent (primary fill), canvas (primary label), muted (secondary border), ink (secondary label).

## Icon use
Optional small trailing icon, one style.

## Content rules
Exactly one primary. Short verb labels (繁中 + optional EN handle).

## Do / Don't
- **Do** keep one primary; align heights.
- **Don't** make both filled or add a third button competing for attention.

## Example
"查看方案 ›" (filled) + "企業導入諮詢 ✈" (outline) (learned from Img19).
