#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Pablo Nogueira Grossi / G6 LLC
"""
book26/nielsen-abstract-arithmetic.py -- recomputes the numbers in the abstract of a third-party preprint
(cited in chapter 8) from the formulas and reference values stated here. Needs mpmath. No network.
    python3 book26/nielsen-abstract-arithmetic.py
It prints each value, the reference it is compared with and where that reference came from.
REFERENCE VALUES: PDG 2025 gauge/Higgs summary table (m_W, m_Z, m_H, sin2 theta_eff), read 2026-10-26 through a
summarising fetch tool; NuFit-6.0 (arXiv:2410.05380) Table 1, the block "IC19 without SK atmospheric data"
only; the paper's own quoted comparison values for the Thomson-limit sin2 theta_W and Delta m2_21.
NOT VERIFIED: the paper's 0.23867(16) "PDG Thomson limit", its 0.23122(6) MS-bar value, its 7.53(18)e-5 and
2.453(33)e-3. The last is probably the PDG value for Delta m2_32, not Delta m2_31 (my recollection, not retrieved).
"""
from mpmath import mp, mpf, pi, exp, zeta
mp.dps = 40
FAIL = []
def row(name, val, ref=None, unc=None, note=""):
    s = f"{name:<58} {mp.nstr(val, 10)}"
    if ref is not None and unc is not None:
        s += f"   vs {mp.nstr(ref,8)} +- {mp.nstr(unc,3)}: {mp.nstr((val-ref)/unc,4)} sigma"
    print(s + (f"   [{note}]" if note else ""))
    return val
def must(label, ok):
    print(("PASS " if ok else "FAIL ") + label)
    if not ok: FAIL.append(label)
print("--- sin2 theta_W = 3/(4 pi)")
s = row("3/(4 pi)", 3/(4*pi))
r1 = row("  vs Thomson limit as quoted by the paper", s, mpf("0.23867"), mpf("0.00016"), "paper's own comparison")
r2 = row("  vs PDG 2025 sin2 theta_eff (Z pole, effective)", s, mpf("0.23148"), mpf("0.00013"), "different quantity from sin2 theta_W")
r3 = row("  vs MS-bar at M_Z as quoted by the paper", s, mpf("0.23122"), mpf("0.00006"), "paper says gap is a finite 'dressing' of -0.0075")
sig1 = (s - mpf("0.23867"))/mpf("0.00016")
must("the paper's 0.4 sigma at the Thomson point is reproduced", mpf("0.35") < sig1 < mpf("0.45"))
sig2 = (s - mpf("0.23148"))/mpf("0.00013")
must("at the Z pole the bare value is far from the measured one (more than 50 sigma against theta_eff)", sig2 > 50)
print("--- on-shell 1 - (m_W/m_Z)^2 from the abstract's own masses")
os_paper = row("1-(80.3695/91.1878)^2", 1 - (mpf("80.3695")/mpf("91.1878"))**2)
row("1-(80.3692/91.1880)^2 (PDG 2025 masses)", 1 - (mpf("80.3692")/mpf("91.1880"))**2)
must("on-shell value from the abstract's masses is 0.22320 (the paper's own script target)", abs(os_paper - mpf("0.22320")) < mpf("0.000001"))
must("3/(4 pi) and the abstract's own on-shell value differ by more than 0.015", s - os_paper > mpf("0.015"))
print("--- boson masses against PDG 2025")
row("m_W (GeV)", mpf("80.3695"), mpf("80.3692"), mpf("0.0133"))
row("m_Z (GeV)", mpf("91.1878"), mpf("91.1880"), mpf("0.0020"))
row("m_H (GeV)", mpf("125.225"), mpf("125.20"), mpf("0.11"))
print("--- neutrinos")
m1, m2, m3 = mpf("0.970"), mpf("8.708"), mpf("49.604")
tot = row("sum of masses (meV)", m1+m2+m3)
must("sum is 59.282 meV, i.e. about 0.059 eV", abs(tot - mpf("59.282")) < mpf("1e-9"))
d21 = (m2**2 - m1**2)*mpf("1e-6"); d31 = (m3**2 - m1**2)*mpf("1e-6")
row("Delta m2_21 (eV^2) vs paper's 7.53(18)e-5", d21, mpf("7.53e-5"), mpf("0.18e-5"))
row("Delta m2_21 (eV^2) vs NuFit-6.0 IC19 7.49(19)e-5", d21, mpf("7.49e-5"), mpf("0.19e-5"))
row("Delta m2_31 (eV^2) vs paper's 2.453(33)e-3", d31, mpf("2.453e-3"), mpf("0.033e-3"), "paper's comparison")
row("Delta m2_31 (eV^2) vs NuFit-6.0 IC19 2.534(-23)e-3", d31, mpf("2.534e-3"), mpf("0.023e-3"), "one NuFit block only")
row("Delta m2_32 = Delta m2_31 - Delta m2_21 (eV^2)", d31 - d21, mpf("2.453e-3"), mpf("0.033e-3"), "if 2.453 is the 3-2 splitting")
print("--- cosmology")
a = 1/mpf("137.035999177")
lam = row("Lambda = 3 exp(-(2+zeta(3)/24)/alpha), alpha=1/137.036", 3*exp(-(2+zeta(3)/24)/a))
must("the Lambda formula gives 2.94e-122", abs(lam/mpf("1e-122") - mpf("2.94")) < mpf("0.005"))
H = mpf("68.5")/mpf("3.0856775814913673e19")*mpf("5.391247e-44")
oml = row("Omega_Lambda needed for H0=68.5 from Lambda=3 Omega H^2", mpf("2.94e-122")/(3*H**2))
must("H0=68.5 corresponds to Omega_Lambda about 0.684 (the measured value is an input to that step)", abs(oml - mpf("0.684")) < mpf("0.002"))
print("[HONESTY] Reproduces the abstract's arithmetic from stated formulas. It does not show the formulas follow from the paper's geometry, and the reference values are as stated above.")
import sys
sys.exit(1 if FAIL else 0)
