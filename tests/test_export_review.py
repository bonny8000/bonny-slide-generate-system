import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from export_pdf import printable
import calibrate_gate as calibration


class ExportReviewTests(unittest.TestCase):
    def test_print_wrapper_preserves_source_and_relative_assets(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/'slide.html'
            text='<html><head><title>x</title></head><body><main class="slide"><img src="art.png">Hello</main></body></html>'
            p.write_text(text, encoding='utf-8')
            result=printable(p)
            self.assertIn(p.parent.as_uri()+'/',result)
            self.assertIn('1920px 1080px',result)
            self.assertIn('src="art.png"',result)
            self.assertEqual(p.read_text(encoding='utf-8'),text)

    def test_export_rejects_viewers(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/'viewer.html';p.write_text('<main class="slide"></main>'*2, encoding='utf-8')
            with self.assertRaises(ValueError):printable(p)

    def test_reviewed_variants_are_hash_verified(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/'manifest.json';slide=Path(tmp)/'a.html';slide.write_text('changed', encoding='utf-8')
            p.write_text(json.dumps({'rounds':{'51':{'variants':{'A':{'path':'a.html','sha256':'bad'}}}}}), encoding='utf-8')
            with patch.object(calibration,'parse_spec',return_value={51:{'winner':'B'}}):
                with self.assertRaisesRegex(ValueError,'changed after rendering'):
                    calibration.load_pairs(p)

    def test_all_five_new_human_votes_have_portable_evidence(self):
        pairs,_=calibration.load_pairs(ROOT/'specs/ab-reviewed/2026-08-31/manifest.json')
        votes={n:w for n,w,_,_ in pairs if n>=51}
        self.assertEqual(votes,{51:'B',52:'A',53:'A',54:'B',55:'A'})
