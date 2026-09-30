#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ulam-dual-verify.py -- companion to book7/ulam-dual.html (Dual Ulam Spiral Overlay).

Written 2026-09-29 (R24: the script runs before the sentence). The page's spiral is ported
line for line from its JavaScript (buildSpiral) and the sieve likewise. Checks:

  [1] the page as found (git ref pinned below)
  [2] the spiral: fills each N x N grid exactly once, for the four sizes on the page
  [3] Euler's n^2+n+41: prime for n = 0..39, on one diagonal of the page's spiral
  [4] primes on the diagonals versus off them
  [5] the overlay: coincidences of prime cells under rotation (0, 90, 180, 270 degrees)
  [6] which slider angles can give exact cell coincidences at all (step 0.5 degrees)
  [7] "r* = 0.776 corresponds to a 7th-order Chebyshev node (2cos(3pi/7))"
  [8] the corrected page prints the corrected statements

Prints SKIP, never PASS, when the pinned ref or the page is missing.
"""
import math, os, random, re, subprocess, sys, html
BASELINE = 'ef5e823'
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGE = 'book7/ulam-dual.html'
fails, skips = [], []
def check(ok, msg, detail=''):
    print('    %s  %s%s' % ('PASS' if ok else 'FAIL', msg, ('  -- ' + detail) if detail and not ok else ''))
    if not ok: fails.append(msg)
def note(s): print('          ' + s)
def head(n, t): print('\n' + '=' * 72 + '\n  [%s]  %s\n' % (n, t) + '=' * 72)
def sq(s): return re.sub(r'\s+', '', html.unescape(re.sub(r'<[^>]+>', ' ', s)).lower())

def sieve(m):
    c = [0] * (m + 1); c[0] = c[1] = 1
    for i in range(2, int(m ** .5) + 1):
        if not c[i]:
            for j in range(i * i, m + 1, i): c[j] = 1
    return c            # 0 = prime, as in the page
def spiral(N):          # buildSpiral(N) of the page
    pos = [None] * (N * N + 1); x = y = N // 2; dx, dy = 0, -1; steps = 1; sc = 0; tc = 0
    for n in range(1, N * N + 1):
        pos[n] = (x, y); x += dx; y += dy; sc += 1
        if sc == steps:
            sc = 0; dx, dy = -dy, dx; tc += 1
            if tc % 2 == 0: steps += 1
    return pos
SIZES = (51, 71, 101, 141)

head(1, 'THE PAGE AS FOUND   (git %s)' % BASELINE)
r = subprocess.run(['git', '-C', ROOT, 'show', '%s:%s' % (BASELINE, PAGE)], capture_output=True, text=True, errors='ignore')
if r.returncode != 0:
    print('    SKIP  %s not in this checkout' % BASELINE); skips.append('baseline')
else:
    old = sq(r.stdout)
    for needle, msg in (('at0°thecoincidencesetisdensealongthemaindiagonals', 'at 0 degrees the coincidence set is "dense along the main diagonals"'),
                        ('atirrationalanglesitthinstoisolatedpoints', '"at irrational angles it thins to isolated points"'),
                        ('7th-orderchebyshevnode(2cos(3π/7))', 'r* = 0.776 called a 7th-order Chebyshev node, 2cos(3pi/7)')):
        check(needle in old, 'as found: ' + msg)

head(2, 'THE SPIRAL FILLS EACH GRID EXACTLY ONCE')
P = {}
for N in SIZES:
    p = spiral(N); cells = set(p[1:])
    check(len(cells) == N * N and all(0 <= a < N and 0 <= b < N for a, b in cells), '%d x %d: %d integers land on %d distinct cells inside the grid' % (N, N, N * N, len(cells)))
    P[N] = p
note('the page\'s draw loops run n = 1 .. N^2-1, so the last integer N^2 is never drawn; it is a perfect square, hence never prime: no effect on the prime views; one cell is missing in "all integers" view.')

head(3, "EULER'S n^2 + n + 41")
def isp(m): return m > 1 and all(m % d for d in range(2, int(m ** .5) + 1))
check(all(isp(n * n + n + 41) for n in range(40)), 'prime for n = 0..39 (40 values)')
check(not isp(40 * 40 + 40 + 41) and 40 * 40 + 40 + 41 == 41 * 41, 'n = 40 gives 41^2 = 1681')
def collinear(cells):
    ds = {(cells[i + 1][0] - cells[i][0], cells[i + 1][1] - cells[i][1]) for i in range(len(cells) - 1)}
    return len(ds) == 1 and all(abs(a) == abs(b) for a, b in ds)
p = P[101]                                            # centre = 1, as on the page
ev = [p[(2 * m) ** 2 + 2 * m + 41] for m in range(20)]; od = [p[(2 * m + 1) ** 2 + (2 * m + 1) + 41] for m in range(20)]
check(not collinear(ev) and not collinear(od), 'on the page\'s spiral (centre = 1) the Euler values are on no single diagonal (even n: %s, odd n: %s)' % (collinear(ev), collinear(od)))
x0, y0 = p[41]; inv = {v: k for k, v in enumerate(p) if v}
best = 0
for dx, dy in ((1, 1), (1, -1)):
    for sgn in (1, -1):
        run = 0; t = 0
        while (x0 + sgn * t * dx, y0 + sgn * t * dy) in inv and isp(inv[(x0 + sgn * t * dx, y0 + sgn * t * dy)]): t += 1
        best = max(best, t)
note('longest unbroken run of primes on a diagonal ray from 41 in the page\'s spiral: %d' % best)
check(best < 10, 'that run is short (%d), against 40 consecutive Euler primes' % best)
q = ns_sp = spiral(101); c = 50                        # spiral started at 41: value v sits where the page puts v - 40
ev2 = [q[(2 * m) ** 2 + 2 * m + 1] for m in range(20)]; od2 = [q[(2 * m + 1) ** 2 + (2 * m + 1) + 1] for m in range(20)]
check(collinear(ev2) and collinear(od2), 'with the spiral started at 41 (value n^2+n+41 at cell n^2+n+1) the even-n terms lie on one main diagonal and the odd-n terms on the other')

head(4, 'PRIMES ON THE DIAGONALS VERSUS OFF THEM   (101 x 101)')
N = 101; p = P[N]; c = N // 2; comp = sieve(N * N + 1)
on = tot_on = off = tot_off = 0
for n in range(2, N * N):
    x, y = p[n]; u, v = x - c, y - c
    if abs(u) == abs(v): tot_on += 1; on += (not comp[n])
    else: tot_off += 1; off += (not comp[n])
note('prime fraction on the two main diagonals: %.3f (%d of %d);  off them: %.3f (%d of %d)' % (on / tot_on, on, tot_on, off / tot_off, off, tot_off))
check(on / tot_on > off / tot_off, 'primes are denser on the main diagonals than off them')

head(5, 'THE OVERLAY: PRIME CELLS THAT COINCIDE AFTER ROTATION')
random.seed(7)
for N in SIZES:
    p = P[N]; c = N // 2; comp = sieve(N * N + 1)
    prim = [n for n in range(1, N * N) if not comp[n]]; S = set(p[n] for n in prim); row = {}
    for k in range(4):
        cnt = 0
        for n in prim:
            u, v = p[n][0] - c, p[n][1] - c
            for _ in range(k): u, v = -v, u
            cnt += (u + c, v + c) in S
        row[90 * k] = cnt
    dens = len(prim) / (N * N); exp = dens * len(prim)
    note('%3d x %3d: %5d primes; coincide at 0: %d, 90: %d, 180: %d, 270: %d;  if independent at that density: about %.0f' % (N, N, len(prim), row[0], row[90], row[180], row[270], exp))
    check(row[0] == len(prim), '%d: at 0 degrees every prime is a coincidence (%d of %d)' % (N, row[0], len(prim)))
    check(row[90] > 1.5 * exp and row[180] > 1.5 * exp, '%d: at 90 and 180 degrees coincidences exceed the independent expectation (%d, %d against %.0f)' % (N, row[90], row[180], exp))
    check(row[90] < 0.5 * len(prim), '%d: at 90 degrees fewer than half of the primes coincide (%.0f%%)' % (N, 100.0 * row[90] / len(prim)))

head(6, 'WHICH SLIDER ANGLES GIVE EXACT COINCIDENCES   (min -180, max 180, step 0.5)')
exact = []
for i in range(-360, 361):
    a = i * 0.5; c_, s_ = math.cos(math.radians(a)), math.sin(math.radians(a))
    if all(min(abs(z - w) for w in (0, .5, 1)) < 1e-9 for z in (abs(c_), abs(s_))) and abs(abs(c_) - .5) > 1e-9 and abs(abs(s_) - .5) > 1e-9:
        exact.append(a)
note('angles where both cos and sin are rational (Niven: rational cos at a rational-degree angle is 0, +-1/2, +-1; both rational forces a multiple of 90): %s' % exact)
check(exact == [-180.0, -90.0, 0.0, 90.0, 180.0], 'only -180, -90, 0, 90, 180 map cell centres onto cell centres; every other slider angle is a rational number of degrees (never "irrational")')

head(7, '"r* = 0.776 CORRESPONDS TO A 7TH-ORDER CHEBYSHEV NODE (2 cos(3 pi/7))"')
R = 0.77594058
val = 2 * math.cos(3 * math.pi / 7)
note('2 cos(3 pi/7) = %.6f' % val)
check(abs(val - R) > 0.3, '2cos(3pi/7) is %.4f, not 0.776' % val)
T7 = sorted(math.cos((2 * k - 1) * math.pi / 14) for k in range(1, 8))
note('nodes of T7: %s' % ', '.join('%.4f' % t for t in T7))
near = min(T7, key=lambda t: abs(t - R))
check(abs(near - R) > 1e-3, 'nearest T7 node is %.4f, %.4f away from r* = 0.77594058' % (near, abs(near - R)))
cands = {'cos(k pi/7)': [math.cos(k * math.pi / 7) for k in range(0, 8)], '2cos(k pi/7)': [2 * math.cos(k * math.pi / 7) for k in range(0, 8)], 'cos(k pi/14)': [math.cos(k * math.pi / 14) for k in range(0, 15)]}
best = min((abs(v - R), name, v) for name, vs in cands.items() for v in vs)
note('closest of cos(k pi/7), 2cos(k pi/7), cos(k pi/14): %s = %.6f (off by %.4f)' % (best[1], best[2], best[0]))
check(best[0] > 1e-3, 'no seventh-root-of-unity cosine equals r* to 3 places')

head(8, 'THE PAGE AS CORRECTED   (working tree)')
try: cur = sq(open(os.path.join(ROOT, PAGE), encoding='utf-8').read())
except OSError: print('    SKIP  page not found'); skips.append('page'); cur = None
if cur is not None:
    check('diagonals;atirrationalanglesitthins' not in cur and 'corresponds toa7th-order'.replace(' ','') not in cur and 'primescluster' not in cur, 'the three unsupported statements are gone')
    for needle, msg in (('everyprimeisacoincidence', 'at 0 degrees every prime is a coincidence'),
                        ('359of1,252', '90 degrees: 359 of 1,252 on the 101 x 101 grid'),
                        ('−180°,−90°,0°,90°and180°areexact', 'exact coincidences only at multiples of 90'),
                        ('isnota7th-orderchebyshevnode', 'r* is not a Chebyshev node'),
                        ('verificationnote', 'a verification note is on the page')):
        check(needle in cur, 'corrected page: ' + msg)

print('\n' + '=' * 72)
if skips: print('  SKIPPED (not passed, not failed): %s' % ', '.join(skips))
if fails:
    print('  %d FAIL:' % len(fails)); [print('    - ' + f) for f in fails]; sys.exit(1)
print('  all run checks passed.')
print('  Recorded as open, NOT checked here:')
print('   - "interference bands" / "moire": a visual claim about the canvas at non-multiple angles; no measurement here (the canvas drawing is not run in this script).')
print('   - "the contact-geometric fingerprint of two lattice rotations" and "a discrete analogue of a Whitney A1 caustic": MODEL, not derived.')
print('   - where r* = 0.77594058 does come from is the series\' own claim (book6/wp69-verify.py; labs/dm3_numeric.py); the link to lensing (WP58, WP59) is not tested here.')
print('   - the page has no sources for the Ulam spiral or the Euler polynomial (Ulam 1964 / Gardner 1964; Euler 1772): cited from general knowledge, not held.')
