#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Pablo Nogueira Grossi / G6 LLC
"""
gold_blind.py -- blind label sheets for a SECOND labeller, and the agreement between two labellers.

The four gold sets (docs/key-register-gold.tsv, lean-addresses-gold.tsv, crossref-gold.tsv, subject-tags-gold.tsv) were labelled by
one reader (Claude, one session each). A second reader who has not seen those labels is what turns "my reading" into a check.

    python3 tools/gold_blind.py sheet  key-register  > key-register-blind.tsv     labels removed, rows shuffled
    python3 tools/gold_blind.py agree  key-register  key-register-blind.tsv        compare the returned sheet with the gold
    names: key-register | lean-addresses | crossref | subject-tags

How to label: fill the LAST column (label) of every row; for crossref also the targets column (repo paths, ';' between several).
Use Y / N / A as the instructions at the top of the sheet say; for subject-tags write a subject from the list. Do not open the gold
file or the tool outputs first. The sheet carries row ids, so the returned file can be in any order.

agree reports exact agreement and Cohen's kappa on the labels (A rows are counted as a label, and also reported with A removed),
lists every disagreement, and for crossref compares the target sets on rows both mark Y.
Standard library only.
"""
import os, random, sys
from collections import Counter
HERE = os.path.dirname(os.path.abspath(__file__))
DOCS = os.path.join(os.path.dirname(HERE), 'docs')
SEED = 20261114

SETS = {   # name -> (file, columns of the gold rows, index of label column, instructions)
 'key-register': ('key-register-gold.tsv', ['page', 'letter', 'label', 'context'], 2,
   'Each row is a place in a page where a letter (C, K, F or U) stands near a word. Y = the page ties that letter to that sense in some wording '
   '(a gloss such as "K = threshold"); N = it is not a gloss; A = ambiguous. Context is a short window of the page text.'),
 'lean-addresses': ('lean-addresses-gold.tsv', ['page', 'token', 'label', 'context'], 2,
   'Each row is a token containing ".lean" in a page. Y = the token names a Lean file; N = it does not (a bare ".lean" or "*.lean" in a sentence '
   'about the extension); A = ambiguous.'),
 'crossref': ('crossref-gold.tsv', ['page', 'kind', 'mention', 'label', 'targets', 'context'], 3,
   'Each row is a place where the prose of a page might refer to another page of this repository. Y = this context refers to a specific other '
   'page (write its repo path in the targets column; several with ";"); N = it does not (the page itself, the page\'s own navigation links, a book '
   'with no chapter named, a word that is not the person, a source outside the series); A = ambiguous.'),
 'subject-tags': ('subject-tags-gold.tsv', ['page', 'label'], 1, ''),
}

def read_gold(name):
    fn, cols, li, _ = SETS[name]
    rows = []
    for line in open(os.path.join(DOCS, fn), encoding='utf-8'):
        if line.startswith('#') or not line.strip(): continue
        f = line.rstrip('\n').split('\t', len(cols) - 1)
        if f[li] == 'label': continue          # a column-header row
        rows.append(f)
    return rows

def sheet(name):
    if name == 'subject-tags':
        import subprocess
        sys.stdout.write(subprocess.run([sys.executable, os.path.join(HERE, 'subject_tags_sheet.py')], capture_output=True, text=True, check=True).stdout)
        return
    fn, cols, li, instr = SETS[name]
    rows = read_gold(name)
    order = list(range(1, len(rows) + 1)); random.Random(SEED).shuffle(order)
    print('# BLIND SHEET for', name, '-', instr)
    print('# Fill the last column' + (' and the targets column' if name == 'crossref' else '') + '. Row ids are kept so order does not matter.')
    keep = [c for i, c in enumerate(cols) if i != li and c != 'targets']
    head = ['id'] + keep + (['targets'] if name == 'crossref' else []) + ['label']
    print('# ' + '\t'.join(head))
    for i in order:
        r = dict(zip(cols, rows[i - 1]))
        print('\t'.join([str(i)] + [r[c] for c in keep] + ([''] if name == 'crossref' else []) + ['']))

def kappa(a, b):
    n = len(a); po = sum(x == y for x, y in zip(a, b)) / n
    ca, cb = Counter(a), Counter(b)
    pe = sum(ca[k] * cb[k] for k in set(a) | set(b)) / (n * n)
    return (po - pe) / (1 - pe) if pe < 1 else 1.0

def agree(name, path):
    fn, cols, li, _ = SETS[name]
    gold = read_gold(name)
    g = {i + 1: r for i, r in enumerate(gold)}
    ret = {}
    for line in open(path, encoding='utf-8'):
        if line.startswith('#') or not line.strip(): continue
        f = line.rstrip('\n').split('\t')
        ret[int(f[0])] = f
    if name == 'subject-tags':   # the sheet's id is the position in the sample; gold rows are in the same order
        pairs = [(g[i][1], ret[i][-1].strip(), g[i][0]) for i in sorted(ret) if i in g]
    else:
        pairs = [(g[i][li], ret[i][-1].strip(), g[i][0]) for i in sorted(ret) if i in g]
    pairs = [p for p in pairs if p[1]]
    n = len(pairs)
    if not n: print('no labelled rows in', path); return 1
    a, b = [p[0] for p in pairs], [p[1] for p in pairs]
    ag = sum(x == y for x, y in zip(a, b))
    print(f'{name}: {n} rows labelled by both; exact agreement {ag}/{n} = {ag/n:.2f}; Cohen kappa {kappa(a, b):.2f}')
    if name != 'subject-tags':
        c = [(x, y) for x, y in zip(a, b) if x != 'A' and y != 'A']
        if c:
            ag2 = sum(x == y for x, y in c)
            print(f'  with A removed (rows both call Y or N): {len(c)} rows, agreement {ag2}/{len(c)} = {ag2/len(c):.2f}, kappa {kappa([x for x,_ in c],[y for _,y in c]):.2f}')
    if name == 'crossref':
        both = [i for i in sorted(ret) if i in g and g[i][3] == 'Y' and ret[i][-1].strip() == 'Y']
        same = sum(set(g[i][4].split(';')) == set(t for t in ret[i][-2].split(';') if t) for i in both)
        print(f'  rows both mark Y: {len(both)}; same target set on {same}')
    if name == 'subject-tags':
        coarse = sum(x.split(' · ')[0] == y.split(' · ')[0] for x, y, _ in pairs)
        print(f'  same field (text before the dot): {coarse}/{n} = {coarse/n:.2f}')
    print('disagreements (gold label | returned label | page):')
    for x, y, p in pairs:
        if x != y: print(f'  {x} | {y} | {p}')
    return 0

if __name__ == '__main__':
    if len(sys.argv) >= 3 and sys.argv[1] == 'sheet' and sys.argv[2] in SETS:
        sheet(sys.argv[2])
    elif len(sys.argv) == 4 and sys.argv[1] == 'agree' and sys.argv[2] in SETS:
        sys.exit(agree(sys.argv[2], sys.argv[3]))
    else:
        print(__doc__); sys.exit(2)
