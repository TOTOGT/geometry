#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Pablo Nogueira Grossi / G6 LLC
"""
crossref_recall.py -- recall of tools/crossref.py's "Named on this page" detection against docs/crossref-gold.tsv.

For every context labelled Y (the prose refers to a specific other page), and every target it names, ask whether crossref
accounts for that target on that page: it is in the tool's named-mentions list, or the page already links it. Reported by kind
(WP number, gallery person, 'chapter N'). Also the other direction on the same 39 pages: how many of the tool's named entries have
a Y label behind them (a precision on this sample, with the unlabelled ones counted separately, not as wrong).

    python3 tools/crossref_recall.py
Standard library only. Run from a checkout near the commit named in the gold file; rows whose page is gone are counted stale.
Limits, also stated on Book XIV ch 5: one labeller (Claude), one sample of 40 chapters, only this one of the four tools.
"""
import os, sys
from collections import Counter, defaultdict
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import crossref as C

GOLD = os.path.join(C.ROOT, 'docs', 'crossref-gold.tsv')

def main():
    pages = C.load()
    named = C.named_mentions(pages)
    rows = []
    for line in open(GOLD, encoding='utf-8'):
        if line.startswith('#') or not line.strip(): continue
        p, k, m, lab, tg, ctx = line.rstrip('\n').split('\t', 5)
        rows.append((p, k, m, lab, [t for t in tg.split(';') if t]))
    stale = sum(1 for r in rows if r[0] not in pages)
    ok = Counter(); tot = Counter(); missed = []
    pairs_y = set()
    for p, k, m, lab, tg in rows:
        if lab != 'Y' or p not in pages: continue
        for t in tg:
            pairs_y.add((p, t))
            tot[k] += 1
            found = {x for x, _ in named.get(p, [])}
            if t in found: ok[(k, 'named')] += 1
            elif t in pages[p]['links']: ok[(k, 'linked')] += 1
            else: missed.append((p, k, m, t))
    print(f'gold: {len(rows)} rows, stale {stale}; labels {dict(Counter(r[3] for r in rows))}')
    print('Y (page, target) pairs by kind, and whether the tool accounts for them:')
    allt = allo = 0
    for k in ('WP', 'PERSON', 'CHAPTER'):
        n = tot[k]
        a, b = ok[(k, 'named')], ok[(k, 'linked')]
        allt += n; allo += a + b
        print(f'  {k:8} {n:3} pairs: {a} in the tool\'s named list, {b} already linked, {n-a-b} missed'
              + (f'  recall {(a+b)/n:.2f}  (named list alone {a/n:.2f})' if n else ''))
    print(f'  all      {allt:3} pairs: recall {allo/allt:.2f}' if allt else '')
    print('missed:')
    for p, k, m, t in missed: print(f'  {k:7} {p}  [{m}] -> {t}')
    sample = {r[0] for r in rows}
    ent = [(p, t) for p in sample if p in pages for t, _ in named.get(p, [])]
    backed = sum(1 for e in ent if e in pairs_y)
    print(f'tool named entries on the {len(sample)} sampled pages: {len(ent)}; with a Y label behind them: {backed}; '
          f'without (no row, or labelled N/A): {len(ent)-backed}')
    print('-- these are NOT all errors: the gold covers only the candidates listed, so an entry with no row may still be right')
    return 0

if __name__ == '__main__':
    sys.exit(main())
