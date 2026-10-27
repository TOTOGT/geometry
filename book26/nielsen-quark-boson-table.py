#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Pablo Nogueira Grossi / G6 LLC
"""
book26/nielsen-quark-boson-table.py -- checklist item C11.

C12 did this for the leptons. This does it for the quark and boson sectors: the formulas
transcribed verbatim from the preprint's own Appendix A script (TUFT_Verification.py,
SECTION 3 eq.(97) and SECTION 4 eq.(122)), with the PDG references taken from that
script's own dictionary, not re-fetched.

THE QUESTION C11 WAS ASKED: do the other sectors show the uniform +0.23% offset that
C12 found in the leptons? THE ANSWER: no. The quark and boson deviations scatter in both
signs and all sit inside PDG error. But that is not a point in the paper's favour, for
two reasons this script makes explicit.

(1) THE UNCERTAINTIES ARE NOT COMPARABLE. The electron mass is known to 3e-8 %, the up
    quark to 3.2 %. "Within experimental error" means something eight orders of magnitude
    weaker in the quark sector. A 0.2 % quark deviation is 0.06 sigma; the same relative
    deviation on the electron was over 10^6 sigma.
(2) THE SECTORS DO NOT SHARE A FORMULA. There is no uniform offset because there is no
    uniform expression. Each sector carries its own constants, and the quark sector
    carries THREE SEPARATE EXPRESSIONS for lambda_T, one per generation, with a sign flip
    between n=2 and n=3, plus three torsion values and a 2/3 prefactor at n=1 alone. Six
    quark masses are produced from a formula carrying that many per-generation choices.

Requires mpmath.   python3 book26/nielsen-quark-boson-table.py
"""
import sys
try:
    from mpmath import mp, mpf, pi, sqrt, exp, log, sin, zeta
except ImportError:
    print("SKIP: mpmath not installed. C11 is UNCHECKED here."); sys.exit(0)
mp.dps = 40
FAIL = []
def check(label, ok, detail=""):
    print(("PASS " if ok else "FAIL ") + label + (f"  -- {detail}" if detail else ""))
    if not ok: FAIL.append(label)

z3, z5 = zeta(3), zeta(5)
alpha = (9/(8*pi**4))*(pi**5/1920)**(mpf(1)/4)
v = mpf("246220")
PDG = {'W':(mpf('80369.2'),mpf('13.3')), 'Z':(mpf('91188.0'),mpf('2.0')), 'H':(mpf('125200'),mpf('110')),
       'u':(mpf('2.16'),mpf('0.07')), 'd':(mpf('4.67'),mpf('0.09')), 's':(mpf('93.4'),mpf('0.8')),
       'c':(mpf('1270'),mpf('20')), 'b':(mpf('4180'),mpf('30')), 't':(mpf('172760'),mpf('300'))}

# ---- SECTION 3, bosons, eq.(97), verbatim from the appendix
r    = mpf(8)
LamB = v*sqrt(2/r)*sin(pi/r)*exp(-(2+1/(4*pi))*alpha)
aB   = -alpha*sqrt(2)/pi
zB   = sqrt(3)*alpha/(2*pi)
rf   = r + zB
TW, TZ, TH = (sqrt(3)/2)*exp(aB+zB), sin(4*pi/rf)/(4*sin(pi/rf)), (mpf(2)/3)*exp(3*aB+9*zB)
mW, mZ, mH = LamB*2*exp(alpha/6)*TW, LamB*3*exp(2*alpha/6)*TZ, LamB*4*exp(3*alpha/6)*TH

# ---- SECTION 4, quarks, eq.(122), verbatim
spec5 = (3*z5 + 5*pi**2*z3)/(8*pi**4)
kap5  = exp(spec5/6)/(8*pi**3)
Lam5  = (2*pi/sqrt(3))*v*kap5**3
a5    = exp(spec5/6)*sqrt(3)*(2 + z3/(4*pi**2))
C5, b5, s5 = z3/12, z5/(8*pi**4), z3/(16*pi**2)
lT    = {1: 2/(3*sqrt(3)), 2: 2/pi + z3/(24*pi), 3: 2/pi - z3/(24*pi)}
tq    = {1: mpf(1), 2: mpf(4), 3: mpf(3)}
pref  = {1: mpf(2)/3, 2: mpf(1), 3: mpf(1)}
names = {1: ('u','d'), 2: ('s','c'), 3: ('b','t')}

rows = [('W', mW), ('Z', mZ), ('H', mH)]
for n in (1, 2, 3):
    base = a5*n + C5*n**2 + b5*n*(n+1)/2 + s5*log(tq[n])
    rows += [(names[n][0], Lam5*(n+1)*exp(base - lT[n]*n)*pref[n]),
             (names[n][1], Lam5*(n+1)*exp(base + lT[n]*n)*pref[n])]

print("  particle      computed (MeV)        PDG      rel.dev %     pull (sigma)   PDG err %")
dev = {}
for lab, m in rows:
    rr, uu = PDG[lab]; dev[lab] = (m-rr)/rr
    print(f"  {lab:<8} {mp.nstr(m,10):>18} {mp.nstr(rr,8):>10} {mp.nstr(dev[lab]*100,4):>11}"
          f" {mp.nstr((m-rr)/uu,4):>14} {mp.nstr(uu/rr*100,3):>11}")

check("the transcription reproduces the paper's own printed constants",
      abs(Lam5 - mpf('6.09144e-2')) < mpf('1e-7') and abs(a5 - mpf('3.564112')) < mpf('1e-6'),
      "Lambda_5 and a_5 as printed on pp.127-128")
check("the transcription reproduces the paper's printed quark table",
      abs(dev['u']) < mpf('1e-5') and abs(rows[3][1] - mpf('2.160005')) < mpf('1e-5'),
      "u = 2.160005 MeV as printed on p.131")
check("NO uniform offset in the quark or boson sectors (unlike the leptons' +0.23%)",
      max(dev[k] for k in dev) > 0 and min(dev[k] for k in dev) < 0
      and (max(dev[k] for k in dev) - min(dev[k] for k in dev)) > mpf('0.002'),
      "signs mixed, spread %s percentage points" % mp.nstr((max(dev.values())-min(dev.values()))*100, 3))
check("but the quark uncertainties are orders of magnitude looser than the leptons'",
      PDG['u'][1]/PDG['u'][0] > 1000 * mpf('1.6e-10')/mpf('0.51099895069'),
      "up quark +-3.2%% vs electron +-3e-8%%")
check("so 'within experimental error' is a far weaker claim here",
      all(abs((m-PDG[l][0])/PDG[l][1]) < 2 for l, m in rows),
      "every pull < 2 sigma, on uncertainties 0.6-3.2%")
check("the quark formula carries three separate lambda_T expressions, one per generation",
      len({mp.nstr(lT[n], 12) for n in (1,2,3)}) == 3,
      "2/(3sqrt3); 2/pi + z3/(24pi); 2/pi - z3/(24pi)  -- note the sign flip")
check("and a 2/3 prefactor applied to the first generation alone",
      pref[1] != pref[2] and pref[2] == pref[3])

print()
ctl = []
def control(name, ok_when_damaged):
    print(("PASS " if not ok_when_damaged else "FAIL ") + "control rejected: " + name)
    if ok_when_damaged: ctl.append(name)
control("uniform-offset test passed by a uniform set", (lambda d: max(d)-min(d) > 0.002)([0.0023]*9))
control("three-expression test passed by one repeated value", len({"x","x","x"}) == 3)

print()
print("[HONESTY] This runs the preprint's own formulas with its own constants and its own")
print("          PDG references. It does NOT show the quark or boson numbers are wrong -")
print("          they agree within the quoted errors. What it shows is that the sectors do")
print("          not share one formula, that the quark agreement is tested against")
print("          uncertainties 10^5 times looser than the leptons', and that six quark")
print("          masses rest on three per-generation lambda_T values, three torsion values")
print("          and a first-generation-only prefactor.")
if FAIL or ctl:
    print(f"\nFAILED: {len(FAIL)} check(s), {len(ctl)} control(s) not rejected"); sys.exit(1)
print("\nALL PASS")
