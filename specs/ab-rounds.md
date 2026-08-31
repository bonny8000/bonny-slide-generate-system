# A/B rounds — the labelled data

Every claim this system makes about taste rests on these. Nine geometric metrics were scored against
rounds 1–50 and none predicted a winner; one static CSS feature reached 74% on n=19. Both conclusions
sit on the 37 usable pairs those rounds yielded, which is too few to be sure of either — so more
rounds is the highest-value thing that can be added here. Calibration now runs over 42 pairs, after
R51–R55; the two conclusions above have not been recomputed against them.

Declare a round below, build it with `python scripts/ab_round.py 51`, judge the one image it renders,
then record the human verdict in `winner:` (A or B) and run
`python scripts/calibrate_gate.py --manifest work/ab-review/manifest.json`.
Pending or tied rounds remain unlabelled; the agent must never choose on the user's behalf.

The builder writes a new review folder with variant hashes, never into frozen `_ab` history.
Once rendered, a pair is immutable in that output folder; use a fresh round for a changed experiment.
Keep the manifest and variants beside the judgement. A hash mismatch stops calibration.

**A round is only worth running if both variants are defensible.** A pair where one option is
obviously broken teaches nothing except that broken is worse. The useful rounds are the ones where a
reasonable designer could pick either, because that is exactly where the system has no opinion today.

Rounds 1–50 live in `preferences.md` with their verdicts and the principles drawn from them.

---

### R51 — header pinned to the top vs composed as a centred group
base: light-keyword-cards
question: Same content both ways. Does the header belong at the top of the canvas, or down against its cards?
winner: B

Human selected B on 2026-08-31: keep the header and cards composed as a centred group.

```css
.kw{align-items:center}
main.slide{justify-content:flex-start}
.kw{flex:1;min-height:0}
```

```css
.kw{align-items:center}
main.slide{justify-content:center}
```

### R52 — accent as filled surface vs accent as type
base: light-results-grid
question: Which carries the emphasis better — painting the key figure's surface, or accenting the numeral itself?
winner: A

Human selected A on 2026-08-31 with an additional correction: numeric values in different rows/fields
must align with each other, not with the edge of the coloured surface. The archived pair records the
original judgement; the subsequent shared-inset fix is an explicit implementation refinement.

Fresh test of the strongest static signal found so far (`accent_ink`, 74% on n=19). Rounds 1–50 are
what produced that number, so they cannot also confirm it.

```css
.row:first-child{background:var(--accent-soft);border-radius:var(--r-card);padding:var(--s4) var(--s5)}
.row:first-child .v{color:var(--ink)}
```

```css
.row:first-child .v{color:var(--accent)}
.row:first-child .l{color:var(--ink);font-weight:700}
```

### R53 — card sized to its content vs card given room to breathe
base: light-metric-cards
question: Do the metric cards read better tight to their content, or with generous height around it?
winner: A

Principle 2 says a box drawn bigger than its contents reads as a void. This asks where the line sits,
since some breathing room is clearly right.

```css
.mc{min-height:430px;justify-content:center}
```

```css
.mc{min-height:0;padding:var(--s5) var(--s6)}
```

### R54 — table rows separated by fill vs by rule
base: light-09-comparison
question: The comparison table: zebra-striped rows, or plain rows divided by a hairline?
winner: B

Round 34 answered fill-versus-rule once, on a different table. This re-tests it to see whether the
answer was about the principle or about that one slide.

First attempt at this round was withdrawn: the two variants were "not really different" because the
CSS landed on the supporting list, and the table itself had been shrunk to content width by a
neutralisation revert that stripped `width:100%`. Both were fixed before re-posing the question — a
round run on a broken base measures the breakage, not the axis.

```css
.ctable tbody tr:nth-child(odd){background:var(--surface)}
.ctable th,.ctable td{border-bottom:0}
```

```css
.ctable tbody tr{background:transparent}
```

### R55 — one accent vs accent on every value point
base: light-value-points
question: Should the accent mark a single load-bearing idea, or every parallel point equally?
winner: A

Principle 6 says the accent is scarce. Parallel peers are the case that most tempts you to break it.

```css
.pt .lbl{color:var(--accent)}
.pt .dot{background:var(--accent)}
.skill-chip{border-color:var(--accent);color:var(--accent)}
```

```css
.pt:first-child .lbl{color:var(--accent)}
.pt:first-child .dot{background:var(--accent)}
.pt:not(:first-child) .lbl{color:var(--muted)}
.pt:not(:first-child) .dot{background:var(--muted-soft)}
```

## Recorded evidence — 2026-08-31
User votes: **51B, 52A (numeric alignment correction), 53A, 54B, 55A**.
Frozen portable variants, the shown comparisons, and SHA256 hashes are in
`specs/ab-reviewed/2026-08-31/manifest.json`. Only the local `<base>` URL was rewritten on archival;
`sourceSha256` identifies the originally shown file and `sha256` guards the portable copy.
