#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Pablo Nogueira Grossi / G6 LLC
"""
crossref_gold_candidates.py -- candidate contexts for the crossref.py recall gold set (docs/crossref-gold.tsv).

Draws 40 chapters with random.seed(20261114) from crossref.load(). For each, lists every place the prose might
refer to another chapter, by a LOOSER rule than the tool's, independent of what the tool finds:
  WP       'WP-n' (any n, including numbers the tool skips as ambiguous)
  PERSON   a Scientist Gallery person: full name, or surname of 4+ letters even once, even on the tool's stop-list
  CHAPTER  'chapter N', 'Book X' (a possible reference to a specific chapter; the target is the labeller's to give)
One row per (page, kind, mention); the first context is shown. Candidates are NOT labelled here.

    python3 tools/crossref_gold_candidates.py > candidates.tsv
Standard library only. Needs the repo checkout the sample was drawn from (commit recorded in the gold file header).
"""
import os, random, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import crossref as C

def sample(pages, n=40, seed=20261114):
    random.seed(seed)
    return random.sample(sorted(pages), n)

def candidates(pages, rel):
    t = re.sub(r'\s+', ' ', pages[rel]['text'])
    people = C.people_index(pages)
    out, seen = [], set()
    def ctx(m): return t[max(0, m.start() - 90): m.end() + 90]
    for m in re.finditer(r'\bWP[-‑\s]?(\d{1,3}[A-Za-z]?)\b', t):
        k = ('WP', 'WP-' + m.group(1))
        if k not in seen: seen.add(k); out.append((k[0], k[1], ctx(m)))
    for name, tgt in people.items():
        if tgt == rel: continue
        sur = name.split()[-1]
        m = re.search(re.escape(name), t) if len(name.split()) > 1 else None
        if not m and len(sur) >= 4: m = re.search(r'\b' + re.escape(sur) + r'\b', t)
        if m:
            k = ('PERSON', name)
            if k not in seen: seen.add(k); out.append((k[0], name, ctx(m)))
    for m in re.finditer(r'\b(?:[Cc]hapters?|Books?|Volume)\s+(?:[IVXL]+|\d+)\b', t):
        k = ('CHAPTER', m.group(0))
        if k not in seen: seen.add(k); out.append((k[0], m.group(0), ctx(m)))
    return out

if __name__ == '__main__':
    pages = C.load()
    print('# page\tkind\tmention\tcontext')
    for rel in sample(pages):
        for kind, ment, c in candidates(pages, rel):
            print(f'{rel}\t{kind}\t{ment}\t{c}')
