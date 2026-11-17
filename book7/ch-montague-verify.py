#!/usr/bin/env python3
"""
Montague -- verifier for book7/ch-montague.html.

CHECKS (exhaustive, finite):
  1. A model with 3 men and 2 women; "loves" is any relation from men to women (2^6 = 64 relations).
     Quantifiers as functions on sets: every(P)(Q) = P subset of Q; a(P)(Q) = P and Q intersect.
     The two readings of "every man loves a woman", built compositionally:
        surface:  every(man)(lambda x. a(woman)(lambda y. loves(x,y)))
        inverse:  a(woman)(lambda y. every(man)(lambda x. loves(x,y)))
     are compared with the first-order sentences  forall x exists y  and  exists y forall x.
     Counts of relations satisfying each reading are printed.
  2. The inverse reading entails the surface reading on all 64 relations, and the converse fails on some.
  3. Conservativity (Barwise-Cooper): for every, a, no, exactly two, at least two and most, Q(A,B) = Q(A, A and B)
     for all pairs of subsets of a 4-element domain (256 pairs). Control: "only" (B subset of A) is NOT conservative.
  4. The page's counts equal the computed values.

DOES NOT ESTABLISH: that Montague's fragment of English, or any grammar, covers natural language; the historical
statements about Montague, which are CITED and were not checked.

    python3 book7/ch-montague-verify.py
"""
import itertools, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
fails = []
def check(ok, msg):
    print('    %s  %s' % ('PASS' if ok else 'FAIL', msg))
    if not ok: fails.append(msg)
def head(n, t): print('\n' + '=' * 70 + '\n  [%s]  %s\n' % (n, t) + '=' * 70)

MEN = ['m1', 'm2', 'm3']; WOMEN = ['w1', 'w2']
pairs = [(m, w) for m in MEN for w in WOMEN]
every = lambda P: lambda Q: all(Q(x) for x in P)
a_ = lambda P: lambda Q: any(Q(x) for x in P)

head(1, 'TWO READINGS OF "EVERY MAN LOVES A WOMAN" IN ALL 64 MODELS')
c_surf = c_inv = c_both = c_fo = 0; inv_implies_surf = True; converse_fails = False
for bits in itertools.product([0, 1], repeat=len(pairs)):
    loves = {p for p, b in zip(pairs, bits) if b}
    L = lambda x, y: (x, y) in loves
    surf = every(MEN)(lambda x: a_(WOMEN)(lambda y: L(x, y)))
    inv = a_(WOMEN)(lambda y: every(MEN)(lambda x: L(x, y)))
    fo_surf = all(any((x, y) in loves for y in WOMEN) for x in MEN)
    fo_inv = any(all((x, y) in loves for x in MEN) for y in WOMEN)
    assert surf == fo_surf and inv == fo_inv
    c_surf += surf; c_inv += inv; c_both += (surf and inv)
    if inv and not surf: inv_implies_surf = False
    if surf and not inv: converse_fails = True
print('    relations: 64   surface reading true in %d   inverse reading true in %d   both in %d   surface only in %d   neither in %d' % (c_surf, c_inv, c_both, c_surf - c_both, 64 - c_surf))
check(c_surf == 27 and c_inv == 15, 'counts are 27 (surface) and 15 (inverse), as inclusion-exclusion gives: (2^2-1)^3 = 27 and 2*2^3 - 1 = 15')
check(inv_implies_surf and c_both == c_inv, 'inverse reading entails surface reading on all 64 relations')
check(converse_fails and c_surf > c_inv, 'surface does not entail inverse: the two readings are different sentences')
check(c_surf - c_both == 12 and 64 - c_surf == 37, '12 relations make only the surface reading true; 37 make neither true')

head(2, 'CONSERVATIVITY OF SIMPLE QUANTIFIERS (4-ELEMENT DOMAIN)')
D = range(4)
subsets = [frozenset(s) for r in range(5) for s in itertools.combinations(D, r)]
quant = {
 'every': lambda A, B: A <= B, 'a': lambda A, B: bool(A & B), 'no': lambda A, B: not (A & B),
 'exactly two': lambda A, B: len(A & B) == 2, 'at least two': lambda A, B: len(A & B) >= 2,
 'most': lambda A, B: len(A & B) > len(A - B)}
for n, q in quant.items():
    check(all(q(A, B) == q(A, A & B) for A in subsets for B in subsets), '"%s" is conservative on all 256 pairs' % n)
only = lambda A, B: B <= A
check(not all(only(A, B) == only(A, A & B) for A in subsets for B in subsets), 'control: "only" is not conservative')

head(3, "THE PAGE'S COUNTS")
html = open(os.path.join(HERE, 'ch-montague.html'), encoding='utf-8').read()
m = re.search(r'data-surf="(\d+)" data-inv="(\d+)" data-both="(\d+)"', html)
check(bool(m) and tuple(map(int, m.groups())) == (c_surf, c_inv, c_both), 'page states counts %d, %d, %d' % (c_surf, c_inv, c_both))
for lab in ('CITED RESULT', 'CHECKED INSTANCE', 'OPEN QUESTION', 'THEOREM'):
    check(('<b>%s</b>' % lab) in html, 'visible evidence label %s present' % lab)
check('ch-montague-verify.py' in html, 'page names this verifier')
check('were not checked for this page' in html, 'page states which items were not checked')
check('href="ch-chomsky.html"' in html, 'link to ch-chomsky')
print('\n' + '=' * 70)
if fails:
    print('  %d CHECK(S) FAILED:' % len(fails)); [print('    - ' + f) for f in fails]; sys.exit(1)
print('  ALL CHECKS PASSED')
