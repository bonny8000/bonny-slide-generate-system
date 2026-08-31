#!/usr/bin/env python3
"""Fail closed when a deck silently skips a selected editorial explainer."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from slide_html import slides as html_slides, local_asset


VALID_VARIANTS = {"agenda-dialogue", "guided-dialogue", "workflow-transform", "ui-qa"}
VALID_OVERRIDES = {"precise-table", "data", "code", "evidence", "real-ui-detail"}


def fail(message: str) -> None:
    print(f"FAIL: {message}", file=sys.stderr)
    raise SystemExit(1)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("plan", type=Path)
    parser.add_argument("deck", type=Path)
    args = parser.parse_args()

    if not args.plan.is_file():
        fail(f"missing illustration plan: {args.plan}")
    if not args.deck.is_file():
        fail(f"missing deck: {args.deck}")

    try:
        payload = json.loads(args.plan.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        fail(f"cannot read illustration plan: {exc}")
    if not isinstance(payload, dict):
        fail("plan must be an object")
    slides = payload.get("slides")
    if not isinstance(slides, list) or not slides:
        fail("plan.slides must be a non-empty list")

    html = args.deck.read_text(encoding="utf-8")
    rendered = html_slides(html)
    if not rendered:
        fail("deck has no .slide elements")
    by_id = {}
    for node in rendered:
        slide_id = node.attrs.get("id", "").strip()
        if not slide_id or any(c.isspace() for c in slide_id):
            fail("every .slide element needs a non-empty, whitespace-free id")
        if slide_id in by_id:
            fail(f"duplicate HTML slide id: {slide_id}")
        if any("slide" in child.classes for child in list(node.walk())[1:]):
            fail(f"nested .slide element inside {slide_id}")
        by_id[slide_id] = node
    seen: set[str] = set()
    required = 0

    for index, slide in enumerate(slides, start=1):
        if not isinstance(slide, dict):
            fail(f"slides[{index}] must be an object")
        slide_id = str(slide.get("id", "")).strip()
        gate = slide.get("gate")
        trigger = str(slide.get("trigger", "")).strip()
        hard_candidate = slide.get("hard_candidate")
        reason = str(slide.get("reason", "")).strip()
        if not slide_id or slide_id in seen:
            fail(f"slides[{index}] has a missing or duplicate id")
        seen.add(slide_id)
        if slide_id not in by_id:
            fail(f"{slide_id} is not an actual .slide in the deck HTML")
        elements = list(by_id[slide_id].walk(visible=True))
        if gate not in {"yes", "no"}:
            fail(f"{slide_id} gate must be yes or no")
        if not trigger:
            fail(f"{slide_id} needs an illustration trigger")
        if not isinstance(hard_candidate, bool):
            fail(f"{slide_id} hard_candidate must be true or false")
        if not reason:
            fail(f"{slide_id} needs a gate reason")
        if gate == "no":
            override = slide.get("override")
            if hard_candidate and override not in VALID_OVERRIDES:
                fail(
                    f"{slide_id} is a hard candidate with gate no; override must be one of: "
                    + ", ".join(sorted(VALID_OVERRIDES))
                )
            continue

        required += 1
        variant = slide.get("variant")
        if variant not in VALID_VARIANTS:
            fail(f"{slide_id} has invalid variant: {variant}")
        if slide.get("generator") != "built-in-imagegen":
            fail(f"{slide_id} must record generator: built-in-imagegen")
        asset_value = str(slide.get("asset", "")).strip()
        if not asset_value:
            fail(f"{slide_id} is missing an asset path")
        asset = (args.plan.parent / asset_value).resolve()
        if not asset.is_file():
            fail(f"{slide_id} asset does not exist: {asset}")
        refs = slide.get("references")
        if not isinstance(refs, list) or not refs:
            fail(f"{slide_id} must record matching style references")
        stages = [node for node in elements if node.attrs.get("data-editorial-explainer") == variant]
        if not stages:
            fail(f"{slide_id} lacks the matching visible HTML variant marker")
        if not any(local_asset(url, args.deck) == asset
                   for stage in stages for node in stage.walk(visible=True)
                   for url in node.asset_urls()):
            fail(f"{slide_id} asset is not placed inside its matching variant stage")

    missing = sorted(set(by_id) - seen)
    if missing:
        fail("slides missing illustration decisions: " + ", ".join(missing))

    print(f"PASS: {len(slides)} slide decisions; {required} generated asset records checked (provenance is declared, not independently attested)")


if __name__ == "__main__":
    main()
