"""Measure agreement with human A/B judgements; never use this as a pass/fail taste gate.

Historical pairs come from preferences.md + frozen _ab files. New labelled rounds come
from ab-rounds.md + a SHA256-verified ab_round.py manifest. Pending rounds are excluded.
Exit 0 = measurement completed (even low agreement); 2 = invalid data/render failure.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import re
import sys

import validate_layout as V
from ab_round import parse_spec

ROOT=Path(__file__).resolve().parents[1]
AB=ROOT/'examples/case-study/_ab'


def load_pairs(manifest_path=None):
    text=(ROOT/'specs/preferences.md').read_text(encoding='utf-8')
    historical={int(m[1]):m[2] for m in re.finditer(r'Round\s+(\d+)\s*[—-]\s*([AB])\s*>\s*([AB])',text)}
    pairs=[];missing=[]
    for n,winner in sorted(historical.items()):
        a,b=(AB/f'r{n}{letter}.html' for letter in 'AB')
        if a.is_file() and b.is_file(): pairs.append((n,winner,a,b))
        else: missing.append(n)
    declared={n:r for n,r in parse_spec().items() if r['winner']}
    if declared and manifest_path is None:
        raise ValueError('judged new rounds require --manifest; do not silently omit their votes')
    if manifest_path is not None:
        manifest_path=Path(manifest_path).resolve()
        manifest=json.loads(manifest_path.read_text(encoding="utf-8"))['rounds']
        for n,r in declared.items():
            if n in historical: raise ValueError(f'R{n}: duplicate historical/new round')
            row=manifest.get(str(n))
            if not row: raise ValueError(f'R{n}: judged but absent from manifest')
            paths=[]
            for side in 'AB':
                entry=row['variants'][side];path=manifest_path.parent/entry['path']
                if hashlib.sha256(path.read_bytes()).hexdigest()!=entry['sha256']:
                    raise ValueError(f'R{n}{side}: judged variant changed after rendering')
                paths.append(path)
            pairs.append((n,r['winner'],*paths))
    return pairs,missing


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--manifest',type=Path,default=ROOT/'specs/ab-reviewed/2026-08-31/manifest.json')
    parser.add_argument('--json',type=Path)
    args=parser.parse_args()
    try:
        pairs,missing=load_pairs(args.manifest)
        if not pairs: raise ValueError('no labelled pairs available')
        browsers=V.find_browsers(None)
        rows=[];counts=dict(agree=0,disagree=0,tie=0)
        for n,winner,a,b in pairs:
            scores=[]
            for path in (a,b):
                html=path.read_text(encoding='utf-8')
                png=V.render_with_any(path,browsers,1920,1080,.25)
                metrics=V.analyse(*V.decode_png(png))
                scores.append(len(V.evaluate(path,metrics,V.slide_kind(html),V.find_hardcoded_hex(html,False),
                                             V.visible_text(html),V.declared_langs(html,None))))
            sa,sb=scores
            verdict='tie' if sa==sb else ('agree' if ('A' if sa<sb else 'B')==winner else 'disagree')
            counts[verdict]+=1;rows.append(dict(round=n,winner=winner,A=sa,B=sb,verdict=verdict))
            print(f'R{n}: human={winner} gate A={sa} B={sb} {verdict}',flush=True)
        report=dict(pairs=len(rows),**counts,missingHistoricalPairs=missing,rows=rows)
        print(json.dumps({k:v for k,v in report.items() if k!='rows'}))
        print('Diagnostic only: agreement is environment-dependent and does not certify design quality.')
        if args.json:args.json.write_text(json.dumps(report,indent=2)+'\n', encoding="utf-8", newline="\n")
        return 0
    except (OSError,ValueError,KeyError,V.LayoutError) as exc:
        print(f'calibration could not run: {exc}',file=sys.stderr);return 2


if __name__=='__main__':
    raise SystemExit(main())
