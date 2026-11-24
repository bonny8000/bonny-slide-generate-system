#!/usr/bin/env python3
"""Bring the zh-TW writing rules into ``specs/writing/`` from a checkout of the writing skill.

The slide system carries its own copy of the writing rules so a build never depends on a second
skill being installed. The rules are still trained in the standalone ``zh-tw-writing`` skill; this
script is the one-way door between the two.

What it does:

* copies each dimension file (intent, wording, sentences, ...) into ``specs/writing/`` with slide
  system frontmatter, rewriting the few links that point at files the slide system does not carry;
* refreshes the two marked blocks in ``specs/writing/slide-copy.md`` that hold the selection
  preferences for slide copy and on-screen interface copy.

Everything else in ``slide-copy.md`` and ``specs/writing/README.md`` is written for slides and is
never touched.

This is not part of ``check_system.py``: CI cannot see the writing skill. Run it by hand after the
writing skill changes.

Usage:
    python scripts/sync_writing.py --from ~/.codex/skills/zh-tw-writing
    python scripts/sync_writing.py --from ~/.codex/skills/zh-tw-writing --check
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEST = ROOT / "specs" / "writing"

FILES = (
    "intent.md",
    "wording.md",
    "sentences.md",
    "titles-and-body.md",
    "translation.md",
    "taiwan-usage.md",
    "ui-components.md",
    "drafting-habits.md",
    "revision-pairs.md",
    "revision-practice-2.md",
    "revision-practice-3.md",
)

# Links into the per-channel checklist are redirected to the slide-surface guide.
LINKS = (
    ("[formats.md](formats.md#介面文案)", "[slide-copy.md](slide-copy.md#畫面上的介面文案)"),
    ("](formats.md#介面文案)", "](slide-copy.md#畫面上的介面文案)"),
    ("](formats.md#簡報)", "](slide-copy.md)"),
    ("](formats.md)", "](slide-copy.md)"),
)

# heading in the skill's formats.md -> marker name in slide-copy.md
BLOCKS = (("簡報", "slide-preferences"), ("介面文案", "interface-preferences"))


def read(path: Path) -> str:
    return path.read_bytes().decode("utf-8-sig").replace("\r\n", "\n")


def vendored(name: str, source: str) -> str:
    for old, new in LINKS:
        source = source.replace(old, new)
    front = f"---\nid: writing-{Path(name).stem}\nkind: writing\nstatus: stable\n---\n"
    return front + source.lstrip("\n")


def section_bullets(formats: str, heading: str) -> str:
    match = re.search(rf"^## {re.escape(heading)}\n(.*?)(?=^## |\Z)", formats, re.S | re.M)
    if not match:
        raise SystemExit(f"formats.md has no '## {heading}' section")
    lines = match.group(1).split("\n")
    start = next((i for i, line in enumerate(lines) if line.startswith("- ")), None)
    if start is None:
        raise SystemExit(f"formats.md section '{heading}' has no bullets")
    body = "\n".join(lines[start:]).rstrip("\n")
    for old, new in LINKS:
        body = body.replace(old, new)
    return body


def fill_blocks(slide_copy: str, formats: str) -> str:
    for heading, marker in BLOCKS:
        pattern = re.compile(
            rf"(<!-- sync:{marker} start -->\n)(.*?)(<!-- sync:{marker} end -->)", re.S
        )
        if not pattern.search(slide_copy):
            raise SystemExit(f"slide-copy.md is missing the sync:{marker} markers")
        bullets = section_bullets(formats, heading) + "\n"
        slide_copy = pattern.sub(lambda m: m.group(1) + bullets + m.group(3), slide_copy)
    return slide_copy


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--from", dest="source", required=True, help="path to the zh-tw-writing skill folder")
    parser.add_argument("--check", action="store_true", help="report drift and exit 1; write nothing")
    args = parser.parse_args()

    refs = Path(args.source).expanduser() / "references"
    if not refs.is_dir():
        print(f"no references/ folder under {args.source}", file=sys.stderr)
        return 2

    wanted: dict[Path, str] = {}
    for name in FILES:
        wanted[DEST / name] = vendored(name, read(refs / name))
    slide_copy = DEST / "slide-copy.md"
    if slide_copy.exists():
        wanted[slide_copy] = fill_blocks(read(slide_copy), read(refs / "formats.md"))

    drift = [path for path, text in wanted.items() if not path.exists() or read(path) != text]
    if args.check:
        for path in drift:
            print(f"out of date: {path.relative_to(ROOT).as_posix()}")
        print("writing rules match the skill" if not drift else f"{len(drift)} file(s) differ")
        return 1 if drift else 0

    DEST.mkdir(parents=True, exist_ok=True)
    for path in drift:
        path.write_bytes(wanted[path].encode("utf-8"))
        print(f"wrote {path.relative_to(ROOT).as_posix()}")
    if not drift:
        print("already up to date")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
