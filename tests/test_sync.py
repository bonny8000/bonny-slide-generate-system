from pathlib import Path
import sys
import tempfile
import unittest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from sync_examples import rebuild, shipped_css, dark_theme
from example_files import collect

class SyncTests(unittest.TestCase):
    def test_bundle_includes_base_only_once(self):
        self.assertEqual(shipped_css(False).count('Bonny Slide System v6'),1)

    def test_dark_mode_and_authored_rules_survive_repeated_sync(self):
        local='/* keep design rationale */\n@media print {.ctable {width:100%}}\n.ctable{font-size:17px}'
        html='<html><head><style data-shipped>:root{--canvas:#1B1B20}</style><style data-slide>'+local+'</style></head><main class="slide deck"><table class="ctable"></table></main></html>'
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/'a.html';p.write_text(html)
            new,_=rebuild(p);p.write_text(new)
            twice,_=rebuild(p)
        self.assertEqual(new,twice)
        self.assertTrue(dark_theme(new))
        self.assertIn(local,new)
        self.assertNotIn('width:revert',new)

    def test_frozen_examples_are_not_default_targets(self):
        paths=collect([ROOT/'examples'])
        self.assertTrue(paths)
        self.assertFalse(any('_ab' in p.parts or '_audit' in p.parts for p in paths))
        self.assertGreater(len(collect([ROOT/'examples'],True)),len(paths))
