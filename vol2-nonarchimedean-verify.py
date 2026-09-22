#!/usr/bin/env python3
"""
Non-Archimedean Contact Geometry -- verify script for vol2-nonarchimedean.html.

This page is a first-draft RESEARCH PROPOSAL, not a settled result, and its own text
already tags every claim (T)/(S)/(C). This script does not try to erase that honesty --
it can only check what a standard-library script can check:

[1] the wedge-power identity alpha_0 ^ (dalpha_0)^n = n! . dz^dx_1^dy_1^...^dx_n^dy_n,
    computed symbolically over Q (exact fractions.Fraction arithmetic, no floats) for
    n = 1..4. This is the field-independent algebraic fact the page's Part II rests on --
    it is checked here as a characteristic-0 identity, which is what the page itself
    claims it is ("an identity in the exterior algebra over any commutative ring"). This
    does NOT verify p-adic analytic convergence and does not touch the paper's genuinely
    open step (Part III, Step 2) -- that gap is real and this script cannot close it.

[2] the Reeb vector field equations on the standard model, R = d/dz: alpha_0(R) = 1 and
    the interior product iota_R(dalpha_0) = 0, via the same exterior-algebra engine.

[3] the five external arXiv citations this draft leans on. This session fetched each one
    directly (arxiv.org abstract/HTML pages) and independently web-searched the one whose
    PDF returned no machine-readable text. The titles and author lists recorded below are
    what was actually found live, not assumed -- see the comment above CITATIONS. This
    script cannot re-run that search (standard library only, no network per repo policy);
    it can only check that the chapter file cites the same ids/titles it was checked
    against. It does NOT verify the mathematical CONTENT of arXiv:2508.15443 (the p-adic
    Moser lemma) -- that is exactly OP1 in the chapter, named as open there too.

[4] that the chapter file actually carries its own T/S/C tags, the four open problems, and
    the specific named gap in Part III -- so the honesty apparatus described above isn't
    just asserted in this docstring but present on the page a reader will see.

Standard library only. python3 vol2-nonarchimedean-verify.py
"""

import os, re, sys
from fractions import Fraction

fails = []
def check(ok, msg, detail=''):
    print('    %s  %s%s' % ('PASS' if ok else 'FAIL', msg, ('  -- ' + detail) if detail and not ok else ''))
    if not ok: fails.append(msg)
def head(n, t):
    print('\n' + '=' * 72 + '\n  [%s]  %s\n' % (n, t) + '=' * 72)

HERE = os.path.dirname(os.path.abspath(__file__))
CHAPTER = os.path.join(HERE, 'vol2-nonarchimedean.html')

# ==========================================================================
# A tiny exact exterior-algebra engine: a k-form is a dict {sorted index-tuple: Fraction}.
# Basis index convention on (Q_p)^(2n+1): 0 = z, then for i=1..n: 2i-1 = x_i, 2i = y_i.
# This puts the canonical top-form in index order (z, x_1, y_1, ..., x_n, y_n), matching
# the page's own dz ^ dx_1 ^ dy_1 ^ ... ^ dx_n ^ dy_n.

def idx_z(): return 0
def idx_x(i): return 2 * i - 1
def idx_y(i): return 2 * i

def sort_sign(lst):
    arr = list(lst)
    swaps = 0
    for i in range(len(arr)):
        for j in range(len(arr) - 1 - i):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swaps += 1
    return (Fraction(-1) if swaps % 2 else Fraction(1)), tuple(arr)

def wedge(A, B):
    out = {}
    for ka, va in A.items():
        for kb, vb in B.items():
            if set(ka) & set(kb):
                continue  # repeated basis index -> zero, e.g. dx_i ^ dx_i = 0
            sign, key = sort_sign(list(ka) + list(kb))
            out[key] = out.get(key, Fraction(0)) + va * vb * sign
    return {k: v for k, v in out.items() if v != 0}

def wedge_power(form, n):
    result = dict(form)
    for _ in range(n - 1):
        result = wedge(result, form)
    return result

def contract(form, v_idx):
    """iota_v of a k-form, v = the basis vector dual to index v_idx."""
    out = {}
    for k, v in form.items():
        if v_idx not in k:
            continue
        p = k.index(v_idx)
        rest = k[:p] + k[p + 1:]
        sign = Fraction(-1) ** p
        out[rest] = out.get(rest, Fraction(0)) + v * sign
    return {k: v for k, v in out.items() if v != 0}

def factorial(n):
    r = 1
    for i in range(2, n + 1):
        r *= i
    return r

# ==========================================================================
head(1, "THE WEDGE-POWER IDENTITY, n = 1..4, EXACT ARITHMETIC")
print("  alpha_0 = dz - sum y_i dx_i on (Q_p)^(2n+1). dalpha_0 = sum dx_i ^ dy_i has")
print("  CONSTANT coefficients (the y_i dependence is exact and disappears under d), so it")
print("  is represented directly. The dx_i term of alpha_0 carries a coefficient that is a")
print("  FUNCTION (y_i), not a constant -- but the page's own claim is a purely structural")
print("  one (repeated-index cross terms vanish), so a nonzero placeholder coefficient (-1)")
print("  is used for that term: it tests exactly the structural claim being made, and no")
print("  more.\n")

for n in range(1, 5):
    dalpha0 = {}
    for i in range(1, n + 1):
        key_tuple = tuple(sorted((idx_x(i), idx_y(i))))
        dalpha0[key_tuple] = Fraction(1)
    dalpha0_n = wedge_power(dalpha0, n)

    expected_top_key = tuple(sorted([idx_x(i) for i in range(1, n + 1)] + [idx_y(i) for i in range(1, n + 1)]))
    check(set(dalpha0_n.keys()) == {expected_top_key},
          'n=%d: (dalpha_0)^n has exactly one nonzero basis term' % n,
          'got keys %s' % list(dalpha0_n.keys()))
    coeff = dalpha0_n.get(expected_top_key, Fraction(0))
    check(coeff == factorial(n),
          'n=%d: (dalpha_0)^n coefficient equals n! = %d' % (n, factorial(n)),
          'got %s' % coeff)

    alpha0 = {(idx_z(),): Fraction(1)}
    for i in range(1, n + 1):
        alpha0[(idx_x(i),)] = Fraction(-1)   # placeholder for -y_i; see note above

    full = wedge(alpha0, dalpha0_n)
    expected_full_key = tuple(sorted([idx_z()] + list(expected_top_key)))
    check(set(full.keys()) == {expected_full_key},
          'n=%d: alpha_0 ^ (dalpha_0)^n has exactly one nonzero basis term (the dx_i terms cancel structurally)' % n,
          'got keys %s' % list(full.keys()))
    fcoeff = full.get(expected_full_key, Fraction(0))
    check(fcoeff == factorial(n),
          'n=%d: alpha_0 ^ (dalpha_0)^n coefficient equals n! = %d (nowhere-vanishing, all p)' % (n, factorial(n)),
          'got %s' % fcoeff)
    print('      n=%d:  (dalpha_0)^%d = %d . e_%s   |   alpha_0^(dalpha_0)^%d = %d . e_%s'
          % (n, n, factorial(n), expected_top_key, n, factorial(n), expected_full_key))

# ==========================================================================
head(2, "THE REEB VECTOR FIELD ON THE STANDARD MODEL, R = d/dz")
n = 3
dalpha0 = {tuple(sorted((idx_x(i), idx_y(i)))): Fraction(1) for i in range(1, n + 1)}
alpha0 = {(idx_z(),): Fraction(1)}
for i in range(1, n + 1):
    alpha0[(idx_x(i),)] = Fraction(-1)  # placeholder, see [1]

alpha0_R = contract(alpha0, idx_z())
check(alpha0_R == {(): Fraction(1)} or alpha0_R == {},
      'alpha_0(R) picks out only the dz term',
      'got %s' % alpha0_R)
# contract() drops the empty tuple only if its coefficient were 0; here it must be 1
check(alpha0_R.get((), Fraction(0)) == Fraction(1), 'alpha_0(d/dz) = 1', 'got %s' % alpha0_R)

dalpha0_R = contract(dalpha0, idx_z())
check(dalpha0_R == {}, 'iota_(d/dz)(dalpha_0) = 0 identically (dalpha_0 involves only dx_i, dy_i)',
      'got %s' % dalpha0_R)

print('      alpha_0(d/dz) = 1                 : PASS above')
print('      iota_(d/dz)(dalpha_0) = 0          : PASS above')
print('      -> matches this series\' real-contact toy model, alpha = dz - r^2 dtheta, Reeb = d/dz')

# ==========================================================================
head(3, "THE FIVE EXTERNAL CITATIONS -- CHECKED LIVE THIS SESSION, RECORDED HERE")
print("  Fetched directly from arxiv.org (abstract and/or HTML pages) or, where the PDF had")
print("  no machine-readable text (2508.15443), cross-checked by web search against an")
print("  independent index (results included the exact title line as typeset on the PDF).")
print("  This script cannot re-run that search (no network, stdlib only) -- it checks only")
print("  that the chapter file cites the SAME ids and titles that were actually checked.\n")

# (arxiv_id, title substring as confirmed, authors substring as confirmed)
CITATIONS = [
    ("2406.18415", "p-adic Jaynes", "Crespo"),
    ("2505.07663", "Rigidity and flexibility in p-adic symplectic geometry", "Crespo"),
    ("2512.15575", "Group actions on p-adic symplectic manifolds", None),
    ("2508.15443", "Darboux", "Crespo"),
    ("2501.14444", "Weierstrass", None),
]

if not os.path.exists(CHAPTER):
    check(False, 'vol2-nonarchimedean.html present next to this script', CHAPTER)
    raw = ''
else:
    raw = open(CHAPTER, encoding='utf-8').read()

for arxiv_id, title_frag, author_frag in CITATIONS:
    check(arxiv_id in raw, 'chapter cites arXiv:%s' % arxiv_id)
    if title_frag:
        check(title_frag.lower() in raw.lower(), 'chapter carries the confirmed title fragment "%s" for %s' % (title_frag, arxiv_id))
    if author_frag:
        check(author_frag in raw, 'chapter credits %s for %s' % (author_frag, arxiv_id))

check('2508.15443' in raw and ('not verified' in raw.lower() or 'not been checked' in raw.lower() or 'not verified line-by-line' in raw.lower()),
      'the one citation whose CONTENT is unverified (2508.15443, the Moser lemma) is explicitly flagged as such, not silently used as settled')

# ==========================================================================
head(4, "THE HONESTY APPARATUS IS ON THE PAGE, NOT JUST IN THIS DOCSTRING")
for tag in ('[T]', '[S]', '[C]'):
    check(tag in raw, 'chapter carries the %s tag' % tag)
for op in ('OP1', 'OP2', 'OP3', 'OP4'):
    check(op in raw, 'chapter states open problem %s' % op)
check('gap' in raw.lower() and 'crespo' in raw.lower() and 'moser' in raw.lower(),
      'the Part III gap (Crespo-Pelayo Moser lemma, unverified) is named in the chapter, not just asserted to exist')
check('|\\lambda|_p' in raw or '|lambda|_p' in raw or '\\lambda|_p' in raw,
      'chapter states the p-adic contraction substitute |lambda|_p < 1')
for word in ('collatz', 'smoothness bridge', 'legendrian', 'reeb'):
    check(word in raw.lower(), 'chapter carries "%s"' % word)
OVERCLAIM = ['proves the p-adic darboux theorem', 'settles the collatz', 'proves collatz',
             'this establishes a non-archimedean dm3']
for phrase in OVERCLAIM:
    check(phrase not in raw.lower(), 'chapter prose does not say "%s"' % phrase)

# ==========================================================================
print('\n' + '=' * 72)
if fails:
    print('  %d FAILED' % len(fails))
    for f in fails: print('    - ' + f)
    sys.exit(1)
print('  ALL CHECKS PASSED')
print('=' * 72)
print()
print('[HONESTY]')
print('  This script establishes: (a) the wedge-power and Reeb-field identities the page')
print('  calls (T) are correct as characteristic-0 exterior-algebra facts, checked with exact')
print('  rational arithmetic, not floats or numerical approximation; (b) the five external')
print('  arXiv citations this page leans on are real papers with the titles/authors recorded')
print('  above, as confirmed by live fetches and search this session -- but this script has')
print('  NOT independently re-verified that confirmation (no network access here) and has NOT')
print('  checked the mathematical content of arXiv:2508.15443\'s Moser-path construction line')
print('  by line -- that is exactly OP1 in the chapter, and it is still open. This script does')
print('  not, and cannot, establish that the proposed p-adic contact Darboux theorem is true,')
print('  that a p-adic dissipative dynamics exists, or that the Collatz obstruction is')
print('  resolvable. Those are exactly what the page itself tags (S) and (C).')
