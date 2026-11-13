#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Pablo Nogueira Grossi / G6 LLC
"""
subject_tags_sheet.py -- a BLIND sheet for checking the subject tags in docs/subjects.tsv.

subject_tags.py does not detect anything: docs/subjects.tsv is an editorial decision and the tool stamps it. What can be
measured is whether a second reading reaches the same decision. This draws 60 chapters with random.seed(20261114) from the
chapters that have a non-apparatus row, and writes title, description and the opening of the text for each, with the tag
REMOVED, so a labeller can choose from the vocabulary without seeing the editor's choice.

    python3 tools/subject_tags_sheet.py > subject-tags-blind.tsv

Note: the draw is from the pool of rows as it stood on 2026-11-13 BEFORE 187 rows were added the same day (docs/subjects.tsv);
re-running now draws a different 60. docs/subject-tags-gold.tsv and docs/blind/subject-tags-blind.tsv are the frozen sample.

Columns: id, page, title, description, opening, label (empty, for the labeller). The vocabulary is the VOCAB set of subject_tags.py
(listed at the top of the sheet). Standard library only.
"""
import html, os, random, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import subject_tags as ST

def opening(src):
    s = ST.BLOCK.sub('', src)
    s = re.sub(r'(?is)<!--po-(related|gss|run)-->.*?<!--/po-\1-->', ' ', s)
    s = re.sub(r'(?is)<(script|style|nav|header\b[^>]*class="[^"]*pillars)[^>]*>.*?</\1>', ' ', s)
    m = re.search(r'(?i)<h1\b', s)
    s = s[m.start():] if m else s
    t = html.unescape(re.sub(r'(?s)<[^>]+>', ' ', s))
    return re.sub(r'\s+', ' ', t).strip()[:420]

def meta(src, key):
    m = re.search(r'<meta name="%s" content="([^"]*)"' % key, src)
    return html.unescape(m.group(1)).strip() if m else ''

def title(src):
    m = re.search(r'<title[^>]*>(.*?)</title>', src, re.S | re.I)
    return re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', '', m.group(1)))).strip() if m else ''

def sample(n=60, seed=20261114):
    rows = ST.rows()
    pool = sorted(r for r in ST.chapters() if r in rows and rows[r][0] in ST.VOCAB and rows[r][0] != 'SERIES APPARATUS')
    random.seed(seed)
    return random.sample(pool, n), rows

if __name__ == '__main__':
    pages, _ = sample()
    print('# Choose one subject for each page from this list (exactly as written); write it in the last column.')
    print('# ' + ' | '.join(sorted(ST.VOCAB - {'PROFILE', 'SERIES APPARATUS'})))
    print('# id\tpage\ttitle\tdescription\topening\tlabel')
    for i, rel in enumerate(pages, 1):
        src = open(os.path.join(ST.ROOT, rel), encoding='utf-8', errors='replace').read()
        d = meta(src, 'description') or meta(src, 'og:description')
        print(f'{i}\t{rel}\t{title(src)}\t{d[:300]}\t{opening(src)}\t')
