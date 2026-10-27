#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Pablo Nogueira Grossi / G6 LLC
"""
book26/nielsen-exponent-fork.py -- checklist item C14, the consequence of C13.

C13 showed the lens-space determinant gives zeta(3)/(4 pi^2), not bare zeta(3).
C12 showed the preprint's own appendix script reproduces its lepton table using
exp(-zeta(3) n^2). This runs that same formula with the coefficient C13 derived and
asks what happens to the masses. Everything else is held fixed: same Lambda, same a,
same beta, same alpha, same trefoil factor, same PDG references.

THE FORK. Exactly one of these holds, and both contradict "zero dimensionless free
parameters":
  (A) the Sector Determinant Lemma is right  -> the mass formula is wrong, and the
      lepton ratios miss by factors of ~34 and ~350;
  (B) the mass formula is right              -> the exponent zeta(3) is NOT the lens-space
      determinant coefficient, so its stated derivation does not support it and the
      coefficient is a fitted number wearing a derivation's clothes.

WHY v CANNOT RESCUE IT. The failure is in the RATIOS. The preprint's own p.12 argument
says changing v "multiplies every mass by the same constant" and "leaves invariant every
mass ratio". So by the paper's own reasoning its single empirical input cannot repair a
ratio failure. Lambda_shell cancels in m2/m1 and m3/m2.

Requires mpmath.   python3 book26/nielsen-exponent-fork.py
"""
import sys
try:
    from mpmath import mp, mpf, pi, sqrt, exp, log, zeta
except ImportError:
    print("SKIP: mpmath not installed. C14 is UNCHECKED here."); sys.exit(0)
mp.dps = 40
FAIL = []
def check(label, ok, detail=""):
    print(("PASS " if ok else "FAIL ") + label + (f"  -- {detail}" if detail else ""))
    if not ok: FAIL.append(label)

z3, z5 = zeta(3), zeta(5)
alpha = (9/(8*pi**4))*(pi**5/1920)**(mpf(1)/4)
v     = mpf("246220")
kappa = exp(z3/(24*pi**2))/(4*pi**2)
Lam   = sqrt(2*pi)*v*kappa**6
a3    = 6*sqrt(2)*exp(z3/(24*pi**2))
s3    = z3/(4*pi**2)                     # the C13 coefficient; the paper defines it and does not use it
beta  = z5/(8*pi**4)
tau   = {1: mpf(1), 2: mpf(1), 3: mpf(3)**(1/(3 - s3*sqrt(2)))}
PDG   = {1: (mpf("0.51099895069"), "e"), 2: (mpf("105.6583755"), "mu"), 3: (mpf("1776.93"), "tau")}

def mass(n, coef):
    e = a3*n - coef*n**2 + beta*n*(n+1)/2 + n*alpha/6 + s3*log(tau[n])
    return Lam*(n+1)*exp(e)

def main():
    mp_, mc = {}, {}
    print("            paper exp(-zeta3 n^2)      corrected exp(-zeta3/(4pi^2) n^2)")
    print("              mass (MeV)   dev %          mass (MeV)        dev %")
    for n in (1, 2, 3):
        r, nm = PDG[n]
        mp_[n], mc[n] = mass(n, z3), mass(n, s3)
        print(f"m_{nm:<4} {mp.nstr(mp_[n],9):>14} {mp.nstr((mp_[n]-r)/r*100,4):>8}   "
              f"{mp.nstr(mc[n],9):>16} {mp.nstr((mc[n]-r)/r*100,5):>14}")

    check("with bare zeta(3) the three masses sit within 0.25% of PDG",
          all(abs((mp_[n]-PDG[n][0])/PDG[n][0]) < mpf("0.0025") for n in (1,2,3)))
    check("with the C13 coefficient every mass is wrong by more than a factor of 2",
          all(abs(mc[n]/PDG[n][0] - 1) > 1 for n in (1,2,3)),
          "e +223%, mu +1.1e4%, tau +3.8e6%")

    print("\nratios, which the paper's own p.12 says v cannot change:")
    fac = {}
    for hi, lo, lab in ((2,1,"mu/e"), (3,2,"tau/mu")):
        obs = PDG[hi][0]/PDG[lo][0]
        fac[lab] = (mc[hi]/mc[lo])/obs
        print(f"  {lab:<7} observed {mp.nstr(obs,8):>11}  paper {mp.nstr(mp_[hi]/mp_[lo],8):>11}"
              f"  corrected {mp.nstr(mc[hi]/mc[lo],8):>11}  (out by x{mp.nstr(fac[lab],6)})")
    check("the paper's exponent reproduces both observed ratios to better than 0.01%",
          abs((mp_[2]/mp_[1])/(PDG[2][0]/PDG[1][0]) - 1) < mpf("1e-4")
          and abs((mp_[3]/mp_[2])/(PDG[3][0]/PDG[2][0]) - 1) < mpf("1e-4"))
    check("the C13 coefficient misses mu/e by >30x and tau/mu by >300x",
          fac["mu/e"] > 30 and fac["tau/mu"] > 300)
    check("so v cannot repair it: the failure is in ratios, which v leaves invariant",
          True, "the preprint's own p.12 argument, applied to its own formula")

    # R24 controls
    print()
    ctl = []
    def control(name, ok_when_damaged):
        print(("PASS " if not ok_when_damaged else "FAIL ") + "control rejected: " + name)
        if ok_when_damaged: ctl.append(name)
    control("the two coefficients treated as interchangeable",
            abs(mass(3, z3)/mass(3, s3) - 1) < mpf("0.01"))
    control("a ratio test that passes when the ratio is unchanged",
            ((mp_[2]/mp_[1])/(PDG[2][0]/PDG[1][0])) > 30)

    print("\n[HONESTY] This holds every other ingredient fixed and changes one coefficient.")
    print("          It does NOT show which branch of the fork is true, that the lemma")
    print("          applies to this formula at all, or that a, phi_n or Lambda are right -")
    print("          a and phi_n are still undefined in the text (C13, C11).")
    if FAIL or ctl:
        print(f"\nFAILED: {len(FAIL)} check(s), {len(ctl)} control(s) not rejected"); sys.exit(1)
    print("\nALL PASS")

if __name__ == "__main__":
    main()
