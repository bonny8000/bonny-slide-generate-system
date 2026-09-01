#!/usr/bin/env python3
"""Scaffold an A/B round: two variants of one slide, plus a side-by-side image to judge them from.

The labelled A/B rounds are the scarcest input this system has. They are the only data that says
what a *person* prefers, and every attempt to measure taste from the slide itself has been scored
against them: nine geometric metrics found nothing, one static CSS feature found 74% on n=19. Both of
those conclusions rest on 37 pairs, which is too few to be sure of either. More rounds is the single
highest-value thing that can be added.

The cost of a round is not the building, it is the looking. So each round renders to **one image**
with both variants side by side and labelled, which is all that is needed to make a call.

A round is only worth running if both variants are defensible. A pair where one option is obviously
broken teaches nothing except that broken is worse; the useful rounds are the ones where a reasonable
designer could pick either, because that is where the system currently has no opinion.

Rounds are declared in `specs/ab-rounds.md` and generated from it, so the axis being tested is
recorded next to the result rather than living in a commit message.

Usage:
    python scripts/ab_round.py --list
    python scripts/ab_round.py 51 52 53      # build these rounds and render their comparisons
    python scripts/ab_round.py --all
"""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
AB = ROOT / "examples" / "case-study" / "_ab"
SPEC = ROOT / "specs" / "ab-rounds.md"

sys.path.insert(0, str(ROOT / "scripts"))
import sync_examples  # noqa: E402
from visual_baseline import find_browsers, render_with_any  # noqa: E402

COMPARE = """<!doctype html><html lang="zh-Hant"><head><meta charset="utf-8"><style>
html,body{{margin:0;width:1920px;height:660px;background:#ffffff;font-family:Arial,"Helvetica Neue",sans-serif}}
.hdr{{height:74px;padding:14px 26px 0;box-sizing:border-box}}
.hdr .q{{font-size:21px;font-weight:700;color:#1c2233;margin:0}}
.hdr .s{{font-size:15px;color:#6b7280;margin:4px 0 0}}
.row{{display:flex;gap:18px;padding:0 26px}}
.pane{{width:925px}}
.tag{{font-size:19px;font-weight:700;color:#1c2233;margin:0 0 6px}}
.box{{width:925px;height:521px;overflow:hidden;border:1px solid #d5d9e2;border-radius:8px}}
iframe{{width:1920px;height:1080px;border:0;transform:scale(.4818);transform-origin:top left}}
</style></head>
<div class="hdr"><p class="q">Round {n} — {axis}</p><p class="s">{question}</p></div>
<div class="row">
  <div class="pane"><p class="tag">A</p><div class="box"><iframe src="r{n}A.html" scrolling="no"></iframe></div></div>
  <div class="pane"><p class="tag">B</p><div class="box"><iframe src="r{n}B.html" scrolling="no"></iframe></div></div>
</div>
</html>
"""


def parse_spec() -> dict[int, dict]:
    """Rounds declared as `### R51 — axis` with a question line and two fenced css blocks."""
    if not SPEC.is_file():
        return {}
    text = SPEC.read_text(encoding="utf-8")
    rounds: dict[int, dict] = {}
    for block in re.split(r"\n(?=### R\d+)", text):
        head = re.match(r"### R(\d+)\s*[—-]\s*(.+)", block)
        if not head:
            continue
        n = int(head.group(1))
        base = re.search(r"^base:\s*(\S+)", block, re.M)
        question = re.search(r"^question:\s*(.+)$", block, re.M)
        css = re.findall(r"```css\n(.*?)```", block, re.S)
        if not (base and question and len(css) == 2):
            continue
        rounds[n] = {
            "axis": head.group(2).strip(),
            "base": base.group(1).strip(),
            "question": question.group(1).strip(),
            "winner": (re.search(r"^winner:[ \t]*([AB])?[ \t]*$", block, re.M).group(1) or "") if re.search(r"^winner:[ \t]*([AB])?[ \t]*$", block, re.M) else "",
            "a": css[0].strip(),
            "b": css[1].strip(),
        }
    return rounds


def build_variant(base_html: str, extra_css: str) -> str:
    """Append the variant's CSS to the slide's own block so it wins over the shipped sheet."""
    if "<style data-slide>" in base_html:
        return re.sub(
            r"(<style data-slide>)(.*?)(</style>)",
            lambda m: m.group(1) + m.group(2).rstrip() + "\n" + extra_css + "\n" + m.group(3),
            base_html, count=1, flags=re.S,
        )
    return base_html.replace(
        "</style>", "</style>\n<style data-slide>\n" + extra_css + "\n</style>", 1
    )


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("rounds", nargs="*", type=int)
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--out", type=Path, default=ROOT / "work" / "ab-review")
    args = ap.parse_args()

    spec = parse_spec()
    if args.list or not (args.rounds or args.all):
        for n, r in sorted(spec.items()):
            built = "judged " + r["winner"] if r["winner"] else "pending"
            print(f"  R{n}  {built}  {r['axis']}  (base: {r['base']})")
        return 0

    wanted = sorted(spec) if args.all else args.rounds
    args.out = args.out.resolve()
    args.out.mkdir(parents=True, exist_ok=True)
    variants = args.out / "variants"
    variants.mkdir(exist_ok=True)
    manifest_path = args.out / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8")) if manifest_path.exists() else {"rounds":{}}
    errors = 0
    browsers = find_browsers(None)

    for n in wanted:
        if n not in spec:
            print(f"R{n}: not declared in {SPEC.name}", file=sys.stderr)
            errors += 1
            continue
        r = spec[n]
        if r["winner"] or str(n) in manifest["rounds"]:
            print(f"R{n}: already judged or rendered; preserve the pair and create a new round/output directory", file=sys.stderr)
            errors += 1
            continue
        base_path = ROOT / "examples" / f"{r['base']}.html"
        if not base_path.is_file():
            print(f"R{n}: base not found: {base_path}", file=sys.stderr)
            errors += 1
            continue
        base_html = base_path.read_text(encoding="utf-8")

        # Preserve relative assets when moving a slide into the review folder.
        base_html = base_html.replace("<head>", '<head><base href="' + html.escape(base_path.parent.as_uri()+"/") + '">', 1)
        pair = {}
        for letter in ("a", "b"):
            out = variants / f"r{n}{letter.upper()}.html"
            out.write_text(build_variant(base_html, r[letter]), encoding="utf-8", newline="\n")
            # Bring the fresh variant in line with the shipped stylesheet immediately. Building
            # a round writes a file derived from the base, which leaves it out of sync until
            # someone remembers to run sync_examples.py - and rebuilding a round would silently
            # undo that sync again. Doing it here removes the ordering trap entirely.
            rebuilt = sync_examples.rebuild(out)
            if rebuilt is not None:
                out.write_text(rebuilt[0], encoding="utf-8", newline="\n")

            pair[letter.upper()] = {"path":out.relative_to(args.out).as_posix(), "sha256":hashlib.sha256(out.read_bytes()).hexdigest()}
        compare = variants / f"compare-r{n}.html"
        compare.write_text(
            COMPARE.format(n=n, axis=html.escape(r["axis"]), question=html.escape(r["question"])), encoding="utf-8", newline="\n"
        )
        png = args.out / f"round-{n}.png"
        png.write_bytes(render_with_any(compare, browsers, 1920, 660, 1.0))
        manifest["rounds"][str(n)] = {"base":r["base"], "baseSha256":hashlib.sha256(base_path.read_bytes()).hexdigest(), "variants":pair}
        manifest_path.write_text(json.dumps(manifest,indent=2)+"\n", encoding="utf-8", newline="\n")
        print(f"R{n}  {r['axis']}  ->  {png}", flush=True)

    print("\nJudge each image and record the winner in specs/ab-rounds.md, then re-run calibrate_gate.py --manifest <this output>/manifest.json.")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
