#!/usr/bin/env python3
"""Triage of every theorem-like statement in the early master_book (model-3 era).
Classifies by what is ON THE PAGE: no proof / short proof / proof that defers / proof with a computation.
It does NOT check that a proof is correct (that is the next pass); it finds where a proof is absent or defers.
R24: runs before any sentence about the book's theorems is written. R9: nothing is changed in the book."""
import os, re, sys, csv
D = os.environ.get('EARLY_DIR', os.path.expanduser('~/Downloads'))
F = sys.argv[1] if len(sys.argv) > 1 else 'master_book_FINAL_v2.tex'
OUT = sys.argv[2] if len(sys.argv) > 2 else None
s = open(os.path.join(D, F), errors='ignore').read()
STM = ('theorem', 'proposition', 'lemma', 'corollary', 'conjecture')
tok = re.compile(r'\\begin\{(%s|proof)\}(\[[^\]]*\])?(.*?)\\end\{\1\}' % '|'.join(STM), re.S)
sec = re.compile(r'\\(chapter|section)\*?\{([^}]*)\}')
secs = [(m.start(), m.group(2)) for m in sec.finditer(s)]
def where(pos):
    t = ''
    for p, n in secs:
        if p <= pos: t = n
    return t[:60]
DEFER = re.compile(r'(see|cf\.?|proof (is )?(omitted|deferred|left)|left to the reader|omitted|well[- ]known|standard (argument|result)|follows from|by (the )?(standard|classical)|stated without|we (do not|omit)|sketch|appendix|\\cite|\\ref\{(thm|prop)|Lean|zenodo|reference)', re.I)
HAND = re.compile(r'(clearly|obviously|it is easy|trivial|straightforward|by construction|by definition|immediate)', re.I)
MATH = re.compile(r'(\$|\\\[|\\begin\{(equation|align))')
items = []; last = None
LAB = re.compile(r'\\label\{([^}]*)\}')
for m in tok.finditer(s):
    kind, title, body = m.group(1), (m.group(2) or '').strip('[]'), m.group(3)
    if kind != 'proof':
        lab = LAB.search(m.group(0)[:300])
        last = dict(kind=kind, title=title, label=lab.group(1) if lab else '', line=s.count('\n', 0, m.start()) + 1,
                    where=where(m.start()), stmt=re.sub(r'\s+', ' ', body).strip()[:140], proofs=[], ptitles=[])
        items.append(last)
    else:
        ref = re.search(r'\\ref\{([^}]*)\}', title)
        tgt = None
        if ref:   # "Proof of Theorem~\ref{thm:A}" binds to the latest statement with that label, wherever it sits
            for it in reversed(items):
                if it['label'] == ref.group(1): tgt = it; break
        elif last is not None and not last['proofs']:
            tgt = last
        if tgt is not None:
            tgt['proofs'].append(body); tgt['ptitles'].append(title)
rows = []
for it in items:
    P = it['proofs']
    if not P:
        cls = 'NO-PROOF'; w = 0; flag = ''
    else:
        p = ' '.join(P)
        w = len(re.sub(r'\\[a-zA-Z]+|[$\\{}^_]', ' ', p).split())
        d = DEFER.findall(p); h = HAND.findall(p)
        eqs = len(MATH.findall(p))
        sk = any('sketch' in t.lower() for t in it['ptitles'])
        if sk: cls = 'SKETCH'
        elif w < 25: cls = 'ONE-LINER'
        elif d and w < 120: cls = 'DEFERS'
        elif h and eqs < 3: cls = 'HAND-WAVED'
        else: cls = 'FULL-LOOKING'
        flag = ','.join(sorted(set(x[0].lower() if isinstance(x, tuple) else x.lower() for x in (d + h))))[:60]
    rows.append((it['line'], it['kind'], it['label'] or it['title'][:30], it['where'], cls, w, flag, it['stmt']))
from collections import Counter
c = Counter(r[4] for r in rows)
print('%s: %d theorem-like statements' % (F, len(rows)))
for k in ('NO-PROOF', 'SKETCH', 'ONE-LINER', 'DEFERS', 'HAND-WAVED', 'FULL-LOOKING'): print('  %-13s %3d' % (k, c[k]))
print('  by kind:', dict(Counter(r[1] for r in rows)))
for r in rows:
    print('  L%-5d %-11s %-12s %-46s w=%-4d %s' % (r[0], r[1][:11], r[4], (r[3] or '-')[:46], r[5], r[6]))
if OUT:
    with open(OUT, 'w', newline='') as f:
        w_ = csv.writer(f, delimiter='\t'); w_.writerow(['line', 'kind', 'title', 'section', 'class', 'proof_words', 'markers', 'statement'])
        w_.writerows(rows)
    print('wrote', OUT)
