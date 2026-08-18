#!/usr/bin/env python3
"""Reject generated editorial explainers with the wrong ratio or effectively grayscale output."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

try:  # Pillow is optional: it adds JPEG/WebP support but is not required for PNG output.
    from PIL import Image
except ModuleNotFoundError:  # pragma: no cover - depends on the machine
    Image = None

sys.path.insert(0, str(Path(__file__).resolve().parent))
from validate_layout import decode_png  # noqa: E402  (stdlib PNG fallback)


def parse_aspect(value: str) -> float:
    left, right = value.split(":", 1)
    return float(left) / float(right)


def sample_image(path: Path, step: int) -> tuple[int, int, list[tuple[int, int, int]]]:
    """Return (width, height, sampled RGB pixels), preferring Pillow when it is installed."""
    if Image is not None:
        with Image.open(path) as source:
            image = source.convert("RGB")
            width, height = image.size
            sample = image.copy()
            sample.thumbnail((320, 320))
            reader = getattr(sample, "get_flattened_data", sample.getdata)
            return width, height, list(reader())

    if path.suffix.lower() != ".png":
        raise SystemExit(
            f"cannot read {path.name}: Pillow is not installed and only PNG is supported without it. "
            "Install Pillow (pip install pillow) or save the generated asset as PNG."
        )
    width, height, channels, pixels = decode_png(path.read_bytes())
    stride = max(1, min(width, height) // 320) * step
    sampled: list[tuple[int, int, int]] = []
    for y in range(0, height, stride):
        base = y * width * channels
        for x in range(0, width, stride):
            i = base + x * channels
            sampled.append((pixels[i], pixels[i + 1], pixels[i + 2]))
    return width, height, sampled


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("image", type=Path)
    parser.add_argument("--aspect", default="16:9")
    parser.add_argument("--tolerance", type=float, default=0.035)
    parser.add_argument("--min-colorful", type=float, default=0.008)
    args = parser.parse_args()

    width, height, pixels = sample_image(args.image, 1)
    ratio = width / height
    expected = parse_aspect(args.aspect)
    ratio_error = abs(ratio - expected) / expected
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
