#!/usr/bin/env python3
"""Read and render bundled manual pages using original PDF page numbers."""
import argparse
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]


def load_source():
    meta = json.loads((ROOT / 'references/source.json').read_text(encoding='utf-8'))
    lines = (ROOT / 'references/manual-text.md').read_text(encoding='utf-8').splitlines()
    return meta, lines


def page_text(page, lines):
    return '\n'.join(lines[page['start_line'] - 1:page['end_line']])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    search = sub.add_parser('search', help='Literal search; add --regex for a regular expression')
    search.add_argument('pattern')
    search.add_argument('--regex', action='store_true')
    search.add_argument('--limit', type=int, default=12)
    show = sub.add_parser('show', help='Show pages by original PDF page number')
    show.add_argument('pages', type=int, nargs='+')
    render = sub.add_parser('render', help='Render an original PDF page from the local excerpt')
    render.add_argument('page', type=int)
    render.add_argument('--out', required=True, type=Path)
    render.add_argument('--dpi', type=int, default=180)
    render.add_argument('--clip', nargs=4, type=float, metavar=('X0', 'Y0', 'X1', 'Y1'),
                        help='Optional normalized crop, coordinates from 0 to 1')
    sub.add_parser('info', help='Print provenance and included page numbers')
    args = parser.parse_args()
    meta, lines = load_source()
    pages = {p['original_pdf_page']: p for p in meta['pages']}
    if args.command == 'info':
        print(json.dumps({k: v for k, v in meta.items() if k != 'pages'}, ensure_ascii=False, indent=2))
        print('Included original PDF pages:', ', '.join(map(str, pages)))
        return
    if args.command == 'search':
        if args.limit < 1:
            parser.error('--limit must be positive')
        try:
            pattern = re.compile(args.pattern if args.regex else re.escape(args.pattern), re.I)
        except re.error as e:
            parser.error(str(e))
        hits = 0
        for page in pages.values():
            content = page_text(page, lines)
            found = pattern.search(content)
            if not found:
                continue
            print(f"PDF {page['original_pdf_page']} | 纸面 {page['printed_page'] or '未辨认/无页码'} | 节选页 {page['excerpt_page']} | {page['text_status']}")
            print(content[max(0, found.start() - 100):found.end() + 230].strip())
            print()
            hits += 1
            if hits >= args.limit:
                break
        if not hits:
            print('未找到文字匹配。扫描页/图中标注可能没有文字层；先查 references/index.md，再 render 原页。')
        return
    if args.command == 'show':
        missing = [n for n in args.pages if n not in pages]
        if missing:
            parser.error(f'本技能没有这些原PDF页: {missing}；请查看 references/index.md 或总导航技能。')
        for n in args.pages:
            print(page_text(pages[n], lines))
            print()
        return
    if args.page not in pages:
        parser.error(f'本技能没有原PDF第 {args.page} 页；请查看 references/index.md。')
    if not 36 <= args.dpi <= 600:
        parser.error('--dpi must be between 36 and 600')
    if args.out.suffix.lower() != '.png':
        parser.error('--out must be a PNG path')
    if args.clip:
        x0, y0, x1, y1 = args.clip
        if not (0 <= x0 < x1 <= 1 and 0 <= y0 < y1 <= 1):
            parser.error('--clip requires 0 <= x0 < x1 <= 1 and 0 <= y0 < y1 <= 1')
    args.out.parent.mkdir(parents=True, exist_ok=True)
    pdf = ROOT / meta['excerpt_path']
    number = pages[args.page]['excerpt_page']
    try:
        import fitz
    except ImportError:
        if args.clip:
            parser.error('裁剪需要 PyMuPDF；可去掉 --clip 先渲染整页。')
        renderer = shutil.which('pdftoppm')
        if not renderer:
            parser.error('需要 PyMuPDF 或 pdftoppm 才能查看原图；不要根据缺失文字猜测。')
        prefix = args.out.with_suffix('')
        subprocess.run([renderer, '-f', str(number), '-l', str(number), '-singlefile',
                        '-r', str(args.dpi), '-png', str(pdf), str(prefix)], check=True)
    else:
        with fitz.open(pdf) as doc:
            page = doc[number - 1]
            crop = None
            if args.clip:
                r = page.rect
                crop = fitz.Rect(r.x0 + x0*r.width, r.y0 + y0*r.height,
                                 r.x0 + x1*r.width, r.y0 + y1*r.height)
            page.get_pixmap(dpi=args.dpi, clip=crop, alpha=False).save(args.out)
    print(f"原PDF第 {args.page} 页（节选第 {number} 页）已渲染到 {args.out.resolve()}")


if __name__ == '__main__':
    main()
