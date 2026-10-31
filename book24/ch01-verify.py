#!/usr/bin/env python3
"""Book XXIV, Chapter 1 -- exact checks on the statements the chapter makes.

What this script checks (all in exact rational arithmetic, no floating point):
  A. For 2x2 integer matrices with entries in -3..3, "det != 0" agrees with
     "the only integer combination c1*v1 + c2*v2 = 0 with |c| <= 6 is c = 0".
     (A finite search, so it can only refute the equivalence, not prove it;
     the proof is in the chapter, section 2.)
  B. The witness the chapter names for the dependent case, (d,-c) or (b,-a)
     or (1,0), really is a nonzero combination giving zero when det = 0.
  C. The coordinate formulas c1=(w1*d-b*w2)/det, c2=(a*w2-c*w1)/det
     reconstruct w exactly, on every independent pair in the grid and a set
     of target vectors.
Each check has a control that must FAIL, so a silent pass of a broken check
is visible.  This script does not touch Lean and does not run the page's
JavaScript; it checks the mathematics the page states, not the page.
"""
from fractions import Fraction as F
from itertools import product
import sys

R = range(-3, 4)
C = range(-6, 7)

def det(a, b, c, d):
    return a * d - b * c

def combo_zero(a, b, c, d, c1, c2):
    # v1 = (a, c), v2 = (b, d)
    return c1 * a + c2 * b == 0 and c1 * c + c2 * d == 0

def has_nontrivial(a, b, c, d):
    return any((c1, c2) != (0, 0) and combo_zero(a, b, c, d, c1, c2)
               for c1 in C for c2 in C)

def witness(a, b, c, d):
    for cand in ((d, -c), (b, -a), (1, 0)):
        if cand != (0, 0):
            return cand
    return None

def coords(a, b, c, d, w1, w2, sign=1):
    D = det(a, b, c, d)
    return (F(w1 * d - b * w2, D), F(sign * (a * w2 - c * w1), D))

fails = 0
def check(name, ok):
    global fails
    print(("PASS  " if ok else "FAIL  ") + name)
    if not ok:
        fails += 1

# A
bad = [(a, b, c, d) for a, b, c, d in product(R, R, R, R)
       if (det(a, b, c, d) != 0) == has_nontrivial(a, b, c, d)]
check(f"A: det!=0 <=> only trivial combination, all {7**4} matrices", not bad)

# A control: a wrong criterion (trace instead of det) must disagree somewhere
bad_ctrl = [(a, b, c, d) for a, b, c, d in product(R, R, R, R)
            if ((a + d) != 0) == has_nontrivial(a, b, c, d)]
check("A control: 'trace != 0' is NOT the criterion (must disagree)", bool(bad_ctrl))

# B
okB = True
for a, b, c, d in product(R, R, R, R):
    if det(a, b, c, d) == 0:
        w = witness(a, b, c, d)
        if w is None:                      # zero matrix: (1,0) is the witness
            okB = False
        elif not combo_zero(a, b, c, d, *w):
            okB = False
        if w is not None and w == (1, 0) and (a, c) != (0, 0):
            okB = False                    # (1,0) is only allowed for v1 = 0
check("B: named witness gives a nonzero combination = 0 whenever det = 0", okB)
# B control: a witness (c, d) swapped must fail on some dependent matrix
ctrl = any(det(a, b, c, d) == 0 and (c, d) != (0, 0) and
           not combo_zero(a, b, c, d, c, d)
           for a, b, c, d in product(R, R, R, R))
check("B control: a wrong witness (c,d) fails on some dependent matrix", ctrl)

# C
targets = [(w1, w2) for w1 in range(-4, 5) for w2 in range(-4, 5)]
okC = True
for a, b, c, d in product(R, R, R, R):
    D = det(a, b, c, d)
    if D == 0:
        continue
    for w1, w2 in targets:
        c1, c2 = coords(a, b, c, d, w1, w2)
        if c1 * a + c2 * b != w1 or c1 * c + c2 * d != w2:
            okC = False
check("C: coordinate formulas reconstruct w exactly, all independent pairs", okC)
# C control: flipping a sign in c2 must break reconstruction somewhere
brk = False
for a, b, c, d in product(R, R, R, R):
    D = det(a, b, c, d)
    if D == 0:
        continue
    for w1, w2 in targets:
        c1, c2 = coords(a, b, c, d, w1, w2, sign=-1)
        if c1 * a + c2 * b != w1 or c1 * c + c2 * d != w2:
            brk = True
check("C control: a sign error in c2 is caught", brk)

print("\nALL CHECKS PASSED" if not fails else f"\n{fails} CHECK(S) FAILED")
sys.exit(1 if fails else 0)
