#!/usr/bin/env python3
"""Flag slide CSS that contradicts the taste recorded in preferences.md.

Why this is static and not another pixel metric: it was tested. Nine geometric measures were scored
against the 37 human-labelled A/B pairs — coverage, interior gap, text gap, band ratio, margin ratio,
quadrant spread, ink ratio, and fill-vs-ink share — and **none of them separated a preferred slide
from a rejected one**. The best was 60% on n=20, which is noise. The differences a person actually
decides on are not geometric, so measuring more geometry harder was never going to help.

The same test over markup and CSS found signal. The strongest, `accent_ink` — how often the accent
carries *type* rather than a filled surface — agreed with the user on 14 of 19 rounds where the two
variants differed (74%). That is the empirical form of preferences.md principle 7,
**emphasis-by-ink > emphasis-by-fill**, and it is legible in the stylesheet where no renderer is
needed to see it.

Round 34 is the worked example: the rejected variant striped its table with
`tr:nth-child(odd){background:var(--surface)}`, the chosen one separated rows with `border-bottom`.
Identical geometry, identical gate score, opposite verdicts.

**This advises, it does not gate.** Every rule here is a preference with a real exception, sample
sizes are small, and a rule that blocks on 74% confidence would be wrong once in four. Exit status is
always 0; read the output as a second opinion and overrule it when the slide's intent calls for it.

Usage:
    python scripts/check_style_rules.py examples/light-metric-cards.html
    python scripts/check_style_rules.py examples/*.html --quiet
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ACCENT_FILL = re.compile(r"background:\s*var\(--accent\)")
ACCENT_SOFT = re.compile(r"background:\s*var\(--accent-soft\)")
ACCENT_INK = re.compile(r"color:\s*var\(--accent\)")
ZEBRA = re.compile(r"nth-child\([^)]*\)\s*\{[^}]*background", re.S)


def slide_parts(html: str) -> tuple[str, str]:
    match = re.search(r"<style data-slide>(.*?)</style>", html, re.S)
    css = match.group(1) if match else ""
    return css, html.rsplit("</style>", 1)[-1]


def review(path: Path) -> list[str]:
    html = path.read_text(encoding="utf-8", errors="replace")
    css, markup = slide_parts(html)
    both = css + markup
    notes: list[str] = []

    if ZEBRA.search(css):
        notes.append(
            "zebra row fill — `nth-child(...){background:...}` paints alternate rows. Round 34 chose "
            "the variant that separated rows with a border instead. Tint a row only to encode "
            "ranking, not to stripe. (principle 7)"
        )

    fills = len(ACCENT_FILL.findall(both)) + len(ACCENT_SOFT.findall(both))
    inks = len(ACCENT_INK.findall(both)) + both.count('class="accent"')
    if fills > max(inks, 1) * 2 and fills >= 3:
        notes.append(
            f"accent carried by fill, not ink — {fills} filled surfaces against {inks} accented "
            "words. The preferred variant used accent on type in 14 of 19 rounds where the two "
            "differed. Paint a surface only when it also supplies mass a sparse slide needs. "
            "(principle 7)"
        )

    regions = len(ACCENT_FILL.findall(both))
    if regions > 4:
        notes.append(
            f"accent spread across {regions} filled regions — one chromatic accent is meant to be a "
            "scarce, precise highlight, and a single-hue ramp is the only sanctioned widening. "
            "(principle 6)"
        )
    return notes


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("slides", nargs="+", type=Path)
    ap.add_argument("--quiet", action="store_true", help="only list slides that have notes")
    args = ap.parse_args()

    flagged = 0
    for slide in args.slides:
        if not slide.is_file():
            continue
        notes = review(slide)
        if notes:
            flagged += 1
            print(f"note {slide}")
            for note in notes:
                print(f"       - {note}")
        elif not args.quiet:
            print(f"ok   {slide}")

    print(f"\n{flagged} slide(s) carry a style note. Advisory only — the intent can overrule any of them.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
