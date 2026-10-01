#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Insert a one-line link to each book's Chapter 0 (definitions and notation) on its entry page.
Idempotent: skips a page that already carries the marker. Run: python3 tools/link_chapter_zero.py [--check]"""
import re, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
PAGES = {'book1':'index.html','book2':'index.html','book3':'index.html','book4':'contents.html','book5':'index.html',
         'book6':'index.html','book7':'index.html','book8':'index.html','omega':'omega-point-index.html','book10':'index.html'}
MARK = '<!--ch0-link-->'
LINE = (MARK + '<p class="ch0-link" style="max-width:860px;margin:.8rem auto;padding:.5rem 1rem;border-left:3px solid currentColor;font-size:.95em;">'
        '<a href="ch00-definitions.html">Chapter 0 &middot; Definitions and notation</a> '
        '&mdash; every defined term in this book, with its status (decided, verified, open).</p>\n')
def main():
    check = '--check' in sys.argv; bad = 0
    for b, f in PAGES.items():
        p = ROOT / b / f
        s = p.read_text(encoding='utf-8')
        if not (ROOT / b / 'ch00-definitions.html').exists(): print('MISSING ch00 for', b); bad += 1; continue
        if MARK in s: print('ok   ', b); continue
        if check: print('NOT LINKED', b); bad += 1; continue
        m = re.search(r'</h1>', s) or re.search(r'<body[^>]*>', s)
        if not m: print('NO ANCHOR', b); bad += 1; continue
        s = s[:m.end()] + '\n' + LINE + s[m.end():]
        p.write_text(s, encoding='utf-8'); print('added', b)
    sys.exit(1 if bad else 0)
main()
