#!/usr/bin/env python3
"""Validate and compile the Bonny Slide System token pipeline.

Canonical inputs live in system/. Generated outputs are deterministic and
must not be edited by hand.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SYSTEM = ROOT / "system"
REF_RE = re.compile(r"^\{([a-z][a-z0-9-]*)\}$")
TOKEN_NAME_RE = re.compile(r"^[a-z][a-z0-9-]*$")
HYPERTOKEN_NAME_RE = re.compile(r"^[a-z][a-z0-9-]*(\.[a-z][a-z0-9-]*)+$")
SELECTOR_RE = re.compile(r"^\.[a-z][a-z0-9_-]*$")
PROPERTY_RE = re.compile(r"^[a-z][a-z0-9-]*$")


class BuildError(ValueError):
    """Raised when canonical design-system data is invalid."""


def _no_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise BuildError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def load_json(path: Path) -> dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=_no_duplicate_keys)
    except (json.JSONDecodeError, OSError) as exc:
        raise BuildError(f"cannot read {path.relative_to(ROOT)}: {exc}") from exc


def require_keys(data: dict[str, Any], required: set[str], allowed: set[str], where: str) -> None:
    missing = required - data.keys()
    extra = data.keys() - allowed
    if missing:
        raise BuildError(f"{where}: missing keys {sorted(missing)}")
    if extra:
        raise BuildError(f"{where}: unsupported keys {sorted(extra)}")


def validate_token_map(token_map: Any, where: str) -> None:
    if not isinstance(token_map, dict) or not token_map:
        raise BuildError(f"{where}: expected a non-empty token object")
    allowed_types = {"color", "dimension", "fontFamily", "letterSpacing", "lineHeight", "shadow"}
    for name, token in token_map.items():
        if not TOKEN_NAME_RE.fullmatch(name):
            raise BuildError(f"{where}: invalid token name {name!r}")
        if not isinstance(token, dict):
            raise BuildError(f"{where}.{name}: expected an object")
        require_keys(token, {"type", "value"}, {"type", "value"}, f"{where}.{name}")
        if token["type"] not in allowed_types:
            raise BuildError(f"{where}.{name}: unsupported type {token['type']!r}")
        if not isinstance(token["value"], str) or not token["value"]:
            raise BuildError(f"{where}.{name}: value must be a non-empty string")


def validate_tokens(data: dict[str, Any]) -> tuple[dict[str, Any], dict[str, dict[str, Any]]]:
    require_keys(
        data,
        {"$schema", "version", "description", "foundations", "themes"},
        {"$schema", "version", "description", "foundations", "themes"},
        "tokens.json",
    )
    foundations = data["foundations"]
    themes = data["themes"]
    validate_token_map(foundations, "tokens.foundations")
    if not isinstance(themes, dict) or len(themes) < 2:
        raise BuildError("tokens.themes: expected at least two themes")
    for mode, token_map in themes.items():
        if not TOKEN_NAME_RE.fullmatch(mode):
            raise BuildError(f"tokens.themes: invalid theme name {mode!r}")
        validate_token_map(token_map, f"tokens.themes.{mode}")
    theme_key_sets = {tuple(sorted(token_map)) for token_map in themes.values()}
    if len(theme_key_sets) != 1:
        raise BuildError("all themes must expose the same token names")
    foundation_names = set(foundations)
    for name, token in foundations.items():
        match = REF_RE.fullmatch(token["value"])
        if match and match.group(1) not in foundation_names:
            raise BuildError(f"tokens.foundations.{name}: unknown reference {match.group(1)!r}")
    return foundations, themes


def validate_hypertokens(
    data: dict[str, Any], foundations: dict[str, Any], themes: dict[str, dict[str, Any]]
) -> dict[str, Any]:
    require_keys(
        data,
        {"$schema", "version", "selectionPolicy", "hypertokens"},
        {"$schema", "version", "selectionPolicy", "hypertokens"},
        "hypertokens.json",
    )
    policy = data["selectionPolicy"]
    require_keys(
        policy,
        {"migrationStatusAffectsSelection", "note"},
        {"migrationStatusAffectsSelection", "note"},
        "hypertokens.selectionPolicy",
    )
    if policy["migrationStatusAffectsSelection"] is not False:
        raise BuildError("hypertoken migration status must never affect component selection")
    hypertokens = data["hypertokens"]
    if not isinstance(hypertokens, dict) or not hypertokens:
        raise BuildError("hypertokens.hypertokens: expected a non-empty object")
    available_tokens = set(foundations) | set(next(iter(themes.values())))
    statuses = {"pilot", "migrated", "legacy"}
    claimed_selectors: dict[str, str] = {}
    for name, item in hypertokens.items():
        if not HYPERTOKEN_NAME_RE.fullmatch(name):
            raise BuildError(f"invalid hypertoken name {name!r}")
        if not isinstance(item, dict):
            raise BuildError(f"hypertokens.{name}: expected an object")
        require_keys(
            item,
            {"description", "migrationStatus", "selectors", "properties"},
            {"description", "migrationStatus", "selectors", "properties"},
            f"hypertokens.{name}",
        )
        if item["migrationStatus"] not in statuses:
            raise BuildError(f"hypertokens.{name}: invalid migrationStatus")
        selectors = item["selectors"]
        if not isinstance(selectors, list) or not selectors or len(selectors) != len(set(selectors)):
            raise BuildError(f"hypertokens.{name}: selectors must be a non-empty unique list")
        expected_class = ".ht-" + name.replace(".", "-")
        if selectors[0] != expected_class:
            raise BuildError(f"hypertokens.{name}: first selector must be {expected_class!r}")
        for selector in selectors:
            if not isinstance(selector, str) or not SELECTOR_RE.fullmatch(selector):
                raise BuildError(f"hypertokens.{name}: unsafe selector {selector!r}")
            if selector.startswith(".ht-") and selector in claimed_selectors:
                raise BuildError(
                    f"hypertokens.{name}: generated selector {selector!r} already belongs to "
                    f"{claimed_selectors[selector]!r}"
                )
            if selector.startswith(".ht-"):
                claimed_selectors[selector] = name
        properties = item["properties"]
        if not isinstance(properties, dict) or not properties:
            raise BuildError(f"hypertokens.{name}: properties must be a non-empty object")
        for prop, value in properties.items():
            if not PROPERTY_RE.fullmatch(prop):
                raise BuildError(f"hypertokens.{name}: unsafe CSS property {prop!r}")
            if not isinstance(value, str) or not value:
                raise BuildError(f"hypertokens.{name}.{prop}: value must be a non-empty string")
            match = REF_RE.fullmatch(value)
            if match and match.group(1) not in available_tokens:
                raise BuildError(f"hypertokens.{name}.{prop}: unknown token {match.group(1)!r}")
    return hypertokens


def validate_recipes(data: dict[str, Any], hypertokens: dict[str, Any]) -> dict[str, Any]:
    require_keys(
        data,
        {"$schema", "version", "selectionPolicy", "recipes"},
        {"$schema", "version", "selectionPolicy", "recipes"},
        "recipes.json",
    )
    policy = data["selectionPolicy"]
    require_keys(
        policy,
        {"primaryKey", "migrationStatusAffectsSelection", "source"},
        {"primaryKey", "migrationStatusAffectsSelection", "source"},
        "recipes.selectionPolicy",
    )
    if policy != {
        "primaryKey": "intent",
        "migrationStatusAffectsSelection": False,
        "source": "specs/content-map.md",
    }:
        raise BuildError("recipe selection policy must remain intention-first with zero migration weighting")
    recipes = data["recipes"]
    if not isinstance(recipes, dict) or not recipes:
        raise BuildError("recipes.recipes: expected a non-empty object")
    statuses = {"pilot", "migrated", "legacy"}
    for name, recipe in recipes.items():
        if not TOKEN_NAME_RE.fullmatch(name):
            raise BuildError(f"invalid recipe name {name!r}")
        if not isinstance(recipe, dict):
            raise BuildError(f"recipes.{name}: expected an object")
        require_keys(
            recipe,
            {"migrationStatus", "componentSpec", "slots"},
            {"migrationStatus", "componentSpec", "slots"},
            f"recipes.{name}",
        )
        if recipe["migrationStatus"] not in statuses:
            raise BuildError(f"recipes.{name}: invalid migrationStatus")
        spec_path = ROOT / recipe["componentSpec"]
        if not spec_path.is_file():
            raise BuildError(f"recipes.{name}: missing component spec {recipe['componentSpec']!r}")
        slots = recipe["slots"]
        if not isinstance(slots, dict) or not slots:
            raise BuildError(f"recipes.{name}: slots must be a non-empty object")
        for slot, refs in slots.items():
            if not TOKEN_NAME_RE.fullmatch(slot):
                raise BuildError(f"recipes.{name}: invalid slot {slot!r}")
            if not isinstance(refs, list) or not refs or len(refs) != len(set(refs)):
                raise BuildError(f"recipes.{name}.{slot}: expected a non-empty unique list")
            for ref in refs:
                if ref not in hypertokens:
                    raise BuildError(f"recipes.{name}.{slot}: unknown hypertoken {ref!r}")
    return recipes


def css_value(value: str) -> str:
    match = REF_RE.fullmatch(value)
    return f"var(--{match.group(1)})" if match else value


def render_foundations_css(foundations: dict[str, Any]) -> str:
    lines = [
        "/* AUTO-GENERATED by scripts/compile_system.py. DO NOT EDIT. */",
        "@layer tokens {",
        "  :root {",
    ]
    lines.extend(f"    --{name}: {css_value(token['value'])};" for name, token in foundations.items())
    lines.extend(["  }", "}", ""])
    return "\n".join(lines)


def render_theme_css(mode: str, token_map: dict[str, Any]) -> str:
    lines = [
        "/* AUTO-GENERATED by scripts/compile_system.py from system/tokens.json. DO NOT EDIT. */",
        f"/* Theme: {mode}. Load exactly one theme per deck. */",
        "@layer tokens {",
        "  :root {",
    ]
    lines.extend(f"    --{name}: {css_value(token['value'])};" for name, token in token_map.items())
    lines.extend(["  }", "}", ""])
    return "\n".join(lines)


def render_hypertokens_css(hypertokens: dict[str, Any]) -> str:
    lines = [
        "/* AUTO-GENERATED by scripts/compile_system.py. DO NOT EDIT. */",
        "/* Low-specificity implementation fragments; component rules remain authoritative. */",
        "@layer hypertokens {",
    ]
    for name, item in hypertokens.items():
        selectors = ", ".join(item["selectors"])
        lines.append(f"  /* {name} [{item['migrationStatus']}] */")
        lines.append(f"  :where({selectors}) {{")
        lines.extend(f"    {prop}: {css_value(value)};" for prop, value in item["properties"].items())
        lines.append("  }")
    lines.extend(["}", ""])
    return "\n".join(lines)


def render_base_bundle(foundations_css: str, hypertokens_css: str) -> str:
    """Create an import-free base stylesheet for self-contained HTML outputs."""
    base_source = (ROOT / "assets" / "base.css").read_text(encoding="utf-8").replace("\r\n", "\n")
    base_body = "\n".join(
        line for line in base_source.splitlines() if not line.startswith("@import url(")
    ).lstrip()
    return "\n".join(
        [
            "/* AUTO-GENERATED self-contained bundle. DO NOT EDIT. */",
            foundations_css.rstrip(),
            "",
            hypertokens_css.rstrip(),
            "",
            base_body.rstrip(),
            "",
        ]
    )


def resolve_foundation(name: str, foundations: dict[str, Any], seen: set[str] | None = None) -> str:
    seen = set() if seen is None else set(seen)
    if name in seen:
        raise BuildError(f"cyclic foundation token reference at {name!r}")
    seen.add(name)
    value = foundations[name]["value"]
    match = REF_RE.fullmatch(value)
    return resolve_foundation(match.group(1), foundations, seen) if match else value


def python_value(value: str) -> str:
    if re.fullmatch(r"#[0-9A-Fa-f]{6}", value):
        return value[1:].upper()
    return value


def render_pptx_tokens(
    foundations: dict[str, Any], themes: dict[str, dict[str, Any]], hypertokens: dict[str, Any]
) -> str:
    lines = [
        '"""AUTO-GENERATED by scripts/compile_system.py. DO NOT EDIT."""',
        "",
        "FOUNDATIONS = {",
    ]
    for name in foundations:
        lines.append(f"    {name!r}: {python_value(resolve_foundation(name, foundations))!r},")
    lines.extend(["}", "", "THEME_TOKENS = {"])
    for mode, token_map in themes.items():
        lines.append(f"    {mode!r}: {{")
        for name, token in token_map.items():
            lines.append(f"        {name!r}: {python_value(token['value'])!r},")
        lines.append("    },")
    lines.extend(["}", "", "HYPERTOKEN_VALUES = {"])
    for name, item in hypertokens.items():
        lines.append(f"    {name!r}: {{")
        for prop, value in item["properties"].items():
            match = REF_RE.fullmatch(value)
            record = {"token": match.group(1)} if match else {"value": value}
            lines.append(f"        {prop!r}: {record!r},")
        lines.append("    },")
    lines.extend(
        [
            "}",
            "",
            "def _compat_tokens(mode):",
            "    return {name.replace('-', '_'): value for name, value in THEME_TOKENS[mode].items()}",
            "",
            "LIGHT = _compat_tokens('light')",
            "DARK = _compat_tokens('dark')",
            "",
            "def apply_tone(token_map, tone=None):",
            "    result = dict(token_map)",
            "    if tone == 'pos':",
            "        result['accent'], result['accent_soft'] = result['pos'], result['pos_soft']",
            "    if tone == 'neg':",
            "        result['accent'], result['accent_soft'] = result['neg'], result['neg_soft']",
            "    if tone == 'warn':",
            "        result['accent'], result['accent_soft'] = result['warn'], result['warn_soft']",
            "    return result",
            "",
            "def tokens(mode):",
            "    if mode not in THEME_TOKENS:",
            "        raise ValueError(f'unknown mode: {mode}')",
            "    return _compat_tokens(mode)",
            "",
            "def hypertoken(name, mode):",
            "    if name not in HYPERTOKEN_VALUES:",
            "        raise KeyError(name)",
            "    if mode not in THEME_TOKENS:",
            "        raise ValueError(f'unknown mode: {mode}')",
            "    pool = {**FOUNDATIONS, **THEME_TOKENS[mode]}",
            "    result = {}",
            "    for prop, record in HYPERTOKEN_VALUES[name].items():",
            "        result[prop] = pool[record['token']] if 'token' in record else record['value']",
            "    return result",
            "",
        ]
    )
    return "\n".join(lines)


def render_reference(hypertokens: dict[str, Any], recipes: dict[str, Any]) -> str:
    lines = [
        "<!-- AUTO-GENERATED by scripts/compile_system.py. DO NOT EDIT. -->",
        "# Hypertoken reference",
        "",
        "Hypertokens are reusable implementation fragments. They do **not** select components or layouts.",
        "Selection remains intention-first in `specs/content-map.md`; migration status has zero selection weight.",
        "",
        "## Pilot hypertokens",
        "",
        "| id | status | selectors | properties |",
        "|---|---|---|---|",
    ]
    for name, item in hypertokens.items():
        selectors = "<br>".join(f"`{selector}`" for selector in item["selectors"])
        properties = "<br>".join(
            f"`{prop}: {value}`" for prop, value in item["properties"].items()
        )
        lines.append(f"| `{name}` | {item['migrationStatus']} | {selectors} | {properties} |")
    lines.extend(
        [
            "",
            "## Pilot recipes",
            "",
            "| recipe | status | spec | slot mappings |",
            "|---|---|---|---|",
        ]
    )
    for name, recipe in recipes.items():
        mappings = "<br>".join(
            f"`{slot}` → " + ", ".join(f"`{ref}`" for ref in refs)
            for slot, refs in recipe["slots"].items()
        )
        lines.append(
            f"| `{name}` | {recipe['migrationStatus']} | `{recipe['componentSpec']}` | {mappings} |"
        )
    lines.append("")
    return "\n".join(lines)


def outputs() -> dict[Path, str]:
    token_data = load_json(SYSTEM / "tokens.json")
    hypertoken_data = load_json(SYSTEM / "hypertokens.json")
    recipe_data = load_json(SYSTEM / "recipes.json")
    foundations, themes = validate_tokens(token_data)
    hypertokens = validate_hypertokens(hypertoken_data, foundations, themes)
    recipes = validate_recipes(recipe_data, hypertokens)
    foundations_css = render_foundations_css(foundations)
    hypertokens_css = render_hypertokens_css(hypertokens)
    result = {
        ROOT / "assets" / "generated" / "foundations.css": foundations_css,
        ROOT / "assets" / "generated" / "hypertokens.css": hypertokens_css,
        ROOT / "assets" / "generated" / "base-bundle.css": render_base_bundle(
            foundations_css, hypertokens_css
        ),
        ROOT / "pptx" / "generated_tokens.py": render_pptx_tokens(foundations, themes, hypertokens),
        ROOT / "specs" / "tokens" / "generated-hypertoken-reference.md": render_reference(
            hypertokens, recipes
        ),
    }
    for mode, token_map in themes.items():
        result[ROOT / "assets" / f"tokens-{mode}.css"] = render_theme_css(mode, token_map)
    return result


def write_if_changed(path: Path, content: str) -> bool:
    encoded = content.replace("\r\n", "\n")
    if path.is_file() and path.read_text(encoding="utf-8").replace("\r\n", "\n") == encoded:
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(encoded, encoding="utf-8", newline="\n")
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="validate and fail if generated files are stale")
    args = parser.parse_args()
    try:
        compiled = outputs()
        stale = [path for path, content in compiled.items() if not path.is_file() or path.read_text(encoding="utf-8").replace("\r\n", "\n") != content]
        if args.check:
            if stale:
                print("stale generated files:", file=sys.stderr)
                for path in stale:
                    print(f"  - {path.relative_to(ROOT)}", file=sys.stderr)
                return 1
            print(f"hypertoken check passed: {len(compiled)} generated files are current")
            return 0
        changed = [path for path, content in compiled.items() if write_if_changed(path, content)]
        print(f"hypertoken compile passed: {len(compiled)} outputs, {len(changed)} changed")
        for path in changed:
            print(f"  - {path.relative_to(ROOT)}")
        return 0
    except BuildError as exc:
        print(f"hypertoken compile failed: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
