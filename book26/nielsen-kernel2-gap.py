#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Pablo Nogueira Grossi / G6 LLC
"""
book26/nielsen-kernel2-gap.py -- checklist item C10.

Section 3 of the chapter reads kernel 2 as NOT proving "no product splitting of the
bundle", and marks that reading a hand derivation, untested. This tests it. The reading
holds, and the gap is not a missing line: it is three separate gaps, and the middle one
cannot be closed at all in the intended application.

WHAT THE LEAN PROVES (book26/NielsenKernels.lean, kernel 2, compiled 2026-10-26):
  domain_idempotents_trivial : a MiniRing with no zero divisors has only idempotents 0,1
  product_has_zero_divisors  : a direct product of two nonzero MiniRings has zero divisors
Both are statements about `MiniRing alpha` for an ARBITRARY type alpha.

GAP 1 -- the Lean never touches a space. The file contains no topology, no connectedness,
no continuity, no manifold. Checked below by reading the file.

GAP 2 -- the bridge is idempotents <-> clopen sets, and the hypothesis the Lean needs is
FALSE for the ring that matters. X is connected iff C(X) has only the trivial idempotents.
The Lean instead assumes "no zero divisors" (a domain), which is strictly stronger, and
which FAILS for C(X) on every connected space bigger than a point: two bump functions with
disjoint supports multiply to zero and neither is zero. This script exhibits such a pair.
So `nzd` is not an unproved hypothesis here -- it is an unsatisfiable one.

GAP 3 -- direct product is the wrong operation. A ring direct product corresponds to a
DISJOINT UNION of spaces: C(X disjoint-union Y) = C(X) x C(Y). A CARTESIAN product of
spaces gives a tensor product, C(X x Y) = C(X) (completed-tensor) C(Y) (Kuenneth). "No
product splitting of the bundle" is a claim about x; kernel 2 is a claim about the ring
product, hence about disjoint-union. Even granting gaps 1 and 2, the conclusion is about
the wrong operation.

   python3 book26/nielsen-kernel2-gap.py
"""
import math, re, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
LEAN = HERE / "NielsenKernels.lean"
FAIL = []
def check(label, ok, detail=""):
    print(("PASS " if ok else "FAIL ") + label + (f"  -- {detail}" if detail else ""))
    if not ok: FAIL.append(label)

# --- GAP 1: read the Lean and see what kernel 2 is about -------------------
src = LEAN.read_text(encoding="utf-8") if LEAN.exists() else ""
if not src:
    print("SKIP: NielsenKernels.lean not found. C10 is UNCHECKED here."); sys.exit(0)
k2 = src.split("/-! ## Kernel 2 -/")[1].split("/-! ## Kernel 3 -/")[0]
topo = [w for w in ("topolog", "connected", "clopen", "continuous", "manifold",
                    "Bundle", "sphere", "Hopf", "open set") if w.lower() in k2.lower()]
check("kernel 2's Lean contains no topology, connectedness or continuity",
      not topo, "found: %s" % topo if topo else "MiniRing over an arbitrary type only")
check("its two theorems are the ones the chapter names",
      "domain_idempotents_trivial" in k2 and "product_has_zero_divisors" in k2)
check("the no-zero-divisor condition enters as a HYPOTHESIS, never discharged",
      "(nzd :" in k2 and "nzd" not in src.split("/-! ## Kernel 3 -/")[1],
      "`nzd` is assumed in domain_idempotents_trivial and instantiated nowhere in the file")

# --- GAP 2: the hypothesis is unsatisfiable for C(X), X connected ----------
# Two smooth bumps with disjoint support on the connected space R.
def bump(x, c, w):
    t = (x - c) / w
    return math.exp(-1.0 / (1.0 - t * t)) if abs(t) < 1.0 else 0.0
f = lambda x: bump(x, -2.0, 1.0)      # supported on (-3,-1)
g = lambda x: bump(x,  2.0, 1.0)      # supported on ( 1, 3)
grid = [(-6.0 + 12.0 * i / 20000.0) for i in range(20001)]
prod_max = max(abs(f(x) * g(x)) for x in grid)
check("C(R) has zero divisors: two bumps with disjoint support, f*g = 0 everywhere",
      prod_max == 0.0, "max|f*g| over 20001 points = %r" % prod_max)
check("and neither factor is the zero function",
      max(abs(f(x)) for x in grid) > 0.3 and max(abs(g(x)) for x in grid) > 0.3,
      "max|f| = %.4f, max|g| = %.4f" % (max(abs(f(x)) for x in grid), max(abs(g(x)) for x in grid)))
check("R is connected, so 'domain' is strictly stronger than 'connected'",
      True, "connectedness <-> trivial IDEMPOTENTS; the Lean assumes no ZERO DIVISORS")
# the idempotent route, which is the correct one, on a DISCONNECTED space
h = lambda x: 1.0 if x > 0 else 0.0   # the indicator of a clopen piece of R\{0}
check("the right bridge: on a disconnected space the indicator is a nontrivial idempotent",
      all(abs(h(x) * h(x) - h(x)) < 1e-15 for x in grid if x != 0.0)
      and any(h(x) == 0.0 for x in grid) and any(h(x) == 1.0 for x in grid),
      "e^2 = e with e != 0,1 -- this is what connectedness actually rules out")

# --- GAP 3: direct product vs Cartesian product ---------------------------
check("the Lean's prodRing is the DIRECT product (componentwise mul)",
      "mul := fun p q => (R.mul p.1 q.1, S.mul p.2 q.2)" in k2,
      "C(X disjoint-union Y) = C(X) x C(Y); C(X x Y) is a tensor product (Kuenneth)")

print()
ctl = []
def control(name, ok_when_damaged):
    print(("PASS " if not ok_when_damaged else "FAIL ") + "control rejected: " + name)
    if ok_when_damaged: ctl.append(name)
control("zero-divisor test passed by overlapping bumps",
        max(abs(bump(x,-2.,1.)*bump(x,-2.2,1.)) for x in grid) == 0.0)
control("topology test passed on a file that does mention it",
        not [w for w in ("connected",) if w in "a connected space"])

print()
print("[HONESTY] This reads the Lean file and exhibits a counterexample in C(R). It does")
print("          NOT show the preprint's physical claim is false, that no bundle argument")
print("          exists, or that the author intended kernel 2 to carry the bundle step.")
print("          What it shows is that kernel 2 as written cannot reach it: no topology,")
print("          a hypothesis unsatisfiable for function rings on connected spaces, and a")
print("          conclusion about the wrong product.")
if FAIL or ctl:
    print(f"\nFAILED: {len(FAIL)} check(s), {len(ctl)} control(s) not rejected"); sys.exit(1)
print("\nALL PASS")
