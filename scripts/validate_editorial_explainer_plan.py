#!/usr/bin/env python3
"""Fail closed when a deck silently skips a selected editorial explainer."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


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

    payload = json.loads(args.plan.read_text(encoding="utf-8"))
    slides = payload.get("slides")
    if not isinstance(slides, list) or not slides:
        fail("plan.slides must be a non-empty list")

    html = args.deck.read_text(encoding="utf-8")
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
        if f'id="{slide_id}"' not in html and f"id='{slide_id}'" not in html:
            fail(f"{slide_id} is not present in the deck HTML")
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
        if asset_value.replace("\\", "/") not in html.replace("\\", "/"):
            fail(f"{slide_id} asset is not placed in the deck HTML")
        marker = f'data-editorial-explainer="{variant}"'
        marker_single = f"data-editorial-explainer='{variant}'"
        if marker not in html and marker_single not in html:
            fail(f"{slide_id} lacks the matching HTML variant marker")

    print(f"PASS: {len(slides)} slide decisions; {required} generated editorial explainers verified")


if __name__ == "__main__":
    main()
