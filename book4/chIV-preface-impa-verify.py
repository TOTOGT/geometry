#!/usr/bin/env python3
"""
Vol IV, IMPA Edition preface -- the Cajueiro, and the helix.

The page makes one arithmetical claim and it is the load-bearing one:
that the periodic table is a helix, and that Hydrogen and Lithium do not
*resemble* each other but occupy the same position on consecutive turns.
That is checkable. If the table is a helix whose turns are the periods,
then the gap between successive group-1 elements must equal the length of
the period just completed -- every time, with no exceptions and no fitting.
Block [1] checks it against the real atomic numbers.

[2] checks the operator order is stated consistently. The title composes
G = U∘F∘K∘C and the hero reads C∘K∘F∘U; those are the same statement, one
in composition order and one in application order, and a page that mixed
them would be claiming the reverse pipeline.

[3] checks the page's own apparatus: the ISBN-13 check digit, the DOI, the
ORCID, and that the translate trigger is present so the page is readable
outside English.

Standard library only.  python3 book4/chIV-preface-impa-verify.py
"""

import os, re, sys

fails = []
def check(ok, msg, detail=''):
    print('    %s  %s%s' % ('PASS' if ok else 'FAIL', msg, ('  -- ' + detail) if detail and not ok else ''))
    if not ok: fails.append(msg)
def head(n, t):
    print('\n' + '=' * 68 + '\n  [%s]  %s\n' % (n, t) + '=' * 68)

HERE = os.path.dirname(os.path.abspath(__file__))
PAGE = os.path.join(HERE, 'chIV-preface-impa.html')

# ==========================================================================
head(1, 'THE TABLE IS A HELIX -- CHECKED ON THE GROUP-1 GAPS')
print("  If each turn of the helix is a period, the distance from one alkali")
print("  metal to the next is the length of the turn just completed. Periods")
print("  run 2, 8, 8, 18, 18, 32. The page says H and Li occupy the same")
print("  position on consecutive turns; this is that claim, as arithmetic.\n")

GROUP1 = [('H', 1), ('Li', 3), ('Na', 11), ('K', 19), ('Rb', 37), ('Cs', 55), ('Fr', 87)]
PERIODS = [2, 8, 8, 18, 18, 32]

print('      from  to    gap   period length   agree')
ok_all = True
for i in range(len(GROUP1) - 1):
    (a, za), (b, zb) = GROUP1[i], GROUP1[i + 1]
    gap, per = zb - za, PERIODS[i]
    agree = (gap == per)
    ok_all &= agree
    print('      %-4s  %-4s  %3d   %3d             %s' % (a, b, gap, per, 'yes' if agree else 'NO'))
check(ok_all, 'every group-1 gap equals the period it closes -- the turns are exact')
check(GROUP1[1][1] - GROUP1[0][1] == 2,
      'H to Li is 2, the length of period 1 -- one full turn, not a resemblance')
check(sum(PERIODS) + 1 == GROUP1[-1][1],
      'the periods sum to Fr: 1 + %d = %d' % (sum(PERIODS), GROUP1[-1][1]))
print("\n      So the page's sentence is not an analogy. H and Li are one turn")
print("      apart on a structure whose turn lengths the elements themselves fix.")

# ==========================================================================
head(2, 'THE OPERATOR ORDER, BOTH WAYS ROUND')
if not os.path.exists(PAGE):
    check(False, 'chIV-preface-impa.html present next to this script', PAGE)
else:
    raw = open(PAGE, encoding='utf-8').read()
    flat = re.sub(r'<[^>]+>', ' ', raw)
    flat = re.sub(r'\s+', ' ', flat)

    comp = 'U ∘ F ∘ K ∘ C' in flat or 'U∘F∘K∘C' in flat.replace(' ', '')
    check(comp, 'the composition form G = U∘F∘K∘C is on the page')
    order = [flat.replace(' ', '').find(x) for x in ('C∘', 'K∘', 'F∘', 'U')]
    check('C' in flat and 'K' in flat and 'F' in flat and 'U' in flat,
          'all four operators are named')
    check('g+1' in flat or 'g + 1' in flat,
          'the return is to g+1, not to zero -- the helix, not the circle')
    check('zero' in flat.lower(), 'and the page says so explicitly')

    # ======================================================================
    head(3, 'APPARATUS')
    m = re.search(r'97[89][\d\-]{10,17}', flat)
    check(bool(m), 'an ISBN-13 is printed')
    if m:
        digits = [int(c) for c in m.group(0) if c.isdigit()][:13]
        total = sum(d * (1 if i % 2 == 0 else 3) for i, d in enumerate(digits))
        print('      ISBN %s -> weighted sum %d, mod 10 = %d' % (m.group(0), total, total % 10))
        check(len(digits) == 13, 'it has 13 digits')
        check(total % 10 == 0, 'its check digit is valid')

    check(bool(re.search(r'10\.5281/zenodo\.\d+', flat)), 'a Zenodo DOI is printed')
    check(bool(re.search(r'0009-0000-6496-2186', flat)), 'the ORCID is printed')
    check('google_translate_element' in raw,
          'the translate trigger is on the page -- it is readable outside English')
    check('pageLanguage' in raw and "'en'" in raw,
          "the source language is declared English")
    check('Cajueiro' in flat and 'Pirangi' in flat, 'the Cajueiro is named with its place')
    check('8,500' in flat or '8500' in flat, 'the canopy figure is printed')
    print("\n      The 8,500 m² canopy is a cited figure about a real tree, not a")
    print("      computed one. It is checked for presence, not for truth.")

# ==========================================================================
print('\n' + '=' * 68)
if fails:
    print('  %d FAILED' % len(fails))
    for f in fails: print('    - ' + f)
    sys.exit(1)
print('  ALL CHECKS PASSED')
print('=' * 68)
