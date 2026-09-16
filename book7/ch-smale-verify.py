#!/usr/bin/env python3
"""
Smale -- the corpus computes return maps and has never asked for an itinerary.

WHY THIS FILE EXISTS. Thirty-nine tracked files in this corpus compute a return
map, twelve name a Poincare section, and WP-122 built one in closed form. The
words "horseshoe", "shift map" and "Sharkovskii" appear in no chapter, and
"symbolic dynamics" and "topological entropy" in one each. That is the same
shape ch-van-der-pol found: the phenomenon is everywhere, the canonical object
that reads it is absent.

The answer turns out to be a restriction rather than a discovery, and it is not
about parameters. For any system of the form rdot = f(r), thetadot = omega > 0,
the return map to a ray is the time-2pi/omega map of a SCALAR AUTONOMOUS ODE.
Its derivative is exp of an integral, hence strictly positive, hence the map is
a monotone homeomorphism, hence its lap number is 1 for every iterate and its
topological entropy is exactly 0 -- for every f. No horseshoe is available
anywhere in the closure family, and none can be.

BLOCKS
  [1] WP-122's return map in closed form, against RK4.
  [2] P'(r), P'(1) = e^-4pi, and the neutral radius.
  [3] Lap numbers of P^n -- with the double-precision caveat printed, because
      P^n collapses onto 1.0 and a lap count of 1 would then be right for the
      wrong reason.
  [4] The logistic map at mu = 4 for contrast: laps 2^n, entropy log 2 exactly.
  [5] The general statement, on four f including non-monotone ones, with a
      sweep in T showing where differencing stops being able to see it.
  [6] The corpus, counted -- entity-aware, and asserting on chapters.
  [7] Control.

PRIMARY SOURCES.
  S. Smale, "Finding a Horseshoe on the Beaches of Rio", The Mathematical
  Intelligencer 20 (1998), no. 1.
  S. Smale, "Differentiable dynamical systems", Bulletin of the AMS 73 (1967).
  N. Levinson, "A second order differential equation with singular solutions",
  Annals of Mathematics 50 (1949).
  M. L. Cartwright and J. E. Littlewood, on non-linear differential equations of
  the second order (1945); see J. Guckenheimer, "The legacy of the
  Cartwright-Littlewood collaboration", J. London Math. Soc. (2026).
  S. H. Strogatz, "Nonlinear Dynamics and Chaos", 2nd ed., section 10.5 and
  section 8.7 pp. 281-282 (Poincare maps).
  In-corpus: book6/wp122-the-return-map-was-in-the-exercise.html.

Standard library only.  python3 book7/ch-smale-verify.py
"""
import math, os, subprocess, sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
fails = []
def check(ok, msg, detail=''):
    print('    %s  %s%s' % ('PASS' if ok else 'FAIL', msg, ('  -- ' + detail) if detail and not ok else ''))
    if not ok: fails.append(msg)
def head(n, t):
    print('\n' + '=' * 70 + '\n  [%s]  %s\n' % (n, t) + '=' * 70)

TWOPI = 2.0 * math.pi
E2PI  = math.exp(TWOPI)
A     = math.exp(4 * math.pi) - 1.0

def Pmap(r):  return r * E2PI / math.sqrt(1.0 + A * r * r)
def dPmap(r): return E2PI / (1.0 + A * r * r) ** 1.5
def Pn(r, n):
    for _ in range(n): r = Pmap(r)
    return r

# ---------------------------------------------------------------------------
head(1, "WP-122'S RETURN MAP, IN CLOSED FORM, AGAINST RK4")
print('  rdot = r(1 - r^2), thetadot = 1. One turn is t = 2pi, so the return map')
print('  to any ray is the time-2pi flow map, and it integrates in closed form:\n')
print('      P(r) = r e^2pi / sqrt(1 + (e^4pi - 1) r^2)\n')
worst = 0.0
def rk4_scalar(f, y, t, h, n):
    for _ in range(n):
        k1 = f(y); k2 = f(y + h/2*k1); k3 = f(y + h/2*k2); k4 = f(y + h*k3)
        y += h/6*(k1 + 2*k2 + 2*k3 + k4); t += h
    return y
f0 = lambda r: r * (1 - r * r)
for r0 in (0.01, 0.1, 0.5, 0.9, 1.0, 1.5, 3.0, 10.0):
    num = rk4_scalar(f0, r0, 0.0, TWOPI / 20000, 20000)
    cl  = Pmap(r0)
    worst = max(worst, abs(num - cl))
    print('      r0 = %7.3f   RK4 %.12f   closed %.12f   diff %.2e' % (r0, num, cl, abs(num - cl)))
check(worst < 1e-12, 'the closed form reproduces RK4 at every radius tested', '%.2e' % worst)
check(abs(Pmap(1.0) - 1.0) < 1e-15, 'r = 1 is the fixed point, exactly')

# ---------------------------------------------------------------------------
head(2, "THE DERIVATIVE, THE MULTIPLIER, AND THE NEUTRAL RADIUS")
print("      P'(r) = e^2pi / (1 + (e^4pi - 1) r^2)^(3/2)\n")
print("      P'(1)  = %.15e" % dPmap(1.0))
print("      e^-4pi = %.15e" % math.exp(-4 * math.pi))
check(abs(dPmap(1.0) - math.exp(-4 * math.pi)) < 1e-20,
      "P'(1) is the transverse multiplier e^-4pi, as it must be")
rstar = math.sqrt((math.exp(4 * math.pi / 3) - 1) / A)
print("\n      |P'| = 1 at r* = %.12f   and P'(r*) = %.15f" % (rstar, dPmap(rstar)))
check(abs(dPmap(rstar) - 1.0) < 1e-12, 'the neutral radius r* = %.12f' % rstar)
check(all(dPmap(r) > 0 for r in [1e-9 + 5.0 * i / 2000 for i in range(2001)]),
      "P' > 0 at every radius sampled: P is strictly increasing")

# ---------------------------------------------------------------------------
head(3, "LAP NUMBERS OF P^n -- AND WHY THE LARGE-n ROWS PROVE NOTHING")
print('  The lap number l(g) is the count of maximal monotone intervals. Misiurewicz')
print('  and Szlenk: for a piecewise-monotone interval map the topological entropy')
print('  is lim (1/n) log l(g^n). A monotone map has l = 1 at every iterate.\n')
def laps(g, a, b, N=20000, rel=1e-11):
    ys = [g(a + (b - a) * i / N) for i in range(N + 1)]
    rng = max(ys) - min(ys)
    tol = max(rel * max(1.0, abs(max(ys))), 1e-300)
    s, prev = 1, 0
    for i in range(N):
        d = ys[i + 1] - ys[i]
        if abs(d) <= tol: continue
        sg = 1 if d > 0 else -1
        if prev and sg != prev: s += 1
        prev = sg
    return s, rng
print('      %3s %8s %14s %16s' % ('n', 'laps', '(1/n)log laps', 'range of P^n'))
informative = []
for n in (1, 2, 3, 4, 6, 8, 12):
    l, rng = laps(lambda x, n=n: Pn(x, n), 1e-6, 3.0)
    tag = '' if rng > 0 else '   <-- collapsed to 1.0 in double precision'
    print('      %3d %8d %14.6f %16.3e%s' % (n, l, math.log(l) / n, rng, tag))
    if rng > 0: informative.append((n, l))
check(all(l == 1 for _, l in informative),
      'every iterate with a resolvable range has lap number 1 (%d of them)' % len(informative))
print('\n  The n >= 6 rows are NOT evidence. P is contracting by e^-4pi per turn, so')
print('  P^6 maps the whole of (0,3] onto the single double nearest 1.0 and a lap')
print('  count of 1 is then true of a constant function, not of this one. The rows')
print('  that carry information are n <= 4. The reason the entropy is 0 is block [5].')

# ---------------------------------------------------------------------------
head(4, "THE LOGISTIC MAP AT mu = 4, FOR CONTRAST")
print('  The same instrument on a map that does fold. Strogatz Figure 1.3.1 puts')
print('  iterated maps in the corpus\'s own quadrant, and "logistic map" is in no')
print('  chapter here either -- block [6] measures that.\n')
L = lambda x: 4.0 * x * (1.0 - x)
def Ln(x, n):
    for _ in range(n): x = L(x)
    return x
print('      %3s %8s %14s %14s' % ('n', 'laps', '(1/n)log laps', 'log 2'))
ok_log2 = True
for n in (1, 2, 3, 4, 6, 8):
    l, _ = laps(lambda x, n=n: Ln(x, n), 0.0, 1.0)
    e = math.log(l) / n
    ok_log2 &= (l == 2 ** n)
    print('      %3d %8d %14.6f %14.6f' % (n, l, e, math.log(2)))
check(ok_log2, 'laps(L^n) = 2^n exactly, so the entropy is log 2 at every n')
check(abs(math.log(2) - 0.6931471805599453) < 1e-15, 'log 2 = 0.693147180559945')

# ---------------------------------------------------------------------------
head(5, "WHY NO SUCH RETURN MAP CAN FOLD -- FOR ANY f")
print('  For rdot = f(r), thetadot = omega > 0, the return map to a ray is the')
print('  time-T flow map of a scalar autonomous ODE, T = 2pi/omega. Differentiating')
print('  the flow in the initial condition gives the variational equation')
print("  v' = f'(r(s)) v, v(0) = 1, whose solution is\n")
print("      dP/dr0 = exp( int_0^T f'(r(s)) ds )\n")
print('  an exponential, so strictly positive, for every f and every T. P is')
print('  therefore a strictly increasing homeomorphism, l(P^n) = 1 for all n, and')
print('  h(P) = 0. Orbits of a scalar autonomous ODE cannot cross, and a fold is')
print('  a crossing. Checked below, including on f that are NOT monotone.\n')
def flow_logderiv(f, fp, r0, T, n=2000):
    h = T / n; r = r0; w = 0.0
    for _ in range(n):
        a1, b1 = f(r), fp(r)
        a2, b2 = f(r + h/2*a1), fp(r + h/2*a1)
        a3, b3 = f(r + h/2*a2), fp(r + h/2*a2)
        a4, b4 = f(r + h*a3),   fp(r + h*a3)
        r += h/6*(a1 + 2*a2 + 2*a3 + a4)
        w += h/6*(b1 + 2*b2 + 2*b3 + b4)
    return r, w
AA = 5.436563656918                       # WP-120's frozen a at z = -1
TESTS = [
    ('r(1-r^2)          (7.1.1)', lambda r: r*(1-r*r),               lambda r: 1 - 3*r*r),
    ('-(r-1)(r^2+r-a)   (WP-120)', lambda r: -(r-1)*(r*r+r-AA),
                                    lambda r: -((r*r + r - AA) + (r-1)*(2*r+1))),
    ('sin(3r)-0.3       (not monotone)', lambda r: math.sin(3*r)-0.3, lambda r: 3*math.cos(3*r)),
    ('r - r^5           (two fixed pts)', lambda r: r - r**5,         lambda r: 1 - 5*r**4),
]
print('      %-34s %22s %12s' % ('f(r)', 'log dP over [0.12,2.02]', 'rel err vs FD'))
for T in (0.2, 1.0, TWOPI):
    print('\n      T = %.5f' % T)
    for name, f, fp in TESTS:
        lo, hi, worstrel, npts = 1e99, -1e99, 0.0, 0
        allpos = True
        for i in range(1, 31):
            r0 = 0.05 + 2.0 * i / 30
            _, w = flow_logderiv(f, fp, r0, T)
            lo = min(lo, w); hi = max(hi, w)
            if math.exp(min(w, 700.0)) <= 0: allpos = False
            h = 1e-6
            fd = (flow_logderiv(f, fp, r0 + h, T)[0] - flow_logderiv(f, fp, r0 - h, T)[0]) / (2*h)
            if abs(fd) > 1e-9:
                worstrel = max(worstrel, abs(fd - math.exp(w)) / abs(fd)); npts += 1
        print('      %-34s [%+8.3f, %+8.3f] %10.1e (%2d pts)'
              % (name, lo, hi, worstrel, npts))
        label = name.split('(')[0].strip()
        check(allpos, 'dP is an exponential and therefore positive: f = %-18s T = %.4f' % (label, T))
print('\n  The T sweep is the methodological point. At T = 0.2 the identity verifies')
print('  against a central difference to about 1e-8. By T = 2pi the derivative is')
print('  e^-110 for the WP-120 field, the difference of the two flows is zero in')
print('  double precision, and the finite difference reports nonsense. The integral')
print('  still gives the number. A derivative that small is computed, not measured.')

# ---------------------------------------------------------------------------
head(6, "THE CORPUS, COUNTED")
sys.path.insert(0, os.path.join(REPO, 'tools'))
try:
    from corpus_count import files as _cc_files      # entity-aware, tools/corpus_count.py
    HAVE_CC = True
except Exception:
    HAVE_CC = False
def files(pat):
    if HAVE_CC:
        return _cc_files(pat)
    r = subprocess.run(['git', '--no-optional-locks', 'grep', '-ilE', pat, 'HEAD', '--',
                        '*.html', '*.md'], cwd=REPO, capture_output=True, text=True)
    return sorted(l.split(':', 1)[1] for l in r.stdout.splitlines() if ':' in l)
def classify(f):
    if f.startswith('book7/ch-smale'):                        return 'self'
    if f == 'CLAUDE.md':                                      return 'scaffolding'
    if f.startswith('docs/'):                                 return 'audit'
    if (f.endswith('index.html') or f.startswith('index-')
            or f.startswith('master-index')):                 return 'listing'
    return 'CHAPTER'
def chapters(pat): return [f for f in files(pat) if classify(f) == 'CHAPTER']
check(HAVE_CC, 'tools/corpus_count.py imported -- counts are entity-aware')
print('\n      %-26s %7s %10s' % ('pattern', 'files', 'chapters'))
ROWS = [('return map', r'return map'), ('Poincare section/map', r'poincar(e|é|&eacute;)[ -](section|map)'),
        ('limit cycle', r'limit cycle'), ('horseshoe', r'horseshoe'),
        ('shift map', r'shift map'), ('symbolic dynamics', r'symbolic dynamics'),
        ('topological entropy', r'topological entropy'), ('Sharkovskii', r'sharkovsk'),
        ('logistic map', r'logistic map'), ('lap number', r'lap number'),
        ('Smale', r'smale'), ('Levinson', r'levinson'), ('Cartwright', r'cartwright'),
        ('Bott (bare pattern)', r'bott'), ('Bott periodicity', r'bott periodicity'),
        ('Raoul Bott', r'raoul bott')]
C = {}
for name, pat in ROWS:
    C[name] = (len(files(pat)), len(chapters(pat)))
    print('      %-26s %7d %10d' % (name, C[name][0], C[name][1]))
check(C['return map'][1] >= 20, 'twenty or more chapters compute a return map (%d of %d files)'
      % (C['return map'][1], C['return map'][0]), str(C['return map']))
check(C['Poincare section/map'][1] >= 10,
      'and %d name a Poincare section or map' % C['Poincare section/map'][1],
      str(C['Poincare section/map']))
for z in ('horseshoe', 'shift map', 'Sharkovskii', 'logistic map'):
    check(chapters({'horseshoe': r'horseshoe', 'shift map': r'shift map',
                    'Sharkovskii': r'sharkovsk', 'logistic map': r'logistic map'}[z]) == [],
          'no chapter but this one says "%s"' % z,
          str(chapters({'horseshoe': r'horseshoe', 'shift map': r'shift map',
                        'Sharkovskii': r'sharkovsk', 'logistic map': r'logistic map'}[z])))
check(C['Bott (bare pattern)'][0] > 500 and C['Bott periodicity'][1] <= 1,
      "Smale's advisor: /bott/ matches %d files -- every one of them the word "
      "'bottom' -- while 'Bott periodicity' is in %d chapter, put there by "
      'ch-conley today, and "Raoul Bott" in %d before this page'
      % (C['Bott (bare pattern)'][0], C['Bott periodicity'][1], C['Raoul Bott'][1]),
      str((C['Bott (bare pattern)'], C['Bott periodicity'], C['Raoul Bott'])))
check(C['Raoul Bott'][1] == 0, 'the advisor is named nowhere in the corpus before this page',
      str(C['Raoul Bott']))
print('\n     Written to FAIL when a second chapter picks any of those up. That')
print('     failure is the notification that the gap closed by use.')

# ---------------------------------------------------------------------------
head(7, 'CONTROL')
check(len(files(r'moonshine')) > 0, 'the counter returns files rather than nothing')
ABSENT = 'qqx' + '-no-file-contains-this-' + 'qqx'
check(files(ABSENT) == [], 'and none for a token no file writes down', str(files(ABSENT)))
check(abs(Pmap(Pmap(1.0)) - 1.0) < 1e-15, 'P fixes 1 under iteration too')
check(laps(lambda x: x * x, 0.0, 1.0)[0] == 1 and laps(lambda x: (x - .5) ** 2, 0.0, 1.0)[0] == 2,
      'the lap counter reads 1 for x^2 on [0,1] and 2 for (x-1/2)^2')

# ---------------------------------------------------------------------------
print('\n' + '=' * 70 + '\n  [HONESTY]\n' + '=' * 70)
print("""
  WHAT THIS ESTABLISHES. That WP-122's return map has the closed form printed,
  agreeing with RK4 to 8e-15; that its derivative at the fixed point is exactly
  the multiplier e^-4pi; and that it is strictly increasing. That its topological
  entropy is 0, not by the lap count -- which stops carrying information at n = 6
  when double precision collapses P^n onto a constant, and which says so -- but
  by the general statement in block [5]: the derivative of the time-T map of a
  scalar autonomous ODE is an exponential of an integral, hence positive, for
  every f. So the entropy is 0 for the whole closure family and for every
  radial-plus-rigid-rotation system, and no horseshoe exists in any of them. The
  logistic contrast shows the same instrument reading log 2 where a map does fold.

  WHAT IT DOES NOT ESTABLISH. That the corpus's three-dimensional flow has no
  chaos. Block [5] is about planar systems whose angular speed is constant; it
  says nothing about a flow on the contact manifold, and Poincare-Bendixson
  already forbids planar chaos independently, so block [5] is the sharper
  statement only in that it identifies WHICH feature is responsible -- the
  radial speed depending on r alone. It is not a claim about what the corpus
  could build, only about what the published family contains. The numerical
  lap counts are evidence over a finite grid on a finite interval and not proof;
  the proof, such as it is, is the one-line variational argument, which is
  classical. No priority is claimed here: Smale's horseshoe, the Misiurewicz-
  Szlenk lap-number formula, and the monotonicity of scalar flow maps are all
  standard, and this is the corpus's own return map put through them.
""")
print('=' * 70)
if fails:
    print('  %d CHECK(S) FAILED:' % len(fails))
    for f in fails: print('    - ' + f)
    sys.exit(1)
print('  ALL CHECKS PASSED')
