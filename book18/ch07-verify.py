#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Pablo Nogueira Grossi / G6 LLC
"""
book18/ch07-verify.py -- every number on book18/ch07-sequences-and-series.html. Run first.

    python3 book18/ch07-verify.py

All arithmetic is exact (fractions), so a PASS is an equality, not a rounding.

  [1] finite geometric sum: r^0 + ... + r^(n-1) = (r^n - 1)/(r - 1), r != 1
  [2] the error of the geometric partial sum is exactly |r|^n / |1 - r|, which is why it tends to 0
  [3] r = 1/2: the partial sums are 2 - 2^(1-n), below 2 and approaching it
  [4] a bounded monotone sequence, 1 - 1/(n+1): the N that works for a given epsilon
  [5] comparison: 1/(i+2)^2 <= 1/((i+1)(i+2)); the larger series telescopes to 1 - 1/(n+1)
  [6] control: the partial sums of the constant 1 exceed every bound
  [7] illustration (NOT a proof, and not in the Lean file): without nonnegativity, bounded partial sums
      do not give convergence -- (-1)^n
  [8] the Lean file: the eight theorems are present, none is proved with sorry, and the axiom report
      shows no sorryAx
  [HONESTY]
"""
import re, sys
from fractions import Fraction as F
from math import ceil
from pathlib import Path
FAIL = []
def check(label, ok, detail=""):
    print(("PASS " if ok else "FAIL ") + label + (f"  -- {detail}" if detail else ""))
    if not ok: FAIL.append(label)

def S(a, n): return sum((a(i) for i in range(n)), F(0))

print("[1] finite geometric sum")
for r in (F(1, 2), F(-1, 3), F(3, 4), F(2), F(-5, 2)):
    ok = all(S(lambda i: r ** i, n) == (r ** n - 1) / (r - 1) for n in range(0, 31))
    check(f"r = {r}: sum_(i<n) r^i = (r^n - 1)/(r - 1) for n = 0..30", ok)

print("[2] the error is |r|^n / |1 - r|")
for r in (F(1, 2), F(-1, 3), F(3, 4), F(-9, 10)):
    L = 1 / (1 - r)
    ok = all(abs(S(lambda i: r ** i, n) - L) == abs(r) ** n / abs(1 - r) for n in range(0, 41))
    check(f"r = {r}: |S_n - 1/(1-r)| = |r|^n/|1-r| for n = 0..40", ok)
    eps = F(1, 10 ** 6)
    N = next(n for n in range(0, 10 ** 4) if abs(r) ** n / abs(1 - r) < eps)
    ok2 = all(abs(r) ** n / abs(1 - r) < eps for n in range(N, N + 200))
    check(f"r = {r}: for eps = 1e-6 the error is below eps from N = {N} on (checked n = N..N+199)", ok2)

print("[3] r = 1/2")
h = F(1, 2)
check("S_n = 2 - 2^(1-n) for n = 1..40", all(S(lambda i: h ** i, n) == 2 - F(2) ** (1 - n) for n in range(1, 41)))
check("S_n < 2 for n = 0..40", all(S(lambda i: h ** i, n) < 2 for n in range(0, 41)))

print("[4] bounded monotone: s_n = 1 - 1/(n+1)")
s = lambda n: 1 - F(1, n + 1)
check("monotone increasing, n = 0..500", all(s(n) <= s(n + 1) for n in range(500)))
check("bounded above by 1", all(s(n) <= 1 for n in range(500)))
for eps in (F(1, 10), F(1, 1000), F(1, 10 ** 6)):
    N = ceil(1 / eps)
    check(f"eps = {eps}: from N = {N} on, |s_n - 1| < eps (checked N..N+999)", all(abs(s(n) - 1) < eps for n in range(N, N + 1000)))

print("[5] comparison: a_i = 1/(i+2)^2 <= b_i = 1/((i+1)(i+2))")
a = lambda i: F(1, (i + 2) ** 2); b = lambda i: F(1, (i + 1) * (i + 2))
check("0 <= a_i <= b_i for i = 0..2000", all(0 <= a(i) <= b(i) for i in range(2001)))
check("sum of b telescopes: S_n(b) = 1 - 1/(n+1), n = 0..300", all(S(b, n) == 1 - F(1, n + 1) for n in range(301)))
check("so S_n(a) <= S_n(b) <= 1 for n = 0..300", all(S(a, n) <= S(b, n) <= 1 for n in range(301)))

print("[6] control: constant 1")
check("S_n = n, so for M = 10, 1000, 10^6 the sum exceeds M at n = M + 1", all(S(lambda i: F(1), M + 1) > M for M in (10, 1000, 10 ** 6)))

print("[7] illustration only: (-1)^n has bounded partial sums and no limit")
T = lambda n: S(lambda i: F((-1) ** i), n)
check("partial sums stay in {0, 1}", all(T(n) in (0, 1) for n in range(200)))
check("consecutive partial sums differ by 1, so none can be within 1/4 of a common L (triangle inequality)",
      all(abs(T(n) - T(n + 1)) == 1 for n in range(200)))

print("[8] the Lean file")
here = Path(__file__).resolve().parent
src = (here / "Series.lean").read_text(encoding="utf-8")
rep = (here / "series.axioms.txt").read_text(encoding="utf-8")
code = re.sub(r"/-.*?-/", "", src, flags=re.S)
code = re.sub(r"--[^\n]*", "", code)
names = ["convergesTo_iff", "geom_partial_sum", "geom_series_converges", "bounded_monotone_converges",
         "nonneg_series_bounded_converges", "comparison_test", "control_constant_unbounded", "control_half_geometric"]
for n in names:
    check(f"theorem {n} is declared", re.search(r"\btheorem\s+" + n + r"\b", code) is not None)
check("no proof in the file uses sorry", re.search(r"\bsorry\b", code) is None)
lines = [l for l in rep.splitlines() if l.startswith("'Book18Series.")]
check("the axiom report has one line per theorem", len(lines) == len(names), f"{len(lines)} lines")
check("no theorem line shows sorryAx", all("sorryAx" not in l for l in lines))
check("each theorem line lists only propext, Classical.choice, Quot.sound",
      all(l.split("depends on axioms:")[1].strip() == "[propext, Classical.choice, Quot.sound]" for l in lines))

print("[HONESTY]")
print("  This script checks arithmetic and the text of two files. It does not run Lean; the axiom report is the author's run.")
print("  geom_series_converges and bounded_monotone_converges are proved in Lean by Mathlib's own lemmas, not from scratch.")
print("  [7] is an illustration; the Lean file does not prove that nonnegativity is necessary.")
print("  Held text: none. The chapter follows no page-addressed source yet.")
print()
print("0 FAIL" if not FAIL else f"{len(FAIL)} FAIL: {FAIL}")
sys.exit(1 if FAIL else 0)
