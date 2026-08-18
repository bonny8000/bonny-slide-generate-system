#!/usr/bin/env python3
"""Render a built slide and measure whether it obeys the layout-balance rules.

`specs/foundations/layout-balance.md` describes whole-page balance, density (不空不擠),
uniform four-side margins, and full top-to-bottom fill. Those rules were prose only, so they
degraded first whenever context got tight. This turns them into a gate.

The slide is rendered headlessly and analysed as pixels — the same thing a human sees, and the
only way to catch a broken render (a silently unstyled page passes every structural check).

Usage:
    python scripts/validate_layout.py DECK.html [more.html ...]
    python scripts/validate_layout.py examples/*.html --json report.json

Exit codes: 0 = every slide passes · 1 = at least one slide fails · 2 = could not run.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import struct
import subprocess
import sys
import tempfile
import zlib
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]

# Thresholds mirror specs/foundations/layout-balance.md
# Coverage is a weak proxy for perceived density, so it only fails at genuine extremes; the
# structural checks below carry the real weight because they name a defect the builder can fix.
COVERAGE_MIN = 0.08         # under this the canvas is essentially empty
COVERAGE_MAX = 0.92         # over this the page is wall-to-wall with no breathing room
INTERIOR_GAP_MAX = 0.18     # longest dead band inside the content, as a share of the canvas
MARGIN_RATIO_MAX = 2.5      # uniform safe-area; measured on the ink box, so allow glyph slack
BAND_RATIO_MAX = 2.2        # empty top vs empty bottom band
DEAD_QUADRANT_SHARE = 0.06  # a quadrant holding <6% of the ink reads as a dead corner
INK_ROW_FLOOR = 0.004       # a row/col needs this fraction of ink to count as content
COLOR_DELTA = 5             # per-channel delta that counts as "not background"; theme
                            # surfaces sit only ~5-10 off canvas, so this must stay sensitive
STRONG_INK_DELTA = 40       # text / icons / charts, as opposed to a flat surface fill
GRID_COLS, GRID_ROWS = 48, 27   # occupancy grid over the 16:9 canvas
CELL_INK_MIN = 0.02         # a grid cell counts as occupied at this much ink

BROWSER_CANDIDATES = (
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
)


class LayoutError(RuntimeError):
    """Raised when the slide cannot be rendered or measured at all."""


# ---------------------------------------------------------------- PNG decoding


def _paeth(a: int, b: int, c: int) -> int:
    p = a + b - c
    pa, pb, pc = abs(p - a), abs(p - b), abs(p - c)
    if pa <= pb and pa <= pc:
        return a
    return b if pb <= pc else c


def decode_png(data: bytes) -> tuple[int, int, int, bytearray]:
    """Minimal stdlib PNG decoder (8-bit, non-interlaced). Returns (w, h, channels, pixels)."""
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        raise LayoutError("not a PNG file")
    pos = 8
    idat = bytearray()
    width = height = channels = 0
    palette = b""
    color_type = bit_depth = 0
    while pos < len(data):
        (length,) = struct.unpack(">I", data[pos : pos + 4])
        ctype = data[pos + 4 : pos + 8]
        body = data[pos + 8 : pos + 8 + length]
        pos += 12 + length
        if ctype == b"IHDR":
            width, height, bit_depth, color_type, _, _, interlace = struct.unpack(">IIBBBBB", body)
            if bit_depth != 8:
                raise LayoutError(f"unsupported PNG bit depth {bit_depth}")
            if interlace:
                raise LayoutError("interlaced PNG is not supported")
            channels = {0: 1, 2: 3, 3: 1, 4: 2, 6: 4}.get(color_type, 0)
            if not channels:
                raise LayoutError(f"unsupported PNG color type {color_type}")
        elif ctype == b"PLTE":
            palette = bytes(body)
        elif ctype == b"IDAT":
            idat += body
        elif ctype == b"IEND":
            break

    raw = zlib.decompress(bytes(idat))
    stride = width * channels
    out = bytearray(height * stride)
    prev = bytearray(stride)
    src = 0
    for y in range(height):
        filter_type = raw[src]
        src += 1
        line = bytearray(raw[src : src + stride])
        src += stride
        if filter_type == 1:
            for i in range(channels, stride):
                line[i] = (line[i] + line[i - channels]) & 0xFF
        elif filter_type == 2:
            for i in range(stride):
                line[i] = (line[i] + prev[i]) & 0xFF
        elif filter_type == 3:
            for i in range(stride):
                left = line[i - channels] if i >= channels else 0
                line[i] = (line[i] + ((left + prev[i]) >> 1)) & 0xFF
        elif filter_type == 4:
            for i in range(stride):
                left = line[i - channels] if i >= channels else 0
                upleft = prev[i - channels] if i >= channels else 0
                line[i] = (line[i] + _paeth(left, prev[i], upleft)) & 0xFF
        elif filter_type != 0:
            raise LayoutError(f"unknown PNG filter {filter_type}")
        out[y * stride : (y + 1) * stride] = line
        prev = line

    if color_type == 3:
        if not palette:
            raise LayoutError("indexed PNG without a palette")
        expanded = bytearray(width * height * 3)
        for i, idx in enumerate(out):
            expanded[i * 3 : i * 3 + 3] = palette[idx * 3 : idx * 3 + 3]
        return width, height, 3, expanded
    return width, height, channels, out


# ---------------------------------------------------------------- rendering


def find_browsers(explicit: str | None) -> list[str]:
    """Every Chromium we could use, best first.

    An installed browser is not necessarily a usable one — Edge is commonly blocked by enterprise
    policy and exits silently — so the caller tries each in turn until one really writes a PNG.
    """
    if explicit:
        if not Path(explicit).is_file():
            raise LayoutError(f"browser not found: {explicit}")
        return [explicit]
    found: list[str] = []
    for name in ("chrome", "chromium", "google-chrome", "msedge"):
        path = shutil.which(name)
        if path and path not in found:
            found.append(path)
    for candidate in BROWSER_CANDIDATES:
        if Path(candidate).is_file() and candidate not in found:
            found.append(candidate)
    if not found:
        raise LayoutError(
            "no Chromium browser found — pass --browser with the path to chrome.exe or msedge.exe"
        )
    return found


def render_with_any(html: Path, browsers: list[str], width: int, height: int, scale: float) -> bytes:
    problems: list[str] = []
    for browser in browsers:
        try:
            return render(html, browser, width, height, scale)
        except LayoutError as exc:
            problems.append(f"{Path(browser).name}: {exc}")
    raise LayoutError("no usable browser. " + " | ".join(problems))


def render(html: Path, browser: str, width: int, height: int, scale: float) -> bytes:
    # ignore_cleanup_errors: on Windows the browser still holds its profile lockfile at exit
    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmp:
        shot = Path(tmp) / "shot.png"
        cmd = [
            browser,
            "--headless=new",
            "--disable-gpu",
            "--hide-scrollbars",
            "--no-first-run",
            "--disable-extensions",
            f"--user-data-dir={tmp}/profile",
            f"--window-size={width},{height}",
            f"--force-device-scale-factor={scale}",
            "--virtual-time-budget=3000",
            f"--screenshot={shot}",
            html.resolve().as_uri(),
        ]
        proc = subprocess.run(cmd, capture_output=True, timeout=120)
        if not shot.is_file():
            detail = (proc.stderr or b"").decode("utf-8", "replace").strip()[-500:]
            raise LayoutError(f"headless render produced no screenshot. {detail}")
        return shot.read_bytes()


# ---------------------------------------------------------------- measurement


def analyse(width: int, height: int, channels: int, pixels: bytearray) -> dict[str, Any]:
    """Build an ink map (pixels that differ from the page background) and measure balance."""
    step = channels

    def at(x: int, y: int) -> tuple[int, int, int]:
        i = (y * width + x) * step
        return pixels[i], pixels[i + 1], pixels[i + 2]

    # The page background is the colour of the outer ring, NOT the most common colour: on a
    # card-heavy slide the card surface out-numbers the canvas, which would invert every measure.
    ring: Counter[tuple[int, int, int]] = Counter()
    for x in range(0, width, 2):
        ring[at(x, 1)] += 1
        ring[at(x, height - 2)] += 1
    for y in range(0, height, 2):
        ring[at(1, y)] += 1
        ring[at(width - 2, y)] += 1
    (bg_r, bg_g, bg_b), bg_hits = ring.most_common(1)[0]
    sampled = sum(ring.values())

    row_ink = [0] * height
    col_ink = [0] * width
    total_ink = 0
    strong_ink = 0
    # Density is about how much of the canvas the CONTENT occupies, not how many glyph pixels
    # are painted — black text on white is ~5% ink but can fill the page. So mark occupancy on a
    # coarse grid: a cell counts as occupied once it holds any meaningful content.
    cell_w = max(1, width // GRID_COLS)
    cell_h = max(1, height // GRID_ROWS)
    cells = [[0] * GRID_COLS for _ in range(GRID_ROWS)]

    for y in range(height):
        base = y * width * step
        row_total = 0
        cell_row = cells[min(y // cell_h, GRID_ROWS - 1)]
        for x in range(width):
            i = base + x * step
            delta = max(
                abs(pixels[i] - bg_r), abs(pixels[i + 1] - bg_g), abs(pixels[i + 2] - bg_b)
            )
            if delta > COLOR_DELTA:
                row_total += 1
                col_ink[x] += 1
                cell_row[min(x // cell_w, GRID_COLS - 1)] += 1
                if delta > STRONG_INK_DELTA:
                    strong_ink += 1
        row_ink[y] = row_total
        total_ink += row_total

    cell_area = cell_w * cell_h
    occupied = [
        [1 if cells[r][c] >= cell_area * CELL_INK_MIN else 0 for c in range(GRID_COLS)]
        for r in range(GRID_ROWS)
    ]
    occupied_count = sum(sum(row) for row in occupied)
    coverage = occupied_count / (GRID_COLS * GRID_ROWS)

    mid_c, mid_r = GRID_COLS // 2, GRID_ROWS // 2
    quadrants = [0, 0, 0, 0]
    for r in range(GRID_ROWS):
        for c in range(GRID_COLS):
            if occupied[r][c]:
                quadrants[(0 if r < mid_r else 2) + (0 if c < mid_c else 1)] += 1

    row_floor = width * INK_ROW_FLOOR
    col_floor = height * INK_ROW_FLOOR
    rows = [y for y, v in enumerate(row_ink) if v > row_floor]
    cols = [x for x, v in enumerate(col_ink) if v > col_floor]

    if not rows or not cols or not occupied_count:
        return {
            "blank": True,
            "background": [bg_r, bg_g, bg_b],
            "background_share": bg_hits / sampled,
            "ink_ratio": total_ink / (width * height),
            "coverage": coverage,
            "whitespace_ratio": 1 - coverage,
        }

    top, bottom = rows[0], height - 1 - rows[-1]
    left, right = cols[0], width - 1 - cols[-1]
    margins = {"top": top, "bottom": bottom, "left": left, "right": right}
    quadrant_share = [q / occupied_count for q in quadrants]

    # The most common real failure is a void INSIDE the content, not at its edges: a slide whose
    # top/bottom margins look even but whose lower half is dead. Margins cannot see that, so
    # measure the longest empty band between the first and last occupied cell-row.
    band_rows = [any(occupied[r]) for r in range(GRID_ROWS)]
    filled = [r for r, v in enumerate(band_rows) if v]
    longest_gap = run = 0
    for r in range(filled[0], filled[-1] + 1):
        run = 0 if band_rows[r] else run + 1
        longest_gap = max(longest_gap, run)
    interior_gap = longest_gap / GRID_ROWS

    band_cols = [any(occupied[r][c] for r in range(GRID_ROWS)) for c in range(GRID_COLS)]
    filled_c = [c for c, v in enumerate(band_cols) if v]
    longest_cgap = run = 0
    for c in range(filled_c[0], filled_c[-1] + 1):
        run = 0 if band_cols[c] else run + 1
        longest_cgap = max(longest_cgap, run)
    interior_gap_x = longest_cgap / GRID_COLS

    return {
        "blank": False,
        "background": [bg_r, bg_g, bg_b],
        "background_share": bg_hits / sampled,
        "ink_ratio": total_ink / (width * height),
        "coverage": coverage,
        "whitespace_ratio": 1 - coverage,
        "content_ink": strong_ink / max(1, occupied_count * cell_area),
        "margins": margins,
        "margin_ratio": max(margins.values()) / max(1, min(margins.values())),
        "band_ratio": max(top, bottom) / max(1, min(top, bottom)),
        "interior_gap": interior_gap,
        "interior_gap_x": interior_gap_x,
        "quadrant_share": quadrant_share,
        "content_box": {
            "x": left,
            "y": top,
            "w": width - left - right,
            "h": height - top - bottom,
        },
    }


# ---------------------------------------------------------------- static checks


TOKEN_BLOCK_RE = re.compile(
    r"(:root|\[data-theme[^\]]*\]|html\[[^\]]*\])[^{]*\{[^}]*\}", re.I | re.S
)
HEX_VALUE_RE = re.compile(r"[:,(]\s*(#[0-9a-fA-F]{3,8})\b")


INLINE_STYLE_RE = re.compile(r"""style\s*=\s*["']([^"']*)["']""", re.I)


def find_hardcoded_hex(html: str, strict: bool) -> list[str]:
    """Hex is legitimate in the token layer only; everything else must use token names.

    By default this inspects inline `style="…"` attributes — where per-slide authoring drift shows
    up. `--strict-hex` also scans <style> blocks, which catches drift in the shared base/theme CSS;
    that is a system-level fix (one edit in assets/base.css), not a per-slide one, so it is opt-in
    to keep the per-slide gate from firing the same finding on every page of a deck.
    """
    if strict:
        haystack = TOKEN_BLOCK_RE.sub(" ", html)
    else:
        haystack = " ".join(m.group(1) for m in INLINE_STYLE_RE.finditer(html))
    return sorted({m.group(1) for m in HEX_VALUE_RE.finditer(haystack)})


# layout-balance.md grants these a whitespace exception; everything else must fill the canvas
SPARSE_CLASSES = {"cover", "section-cover", "statement", "hero-quote", "divider"}
SLIDE_CLASS_RE = re.compile(r"""class\s*=\s*["']([^"']*\bslide\b[^"']*)["']""", re.I)


def slide_kind(html: str) -> str:
    """Classify the slide so the documented balance exceptions can apply.

    Only the rendered body is inspected — a <style> block naming `.slide.section-cover` says
    nothing about what this particular slide is.
    """
    body = html.split("<body", 1)[-1] if "<body" in html else html
    if "data-editorial-explainer" in body.lower():
        return "editorial-explainer"
    match = SLIDE_CLASS_RE.search(body)
    if match and SPARSE_CLASSES & set(match.group(1).lower().split()):
        return "sparse-exception"
    return "content"


# ---------------------------------------------------------------- gate


def evaluate(path: Path, metrics: dict[str, Any], kind: str, hexes: list[str]) -> list[str]:
    failures: list[str] = []

    if metrics["blank"]:
        failures.append(
            "page renders essentially blank — content did not paint. A linked <link href=\"../assets/…\"> "
            "stylesheet commonly fails silently under file://; inline the theme + base.css instead."
        )
        return failures

    # A cover / statement / divider is *meant* to be a few words on open canvas, so only hold a
    # content slide to this. layout-balance.md grants exactly that exception.
    if kind == "content" and metrics["background_share"] > 0.985 and metrics["ink_ratio"] < 0.02:
        failures.append(
            "page is a near-empty canvas — nothing meaningful was laid out. If this is a cover, "
            "statement, or section divider, give the slide element that class so the documented "
            "whitespace exception applies."
        )
        return failures

    whitespace = metrics["whitespace_ratio"]
    if kind == "content":
        if metrics["coverage"] < COVERAGE_MIN:
            failures.append(
                f"很空 — content covers only {metrics['coverage']:.0%} of the canvas. "
                "Grow the content, not the padding: enlarge the hero visual or add supporting mass."
            )
        elif metrics["coverage"] > COVERAGE_MAX:
            failures.append(
                f"太擠 — content covers {metrics['coverage']:.0%} of the canvas, leaving no margin. "
                "Remove, don't shrink: fewer items, wider gaps, or split the slide."
            )

    if kind == "content":
        # The signature failure: even margins, but a dead band through the middle or lower half.
        if metrics["interior_gap"] > INTERIOR_GAP_MAX:
            failures.append(
                f"content does not distribute — a dead horizontal band {metrics['interior_gap']:.0%} "
                f"of the canvas tall sits inside the content (max {INTERIOR_GAP_MAX:.0%}). "
                "Growing isn't enough: use .vspread so sub-blocks reach the body's top and bottom, "
                "or add vertical mass that earns its space."
            )
        if metrics["interior_gap_x"] > INTERIOR_GAP_MAX * 1.5:
            failures.append(
                f"content does not distribute horizontally — a dead column band "
                f"{metrics['interior_gap_x']:.0%} of the canvas wide sits inside the content. "
                "Balance the quadrants or widen the content to the grid."
            )

    # NOTE: no failure on four-side margin symmetry. `.slide` already enforces uniform padding in
    # CSS, so measuring it on the *ink* box only reports that content does not fill the safe area —
    # which is legitimate for sanctioned patterns like an editorial-left title slide. The ratio is
    # still reported in the metrics for eyeballing.
    if kind in ("content", "editorial-explainer"):
        if metrics["band_ratio"] > BAND_RATIO_MAX:
            m = metrics["margins"]
            heavier = "top" if m["top"] > m["bottom"] else "bottom"
            failures.append(
                f"empty {heavier} band — T{m['top']}px vs B{m['bottom']}px "
                f"({metrics['band_ratio']:.1f}× > {BAND_RATIO_MAX}×). "
                "Fill the canvas top→bottom: use .grow on the body and .vspread to distribute it."
            )

    if kind == "content":
        dead = [
            name
            for name, share in zip(("top-left", "top-right", "bottom-left", "bottom-right"),
                                   metrics["quadrant_share"])
            if share < DEAD_QUADRANT_SHARE
        ]
        if dead:
            shares = " / ".join(f"{s:.0%}" for s in metrics["quadrant_share"])
            failures.append(
                f"dead quadrant(s): {', '.join(dead)} (TL/TR/BL/BR = {shares}). "
                "Anchor, then counterbalance — add a caption row, bottom band, or equal card min-heights."
            )

    if hexes:
        shown = ", ".join(hexes[:6]) + (" …" if len(hexes) > 6 else "")
        failures.append(
            f"hardcoded colour outside the token layer: {shown}. "
            "Golden rule is token names only — never hardcode colour."
        )

    return failures


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("slides", nargs="+", type=Path, help="built slide HTML file(s)")
    parser.add_argument("--browser", help="path to msedge.exe / chrome.exe")
    parser.add_argument("--width", type=int, default=1920, help="deck width (default 1920)")
    parser.add_argument("--height", type=int, default=1080, help="deck height (default 1080)")
    parser.add_argument(
        "--scale",
        type=float,
        default=0.5,
        help="render scale; 0.5 keeps the 1920x1080 layout but analyses a 960x540 image (default 0.5)",
    )
    parser.add_argument("--json", type=Path, help="write a machine-readable report here")
    parser.add_argument("--quiet", action="store_true", help="only print failures")
    parser.add_argument(
        "--strict-hex",
        action="store_true",
        help="also scan <style> blocks for hardcoded colour, not just inline style attributes",
    )
    args = parser.parse_args()

    try:
        browsers = find_browsers(args.browser)
    except LayoutError as exc:
        print(f"layout validate: {exc}", file=sys.stderr)
        return 2

    targets: list[Path] = []
    for slide in args.slides:
        if slide.is_dir():
            targets.extend(sorted(slide.glob("*.html")))
        else:
            targets.append(slide)
    if not targets:
        print("layout validate: no slides given", file=sys.stderr)
        return 2

    report: dict[str, Any] = {"slides": [], "thresholds": {
        "coverage": [COVERAGE_MIN, COVERAGE_MAX],
        "interiorGapMax": INTERIOR_GAP_MAX,
        "marginRatioMax": MARGIN_RATIO_MAX,
        "bandRatioMax": BAND_RATIO_MAX,
        "deadQuadrantShare": DEAD_QUADRANT_SHARE,
    }}
    failed = 0

    for slide in targets:
        if not slide.is_file():
            print(f"FAIL {slide} — file not found", file=sys.stderr)
            failed += 1
            continue
        html = slide.read_text(encoding="utf-8", errors="replace")
        kind = slide_kind(html)
        try:
            png = render_with_any(slide, browsers, args.width, args.height, args.scale)
            width, height, channels, pixels = decode_png(png)
            metrics = analyse(width, height, channels, pixels)
        except (LayoutError, subprocess.TimeoutExpired, zlib.error) as exc:
            print(f"FAIL {slide} — {exc}", file=sys.stderr)
            failed += 1
            report["slides"].append({"slide": str(slide), "error": str(exc)})
            continue

        problems = evaluate(slide, metrics, kind, find_hardcoded_hex(html, args.strict_hex))
        report["slides"].append(
            {"slide": str(slide), "kind": kind, "metrics": metrics, "failures": problems}
        )
        if problems:
            failed += 1
            print(f"FAIL {slide}  [{kind}]")
            for problem in problems:
                print(f"       - {problem}")
        elif not args.quiet:
            ws = metrics["whitespace_ratio"]
            note = "" if kind == "content" else f", {kind} exception applied"
            print(f"pass {slide}  [{kind}]  whitespace {ws:.0%}{note}")

    if args.json:
        args.json.write_text(json.dumps(report, indent=2), encoding="utf-8")

    total = len(targets)
    if failed:
        print(f"\nlayout gate FAILED: {failed}/{total} slide(s) need fixing", file=sys.stderr)
        return 1
    print(f"\nlayout gate passed: {total}/{total} slide(s) balanced")
    return 0


if __name__ == "__main__":
    os.environ.setdefault("PYTHONIOENCODING", "utf-8")
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except AttributeError:
        pass
    raise SystemExit(main())
