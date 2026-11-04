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

print("[9] the held text: Lebl, Basic Analysis I, v6.3 (printed page = pdf page)")
import os, subprocess
flat = lambda t: re.sub(r"\s+", " ", t)
pdf = None
for c in ("~/Downloads", "~/mnt/Downloads", "."):
    q = Path(os.path.expanduser(c)) / "realanal.pdf"
    if q.is_file(): pdf = q; break
if pdf is None:
    print("  SKIP: realanal.pdf not found (pass-through; no claim made)")
else:
    L = subprocess.run(["pdftotext", "-layout", str(pdf), "-"], capture_output=True, text=True, timeout=150).stdout.split("\f")
    pg = lambda n: flat(L[n - 1])
    check("p.55: Theorem 2.1.10 (Monotone convergence theorem)", "Theorem 2.1.10 (Monotone convergence theorem)" in pg(55))
    check("p.88: Proposition 2.5.5, geometric series", "Proposition 2.5.5" in pg(88) and "geometric series" in pg(88))
    check("p.92: Proposition 2.5.13, nonnegative terms <=> partial sums bounded above", "Proposition 2.5.13" in pg(92) and "bounded above" in pg(92))
    check("p.93: Proposition 2.5.16 (Comparison test)", "Proposition 2.5.16 (Comparison test)" in pg(93))

print("[10] second held text: Thomson, Bruckner & Bruckner, Elementary Real Analysis, 2nd ed. 2008 (printed page = pdf page - 22)")
tbb = None
for c in ("~/Downloads", "~/mnt/Downloads", "."):
    q = Path(os.path.expanduser(c)) / "TBB-AllChapters-Landscape.pdf"
    if q.is_file(): tbb = q; break
if tbb is None:
    print("  SKIP: TBB-AllChapters-Landscape.pdf not found (no claim made)")
else:
    T = subprocess.run(["pdftotext", "-layout", "-f", "80", "-l", "170", str(tbb), "-"], capture_output=True, text=True, timeout=150).stdout.split("\f")
    tp = lambda n: flat(T[n + 22 - 80])
    check("p.68: Theorem 2.28 (Monotone Convergence Theorem)", "Theorem 2.28 (Monotone Convergence Theorem)" in tp(68))
    check("p.124: Example 3.12, sum 1/(k(k+1)) telescopes to 1", "Example 3.12" in tp(124) and "k(k + 1)" in tp(124))
    check("p.124: geometric series, |r| < 1 converges to 1/(1-r)", "Geometric Series" in tp(124) and "|r| < 1" in tp(124))
    check("p.132: monotonic sequence converges iff bounded, applied to nonnegative series", "convergent if and only if it is bounded" in tp(132))
    check("p.141: Direct Comparison Test I", "Direct Comparison Test I" in tp(141))

print("[11] third held text: Ross, Elementary Analysis, 2nd ed. 2013 (printed page = pdf page - 12)")
ross = None
for c in ("~/Downloads", "~/mnt/Downloads", "."):
    q = Path(os.path.expanduser(c)) / "RCmplx01_Ross.pdf"
    if q.is_file(): ross = q; break
if ross is None:
    print("  SKIP: RCmplx01_Ross.pdf not found (no claim made)")
else:
    R = subprocess.run(["pdftotext", "-layout", "-f", "60", "-l", "120", str(ross), "-"], capture_output=True, text=True, timeout=150).stdout.split("\f")
    rp = lambda n: flat(R[n + 12 - 60])
    check("p.57: 10.2 Theorem, all bounded monotone sequences converge", "10.2 Theorem" in rp(57) and "All bounded monotone sequences converge" in rp(57))
    check("p.96: geometric series Example 1 and nonnegative terms give an increasing sequence of partial sums", "geometric series" in rp(96) and "increasing sequence" in rp(96))
    check("p.98: 14.6 Comparison Test", "Comparison Test" in rp(98) and "14.6" in rp(98))


print("[12] second Lean file: Series2.lean (ratio test, alternating series test, Abel's lemma)")
src2f = Path(__file__).resolve().parent / "Series2.lean"
src2 = src2f.read_text(encoding="utf-8")
code2 = re.sub(r"/-.*?-/", "", src2, flags=re.S)
code2 = re.sub(r"--[^\n]*", "", code2)
names2 = ["dominated_by_geometric", "terms_tend_to_zero", "ratio_test_converges", "ratio_test_diverges",
          "alternating_series_test", "control_alternating_needs_limit_zero", "power_series_abel",
          "exp_series_converges_of_ne_zero"]
for n in names2:
    check(f"theorem {n} is declared", re.search(r"\btheorem\s+" + n + r"\b", code2) is not None)
check("no proof in Series2.lean uses sorry", re.search(r"\bsorry\b", code2) is None)
rep2 = Path(__file__).resolve().parent / "series2.axioms.txt"
if not rep2.is_file():
    print("  NOT YET RUN: series2.axioms.txt does not exist.")
else:
    l2 = [l for l in rep2.read_text(encoding="utf-8").splitlines() if l.startswith("'Book18Series2.")]
    check("the Series2 axiom report has one line per theorem", len(l2) == len(names2), f"{len(l2)} lines")
    check("no Series2 theorem line shows sorryAx", all("sorryAx" not in l for l in l2),
          "; ".join(l.split("'")[1] for l in l2 if "sorryAx" in l) or "")

print("[13] illustrations for the new tests (exact; NOT proofs, not in the Lean file)")
# ratio -> 1 is inconclusive: harmonic diverges, 1/(n+1)^2 converges, both have ratio -> 1
rat_h = [F(1, n + 2) / F(1, n + 1) for n in range(2000)]      # a_n = 1/(n+1)
rat_s = [F(1, (n + 2) ** 2) / F(1, (n + 1) ** 2) for n in range(2000)]  # a_n = 1/(n+1)^2
check("harmonic ratios (n+1)/(n+2) are below 1 and exceed 0.999 by n = 1999", rat_h[-1] > F(999, 1000) and rat_h[-1] < 1)
check("1/(n+1)^2 ratios are below 1 and exceed 0.998 by n = 1999", rat_s[-1] > F(998, 1000) and rat_s[-1] < 1)
H = lambda m: sum((F(1, i) for i in range(1, m + 1)), F(0))
check("harmonic H(2^k) >= 1 + k/2 for k = 0..14 (it diverges although the ratio tends to 1)",
      all(H(2 ** k) >= 1 + F(k, 2) for k in range(15)))
check("1/(n+1)^2 partial sums stay below 2 (it converges although the ratio tends to 1)",
      sum((F(1, (n + 1) ** 2) for n in range(5000)), F(0)) < 2)
# ratio test with a_n = x^n/n!: ratio |x|/(n+1) falls below r = (L+1)/2 = 1/2 for n >= 2|x| - 1
for x in (F(2), F(5), F(-7, 2)):
    ok = all(abs(x) / (n + 1) < F(1, 2) for n in range(int(2 * abs(x)) + 1, int(2 * abs(x)) + 60))
    check(f"x = {x}: the ratio |x|/(n+1) is below 1/2 from n = {int(2 * abs(x)) + 1} on", ok)
# n! |x|^n: ratio (n+1)|x| exceeds 1 for large n, so the terms do not tend to 0
check("n!*(3/2)^n: ratio (n+1)*3/2 > 1 from n = 0, terms increase", all(F(3, 2) * (n + 1) > 1 for n in range(0, 50)))
# alternating series: b_n = 1/(n+1): even partial sums decrease, odd increase, and they bracket the limit
def alt(n): return sum((F((-1) ** i, i + 1) for i in range(n)), F(0))
check("alternating harmonic: the even partial sums s(2k) increase and the odd ones s(2k+1) decrease for k = 1..200",
      all(alt(2 * k + 2) > alt(2 * k) and alt(2 * k + 3) < alt(2 * k + 1) for k in range(1, 200)))
check("alternating harmonic: s(2k+1) > s(2k) and the gap is exactly b(2k) = 1/(2k+1)",
      all(alt(2 * k + 1) - alt(2 * k) == F(1, 2 * k + 1) for k in range(1, 100)))
check("control: b = 1 gives partial sums 0,1,0,1,... (no limit)", [alt_c for alt_c in [sum((F((-1) ** i) for i in range(n)), F(0)) for n in range(8)]] == [0, 1, 0, 1, 0, 1, 0, 1])
# Abel's lemma: a_n = 1, x0 = 1 (bounded by M = 1), |x| = 9/10: terms |x|^n <= M * r^n with r = 9/10
check("Abel: a_n = 1, x0 = 1, M = 1, x = 9/10: |a_n x^n| <= M r^n with r = max(|x/x0|, 1/2) = 9/10",
      all(abs(F(9, 10) ** n) <= F(9, 10) ** n for n in range(60)))

print("[14] the held texts, second pass: ratio test, alternating series test")
if pdf is not None:
    check("Lebl p.96: Proposition 2.5.19 (Ratio test), with a convergence case and a divergence case", "Proposition 2.5.19 (Ratio test)" in pg(96) and "converges absolutely" in pg(96) and "diverges" in pg(96))
    check("Lebl p.97: Example 2.5.20, a series settled by the ratio test", "Example 2.5.20" in pg(97) and "ratio test" in pg(97))
    check("Lebl p.101: Proposition 2.6.2 (Alternating series)", "Proposition 2.6.2 (Alternating series)" in pg(101))
if tbb is not None:
    T2 = subprocess.run(["pdftotext", "-layout", "-f", "165", "-l", "190", str(tbb), "-"], capture_output=True, text=True, timeout=150).stdout.split("\f")
    tp2 = lambda n: flat(T2[n + 22 - 165])
    check("TBB p.147: 3.28 (Ratio Test), limit < 1", "3.28 (Ratio Test)" in tp2(147))
    check("TBB p.148: ratio limit L > 1 gives divergence", "If L > 1" in tp2(148) and "divergent" in tp2(148))
    check("TBB p.162: 3.6.12 Alternating Series Test", "Alternating Series Test" in tp2(162))
if ross is not None:
    check("Ross p.99: 14.8 Ratio Test, (i) converges absolutely, (ii) diverges", "14.8 Ratio" in rp(99) and "converges absolutely" in rp(99) and "diverges if lim inf" in rp(99))
    check("Ross p.108: 15.3 Alternating Series Theorem", "15.3 Alternating Series Theorem" in rp(108))
print("  Abel's lemma (bounded at x0 => converges for |x| < |x0|): no matching statement located in the held texts; NOT page-checked.")

print("[HONESTY]")
print("  This script checks arithmetic and the text of two files. It does not run Lean; the axiom report is the author's run.")
print("  geom_series_converges and bounded_monotone_converges are proved in Lean by Mathlib's own lemmas, not from scratch.")
print("  [7] is an illustration; the Lean file does not prove that nonnegativity is necessary.")
print("  Series2.lean was compiled once by the author (7 of 8 theorems clean; the exponential-series theorem failed and was fixed in source, not recompiled), so the [12] check reports a FAIL until it is recompiled; [13] are exact illustrations, not proofs. Root test, radius of convergence and Taylor are not covered.")
print("  Held texts: Lebl, Thomson-Bruckner-Bruckner and Ross (Springer-copyrighted; page references only, nothing copied). Lebl, Basic Analysis I v6.3 (CC BY-NC-SA). [9] checks only that the four cited statements sit on the cited pages;")
print("  it does not check that the chapter's wording matches Lebl line by line, and nothing is copied from him.")
print()
print("0 FAIL" if not FAIL else f"{len(FAIL)} FAIL: {FAIL}")
sys.exit(1 if FAIL else 0)
