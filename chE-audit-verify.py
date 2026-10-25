#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""chE-audit-verify.py - audit script for chE-gtct.html (Book 3, Extended Chapter E).

Two parts, kept apart on purpose (A1-A6 math, B page guards).
  [A] MATH checks: numbers and linear algebra the chapter relies on. A failure here
      exits non-zero. These test the chapter's true claims AND the facts that
      contradict its Theorem 5 / Axiom 8 / Time sections.
  [B] PAGE checks: reads the page and reports internal contradictions as FINDING.
      Findings do not change the exit code; they are the audit's output and go
      away only when the page is edited.

Requires: standard library only.   Run: python3 chE-audit-verify.py
Principia Orthogona - Book 3 - G6 LLC - CC BY-NC-ND 4.0
"""
import html as H, math, random, re, sys
from pathlib import Path

PAGE = Path(__file__).resolve().parent / "chE-gtct.html"
FAIL, FINDINGS = [], []

def check(label, ok, detail=""):
    print(f"    {'PASS' if ok else 'FAIL'}  {label}" + (f"   {detail}" if detail else ""))
    if not ok: FAIL.append(label)

def finding(label, detail=""):
    print(f"    FINDING  {label}" + (f"   {detail}" if detail else ""))
    FINDINGS.append(label)

# ---------------------------------------------------------------- [A] math
print("[A1] n-bonacci dominant roots (root in (1,2) of x^(n+1) - 2x^n + 1 = 0)")
def root(n):
    f = lambda x: x**(n+1) - 2*x**n + 1
    lo, hi = 1.0 + 1e-9, 2.0 - 1e-12      # f(lo) < 0 < f(hi) for n >= 2
    for _ in range(200):
        mid = (lo+hi)/2
        lo, hi = (mid, hi) if f(mid) < 0 else (lo, mid)
    return (lo+hi)/2
r = {n: root(n) for n in range(2, 40)}
check("tribonacci root = 1.8393 (to 4 dp)", round(r[3], 4) == 1.8393, f"{r[3]:.6f}")
check("hexanacci root = 1.9836 (to 4 dp)", round(r[6], 4) == 1.9836, f"{r[6]:.6f}")
check("roots strictly increasing for n = 2..39",
      all(r[n] < r[n+1] for n in range(2, 39)))
check("every root < 2 (so tau = 2 is a limit, never attained)",
      all(v < 2 for v in r.values()), f"2 - r_39 = {2 - r[39]:.2e}")
check("tau - Omega = 0.0164 (to 4 dp)", round(2 - r[6], 4) == 0.0164, f"{2 - r[6]:.6f}")

print("[A2] critDim arithmetic (page: critDim(n) = 2(size(n)-1)+2)")
cd = lambda s: 2*(s-1)+2
check("critDim(3) = 26 from size 13", cd(13) == 26)
check("critDim(4) = 112 from size 56", cd(56) == 112)
print("    NOTE  sizes 13 and 56 are taken from the page's axioms; the page never")
print("          defines nBonacciRingSize, so this script cannot recompute them.")

print("[A3] Theorem 5 versus Theorem 3 (linear algebra at the fixed point)")
def matmul(A, B): return [[sum(A[i][k]*B[k][j] for k in range(2)) for j in range(2)] for i in range(2)]
def spec_radius(A):
    t, d = A[0][0]+A[1][1], A[0][0]*A[1][1]-A[0][1]*A[1][0]
    disc = t*t - 4*d
    if disc >= 0: return max(abs((t+s*math.sqrt(disc))/2) for s in (1,-1))
    return math.sqrt(d)
def power(A, n):
    P = [[1,0],[0,1]]
    for _ in range(n): P = matmul(P, A)
    return P
boost = [[1, 1], [0, 1]]                 # (x, v) -> (x + v, v), one time step
check("Galilean boost has spectral radius 1, so it is NOT a contraction",
      abs(spec_radius(boost) - 1) < 1e-12)
check("boost fixes every point (x, 0): distance between two such points is preserved",
      power(boost, 50)[0][0] == 1 and power(boost, 50)[1][1] == 1)
check("boost iterate B^n(0,1) = (n,1): orbit leaves every ball",
      power(boost, 1000)[0][1] == 1000)
star2 = [[2, 0], [0, 2]]                 # page 5(iii): two eigenvalues, both tau = 2
check("eigenvalues (2,2): spectral radius 2 > 1, iterates grow like 2^n (unstable, not 'stable star node')",
      spec_radius(star2) == 2 and power(star2, 20)[0][0] == 2**20)
print("    READ  a contraction near a fixed point needs spectral radius < 1.")
print("          Boost has 1, star node as written has 2. Neither is the contraction of Theorem 3.")

print("[A4] Axiom 8: non-commuting does not mean irreversible")
random.seed(1)
def inv(A):
    d = A[0][0]*A[1][1]-A[0][1]*A[1][0]
    return [[A[1][1]/d, -A[0][1]/d], [-A[1][0]/d, A[0][0]/d]]
def rnd():
    while True:
        A = [[random.uniform(-2,2) for _ in range(2)] for _ in range(2)]
        if abs(A[0][0]*A[1][1]-A[0][1]*A[1][0]) > 0.3: return A
C, K, F, U = rnd(), rnd(), rnd(), rnd()
close = lambda A, B: all(abs(A[i][j]-B[i][j]) < 1e-9 for i in range(2) for j in range(2))
check("C K != K C (non-commuting invertible maps)", not close(matmul(C, K), matmul(K, C)))
G = matmul(U, matmul(F, matmul(K, C)))
Ginv = matmul(inv(C), matmul(inv(K), matmul(inv(F), inv(U))))
check("G = U F K C still has an exact inverse C^-1 K^-1 F^-1 U^-1", close(matmul(G, Ginv), [[1,0],[0,1]]))
check("a strict contraction (scaling by 0.5) is also invertible",
      close(matmul([[0.5,0],[0,0.5]], [[2,0],[0,2]]), [[1,0],[0,1]]))
print("    READ  non-commutativity and contraction each leave G invertible; 'cannot undo G'")
print("          needs non-injectivity, which Axiom 2 (diffeomorphisms) rules out.")

print("[A5] nBonacciRingSize: 'the 7th term of the rank-n recurrence' (GTCT repo docstring)")
def kseq(n, seed, N=12):
    a = list(seed)
    while len(a) < N: a.append(sum(a[-n:]))
    return a
conv = {
  "seed 1,1,2,4,..": lambda n: ([1, 1, 2, 4, 8, 16, 32][:n]),
  "seed 0,1,1,2,..": lambda n: ([0] + [1, 1, 2, 4, 8, 16, 32][:n-1]),
  "seed 0,..,0,1":   lambda n: [0]*(n-1) + [1],
}
hit = False
for name, f in conv.items():
    a7 = {n: kseq(n, f(n))[6] for n in range(2, 13)}
    print(f"    INFO  {name:16s} 7th terms n=2..12: {[a7[n] for n in range(2, 13)]}")
    if a7[3] == 13 and a7[4] == 56: hit = True
    check(f"{name}: 7th term stops changing for n >= 8, so it cannot be strictly increasing",
          len({a7[n] for n in range(8, 13)}) == 1 and not all(a7[k] < a7[k+1] for k in range(2, 12)))
check("no convention tried gives 13 at n=3 AND 56 at n=4 as the 7th term", not hit)
print("    READ  56 is the 8th term of 1,1,2,4,8,15,29,56 and 13 the 6th/7th of tribonacci, so the two")
print("          axioms use different indices. Lean theorems critDim_monotone / no_return_to_critical")
print("          are valid but conditional on axioms the docstring definition does not satisfy.")
print("          Not ruled out: another convention. Needs the original definition (the GTCT docstring")
print("          credits Navratil; the author says the definition predates that document, source not yet located).")

print("[A5b] Candidate ring size N(k) = f^(k)_(2k-1), Parks-Wills convention (f_0 = 1, f_n = 0 for n < 0)")
from math import comb
def fpw(k, N):
    a = [1]
    for n in range(1, N+1): a.append(sum(a[n-i] for i in range(1, k+1) if n-i >= 0))
    return a
def cor32(k, n):   # Parks-Wills Corollary 3.2, exact rational arithmetic
    from fractions import Fraction as Fr
    t = Fr(0)
    for j in range(0, n//(k+1)+1):
        d = 1 if (n == 0 and j == 0) else 0
        num, den = (n-j*k)+j+(1 if n == 0 else 0), 2*(n-j*k)+(1 if n == 0 else 0)
        t += (-1)**j * Fr(num, den) * comb(n-j*k, j) * Fr(2)**(n-j*(k+1))
    return t
check("Corollary 3.2 reproduces the recurrence for k=1..8, n=0..30",
      all(cor32(k, n) == fpw(k, 30)[n] for k in range(1, 9) for n in range(0, 31)))
Nk = {k: fpw(k, 2*k)[2*k-1] for k in range(2, 41)}
check("N(3) = 13 and N(4) = 56", Nk[3] == 13 and Nk[4] == 56)
check("closed form N(k) = 2^(k-3) (2^(k+1) - k) for k = 3..40", all(Nk[k] == 2**(k-3)*(2**(k+1)-k) for k in range(3, 41)))
check("N strictly increasing for k = 2..40, so critDim(k) -> infinity", all(Nk[k] < Nk[k+1] for k in range(2, 40)))
check("N(2) = 3, NOT 13: the docstring's 'Dcrit(2) = 26 (accidental)' would not hold", Nk[2] == 3)
print("    READ  HYPOTHESIS ONLY. Two data points fit by an index rule; the original definition is still unsourced.")

print("[A6] Book 4 Ch 10 numbers, recomputed from the ODE (eps = 2)")
E = 2.0
def jac(r, z):
    ez = math.exp(-z)
    return [[1 - 3*r*r + E*ez, -E*(r-1)*ez], [2*r - 2*E*(r-1)*ez, E*(r-1)**2*ez]]
# transverse rate at r = 1 for large z
J = jac(1.0, 30.0)
check("transverse rate at r=1 (z large): d(rdot)/dr = -2 = -tau", abs(J[0][0] + 2) < 1e-9, f"{J[0][0]:.9f}")
# saddle: r^3 - r^2 - 2r + 1 = 0, root in (0,1)
f = lambda r: r**3 - r**2 - 2*r + 1
lo, hi = 0.0, 1.0
for _ in range(200):
    m = (lo+hi)/2
    lo, hi = (m, hi) if f(m)*f(lo) > 0 else (lo, m)
rs = (lo+hi)/2
check("saddle root = 2cos(3pi/7) = 0.4450", abs(rs - 2*math.cos(3*math.pi/7)) < 1e-12, f"{rs:.6f}")
ez = rs**2 / (E*(rs-1)**2); zs = -math.log(ez)
check("saddle satisfies rdot = 0", abs(rs*(1-rs*rs) + E*(rs-1)*ez) < 1e-12)
J = jac(rs, zs); tr = J[0][0]+J[1][1]; det = J[0][0]*J[1][1]-J[0][1]*J[1][0]
disc = tr*tr - 4*det
lp, lm = (tr+math.sqrt(disc))/2, (tr-math.sqrt(disc))/2
check("trace = 2cos(2pi/7)", abs(tr - 2*math.cos(2*math.pi/7)) < 1e-9, f"{tr:.6f}")
check("eigenvalues 1.4915 / -0.2445 (page erratum values)", round(lp, 4) == 1.4915 and round(lm, 4) == -0.2445, f"{lp:.5f} {lm:.5f}")
check("discriminant = 32 rs^2 + 15 rs - 10 = 3.0136", abs(disc - (32*rs*rs + 15*rs - 10)) < 1e-9, f"{disc:.5f}")
print("    READ  Ch 10: one stable transverse direction (-2); the saddle separates the basin.")

# ---------------------------------------------------------------- [B] page
print("[B] page regression guards (PASS = the audited wording is in place)")
raw = PAGE.read_text(encoding="utf-8")
txt = H.unescape(re.sub(r"<[^>]+>", " ", re.sub(r"(?s)<(style|script).*?</\1>", "", raw)))
txt = re.sub(r"\s+", " ", txt)
has = lambda x: x in txt
guard = lambda label, gone, here: check(label, all(not has(g) for g in gone) and all(has(h) for h in here))
guard("hero counts: 'One Conjecture' added", [], ["Four Theorems · One Conjecture"])
guard("Theorem 5 relabelled Conjecture 5 with audit note", ["Theorem 5 · The Galilean Confluence Theorem"], ["Conjecture 5 · The Galilean Confluence", "Audit note, 2026-10-24"])
guard("5(i)/(iii) marked withdrawn as printed", [], ["Galilean linearization (withdrawn)", "Embodiment threshold (withdrawn)"])
guard("Lean block no longer headed 'Closed' / 'Lean-verified'", ["Closed 2026-06-15", "(Lean-verified, 2026-06-15)", "a Lean-verified axiom"], ["Hand-proved 2026-06-15"])
guard("axiom 8: irreversibility is a postulate", ["because the operator sequence cannot be reversed"], ["a postulate of this model"])
guard("axiom 6: no 'exact identities' over-claim", ["not analogies, exact identities", "not as analogy but as instances"], ["shared functional form, not a shared invariant"])
guard("Theorem 1 labelled a proposal", ["by mathematical necessity", "They are derived."], ["a proposal: no derivation given here"])
guard("Time III/IV: spiral and irreversibility claims scoped", ["You cannot undo G because G is a contraction", "generating logarithmic spirals"], ["has an inverse", "a picture, not a derived Reeb flow"])
guard("axiom 9 sorry count attributed to the extended file", ["AXLE v6.1 carries 9 named sorrys"], ["dm3CriticalityPrinciple_extended.lean, GTCT repo) carries 9 named sorrys"])
guard("ring-size definition flagged", [], ["definition behind these axioms needs to be pinned down"])
guard("credit and sources block present (Agronomof 1914, Miles 1960, Dunkel 1925, Parks-Wills, Tuenter)", [], ["Agronomof (1914)", "Miles Jr.", "Dunkel", "Parks and D. C. Wills", "Tuenter"])
guard("ring-size candidate stated as hypothesis only", [], ["It is a hypothesis only: it gives 3, not 13, at k = 2"])
print("    NOTE  Whitney labels (fold A1, cusp A2, swallowtail A3) follow the map-germ convention;")
print("          Book 4 Ch 10 uses the same (r* is the 'Whitney A1 fold'). An earlier draft of this")
print("          audit called them off by one under Arnold's Lagrangian convention; retracted.")
print()
print(f"math/page checks failed: {len(FAIL)}")
sys.exit(1 if FAIL else 0)
