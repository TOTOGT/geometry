#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Pablo Nogueira Grossi / G6 LLC
"""
book26/nielsen-sector-coefficients.py -- checklist item C11.

C13 computed the lens-space determinant on S^3 exactly: the n^2 coefficient is
zeta(3)/(4 pi^2). C14 showed the lepton formula needs bare zeta(3) instead, or the
spectrum collapses. C11 asks the next question: what does the preprint use in its OTHER
sectors, and is it the same number?

It is not. Every sector carries zeta(3) with a different prefactor, each asserted as
derived and none derived in the text, and the bosons use a different quantity under a
confusingly similar symbol.

  sector   where                 n^2 coefficient            stated origin
  lepton   Thm 51, eq (88)       -zeta(3)                   "Casimir determinant suppression"
  quark    Thm 55, eq (121)      +C5 = +zeta(3)/12          "quadratic Casimir-determinant
                                                             coefficient from the lens-space
                                                             zeta evaluation on S^5"
  boson    Thm 53, eq (96)       +zeta_B = +sqrt3 alpha/2pi "spectral determinant corrections"
  lepton torsion  sigma3 = zeta(3)/(4 pi^2)
  quark  torsion  sigma5 = zeta(3)/(16 pi^2) = sigma3/4

Two sectors claim the SAME origin -- a lens-space zeta determinant -- and take
coefficients differing by a factor of 12. The S^3 case is the one C13 computed
independently, and it gives neither: not 1, not 1/12, but 1/(4 pi^2). The signs differ
too: the leptons are suppressed, the quarks enhanced, from a stated common mechanism.

Requires mpmath.  python3 book26/nielsen-sector-coefficients.py
"""
import sys
try:
    from mpmath import mp, mpf, pi, sqrt, zeta, exp
except ImportError:
    print("SKIP: mpmath not installed. C11 is UNCHECKED here."); sys.exit(0)
mp.dps = 30
FAIL = []
def check(label, ok, detail=""):
    print(("PASS " if ok else "FAIL ") + label + (f"  -- {detail}" if detail else ""))
    if not ok: FAIL.append(label)

z3 = zeta(3)
alpha = (9/(8*pi**4))*(pi**5/1920)**(mpf(1)/4)
lens_S3 = z3/(4*pi**2)          # computed in C13, exact
lepton  = z3                    # eq (88)
quark   = z3/12                 # eq (121), C5
boson   = sqrt(3)*alpha/(2*pi)  # eq (96), zeta_B
sig3    = z3/(4*pi**2)
sig5    = z3/(16*pi**2)

print("n^2 coefficients as the preprint uses them:")
for lab, val, sign in (("lepton  -zeta(3)", lepton, "-"), ("quark   +zeta(3)/12", quark, "+"),
                       ("boson   +sqrt3 alpha/2pi", boson, "+")):
    print(f"  {lab:<26} {sign}{mp.nstr(val, 10)}")
print(f"  computed on S^3 (C13)      -{mp.nstr(lens_S3, 10)}")
print()
print("torsion coefficients:")
print(f"  sigma3 = zeta(3)/(4 pi^2)  {mp.nstr(sig3, 10)}")
print(f"  sigma5 = zeta(3)/(16 pi^2) {mp.nstr(sig5, 10)}   (the paper says = sigma3/4)")
print()

check("sigma5 = sigma3/4 as the paper states", abs(sig5 - sig3/4) < mpf("1e-25"))
check("the lepton and quark n^2 coefficients differ by exactly 12",
      abs(lepton/quark - 12) < mpf("1e-25"),
      "same stated origin, a lens-space zeta determinant")
check("they also differ in SIGN: leptons suppressed, quarks enhanced", True,
      "eq (88) has -zeta(3)n^2, eq (121) has +C5 n^2")
check("neither equals the value computed for S^3 in C13",
      abs(lepton - lens_S3) > mpf("1") and abs(quark - lens_S3) > mpf("0.05"),
      "lepton/computed = %s, quark/computed = %s" % (mp.nstr(lepton/lens_S3, 7), mp.nstr(quark/lens_S3, 7)))
check("the boson coefficient is not a zeta value at all",
      abs(boson - z3) > mpf("1") and abs(boson - z3/12) > mpf("0.09"),
      "sqrt3*alpha/(2pi) = %s, written as 'zeta_B'" % mp.nstr(boson, 8))
check("the boson n^2 term is numerically inert at n = 1,2,3",
      all(abs(exp(boson*n*n) - 1) < mpf("0.02") for n in (1, 2, 3)),
      "exp(zeta_B n^2) = %s at n=3" % mp.nstr(exp(boson*9), 6))

print()
ctl = []
def control(name, ok_when_damaged):
    print(("PASS " if not ok_when_damaged else "FAIL ") + "control rejected: " + name)
    if ok_when_damaged: ctl.append(name)
control("the 12 test satisfied by equal coefficients", abs(lepton/lepton - 12) < mpf("1e-25"))
control("the sigma relation satisfied by an unrelated pair", abs(sig5 - sig3) < mpf("1e-25"))

print()
print("[HONESTY] This records which coefficients the preprint uses and how they relate.")
print("          It does NOT show that zeta(3)/12 is wrong for S^5 - the S^5 lens-space")
print("          determinant was not computed here, only the S^3 one (C13). What it shows")
print("          is that two sectors cite one mechanism and take values differing by 12")
print("          and in sign, and that the one case checkable from first principles")
print("          matches neither.")
if FAIL or ctl:
    print(f"\nFAILED: {len(FAIL)} check(s), {len(ctl)} control(s) not rejected"); sys.exit(1)
print("\nALL PASS")
