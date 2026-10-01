#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Placeholder index pages for planned books (set 2026-10-01 by Pablo: "index for books 30, 31, 32, 33 ... planned").
Every statement on a page comes from this repo's own records and is listed in FACTS with its source; nothing is invented.
    python3 tools/planned_books.py --write | --check"""
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
BOOKS = {
 30: ('XXX', 'Nothing about the subject of this book is recorded in the repository.',
      [('Rung 30 on the floor ladder is Volume XIII, Coherence (higher category theory); it lives in', 'book13/index.html', 'book13')]),
 31: ('XXXI', 'Nothing about the subject of this book is recorded in the repository.', []),
 32: ('XXXII', 'The only record is one sentence in Book VII, which names rung 32 as Motivic and Langlands.',
      [('That sentence is in', 'book7/ch-feigin.html', 'Book VII, the Feigin chapter')]),
 33: ('XXXIII', 'Rung 33 on the floor ladder: noncommutative geometry. The Lean file book33/Noncommutative.lean is not written.',
      [('Source held: Connes and Marcolli, 705 pages (kept outside the repository). Planning notes and tests:', None, None),
       ('Planning note on holology as a logic', 'docs/book33-holology-note.md', 'docs/book33-holology-note.md'),
       ('Test of operator properties', 'docs/book33-holology-test.py', 'docs/book33-holology-test.py'),
       ('Test of Baaz semantics on the radial toy', 'docs/book33-baaz-semantics-test.py', 'docs/book33-baaz-semantics-test.py')]),
}
CSS = ("body{font-family:Georgia,serif;background:#f6f3ec;color:#12141a;margin:0;line-height:1.7}"
       ".w{max-width:760px;margin:0 auto;padding:3rem 1.4rem}h1{font-weight:500;margin:.2rem 0}"
       ".k{font-family:ui-monospace,Menlo,monospace;font-size:.7rem;letter-spacing:.18em;text-transform:uppercase;color:#7a3410}"
       ".box{border:1px solid #c4bba8;background:#ebe6da;padding:1rem 1.2rem;margin:1.4rem 0}a{color:#17435f}"
       "@media(prefers-color-scheme:dark){body{background:#12141a;color:#e8e2d4}.box{background:#242833;border-color:#4a4d57}a{color:#9cc3e0}.k{color:#e0a070}}")
def page(n):
    r, line, links = BOOKS[n]
    items = ''
    for text, href, label in links:
        if href is None: items += f'<p>{text}</p>\n<ul>\n'
        elif label == href or href.startswith('docs/'):
            if '<ul>' not in items: items += '<ul>\n'
            items += f'<li><a href="../{href}">{text}</a></li>\n'
        else:
            if '<ul>' not in items: items += '<ul>\n'
            items += f'<li>{text} <a href="../{href}">{label}</a>.</li>\n'
    if '<ul>' in items: items += '</ul>\n'
    return (f'<!DOCTYPE html>\n<html lang="en">\n<head>\n<meta charset="UTF-8">\n<meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
            f'<title>Book {r} &middot; Planned &mdash; Principia Orthogona</title>\n'
            f'<meta name="description" content="Placeholder for Book {r}. Planned, not written; only what the repository records is stated.">\n<style>{CSS}</style>\n</head>\n<body>\n<div class="w">\n'
            f'<div class="k">Principia Orthogona &middot; Book {r} &middot; Planned</div>\n<h1>Book {r}</h1>\n'
            f'<p>Status: <strong>planned</strong>. This book has no chapters yet.</p>\n<div class="box"><strong>What the repository records</strong>\n<p>{line}</p>\n{items}</div>\n'
            f'<div class="box"><strong>What is not here</strong>\n<p>A title, a scope and chapters. Those are the author&rsquo;s to set.</p></div>\n'
            f'<p><a href="../index-book{n}.html">Index of this folder</a> &middot; <a href="../master-index.html">All files</a></p>\n</div>\n</body>\n</html>\n')
def main():
    w = '--write' in sys.argv; bad = 0
    for n in BOOKS:
        p = ROOT / f'book{n}' / 'index.html'; new = page(n)
        if p.exists() and p.read_text(encoding='utf-8') == new: print('ok   ', p.relative_to(ROOT)); continue
        if w: p.parent.mkdir(exist_ok=True); p.write_text(new, encoding='utf-8'); print('wrote', p.relative_to(ROOT))
        else: print('STALE', p.relative_to(ROOT)); bad += 1
    sys.exit(1 if bad else 0)
main()
