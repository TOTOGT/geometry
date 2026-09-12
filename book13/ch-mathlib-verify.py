#!/usr/bin/env python3
"""
Volume XIII -- the Mathlib claims, measured against the Mathlib that is here.

WHY THIS EXISTS. This volume's reason for being written first is not a
mathematical argument. It is a claim about the contents of a library: that
Mathlib has no K-theory, so Volume XI cannot have a machine-checked core, and
that CategoryTheory/ is large enough that Volume XIII's work is instantiation
rather than construction. Claims about a library go stale, and on 2026-09-12
three of the six numbers on the index page were wrong against the very tree the
page said it had measured -- 1113 for 1089, 48 for 44, 112 for 108 -- and the
page called CategoryTheory/ the deepest area in all of Mathlib when Algebra/ is
larger. None of it changed the argument, and nothing in the repository could
have told anyone.

WHAT IT CHECKS. It reads the numbers OUT OF index.html and compares them with a
count taken from the checkout. Editing the page without re-measuring fails; a
lake update that moves the tree fails. The two claims that carry the argument --
zero K-theory files, and a populated Bicategory/ and Quasicategory/ -- are
checked separately and named as load-bearing.

Standard library only.  python3 book13/ch-mathlib-verify.py
"""

import os, re, sys

HERE  = os.path.dirname(os.path.abspath(__file__))
REPO  = os.path.dirname(HERE)
ML    = os.path.join(REPO, '.lake', 'packages', 'mathlib', 'Mathlib')
fails = []

def check(ok, msg, detail=''):
    print('    %s  %s%s' % ('PASS' if ok else 'FAIL', msg, ('  -- ' + detail) if detail and not ok else ''))
    if not ok: fails.append(msg)

def head(n, t):
    print('\n' + '=' * 68 + '\n  [%s]  %s\n' % (n, t) + '=' * 68)

def count(rel):
    d = os.path.join(ML, rel)
    if not os.path.isdir(d): return None
    return sum(1 for _, _, fs in os.walk(d) for f in fs if f.endswith('.lean'))

# --------------------------------------------------------------------------
head(1, 'THE CHECKOUT IS THERE AND IS THE ONE THE PAGE MEANS')
print('  Mathlib: %s' % ML.replace(os.path.expanduser('~'), '~'))
check(os.path.isdir(ML), 'the Mathlib checkout exists')
if not os.path.isdir(ML):
    print('\n  Cannot measure. Nothing below is a result.'); sys.exit(1)

tc = os.path.join(REPO, '.lake', 'packages', 'mathlib', 'lean-toolchain')
tool = open(tc).read().strip() if os.path.exists(tc) else '(none)'
print('  toolchain: %s' % tool)
check(tool.endswith('v4.32.0'), 'toolchain is v4.32.0, as the series records', tool)

# --------------------------------------------------------------------------
head(2, 'THE PAGE SAYS N. THE TREE SAYS N.')
print('  Every number is read out of index.html, not hard-coded here.\n')

page = open(os.path.join(HERE, 'index.html'), encoding='utf-8').read()
flat = re.sub(r'<[^>]+>', ' ', page)
flat = re.sub(r'\s+', ' ', flat)

CLAIMS = [
    ('CategoryTheory/',                    'CategoryTheory',
     r'CategoryTheory/\s*is the second largest area in Mathlib\s*&mdash;?\s*(\d+)'),
    ('CategoryTheory/Bicategory/',         'CategoryTheory/Bicategory',
     r'with\s*(\d+)\s*under\s*Bicategory/'),
    ('CategoryTheory/Monoidal/',           'CategoryTheory/Monoidal',
     r'(\d+)\s*under\s*Monoidal/'),
    ('AlgebraicTopology/SimplicialSet/',   'AlgebraicTopology/SimplicialSet',
     r'(\d+)\s*under\s*AlgebraicTopology/SimplicialSet/'),
    ('AlgebraicTopology/Quasicategory/',   'AlgebraicTopology/Quasicategory',
     r'(\d+)\s*under\s*AlgebraicTopology/Quasicategory/'),
]

for label, rel, pat in CLAIMS:
    m = re.search(pat, flat)
    if not m:
        check(False, 'index.html states a count for %s' % label,
              'no number found -- did the sentence change?')
        continue
    claimed, actual = int(m.group(1)), count(rel)
    check(claimed == actual, '%-36s page %s = tree %s' % (label, claimed, actual),
          'page says %s, tree has %s' % (claimed, actual))

# the two comparison figures in the same sentence
for rel, pat in [('Algebra', r'behind\s*Algebra/\s*at\s*(\d+)'),
                 ('Analysis', r'ahead of\s*Analysis/\s*at\s*(\d+)')]:
    m = re.search(pat, flat)
    if not m:
        check(False, 'index.html states a count for %s/' % rel); continue
    check(int(m.group(1)) == count(rel), '%-36s page %s = tree %s'
          % (rel + '/', m.group(1), count(rel)),
          'page %s, tree %s' % (m.group(1), count(rel)))

# --------------------------------------------------------------------------
head(3, 'THE RANKING CLAIM')
print('  The page says CategoryTheory/ is second, behind Algebra/.')
print('  A superlative is the easiest thing in a corpus to get wrong.\n')

areas = sorted(((count(d), d) for d in os.listdir(ML)
                if os.path.isdir(os.path.join(ML, d))), reverse=True)
for n, d in areas[:5]:
    print('    %5d  %s' % (n, d))
check(areas[0][1] == 'Algebra',        'Algebra/ is the largest area',        areas[0][1])
check(areas[1][1] == 'CategoryTheory', 'CategoryTheory/ is the second largest', areas[1][1])
check('second largest area in Mathlib' in flat,
      'the page claims second, not deepest')
check('deepest area in all of Mathlib' not in flat,
      'the withdrawn superlative is gone from the page')

# --------------------------------------------------------------------------
head(4, 'THE TWO CLAIMS THAT CARRY THE ARGUMENT')
print('  Everything above is context. These two decide construction order.\n')

kt = [os.path.join(r, f).replace(ML + os.sep, '')
      for r, _, fs in os.walk(ML) for f in fs
      if f.endswith('.lean') and 'ktheory' in os.path.join(r, f).lower()]
check(len(kt) == 0,
      'Mathlib still contains zero K-theory files, so Volume XI has no core',
      '%d found: %s' % (len(kt), kt[:4]))
check(re.search(r'contains\s*zero\s*K-theory files', flat) is not None,
      'the page states the zero-K-theory claim')

bic, qc = count('CategoryTheory/Bicategory'), count('AlgebraicTopology/Quasicategory')
check(bic and bic > 0, 'Bicategory/ is populated -- the associator is available', str(bic))
check(qc and qc > 0,  'Quasicategory/ is populated -- Chapter 6 has a target', str(qc))

# --------------------------------------------------------------------------
head(5, 'CONTROL: THIS SCRIPT MEASURED SOMETHING')
check(count('CategoryTheory') > 500, 'the walk found a real CategoryTheory tree',
      str(count('CategoryTheory')))
check(len(areas) > 10, 'more than ten top-level areas were counted', str(len(areas)))
check(len(CLAIMS) == 5 and len(flat) > 2000, 'index.html was read and parsed')
print('    A vacuous pass is a pass. Block [5] exists so that block [2] cannot')
print('    report success by having matched nothing against nothing.')

# --------------------------------------------------------------------------
head('HONESTY', 'What this script establishes, and what it does not.')
print("""
  ESTABLISHED. That every number Volume XIII's index page asserts about Mathlib
  matches the Mathlib checked out beside it, that CategoryTheory/ is the second
  largest area and not the largest, and that the two facts the construction-order
  argument rests on still hold: no K-theory files exist, and Bicategory/ and
  Quasicategory/ do.

  NOT ESTABLISHED. That the results this volume needs are IN those files. A file
  count is a measure of a library's size, not of its fit to a purpose, and
  "every result this volume needs is already formalised" is a claim about
  content that no count can support -- it is discharged one lemma at a time,
  by name, and Chapter 7 is where that obligation lives. This script also says
  nothing about the mathematics: whether G = U F K k C is a composite of
  endofunctors at all is Chapter 2's open question, and Chapter 3 closed only
  the strict case.

  AND ONE THING WORTH KEEPING IN VIEW. Mathlib gains K-theory the day someone
  contributes it, and on that day this script fails and the volume's reading
  order stops being forced. That is the intended behaviour. The failure is the
  notification.
""")

print('=' * 68)
if fails:
    print('  %d CHECK(S) FAILED' % len(fails))
    for f in fails: print('    - ' + f)
    print('=' * 68); sys.exit(1)
print('  ALL CHECKS PASSED')
print('=' * 68)
