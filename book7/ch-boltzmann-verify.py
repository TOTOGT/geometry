#!/usr/bin/env python3
"""
Boltzmann -- why a liquid becoming a gas raises entropy, and how far the
counting argument actually gets (2026-10-22).

BLOCKS
  [1] W grows as V^N: counting check, then Delta S = N k ln(V2/V1).
  [2] Water: Delta S_vap = Delta H_vap / T_b, against Trouton's range.
  [3] The position-only estimate R ln(V_gas/V_liq), and the share of the real
      number it explains (it explains only part; the page says so).
  [4] Clapeyron: dP/dT = Delta S / Delta V, computed (not compared to a measurement).
  [5] Page structure: labels, exclusions, chapter links both ways, index card.
  [6] Controls -- checks that must FAIL on damaged input.

INPUTS (typed in, not derived):
  Delta H_vap(water, 373.15 K) = 40.65 kJ/mol   [Wikipedia, Enthalpy of vaporization; table gives 40.66]
  Trouton's rule: about 85-88 J/(K mol)         [Wikipedia, Trouton's rule]
  toluene 87.30, benzene 89.45, chloroform 87.92 J/(K mol)  [same page]
  liquid water molar volume ~18.8 cm^3/mol at 100 C  [APPROXIMATE, from a density of
      about 0.96 g/cm^3; NOT fetched from a table this session -- the page says so]
Standard library only.   python3 book7/ch-boltzmann-verify.py
"""
import math, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
fails = []
def check(ok, msg, detail=''):
    print('    %s  %s%s' % ('PASS' if ok else 'FAIL', msg, ('  -- ' + detail) if detail and not ok else ''))
    if not ok: fails.append(msg)
def head(n, t): print('\n' + '=' * 70 + '\n  [%s]  %s\n' % (n, t) + '=' * 70)

R = 8.314462618; kB = 1.380649e-23; NA = 6.02214076e23
T = 373.15; P = 101325.0
dH = 40650.0

head(1, 'W grows as V^N')
# N distinguishable particles in M cells: W = M^N. Doubling the cells doubles each choice.
for N, M in [(3, 4), (10, 50), (100, 1000)]:
    dlnW = N * math.log(2 * M) - N * math.log(M)
    check(abs(dlnW - N * math.log(2)) < 1e-9, 'N=%d, M=%d: ln W(2M) - ln W(M) = N ln 2' % (N, M))
check(abs(NA * kB - R) / R < 1e-9, 'N_A k_B = R, so per mole Delta S = R ln(V2/V1)')
print('    one mole, volume doubled: Delta S = R ln 2 = %.3f J/(mol K)' % (R * math.log(2)))

head(2, 'Water: Delta S_vap = Delta H_vap / T_b')
dS = dH / T
print('    Delta S_vap(water) = %.2f J/(mol K)' % dS)
check(abs(dS - 108.9) < 0.1, 'water Delta S_vap = 108.9 J/(mol K) to 0.1')
TROUTON_LO, TROUTON_HI = 85.0, 88.0
check(dS > TROUTON_HI, 'water sits ABOVE the Trouton range (85-88): %.1f' % dS)
for name, v in [('toluene', 87.30), ('benzene', 89.45), ('chloroform', 87.92)]:
    check(abs(v - 87) < 3, '%s Delta S_vap %.2f is within 3 of 87 (Trouton)' % (name, v))

head(3, 'Position-only estimate, and what share of the real number it is')
Vg = R * T / P                       # ideal gas molar volume, m^3/mol
Vl = 18.8e-6                         # APPROXIMATE liquid molar volume
ratio = Vg / Vl
est = R * math.log(ratio)
print('    V_gas (ideal) = %.2f L/mol, V_liq ~ %.1f cm^3/mol, ratio ~ %.0f' % (Vg * 1e3, Vl * 1e6, ratio))
print('    R ln(ratio) = %.1f J/(mol K)  =  %.0f%% of %.1f' % (est, 100 * est / dS, dS))
check(1550 < ratio < 1700, 'volume ratio is about 1,600 (ideal-gas vapour, approximate liquid volume)')
check(0.4 < est / dS < 0.7, 'the position-only term explains roughly half to two-thirds of Delta S_vap, not all of it')
check(est < TROUTON_LO, 'and it is below even the Trouton range: free volume alone does not reproduce Trouton')

head(4, 'Clapeyron relation: dP/dT = Delta S / Delta V (computed, not measured)')
dV = Vg - Vl
dPdT = dS / dV
print('    dP/dT = %.2f kPa/K  (from the inputs above; not compared with a measurement here)' % (dPdT / 1e3))
check(3.3e3 < dPdT < 3.8e3, 'dP/dT is of order 3.5 kPa/K')

head(5, 'Page structure')
page = os.path.join(HERE, 'ch-boltzmann.html')
txt = open(page, encoding='utf-8').read() if os.path.exists(page) else ''
check(bool(txt), 'book7/ch-boltzmann.html exists')
low = txt.lower()
check('not established here' in low, 'page carries a "Not established here" block')
check('no priority is claimed' in low, 'page carries a no-priority statement')
check('same functional form, not shared invariant' in low, 'any bridge to the corpus is labeled "same functional form, not shared invariant"')
for link in ['../ch-energy-entropy.html', 'ch-bose.html', 'ch-clapeyron-gibbs.html']:
    check(('href="%s"' % link) in txt, 'links to ' + link)
    p = os.path.normpath(os.path.join(HERE, link))
    check(os.path.exists(p), 'link target exists: ' + link)
def has(path, needle):
    p = os.path.join(ROOT, path)
    return os.path.exists(p) and needle in open(p, encoding='utf-8').read()
check(has('book7/index.html', 'href="ch-boltzmann.html"'), 'Book 7 gallery index has a card for it')
check(has('book7/ch-bose.html', 'ch-boltzmann.html'), 'ch-bose links forward to it')
check(has('book7/ch-clapeyron-gibbs.html', 'ch-boltzmann.html'), 'ch-clapeyron-gibbs links to it')
check(has('ch-energy-entropy.html', 'book7/ch-boltzmann.html'), 'ch-energy-entropy links to it')
for bad in ['coherence bridge', 'clean energy', 'gtct']:
    check(bad not in low, 'page does not reintroduce: ' + bad)
for num in ['108.9', '40.65', '85', '88']:
    check(num in txt, 'page states ' + num)

head(6, 'Controls (must FAIL)')
ctrl = []
def control(ok, msg):
    print('    %s  control: %s' % ('rejected as it must be' if not ok else 'NOT REJECTED', msg))
    if ok: ctrl.append(msg)
control(abs(dS - 87) < 4, 'claim "water obeys Trouton within 4 J/(mol K)"')
control(est / dS > 0.9, 'claim "position-only estimate explains 90% of water Delta S_vap"')
control(math.log(1.0) > 0, 'claim "entropy rises when volume is unchanged"')
control(bool(re.search('zzz-not-on-page', low)), 'a string that is not on the page')

print()
if fails or ctrl:
    print('FAILED: %d check(s), %d control(s) not rejected' % (len(fails), len(ctrl)))
    sys.exit(1)
print('ALL PASS')
