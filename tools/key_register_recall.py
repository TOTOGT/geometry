#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Pablo Nogueira Grossi / G6 LLC
"""
key_register_recall.py -- recall of tools/key_register.py against a small hand-labelled gold set.

Book XIV ch 5 said recall was never measured. This measures it on docs/key-register-gold.tsv.
For every context labelled Y it asks whether key_register's own pattern (the same regular
expression, the same sense words) fires on that place in the page. Standard library only.

    python3 tools/key_register_recall.py

Limits, all stated on the page too: the labels are one reader's (Claude's), candidates come from a
window search, so a gloss written with no sense word near the letter is invisible to this set;
one sample of 60 pages; only this one of the four tools.
"""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import key_register as kr

GOLD = os.path.join(kr.ROOT, 'docs', 'key-register-gold.tsv')
WORD = {L: {w: s for s, ws in kr.SENSES[L].items() for w in ws} for L in kr.SENSES}


def tool_fires(L, t, start, end):
    rx = re.compile(r'(?<![A-Za-z0-9_])' + L +
                    r'\s*(?:—|–|-|=|:|\()\s*(?i:the\s+|a\s+|o\s+)?([A-Za-zçãõéêíóúàÀ-Ú]+)')
    for m in rx.finditer(t, max(0, start - 5), end + 5):
        if m.start() < end and WORD[L].get(m.group(1).lower()):
            return True
    return False


def main():
    rows, stale = [], 0
    for line in open(GOLD, encoding='utf-8'):
        if line.startswith('#') or not line.strip():
            continue
        f, L, lab, ctx = line.rstrip('\n').split('\t', 3)
        if lab != 'Y':
            rows.append((f, L, lab, None))
            continue
        t = kr.text(f)
        i = t.find(ctx)
        if i < 0:
            stale += 1
            continue
        rows.append((f, L, lab, tool_fires(L, t, i, i + len(ctx))))
    Y = [r for r in rows if r[2] == 'Y']
    pairs = {(r[0], r[1]) for r in Y}
    hit_pairs = {(r[0], r[1]) for r in Y if r[3]}
    pages = {r[0] for r in Y}
    hit_pages = {r[0] for r in Y if r[3]}
    print(f"gold contexts labelled Y: {len(Y)}; tool fires on {sum(1 for r in Y if r[3])}"
          f" -> mention recall {sum(1 for r in Y if r[3])/len(Y):.2f}")
    print(f"page-letter pairs with a gold gloss: {len(pairs)}; tool finds {len(hit_pairs)}"
          f" -> pair recall {len(hit_pairs)/len(pairs):.2f}")
    print(f"pages with a gold gloss: {len(pages)}; tool finds one on {len(hit_pages)}")
    print(f"labelled N: {sum(1 for r in rows if r[2]=='N')}, A (excluded): {sum(1 for r in rows if r[2]=='A')}, stale: {stale}")
    return 1 if stale else 0


if __name__ == '__main__':
    sys.exit(main())
