#!/usr/bin/env python3
"""One entrypoint for repository checks. Core is stdlib-only; --render needs Chromium.

This does not generate artwork or approve design. Posters, reference galleries and
scroll viewers are explicitly separate from the 16:9 geometry gate.
"""
import argparse
from pathlib import Path
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[1]


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--render',action='store_true')
    args=parser.parse_args()
    commands=[
        ['scripts/compile_system.py','--check'],
        ['scripts/sync_examples.py','--check'],
        ['scripts/validate_editorial_explainer_plan.py','examples/case-study/illustration-plan.json','examples/case-study'],
        ['-m','unittest','discover','-s','tests'],
        ['scripts/validate_routing.py'],
        ['scripts/validate_routing.py','--cases','specs/routing-cases-heldout.md'],
    ]
    if args.render:
        commands += [
            ['scripts/validate_layout.py','examples','--quiet'],
            ['scripts/validate_layout.py','examples/case-study','--deck','--quiet'],
            ['scripts/validate_layout.py','examples/deck-demo','--deck','--quiet'],
            ['scripts/check_antipatterns.py'],
        ]
    failures=[]
    for command in commands:
        print('\nRunning: python '+' '.join(command),flush=True)
        try: code=subprocess.run([sys.executable,*command],cwd=ROOT).returncode
        except OSError as exc: print(exc,file=sys.stderr);code=2
        if code:failures.append((command,code))
    if failures:
        print(f'\n{len(failures)} check(s) failed',file=sys.stderr)
        return 2 if any(code==2 for _,code in failures) else 1
    print('\nAll selected checks passed. Rendered visual review is still required.')
    return 0


if __name__=='__main__':
    raise SystemExit(main())
