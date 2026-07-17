#!/usr/bin/env python3
"""Reject generated editorial explainers with the wrong ratio or effectively grayscale output."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from PIL import Image


def parse_aspect(value: str) -> float:
    left, right = value.split(":", 1)
    return float(left) / float(right)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("image", type=Path)
    parser.add_argument("--aspect", default="16:9")
    parser.add_argument("--tolerance", type=float, default=0.035)
    parser.add_argument("--min-colorful", type=float, default=0.008)
    args = parser.parse_args()

    with Image.open(args.image) as source:
        image = source.convert("RGB")
        width, height = image.size
        ratio = width / height
        expected = parse_aspect(args.aspect)
        ratio_error = abs(ratio - expected) / expected

        sample = image.copy()
        sample.thumbnail((320, 320))
        pixel_reader = getattr(sample, "get_flattened_data", sample.getdata)
        pixels = list(pixel_reader())
        colorful = sum(1 for r, g, b in pixels if max(r, g, b) - min(r, g, b) >= 24)
        colorful_share = colorful / max(1, len(pixels))

    problems = []
    if ratio_error > args.tolerance:
        problems.append(
            f"aspect {width}:{height} ({ratio:.4f}) misses {args.aspect} by {ratio_error:.1%}"
        )
    if colorful_share < args.min_colorful:
        problems.append(
            f"only {colorful_share:.2%} of sampled pixels are chromatic; output appears grayscale"
        )

    if problems:
        print("FAIL: " + "; ".join(problems), file=sys.stderr)
        raise SystemExit(1)

    print(
        f"PASS: {width}x{height}, aspect error {ratio_error:.2%}, "
        f"chromatic pixels {colorful_share:.2%}"
    )


if __name__ == "__main__":
    main()
