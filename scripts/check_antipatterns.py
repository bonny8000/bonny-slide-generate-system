#!/usr/bin/env python3
"""Every slide in specs/gate-antipatterns/ must FAIL the layout gate.

These are slides that look wrong. Some of them once passed: `A1` is the layout that went from FAIL to
pass at 34% whitespace with its label, title and body flung to the card's extremes, which read as
broken rather than designed. A pass bought that way is worth less than the failure it replaced.

A gate can only be made so clever, but it can be made to remember every case where it was fooled.
This turns those one-off observations into a permanent regression suite for the checker itself, so a
future "improvement" to a threshold cannot quietly reintroduce a defect the system already learned to
see. If a change to `validate_layout.py` makes any of these pass, that change is wrong regardless of
what it does to the failure count elsewhere.

Adding one: save the rendered-and-rejected slide here with a name that says what is wrong with it, and
note it in `specs/gate-antipatterns/README.md`.

Usage:
    python scripts/check_antipatterns.py

Exit codes: 0 = every antipattern still fails (good) · 1 = one of them now passes · 2 = cannot run.

The three outcomes have to stay distinct. This gate used to decide by looking for the string "FAIL"
anywhere in the checker's output, which quietly conflated them: when `validate_layout.py` could not
run at all — no Chromium on the machine, a render timeout — its message carries no "FAIL", so the
fixture was reported LEAKED and the operator was told to "fix the gate" over a defect that had never
been measured. The reverse was worse: a per-slide render crash prints "FAIL <slide> — <reason>", which
counted as *still caught* and turned an unrunnable gate green.

A verdict now comes from the exit code, and an unrunnable checker is its own outcome, never a result.
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CASES = ROOT / "specs" / "gate-antipatterns"

# A real layout verdict prints "FAIL <slide>  [<kind>]". A slide that never rendered prints
# "FAIL <slide> — <reason>" — same word, no measurement behind it.
RENDER_FAILURE = re.compile(r"^FAIL .+ — ", re.MULTILINE)


def verdict(slide: Path) -> tuple[str, str]:
    """One of 'caught' (still fails, good) · 'leaked' (now passes) · 'cannot-run'."""
    run = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "validate_layout.py"), str(slide), "--quiet"],
        capture_output=True, text=True, encoding="utf-8", errors="replace",
    )
    output = (run.stdout + run.stderr).strip()
    if run.returncode == 2 or RENDER_FAILURE.search(output):
        return "cannot-run", output
    return ("caught" if run.returncode == 1 else "leaked"), output


def reason(output: str) -> str:
    """The line that explains why nothing could be measured, not the run's summary."""
    hit = RENDER_FAILURE.search(output)
    if hit:
        return output[hit.start():].splitlines()[0].split(" — ", 1)[-1]
    for line in output.splitlines():
        if line.startswith("layout validate:"):
            return line.split("layout validate:", 1)[1].strip()
    return output.splitlines()[-1] if output else "no output"


def main() -> int:
    slides = sorted(CASES.glob("*.html"))
    if not slides:
        print(f"no antipattern fixtures in {CASES}", file=sys.stderr)
        return 2

    leaked, unrunnable = [], []
    for slide in slides:
        result, output = verdict(slide)
        label = {"caught": "still caught", "leaked": "LEAKED     ", "cannot-run": "cannot run  "}[result]
        print(f"{label}  {slide.name}")
        if result == "leaked":
            leaked.append(slide.name)
        elif result == "cannot-run":
            unrunnable.append(f"{slide.name}: {reason(output)}")

    # Never report a leak off the back of a checker that never measured anything.
    if unrunnable:
        print(
            f"\ncannot run the layout gate on {len(unrunnable)} fixture(s):\n  "
            + "\n  ".join(unrunnable)
            + "\nThis says nothing about whether the antipatterns still fail. Fix the renderer first.",
            file=sys.stderr,
        )
        return 2

    if leaked:
        print(
            f"\n{len(leaked)} antipattern(s) now PASS the gate: " + ", ".join(leaked)
            + "\nThe gate has lost the ability to see a defect it once caught. Fix the gate, not this file.",
            file=sys.stderr,
        )
        return 1
    print(f"\nall {len(slides)} antipatterns still fail the gate, as they must")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
