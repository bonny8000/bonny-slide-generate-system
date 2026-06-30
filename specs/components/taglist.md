---
id: taglist
kind: component
tier: atom
status: stable        # example built + render-validated
intent: show breadth/coverage as a cluster of small labels
triggers: [many categories/tags, "#handles", a capability/coverage list, chips, "we cover all of these"]
depends_on: [tokens]
tokens_used: [surface, ink, muted, muted-soft, accent]
icon_use: none
learned_from: Img25
example: examples/light-value-points.html
---
# taglist (chips)

## Purpose
A wrapped cluster of chips showing many items at once — breadth as a shape.

## Intention & rationale
The job is to **make "there are many" visible at a glance**. A cluster reads as coverage instantly; chips
keep each item terse; the **accent stays on the count/title**, not on every chip (else the eye lands
nowhere).

## Structure
A wrapped cluster of **chips** (pill: `--muted-soft`/`--surface` fill, `--ink`/`--muted` text), grouped in a
card with an optional title (accent the count/keyword). Chips equal height, wrapping to rows.

## Tokens used
surface (card), muted-soft (chip fill), ink/muted (chip text), accent (title count/keyword only).

## Icon use
None.

## Content rules
Terse chip labels (繁中 or Latin). Don't accent individual chips; group under one title. Let the cluster
show breadth — don't trim it to look tidy if breadth is the point.

## Do / Don't
- **Do** keep chips uniform; accent only the count/title.
- **Don't** color individual chips or let a label wrap to two lines.

## Example
"Video **Categories**" and "**9,000+** Influencers" chip clusters (learned from Img25).
