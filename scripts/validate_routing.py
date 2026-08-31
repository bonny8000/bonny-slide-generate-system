#!/usr/bin/env python3
"""Replay requests through the lexical shape/intent router.

A diagnostic for the routing table, not a prediction or lower bound on AI performance.
A declared shape must match a default or explicit variant; equal scores are AMBIG.
The original held-out cases have now been inspected and repaired, so both fixtures are
regression tests. Their pass rate is not independent evidence of generalization.

Usage: python scripts/validate_routing.py [--cases specs/routing-cases-heldout.md] [--verbose]
Exit: 0 all expected layouts; 1 wrong/unmatched/ambiguous; 2 cannot run.
"""

from __future__ import annotations

import argparse
import json
import math
import re
import sys
from pathlib import Path
from example_files import collect
from slide_html import document

ROOT = Path(__file__).resolve().parent.parent
ROUTER = ROOT / "system" / "router.json"
CASES = ROOT / "specs" / "routing-cases.md"

CJK = r"㐀-䶿一-鿿"
# Function words carry no routing signal and would otherwise let any two Chinese sentences overlap.
STOP_BIGRAMS = {"我們", "這個", "怎麼", "可以", "他們", "還有", "一個", "幾個", "把它", "們的", "我的", "你的", "他的", "它的", "什麼", "哪些"}
STOP_WORDS = {"the", "and", "with", "for", "each", "that", "this", "into", "から", "their", "them"}


def tokens(text: str) -> set[str]:
    """CJK bigrams + latin word stems. Chinese has no spaces, so bigrams stand in for words."""
    text = text.lower()
    out: set[str] = set()
    for run in re.findall(f"[{CJK}]+", text):
        for i in range(len(run) - 1):
            bg = run[i : i + 2]
            if bg not in STOP_BIGRAMS:
                out.add(bg)
        if len(run) == 1:
            out.add(run)
    for word in re.findall(r"[a-z]{3,}", text):
        if word not in STOP_WORDS:
            out.add(word[:6])  # crude stem: plan/plans/planning collapse
    return out


def corpus_idf() -> dict[str, float]:
    """IDF from visible copy in current examples; frozen A/B duplicates do not bias weights."""
    docs: list[set[str]] = []
    for path in collect([ROOT / "examples"]):
        text = path.read_text(encoding="utf-8", errors="replace")
        body = document(text).text()
        docs.append(tokens(body))
    n = len(docs) or 1
    df: dict[str, int] = {}
    for doc in docs:
        for tok in doc:
            df[tok] = df.get(tok, 0) + 1
    return {tok: math.log((n + 1) / (count + 1)) for tok, count in df.items()}


UNSEEN_IDF = 5.0  # a token absent from the corpus is maximally distinctive


def load_router() -> dict[str, dict]:
    data = json.loads(ROUTER.read_text(encoding="utf-8"))
    return {k: v for k, v in data["entries"].items() if v.get("kind") == "layout"}


def load_cases(path: Path) -> list[tuple[str, str, str]]:
    """Rows are `request | expect` or `request | shape | expect`.

    The three-column form is the normalised mode: `shape` is what the agent would declare after
    reading the request — material/arrangement/count — instead of leaving the table to guess it from
    however the user happened to phrase things.
    """
    cases: list[tuple[str, str, str]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line.startswith("|") or line.startswith("| ---"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if cells and cells[0] in ("request",):
            continue
        if len(cells) == 2:
            cases.append((cells[0], "", cells[1]))
        elif len(cells) == 3:
            cases.append((cells[0], cells[1], cells[2]))
    return cases


def by_shape(shape: str, entries: dict[str, dict]) -> list[str]:
    """Layouts whose declared shape matches, as an exact tag match rather than a text similarity.

    This is the whole point of normalising: `chart / split / one` either matches or it does not.
    Prose shape was tried first and made things worse — 13/25 down to 11/25 — because every shape
    sentence shares filler vocabulary ("one X and its Y"), so fuzzy matching drowned in it.
    """
    want = tuple(part.strip() for part in shape.split("/"))
    if len(want) != 3:
        return []
    return [
        k
        for k, e in entries.items()
        if any((v.get("material"), v.get("arrangement"), v.get("itemCount")) == want
               for v in [e, *e.get("shapeVariants", [])])
    ]


def resolve(request: str, shape: str, entries: dict[str, dict], idf: dict[str, float]) -> dict:
    """A declared shape is a constraint. Never discard it or break a tie alphabetically."""
    keys = by_shape(shape, entries) if shape else list(entries)
    if not keys:
        return dict(status="MISS", top=None, score=0, candidates=[], runner="-")
    ranked = sorted(((score(request, entries[k], idf), k) for k in keys), reverse=True)
    top_score, top = ranked[0]
    if shape and len(keys) == 1:
        top_score = max(top_score, 1.0)
    tied = [k for value, k in ranked if math.isclose(value, top_score, abs_tol=1e-9)]
    status = "resolved"
    if top_score <= 0:
        status = "AMBIG" if shape else "MISS"
    elif len(tied) > 1:
        status = "AMBIG"
    return dict(status=status, top=top if status == "resolved" else None,
                score=top_score, candidates=tied or keys, runner=ranked[1][1] if len(ranked)>1 else "-")


def score(query: str, entry: dict, idf: dict[str, float]) -> float:
    """How strongly this entry answers the query, weighting each match by how distinctive it is.

    A trigger appearing verbatim in the request is decisive — that is what triggers are for. Failing
    that, matched tokens are summed by IDF rather than counted, so overlapping on 使用者 earns almost
    nothing while overlapping on 人物誌 nearly settles it.
    """
    q = tokens(query)
    if not q:
        return 0.0

    def weight(toks: set[str]) -> float:
        return sum(idf.get(t, UNSEEN_IDF) for t in toks)

    best = 0.0
    for trig in entry.get("triggers", []):
        norm = trig.lower().strip()
        if len(norm) >= 4 and norm in query.lower():
            return 10.0
        tt = tokens(trig)
        shared = q & tt
        if shared:
            best = max(best, 2.0 * weight(shared) / max(weight(tt), 1e-9))
    it = tokens(entry.get("intent", ""))
    shared = q & it
    if shared:
        best = max(best, 1.0 * weight(shared) / max(weight(q), 1e-9))
    return best


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--verbose", action="store_true", help="show runner-up and scores")
    ap.add_argument("--cases", type=Path, default=CASES, help="alternate regression fixture")
    args = ap.parse_args()

    if not ROUTER.exists() or not args.cases.exists():
        print("router.json or routing-cases.md missing — run compile_system.py first", file=sys.stderr)
        return 2

    entries = load_router()
    idf = corpus_idf()
    cases = load_cases(args.cases)
    if not cases:
        print(f"no cases parsed from {args.cases}", file=sys.stderr)
        return 2

    hits = wrong = miss = ambig = 0
    rows: list[tuple[str, str, str, str, float]] = []
    for request, shape, expected in cases:
        result = resolve(request, shape, entries, idf)
        top_score, top, runner = result["score"], result["top"], result["runner"]
        if result["status"] == "AMBIG":
            verdict, ambig = "AMBIG", ambig + 1
        elif result["status"] == "MISS":
            verdict, miss = "MISS ", miss + 1
        elif top == expected:
            verdict, hits = "hit  ", hits + 1
        else:
            verdict, wrong = "WRONG", wrong + 1
        rows.append((verdict, request, expected, top, top_score))
        if verdict != "hit  " or args.verbose:
            got = ("[" + " | ".join(sorted(result["candidates"])) + "]") if verdict == "AMBIG" else (top or "—")
            print(f"{verdict}  {request[:44]:44s}  expect {expected:26s} got {got:26s} {top_score:4.1f}")
            if args.verbose:
                print(f"{'':53s}runner-up {runner}")

    total = len(cases)
    print(
        f"\n{hits}/{total} resolve to the expected layout"
        f"  ·  {wrong} misrouted  ·  {miss} unmatched  ·  {ambig} ambiguous"
    )
    if miss:
        print(
            "Unresolved cases are the ones worth fixing first: the table gives the agent nothing, so "
            "the layout it picks is whatever it happens to favour that day.",
            file=sys.stderr,
        )
    return 0 if hits == total else 1


if __name__ == "__main__":
    raise SystemExit(main())
