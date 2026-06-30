---
id: token-reference
kind: token
status: stable
---
# Token reference — the contract components depend on

Components/layouts use these **names**; the active theme supplies the values. Never hardcode a color.

| token | role |
|---|---|
| --canvas | page background |
| --surface | card / panel background |
| --ink | primary text |
| --muted | secondary text, inactive data |
| --muted-soft | hairlines, inactive fills, dividers |
| --accent | the one emphasis: active series, highlight, badge, keyword |
| --accent-soft | accent tint for soft bands / chips |
| --band-fill | text-color fill for insight bands & section covers (adds no new color) |
| --pos / --neg / --warn | semantic; only inside KPI/delta or tone slides |

Spacing tokens (`--s0…--s9`) and type are defined in `foundations/`. Same name-only contract applies.
