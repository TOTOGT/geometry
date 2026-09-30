#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""index-count-verify.py -- checks the count in the "Chapters & Papers" heading of book6/index.html.

Written 2026-09-30 (R24: the script runs before the sentence). The heading said 118; it was a hand-written
number that had gone stale as papers were added. This script counts the rows of the chapter list itself
(anchors with class "ch-row" between the heading and "The Vow, Held in Reserve") and compares:

  distinct pages listed   = unique hrefs in the list          <- the number the heading prints
  in this folder          = hrefs with no '/'                 (each must exist as book6/<file>)
  sibling pages listed    = hrefs that leave the folder        (each must exist; ../../ ones are another repository: SKIP)
  rows                    = anchors, counting a page listed twice twice
  not in the list         = book6/*.html that no row links to (index.html excluded)

Prints SKIP, never PASS, when a file is missing. Exit 1 on a FAIL.
"""
import glob, os, re, sys
from collections import Counter
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
fails = []
def check(ok, msg, detail=''):
    print('    %s  %s%s' % ('PASS' if ok else 'FAIL', msg, ('  -- ' + detail) if detail and not ok else ''))
    if not ok: fails.append(msg)
try: s = open(os.path.join(ROOT, 'book6/index.html'), encoding='utf-8').read()
except OSError: print('SKIP  book6/index.html missing'); sys.exit(0)
m = re.search(r'<h2 class="section-h2">(\d+) Chapters &amp; Papers</h2>', s)
if not m: print('FAIL  heading "N Chapters & Papers" not found'); sys.exit(1)
printed = int(m.group(1))
sec = s[m.end():s.index('The Vow, Held in Reserve')]
rows = re.findall(r'<a href="([^"#]+)" class="ch-row">', sec)
uniq = set(rows); local = {h for h in uniq if '/' not in h}; sib = uniq - local
dup = [h for h, n in Counter(rows).items() if n > 1]
files = {os.path.basename(f) for f in glob.glob(os.path.join(ROOT, 'book6/*.html'))} - {'index.html'}
other_repo = sorted(h for h in uniq if h.startswith('../../'))
missing = [h for h in uniq if h not in other_repo and not os.path.exists(os.path.normpath(os.path.join(ROOT, 'book6', h)))]
notin = sorted(files - local)
print('rows %d | distinct pages %d (in this folder %d, sibling pages %d) | listed twice: %d | not in list: %s' % (len(rows), len(uniq), len(local), len(sib), len(dup), notin or 'none'))
check(not missing, 'every listed page in this repository exists', ', '.join(missing))
if other_repo: print('    SKIP  %d listed page(s) live in a sibling repository (../../) and cannot be checked here: %s' % (len(other_repo), ', '.join(other_repo)))
check(printed == len(uniq), 'the heading prints the number of distinct pages listed (%d)' % len(uniq), 'heading says %d' % printed)
declared = set()
try:
    for ln in open(os.path.join(ROOT, 'docs/unlisted.tsv'), encoding='utf-8'):
        if ln.startswith('book6/'): declared.add(os.path.basename(ln.split('\t')[0]))
except OSError: pass
check(set(notin) <= declared, 'every book6 page missing from the list is declared in docs/unlisted.tsv (R9)', ', '.join(sorted(set(notin) - declared)))
if fails: print('  %d FAIL' % len(fails)); sys.exit(1)
print('  all run checks passed.')
