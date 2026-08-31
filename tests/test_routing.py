from pathlib import Path
import sys
import unittest

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import validate_routing as routing
import compile_system as compiler


class RoutingTests(unittest.TestCase):
    def test_equal_scores_are_ambiguous(self):
        entries = {k:dict(triggers=['customer types'],intent='') for k in ('alpha','zulu')}
        result = routing.resolve('customer types','',entries,{})
        self.assertEqual(result['status'],'AMBIG')
        self.assertIsNone(result['top'])

    def test_unmatched_shape_cannot_fall_back_to_words(self):
        entries = {'a':dict(material='chart', arrangement='grid', itemCount='few',triggers=['customer types'])}
        self.assertEqual(routing.resolve('customer types','text-only / grid / few',entries,{})['status'],'MISS')

    def test_declared_variants_have_their_own_asset_policy(self):
        specs=compiler.load_specs()
        compiler.annotate_assets_and_alternates(specs)
        audience=specs['use-case-cards']
        self.assertEqual(audience['assetPolicy'],'generate')
        self.assertEqual(audience['shapeVariants'][0]['assetPolicy'],'none')
        screen=specs['feature-showcase']['shapeVariants'][0]
        self.assertEqual(screen['assetPolicy'],'must-supply')
        self.assertIn('use-case-cards',routing.by_shape('text-only / grid / few',specs))

    def test_malformed_variant_fails_compilation(self):
        specs=compiler.load_specs()
        specs['use-case-cards']['shapeVariants']=['text-only / grid']
        with self.assertRaises(compiler.BuildError):
            compiler.annotate_assets_and_alternates(specs)

    def test_all_existing_requests_keep_their_expected_layout(self):
        entries=routing.load_router();idf=routing.corpus_idf()
        for file in ('routing-cases.md','routing-cases-heldout.md'):
            for query,shape,expected in routing.load_cases(routing.ROOT/'specs'/file):
                with self.subTest(query=query):
                    result=routing.resolve(query,shape,entries,idf)
                    self.assertEqual(result['status'],'resolved')
                    self.assertEqual(result['top'],expected)
