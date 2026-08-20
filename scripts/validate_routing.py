#!/usr/bin/env python3
"""Measure whether the router actually resolves a real request to the right layout.

`compile_system.py --check` proves every layout is *reachable* — it has a `content-map.md` row, its
triggers are unique, its `dependsOn` resolve. That is structure. It says nothing about whether a
request phrased the way a person phrases it lands on the right entry, which is the failure the whole
router exists to prevent: the agent finds nothing to match, free-picks from memory, and reaches for
the same familiar layout every time.

So this replays `specs/routing-cases.md` through the router and reports one of three outcomes:

    HIT    the expected layout scored top
    WRONG  a different layout scored top — the table actively misroutes this request
    MISS   nothing scored at all — the table gave the agent no signal, so it free-picks

**Read MISS as the important number.** WRONG is a trigger that needs sharpening; MISS is a hole.

This matcher is lexical: CJK bigrams plus latin word stems, scored against each entry's triggers and
intent line. The agent reading `generated-router.md` matches *semantically* and will do better, so
these results are a **lower bound**, not a prediction of agent behaviour. That is the point — a case
that HITs here is one the agent cannot get wrong, because the table alone determines it. A MISS here
is a case whose outcome rests entirely on the model's judgement that day, which is exactly the
inconsistency this system was built to remove.

**Two fixtures, and the gap between them is the real result.** `specs/routing-cases.md` is the
working set; triggers were sharpened against it, so it scores 30/30 and that number means very
little. `specs/routing-cases-heldout.md` was written afterwards without consulting any trigger list
and scores **4/10**. Trust the held-out number. If you tune against it, it is spent — write a new one.

Measured so far: adding 繁中 triggers to 17 layouts moved blind performance from 30% to ~40%. The
first pass found the cause of the original failure — only 10 of 122 triggers contained any 繁中 while
繁中 is the primary output language, so 17 of 25 layouts were invisible to Chinese input and the 8
that were visible swallowed everything.

Usage:
    python scripts/validate_routing.py            # the working fixture
    python scripts/validate_routing.py --cases specs/routing-cases-heldout.md   # the honest one
    python scripts/validate_routing.py --verbose  # show the runner-up and score for each

Exit codes: 0 = every case HITs · 1 = some WRONG or MISS · 2 = cannot run.
"""

from __future__ import annotations

import argparse
import json
import math
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ROUTER = ROOT / "system" / "router.json"
CASES = ROOT / "specs" / "routing-cases.md"

CJK = r"㐀-䶿一-鿿"
# Function words carry no routing signal and would otherwise let any two Chinese sentences overlap.
STOP_BIGRAMS = {"我們", "這個", "怎麼", "可以", "他們", "還有", "一個", "幾個", "把它"}
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
    """How common each token is in real deck copy — the weight a match on it deserves.

    The first version of this scorer weighted every token equally, which is how `使用者輪廓` turned
    the bigram 使用者 into an attractor that won unrelated requests outright. The obvious fix — IDF
    over the router's own 25 entries — does not work: it scores 改版 (in one layout) as *more*
    distinctive than 使用者 (in four), yet 改版 was an attractor too. Rarity among layouts is the
    wrong question. What matters is rarity among the things people actually say, so the corpus is the
    161 example slides' real copy. Measured against the two attractors found by hand, it ranks them
    lowest (使用 1.20, 用者 1.37, 改版 2.00) and the distinctive replacements highest (人物誌 5.09,
    親和 5.09, 象限 4.39).
    """
    docs: list[set[str]] = []
    for path in (ROOT / "examples").rglob("*.html"):
        text = path.read_text(encoding="utf-8", errors="replace")
        body = text.rsplit("</style>", 1)[-1]
        body = re.sub(r"<[^>]+>", " ", body)
        body = re.sub(r"&[a-z]+;", " ", body)
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
        if (e.get("material"), e.get("arrangement"), e.get("itemCount")) == want
    ]


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
    ap.add_argument("--cases", type=Path, default=CASES, help="alternate fixture (for held-out runs)")
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
        pool = entries
        if shape:
            narrowed = by_shape(shape, entries)
            if narrowed:
                pool = {k: entries[k] for k in narrowed}
        ranked = sorted(
            ((score(request, e, idf), k) for k, e in pool.items()), reverse=True
        )
        top_score, top = ranked[0]
        if shape and len(pool) == 1:
            top_score = max(top_score, 1.0)  # shape alone settled it
        runner = ranked[1][1] if len(ranked) > 1 else "-"
        if top_score <= 0 and shape and len(pool) < len(entries):
            # shape did narrow it; intent just failed to break the remaining tie. That is a much
            # smaller failure than "nothing matched" and must not be reported as a free-pick.
            verdict, ambig = "AMBIG", ambig + 1
        elif top_score <= 0:
            verdict, miss = "MISS ", miss + 1
        elif top == expected:
            verdict, hits = "hit  ", hits + 1
        else:
            verdict, wrong = "WRONG", wrong + 1
        rows.append((verdict, request, expected, top, top_score))
        if verdict != "hit  " or args.verbose:
            got = ("[" + " | ".join(sorted(pool)) + "]") if verdict == "AMBIG" else ("—" if top_score <= 0 else top)
            print(f"{verdict}  {request[:44]:44s}  expect {expected:26s} got {got:26s} {top_score:4.1f}")
            if args.verbose:
                print(f"{'':53s}runner-up {runner}")

    total = len(cases)
    print(
        f"\n{hits}/{total} resolve to the expected layout"
        f"  ·  {wrong} misrouted  ·  {miss} unresolved (agent free-picks)"
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
