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

KNOWN LIMIT — column-local emptiness is not detected.
The emptiness checks scan rows across the whole canvas, so text anywhere on a row hides emptiness
elsewhere on it. A three-column slide whose middle column carries labels can hide two ballooned
side cards; that happened during this work and passed at 57% whitespace. A column-wise version was
built and withdrawn: measuring "surface with no text" per column cannot tell a stretched empty card
from a chart, a device mockup, or an illustration — six legitimate slides scored the same 74% as the
real defect. Since the deck-pacing rule actively wants those visuals, a check that flags them is
worse than the gap. Separating the two needs a measure of internal structure, not just ink.

Until then: this gate cannot tell you a card is inflated around its content. Look at the render.
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
BAND_SHARE_MIN = 0.12       # ...and the larger gap must be this share of the canvas to count
DEAD_QUADRANT_SHARE = 0.06  # a quadrant holding <6% of the ink reads as a dead corner
INK_ROW_FLOOR = 0.004       # a row/col needs this fraction of ink to count as content
COLOR_DELTA = 5             # per-channel delta that counts as "not background"; theme
                            # surfaces sit only ~5-10 off canvas, so this must stay sensitive
STRONG_INK_DELTA = 40       # text / icons / charts, as opposed to a flat surface fill
GRID_COLS, GRID_ROWS = 48, 27   # occupancy grid over the 16:9 canvas
CELL_INK_MIN = 0.02         # a grid cell counts as occupied at this much ink
CELL_TEXT_MIN = 0.006       # ...and as carrying real content at this much strong ink
TEXT_GAP_MAX = 0.22         # longest run of rows holding surface but no text

BROWSER_CANDIDATES = (
    # Windows
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    # macOS. The binary lives inside the .app bundle and is never on PATH, so the
    # shutil.which() scan above cannot see it — without these the gate is simply
    # unrunnable on a Mac, and "cannot run" is easy to mistake for "nothing to fix".
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
    "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
    str(Path.home() / "Applications/Google Chrome.app/Contents/MacOS/Google Chrome"),
    # Linux distributions that ship a versioned binary rather than a PATH alias
    "/usr/bin/google-chrome-stable",
    "/usr/bin/chromium-browser",
    "/snap/bin/chromium",
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
            "no Chromium browser found — pass --browser with the path to the Chrome/Edge binary "
            "(macOS: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome')"
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
    text_cells = [[0] * GRID_COLS for _ in range(GRID_ROWS)]

    for y in range(height):
        base = y * width * step
        row_total = 0
        row_index = min(y // cell_h, GRID_ROWS - 1)
        cell_row = cells[row_index]
        text_row = text_cells[row_index]
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
                    text_row[min(x // cell_w, GRID_COLS - 1)] += 1
        row_ink[y] = row_total
        total_ink += row_total

    cell_area = cell_w * cell_h
    occupied = [
        [1 if cells[r][c] >= cell_area * CELL_INK_MIN else 0 for c in range(GRID_COLS)]
        for r in range(GRID_ROWS)
    ]
    occupied_count = sum(sum(row) for row in occupied)
    coverage = occupied_count / (GRID_COLS * GRID_ROWS)

    # A second, stricter grid of cells that hold actual text/icons rather than a flat surface.
    # A card stretched tall with a tiny label inside is 'occupied' but carries no content, which
    # is the relocated-emptiness failure layout-balance.md warns about.
    text_occupied = [
        [1 if text_cells[r][c] >= cell_area * CELL_TEXT_MIN else 0 for c in range(GRID_COLS)]
        for r in range(GRID_ROWS)
    ]

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

    # Work out where the CONTENT ends before measuring anything, so a footer pinned 42px off the
    # canvas bottom does not become the slide's lower edge. It always did, which made the bottom
    # margin ~20px on every slide and turned any honest top margin into a lopsided band failure.
    band_rows = [any(occupied[r]) for r in range(GRID_ROWS)]
    filled = [r for r, v in enumerate(band_rows) if v]
    content_last = trim_page_chrome(band_rows, filled)
    content_bound = int((content_last + 1) * height / GRID_ROWS)
    body_rows = [r for r in rows if r < content_bound] or rows

    top, bottom = rows[0], height - 1 - body_rows[-1]
    left, right = cols[0], width - 1 - cols[-1]
    margins = {"top": top, "bottom": bottom, "left": left, "right": right}
    quadrant_share = [q / occupied_count for q in quadrants]

    # The most common real failure is a void INSIDE the content, not at its edges: a slide whose
    # top/bottom margins look even but whose lower half is dead. Margins cannot see that, so
    # measure the longest empty band between the first and last occupied cell-row.
    longest_gap = run = 0
    for r in range(filled[0], content_last + 1):
        run = 0 if band_rows[r] else run + 1
        longest_gap = max(longest_gap, run)
    interior_gap = longest_gap / GRID_ROWS

    text_rows = [any(text_occupied[r]) for r in range(GRID_ROWS)]
    t_filled = [r for r, v in enumerate(text_rows) if v]
    text_gap = 0.0
    if t_filled:
        longest_t = run = 0
        for r in range(t_filled[0], t_filled[-1] + 1):
            run = 0 if text_rows[r] else run + 1
            longest_t = max(longest_t, run)
        text_gap = longest_t / GRID_ROWS

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
        "band_share": max(top, bottom) / height,
        "interior_gap": interior_gap,
        "text_gap": text_gap,
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

# A "visual moment" per layout-balance.md: a real image, a logo row, a device mockup, or a
# generated editorial explainer. Icons and chips are seasoning and deliberately do not count.
VISUAL_MARKERS = (
    "data-editorial-explainer",
    "class=\"shot",
    "class='shot",
    " shot\"",
    " shot'",
    "logo-row",
    "logorow",
    "ui-mockup",
    "appframe",
    "phone",
    "device-stack",
    "<img",
)
# Output language is DECLARED, not hardcoded. The system's default is 繁中 primary + English
# supporting, but a deck asked for in another language must be able to pass — so the check is
# "does this slide contain a script its declared languages do not imply", not "is this Korean".
SCRIPTS = {
    "han": r"㐀-䶿一-鿿豈-﫿",
    "hangul": r"ᄀ-ᇿ㄰-㆏가-힣",
    # syllabaries only. U+30FB (・) and friends are CJK punctuation used throughout 繁中 —
    # including them made every slide with "IG・部落格" look like a Japanese deck.
    "kana": r"ぁ-ゖァ-ヺー",
    "cyrillic": r"Ѐ-ӿ",
    "arabic": r"؀-ۿ",
    "thai": r"฀-๿",
    "devanagari": r"ऀ-ॿ",
}
SCRIPT_RE = {name: re.compile("[" + rng + "]") for name, rng in SCRIPTS.items()}
# what each declared language legitimately brings with it
LANG_SCRIPTS = {
    "zh": {"han"}, "zh-hant": {"han"}, "zh-hans": {"han"},
    "ja": {"han", "kana"}, "ko": {"hangul", "han"},
    "en": set(), "fr": set(), "de": set(), "es": set(), "pt": set(), "it": set(), "vi": set(),
    "ru": {"cyrillic"}, "ar": {"arabic"}, "th": {"thai"}, "hi": {"devanagari"},
}
DEFAULT_LANGS = ("zh-hant", "en")
HTML_LANG_RE = re.compile(r"""<html[^>]*lang\s*=\s*["']([^"']+)["']""", re.I)


def declared_langs(html: str, override: str | None) -> list[str]:
    """Explicit --lang wins; otherwise the document's own <html lang>; otherwise the system default."""
    if override:
        return [x.strip().lower() for x in override.split(",") if x.strip()]
    match = HTML_LANG_RE.search(html)
    if match:
        tags = [match.group(1).strip().lower()]
        if not any(t.startswith("en") for t in tags):
            tags.append("en")  # English supporting copy is always allowed
        return tags
    return list(DEFAULT_LANGS)


def allowed_scripts(langs: list[str]) -> set[str]:
    allowed: set[str] = set()
    for tag in langs:
        allowed |= LANG_SCRIPTS.get(tag, LANG_SCRIPTS.get(tag.split("-")[0], set()))
    return allowed


TAG_RE = re.compile(r"<(script|style)\b.*?</\1>|<[^>]+>", re.S | re.I)


def visible_text(html: str) -> str:
    body = html.split("<body", 1)[-1] if "<body" in html else html
    return TAG_RE.sub(" ", body)


def has_visual_moment(html: str) -> bool:
    body = (html.split("<body", 1)[-1] if "<body" in html else html).lower()
    return any(marker.lower() in body for marker in VISUAL_MARKERS)


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
SPARSE_CLASSES = {
    "cover", "section-cover", "statement", "hero-quote", "divider",
    # a contents page, a scene-setting page and a closing thank-you are meant to breathe;
    # holding them to a content slide's density is what produced false "很空" findings
    "toc", "agenda", "context", "thanks", "appreciation", "closing",
}
SLIDE_CLASS_RE = re.compile(r"""class\s*=\s*["']([^"']*\bslide\b[^"']*)["']""", re.I)


CHROME_MAX_ROWS = 2      # a footer is one line of small type, never a block
CHROME_ZONE = 0.88       # ...and it lives in the bottom slice of the canvas


def trim_page_chrome(band_rows: list[bool], filled: list[int]) -> int:
    """Last row of real CONTENT, ignoring a footer or page number pinned to the canvas bottom.

    Page chrome is not content. It is one line of small muted type in the same place on every slide,
    and a designer does not compose against it. But it is the last ink on the canvas, so measuring
    the content extent to it charged every slide for the gap above its own footer — a slide whose
    content ended at 70% height was reported as having a 25% dead band it could only "fix" by
    stretching something into the footer's lap. That penalised composition rather than measuring it,
    and it is why a well-made sparse slide could not pass no matter how it was arranged.

    Chrome is recognised structurally, not by class name, since this works from pixels: a run of at
    most CHROME_MAX_ROWS cell-rows, starting inside the bottom CHROME_ZONE of the canvas, separated
    from the body by at least one empty row. Anything thicker or higher up is content and still
    counts, so a slide that genuinely dies before the bottom is still caught.
    """
    last = filled[-1]
    start = last
    while start - 1 >= 0 and band_rows[start - 1]:
        start -= 1
    if start == filled[0]:
        return last  # one contiguous block: there is no separated chrome
    if (last - start + 1) > CHROME_MAX_ROWS:
        return last
    if start / GRID_ROWS < CHROME_ZONE:
        return last
    body = [r for r in filled if r < start]
    return body[-1] if body else last


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


def evaluate(
    path: Path,
    metrics: dict[str, Any],
    kind: str,
    hexes: list[str],
    slide_text: str = "",
    langs: list[str] | None = None,
) -> list[str]:
    visible_text_cache = (slide_text,)
    langs = langs or list(DEFAULT_LANGS)
    lang_cache = (langs, allowed_scripts(langs))
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
            failures.append(
                "…and re-open this page's illustration decision before adding anything: a content "
                "page this thin is usually one of two things — an intention that was always visual "
                "and got routed to native cards (re-run the editorial-explainer suitability gate in "
                "slide-plan.md for it), or a page that should be merged with its neighbour or cut. "
                "Generating an image purely to fill the space is decoration, not density."
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
        # Catches the opposite mistake to the one above: stretching a card or table row until the
        # canvas is "covered" while the content inside stays tiny. Passing the gap check by
        # inflating empty surface is not a fix.
        if metrics["text_gap"] > TEXT_GAP_MAX:
            failures.append(
                f"stretched empty surface — a band {metrics['text_gap']:.0%} of the canvas tall is "
                f"covered but holds no text or figure (max {TEXT_GAP_MAX:.0%}). "
                "That is relocated emptiness, not density: grow the content itself (type scale, a "
                "real chart, more rows), don't inflate the container around it."
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
        # A ratio alone is not a band: 98px vs 44px is 2.2x but neither gap is empty space worth
        # naming. Require the larger gap to be a meaningful share of the canvas first.
        if metrics["band_ratio"] > BAND_RATIO_MAX and metrics["band_share"] > BAND_SHARE_MIN:
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

    stray = []
    for name, pattern in SCRIPT_RE.items():
        if name in lang_cache[1]:
            continue
        found = pattern.findall(visible_text_cache[0])
        if found:
            stray.append((name, "".join(sorted(set(found))[:8])))
    if stray:
        names = ", ".join(f"{name} ({sample}…)" for name, sample in stray)
        failures.append(
            f"copy contains script the declared language does not imply: {names}. "
            f"This slide declares {', '.join(lang_cache[0])} — set --lang if the deck is "
            "meant to be in another language."
        )

    if hexes:
        shown = ", ".join(hexes[:6]) + (" …" if len(hexes) > 6 else "")
        failures.append(
            f"hardcoded colour outside the token layer: {shown}. "
            "Golden rule is token names only — never hardcode colour."
        )

    return failures


def is_deck_container(html: str) -> bool:
    """True when the page holds more than one slide, i.e. it is a viewer rather than a slide."""
    return len(re.findall(r'class="(?:[^"]* )?slide[ "]', html)) > 1


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
        "--lang",
        help="declared output language(s), comma separated (default: the file's <html lang> "
        "plus English, else zh-Hant,en)",
    )
    parser.add_argument(
        "--deck",
        action="store_true",
        help="treat the given slides as one deck and also check deck-level visual pacing",
    )
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
            targets.extend(sorted(slide.rglob("*.html")))
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
        "bandShareMin": BAND_SHARE_MIN,
        "deadQuadrantShare": DEAD_QUADRANT_SHARE,
    }}
    failed = 0

    for slide in targets:
        if not slide.is_file():
            print(f"FAIL {slide} — file not found", file=sys.stderr)
            failed += 1
            continue
        html = slide.read_text(encoding="utf-8", errors="replace")
        if is_deck_container(html):
            # A scroll-through viewer holding many slides is not a slide. Rendering it at 1920x1080
            # measures a wall of frames and reports 100% coverage - a real number about the wrong
            # object. The slides inside it are gated individually, where the answer means something.
            print(f"skip {slide}  [deck container - gate its slides individually]")
            report["slides"].append({"slide": str(slide), "skipped": "deck-container"})
            continue
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

        problems = evaluate(
            slide,
            metrics,
            kind,
            find_hardcoded_hex(html, args.strict_hex),
            visible_text(html),
            declared_langs(html, args.lang),
        )
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

    # Deck-level visual pacing (layout-balance.md v12.7): per-slide checks all pass and the deck
    # still reads like a document. Only meaningful once the deck is long enough to feel dry.
    deck_note = ""
    if args.deck and len(targets) >= 8:
        visual = [
            t
            for t in targets
            if t.is_file() and has_visual_moment(t.read_text(encoding="utf-8", errors="replace"))
        ]
        if not visual:
            failed += 1
            print(
                f"\nFAIL deck pacing — {len(targets)} slides carry no genuine visual moment "
                "(real screenshot, logo-row, device mockup, or generated explainer). Icons and chips "
                "do not count. Elevate the best candidate page rather than shipping a dry deck."
            )
        else:
            deck_note = f"deck pacing: {len(visual)}/{len(targets)} slides carry a visual moment"

    total = len(targets)
    if deck_note:
        print(deck_note)
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
