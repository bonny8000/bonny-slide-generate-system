#!/usr/bin/env python3
"""Split an all-in-one deck (a scroll viewer) into ordered single-slide files.

`export_pdf.py` prints one `.slide` per page and rejects anything else, so a deck authored as a
single scrolling HTML file — every slide wrapped in viewer chrome — has no path to PDF. This
rebuilds each slide as a standalone document that the exporter and the layout gate both accept:
shared `<style>` and webfont links are copied to every page, and the slide markup is carried over
byte-for-byte. The source file is never modified.

    python scripts/split_deck.py deck.html --out work/slides
    python scripts/export_pdf.py work/slides --out work/deck.pdf

KNOWN LIMIT — viewer chrome is recognised by its comment marker, not by parsing the CSS.
A viewer restyles the page around its slides (`body{display:block}`, a tinted `html` background,
`.frame`/`.stage` scaling). Carried into a single-slide file those rules fight the deck's own
page rules and the slide renders off-canvas, so the trailing chrome block is dropped. It is found
by the `viewer chrome` comment the compiler emits. A hand-written viewer without that marker keeps
its chrome: the split still succeeds, and the warning says which files to check before exporting.
"""
from __future__ import annotations

import argparse
from pathlib import Path
import re
import sys

from slide_html import slides as html_slides

CHROME_MARKER = re.compile(r"/\*[^\n]*viewer chrome", re.I)
MAIN_RE = re.compile(r'<main\b[^>]*\bclass="[^"]*\bslide\b[^"]*"[^>]*>.*?</main\s*>', re.I | re.S)
STYLE_RE = re.compile(r"<style\b[^>]*>(.*?)</style\s*>", re.I | re.S)
TITLE_RE = re.compile(r"<title\b[^>]*>(.*?)</title\s*>", re.I | re.S)
FONT_LINK_RE = re.compile(r'<link\b[^>]*href="[^"]*fonts\.[^"]*"[^>]*>', re.I)
LABEL_RE = re.compile(r'<p class="pg-label">\s*<span class="n">([^<]*)</span>([^<]*)</p>', re.I)


def deck_css(text: str) -> tuple[str, bool]:
    """Every authored <style>, with a trailing viewer-chrome block removed."""
    blocks, dropped = [], False
    for block in STYLE_RE.findall(text):
        found = CHROME_MARKER.search(block)
        if found:
            block, dropped = block[: found.start()], True
        if block.strip():
            blocks.append(block.rstrip())
    if not blocks:
        raise ValueError("no <style> block found; a split slide would render unstyled")
    return "\n".join(blocks), dropped


def pages(text: str, lang: str) -> list[str]:
    parsed = len(html_slides(text))
    found = MAIN_RE.findall(text)
    if not found:
        raise ValueError("no <main class=\"slide ...\"> element found")
    if len(found) != parsed:
        # The structural reader sees every .slide; the extractor only sees <main> ones.
        raise ValueError(f"{parsed} .slide element(s) present but {len(found)} extractable — "
                         "each slide must be a <main> element")
    css, dropped = deck_css(text)
    if not dropped:
        print("warning: no viewer-chrome marker found — page-level rules were kept as authored",
              file=sys.stderr)
    title = TITLE_RE.search(text)
    title = title.group(1).strip() if title else "Slide"
    links = "\n".join(FONT_LINK_RE.findall(text))
    labels = [f"{number.strip()} {name.strip()}" for number, name in LABEL_RE.findall(text)]
    built = []
    for index, slide in enumerate(found, 1):
        label = labels[index - 1] if index <= len(labels) else f"{index:02}"
        built.append(f"<!doctype html><html lang='{lang}'><head><meta charset='utf-8'>"
                     f"<title>{title} — {label}</title>\n{links}\n"
                     f"<style data-shipped>\n{css}\n</style></head><body>"
                     f"{slide}</body></html>\n")
    return built


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("source", type=Path)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--lang", default="en", help="lang attribute for the built pages")
    args = parser.parse_args()
    try:
        built = pages(args.source.read_text(encoding="utf-8"), args.lang)
        args.out.mkdir(parents=True, exist_ok=True)
        for index, page in enumerate(built, 1):
            (args.out / f"{index:02}.html").write_text(page, encoding="utf-8")
        print(f"{len(built)} slide(s) written to {args.out}")
        return 0
    except (OSError, ValueError) as exc:
        print(f"split deck: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
