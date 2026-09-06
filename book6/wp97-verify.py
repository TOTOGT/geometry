#!/usr/bin/env python3
"""
wp97-verify.py — regenerates every computed claim in
Principia Orthogona, Book VI, WP-97, "Thirty Was Doing the Work".

Repo rule: a published number must be regenerable by a tool.

SCOPE. The Lean side of this paper is NOT reproduced here — a Python script
cannot certify a kernel result and must not appear to. What this file does is
the finite arithmetic the paper's prose asserts: the dimension of the space of
fields on a ring of N sectors invariant under both a sixfold and a tenfold
rotation, for every refinement N the paper mentions and many it does not.

The Lean claims are checked by the kernel and reported at
    geometry/tools/verify-audit/2026-09-05/PolarPolygonCommonRefinement.axioms.txt
and by nothing in this file.

Run:  python3 wp97-verify.py     (exits non-zero on any failure)
Requires: nothing beyond the standard library.
"""
from math import gcd

FAIL = []


def check(label, got, want):
    ok = got == want
    print(("  OK   " if ok else "  FAIL ") + label + f"   got={got}  want={want}")
    if not ok:
        FAIL.append(label)


def invariant_dim(N, m1, m2):
    """Number of free values in the space of fields on Z/N invariant under
    rotation by N/m1 and by N/m2 sectors.

    Computed by orbit counting, not by the gcd formula the paper claims, so
    that the two are independent and a disagreement is a finding rather than a
    tautology.
    """
    p1, p2 = N // m1, N // m2
    parent = list(range(N))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a, b):
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[ra] = rb

    for k in range(N):
        union(k, (k + p1) % N)
        union(k, (k + p2) % N)
    return len({find(k) for k in range(N)})


print("[1] The thirty-sector case — the one the original sentence rested on")
check("30 / 6, the period of a sixfold pattern on thirty sectors", 30 // 6, 5)
check("30 / 10, the period of a tenfold pattern", 30 // 10, 3)
check("gcd(5, 3)", gcd(5, 3), 1)
check("free values on thirty sectors (orbit count)", invariant_dim(30, 6, 10), 1)

print()
print("[2] The sixty-sector case — the witness")
check("60 / 6", 60 // 6, 10)
check("60 / 10", 60 // 10, 6)
check("gcd(10, 6)", gcd(10, 6), 2)
check("free values on sixty sectors (orbit count)", invariant_dim(60, 6, 10), 2)

alt = [k % 2 for k in range(60)]
check("alt is invariant under +10 (sixfold)",
      all(alt[(k + 10) % 60] == alt[k] for k in range(60)), True)
check("alt is invariant under +6 (tenfold)",
      all(alt[(k + 6) % 60] == alt[k] for k in range(60)), True)
check("alt is not constant", len(set(alt)) > 1, True)

print()
print("[3] Every refinement, N = 30 .. 1200 — the general claim")
print("    orbit count must equal N/30 at every step; equal to 1 only at N = 30")
bad_dim, ones = [], []
for N in range(30, 1201, 30):
    d = invariant_dim(N, 6, 10)
    if d != N // 30:
        bad_dim.append((N, d, N // 30))
    if d == 1:
        ones.append(N)
check("refinements where the orbit count differs from N/30", bad_dim, [])
check("refinements forcing a constant", ones, [30])

print()
print("[4] The group-theoretic reading")
check("lcm(6, 10) — the order of the generated rotation",
      6 * 10 // gcd(6, 10), 30)
check("gcd(N/6, N/10) = N/30 for every refinement tested",
      all(gcd(N // 6, N // 10) == N // 30 for N in range(30, 1201, 30)), True)

print()
print("[5] The counting the paper reports about the Lean file")
print("    (these are read off the gate report, not recomputed here)")
REPORT = {
    "declarations in PolarPolygonCommonRefinement.lean": 15,
    "trusting sorryAx": 0,
    "resting on no axiom at all": 5,
    "resting on anything outside the permitted three": 0,
}
for k, v in REPORT.items():
    print(f"  ----  {k}: {v}   (from the gate report; not verifiable from here)")

print()
if FAIL:
    print(f"FAILED: {len(FAIL)}")
    for f in FAIL:
        print("  -", f)
    raise SystemExit(1)
print("all computed claims regenerated.")
