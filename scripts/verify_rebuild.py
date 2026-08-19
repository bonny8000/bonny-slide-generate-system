#!/usr/bin/env python3
"""Check whether each pattern can really be rebuilt from assets/base.css.

`specs/generated-class-coverage.md` answers a *name* question: is every class an example uses
defined somewhere in the stylesheet. That is necessary but not sufficient — a pattern can have every
class name present and still not reproduce, because a descendant rule, a pseudo-element, or an
`nth-child` rule never made it across. Reading the coverage number as "buildable" overstates it.

This is the honest check: re-render each example with **only** the shipped stylesheet — the theme
tokens, the generated bundle, and base.css — and compare against the example as it actually ships.
If the two match, the stylesheet genuinely contains the pattern.

Usage:
    python scripts/verify_rebuild.py                 # every example
    python scripts/verify_rebuild.py light-timeline  # one pattern, by example stem

Exit codes: 0 = every checked pattern rebuilds within tolerance · 1 = some do not · 2 = cannot run.
"""

from __future__ import annotations

import argparse
import re
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from validate_layout import find_browsers, render_with_any  # noqa: E402
from visual_baseline import compare, fingerprint  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
MEAN_MAX = 2.0
PEAK_MAX = 12.0


def shipped_css(dark: bool) -> str:
    theme = "tokens-dark.css" if dark else "tokens-light.css"
    parts = [
        (ROOT / "assets" / theme).read_text(encoding="utf-8"),
        (ROOT / "assets" / "generated" / "base-bundle.css").read_text(encoding="utf-8"),
        # the bundle is already inlined above, so drop base.css's @import of it
        re.sub(r"@import[^;]+;", "", (ROOT / "assets" / "base.css").read_text(encoding="utf-8")),
    ]
    return "".join(parts)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("names", nargs="*", help="example stems to check (default: all)")
    parser.add_argument("--browser")
    parser.add_argument("--mean", type=float, default=MEAN_MAX)
    parser.add_argument("--peak", type=float, default=PEAK_MAX)
    args = parser.parse_args()

    try:
        browsers = find_browsers(args.browser)
    except Exception as exc:  # noqa: BLE001
        print(f"verify rebuild: {exc}", file=sys.stderr)
        return 2

    examples = sorted((ROOT / "examples").rglob("*.html"))
    if args.names:
        wanted = set(args.names)
        examples = [e for e in examples if e.stem in wanted]
    if not examples:
        print("verify rebuild: no examples matched", file=sys.stderr)
        return 2

    failures = 0
    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmp:
        for example in examples:
            src = example.read_text(encoding="utf-8", errors="replace")
            if "</style>" not in src:
                continue
            dark = "--canvas:#1B1B20" in src or "--canvas: #1B1B20" in src
            markup = src.split("</style>")[-1]
            rebuilt = Path(tmp) / (example.stem + ".html")
            rebuilt.write_text(
                "<!doctype html><html lang='zh-Hant'><head><meta charset='utf-8'><style>"
                + shipped_css(dark)
                + "</style></head>"
                + markup,
                encoding="utf-8",
                newline="\n",
            )
            shipped = fingerprint(render_with_any(example, browsers, 1920, 1080, 0.25))
            fresh = fingerprint(render_with_any(rebuilt, browsers, 1920, 1080, 0.25))
            mean, peak = compare(shipped, fresh)
            ok = mean <= args.mean and peak <= args.peak
            failures += not ok
            print(f"{'ok  ' if ok else 'DIFF'}  mean {mean:5.2f}  peak {peak:5.0f}  {example.stem}")

    total = len(examples)
    if failures:
        print(
            f"\n{total - failures}/{total} patterns rebuild from assets/base.css alone. "
            f"{failures} still depend on CSS that lives only in their example.",
            file=sys.stderr,
        )
        return 1
    print(f"\nall {total} patterns rebuild from assets/base.css alone")
    return 0


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except AttributeError:
        pass
    raise SystemExit(main())
