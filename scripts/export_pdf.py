#!/usr/bin/env python3
"""Export ordered single-slide HTML files to a 16:9 PDF with native text.

Needs Chromium and pypdf. Input directories are sorted by filename; explicit file
arguments keep their order. Viewers/reference galleries are rejected, not silently
printed as slides. Source HTML is unchanged. Run check_system.py --render first.
"""
from __future__ import annotations

import argparse
import html
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import time

from example_files import collect
from slide_html import slides
from validate_layout import LayoutError, find_browsers

PRINT_STYLE = """<style>
@page { size:1920px 1080px; margin:0; }
@media print {
 html,body { width:1920px!important; height:1080px!important; margin:0!important; padding:0!important; }
 * { -webkit-print-color-adjust:exact!important; print-color-adjust:exact!important; }
 .slide { width:1920px!important; height:1080px!important; margin:0!important; box-shadow:none!important; }
}
</style>"""


def printable(source: Path) -> str:
    text = source.read_text(encoding="utf-8")
    if len(slides(text)) != 1 or "poster" in slides(text)[0].classes:
        raise ValueError(f"{source}: expected one .slide; export the individual slide files")
    # Existing authored <base> stays authoritative. Otherwise retain relative asset URLs.
    if not re.search(r'<base\b', text, re.I):
        base = '<base href="' + html.escape(source.parent.as_uri()+'/') + '">'
        text, count = re.subn(r'(<head\b[^>]*>)',lambda m:m[0]+base,text,count=1,flags=re.I)
        if not count:
            raise ValueError(f"{source}: missing <head>")
    text, count = re.subn(r'</head\s*>',PRINT_STYLE+'</head>',text,count=1,flags=re.I)
    if not count:
        raise ValueError(f"{source}: missing </head>")
    return text


def print_one(browser: str, page: Path, output: Path, profile: Path) -> None:
    # Isolated profile; never touch the user's open browser. File completion avoids
    # throwing away a valid export when Chrome hangs during profile shutdown.
    command = [browser,'--headless','--disable-gpu','--no-first-run','--no-default-browser-check',
               '--disable-extensions','--disable-background-networking','--disable-component-update',
               '--disable-sync','--metrics-recording-only','--allow-file-access-from-files',
               '--no-pdf-header-footer','--virtual-time-budget=5000',
               f'--user-data-dir={profile}',f'--print-to-pdf={output}',page.as_uri()]
    with tempfile.TemporaryFile() as log:
        process = subprocess.Popen(command,stdout=log,stderr=log)
        try:
            deadline=time.monotonic()+60
            while time.monotonic()<deadline:
                if output.exists() and output.read_bytes().rstrip().endswith(b'%%EOF'):
                    return
                if process.poll() is not None:
                    break
                time.sleep(.1)
            log.seek(0)
            detail=log.read().decode('utf-8','replace')[-600:]
            raise LayoutError(f'PDF print failed: {detail}')
        finally:
            if process.poll() is None:
                process.terminate()
                try: process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    process.kill();process.wait(timeout=5)


def main() -> int:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('slides',type=Path,nargs='+')
    parser.add_argument('--out',type=Path,required=True)
    parser.add_argument('--browser')
    parser.add_argument('--force',action='store_true',help='replace an existing output')
    args=parser.parse_args()
    try:
        from pypdf import PdfReader,PdfWriter
    except ImportError:
        print('PDF export needs pypdf: python -m pip install -r requirements-export.txt',file=sys.stderr)
        return 2
    output=args.out.resolve()
    if output.exists() and not args.force:
        print(f'{output} already exists; choose another path or --force',file=sys.stderr)
        return 2
    try:
        paths=[]
        for value in args.slides:
            if not value.exists(): raise ValueError(f'input not found: {value}')
            for path in collect([value]):
                if path not in paths: paths.append(path)
        if not paths: raise ValueError('no current slide HTML files found')
        pages=[printable(p) for p in paths]  # validate all inputs before rendering
        browsers=find_browsers(args.browser)
        output.parent.mkdir(parents=True,exist_ok=True)
        with tempfile.TemporaryDirectory(prefix='.pdf-build-',dir=output.parent) as tmp:
            tmp=Path(tmp);writer=PdfWriter()
            for index,(source,content) in enumerate(zip(paths,pages),1):
                page=tmp/f'{index:03}.html';page.write_text(content,encoding='utf-8')
                pdf=tmp/f'{index:03}.pdf'
                last_error=None
                for attempt,browser in enumerate(browsers):
                    try:
                        print_one(browser,page,pdf,tmp/f'profile-{index}-{attempt}')
                        last_error=None;break
                    except (LayoutError,OSError) as exc:
                        last_error=exc
                        pdf.unlink(missing_ok=True)
                if last_error: raise last_error
                reader=PdfReader(pdf)
                if len(reader.pages)!=1:
                    raise ValueError(f'{source}: print produced {len(reader.pages)} pages; expected one')
                writer.add_page(reader.pages[0])
                print(f'{index}/{len(paths)} exported: {source.name}',flush=True)
            writer.add_metadata({'/Title':output.stem,'/Creator':'Bonny Slide System — Chromium PDF export'})
            result=tmp/'result.pdf';writer.write(result)
            if len(PdfReader(result).pages)!=len(paths):
                raise ValueError('merged PDF page count mismatch')
            result.replace(output)
        print(f'PDF saved: {output} ({len(paths)} slides; native text, subject to browser/font support)')
        return 0
    except (OSError,ValueError,LayoutError,subprocess.TimeoutExpired) as exc:
        print(f'PDF export: {exc}',file=sys.stderr)
        return 2


if __name__=='__main__':
    raise SystemExit(main())
