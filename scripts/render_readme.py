#!/usr/bin/env python3
"""Refresh README screenshots from current examples, without modifying their HTML.

Uses the same isolated Chromium renderer as validate_layout.py. Requires an installed
Chromium browser. Run compile/sync checks first and visually inspect the results.
This documentation helper is separate from the compiler and the core CI suite.
"""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys

from validate_layout import LayoutError, find_browsers, render_with_any

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "assets/readme"
FIGURES = {
    "metrics-light.png": "examples/light-metric-cards.html",
    "persona-light.png": "examples/case-study/04.html",
    "kpi-dark.png": "examples/dark-07-kpi-results.html",
    "screen-interiors-light.png": "examples/light-screen-interiors.html",
}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--browser", help="explicit Chrome/Chromium/Edge executable")
    args = parser.parse_args()
    try:
        browsers = find_browsers(args.browser)
        # Render everything before replacing any checked-in image.
        rendered = {}
        sources = {}
        for name, source in FIGURES.items():
            path = ROOT / source
            sources[name] = hashlib.sha256(path.read_bytes()).hexdigest()
            rendered[name] = render_with_any(path, browsers, 1920, 1080, 1)
            print(f"Rendered {source} -> {name}", flush=True)
        manifest = {
            "renderer": "scripts/validate_layout.py via scripts/render_readme.py",
            "viewport": {"width": 1920, "height": 1080, "scale": 1},
            "note": "Screenshots depend on the installed browser and fonts; inspect after refreshing.",
            "figures": {
                name: {
                    "source": source,
                    "sourceSha256": sources[name],
                    "imageSha256": hashlib.sha256(rendered[name]).hexdigest(),
                }
                for name, source in FIGURES.items()
            },
        }
        OUTPUT.mkdir(parents=True, exist_ok=True)
        for name, data in rendered.items():
            (OUTPUT / name).write_bytes(data)
        (OUTPUT / "manifest.json").write_text(
            json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
        )
        print("README screenshots refreshed. Visual review is still required.")
        return 0
    except (OSError, LayoutError, subprocess.TimeoutExpired) as exc:
        print(f"README render failed: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
