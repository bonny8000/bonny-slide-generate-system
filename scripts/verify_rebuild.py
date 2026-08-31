#!/usr/bin/env python3
"""Measure how much of each pattern comes from assets/base.css rather than from the example.

`specs/generated-class-coverage.md` answers a *name* question: is every class an example uses
defined somewhere in the stylesheet. That is necessary but not sufficient — a pattern can have every
class name present and still not reproduce, because a descendant rule, a pseudo-element, or an
`nth-child` rule never made it across. Reading the coverage number as "buildable" overstates it.

So this renders each example twice: once as it ships, and once with its `<style data-slide>` block
removed so only the shipped stylesheet applies. The gap between them is **local reliance** — how
much of what you see is the slide's own CSS doing the work.

Read the number as a measure, not a verdict. Every example carries a small deliberate slide block
(per-slide sizing, a one-off mockup), so some reliance is correct and expected. What matters is the
magnitude: a pattern with high reliance is mostly bespoke, which means an agent imitating it learns
local CSS instead of the shared vocabulary — the exact failure this system exists to prevent.

An earlier version of this script called any gap a rebuild FAILURE. That was written when examples
inlined the whole stylesheet and had no slide block, and it misreads the current architecture: it
reports a designed feature as a defect. Do not restore that reading.

Usage:
    python scripts/verify_rebuild.py                 # every example
    python scripts/verify_rebuild.py light-timeline  # one pattern, by example stem

Exit codes: 0 = no pattern exceeds the reliance ceiling · 1 = some do · 2 = cannot run.
"""

from __future__ import annotations

import argparse
import re
import sys
import tempfile
from html import escape
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from validate_layout import find_browsers, render_with_any  # noqa: E402
from visual_baseline import compare, fingerprint
from sync_examples import shipped_css, dark_theme
from example_files import collect  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
MEAN_MAX = 2.0
PEAK_MAX = 12.0


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

    examples = collect([ROOT / "examples"])
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
            if '<style data-shipped>' not in src:
                print(f'verify rebuild: {example} is not synced; run sync_examples.py',file=sys.stderr)
                return 2
            # Change only the sheet under test. Reconstructing a new document discarded
            # metadata/head/body attributes and could report that loss as local CSS reliance.
            content=re.sub(r'<style data-shipped>.*?</style>',
                           lambda m:'<style data-shipped>'+shipped_css(dark_theme(src))+'</style>',src,count=1,flags=re.S)
            content=re.sub(r'<style data-slide>.*?</style>','',content,flags=re.S)
            if not re.search(r'<base\b',content,re.I):
                content=re.sub(r'(<head\b[^>]*>)',lambda m:m[0]+'<base href="'+escape(example.parent.as_uri()+'/')+'">',content,count=1,flags=re.I)
            rebuilt = Path(tmp) / (example.stem + ".html")
            rebuilt.write_text(
                content,
                encoding="utf-8",
                newline="\n",
            )
            shipped = fingerprint(render_with_any(example, browsers, 1920, 1080, 0.25))
            fresh = fingerprint(render_with_any(rebuilt, browsers, 1920, 1080, 0.25))
            mean, peak = compare(shipped, fresh)
            ok = mean <= args.mean and peak <= args.peak
            failures += not ok
            label = "shared" if ok else "LOCAL "
            print(f"{label}  reliance {mean:5.2f}  peak {peak:5.0f}  {example.stem}")

    total = len(examples)
    if failures:
        print(
            f"\n{total - failures}/{total} patterns draw their look from assets/base.css. "
            f"{failures} lean on example-local CSS beyond the ceiling — check whether that "
            f"pattern's vocabulary belongs in base.css instead.",
            file=sys.stderr,
        )
        return 1
    print(f"\nall {total} patterns draw their look from assets/base.css")
    return 0


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except AttributeError:
        pass
    raise SystemExit(main())
