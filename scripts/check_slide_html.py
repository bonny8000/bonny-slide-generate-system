#!/usr/bin/env python3
"""Lightweight checks for Bonny HTML slide files."""

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
        or "lang=\"en\"" in text
    )

    checks = {
        "has 1920 width token or slide class": "1920" in text or 'class="slide"' in text,
        "declares zh-Hant or CJK language": "zh-Hant" in text or "zh-TW" in text,
        "uses CJK class or lang wrapper": "class=\"cjk\"" in text or "lang=\"zh" in text,
        "uses Latin wrapper when English appears": not re.search(r"[A-Za-z]{4,}", text) or has_latin_wrapper,
        "links token stylesheet": "bonny-slide-tokens.css" in text,
    }

    failed = [name for name, ok in checks.items() if not ok]
    for name, ok in checks.items():
        print(f"[{'OK' if ok else 'FAIL'}] {name}")

    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
