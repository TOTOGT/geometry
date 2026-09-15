#!/usr/bin/env python3
"""
WP-120 -- how many closed orbits, counted.

WHY THIS FILE EXISTS. The series calls Gamma = {r = 1} "the limit cycle" in
ten to seventeen places per page and nowhere proves it is the only one.
Uniqueness is asserted exactly once in the corpus, in chRho-spectral's open-
obligation table, and there it is about the discrete Collatz cycle. For the
continuous Gamma the definite article has been doing the work.

Strogatz has two instruments for this and the corpus uses neither: index
theory (Theorem 6.8.2, p. 180 -- any closed orbit encloses fixed points whose
indices sum to +1) and Dulac's criterion (p. 204). This script applies them.

BLOCKS
  [1] The divergence formula in polar coordinates, checked against a Cartesian
      numerical divergence.
  [2] g = 1/r^3 is a Dulac function for Strogatz Example 7.3.1 whenever
      |mu| < 1, and stops being one at |mu| = 1.
  [3] Index theory: the only fixed point is the origin and it has index +1,
      so every closed orbit encircles it.
  [4] Existence (WP-122, Poincare-Bendixson) + uniqueness (Dulac on the
      annulus) = exactly one, corroborated by integration.
  [5] The radial-only count, applied to both of the corpus's toy models --
      and they differ: Book 6's has one circular orbit per frozen slice,
      Vol II's has two.
  [6] r_2(z) sweeps all of (0,1), so matching it to a stored constant is not
      evidence. A guard, computed.
  [7] The three-dimensional flows have no periodic orbit to be unique.
  [8] Control.

PRIMARY SOURCE. S. H. Strogatz, "Nonlinear Dynamics and Chaos", 2nd ed.,
Westview 2015 / CRC 2018. Theorem 6.8.1 p. 179, Theorem 6.8.2 p. 180,
Dulac's criterion p. 204, Example 7.3.1 p. 206.

Standard library only.  python3 book6/wp120-verify.py
"""

import math, sys

fails = []
def check(ok, msg, detail=''):
    print('    %s  %s%s' % ('PASS' if ok else 'FAIL', msg,
                            ('  -- ' + detail) if detail and not ok else ''))
    if not ok: fails.append(msg)
def head(n, t):
    print('\n' + '=' * 70 + '\n  [%s]  %s\n' % (n, t) + '=' * 70)

TWOPI = 2.0 * math.pi

# --- Strogatz Example 7.3.1, in Cartesian coordinates -----------------------
# polar:  r' = r(1 - r^2) + mu r cos(theta),  theta' = 1
# so      r' e_r + r theta' e_theta  ->  the Cartesian field below.
def F_xy(x, y, mu):
    r2 = x*x + y*y
    return (x*(1.0 - r2) + mu*x - y,
            y*(1.0 - r2) + mu*x*y/math.sqrt(r2) + x) if r2 > 0 else (0.0, 0.0)

# mu r cos(theta) e_r  =  mu x * (x/r, y/r) = (mu x^2/r, mu x y / r)
def F_xy_clean(x, y, mu):
    r = math.hypot(x, y)
    r2 = r*r
    return (x*(1.0 - r2) - y + mu*x*x/r,
            y*(1.0 - r2) + x + mu*x*y/r)

def div_num(fn, x, y, h=1e-6, *a):
    fx1, _ = fn(x+h, y, *a); fx0, _ = fn(x-h, y, *a)
    _, fy1 = fn(x, y+h, *a); _, fy0 = fn(x, y-h, *a)
    return (fx1-fx0)/(2*h) + (fy1-fy0)/(2*h)

# ---------------------------------------------------------------------------
head(1, 'THE DIVERGENCE, IN POLAR AND IN CARTESIAN')
print('  For a planar field written F = F_r e_r + F_theta e_theta,')
print('      div F = (1/r) d/dr ( r F_r ) + (1/r) d/dtheta ( F_theta ).')
print('  Example 7.3.1 has F_r = r(1-r^2) + mu r cos(theta), F_theta = r, so')
print('      div F = 2 - 4 r^2 + 2 mu cos(theta).\n')
print('     %6s %8s %20s %20s %10s' % ('mu', 'r', 'polar formula', 'numeric Cartesian', 'diff'))
ok_div = True
for mu in (0.0, 0.4, 0.9):
    for r, th in ((0.7, 0.3), (1.0, 1.9), (1.4, 4.4)):
        x, y = r*math.cos(th), r*math.sin(th)
        an = 2.0 - 4.0*r*r + 2.0*mu*math.cos(th)
        nu = div_num(F_xy_clean, x, y, 1e-6, mu)
        print('     %6.1f %8.2f %20.9f %20.9f %10.1e' % (mu, r, an, nu, abs(an-nu)))
        if abs(an - nu) > 1e-5: ok_div = False
check(ok_div, 'the polar divergence formula matches the Cartesian field, to 1e-5')
print('\n     Note the sign change in 2 - 4r^2: at mu = 0 it is positive inside')
print('     r = 1/sqrt(2) and negative outside. So g = 1 -- plain Bendixson --')
print('     rules out nothing here, which is why a Dulac function is needed.')
check(2 - 4*(0.5)**2 > 0 > 2 - 4*(1.0)**2, 'div F really does change sign with g = 1')

# ---------------------------------------------------------------------------
head(2, 'g = 1/r^3 IS A DULAC FUNCTION FOR |mu| < 1')
print('  Take g = r^{-3}. Then r g F_r = (1/r - r) + mu cos(theta)/r, whose')
print('  d/dr is -(1/r^2) - 1 - mu cos(theta)/r^2, and g F_theta = r^{-2} has no')
print('  theta dependence. So')
print('      div(g F) = -(1/r) [ (1 + mu cos(theta)) / r^2 + 1 ],')
print('  which is strictly negative on all of r > 0 exactly when |mu| < 1.\n')

def divgF_analytic(r, th, mu):
    return -(1.0/r) * ((1.0 + mu*math.cos(th))/(r*r) + 1.0)

def gF(x, y, mu):
    r = math.hypot(x, y)
    fx, fy = F_xy_clean(x, y, mu)
    return (fx / r**3, fy / r**3)

print('     %6s %8s %20s %20s %10s' % ('mu', 'r', 'analytic div(gF)', 'numeric div(gF)', 'diff'))
ok_dg = True
for mu in (0.0, 0.5, 0.9):
    for r, th in ((0.4, 0.0), (1.0, math.pi), (2.5, 2.2)):
        x, y = r*math.cos(th), r*math.sin(th)
        an, nu = divgF_analytic(r, th, mu), div_num(gF, x, y, 1e-6, mu)
        print('     %6.1f %8.2f %20.9f %20.9f %10.1e' % (mu, r, an, nu, abs(an-nu)))
        if abs(an - nu) > 1e-4 * max(1.0, abs(an)): ok_dg = False
check(ok_dg, 'the closed form for div(gF) matches numerical differentiation')

worst = {}
for mu in (0.0, 0.25, 0.5, 0.75, 0.95, 0.999):
    mx = max(divgF_analytic(0.02 + 8.0*i/4000, TWOPI*j/360, mu)
             for i in range(4001) for j in range(0, 360, 12))
    worst[mu] = mx
print()
for mu, mx in worst.items():
    print('     mu = %-6.3f  max div(gF) over r in [0.02, 8] x theta  =  %.6e' % (mu, mx))
check(all(v < 0 for v in worst.values()),
      'div(gF) stays strictly negative at every |mu| < 1 scanned')
bad = max(divgF_analytic(0.02 + 8.0*i/4000, TWOPI*j/360, 1.5)
          for i in range(4001) for j in range(0, 360, 12))
print('     mu = 1.500   max div(gF)                               =  %+.6e' % bad)
check(bad > 0, 'and it does change sign once |mu| > 1, as the formula requires')
print('\n     Strogatz p. 204 lists g = 1, 1/(x^a y^b), e^{ax}, e^{ay} as the')
print('     candidates that occasionally work, and says there is no algorithm.')
print('     1/r^3 is not on that list; it is the polar analogue of the second.')

# ---------------------------------------------------------------------------
head(3, 'INDEX THEORY: EVERY CLOSED ORBIT ENCIRCLES THE ORIGIN')
print('  Theorem 6.8.2, p. 180: any closed orbit in the phase plane must enclose')
print('  fixed points whose indices sum to +1. So a closed orbit avoiding the')
print('  origin would enclose nothing and sum to 0.\n')
MU = 0.5
mn, arg = None, None
for i in range(1, 801):
    r = 0.01 + 4.0*i/800
    for j in range(0, 720):
        th = TWOPI*j/720
        x, y = r*math.cos(th), r*math.sin(th)
        n = math.hypot(*F_xy_clean(x, y, MU))
        if mn is None or n < mn: mn, arg = n, (r, th)
print('     mu = %.2f, scan r in (0.01, 4] x theta on 800 x 720' % MU)
print('     min |F| = %.6f at r = %.3f' % (mn, arg[0]))
check(mn > 1e-3, 'the field has no zero off the origin, so the origin is the only one')

def index_on_circle(rad, mu, n=20000):
    tot, prev = 0.0, None
    for j in range(n + 1):
        th = TWOPI*j/n
        fx, fy = F_xy_clean(rad*math.cos(th), rad*math.sin(th), mu)
        a = math.atan2(fy, fx)
        if prev is not None:
            d = a - prev
            while d > math.pi: d -= TWOPI
            while d < -math.pi: d += TWOPI
            tot += d
        prev = a
    return tot / TWOPI

print()
print('     %10s %14s' % ('circle r', 'index'))
ok_ix = True
for rad in (0.05, 0.3, 1.0, 2.0, 5.0):
    ix = index_on_circle(rad, MU)
    print('     %10.2f %14.9f' % (rad, ix))
    if abs(ix - 1.0) > 1e-6: ok_ix = False
check(ok_ix, 'the index is +1 on every circle about the origin, inside and out')
print('\n     Origin has index +1, it is the only fixed point, and a closed orbit')
print('     must total +1. So every closed orbit encircles it -- and therefore')
print('     any two of them are nested, with an annulus between them in r > 0.')

# ---------------------------------------------------------------------------
head(4, 'EXACTLY ONE, FOR |mu| < 1')
print('  Dulac as Strogatz states it (p. 204) needs a SIMPLY CONNECTED region and')
print('  concludes "no closed orbits". r > 0 is not simply connected, and there')
print('  IS a closed orbit, so that statement does not apply as written. What')
print('  applies is one extra line of his own proof:\n')
print('      if C1 lies inside C2, both closed orbits, and the annulus A between')
print('      them lies in R, then Green\'s theorem gives')
print('          int_A div(gF) dA  =  oint_{C2} g F.n  -  oint_{C1} g F.n  =  0,')
print('      because F is tangent to each orbit. If div(gF) has one sign on R')
print('      the left side cannot vanish. So R holds AT MOST ONE closed orbit.\n')
print('  That is not the theorem printed on p. 204; it is p. 204\'s proof applied')
print('  to an annulus instead of a disc, and it is what gives uniqueness.\n')
print('  Existence for |mu| < 1 is Example 7.3.1 and was checked in WP-122.')
print('  Corroboration: integrate from many starts and see one curve.\n')

def rk4_xy(x, y, mu, T, n):
    h = T/n
    def f(s):
        return F_xy_clean(s[0], s[1], mu)
    s = [x, y]
    for _ in range(n):
        k1 = f(s)
        k2 = f([s[0]+h/2*k1[0], s[1]+h/2*k1[1]])
        k3 = f([s[0]+h/2*k2[0], s[1]+h/2*k2[1]])
        k4 = f([s[0]+h*k3[0],   s[1]+h*k3[1]])
        s = [s[0] + h/6*(k1[0]+2*k2[0]+2*k3[0]+k4[0]),
             s[1] + h/6*(k1[1]+2*k2[1]+2*k3[1]+k4[1])]
    return s

print('     %6s %34s %14s' % ('mu', 'r on the +x axis after 60 turns', 'spread'))
ok_one = True
for mu in (0.2, 0.5, 0.9):
    landed = []
    for r0 in (0.05, 0.3, 0.8, 1.2, 3.0):
        # integrate a whole number of turns: theta advances at rate 1
        x, y = rk4_xy(r0, 0.0, mu, 60*TWOPI, 240000)
        landed.append(math.hypot(x, y))
    spread = max(landed) - min(landed)
    print('     %6.1f %34s %14.2e' % (mu, '  '.join('%.6f' % v for v in landed[:3]) + ' ...', spread))
    if spread > 1e-6: ok_one = False
check(ok_one, 'every start lands on the same curve: one attractor, to 1e-6')
print('     Integration is corroboration, not the proof. The proof is index')
print('     theory plus the annulus argument above, and it covers every |mu| < 1')
print('     at once, which no finite set of trajectories can.')

# ---------------------------------------------------------------------------
head(5, "THE RADIAL-ONLY COUNT, AND THE TWO TOY MODELS DIFFER")
print('  When r\' depends on r alone and theta\' > 0, a closed orbit needs r')
print('  periodic; r is monotone wherever r\' is nonzero, and a monotone periodic')
print('  function is constant. So the closed orbits are exactly the circles')
print('  r = root of f in r > 0. No Dulac needed, and the count is exact.\n')

f_cub = lambda r: r - r**3
f_sat = lambda r: -2.0*(r - 1.0)/(1.0 + (r - 1.0)**2)
print('  BOOK 6, r\' = f(r)(1 - e^{-z}): the modulation is a positive factor for')
print('  z > 0, so the roots are f\'s own.')
for nm, f in (('f_cub = r - r^3', f_cub), ('f_sat = -2(r-1)/(1+(r-1)^2)', f_sat)):
    roots = []
    N = 400000
    prev_r, prev_v = 1e-6, f(1e-6)
    for i in range(1, N+1):
        r = 1e-6 + 6.0*i/N
        v = f(r)
        if prev_v == 0.0 or prev_v*v < 0:
            roots.append(0.5*(prev_r + r))
        prev_r, prev_v = r, v
    print('     %-30s positive roots on (0, 6]: %s' % (nm, ['%.6f' % q for q in roots]))
    check(len(roots) == 1 and abs(roots[0] - 1.0) < 1e-4,
          '%s gives exactly one circular orbit, at r = 1' % nm.split('=')[0].strip())

print('\n  VOL II, r\' = r(1 - r^2) + a(r - 1) with a = 2 e^{-z}. Factorise:')
print('      r(1-r^2) + a(r-1)  =  -(r - 1)(r^2 + r - a)')
ok_fac = True
for a in (0.3, 1.0, 2.0, 5.0):
    for r in (0.2, 0.9, 1.7, 3.1):
        lhs = r*(1-r*r) + a*(r-1)
        rhs = -(r-1)*(r*r + r - a)
        if abs(lhs - rhs) > 1e-12: ok_fac = False
check(ok_fac, 'the factorisation is an identity, checked at 16 (a, r) pairs')
print('  so besides r = 1 there is a second positive root,')
print('      r_2(a) = ( -1 + sqrt(1 + 4a) ) / 2,')
print('  and the radial eigenvalues are a - 2 at r = 1 and (1 - r_2) sqrt(1+4a)')
print('  at r = r_2.\n')
r2 = lambda a: (-1.0 + math.sqrt(1.0 + 4.0*a))/2.0
def dfa(r, a, h=1e-7):
    g = lambda q: q*(1-q*q) + a*(q-1)
    return (g(r+h) - g(r-h))/(2*h)
print('     %8s %10s %12s %16s %16s' % ('z', 'a=2e^-z', 'r_2', "f'(1) = a-2", "f'(r_2)"))
ok_eig = True
for z in (1.5, 0.75, 0.25, 0.0, -0.25, -0.75):
    a = 2.0*math.exp(-z)
    q = r2(a)
    e1, e2 = dfa(1.0, a), dfa(q, a)
    pred1, pred2 = a - 2.0, (1.0 - q)*math.sqrt(1.0 + 4.0*a)
    print('     %8.2f %10.6f %12.8f %16.9f %16.9f' % (z, a, q, e1, e2))
    if abs(e1 - pred1) > 1e-5 or abs(e2 - pred2) > 1e-5: ok_eig = False
    if abs(q*q + q - a) > 1e-12: ok_eig = False
check(ok_eig, 'both eigenvalue formulas hold, and r_2 solves r^2 + r - a = 0')
check(abs(r2(2.0) - 1.0) < 1e-15, 'r_2 = 1 exactly at a = 2, i.e. at z = 0')
check(dfa(1.0, 2.0) == 0.0 or abs(dfa(1.0, 2.0)) < 1e-6,
      'and the eigenvalue at Gamma vanishes there too')
print('\n     So Vol II\'s neutral line is not only a sign change: it is the')
print('     collision of two circular orbits, which exchange stability as they')
print('     pass through each other. That is a transcritical bifurcation of')
print('     cycles, and it has a name the eigenvalue statement does not carry.')
print('     For z > 0, r_2 < 1 is repelling and is the BASIN BOUNDARY of Gamma')
print('     in the frozen slice. Book 6\'s model has no such second orbit, so')
print('     the two toy models the series runs in parallel are not variants of')
print('     one another.')

# ---------------------------------------------------------------------------
head(6, 'A GUARD: r_2(z) TAKES EVERY VALUE IN (0, 1)')
print('  a = 2e^{-z} runs over (0, 2) as z runs over (0, infinity), and')
print('  r_2 = (-1 + sqrt(1+4a))/2 is strictly increasing in a with r_2 -> 0 and')
print('  r_2 -> 1 at the ends. So r_2 hits every number in (0,1) exactly once.\n')
print('     %14s %14s' % ('target', 'the z that gives it'))
ok_sweep = True
for target in (0.25, 0.5, 0.773, 0.882, 0.99):
    lo, hi = 1e-9, 60.0
    for _ in range(200):
        mid = 0.5*(lo+hi)
        if r2(2.0*math.exp(-mid)) > target: lo = mid
        else: hi = mid
    z = 0.5*(lo+hi)
    got = r2(2.0*math.exp(-z))
    print('     %14.6f %14.6f' % (target, z))
    if abs(got - target) > 1e-9: ok_sweep = False
check(ok_sweep, 'every target in (0,1) is attained, to 1e-9, at a unique z')
print('\n     Which is the point. A one-parameter family sweeping an interval will')
print('     pass through any stored constant of that interval, so a numerical')
print('     match between r_2(z) and a constant from elsewhere in the corpus is')
print('     not evidence of anything. It would become evidence only if the z at')
print('     which it matched were independently fixed. None is.')

# ---------------------------------------------------------------------------
head(7, 'AND THE 3-D FLOWS HAVE NO PERIODIC ORBIT TO BE UNIQUE')
print('  BOOK 6: z\' = 1 identically, so z(t) = z_0 + t is strictly increasing')
print('  and no trajectory returns to its starting point. The flow has no')
print('  periodic orbit at all. Gamma = {r = 1} is a helix, and a helix is a')
print('  closed orbit of the (r, theta) PROJECTION, not of the flow.')
check(True, 'z(t) = z_0 + t is injective, so no orbit of the Book 6 model closes')

print('\n  VOL II: z\' = r^2 - 2(r-1)^2 e^{-z}, which is 1 on Gamma. Scan a tube.')
zdot = lambda r, z: r*r - 2.0*(r-1.0)**2*math.exp(-z)
mn2, arg2 = None, None
for i in range(401):
    r = 0.6 + 0.8*i/400          # |r - 1| <= 0.4
    for j in range(401):
        z = 0.0 + 12.0*j/400     # z >= 0
        v = zdot(r, z)
        if mn2 is None or v < mn2: mn2, arg2 = v, (r, z)
print('     min z\' over |r-1| <= 0.4, z in [0, 12]  =  %.6f  at (r, z) = (%.3f, %.2f)'
      % (mn2, arg2[0], arg2[1]))
check(mn2 > 0, 'z\' is strictly positive on that tube, so no periodic orbit lies in it')
print('     The bound is analytic too: r^2 >= (1-d)^2 and 2(r-1)^2 e^{-z} <= 2d^2')
print('     for z >= 0, and (1-d)^2 > 2d^2 whenever d < 1/(1+sqrt2) = %.6f.'
      % (1.0/(1.0+math.sqrt(2.0))))
check(0.4 < 1.0/(1.0+math.sqrt(2.0)), 'd = 0.4 is inside that range')
print('     Outside the tube z\' does change sign for Vol II, so this is a')
print('     statement about a neighbourhood of Gamma and not about the whole')
print('     flow. Book 6\'s z\' = 1 needs no neighbourhood.')

# ---------------------------------------------------------------------------
head(8, 'CONTROL: THIS SCRIPT COMPUTED SOMETHING')
check(abs(index_on_circle(1.0, 0.0) - 1.0) < 1e-6, 'the winding integrator ran')
check(abs(divgF_analytic(1.0, 0.0, 0.0) + 2.0) < 1e-12,
      'div(gF) at r = 1, mu = 0 is -2, which is -(1/1)(1+1)')
check(abs(r2(6.0) - 2.0) < 1e-12, 'r_2(6) = (-1+5)/2 = 2, by hand')
check(mn > 0 and mn2 is not None, 'both grid scans found something rather than nothing')
print('    A vacuous pass is a pass. Block [8] exists so that block [3] cannot')
print('    report an index of +1 by having summed no angles.')

# ---------------------------------------------------------------------------
head('HONESTY', 'What this establishes, and what it must not be read as.')
print("""
  ESTABLISHED. For Strogatz Example 7.3.1, g = 1/r^3 makes div(gF) strictly
  negative on all of r > 0 exactly when |mu| < 1, checked against numerical
  differentiation and scanned over a grid; it changes sign at mu = 1.5. The
  field has no zero off the origin and the index on every circle about the
  origin is +1, so by Theorem 6.8.2 every closed orbit encircles it and any two
  are nested. With Green's theorem on the annulus between them, that gives at
  most one closed orbit; with Example 7.3.1's trapping annulus it gives exactly
  one, for every |mu| < 1. For radial-only fields the count is exact and needs
  no Dulac: Book 6's two canonical closures each have exactly one positive root,
  and Vol II's frozen slice factorises as -(r-1)(r^2 + r - a) and has two
  circular orbits, r = 1 and r_2 = (-1 + sqrt(1+4a))/2, with radial eigenvalues
  a - 2 and (1 - r_2)sqrt(1+4a), colliding and exchanging stability at a = 2,
  i.e. at z = 0. r_2(z) attains every value in (0,1) exactly once. Book 6's
  z' = 1 rules out periodic orbits outright; Vol II's z' is positive on the
  tube |r - 1| <= 0.4, z >= 0.

  NOT ESTABLISHED. Nothing here is a uniqueness result for the corpus's own
  three-dimensional flows, because those have no periodic orbits for it to be
  about -- which is itself the finding of block [7], not a gap in the method.
  The annulus form of Dulac used in block [4] is NOT the theorem printed on
  Strogatz p. 204; it is that theorem's proof applied to an annulus, stated
  here with its one extra line, and a reader should check that line rather than
  take it on the citation. The integrations in [4] are corroboration and cover
  three values of mu; the theorem covers all of them. The grid scans in [2],
  [3] and [7] are exhaustions over finite boxes and are evidence, with the
  analytic inequality printed beside each.

  AND ON r_2. It is elementary, it falls out of a factorisation anyone can do,
  and the corpus does not have it: the string sqrt(1+8e^{-z}) appears nowhere,
  nor does any second circular orbit. Block [6] exists so that it does not now
  get matched to r_star or to kappa* on the strength of a decimal agreement.
  A family that sweeps an interval meets every constant in it.
""")

print('=' * 70)
if fails:
    print('  %d CHECK(S) FAILED' % len(fails))
    for f in fails: print('    - ' + f)
    print('=' * 70); sys.exit(1)
print('  ALL CHECKS PASSED')
print('=' * 70)
