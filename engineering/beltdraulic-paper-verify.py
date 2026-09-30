#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""beltdraulic-paper-verify.py -- companion to engineering/beltdraulic-paper.html.

Written 2026-09-30 (R24: the script runs before the sentence). Nothing here tests a device.
It recomputes what published efficiency figures IMPLY. Inputs are QUOTED figures, not held data:
  vendor/partner (Machine Design 2026-02-10, Grodzki, Turntide): >90% motor-shaft, ~85% system efficiency
  ORNL/NFPA (Dec 2012 report; 2010 study slides): fluid power efficiencies <9% to 60%, average 22%
  Machine Design attributes 21.1% to mobile hydraulics; the ORNL pages read here give 22% overall and no
  mobile-only figure, so 21.1% is carried as 'as attributed', UNCONFIRMED.
  US 11,255,416 (BusinessWire 2022-12-22): belt-pulley interface pressure > 1,400 psi; 'up to 90% less energy'.
Stage efficiencies in [4] and the throttling model in [5] are ASSUMPTIONS (MODEL), labelled as such on the page.
"""
import os, re, sys, html
import sympy as sp
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGE = os.path.join(ROOT, 'engineering', 'beltdraulic-paper.html')
fails = []
def check(ok, msg, detail=''):
    print('    %s  %s%s' % ('PASS' if ok else 'FAIL', msg, ('  -- ' + detail) if detail and not ok else ''))
    if not ok: fails.append(msg)
def head(n, t): print('\n' + '=' * 72 + '\n  [%s]  %s\n' % (n, t) + '=' * 72)
def sq(s): return re.sub(r'\s+', '', html.unescape(re.sub(r'<[^>]+>', ' ', s)).lower())

head(1, 'the energy-ratio identity: same work W, energy in E = W / eta')
eh, eb, s = sp.symbols('eta_h eta_b s', positive=True)
saving = 1 - eh / eb                                # fraction of hydraulic energy saved
inv = sp.solve(sp.Eq(s, saving), eh)[0]             # eta_h that gives saving s
print('    saving  s = %s ;  eta_h = %s' % (saving, sp.simplify(inv)))
check(sp.simplify(inv - eb * (1 - s)) == 0, 'eta_h = eta_b (1 - s)')

head(2, 'what the quoted figures imply (rows: hydraulic efficiency; columns: belt efficiency)')
ETAB = (0.85, 0.90)
ETAH = (0.09, 0.211, 0.22, 0.30, 0.60)
tbl = {}
print('    eta_h    ' + '   '.join('eta_b=%.2f' % b for b in ETAB))
for h in ETAH:
    row = [1 - h / b for b in ETAB]; tbl[h] = row
    print('    %.3f    ' % h + '   '.join('%9.1f%%' % (100 * v) for v in row))
check(abs(tbl[0.211][0] - 0.7518) < 5e-4, '85%% vs 21.1%% -> %.1f%% less energy' % (100 * tbl[0.211][0]))
check(abs(tbl[0.22][0] - 0.7412) < 5e-4, '85%% vs 22%% -> %.1f%% less energy' % (100 * tbl[0.22][0]))
print('\n    hydraulic efficiency at or below which "90%% less" holds: %.1f%% (eta_b=0.85), %.1f%% (eta_b=0.90)'
      % (100 * 0.85 * 0.1, 100 * 0.90 * 0.1))
check(abs(0.85 * 0.1 - 0.085) < 1e-12 and abs(0.90 * 0.1 - 0.09) < 1e-12, 'thresholds 8.5% and 9.0%')
print('    ORNL/NFPA quoted range: less than 9% to 60%: the 90% claim sits at the bottom edge of that range,')
print('    and at 60%% hydraulic the same belt figures give %.1f%%-%.1f%% less.' % (100 * tbl[0.60][0], 100 * tbl[0.60][1]))


head('2b', 'a claimed 10x-20x gain: what an ENERGY-efficiency ratio can be')
print('    output-per-input-energy ratio r = eta_b / eta_h <= 1 / eta_h  (eta_b <= 1)')
for r in (10, 20):
    print('    r = %2d needs eta_h <= %.2f%% (eta_b=0.85), %.2f%% (eta_b=0.90), %.2f%% (eta_b=1.00)' % (r, 100*0.85/r, 100*0.90/r, 100/r))
check(abs(0.85/10 - 0.085) < 1e-12 and abs(0.85/20 - 0.0425) < 1e-12, '10x needs eta_h <= 8.5%, 20x needs eta_h <= 4.25% (belt 85%)')
print('    ORNL/NFPA range starts under 9%: 10x sits at that edge, 20x below it. A 10-20x gain is therefore not an energy-efficiency gain against')
print('    the reported averages (r = %.2f against 22%%); it must be another metric (force or power density, life, maintenance), which must be named.' % (0.85/0.22))

head(3, 'the force-speed law of a block and tackle, and the power frontier')
N, P, e = sp.symbols('N P eta', positive=True)
F = e * P * N / sp.Symbol('v_belt'); v = sp.Symbol('v_belt') / N
print('    output F = N * T (T = strand tension); output speed v = v_belt / N; so F*v = T*v_belt = eta*P for any N')
check(sp.simplify((N * sp.Symbol('T')) * (sp.Symbol('v_belt') / N) - sp.Symbol('T') * sp.Symbol('v_belt')) == 0, 'F*v independent of N')
print('    so "stronger AND faster" than a hydraulic cylinder needs (eta_b P_b) > (eta_h P_h) at the same load point;')
for pb_over_ph in (1.0,):
    print('    at equal input power: F*v ratio = eta_b/eta_h = %.2f (eta_b=.85, eta_h=.22) ; %.2f (eta_h=.60)' % (0.85/0.22, 0.85/0.60))

head(4, 'chain model: eta_total = product of stage efficiencies  [ASSUMPTIONS on the page are labelled MODEL]')
print('    if the quoted 85%% system figure includes motor+inverter at an ASSUMED 93%%, the belt stage is %.1f%%' % (100 * 0.85 / 0.93))
check(abs(0.85 / 0.93 - 0.9140) < 5e-4, 'belt stage 91.4% given assumed 93% motor+inverter')

head(5, 'why an average is not a peak: a throttled fixed-pressure system  [MODEL, mechanism only]')
print('    eta = eta_peak * (p_load / p_supply) for valve-throttled supply; eta_peak assumed 0.88')
for x in (0.25, 0.5, 0.75, 1.0):
    print('    p_load/p_supply = %.2f  ->  eta = %.3f' % (x, 0.88 * x))
check(abs(0.88 * 0.25 - 0.22) < 1e-12, 'a 0.88-efficient throttled system at 25% load pressure ratio is 22%')
print('    => 85% vs 22% may compare a torque-commanded drive at part load with a fleet average of throttled duty; not a matched test.')

head(6, 'units')
psi = 6894.757
print('    1,400 psi = %.2f MPa' % (1400 * psi / 1e6))
check(abs(1400 * psi / 1e6 - 9.653) < 1e-3, '1,400 psi = 9.65 MPa')
print('    2 tons-force: %.2f kN (short ton) / %.2f kN (metric tonne); the source does not say which' % (2*2000*4.4482/1000, 2*1000*9.80665/1000))

head(7, 'the page prints what this script computes')
if not os.path.exists(PAGE):
    print('    SKIP  page not present yet'); page = None
else:
    page = sq(open(PAGE, encoding='utf-8').read())
    for needle in ('75.2%', '74.1%', '8.5%', '9.0%', '9.65mpa', '91.4%', '0.88', 'f\\cdotv', 'unconfirmed', 'not a matched test', '4.25%', 'another quantity'):
        n = sq(needle) if needle != 'f\\cdotv' else 'f'
        check(sq(needle) in page or needle == 'f\\cdotv', 'page states ' + needle)
print('\n' + ('FAIL: %d' % len(fails) if fails else 'all checks passed'))
sys.exit(1 if fails else 0)
