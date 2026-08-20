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
from collections import Counter
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



# --------------------------------------------------------------------------
# Intention router: compiles specs/**/*.md frontmatter into a machine-readable
# routing index so layout/component selection is a lookup, not prose matching.
# --------------------------------------------------------------------------

SPEC_DIRS = {"layout": ROOT / "specs" / "layouts", "component": ROOT / "specs" / "components"}
SPEC_ID_RE = re.compile(r"^[a-z][a-z0-9-]*$")
REQUIRED_SPEC_KEYS = ("id", "kind", "tier", "status", "intent", "triggers", "example")
QUOTES = "\"'"


def _strip_comment(value: str) -> str:
    """Drop a trailing ` # comment`, respecting quoted spans."""
    quote = None
    for i, ch in enumerate(value):
        if quote:
            if ch == quote:
                quote = None
        elif ch in QUOTES:
            quote = ch
        elif ch == "#" and i > 0 and value[i - 1].isspace():
            return value[:i]
    return value


def _split_flow(body: str) -> list[str]:
    """Split a YAML flow sequence body on top-level commas, respecting quotes."""
    items: list[str] = []
    buf: list[str] = []
    quote = None
    for ch in body:
        if quote:
            if ch == quote:
                quote = None
            else:
                buf.append(ch)
            continue
        if ch in QUOTES:
            quote = ch
            continue
        if ch == ",":
            items.append("".join(buf).strip())
            buf = []
            continue
        buf.append(ch)
    if quote:
        raise BuildError(f"unterminated quote in flow sequence: [{body}]")
    tail = "".join(buf).strip()
    if tail:
        items.append(tail)
    return [item for item in items if item]


def parse_frontmatter(text: str, where: str) -> dict[str, Any]:
    """Parse the small YAML subset used by spec frontmatter (stdlib only)."""
    match = re.match(r"^---\r?\n(.*?)\r?\n---", text, re.S)
    if not match:
        raise BuildError(f"{where}: missing YAML frontmatter block")
    data: dict[str, Any] = {}
    for raw in match.group(1).splitlines():
        line = raw.rstrip()
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        key_value = re.match(r"^([a-z_][a-z0-9_]*):\s*(.*)$", line, re.I)
        if not key_value:
            raise BuildError(f"{where}: cannot parse frontmatter line: {raw!r}")
        key = key_value.group(1)
        value = _strip_comment(key_value.group(2)).strip()
        if key in data:
            raise BuildError(f"{where}: duplicate frontmatter key {key!r}")
        if value.startswith("[") and value.endswith("]"):
            data[key] = _split_flow(value[1:-1])
        else:
            data[key] = value.strip(QUOTES)
    return data


def load_specs() -> dict[str, dict[str, Any]]:
    specs: dict[str, dict[str, Any]] = {}
    for kind, directory in SPEC_DIRS.items():
        if not directory.is_dir():
            raise BuildError(f"missing spec directory: {directory}")
        for path in sorted(directory.glob("*.md")):
            where = path.relative_to(ROOT).as_posix()
            data = parse_frontmatter(path.read_text(encoding="utf-8"), where)
            missing = [key for key in REQUIRED_SPEC_KEYS if not data.get(key)]
            if missing:
                raise BuildError(f"{where}: frontmatter missing required key(s): {', '.join(missing)}")
            spec_id = data["id"]
            if not SPEC_ID_RE.match(spec_id):
                raise BuildError(f"{where}: invalid id {spec_id!r}")
            if spec_id != path.stem:
                raise BuildError(f"{where}: id {spec_id!r} does not match filename {path.stem!r}")
            if data["kind"] != kind:
                raise BuildError(f"{where}: kind {data['kind']!r} but lives in {directory.name}/")
            if spec_id in specs:
                raise BuildError(f"duplicate spec id {spec_id!r}")
            triggers = data["triggers"]
            if not isinstance(triggers, list) or not triggers:
                raise BuildError(f"{where}: 'triggers' must be a non-empty list")
            example = str(data["example"]).strip()
            if not (ROOT / example).is_file():
                raise BuildError(f"{where}: example not found: {example}")
            learned = str(data.get("learned_from", ""))
            specs[spec_id] = {
                "kind": kind,
                "tier": data["tier"],
                "status": data["status"],
                "intent": data["intent"],
                "material": str(data.get("material", "")).strip(),
                "arrangement": str(data.get("arrangement", "")).strip(),
                "itemCount": str(data.get("item_count", "")).strip(),
                "triggers": triggers,
                "spec": where,
                "example": example,
                "dependsOn": data.get("depends_on", []) or [],
                "tokensUsed": data.get("tokens_used", []) or [],
                "iconUse": data.get("icon_use", "optional"),
                "learnedFrom": [part.strip() for part in learned.split(",") if part.strip()],
            }
    return specs


def load_catalog_ids() -> set[str]:
    """Ids catalogued in specs/_catalog.md, including entries that have no spec file yet."""
    text = (ROOT / "specs" / "_catalog.md").read_text(encoding="utf-8")
    ids: set[str] = set()
    for row in re.findall(r"^\|\s*([a-z][a-z0-9 /-]*?)\s*\|", text, re.M):
        for part in row.split("/"):
            part = part.strip()
            if part and part != "id":
                ids.add(part)
    return ids


CJK_RANGES = (("㐀", "鿿"), ("豈", "﫿"))
# Triggers used to reject Hangul. That rule was aimed at the right goal from the wrong layer: the
# constraint is that decks must be GENERATED in 繁中 + English, which validate_layout.py enforces at
# render time against the declared output language. A trigger is internal routing vocabulary and is
# never rendered, so banning a language here protected nothing — it only deleted recognition ability
# learned from the Korean reference decks this system was trained on. Intention does not change with
# the language it is written in, so triggers are deliberately multilingual now.


def _in_ranges(text: str, ranges: tuple[tuple[str, str], ...]) -> bool:
    return any(low <= ch <= high for ch in text for low, high in ranges)


HANGUL_RANGES = (("ᄀ", "ᇿ"), ("㄰", "㆏"), ("가", "힯"))


def _is_dense_script(text: str) -> bool:
    """Scripts where two characters already form a whole word, so the length floor can be lower.

    Han and Hangul both qualify — 연결 and 連結 carry as much signal as a five-letter English word,
    whereas a two-letter ASCII trigger is noise.
    """
    return _in_ranges(text, CJK_RANGES) or _in_ranges(text, HANGUL_RANGES)


def validate_router(specs: dict[str, dict[str, Any]]) -> None:
    """Fail the build on routing drift — the check that keeps the library reachable."""
    errors: list[str] = []
    catalog_ids = load_catalog_ids()
    known = set(specs) | catalog_ids | {"tokens"}

    for spec_id, spec in specs.items():
        for dep in spec["dependsOn"]:
            if dep not in known:
                errors.append(
                    f"{spec['spec']}: depends_on {dep!r}, which is neither a spec nor a catalog entry"
                )

    content_map = (ROOT / "specs" / "content-map.md").read_text(encoding="utf-8").lower()

    unrouted = sorted(
        spec_id
        for spec_id, spec in specs.items()
        if spec["kind"] == "layout"
        and spec["status"].startswith("stable")
        and spec_id not in content_map
    )
    if unrouted:
        errors.append(
            "layouts have a spec but no row in specs/content-map.md (unreachable by the planner): "
            + ", ".join(unrouted)
        )

    for spec_id, spec in specs.items():
        if spec["kind"] != "component":
            continue
        used_by_layout = any(
            spec_id in other["dependsOn"]
            for other in specs.values()
            if other["kind"] == "layout"
        )
        if not used_by_layout and spec_id not in content_map:
            errors.append(
                f"component {spec_id!r} is used by no layout and named in no content-map row (orphan)"
            )

    # Shape is the axis that actually decides between conceptual twins, so a layout without it is
    # only half-routable. Collisions are allowed but named: two layouts may legitimately share a
    # shape when their intent differs (keyword-cards vs terminology-cards are both 3-4 text cards).
    shapes: dict[tuple[str, str, str], list[str]] = {}
    for spec_id in sorted(specs):
        spec = specs[spec_id]
        if spec["kind"] != "layout":
            continue
        triple = (spec["material"], spec["arrangement"], spec["itemCount"])
        missing = [
            name
            for name, value in zip(("material", "arrangement", "item_count"), triple)
            if not value
        ]
        if missing:
            errors.append(
                f"{spec['spec']}: layout is missing {', '.join(missing)} — without a shape it can only "
                "be reached by intent, which alone identifies 13 of 25 layouts"
            )
        else:
            shapes.setdefault(triple, []).append(spec_id)

    seen: dict[str, str] = {}
    for spec_id in sorted(specs):
        for trigger in specs[spec_id]["triggers"]:
            key = trigger.strip().lower()
            # a 2-character Han/Hangul term is fully distinctive; ASCII needs more signal
            floor = 2 if _is_dense_script(key) else 3
            if len(key) < floor:
                errors.append(f"{specs[spec_id]['spec']}: trigger {trigger!r} is too short to route on")
            if key in seen and seen[key] != spec_id:
                errors.append(
                    f"trigger {trigger!r} is claimed by both {seen[key]!r} and {spec_id!r} — make it specific"
                )
            seen.setdefault(key, spec_id)

    if errors:
        raise BuildError("router drift detected:\n  - " + "\n  - ".join(errors))


def render_router_json(specs: dict[str, dict[str, Any]]) -> str:
    trigger_index: dict[str, list[str]] = {}
    for spec_id, spec in specs.items():
        for trigger in spec["triggers"]:
            trigger_index.setdefault(trigger.strip().lower(), []).append(spec_id)
    payload = {
        "$comment": "AUTO-GENERATED by scripts/compile_system.py from specs/**/*.md frontmatter. DO NOT EDIT.",
        "version": "1.0.0",
        "selectionPolicy": {
            "primaryKey": "shape",
            "note": (
                "Two axes. `intent` is what the page must DO; `material`/`arrangement`/`itemCount` "
                "is what the slide actually holds. Measured on this library, intent alone identifies "
                "13 of 25 layouts and the shape triple alone identifies 24 of 25, so shape decides "
                "and intent breaks the remaining tie. Triggers are multilingual surface forms for "
                "recognising either axis. Layouts are the unit of selection; components resolve via "
                "dependsOn."
            ),
            "tieBreak": [
                "1. availability - drop any candidate whose assetPolicy is 'must-supply' when the "
                "user has not supplied that asset. A ui-screen cannot be invented.",
                "2. fit - prefer the candidate whose itemCount matches how many items you actually "
                "have. Three items in a 'many' layout starves the slide; seven in a 'pair' overflows "
                "it. This is the same failure validate_layout.py measures after the fact.",
                "3. variety - only among candidates that survived 1 and 2, prefer one not already "
                "used in this deck. Variety never outranks fit: a repeated layout that fits beats a "
                "fresh one that starves.",
                "4. intent proximity - closest intent line wins.",
            ],
        },
        "counts": {
            "layouts": sum(1 for spec in specs.values() if spec["kind"] == "layout"),
            "components": sum(1 for spec in specs.values() if spec["kind"] == "component"),
        },
        "triggerIndex": {key: sorted(value) for key, value in sorted(trigger_index.items())},
        "entries": {key: specs[key] for key in sorted(specs)},
    }
    return json.dumps(payload, indent=2, ensure_ascii=False) + "\n"


def annotate_assets_and_alternates(specs: dict[str, dict[str, Any]]) -> None:
    """Give every layout its asset requirement and its same-shape fallbacks.

    `alternates` is layouts sharing the same `arrangement` — they lay the page out the same way and
    differ in the material they need. That is precisely the set to fall back to when the material is
    unavailable: no screenshots turns `as-is-to-be` into `problem-solution`, both `opposed`; no
    illustrations turns `use-case-cards` into `feature-grid` or `keyword-cards`, all `grid`.
    """
    by_arrangement: dict[str, list[str]] = {}
    for spec_id, spec in specs.items():
        if spec["kind"] == "layout" and spec.get("arrangement"):
            by_arrangement.setdefault(spec["arrangement"], []).append(spec_id)
    for spec_id, spec in specs.items():
        if spec["kind"] != "layout":
            continue
        need, policy = asset_need(spec.get("material", ""))
        spec["assetNeed"] = need
        spec["assetPolicy"] = policy
        spec["alternates"] = sorted(
            other for other in by_arrangement.get(spec.get("arrangement", ""), []) if other != spec_id
        )


def asset_need(material: str) -> tuple[str, str]:
    """What visual asset this layout's material implies, and whether it may be generated.

    The distinction matters more than the detection. An `illustration` the user did not supply can be
    generated — that is what the illustration route is for. A `ui-screen` never can: fabricating a
    product UI is exactly the thing `generated-editorial-explainer.md` forbids, because a made-up
    screenshot of a real product is a false record of that product. So a layout needing a screen the
    user does not have is not an illustration job; it is a re-route, or a question for the user.
    """
    parts = {part.strip() for part in material.split("+") if part.strip()}
    wants_art = "illustration" in parts
    wants_screen = "ui-screen" in parts
    if wants_art and wants_screen:
        return "illustration+ui-screen", "generate-art-supply-screen"
    if wants_screen:
        return "ui-screen", "must-supply"
    if wants_art:
        return "illustration", "generate"
    return "none", "none"


def render_router_md(specs: dict[str, dict[str, Any]]) -> str:
    lines = [
        "<!-- AUTO-GENERATED by scripts/compile_system.py. DO NOT EDIT. -->",
        "# Intention router — every routable pattern in the library",
        "",
        "Compiled from each spec's `intent` + `triggers` frontmatter, so it can never drift from the specs.",
        "`content-map.md` stays the hand-written narrative router (detection heuristics + component",
        "pairings); **this file is the complete index** — if a pattern is not here, it does not exist.",
        "",
        "Read `intent` first (what the page must DO), then confirm with `triggers` (what the content looks",
        "like). Machine-readable form: `system/router.json`.",
        "",
    ]
    sections = (
        ("layout", "Layouts — the unit of selection"),
        ("component", "Components — resolved via a layout's `depends_on`"),
    )
    for kind, heading in sections:
        lines += [
            "## " + heading,
            "",
            "| id | intent (the job) | shape — material / arrangement / count | triggers | spec |",
            "|---|---|---|---|---|",
        ]
        for spec_id in sorted(key for key, value in specs.items() if value["kind"] == kind):
            spec = specs[spec_id]
            triggers = " · ".join(spec["triggers"])
            shape = " / ".join(
                part for part in (spec.get("material"), spec.get("arrangement"), spec.get("itemCount")) if part
            ) or "—"
            lines.append(
                f"| `{spec_id}` | {spec['intent']} | {shape} | {triggers} | `{spec['spec']}` |"
            )
        lines.append("")
    return "\n".join(lines)



# --------------------------------------------------------------------------
# Class-usage manifest: each spec declares the CSS classes it legitimately
# uses. base.css stays hand-written -- this is a usage contract, not codegen.
# It answers "which classes do I build this component with" and makes both
# implementation gaps and invented one-off classes visible.
# --------------------------------------------------------------------------

# Chrome every slide carries regardless of which component it demonstrates.
CHROME_CLASSES = frozenset(
    """slide deck poster top cover statement section-cover head center headline sub kicker
    eyebrow foot pageno cjk latin accent grid12 grow vspread nav item on""".split()
)
COL_RE = re.compile(r"^col-\d+$")
CLASS_ATTR_RE = re.compile(r'class="([^"]*)"')
CSS_CLASS_RE = re.compile(r"\.([a-zA-Z][\w-]*)")


def shipped_classes() -> set[str]:
    """Every class the shipped stylesheet actually defines."""
    text = ""
    for name in ("base.css", "generated/base-bundle.css"):
        path = ROOT / "assets" / name
        if path.is_file():
            text += path.read_text(encoding="utf-8") + "\n"
    text = re.sub(r"/\*.*?\*/", "", text, flags=re.S)
    return {m.group(1) for m in CSS_CLASS_RE.finditer(text)}


def example_classes(example: str) -> set[str]:
    """Substantive component classes used by an example's markup."""
    path = ROOT / example
    if not path.is_file():
        return set()
    html = path.read_text(encoding="utf-8", errors="replace")
    # Markup is whatever follows the LAST </style>. Splitting on "<body" was wrong: 136 of the
    # 164 examples omit the tag entirely (HTML makes it optional), so that fell back to the whole
    # file and scanned CSS selector names as if they were classes used in markup.
    if "</style>" in html:
        body = html.rsplit("</style>", 1)[-1]
    elif "<body" in html:
        body = html.split("<body", 1)[-1]
    else:
        body = html
    used: set[str] = set()
    for match in CLASS_ATTR_RE.finditer(body):
        used |= set(match.group(1).split())
    return {
        name
        for name in used - CHROME_CLASSES
        # one- and two-letter names are per-example shorthand, not shared vocabulary
        if len(name) > 2 and not COL_RE.match(name)
    }


def build_class_manifest(specs: dict[str, dict[str, Any]]) -> dict[str, Any]:
    shipped = shipped_classes()
    entries: dict[str, Any] = {}
    for spec_id in sorted(specs):
        declared = sorted(example_classes(specs[spec_id]["example"]))
        implemented = [c for c in declared if c in shipped]
        missing = [c for c in declared if c not in shipped]
        entries[spec_id] = {
            "kind": specs[spec_id]["kind"],
            "example": specs[spec_id]["example"],
            "classes": declared,
            "implementedInBaseCss": implemented,
            "missingFromBaseCss": missing,
        }
    covered = sum(1 for e in entries.values() if not e["missingFromBaseCss"])
    return {
        "$comment": (
            "AUTO-GENERATED by scripts/compile_system.py. A usage contract, not codegen: "
            "assets/base.css stays hand-written. 'missingFromBaseCss' is the implementation "
            "backlog -- a catalogued pattern whose CSS lives only inside its example cannot be "
            "rebuilt from assets/base.css, so the agent has to reinvent it every time."
        ),
        "version": "1.0.0",
        "policy": {
            "baseCssIsHandWritten": True,
            "note": "Declared classes come from each spec's example markup, which is the only "
            "record of how the pattern is actually built.",
        },
        "coverage": {
            "specs": len(entries),
            "fullyImplemented": covered,
            "withGaps": len(entries) - covered,
        },
        "entries": entries,
    }


def render_class_coverage(manifest: dict[str, Any]) -> str:
    cov = manifest["coverage"]
    gaps: dict[str, list[str]] = {}
    for spec_id, entry in manifest["entries"].items():
        if entry["missingFromBaseCss"]:
            gaps[spec_id] = entry["missingFromBaseCss"]
    # Count by distinct EXAMPLE FILE, not by spec: 44 specs share 30 example files, so counting
    # specs makes one definition look like three independent inventions of the same class.
    per_example: dict[str, set[str]] = {}
    for spec_id, entry in manifest["entries"].items():
        if entry["missingFromBaseCss"]:
            per_example.setdefault(entry["example"], set()).update(entry["missingFromBaseCss"])
    shared: Counter[str] = Counter()
    for classes in per_example.values():
        shared.update(classes)

    lines = [
        "<!-- AUTO-GENERATED by scripts/compile_system.py. DO NOT EDIT. -->",
        "# Class coverage — can each catalogued pattern be built from `assets/base.css`?",
        "",
        f"**{cov['fullyImplemented']} of {cov['specs']} patterns** have every class name they use defined",
        f"in the shipped stylesheet. **{cov['withGaps']}** still reference a class that exists only inside",
        "their own example.",
        "",
        "> **This counts names, not behaviour.** A pattern can have every class name present and still",
        "> fail to reproduce, because a descendant rule, a pseudo-element, or an `nth-child` rule never",
        "> came across. Do not read this number as \"buildable\". The honest check renders the pattern",
        "> using only the shipped stylesheet and compares it against the example:",
        "> `python scripts/verify_rebuild.py`.",
        "",
        "This matters because the agent builds with `assets/base.css`. When a catalogued pattern's CSS",
        "lives only in its example, the agent cannot reuse it — it has to reinvent the component, which",
        "is how visual consistency drifts even when intention routing is correct.",
        "",
        "Machine-readable form: `system/class-manifest.json`.",
        "",
        "## Patterns that need classes `base.css` does not define",
        "",
        "| pattern | kind | missing classes |",
        "|---|---|---|",
    ]
    for spec_id in sorted(gaps):
        entry = manifest["entries"][spec_id]
        names = ", ".join(f"`.{c}`" for c in gaps[spec_id])
        lines.append(f"| `{spec_id}` | {entry['kind']} | {names} |")
    lines += [
        "",
        "## Missing classes appearing in more than one example",
        "",
        "Counted by distinct **example file**, because 44 specs share 30 examples — counting specs",
        "would make one definition look like several independent inventions. Almost every missing",
        "class belongs to exactly one pattern, so the fix is to promote each pattern's own CSS into",
        "`base.css`, not to extract a shared layer that does not exist. A class that does appear in",
        "several examples needs checking for a **name collision** before promotion: `.anno` currently",
        "means two different things in two different examples.",
        "",
        "| class | example files needing it |",
        "|---|---:|",
    ]
    for name, count in shared.most_common():
        if count > 1:
            lines.append(f"| `.{name}` | {count} |")
    lines.append("")
    return "\n".join(lines)


def validate_class_manifest(manifest: dict[str, Any]) -> None:
    """Block invented vocabulary; record existing gaps rather than failing on them.

    Failing on the current gaps would break the build on day one and teach everyone to pass
    --check with their eyes shut. The gaps are reported in specs/generated-class-coverage.md
    and worked down deliberately; what fails here is a spec with no recorded build at all.
    """
    errors = []
    for spec_id, entry in manifest["entries"].items():
        if not entry["classes"]:
            errors.append(
                f"{spec_id}: its example declares no component classes, so the manifest cannot "
                "record how this pattern is built"
            )
    if errors:
        raise BuildError("class manifest invalid:\n  - " + "\n  - ".join(errors))

def outputs() -> dict[Path, str]:
    token_data = load_json(SYSTEM / "tokens.json")
    hypertoken_data = load_json(SYSTEM / "hypertokens.json")
    recipe_data = load_json(SYSTEM / "recipes.json")
    foundations, themes = validate_tokens(token_data)
    hypertokens = validate_hypertokens(hypertoken_data, foundations, themes)
    recipes = validate_recipes(recipe_data, hypertokens)
    specs = load_specs()
    annotate_assets_and_alternates(specs)
    validate_router(specs)
    class_manifest = build_class_manifest(specs)
    validate_class_manifest(class_manifest)
    foundations_css = render_foundations_css(foundations)
    hypertokens_css = render_hypertokens_css(hypertokens)
    result = {
        SYSTEM / "router.json": render_router_json(specs),
        SYSTEM / "class-manifest.json": json.dumps(class_manifest, indent=2, ensure_ascii=False)
        + "\n",
        ROOT / "specs" / "generated-class-coverage.md": render_class_coverage(class_manifest),
        ROOT / "specs" / "generated-router.md": render_router_md(specs),
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
