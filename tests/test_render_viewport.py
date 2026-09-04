"""The renderer must measure the whole slide, or say it could not.

`--window-size` sizes the window, not the viewport. Some Chromium builds hand back a shorter
viewport than asked for (994px for a requested 1080 in a Linux container), which silently turns
every screenshot into a CROP of the slide's top. Nothing reported it, and the layout gate read it
as 26 of 38 examples failing: no bottom margin, a lopsided top band, a dead lower half — all of
them artefacts of the missing strip rather than anything on the slide.
"""
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import validate_layout as layout


def solid(width: int, height: int, colour=(200, 100, 50)) -> bytes:
    px = bytearray()
    for _ in range(width * height):
        px += bytes(colour)
    return layout.encode_png(width, height, 3, px)


class PngRoundTripTests(unittest.TestCase):
    def test_encode_decode_round_trip(self):
        png = solid(7, 5, (1, 2, 3))
        self.assertEqual(layout.decode_png(png)[:3], (7, 5, 3))
        self.assertEqual(layout.png_size(png), (7, 5))

    def test_png_size_matches_a_full_decode(self):
        png = solid(13, 9)
        width, height, _, _ = layout.decode_png(png)
        self.assertEqual(layout.png_size(png), (width, height))

    def test_crop_keeps_the_top_left_and_drops_the_rest(self):
        px = bytearray()
        for y in range(4):
            for x in range(4):
                px += bytes((x, y, 0))
        png = layout.encode_png(4, 4, 3, px)
        width, height, channels, out = layout.decode_png(layout.crop_png(png, 2, 3))
        self.assertEqual((width, height), (2, 3))
        got = [tuple(out[i:i + 3]) for i in range(0, len(out), channels)]
        self.assertEqual(got, [(0, 0, 0), (1, 0, 0), (0, 1, 0), (1, 1, 0), (0, 2, 0), (1, 2, 0)])

    def test_an_image_that_already_fits_is_returned_untouched(self):
        png = solid(6, 6)
        self.assertIs(layout.crop_png(png, 6, 6), png)
        self.assertIs(layout.crop_png(png, 9, 9), png)

    def test_a_tall_image_is_cropped_even_when_it_is_narrow_enough(self):
        # A lexicographic tuple compare says (4, 99) <= (9, 9), which would skip this crop and
        # leave the dead strip in place — the exact failure the crop exists to remove.
        self.assertEqual(layout.png_size(layout.crop_png(solid(4, 99), 9, 9)), (4, 9))


class ViewportDeficitTests(unittest.TestCase):
    def setUp(self):
        layout._VIEWPORT_DEFICIT.clear()
        self.addCleanup(layout._VIEWPORT_DEFICIT.clear)

    def test_a_short_viewport_is_reported_as_the_shortfall(self):
        layout._VIEWPORT_DEFICIT[('chrome', 0.5)] = (0, 86)
        self.assertEqual(layout.viewport_deficit('chrome', 1920, 1080, 0.5), (0, 86))

    def test_an_unmeasurable_viewport_refuses_rather_than_guessing_zero(self):
        # Guessing zero is what produced a cropped capture that still looked like a valid render.
        with patch.object(layout, 'PROBE_HTML', '<!doctype html><title>no answer</title>'):
            with self.assertRaises(layout.LayoutError) as caught:
                layout.viewport_deficit(sys.executable, 1920, 1080, 0.5)
        self.assertIn('viewport', str(caught.exception))


class DegenerateBandTests(unittest.TestCase):
    """A band that is absent makes the ratio undefined, not equal to the other band's pixel count."""

    def metrics(self, top_gap: int, bottom_gap: int) -> dict:
        width, height = 96, 54
        px = bytearray()
        for y in range(height):
            for x in range(width):
                inside = top_gap <= y < height - bottom_gap and 4 <= x < width - 4
                px += bytes((0, 0, 0) if inside else (255, 255, 255))
        return layout.analyse(width, height, 3, px)

    def test_a_missing_band_is_unbounded_not_a_pixel_count(self):
        m = self.metrics(top_gap=20, bottom_gap=0)
        self.assertEqual(m['margins']['bottom'], 0)
        self.assertEqual(m['band_ratio'], layout.BAND_RATIO_UNBOUNDED)

    def test_two_real_bands_give_a_true_ratio(self):
        m = self.metrics(top_gap=20, bottom_gap=10)
        self.assertAlmostEqual(m['band_ratio'], m['margins']['top'] / m['margins']['bottom'])
        self.assertLess(m['band_ratio'], layout.BAND_RATIO_UNBOUNDED)


if __name__ == '__main__':
    unittest.main()
