"""Recipe integrity gates must reject false migration claims and unsafe compositions."""
import copy
import json
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import compile_system as compiler


class RecipeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = compiler.load_json(ROOT / 'system/recipes.json')
        cls.fragments = compiler.load_json(ROOT / 'system/hypertokens.json')['hypertokens']
        cls.specs = compiler.load_specs()

    def validate(self, data):
        return compiler.validate_recipes(data, self.fragments, self.specs)

    def test_every_catalog_pattern_has_a_connected_recipe(self):
        recipes = self.validate(self.data)
        output = json.loads(compiler.render_resolved_recipes(recipes, self.fragments, self.specs))
        self.assertEqual(output["coverage"]["layouts"], 30)
        self.assertEqual(output['coverage']['components'], 19)
        self.assertEqual(set(output['entries']), set(self.specs))

    def test_missing_and_orphaned_patterns_fail(self):
        for operation in ('missing', 'orphan'):
            data = copy.deepcopy(self.data)
            if operation == 'missing': del data['recipes']['metric-card']
            else: data['recipes']['made-up'] = data['recipes']['metric-card']
            with self.subTest(operation=operation), self.assertRaisesRegex(compiler.BuildError, 'coverage'):
                self.validate(data)

    def test_wrong_spec_and_status_cannot_claim_migration(self):
        for field, value in [('componentSpec', 'specs/components/evidence-card.md'),
                             ('migrationStatus', 'pilot')]:
            data = copy.deepcopy(self.data)
            data['recipes']['metric-card'][field] = value
            with self.subTest(field=field), self.assertRaises(compiler.BuildError):
                self.validate(data)

    def test_slot_bindings_are_exhaustive(self):
        data = copy.deepcopy(self.data)
        del data['recipes']['metric-card']['bindings']['root']
        with self.assertRaisesRegex(compiler.BuildError, 'bindings must match'):
            self.validate(data)

    def test_nonexistent_and_unsupported_selectors_fail(self):
        for selector in ['.missing .mc', '.mc:hover', '.mc, body', '.mc{color:red}', '']:
            data = copy.deepcopy(self.data)
            data['recipes']['metric-card']['bindings']['root'] = [selector]
            with self.subTest(selector=selector), self.assertRaises(compiler.BuildError):
                self.validate(data)

    def test_binding_evidence_requires_real_ancestry(self):
        doc = compiler.document('<style>.wrong .mc {}</style><div class="wrong"></div>'
                                '<section class="cards"><div class="mc"><b class="t">Value</b></div></section>')
        self.assertFalse(compiler.selector_matches(doc, '.wrong .mc'))
        self.assertTrue(compiler.selector_matches(doc, '.cards .mc b.t'))

    def test_conflicting_and_unknown_fragments_fail(self):
        for ref in ['surface.soft', 'unknown.fragment']:
            data = copy.deepcopy(self.data)
            data['recipes']['metric-card']['slots']['root'].append(ref)
            with self.subTest(ref=ref), self.assertRaises(compiler.BuildError):
                self.validate(data)

    def test_copied_css_values_do_not_count_as_connected(self):
        read_text = Path.read_text
        def disconnected(path, *args, **kwargs):
            text = read_text(path, *args, **kwargs)
            if path == ROOT / 'assets/base.css':
                text = text.replace('display:var(--recipe-layout-grid-display)', 'display:grid')
            return text
        with patch.object(Path, 'read_text', disconnected):
            with self.assertRaisesRegex(compiler.BuildError, 'disconnected'):
                self.validate(self.data)

    def test_variable_read_by_an_unbound_selector_fails(self):
        """A known variable name on a selector no recipe binds is the dangerous case.

        These references carry no fallback, so such a declaration is invalid at computed-value time
        and silently falls back to the property's initial value — `display` drops from grid to
        inline. Checking only that the name exists somewhere let that through with every gate green.
        """
        read_text = Path.read_text
        def unbound(path, *args, **kwargs):
            text = read_text(path, *args, **kwargs)
            if path == ROOT / 'assets/base.css':
                text += '\n.probe-unbound{display:var(--recipe-layout-grid-display)}\n'
            return text
        with patch.object(Path, 'read_text', unbound):
            with self.assertRaisesRegex(compiler.BuildError, 'unbound'):
                self.validate(self.data)

    def test_both_theme_values_reach_python_recipe_bridge(self):
        tokens = compiler.load_json(ROOT / 'system/tokens.json')
        foundations, themes = compiler.validate_tokens(tokens)
        namespace = {}
        exec(compiler.render_pptx_tokens(foundations, themes, self.fragments, self.data['recipes']), namespace)
        for mode in ('light', 'dark'):
            resolved = namespace['recipe']('metric-card', 'root', mode)
            self.assertEqual(resolved['background'], themes[mode]['surface']['value'][1:].upper())
            self.assertEqual(resolved['display'], 'flex')
            self.assertEqual(resolved['flex-direction'], 'column')
        self.assertNotEqual(namespace['recipe']('metric-card', 'root', 'light')['background'],
                            namespace['recipe']('metric-card', 'root', 'dark')['background'])

    def test_hypertoken_edit_propagates_to_both_outputs(self):
        fragments = copy.deepcopy(self.fragments)
        fragments['surface.panel']['properties']['background'] = '{accent-soft}'
        recipes = compiler.validate_recipes(self.data, fragments, self.specs)
        css = compiler.render_recipes_css(recipes, fragments)
        self.assertIn('--recipe-surface-panel-background: var(--accent-soft);', css)
        resolved = json.loads(compiler.render_resolved_recipes(recipes, fragments, self.specs))
        self.assertEqual(resolved['entries']['metric-card']['slots']['root']['properties']['background'],
                         'var(--accent-soft)')

    def test_shared_fragment_values_are_emitted_once(self):
        css = compiler.render_recipes_css(self.data['recipes'], self.fragments)
        self.assertEqual(css.count('--recipe-surface-panel-background:'), 1)
        for name in ('surface.card', 'text.heading', 'text.supporting', 'layout.stack.card'):
            # The consistency pass removed inert base-class aliases; do not restore them.
            self.assertEqual(self.fragments[name]['selectors'], ['.ht-' + name.replace('.', '-')])
