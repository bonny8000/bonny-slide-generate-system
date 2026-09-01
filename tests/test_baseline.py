from contextlib import redirect_stdout,redirect_stderr
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import visual_baseline as baseline


class BaselineTests(unittest.TestCase):
    def test_missing_fingerprint_is_not_success(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);slide=root/'slide.html';slide.write_text('<main class="slide deck">New</main>', encoding='utf-8')
            saved=root/'baseline.json';saved.write_text(json.dumps({'slides':{}}), encoding='utf-8')
            with patch.object(sys,'argv',['visual_baseline.py','diff',str(slide),'--baseline',str(saved)]), \
                 patch.object(baseline,'find_browsers',return_value=['fake']), \
                 redirect_stdout(io.StringIO()),redirect_stderr(io.StringIO()):
                self.assertEqual(baseline.main(),1)

    def test_renderer_error_cannot_be_reported_as_visual_drift(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);slide=root/'slide.html';slide.write_text('<main class="slide deck">A</main>', encoding='utf-8')
            saved=root/'baseline.json'
            with patch.object(sys,'argv',['visual_baseline.py','capture',str(slide),'--baseline',str(saved)]), \
                 patch.object(baseline,'find_browsers',return_value=['fake']), \
                 patch.object(baseline,'render_with_any',side_effect=RuntimeError('render failed')), \
                 redirect_stdout(io.StringIO()),redirect_stderr(io.StringIO()):
                self.assertEqual(baseline.main(),2)
                self.assertFalse(saved.exists())

    def test_non_slide_formats_are_not_baseline_slides(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            for name,html in {'slide':'<main class="slide deck"></main>',
                              'poster':'<main class="slide poster"></main>',
                              'viewer':'<main class="slide"></main>'*2,'gallery':'<main>Reference</main>'}.items():
                (root/f'{name}.html').write_text(html, encoding='utf-8')
            self.assertEqual([p.name for p in baseline.targets([root])],['slide.html'])
