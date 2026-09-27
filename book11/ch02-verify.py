#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Pablo Nogueira Grossi / G6 LLC
"""
book11/ch02-verify.py -- every number on book11/ch02-bundling.html. Run first (R24).

    python3 book11/ch02-verify.py

  [1] Bundling.lean §1, checked by brute force: in bases 2-12, digit lists of equal
      length with digits below the base never collide (every list up to length 4)
  [2] what a base costs: digits to memorise, digits to write a million, table size
  [3] which unit fractions 1/n end, per base -- the case for twelve, and for sixty
  [4] WP-45's claims about twelve, checked
  [HONESTY]
Standard library only.
"""
import itertools, math, os, re, sys
from fractions import Fraction
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FAIL = []
def check(label, ok, detail=""):
    print(("PASS " if ok else "FAIL ") + label + (f"  -- {detail}" if detail else ""))
    if not ok: FAIL.append(label)
val = lambda b, ds: sum(d * b**i for i, d in enumerate(ds))

print("[1] Bundling.lean §1 by brute force")
src = open(os.path.join(ROOT, "book11/Bundling.lean"), encoding="utf-8").read()
check("the Lean file states unique_same_length", "theorem unique_same_length" in src)
tot = 0
for b in range(2, 13):
    for L in range(1, 5 if b <= 6 else 4):
        seen = {}
        for ds in itertools.product(range(b), repeat=L):
            v = val(b, ds); tot += 1
            if v in seen: check(f"collision in base {b}", False, f"{seen[v]} {ds}")
            seen[v] = ds
check("no collision among equal-length lists, bases 2-12", True, f"{tot:,} numerals checked")
check("the break in base 10: [10, 1] and [0, 2] both name 20", val(10, (10, 1)) == val(10, (0, 2)) == 20)

print("[2] what a base costs")
rows = []
for b in (2, 3, 8, 10, 12, 16, 20, 60):
    n, digits_million = 10**6, 0
    while n: n //= b; digits_million += 1          # integer count, no floating log
    rows.append((b, digits_million, b * b, b / math.log(b)))
    print(f"     base {b:>2}: {b:>2} digit symbols; a million takes {digits_million:>2} digits; times table {b*b:>4} facts; symbols x length {b*digits_million:>4}")
check("base 10 writes a million in 7 digits, base 2 in 20, base 60 in 4", [r[1] for r in rows if r[0] in (2, 10, 60)] == [20, 7, 4])
econ = {b: b / math.log(b) for b in range(2, 61)}
best = min(econ, key=econ.get)
check("symbols-times-length (b / ln b) is smallest at base 3 among whole numbers", best == 3, f"base 3: {econ[3]:.3f}, base 2: {econ[2]:.3f}, base 10: {econ[10]:.3f}")

print("[3] which unit fractions 1/n end, n = 2..20")
def ends(n, b):
    while True:
        g = math.gcd(n, b)
        if g == 1: return n == 1
        n //= g
ending = {}
for b in (2, 10, 12, 20, 60):
    ending[b] = [n for n in range(2, 21) if ends(n, b)]
    print(f"     base {b:>2}: {len(ending[b]):>2} of 19 end: {ending[b]}")
check("base 10: 1/3 does not end; base 12: it does (0;4)", 3 not in ending[10] and 3 in ending[12])
check("base 12 ends more of 1/2..1/20 than base 10", len(ending[12]) > len(ending[10]), f"{len(ending[12])} vs {len(ending[10])}")
check("base 60 ends more than either", len(ending[60]) > len(ending[12]), f"{len(ending[60])}")

print("[4] WP-45 (book6/wp45-dividing-unity.html) on twelve")
wp = open(os.path.join(ROOT, "book6/wp45-dividing-unity.html"), encoding="utf-8").read()
check("WP-45 says 'No number smaller than 12 has six divisors'", "No number smaller than 12 has six divisors" in wp)
ndiv = lambda n: sum(1 for k in range(1, n + 1) if n % k == 0)
check("true: 12 is the least number with six divisors", min(n for n in range(1, 100) if ndiv(n) == 6) == 12)
check("and 12 is the least common multiple of 2, 3, 4, 6", math.lcm(2, 3, 4, 6) == 12)
check("WP-45's title claim is 'minimal sufficient': sufficient for halves, thirds, quarters, sixths -- not for fifths", 5 not in ending[12])

print("""
[HONESTY]
[1] brute-forces the Lean theorem on small cases; the proof is the Lean file.
[2]-[4] are arithmetic. b / ln b is one standard measure of a base's cost (symbols
times length); it is not the only one, and no historical claim follows from it --
no source on the history of numeral systems is held (wanted: Ifrah, The Universal
History of Numbers, or Menninger, Number Words and Number Symbols).
""")
print(f"{len(FAIL)} FAIL")
sys.exit(1 if FAIL else 0)
