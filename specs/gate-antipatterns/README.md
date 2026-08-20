# Gate antipatterns — slides that must keep failing

Every file here looks wrong and **must FAIL `validate_layout.py`**. `scripts/check_antipatterns.py`
asserts that, and it is a blocker in `audit.md`.

A gate can only be made so clever. It can be made to *remember*: three separate changes have now
passed every automated check while looking visibly worse, and without a fixture each of those lessons
lives only in a changelog entry nobody re-reads. Freezing the rejected slide turns a one-off
observation into a permanent regression test for the checker itself.

| file | what is wrong with it |
|---|---|
| `A1-content-flung-to-card-edges.html` | Cards stretched to fill a grown row with `justify-content:space-between`, so label, title and body sit at the card's extremes with a hole between them. This is the one that went FAIL → pass at 34% whitespace. It reads as broken, not designed. |
| `A2-hollow-oversized-card.html` | A card given a `min-height` far beyond its contents — the hollow-container failure `preferences.md` principle 2 warns about. A box drawn bigger than its contents reads as a void, not breathing room. |

## Adding one

When a change passes the gate and the render looks worse, save that render's HTML here before fixing
it, name the file after the defect, and add a row above. If a later change to `validate_layout.py`
lets one of these through, **the change is wrong** regardless of what it does to the failure count
elsewhere — it has removed a defect the system had already learned to see.

These are fixtures, not examples. They are excluded from `sync_examples.py` and the visual baseline,
and nothing in `examples/` should imitate them.
