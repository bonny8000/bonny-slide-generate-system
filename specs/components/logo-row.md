---
id: logo-row
kind: component
tier: atom
status: stable
intent: evidence what exists by showing the actual marks
triggers: [tools, competitors, sources, brands, "what's out there", comparison column headers, tech stack]
depends_on: [tokens]
tokens_used: [surface, muted, muted-soft]
icon_use: required
learned_from: Img8, Img9
example: examples/light-08-evidence-trio.html
---
# logo-row
## Purpose
Show a set of sources / tools / competitors as small marks.
## When to use / When NOT
Use to evidence "what's out there" or to head comparison columns. Not for general lists (use chips).
## Structure
A centered row of `logo` tiles (`--surface` + `--muted-soft` border), each holding a wordmark or mark.
## Tokens used
surface (tile), muted (mark), muted-soft (border).
## Icon use
Required — brand marks/logos. Keep them one visual weight; tint to monochrome where possible to respect
the palette. (In templates use neutral placeholder marks; real logos are the user's to drop in.)
## Content rules
≤ 5 tiles. Equal tile height. Don't add color that breaks the 4-color rule.
## Do / Don't
Do keep tiles uniform. Don't let bright multicolor logos hijack the slide's accent.
## Example
A row of app marks under "運動記錄 App 很多,但游泳…?" (Img8).
