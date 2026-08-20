"""Score the layout gate against human taste, using the A/B rounds as labelled data.

Every other check in this repo measures the gate against itself: it passes when its own thresholds are
satisfied. That says nothing about whether a passing slide is any good, and three times now a change
has passed every gate while looking visibly worse.

`preferences.md` records the winner of each A/B round ("Round 5 - B > A") and both variants are on
disk, which makes 37 pairs of **human-labelled** slides. So run the gate on A and on B, see which it
prefers, and compare with the person who actually chose. This is the only number in the system that
measures whether the gate has taste rather than whether it is internally consistent.

First run, recorded so movement is visible:

    37 pairs - the gate had NO OPINION on 20 of them (identical scores)
    of the 17 it did rank, it agreed with the user on 7 and disagreed on 10 -> 41%

Read the 20 ties as the headline. The gate is mostly *blind* to what separates a preferred slide from
a rejected one, rather than wrong about it. 17 decided pairs is far too small a sample to claim 41% is
meaningfully worse than a coin flip; what it does establish is that the gate carries no useful taste
signal today. Raising this number is the goal, and any change to the gate should be scored here before
it is believed.

Usage:
    python scripts/calibrate_gate.py

Exit code is always 0: this reports a measurement, it does not gate a build.
"""
import pathlib
import re
import sys

sys.path.insert(0, "scripts")
import validate_layout as V  # noqa: E402
from visual_baseline import find_browsers, render_with_any  # noqa: E402

AB = pathlib.Path("examples/case-study/_ab")
txt = pathlib.Path("specs/preferences.md").read_text(encoding="utf-8")
rounds = {int(m.group(1)): m.group(2)
          for m in re.finditer(r"Round\s+(\d+)\s*[—-]\s*([AB])\s*>\s*([AB])", txt)}

browsers = find_browsers(None)


def score(path: pathlib.Path) -> int:
    """Number of gate complaints; lower is 'better' in the gate's opinion."""
    html = path.read_text(encoding="utf-8", errors="replace")
    png = render_with_any(path, browsers, 1920, 1080, 0.25)
    w, h, ch, px = V.decode_png(png)
    metrics = V.analyse(w, h, ch, px)
    problems = V.evaluate(
        path, metrics, V.slide_kind(html),
        V.find_hardcoded_hex(html, False), V.visible_text(html), V.declared_langs(html, None),
    )
    return len(problems)


agree = disagree = tie = 0
rows = []
for n, winner in sorted(rounds.items()):
    a, b = AB / f"r{n}A.html", AB / f"r{n}B.html"
    if not (a.is_file() and b.is_file()):
        continue
    sa, sb = score(a), score(b)
    if sa == sb:
        verdict, tie = "tie  ", tie + 1
    else:
        gate_pick = "A" if sa < sb else "B"
        if gate_pick == winner:
            verdict, agree = "agree", agree + 1
        else:
            verdict, disagree = "DISAGREE", disagree + 1
    rows.append((n, winner, sa, sb, verdict))

for n, winner, sa, sb, verdict in rows:
    print(f"  R{n:<3} human={winner}  gate: A={sa} B={sb}   {verdict}")

decided = agree + disagree
print(f"\npairs scored: {len(rows)}")
print(f"gate expressed a preference on {decided}; agreed with the user on {agree}, disagreed on {disagree}")
if decided:
    print(f"agreement where it had an opinion: {agree/decided:.0%}  (50% = no signal)")
print(f"no opinion (equal score): {tie}")
