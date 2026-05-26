#!/usr/bin/env python3
"""Lightweight checks for Bonny Slide System V2 HTML slide files."""

from __future__ import annotations

import re
import sys
from pathlib import Path


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: check_slide_html.py <html-file>", file=sys.stderr)
        return 2

    path = Path(sys.argv[1])
    if not path.exists():
        print(f"Missing file: {path}", file=sys.stderr)
        return 2

    text = path.read_text(encoding="utf-8")
    has_latin_wrapper = (
        re.search(r'class="[^"]*\blatin\b[^"]*"', text) is not None
        or 'lang="en"' in text
    )
    has_cjk_wrapper = (
        re.search(r'class="[^"]*\bcjk\b[^"]*"', text) is not None
        or 'lang="zh' in text
    )
    has_slide_mode = 'data-mode="light"' in text or 'data-mode="dark"' in text

    checks = {
        "has slide container": 'class="slide"' in text or "class='slide'" in text,
        "declares a slide mode": has_slide_mode,
        "declares zh-TW or CJK language": "zh-TW" in text or "zh-Hant" in text,
        "uses CJK class or lang wrapper": has_cjk_wrapper,
        "uses Latin wrapper when English appears": not re.search(r"[A-Za-z]{4,}", text) or has_latin_wrapper,
        "links v2 token stylesheet": "bonny-slide-v2-tokens.css" in text,
        "has one headline class": text.count("headline") >= 1,
        "has source/method cue or intentionally none": "Source:" in text or "source" in text.lower() or "method" in text.lower(),
    }

    failed = [name for name, ok in checks.items() if not ok]
    for name, ok in checks.items():
        print(f"[{'OK' if ok else 'FAIL'}] {name}")

    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
