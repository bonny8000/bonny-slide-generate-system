#!/usr/bin/env python3
"""Make every example carry the SHIPPED stylesheet, not a copy of it.

Examples are reference material: the agent learns layout by imitating them. For most of this
system's life each example also carried its own hand-maintained snapshot of the stylesheet, and
those snapshots drifted — three separate times, over several versions: 30 examples never received
the v9.6 balance helpers, all of them hardcoded a page backdrop that predated the themed token, and
all of them sat on pre-v12.1 geometry. Stale examples do not merely look wrong; they teach rules the
specs had already superseded.

So an example no longer owns CSS. Each is rewritten as:

    <style data-shipped>   the theme tokens + generated bundle + base.css, regenerated from assets/
    <style data-slide>     only what is genuinely specific to this one slide
    markup                 untouched

`--check` fails when any example's shipped block differs from the current stylesheet, which makes
drift a build error rather than something to be discovered later by rendering everything.

Usage:
    python scripts/sync_examples.py            # rewrite every example's shipped block
    python scripts/sync_examples.py --check    # fail if any example is stale
    python scripts/sync_examples.py --report   # show what each example keeps as slide-specific

Exit codes: 0 = in sync (or written) · 1 = stale (--check) · 2 = cannot run.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXAMPLES = ROOT / "examples"
SHIPPED_OPEN = '<style data-shipped>'
SLIDE_OPEN = '<style data-slide>'
DARK_MARKERS = ("--canvas:#1B1B20", "--canvas: #1B1B20")


def shipped_css(dark: bool) -> str:
    """The stylesheet a fresh build would inline: one theme, the generated bundle, then base.css."""
    theme = "tokens-dark.css" if dark else "tokens-light.css"
    bundle = (ROOT / "assets" / "generated" / "base-bundle.css").read_text(encoding="utf-8")
    base = (ROOT / "assets" / "base.css").read_text(encoding="utf-8")
    base = re.sub(r"@import[^;]+;", "", base)  # the bundle is inlined above
    return (
        (ROOT / "assets" / theme).read_text(encoding="utf-8").rstrip()
        + "\n"
        + bundle.rstrip()
        + "\n"
        + base.strip()
        + "\n"
    )


def split_rules(css: str) -> list[tuple[str, str]]:
    """(selector, body) pairs, brace-aware so @media and @font-face survive intact.

    Braceless at-statements (`@layer a, b, c;`, `@charset`) are returned with a body of None.
    They must be split out rather than swept into the following selector: doing the latter made
    the sync non-idempotent, because a mangled selector never matched the shipped sheet and got
    re-copied into the slide block on every run.
    """
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    rules: list[tuple[str, str | None]] = []
    i = 0
    n = len(css)
    while i < n:
        brace = css.find("{", i)
        if brace < 0:
            for stmt in css[i:].split(";"):
                if stmt.strip():
                    rules.append((stmt.strip(), None))
            break
        head = css[i:brace]
        # anything before the last ';' in the head is a standalone statement, not a selector
        if ";" in head:
            *statements, selector = head.split(";")
            for stmt in statements:
                if stmt.strip():
                    rules.append((stmt.strip(), None))
        else:
            selector = head
        depth = 1
        j = brace + 1
        while j < n and depth:
            if css[j] == "{":
                depth += 1
            elif css[j] == "}":
                depth -= 1
            j += 1
        rules.append((selector.strip(), css[brace + 1 : j - 1].strip()))
        i = j
    return [(s, b) for s, b in rules if s]


NESTING_AT_RULES = ("@layer", "@media", "@supports", "@container")


def flatten_rules(css: str) -> list[tuple[str, str]]:
    """split_rules, but descending into @layer/@media/… — the generated tokens live inside
    `@layer tokens { :root { … } }`, so a non-recursive scan never sees a single token."""
    out: list[tuple[str, str]] = []
    for sel, body in split_rules(css):
        if body is not None and sel.startswith(NESTING_AT_RULES) and "{" in body:
            out.extend(flatten_rules(body))
        else:
            out.append((sel, body))
    return out


def normalise(body: str) -> str:
    return re.sub(r"\s+", " ", body).strip().rstrip(";")


def bare_index(shipped: str) -> dict[str, set[str]]:
    """bare single-class selectors in the shipped sheet -> their bodies."""
    out: dict[str, set[str]] = {}
    for sel, body in flatten_rules(shipped):
        if body is None:
            continue
        for part in (p.strip() for p in sel.split(",")):
            if re.fullmatch(r"\.[a-z][\w-]*", part):
                out.setdefault(part, set()).add(normalise(body))
    return out


def used_classes(markup: str) -> set[str]:
    """Every class name the slide's markup actually puts on an element."""
    out: set[str] = set()
    for m in re.finditer(r"""class\s*=\s*["']([^"']*)["']""", markup):
        out |= set(m.group(1).split())
    return out


def slide_specific(existing_css: str, shipped: str, used: set[str] | None = None) -> list[tuple[str, str]]:
    """Rules this slide genuinely adds: absent from the shipped sheet, or deliberately different.

    A :root block is dropped except for custom properties the shipped themes do not define —
    an example that invents its own variable still needs it.

    Rules for classes the markup never uses are dropped outright. Examples were built by inlining a
    snapshot of base.css, so each one carried the whole sheet; anything base.css has since improved
    survived here as a "deliberate difference" even when the slide has no such element. That is dead
    weight in a file whose only job is to be read as reference — 591 of 1523 rules, teaching values
    base.css no longer uses. A rule is kept when any of its classes is present, so a partial match
    like `.cmp .ctable th` stays rather than risking a real style.
    """
    ship = {}
    ship_statements = set()
    for sel, body in flatten_rules(shipped):
        if body is None:
            ship_statements.add(sel)
        else:
            ship.setdefault(sel, set()).add(normalise(body))
    ship_props = set()
    for sel, body in flatten_rules(shipped):
        if body is None:
            continue
        if sel.startswith(":root") or "data-theme" in sel:
            ship_props |= set(re.findall(r"(--[\w-]+)\s*:", body))

    keep: list[tuple[str, str]] = []
    for sel, body in flatten_rules(existing_css):
        if body is None:
            if sel not in ship_statements:
                keep.append((sel, None))
            continue
        if sel.startswith("@"):
            keep.append((sel, body))
            continue
        if sel.startswith(":root") or "data-theme" in sel:
            extras = [
                d.strip()
                for d in body.split(";")
                if d.strip()
                and d.strip().startswith("--")
                and d.split(":")[0].strip() not in ship_props
            ]
            if extras:
                keep.append((sel, "; ".join(extras) + ";"))
            continue
        if normalise(body) in ship.get(sel, set()):
            continue  # identical to the shipped rule: let the shipped sheet provide it
        if used is not None:
            classes = set(re.findall(r"\.([a-zA-Z][\w-]*)", sel))
            if classes and not (classes & used):
                continue  # no such element on this slide
        keep.append((sel, body))
    return keep


def declared_props(body: str) -> dict[str, str]:
    out: dict[str, str] = {}
    depth = 0
    buf = ""
    for ch in body:
        if ch in "([":
            depth += 1
        elif ch in ")]":
            depth -= 1
        if ch == ";" and depth == 0:
            if ":" in buf:
                k, v = buf.split(":", 1)
                out[k.strip()] = v.strip()
            buf = ""
        else:
            buf += ch
    if ":" in buf:
        k, v = buf.split(":", 1)
        out[k.strip()] = v.strip()
    return {k: v for k, v in out.items() if k}


def neutralise(selector: str, body: str, ship: dict[str, set[str]]) -> str:
    """Make a slide rule fully override the bare shipped rule it collides with.

    Both blocks are unlayered and the slide block comes second, so the slide rule already wins for
    every property it SETS. The danger is the properties it does not set: those keep leaking from
    the shipped rule. That is how feature-showcase's `.fs{align-items:start}` collapsed an unrelated
    A/B slide whose own `.fs` was a flex column, and how the v12 `.track` flattened a bar chart.
    So any property the shipped rule declares and this one does not is explicitly reverted.
    """
    shipped_bodies = ship.get(selector.strip())
    if not shipped_bodies:
        return body
    mine = declared_props(body)
    extra: dict[str, None] = {}
    for shipped in shipped_bodies:
        for prop in declared_props(shipped):
            if prop not in mine and not prop.startswith("--"):
                extra[prop] = None
    if not extra:
        return body
    resets = ";".join(f"{prop}:revert" for prop in extra)
    return (body.rstrip().rstrip(";") + ";" + resets) if body.strip() else resets


def render_block(rules: list[tuple[str, str]], ship: dict[str, set[str]] | None = None) -> str:
    ship = ship or {}
    out = []
    for sel, body in rules:
        if body is None:
            out.append(f"{sel};")
            continue
        b = normalise(neutralise(sel, body, ship))
        out.append(f"{sel}{{{b}}}" if b else f"{sel}{{}}")
    return "\n".join(out)


def rebuild(path: Path) -> tuple[str, int] | None:
    """Return (new_text, slide_rule_count) or None when the file has no style block."""
    text = path.read_text(encoding="utf-8")
    first = text.find("<style")
    last = text.rfind("</style>")
    if first < 0 or last < 0:
        return None
    head = text[:first]
    middle = text[first : last + len("</style>")]
    tail = text[last + len("</style>") :]

    existing = "\n".join(re.findall(r"<style[^>]*>(.*?)</style>", middle, re.S))
    dark = any(m in existing for m in DARK_MARKERS)
    ship = shipped_css(dark)
    keep = slide_specific(existing, ship, used_classes(tail))

    block = SHIPPED_OPEN + "\n" + ship.strip() + "\n</style>"
    if keep:
        block += "\n" + SLIDE_OPEN + "\n" + render_block(keep, bare_index(ship)) + "\n</style>"
    return head + block + tail, len(keep)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--check", action="store_true", help="fail if any example is stale")
    parser.add_argument("--report", action="store_true", help="list each example's slide-specific rules")
    parser.add_argument("paths", nargs="*", type=Path, help="limit to these files (default: all examples)")
    args = parser.parse_args()

    def resolve(a: Path) -> Path:
        return a if a.is_absolute() else (Path.cwd() / a).resolve()

    if args.paths:
        targets = []
        for a in (resolve(p) for p in args.paths):
            targets.extend([a] if a.is_file() else sorted(a.rglob("*.html")))
        targets = sorted(set(targets))
    else:
        targets = sorted(EXAMPLES.rglob("*.html"))
    if not targets:
        print("sync examples: no example files found", file=sys.stderr)
        return 2

    stale: list[str] = []
    written = 0
    total_slide_rules = 0
    for path in targets:
        built = rebuild(path)
        if built is None:
            continue
        new_text, slide_rules = built
        total_slide_rules += slide_rules
        try:
            rel = path.relative_to(ROOT).as_posix()
        except ValueError:
            rel = path.as_posix()
        if args.report:
            print(f"{slide_rules:3d} slide rules  {rel}")
            continue
        current = path.read_text(encoding="utf-8")
        if current == new_text:
            continue
        if args.check:
            stale.append(rel)
        else:
            path.write_text(new_text, encoding="utf-8", newline="\n")
            written += 1

    if args.report:
        print(f"\n{total_slide_rules} slide-specific rules across {len(targets)} examples")
        return 0
    if args.check:
        if stale:
            print(
                f"examples carry a stale stylesheet ({len(stale)} of {len(targets)}):",
                file=sys.stderr,
            )
            for rel in stale[:12]:
                print(f"  - {rel}", file=sys.stderr)
            if len(stale) > 12:
                print(f"  … and {len(stale) - 12} more", file=sys.stderr)
            print("run: python scripts/sync_examples.py", file=sys.stderr)
            return 1
        print(f"examples in sync: {len(targets)} carry the current stylesheet")
        return 0
    print(f"synced {written} of {len(targets)} examples ({total_slide_rules} slide-specific rules kept)")
    return 0


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except AttributeError:
        pass
    raise SystemExit(main())
