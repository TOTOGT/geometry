#!/usr/bin/env python3
"""
novelty_check.py -- the register may not say "novel", and may not leave a row blank.

A priority claim is only as good as the search behind it, so every row must carry
the search that produced its verdict. This enforces that, and it enforces the closed
verdict vocabulary, because the whole point of the scale is to stop a row collapsing
back into found / not-found.

    python3 tools/novelty_check.py
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REG  = os.path.join(os.path.dirname(HERE), 'docs', 'novelty-register.md')
VOCAB = {'KNOWN-EXACT', 'KNOWN-GENERAL', 'PRIOR-ART-CANDIDATE',
         'UNRESOLVED', 'UNMATCHED-LIMITED', 'UNMATCHED-BROAD'}
fails = []
def check(ok, msg, detail=''):
    print('    %s  %s%s' % ('PASS' if ok else 'FAIL', msg, ('  -- ' + detail) if detail and not ok else ''))
    if not ok: fails.append(msg)
def head(n, t):
    print('\n' + '=' * 70 + '\n  [%s]  %s\n' % (n, t) + '=' * 70)

src = open(REG, encoding='utf-8').read()
rows = [l for l in src.splitlines() if re.match(r'^\|\s*N\d\d\s*\|', l)]

head(1, 'THE ROWS PARSE, AND CARRY THEIR SEARCH')
print('  Columns: id | claim | stated in | verdict | terms | corpora | date | hits | disposition\n')
ok_all = True
for l in rows:
    c = [x.strip() for x in l.strip().strip('|').split('|')]
    rid = c[0] if c else '??'
    if len(c) != 9:
        print('     %-5s %d columns' % (rid, len(c))); ok_all = False; continue
    verdicts = [v.strip(' `') for v in c[3].split('/')]
    bad = [v for v in verdicts if v not in VOCAB]
    dated = re.match(r'^\d{4}-\d{2}-\d{2}$', c[6]) is not None
    filled = all(c[i] for i in (1, 2, 4, 5, 7, 8))
    print('     %-5s %-22s %-10s %s' % (rid, '/'.join(verdicts)[:22],
                                        c[6], 'ok' if not bad and dated and filled else 'PROBLEM'))
    if bad: print('           verdict not in vocabulary: %s' % bad); ok_all = False
    if not dated: print('           search date missing or malformed'); ok_all = False
    if not filled: print('           a required column is empty'); ok_all = False
check(len(rows) >= 1, 'the register has rows', str(len(rows)))
check(ok_all, 'every row parses, is dated, and names what was searched')

head(2, 'THE WORD THAT MAY NOT APPEAR')
verdict_col = ' '.join(l.strip().strip('|').split('|')[3] for l in rows).lower()
check('novel' not in verdict_col, 'no row carries "novel" as a verdict')
body_claims = re.findall(r'(?i)\b(?:is|are|remains?)\s+novel\b', src)
check(not body_claims, 'and the prose asserts novelty nowhere', str(body_claims[:3]))
check('A failed search is a fact about the search' in src,
      'the register states the rule it exists to enforce')

head(3, 'THE SCALE IS INTACT')
for v in sorted(VOCAB):
    check(v in src, 'vocabulary defines %s' % v)
check('patent' in src.lower(), 'the register says it is not a patent search')

head(4, 'CONTROL')
check(len(src) > 3000, 'the register was read and is not a stub', str(len(src)))
check(len(VOCAB) == 6, 'the vocabulary is the six-value scale, not a binary')
print('    A vacuous pass is a pass. Block [4] exists so that block [1] cannot')
print('    report every row well-formed by having found no rows.')

head('HONESTY', 'What this checks, and what it cannot.')
print("""
  ESTABLISHED. Every row is well-formed, carries a verdict from the closed
  vocabulary, a search date, the terms searched, the corpora searched, and an
  equation-level disposition; and the word "novel" appears in no verdict.

  NOT ESTABLISHED. That any search was adequate. This script cannot run a
  literature search, cannot judge whether the terms chosen were the right ones,
  and cannot tell a thorough pass from a lazy one. It checks that the claim is
  accompanied by its evidence, not that the evidence is good. A row reading
  UNMATCHED-BROAD with three bad search terms will pass here and be wrong in
  the world. The register is a discipline, not a proof of priority.
""")
print('=' * 70)
if fails:
    print('  %d CHECK(S) FAILED' % len(fails))
    for f in fails: print('    - ' + f)
    print('=' * 70); sys.exit(1)
print('  ALL CHECKS PASSED')
print('=' * 70)
