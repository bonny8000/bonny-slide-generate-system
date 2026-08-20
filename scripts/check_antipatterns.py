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
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CASES = ROOT / "specs" / "gate-antipatterns"


def main() -> int:
    slides = sorted(CASES.glob("*.html"))
    if not slides:
        print(f"no antipattern fixtures in {CASES}", file=sys.stderr)
        return 2

    leaked = []
    for slide in slides:
        run = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "validate_layout.py"), str(slide), "--quiet"],
            capture_output=True, text=True, encoding="utf-8", errors="replace",
        )
        output = run.stdout + run.stderr
        failed = "FAIL" in output
        print(f"{'still caught' if failed else 'LEAKED     '}  {slide.name}")
        if not failed:
            leaked.append(slide.name)

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
