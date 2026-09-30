#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""wp57-verify.py -- companion to book7/wp57-causal-integration.html (WP57).

Written 2026-09-29 (R24: the script runs before the sentence). The page carried no script.
It repeats WP56's Andromeda numbers, and states one cosmological threshold, that this script
can check. It checks the page AS FOUND (git ref pinned below) and as corrected.

  [1] the page as found: what it printed
  [2] the Andromeda walk (4.3 days, not ~40,000 years) and where the cones first meet (d/2c)
  [3] the cosmological threshold: two future cones meet iff comoving d < 2 x event horizon
  [4] the merger arithmetic against the page's own cited bracket
  [5] "events deep in the history are outside J^-(M)": a worldline, and a finite-size model
  [6] the corrected page prints the corrected statements

Prints SKIP, never PASS, when the pinned ref or the page is missing. Constants are CITED
reference values, not held: c, Julian year; H0 = 67.4, Omega_m = 0.315 (Planck 2018 style),
flat LCDM with a small radiation term. Not checked, recorded OPEN: see the end.
"""
import math, os, random, re, subprocess, sys, html
BASELINE = 'bc1e9a2'
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGE = 'book7/wp57-causal-integration.html'
fails, skips = [], []
def check(ok, msg, detail=''):
    print('    %s  %s%s' % ('PASS' if ok else 'FAIL', msg, ('  -- ' + detail) if detail and not ok else ''))
    if not ok: fails.append(msg)
def note(s): print('          ' + s)
def head(n, t): print('\n' + '=' * 72 + '\n  [%s]  %s\n' % (n, t) + '=' * 72)
def sq(s): return re.sub(r'\s+', '', html.unescape(re.sub(r'<[^>]+>', ' ', s)).lower())

C = 299_792_458.0; YEAR = 365.25 * 86400.0; LY = C * YEAR; KMH = 1000.0 / 3600.0
D_LY = 2.537e6                                   # M31 distance, ly (the page's figure, CITED)

head(1, 'THE PAGE AS FOUND   (git %s)' % BASELINE)
r = subprocess.run(['git', '-C', ROOT, 'show', '%s:%s' % (BASELINE, PAGE)], capture_output=True, text=True, errors='ignore')
if r.returncode != 0:
    print('    SKIP  %s not in this checkout' % BASELINE); skips.append('baseline')
else:
    old = sq(r.stdout)
    for needle, msg in (('firstintersect,at$\\sim2.537$mly', 'abstract: cones first intersect at 2.537 Mly'),
                        ('t_{\\text{geo}}\\approx2.537\\text{myr}', 'Theorem 3.1: T_geo = 2.537 Myr (and T_geo = d/c)'),
                        ('approximately80,000years', 'section 1: two walkers about 80,000 years apart'),
                        ('\\sim40{,}000$yearsinandromeda', 'section 4: shift about 40,000 years'),
                        ('frame-dependentby$\\sim40{,}000$years', 'section 5: frame-dependent by about 40,000 years per 5 km/h'),
                        ('+2.537myr<br>geometriccibrace'.replace('<br>geometriccibrace', ''), 'timeline row at +2.537 Myr'),
                        ('$d\\gtrsim16$gly', 'Theorem 3.2: permanent separation for d >~ 16 Gly')):
        check(needle in old, 'as found: ' + msg)

head(2, 'THE ANDROMEDA WALK AND WHERE THE CONES MEET')
d = D_LY * LY; v = 5 * KMH
dt = v * d / C ** 2
note('shift = v d / c^2 = %.3f days   (v/c = %.3e)' % (dt / 86400, v / C))
check(abs(dt / 86400 - 4.29) < 0.01, 'one walker, 5 km/h: 4.29 days')
check(abs(2 * dt / 86400 - 8.58) < 0.02, 'two opposite walkers: 8.6 days apart')
check(dt / YEAR < 0.02, 'nowhere near 40,000 years (ratio page/computed = %.2e)' % (40000 * YEAR / dt))
# future cones of two events separated by d: first common point at the midpoint, at t = d/2c
t_meet = d / (2 * C) / YEAR
note('cones meet first at the midpoint, t = d/2c = %.3f Myr; a flash from one reaches the other at d/c = %.3f Myr' % (t_meet / 1e6, D_LY / 1e6))
check(abs(t_meet - D_LY / 2) < 1, 'first intersection at d/2c = 1.27 Myr')
# numeric: smallest t with a point x with |x|<=ct and |x-d|<=ct is t=d/2c
lo, hi = 0.0, D_LY
for _ in range(100):
    mid = (lo + hi) / 2
    if mid + mid >= D_LY: hi = mid
    else: lo = mid
check(abs(hi - D_LY / 2) < 1e-6, 'bisection on "the two balls of radius ct overlap": t = d/2c')

head(3, 'THE COSMOLOGICAL THRESHOLD   (flat LCDM, CITED parameters)')
H0 = 67.4; Om = 0.315; Or = 9.0e-5; OL = 1 - Om - Or
GLY_PER = C / (H0 * 1000 / 3.0856775814913673e22) / LY / 1e9      # c/H0 in Gly
def E(a): return math.sqrt(Or / a**4 + Om / a**3 + OL)
# comoving event horizon at a=1: c int_1^inf da /(a^2 H)   (u = 1/a: du -> int_0^1 du / E(1/u))
n = 200000; s = 0.0
for i in range(n):
    u = (i + 0.5) / n; s += 1.0 / E(1.0 / u)
chi_eh = GLY_PER * s / n
note('c/H0 = %.2f Gly;  comoving event horizon chi_eh = %.2f Gly' % (GLY_PER, chi_eh))
check(15.0 < chi_eh < 17.0, 'event horizon about 16 Gly (Davis & Lineweaver cite ~16): %.2f' % chi_eh)
note('cones of A_0 and B_0 (a=1 now): each reaches comoving radius chi_eh as t -> infinity;')
note('they meet iff the comoving separation d < 2 chi_eh = %.1f Gly, not d < %.1f Gly' % (2 * chi_eh, chi_eh))
check(2 * chi_eh > 32.0, 'the separation threshold is twice the horizon, about 33 Gly')
check(16.0 < 2 * chi_eh, 'a pair 20 Gly apart is beyond the page threshold but their cones still meet (2 chi_eh = %.1f)' % (2 * chi_eh))

head(4, 'THE MERGER ARITHMETIC AGAINST THE PAGE\'S OWN CITED BRACKET')
G = 3.15576e7 * 1e9                                        # s per Gyr
vr = 110.0; dkm = D_LY * LY / 1000
t_lin = dkm / vr / G
note('straight-line approach at 110 km/s: d/v = %.2f Gyr (an upper bound; gravity shortens it)' % t_lin)
lo_b, hi_b = 5.86 - 0.72, 5.86 + 0.72
note('the reference line on the page: coalescence 5.86 +- 0.72 Gyr = %.2f .. %.2f Gyr; the page prints 4.5..6' % (lo_b, hi_b))
check(not (lo_b <= 4.5 and hi_b >= 6.0 and 4.5 >= lo_b), 'the page range 4.5-6 Gyr does NOT sit inside the cited bracket (starts %.2f Gyr below its lower end)' % (lo_b - 4.5))
note('a star at cosmic time 20 Gyr (13.8 + T) is after the merger only if T < 6.2 Gyr; upper end of the bracket is %.2f' % hi_b)
check(13.8 + hi_b > 20.0, 'the upper end of the cited bracket (%.2f Gyr) is later than the page\'s 20 Gyr example' % (13.8 + hi_b))

head(5, '"EVENTS DEEP IN THE HISTORY ARE STILL OUTSIDE J-(M)"   (section 3, regime a)')
random.seed(57)
ok = True
for _ in range(2000):
    dd = random.uniform(0.5, 5)                     # c = 1; A at x=0, B at x=dd, both at rest
    ta, tb = random.uniform(-5, 5), random.uniform(-5, 5)   # present events A0=(ta,0), B0=(tb,dd)
    # a point M in the future of both: choose the midpoint at a late enough time
    x = random.uniform(0, dd); tm = max(ta + abs(x), tb + abs(x - dd)) + random.uniform(0, 3)
    for _k in range(5):
        e = ta - random.uniform(0, 50)              # any earlier event on A's worldline
        ok &= (tm - e) >= abs(x - 0)                # in the past cone of M
        e = tb - random.uniform(0, 50)
        ok &= (tm - e) >= abs(x - dd)
check(ok, 'for 2000 random configurations, every earlier point on either (point-like) worldline lies in J-(M) once M is in J+(A0) and J+(B0)')
note('a causal past is transitive: if A0 is in J-(M), so is everything before A0 on A\'s worldline.')
R = 5e4                                             # ly, a galactic radius; a MODEL number
T_ext = (D_LY + 2 * R) / 1e6
note('two extended discs (radius %.0f ly each, MODEL): every present point of both is in J-(M) from about %.2f Myr' % (R, T_ext))
check(T_ext < 3.0, 'that time is %.2f Myr, not billions of years (ratio to 4.5 Gyr: %.1e)' % (T_ext, 4.5e9 / (T_ext * 1e6)))
note('so what separates regimes (a) and (b) is not "complete histories in the causal past"; the page states it as if it were. Recorded OPEN.')

head(6, 'THE PAGE AS CORRECTED   (working tree)')
cur = None
try: cur = sq(open(os.path.join(ROOT, PAGE), encoding='utf-8').read())
except OSError: print('    SKIP  page not found'); skips.append('page')
if cur is not None:
    for needle, msg in (('first intersect,at$\\approx1.27$myr', 'abstract: cones first intersect at about 1.27 Myr'),
                        ('t_{\\text{geo}}\\approx d/2c', 'Theorem 3.1: T_geo = d/2c'),
                        ('about9days', 'section 1: two walkers about 9 days'),
                        ('about4daysinandromeda', 'section 4: shift about 4 days'),
                        ('+1.27myr', 'timeline row at +1.27 Myr'),
                        ('\\approx33$gly', 'Theorem 3.2: permanent separation beyond about 33 Gly'),
                        ('verificationnote', 'a verification note is on the page')):
        check(needle.replace(' ', '') in cur, 'corrected page: ' + msg)
    check('separatedbyapproximately80,000' not in cur and '\\sim40{,}000' not in cur and '2.537myr<br>' not in cur, 'the wrong Andromeda numbers are gone')

print('\n' + '=' * 72)
if skips: print('  SKIPPED (not passed, not failed): %s' % ', '.join(skips))
if fails:
    print('  %d FAIL:' % len(fails)); [print('    - ' + f) for f in fails]; sys.exit(1)
print('  all run checks passed.')
print('  Recorded as open, NOT checked here:')
print('   - the ~4.5-6 Gyr merger time: the cited bracket is 5.86 +- 0.72 (van der Marel 2012, not held); the page range is not inside it.')
print('   - Sawala et al. 2025 (addendum): ~50/50 for a collision within 10 Gyr; cited, not held.')
print('   - regime (a) vs (b): a causal past is transitive, so "complete histories" arrive by ~2.6 Myr (block 5), not with the merger. The author decides.')
print('   - Penrose 1960 is cited as the origin of the Andromeda paradox, but the reference given is "The apparent shape of a relativistically moving sphere" (Proc. Camb. Phil. Soc. 55, 137, which I recall as 1959): to confirm.')
print('   - "beyond the event horizon" is not "receding at v > c": the Hubble sphere (~14 Gly) and the event horizon (~16 Gly) differ. Not edited.')
print('   - r* = 0.77594058 and the 10^25 magnification, the g^96 identification, WP58 r*_gal = 0.713 and 2.5 kpc: MODEL/CONJECTURE, not run here.')
