---
id: service-flow
kind: layout
tier: organism
status: stable        # example built + render-validated
intent: orient the audience to how the service works — the end-to-end flow and decision paths, grouped by user segment
triggers: [flowchart, 流程圖, decision diamonds, branches, swimlanes by user type, start → ends, an end-to-end process shown whole, 服務流程, 整體流程, 端到端流程, 從頭到尾, 플로우]
material: text-only
arrangement: sequence
item_count: many
depends_on: [tokens]
tokens_used: [canvas, surface, ink, muted, muted-soft, accent, accent-soft]
icon_use: optional
learned_from: Img14
example: examples/light-service-flow.html
---
# service-flow

## Purpose
A full service/decision flow: a start node branching through decision diamonds and process boxes to
several ends, with the flow grouped into regions by user segment.

## Intention & rationale
The job is to **make the logic walkable** — the audience traces the system node by node instead of being
told to trust it. Why the parts are arranged this way:
- **Regions group paths by who they're for**, so a busy diagram still answers "which part is about which
  user."
- **One accent marks the start / the focus path**, so the eye knows where to begin and isn't lost in a
  dense chart.
- **Decision diamonds expose the branches** — showing the choices is what makes it a *flow*, not a list.

## When to use / When NOT
Use to show an end-to-end service flow, onboarding logic, or a decision tree, especially when it differs
by segment. **Not** for a simple linear 3-step process (use `flow`/`stepflow`) or a non-branching list.

## Structure
1. Eyebrow + plain title + muted intro line.
2. **Legend:** the N segments, each a tinted swatch + label.
3. **Flow canvas:** start node (accent pill) → process boxes (`--surface`) → decision diamonds (outline),
   joined by `--muted` directional arrows; nodes grouped into **tinted regions** per segment; optional
   **speech-bubble callouts** (surface tint) annotating key nodes.

## Color (resolving the reference's multi-hue coding)
Img14 codes 3 segments with 3 hues — that breaks the 4-color rule. In this system, differentiate regions
with **neutral surface tints** (`--surface` / `--accent-soft` / `--muted-soft` — variations in lightness),
**not** chromatic hues, and keep the single `--accent` for the primary path / start node / focus region
(see `foundations/color-discipline.md` → Categories).

## Tokens used
canvas, surface (nodes), muted/muted-soft (arrows, inactive nodes, region tints), ink (labels), accent +
accent-soft (start node, primary path, focus region).

## Icon use
Optional small wayfinding glyphs/avatars, one style, theme-colored; drop any that just repeat a label.

## Content rules
Terse node labels (繁中). ≤ ~3 regions, one start, always-directional arrows. If it's too dense to read at
slide size, summarize or split — legibility beats completeness.

## Do / Don't
- **Do** use surface tints for categories + one accent for the focus path.
- **Don't** give each branch its own hue (breaks the 4-color rule) or shrink labels below legibility.

## Example
"Service Flow" — start "首頁" branching by 3 subscriber types into region-tinted paths with callouts
(learned from Img14, Korean reference, structure only).
