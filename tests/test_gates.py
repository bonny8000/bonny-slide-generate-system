"""Regression cases for false passes found in the August 2026 audit."""
from contextlib import redirect_stdout, redirect_stderr
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import validate_layout as layout


class PlanTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        (self.root / 'art').mkdir()
        (self.root / 'art' / 'fresh image.png').write_bytes(b'image fixture')

    def tearDown(self):
        self.tmp.cleanup()

    def record(self, id='s1', generated=False):
        row = dict(id=id, gate='no', trigger='structural-page', hard_candidate=False, reason='cover')
        if generated:
            row.update(gate='yes', variant='workflow-transform', generator='built-in-imagegen',
                       asset='art/fresh image.png', references=['style-reference.png'])
        return row

    def run_plan(self, html, plan):
        (self.root / 'deck.html').write_text(html)
        (self.root / 'plan.json').write_text(json.dumps(plan))
        return subprocess.run([sys.executable, str(ROOT / 'scripts/validate_editorial_explainer_plan.py'),
                               str(self.root/'plan.json'), str(self.root/'deck.html')],
                              capture_output=True, text=True)

    def test_missing_decision_cannot_pass(self):
        r = self.run_plan('<main class="slide" id="s1">A</main><main class="slide" id="s2">B</main>',
                          {'slides':[self.record()]})
        self.assertEqual(r.returncode, 1)
        self.assertIn('s2', r.stderr)

    def test_non_slide_id_is_not_a_slide(self):
        r = self.run_plan('<div id="s1"></div><main class="slide" id="s2">B</main>', {'slides':[self.record()]})
        self.assertEqual(r.returncode, 1)

    def test_duplicate_html_ids_fail(self):
        r = self.run_plan('<main class="slide" id="s1"></main>'*2, {'slides':[self.record()]})
        self.assertIn('duplicate HTML', r.stderr)

    def test_missing_html_id_fails(self):
        r = self.run_plan('<main class="slide"></main>', {'slides':[self.record()]})
        self.assertEqual(r.returncode, 1)

    def test_image_on_another_slide_cannot_satisfy_record(self):
        html = '<main class="slide" id="s1">A</main><main class="slide" id="s2"><img data-editorial-explainer="workflow-transform" src="art/fresh image.png"></main>'
        r = self.run_plan(html, {'slides':[self.record(generated=True), self.record('s2')]})
        self.assertEqual(r.returncode, 1)

    def test_path_in_text_or_comment_is_not_an_asset(self):
        html = '<main class="slide" id="s1"><div data-editorial-explainer="workflow-transform">art/fresh image.png<!-- <img src="art/fresh image.png"> --></div></main>'
        self.assertEqual(self.run_plan(html, {'slides':[self.record(generated=True)]}).returncode, 1)

    def test_hidden_asset_fails(self):
        html = '<main class="slide" id="s1"><div hidden><img data-editorial-explainer="workflow-transform" src="art/fresh image.png"></div></main>'
        self.assertEqual(self.run_plan(html, {'slides':[self.record(generated=True)]}).returncode, 1)

    def test_encoded_local_asset_and_attribute_spacing_pass(self):
        html = "<MAIN class = 'slide deck' id = 's1'><figure data-editorial-explainer='workflow-transform'><img src='./art/fresh%20image.png?rev=1'></figure></MAIN>"
        self.assertEqual(self.run_plan(html, {'slides':[self.record(generated=True)]}).returncode, 0)

    def test_wrong_variant_stage_fails(self):
        html = '<main class="slide" id="s1"><div data-editorial-explainer="workflow-transform"></div><img data-editorial-explainer="ui-qa" src="art/fresh image.png"></main>'
        self.assertEqual(self.run_plan(html, {'slides':[self.record(generated=True)]}).returncode, 1)

    def test_complete_native_plan_passes(self):
        html = '<main class="slide cover" id="s1">A</main><main class="slide" id="s2">B</main>'
        self.assertEqual(self.run_plan(html, {'slides':[self.record(),self.record('s2')]}).returncode, 0)

    def test_invalid_json_shape_reports_failure_not_traceback(self):
        r = self.run_plan('<main class="slide" id="s1"></main>', [])
        self.assertEqual(r.returncode, 1)
        self.assertNotIn('Traceback', r.stderr)

    def test_directory_input_requires_decisions_for_every_file(self):
        (self.root/'one.html').write_text('<main class="slide" id="s1">One</main>')
        (self.root/'two.html').write_text('<main class="slide" id="s2">Two</main>')
        plan=self.root/'plan.json'
        command=[sys.executable,str(ROOT/'scripts/validate_editorial_explainer_plan.py'),str(plan),str(self.root)]
        plan.write_text(json.dumps({'slides':[self.record()]}))
        missing=subprocess.run(command,capture_output=True,text=True)
        self.assertEqual(missing.returncode,1)
        self.assertIn('s2',missing.stderr)
        plan.write_text(json.dumps({'slides':[self.record(),self.record('s2')]}))
        self.assertEqual(subprocess.run(command,capture_output=True).returncode,0)


class MarkupTests(unittest.TestCase):
    def test_omitted_head_end_does_not_hide_real_slides(self):
        for opening in ('', '<body>'):
            html = '<html><head><style>.phone{}</style>' + opening + '<main class="slide" id="one"><img src="real.png"></main><main class="slide" id="two">Text</main>'
            self.assertEqual(len(layout.html_slides(html)),2)
            self.assertTrue(layout.has_visual_moment(html))
            self.assertIn('Text',layout.visible_text(html))

    def test_css_script_comment_and_text_do_not_count(self):
        html = '''<head><style>.phone{display:block}</style><script>let s='<img src="fake.png">'</script></head>
        <!-- <div class="logo-row">A</div> --><main class="slide">phone appframe logo-row</main>'''
        self.assertFalse(layout.has_visual_moment(html))

    def test_template_is_inert(self):
        self.assertFalse(layout.has_visual_moment('<template><img src="a.png"></template>'))
        self.assertFalse(layout.is_deck_container('<main class="slide"></main><template><main class="slide"></main></template>'))

    def test_hidden_ancestors_do_not_count(self):
        for attr in ['hidden', 'style="display: none !important"', 'style="opacity:0"', 'aria-hidden="true"']:
            with self.subTest(attr=attr):
                self.assertFalse(layout.has_visual_moment(f'<div {attr}><img src="a.png"></div>'))

    def test_actual_device_and_image_count(self):
        self.assertTrue(layout.has_visual_moment('<main class="slide"><div class="phone"><span class="sk"></span></div></main>'))
        self.assertTrue(layout.has_visual_moment('<img src="a.png">'))
        self.assertFalse(layout.has_visual_moment('<img>'))

    def test_type_uses_elements_not_script_examples(self):
        html = '''<script>let sample='<main class="slide cover">';</script><main class="slide deck">A</main>'''
        self.assertEqual(layout.slide_kind(html), 'content')
        self.assertEqual(layout.slide_kind('<main class = "slide cover">A</main>'), 'sparse-exception')

    def test_deck_detection_handles_quotes_and_space(self):
        self.assertTrue(layout.is_deck_container("<main class = 'slide deck'></main><section class = 'slide'></section>"))

    def test_renderer_failure_is_exit_two(self):
        with tempfile.TemporaryDirectory() as tmp:
            slide = Path(tmp)/'slide.html'
            slide.write_text('<main class="slide">A</main>')
            with patch.object(sys, 'argv', ['validate_layout.py',str(slide)]), \
                 patch.object(layout,'find_browsers',return_value=['fake']), \
                 patch.object(layout,'render_with_any',side_effect=layout.LayoutError('renderer failed')), \
                 redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
                self.assertEqual(layout.main(), 2)

    def test_viewer_alone_cannot_report_success(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp)/'viewer.html'
            path.write_text('<main class="slide"></main>'*2)
            with patch.object(sys, 'argv', ['validate_layout.py',str(path)]), \
                 patch.object(layout,'find_browsers',return_value=['fake']), \
                 redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
                self.assertEqual(layout.main(), 2)

    def test_footer_does_not_extend_text_gap(self):
        width, height = 320, 180
        pixels = bytearray([255] * width * height * 3)
        def fill(x1,y1,x2,y2,value):
            for y in range(y1,y2):
                for x in range(x1,x2):
                    i=(y*width+x)*3
                    pixels[i:i+3]=bytes([value]*3)
        fill(20,50,300,115,230)
        fill(40,60,280,65,20)
        fill(40,90,280,95,20)
        before=layout.analyse(width,height,3,pixels)['text_gap']
        fill(20,171,60,174,20)
        after=layout.analyse(width,height,3,pixels)['text_gap']
        self.assertEqual(before,after)


if __name__ == '__main__':
    unittest.main()
