#!/usr/bin/env python3
"""Map each theorem-like statement of the early master_book to its best counterpart in Paper 2
(dm3_toy_model_v3.tex, 'The dm3 Operator: Explicit Toy Model and Global Dynamical Analysis', v3 July 2026),
and report wording/number differences. Paper 2 v3 is NEWER than the Zenodo v1 PDF; differences can mean
either an early-file error or a later edit, and the script says which file each side is.
R24: runs before any sentence. R9: no file is changed."""
import os, re, sys, difflib, csv
D = os.environ.get('EARLY_DIR', os.path.expanduser('~/Downloads'))
EARLY = 'master_book_FINAL_v2.tex'; P2 = 'dm3_toy_model_v3.tex'
OUT = sys.argv[1] if len(sys.argv) > 1 else None
def plain(x):
    x = re.sub(r'\\label\{[^}]*\}|\\ref\{[^}]*\}|\\eqref\{[^}]*\}|\\cite[a-z]*(\[[^\]]*\])?\{[^}]*\}', ' ', x)
    x = re.sub(r'\\(mathcal|mathrm|text|emph|textbf|mathbb|cB|Orb)\b', ' ', x)
    x = re.sub(r'[$\\{}\[\]^_~]|\\[a-zA-Z]+', ' ', x)
    return re.sub(r'\s+', ' ', x).strip().lower()
def words(x): return re.findall(r'[a-z0-9.+\-]+', plain(x))
def jacc(a, b):
    a, b = set(a), set(b); return len(a & b) / max(1, len(a | b))
def stmts(f):
    t = open(os.path.join(D, f), errors='ignore').read(); out = []
    for m in re.finditer(r'\\begin\{(theorem|proposition|lemma|corollary|conjecture)\}(\[[^\]]*\])?(.*?)\\end\{\1\}', t, re.S):
        out.append(dict(kind=m.group(1), title=(m.group(2) or '').strip('[]'), body=m.group(3), line=t.count('\n', 0, m.start()) + 1))
    return out
E = stmts(EARLY); P = stmts(P2)
print('early: %d statements; Paper 2 v3: %d statements' % (len(E), len(P)))
rows = []; mapped = 0; nums_bad = 0
for e in E:
    ew = words(e['title'] + ' ' + e['body']); best = None
    for p in P:
        sc = jacc(ew, words(p['title'] + ' ' + p['body']))
        if best is None or sc > best[0]: best = (sc, p)
    sc, p = best
    if sc < 0.35:
        rows.append((e['line'], e['kind'], e['title'][:40], 'NO-MATCH', round(sc, 2), '', '')); continue
    mapped += 1
    a, b = words(e['body']), words(p['body'])
    sm = difflib.SequenceMatcher(None, a, b)
    diffs = ['%s:[%s]->[%s]' % (op[0], ' '.join(a[i1:i2])[:40], ' '.join(b[j1:j2])[:40]) for op, i1, i2, j1, j2 in sm.get_opcodes() if op != 'equal']
    numd = [d for d in diffs if re.search(r'\d', d)]
    status = 'SAME' if sm.ratio() > 0.95 else ('NUMBER-DIFF' if numd else 'WORDING-DIFF')
    if status == 'NUMBER-DIFF': nums_bad += 1
    rows.append((e['line'], e['kind'], e['title'][:40], status, round(sm.ratio(), 2), 'P2 L%d %s' % (p['line'], p['title'][:30]), ' | '.join(diffs)[:280]))
from collections import Counter
c = Counter(r[3] for r in rows)
print('mapped %d of %d; by status: %s' % (mapped, len(E), dict(c)))
for r in rows:
    if r[3] in ('SAME', 'NO-MATCH'): continue
    print('  early L%-5d %-11s %-34s %-12s r=%.2f -> %s' % (r[0], r[1][:11], r[2][:34], r[3], r[4], r[5]))
    print('        ', r[6][:250])
if OUT:
    with open(OUT, 'w', newline='') as f:
        w = csv.writer(f, delimiter='\t'); w.writerow(['early_line', 'kind', 'title', 'status', 'ratio', 'paper2_match', 'diff']); w.writerows(rows)
