#!/usr/bin/env python3
"""Inspect a catalog recipe's bound selectors and theme-resolved fragment values.

The result describes managed fragments, not the entire computed style. Structural
geometry and per-slide overrides remain in CSS. This command never chooses a layout.
"""
import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'pptx'))
from generated_tokens import THEME_TOKENS, recipe as resolve_slot


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('pattern')
    parser.add_argument('--theme', choices=sorted(THEME_TOKENS), default='light')
    args = parser.parse_args()
    try:
        data = json.loads((ROOT / 'system/resolved-recipes.json').read_text(encoding='utf-8'))
        entry = data['entries'][args.pattern]
        result = dict(pattern=args.pattern, theme=args.theme, **entry)
        result['slots'] = {name:dict(**slot, resolved=resolve_slot(args.pattern, name, args.theme))
                           for name, slot in entry['slots'].items()}
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except (OSError, KeyError, ValueError) as exc:
        print(f'Cannot resolve recipe: {exc}; run compile_system.py first.', file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
