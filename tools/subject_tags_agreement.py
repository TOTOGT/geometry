#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Pablo Nogueira Grossi / G6 LLC
"""
subject_tags_agreement.py -- does a blind reading of a page reach the subject docs/subjects.tsv gives it?

subject_tags.py detects nothing: it stamps the editorial subject onto the page, so "recall" has no meaning for it. What can be
measured is reproducibility of the editorial decision. docs/subject-tags-gold.tsv holds a blind label for 60 pages (labeller 1: Claude,
who saw title, description and opening only). This compares those labels with the CURRENT subjects.tsv, exactly and by field
(the text before the dot). The labeller is the model that wrote many of the rows, so this is not independent; a second
labeller's sheet (tools/gold_blind.py) is what would make it so.

    python3 tools/subject_tags_agreement.py
Standard library only.
"""
import os, sys
from collections import Counter
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import subject_tags as ST

GOLD = os.path.join(ST.ROOT, 'docs', 'subject-tags-gold.tsv')

def main():
    rows = ST.rows()
    gold = [l.rstrip('\n').split('\t') for l in open(GOLD, encoding='utf-8') if not l.startswith('#') and l.strip()]
    gold = [g for g in gold if g[0] != 'page']
    n = ex = fld = stale = 0; dis = []
    for page, lab in gold:
        if page not in rows: stale += 1; continue
        ed = rows[page][0]; n += 1
        ex += ed == lab; fld += ed.split(' · ')[0] == lab.split(' · ')[0]
        if ed != lab: dis.append((ed, lab, page))
    print(f'{n} pages ({stale} stale): exact agreement {ex}/{n} = {ex/n:.2f}; same field {fld}/{n} = {fld/n:.2f}')
    print('disagreements (subjects.tsv | blind label | page):')
    for ed, lab, page in sorted(dis): print(f'  {ed} | {lab} | {page}')
    pair = Counter((ed.split(' · ')[0], lab.split(' · ')[0]) for ed, lab, _ in dis if ed.split(' · ')[0] != lab.split(' · ')[0])
    print('field-level disagreements:', dict(pair))
    return 0

if __name__ == '__main__':
    sys.exit(main())
