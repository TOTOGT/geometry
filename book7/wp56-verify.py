#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""wp56-verify.py -- companion to book7/wp56-special-relativity.html (WP56).

Written 2026-09-29 (R24: the script runs before the sentence). The page carried no script
and ten [VERIFIED] tags that were literature citations, not checks. This script re-derives
every number and formula the page prints that a script CAN check, against the page AS FOUND
(git ref pinned below) and against the page as corrected.

  [1] the page as found: what it printed (the five claims found wrong)
  [2] the boost, rapidity, velocity addition, interval invariance
  [3] E = mc^2 for 1 kg
  [4] the Andromeda walk: 5 km/h is ~4 days, not ~40,000 years
  [5] where two future light cones first meet: d/2c, not d/c
  [6] cosmic time of the merger; GW170817 delay as a fraction of the path
  [7] "precisely the group that maps the cone to itself": the rescalings do too
  [8] the reverse triangle inequality on random timelike paths (Theorem SR.3)
  [9] the corrected page prints the corrected statements

Prints SKIP, never PASS, when the pinned ref or the page is missing. Constants (c, year,
light-year, kg) are CITED reference values, not held. Not checked, recorded OPEN: see the end.
"""
import math, os, random, re, subprocess, sys, html
BASELINE = 'ff53f03'
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGE = 'book7/wp56-special-relativity.html'
fails, skips = [], []
def check(ok, msg, detail=''):
    print('    %s  %s%s' % ('PASS' if ok else 'FAIL', msg, ('  -- ' + detail) if detail and not ok else ''))
    if not ok: fails.append(msg)
def note(s): print('          ' + s)
def head(n, t): print('\n' + '=' * 72 + '\n  [%s]  %s\n' % (n, t) + '=' * 72)
def sq(s): return re.sub(r'\s+', '', html.unescape(re.sub(r'<[^>]+>', ' ', s)).lower())

C = 299_792_458.0                     # m/s, exact by definition since 1983 (CITED)
YEAR = 365.25 * 86400.0               # Julian year, s (CITED)
LY = C * YEAR                         # metres
KMH = 1000.0 / 3600.0                 # m/s per km/h

# ---------------------------------------------------------------------------
head(1, 'THE PAGE AS FOUND   (git %s)' % BASELINE)
old = None
r = subprocess.run(['git', '-C', ROOT, 'show', '%s:%s' % (BASELINE, PAGE)], capture_output=True, text=True, errors='ignore')
if r.returncode != 0:
    print('    SKIP  %s not in this checkout' % BASELINE); skips.append('baseline')
else:
    old = sq(r.stdout)
    for needle, msg in (("t'=t\\cosh\\phi-(v/c^2)x\\sinh\\phi\\cdotc", 'boost row printed t\' = t cosh(phi) - (v/c^2) x sinh(phi) . c'),
                        ('4.7\\times10^{-12}c', 'walking speed printed as 4.7e-12 c'),
                        ('\\deltat\'\\approx40{,}000$years', 'the shift printed as ~40,000 years'),
                        ('~80,000yearsapart', 'two walkers printed as ~80,000 years apart'),
                        ('itbeginsapproximately2.537millionyearsfromnow', 'cone intersection printed as beginning at 2.537 million years'),
                        ('isprecisely thegroupoflineartransformationsthatmapthisconetoitself'.replace(' ', ''), 'SO(1,3) printed as precisely the linear maps preserving the cone'),
                        ('measuredvalueof$c$intheseunitsisanartifactofhistory', 'c printed as a "measured value ... artifact of history"')):
        check(needle in old, 'as found: ' + msg)

# ---------------------------------------------------------------------------
head(2, 'THE BOOST')
random.seed(56)
bad = good = inv = 0
for _ in range(2000):
    phi = random.uniform(-3, 3); t = random.uniform(-5, 5); x = random.uniform(-5, 5) * C   # t in s, x in m
    v = C * math.tanh(phi)
    ct_new = C * t * math.cosh(phi) - x * math.sinh(phi)                 # ct' = ct cosh - x sinh
    gam = 1 / math.sqrt(1 - (v / C) ** 2)
    t_std = gam * (t - v * x / C ** 2)                                     # t' = gamma (t - v x / c^2)
    t_page = t * math.cosh(phi) - (v / C ** 2) * x * math.sinh(phi) * C    # as printed on the page
    x_new = -C * t * math.sinh(phi) + x * math.cosh(phi)
    good += abs(ct_new / C - t_std) < 1e-6 * (1 + abs(t_std))
    bad += abs(t_page - t_std) < 1e-6 * (1 + abs(t_std))
    inv += abs((-(ct_new) ** 2 + x_new ** 2) - (-(C * t) ** 2 + x ** 2)) < 1e-6 * (1 + (C * t) ** 2 + x ** 2)
check(good == 2000, "ct' = ct cosh(phi) - x sinh(phi) equals gamma (t - v x / c^2) on 2000 random boosts")
check(bad < 100, "the row as printed t' = t cosh - (v/c^2) x sinh . c matches gamma (t - v x/c^2) on only %d of 2000: it is wrong (units too: metres added to seconds)" % bad)
check(inv == 2000, "the corrected boost preserves -c^2 t^2 + x^2 on 2000 random boosts")
f1, f2 = 0.9, 1.3
ok = all(abs(math.tanh(a + b) - (math.tanh(a) + math.tanh(b)) / (1 + math.tanh(a) * math.tanh(b))) < 1e-14 for a in (0.1, 0.9, 2.0) for b in (0.3, 1.3, 2.5))
check(ok, 'rapidities add and velocities combine by (v1+v2)/(1+v1 v2/c^2): tanh(a+b) identity, 9 pairs')
check(all(math.tanh(a + b) < 1 for a in (1, 2, 4) for b in (1, 2, 4)), 'no finite sum of rapidities reaches c (tanh < 1; in floating point tanh(20) already rounds to 1.0, so the sample stops at 8)')

# ---------------------------------------------------------------------------
head(3, 'E = mc^2 FOR ONE KILOGRAM')
E = C ** 2
check(abs(E / 9e16 - 1) < 0.005, '1 kg -> %.5e J; the page prints "about 9 x 10^16" (within 0.2 percent)' % E)

# ---------------------------------------------------------------------------
head(4, 'THE ANDROMEDA WALK   (M31 at 2.537 million ly, CITED)')
D_ly = 2.537e6
beta = 5 * KMH / C
shift_yr = beta * D_ly                     # delta t' = v * delta x / c^2 = beta * (D/c), in years since D is in ly
print('      5 km/h = %.4e c   (the page as found: 4.7e-12 c)' % beta)
print('      shift  = %.5f years = %.2f days   (the page as found: ~40,000 years)' % (shift_yr, shift_yr * 365.25))
check(abs(beta / 4.63e-9 - 1) < 0.01, '5 km/h is 4.63e-9 c, not 4.7e-12 c: the page was off by a factor of about 1000')
check(abs(shift_yr * 365.25 - 4.29) < 0.05, 'the simultaneity shift at Andromeda is 4.3 days')
check(40000 / shift_yr > 3e6, 'the printed 40,000 years is %.1e times too large; not even the printed beta gives it (4.7e-12 -> %.1e years)' % (40000 / shift_yr, 4.7e-12 * D_ly))
check(abs(2 * shift_yr * 365.25 - 8.6) < 0.1, 'two walkers in opposite directions differ by 8.6 days, not ~80,000 years')
implied = 40000 / D_ly
check(abs(implied - 0.01577) < 1e-4, 'the printed 40,000 years would need v = %.4f c = %.0f km/s, not a walk' % (implied, implied * C / 1000))
in_merger = beta * 1e5
note('Inside a merged galaxy the shift does not vanish: two stars 100,000 ly apart, same 5 km/h walk -> %.1f hours.' % (in_merger * 365.25 * 24))
check(in_merger > 0, '"in 5 billion years that question has one answer" is not shown: any separation gives a non-zero shift, only a smaller one [OPEN, author\'s call]')

# ---------------------------------------------------------------------------
head(5, 'WHERE TWO FUTURE LIGHT CONES FIRST MEET')
# events A=(0,0), B=(0,d). Point (t,x) is in both forward cones iff t>=|x| and t>=|d-x| (c=1). Minimum t over x:
d = D_ly
best = min(max(abs(x), abs(d - x)) for x in [d * i / 10000 for i in range(10001)])
print('      d = %.3f Mly; earliest common-future event at t = %.4f Myr (midpoint); each flash reaches the other galaxy at t = %.3f Myr' % (d / 1e6, best / 1e6, d / 1e6))
check(abs(best / (d / 2) - 1) < 1e-6, 'the two forward cones first meet at t = d/2c = %.3f million years, at the midpoint' % (best / 1e6))
check(abs(best / 1e6 - 1.2685) < 1e-3, '1.27 million years, not 2.537 (that is the time for one flash to reach the other galaxy)')

# ---------------------------------------------------------------------------
head(6, 'COSMIC TIME AND GW170817')
lo, hi = 13.8 + 4.5, 13.8 + 5.0
check(18.0 <= lo and hi <= 19.0, 'merger 4.5-5 Gyr from now at cosmic age %.1f-%.1f Gyr: "approximately 18" is a low rounding of 18.3-18.8' % (lo, hi))
path_s = 130e6 * YEAR
frac = 1.7 / path_s
check(frac < 1e-15, '1.7 s over 130 million light-years is %.2e of the travel time: consistent with the quoted bound of ~1e-15 (if the whole delay were propagation)' % frac)
note('The bound itself (GW vs light speed to ~1e-15) is CITED; the page cites PRL 119 161101, which as far as I recall is the GW170817 detection paper;')
note('the speed bound is in the multi-messenger paper (ApJL 848 L13). Not held; WANTED.')

# ---------------------------------------------------------------------------
head(7, '"SO(1,3) IS PRECISELY THE GROUP OF LINEAR MAPS THAT SEND THE CONE TO ITSELF"')
lam = 3.7
def s2(t, x, y, z): return -t * t + x * x + y * y + z * z
ok_cone = ok_ds = True
for _ in range(500):
    x, y, z = [random.uniform(-1, 1) for _ in range(3)]
    t = math.sqrt(x * x + y * y + z * z)           # a null vector
    ok_cone &= abs(s2(lam * t, lam * x, lam * y, lam * z)) < 1e-9
    t2 = random.uniform(-2, 2); ok_ds &= abs(s2(lam * t2, lam * x, lam * y, lam * z) - lam ** 2 * s2(t2, x, y, z)) < 1e-9
check(ok_cone, 'the linear map x -> %.1f x sends every null vector to a null vector (it maps the cone to itself)' % lam)
check(ok_ds and abs(lam ** 2 - 1) > 1, 'but it multiplies ds^2 by %.2f, so it is not a Lorentz transformation: the statement "precisely" is false' % lam ** 2)
note('Correct statement: linear maps carrying the cone to itself = Lorentz group x uniform rescalings (up to reflections); Lorentz = the subgroup that also fixes ds^2.')

# ---------------------------------------------------------------------------
head(8, 'THEOREM SR.3: A GEODESIC MAXIMISES PROPER TIME')
worst = 1.0
for _ in range(300):
    n = 200; T = 1.0
    v = [random.uniform(-0.9, 0.9) for _ in range(n)]
    m = sum(v) / n; v = [a - m for a in v]                                  # closed loop in space
    tau = sum(math.sqrt(1 - a * a) * (T / n) for a in v)
    worst = min(worst, tau)
    assert tau <= T + 1e-12
check(worst < 1.0, 'on 300 random closed spatial loops (|v| < 0.9 c, c=1) proper time is at most the coordinate time T (largest shortfall %.3f)' % (1 - worst))
check(abs(2 * 0.5 * math.sqrt(1 - 0.8 ** 2) - 0.6) < 1e-12, 'twin B out and back at 0.8 c for T = 1: tau = 0.6 T (gamma = 5/3)')

# ---------------------------------------------------------------------------
head(9, 'THE PAGE AS CORRECTED   (working tree)')
cur = None
try: cur = sq(open(os.path.join(ROOT, PAGE), encoding='utf-8').read())
except OSError: print('    SKIP  page not found'); skips.append('page')
if cur is not None:
    for needle, msg in (("$ct'=ct\\cosh\\phi-x\\sinh\\phi$", 'boost row now ct\' = ct cosh(phi) - x sinh(phi)'),
                        ('4.6\\times10^{-9}c', 'walking speed now 4.6e-9 c'),
                        ('about4days', 'the shift now about 4 days'),
                        ('about9daysapart', 'two walkers now about 9 days apart'),
                        ('about1.27millionyearsfromnow', 'cone intersection now about 1.27 million years'),
                        ('uniformrescalings', 'the cone statement now names the rescalings'),
                        ('since1983', 'c now described as defined since 1983, not measured')):
        check(needle.replace(' ', '') in cur, 'corrected page: ' + msg)
    check('4.7\\times10^{-12}' not in cur and '40{,}000' not in cur and '80,000years' not in cur, 'the three wrong Andromeda numbers are gone from the page')

print('\n' + '=' * 72)
if skips: print('  SKIPPED (not passed, not failed): %s' % ', '.join(skips))
if fails:
    print('  %d FAIL:' % len(fails)); [print('    - ' + f) for f in fails]; sys.exit(1)
print('  all run checks passed.')
print('  Recorded as open, NOT checked here:')
print('   - the ten [VERIFIED] tags are literature citations (Einstein 1905, Hafele-Keating, Abbott 2017, Michelson-Morley, Penrose); none is held.')
print('   - Hafele-Keating 1971 tested clock rates (aircraft time dilation and gravitational shift); the page cites it for simultaneity: to be confirmed.')
print('   - "Andromeda paradox (Penrose 1960)": the year and the attribution are unconfirmed here; WANTED.')
print('   - "Milkomeda resolves the paradox" (section 10): not shown (block 4, last check); the author\'s claim, left as written and MODEL.')
print('   - section 6 (LAW3M attractor, r* = 0.77594058, mu = -2, the A1 fold <-> light cone): a MODEL row. mu = -2 and the orbit are')
print('     checked in book7/ch-feynman-verify.py; r* is located numerically (labs/dm3_numeric.py), and book6/wp69-verify.py prints a')
print('     13-digit value whose 8th digit differs from 0.77594058. Evanescent/propagating <-> timelike/spacelike is an analogy, not a theorem.')
print('   - the number WP-56 is also claimed by book6/wp56-algorithmic-urgency.html (R9; the author decides).')
