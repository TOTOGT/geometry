#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Pablo Nogueira Grossi / G6 LLC
"""
index-verify.py -- verify script for collab/pinot-orthogonal-quivers/index.html (R6).

Primary source: V. Pinot, "Quiver varieties for affine orthogonal quivers",
arXiv:2609.39434 (30 Sep 2026), Theorem 1.2, Lemmas 3.27-3.28, p. 18.

Blocks, one per claim the page makes:
  [1] weights of x = det C3, y = tr(C1C2), z = tr(C1C2C3) in the two D~ rows; the printed
      (D~_{2n-1}, a) relation misses weighted homogeneity by exactly 2; the corrected term
      z x^(n-1) is homogeneous                                              (standard library)
  [2] the only monomials of degree 4L+8 are the four the page lists       (standard library)
  [3] Milnor-Orlik: mu = prod(d/w_i - 1) = L + 3, so the types are D_{2n-2} and D_{2n-1}
                                                                           (standard library)
  [4] group orders of the corrected table and the index-2 table at 2-delta (standard library)
  [5] Seifert data: chi_orb(base) = 2/|Gamma-bar| for Z_m and BD_4k       (standard library)
  [6] the numerical relations recorded in verify_Dtilde_relation_numeric.out: one relation per
      row, integer coefficients as printed on the page, sign -1 rows vanish (standard library;
      --full re-runs the computation, needs numpy, about ten minutes)
  [7] ring identities for the involutions iota_1, iota_2 (needs sympy; SKIP if absent)
  [8] sigma commutes with the quaternionic J; mu_R and mu_C land in k^b  (needs numpy; SKIP if absent)

Usage:  python3 index-verify.py          (blocks 1-8, block 6 from the saved output)
        python3 index-verify.py --full   (block 6 recomputed)
"""
import os, re, subprocess, sys
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPTS = os.path.join(HERE, "scripts")
FAIL, SKIP = [], []

def check(label, ok, detail=""):
    print(f"  {'PASS' if ok else 'FAIL'}  {label}" + (f"  ({detail})" if detail else ""))
    if not ok:
        FAIL.append(label)

def skip(label, why):
    print(f"  SKIP  {label}  ({why})")
    SKIP.append(label)

NS = range(3, 41)
wts = lambda L: (4, 2 * L + 2, 2 * L + 4)
deg = lambda L: 4 * L + 8
Lv = lambda n: 2 * n - 5          # (D~_{2n-2}, v), Pinot p. 18
La = lambda n: 2 * n - 4          # (D~_{2n-1}, a)

print("[1] weights and homogeneity, n = 3..40")
ok_v = ok_a = ok_az = True
for n in NS:
    wx, wy, wz = wts(Lv(n))
    ok_v &= (n - 1) * wx + wy == deg(Lv(n)) == 2 * wz == wx + 2 * wy
    wx, wy, wz = wts(La(n))
    ok_a &= deg(La(n)) - ((n - 1) * wx + wy) == 2           # printed x^(n-1) y misses by 2
    ok_az &= (n - 1) * wx + wz == deg(La(n)) == (2 * n - 2) * wx
check("v-row: z^2, x y^2, x^(n-1) y all of degree 4L+8", ok_v)
check("a-row: printed term x^(n-1) y has degree 4L+6, two short", ok_a)
check("a-row: z x^(n-1) and x^(2n-2) have degree 4L+8", ok_az)

print("[2] all monomials of degree 4L+8")
def mons(L):
    wx, wy, wz = wts(L); d = deg(L)
    return sorted((a, b, c) for a in range(d // wx + 1) for b in range(d // wy + 1)
                  for c in range(d // wz + 1) if a * wx + b * wy + c * wz == d)
ok_v = all(mons(Lv(n)) == sorted([(0, 0, 2), (1, 2, 0), (n - 1, 1, 0), (2 * n - 3, 0, 0)]) for n in NS if n >= 4)
# n = 3: weights (4,4,6), so y^3 is admissible too; the relation is z^2 + binary cubic c(x,y).
# Found 2026-10-05 by this block: the first draft of the page listed four monomials for all n.
ok_v3 = mons(Lv(3)) == sorted([(0, 0, 2), (0, 3, 0), (1, 2, 0), (2, 1, 0), (3, 0, 0)])
ok_a = all(mons(La(n)) == sorted([(0, 0, 2), (n - 1, 0, 1), (1, 2, 0), (2 * n - 2, 0, 0)]) for n in NS)
check("v-row, n >= 4: exactly z^2, x y^2, x^(n-1) y, x^(2n-3)", ok_v)
check("v-row, n = 3: z^2 and the four cubic monomials x^3, x^2 y, x y^2, y^3", ok_v3)

print("[3] Milnor-Orlik number")
ok = True
for n in NS:
    for L, m in ((Lv(n), 2 * n - 2), (La(n), 2 * n - 1)):
        d = deg(L); mu = F(1)
        for w in wts(L):
            mu *= F(d, w) - 1
        ok &= mu == L + 3 == m
check("mu = L+3 = 2n-2 (v-row) and 2n-1 (a-row) for n = 3..40", ok)
check("printed D_{n+1} agrees with D_{2n-2} only at n = 3",
      [n for n in NS if n + 1 == 2 * n - 2] == [3])
check("printed D_{n+1} never agrees with D_{2n-1} for n >= 3",
      [n for n in NS if n + 1 == 2 * n - 1] == [])

print("[4] group orders")
bd = lambda m: 4 * (m - 2)          # |BD| for type D_m
check("|Gamma| = 8(n-2) and 4(2n-3) in the corrected D~ rows",
      all(bd(2 * n - 2) == 8 * (n - 2) and bd(2 * n - 1) == 4 * (2 * n - 3) for n in NS))
idx = all([(4 * n - 2) // (2 * n - 1), (4 * n) // (2 * n), bd(n + 2) // (2 * n), (2 * n) // (2 * n)] == [2, 2, 2, 1]
          and bd(n + 2) == 4 * n for n in range(2, 41))
check("2-delta table: indices 2, 2, 2, 1 against Z_{2n-1}, Z_2n, Z_2n, Z_2n", idx)

print("[5] Seifert data")
chi = lambda cones: 2 - sum(1 - F(1, a) for a in cones)
ok = all(chi((m, m) if m % 2 else (m // 2, m // 2)) == F(2, m if m % 2 else m // 2) for m in range(2, 200))
ok &= all(chi((2, 2, k)) == F(2, 2 * k) for k in range(2, 200))
check("chi_orb(base) = 2/|Gamma-bar|: S^2(m,m), S^2(m/2,m/2), S^2(2,2,k)", ok)

print("[6] numerical relations (saved output)" + (" -- recomputing" if "--full" in sys.argv else ""))
out_path = os.path.join(SCRIPTS, "verify_Dtilde_relation_numeric.out")
if "--full" in sys.argv:
    try:
        text = subprocess.run([sys.executable, os.path.join(SCRIPTS, "verify_Dtilde_relation_numeric.py")],
                              capture_output=True, text=True, timeout=3600).stdout
    except Exception as e:
        text = ""; check("re-run of verify_Dtilde_relation_numeric.py", False, str(e))
else:
    text = open(out_path, encoding="utf-8").read() if os.path.exists(out_path) else ""
check("saved output present", bool(text))
blocks = re.split(r"\n(?=\(D~_)", "\n" + text)
def terms(block):
    m = re.search(r"relation: (.*)", block)
    if not m: return None
    t = {}
    for c, a, b, cc in re.findall(r"\(([+-][\d.]+)[+-][\d.]+i\) x\^(\d+) y\^(\d+) z\^(\d+)", m.group(1)):
        if abs(float(c)) > 1e-3: t[(int(a), int(b), int(cc))] = round(float(c))
    return t
seen = 0
for blk in blocks:
    h = re.match(r"\(D~_(\d+), (a|v)\)(?:, s=([+-]1))?, n=(\d+)", blk)
    if not h: continue
    row, s, n = h.group(2), h.group(3), int(h.group(4))
    if s == "-1":
        check(f"(D~_{2*n-1}, a), sign -1, n={n}: all invariants vanish", "all invariants vanish" in blk); seen += 1; continue
    sv = re.search(r"singular value \(relative\): ([\d.e+-]+) / ([\d.e+-]+)", blk)
    gap = sv and float(sv.group(1)) < 1e-7 and float(sv.group(2)) > 1e-2
    t = terms(blk)
    if row == "a":
        want = {(0, 0, 2): 1, (1, 2, 0): 1, (n - 1, 0, 1): (-1) ** n}   # z^2 = z(-x)^(n-1) - x y^2
    else:
        want = {(0, 0, 2): 1, (1, 2, 0): 1, (n - 1, 1, 0): (-1) ** (n + 1)}   # z^2 = -y(-x)^(n-1) - x y^2
    if row == "v" and n == 3 and t:
        cubic = [t.get(k, 0) for k in ((3, 0, 0), (2, 1, 0), (1, 2, 0), (0, 3, 0))]   # x^3, x^2y, xy^2, y^3
    check(f"({'D~_%d, a' % (2*n-1) if row == 'a' else 'D~_%d, v' % (2*n-2)}), n={n}: one relation, as printed on the page",
          bool(gap) and t == want, f"found {t}")
    seen += 1
a_, b_, c_, d_ = cubic if 'cubic' in globals() else (0, 0, 0, 0)
disc = b_*b_*c_*c_ - 4*a_*c_**3 - 4*b_**3*d_ - 27*a_*a_*d_*d_ + 18*a_*b_*c_*d_
check("(D~_4, v): the computed binary cubic has non-zero discriminant (three distinct factors, so D_4)",
      disc != 0, f"cubic coefficients {cubic if 'cubic' in globals() else None}, discriminant {disc}")
check("all eight computed cases present (a: n=3,4,5; v: n=3,4,5; sign -1: n=3,4)", seen == 8, f"{seen} seen")

print("[7] ring identities for iota_1, iota_2")
try:
    import sympy as sp
    u, v = sp.symbols("u v"); ok = True
    for m in range(2, 12):
        X, Y, Z = u**m, v**m, u*v
        ok &= sp.expand(X**2 * Y**2 - Z**(2 * m)) == 0
        if m % 2 == 0:
            n = m // 2
            ok &= sp.expand((Z * (X - Y))**2 - (Z**2 * (X + Y)**2 - 4 * Z**(2 * (n + 1)))) == 0
    check("A_{m-1}/iota_1 = A_{2m-1} and A_{2n-1}/iota_2 = D_{n+2} relations, m <= 11", bool(ok))
except ImportError:
    skip("ring identities", "sympy not installed; run scripts/verify_2delta_index2.py where it is")

print("[8] quaternionic SRep")
try:
    import numpy  # noqa: F401
    r = subprocess.run([sys.executable, os.path.join(SCRIPTS, "verify_quaternionic_SRep.py")],
                       capture_output=True, text=True, timeout=300)
    vals = [float(x) for x in re.findall(r"([\d.]+e[+-]\d+)", r.stdout)]
    check("sigma∘J = J∘sigma, J(SRep) ⊂ SRep, mu_C and mu_R in k^b (both signs)",
          r.returncode == 0 and len(vals) == 8 and max(vals) < 1e-12, f"max residual {max(vals) if vals else 'n/a'}")
except ImportError:
    skip("quaternionic SRep", "numpy not installed")

print("""
[HONESTY]
What this establishes: the arithmetic behind the corrected D~ labels (weights, the complete
list of admissible monomials, the Milnor-Orlik number L+3), the group orders and Seifert
identities, and that the saved numerical run found exactly one relation per row with the
integer coefficients the page prints, for n = 3, 4, 5. Blocks 7 and 8 confirm two identities
used in the proofs.

What it does not establish: the numerical relations are evidence for n = 3, 4, 5, not a proof
for all n; Theorem A rests on Li's closed immersion applying to Pinot's unframed setting, which
nobody has checked; Conjecture C (the 2-delta surfaces are quotients by an involution) is open;
nothing here checks Pinot's Remark 2.15 or any geometric statement about links. Peer review:
none. V. Pinot has agreed to read the draft; his reply has not arrived.""")
print(f"\n{len(FAIL)} FAIL, {len(SKIP)} SKIP")
sys.exit(1 if FAIL else 0)
