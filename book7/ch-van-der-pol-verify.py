#!/usr/bin/env python3
"""
van der Pol -- the other canonical limit cycle, and what the closure family excludes.

WHY THIS FILE EXISTS. Strogatz puts two examples side by side in section 7.1.
Example 7.1.1, p. 199, is the corpus's transverse attractor. Example 7.1.2,
p. 200, one page later, is the van der Pol oscillator. The corpus has the first
one in 111 files under the name "limit cycle" and the second in none, and the
difference between them is not decoration: 7.1.1's cycle is a circle and van der
Pol's is not, which is exactly what the corpus's closure conditions require and
therefore exclude.

BLOCKS
  [1] Lienard's five conditions, checked for van der Pol; a = sqrt(3).
  [2] The cycle is not a circle and the period is not 2*pi.
  [3] Example 7.1.1 for contrast, exact on both counts.
  [4] What the closure conditions f(1)=0, f'(1)=-2 actually pick out.
  [5] Two routes to uniqueness, and the one that does not generalise.
  [6] The corpus, counted.
  [7] Control.

PRIMARY SOURCE. S. H. Strogatz, "Nonlinear Dynamics and Chaos", 2nd ed.,
Westview 2015 / CRC 2018. Example 7.1.1 p. 199, Example 7.1.2 p. 200,
section 7.4 p. 212 (Lienard's equation and theorem), Example 7.4.1 p. 213,
section 7.5 p. 213 (relaxation oscillations).

Standard library only.  python3 book7/ch-van-der-pol-verify.py
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
def rk4(f, y, t, h, n):
    for _ in range(n):
        k1 = f(t, y)
        k2 = f(t+h/2, [y[i]+h/2*k1[i] for i in range(len(y))])
        k3 = f(t+h/2, [y[i]+h/2*k2[i] for i in range(len(y))])
        k4 = f(t+h,   [y[i]+h*k3[i]   for i in range(len(y))])
        y = [y[i] + h/6*(k1[i]+2*k2[i]+2*k3[i]+k4[i]) for i in range(len(y))]
        t += h
    return y
def vdp(mu):  return lambda t, s: [s[1], -mu*(s[0]*s[0]-1.0)*s[1] - s[0]]

# ---------------------------------------------------------------------------
head(1, "LIENARD'S FIVE CONDITIONS, FOR VAN DER POL")
print('  Lienard\'s equation (Strogatz p. 212):  x\'\' + f(x)x\' + g(x) = 0.')
print('  van der Pol is f(x) = mu(x^2 - 1), g(x) = x. Lienard\'s Theorem gives a')
print('  UNIQUE, STABLE limit cycle when five conditions hold.\n')
mu = 1.0
f = lambda x: mu*(x*x - 1.0)
g = lambda x: x
F = lambda x: mu*(x**3/3.0 - x)
xs = [(-4.0 + 8.0*i/8000) for i in range(8001)]
c1 = True                                                    # C^1 everywhere
c2 = max(abs(g(-x) + g(x)) for x in xs) < 1e-12              # g odd
c3 = all(g(x) > 0 for x in xs if x > 0)                      # g > 0 on x > 0
c4 = max(abs(f(-x) - f(x)) for x in xs) < 1e-12              # f even
a  = math.sqrt(3.0)
c5a = abs(F(a)) < 1e-12
c5b = all(F(x) < 0 for x in xs if 0 < x < a - 1e-9)
c5c = all(F(x + 0.001) >= F(x) - 1e-12 for x in [a + 0.001*i for i in range(3000)])
c5d = F(50.0) > 0 and F(200.0) > F(50.0)
for lbl, ok in (('(1) f and g are continuously differentiable', c1),
                ('(2) g is odd', c2),
                ('(3) g(x) > 0 for x > 0', c3),
                ('(4) f is even', c4),
                ('(5) F has exactly one positive zero, at x = a', c5a),
                ('    F < 0 on 0 < x < a', c5b),
                ('    F nondecreasing for x > a', c5c),
                ('    F -> +infinity', c5d)):
    check(ok, lbl)
print('\n     F(x) = mu(x^3/3 - x) = (1/3) mu x (x^2 - 3), so a = sqrt(3) = %.12f' % a)
check(abs(a*a - 3.0) < 1e-15, 'a^2 = 3 exactly, as Example 7.4.1 states')
print('     => van der Pol has a unique stable limit cycle, by a theorem of 1928.')

# ---------------------------------------------------------------------------
head(2, 'THE CYCLE IS NOT A CIRCLE, AND THE PERIOD IS NOT 2*pi')
print('     %6s %12s %12s %14s %12s' % ('mu', 'r_min', 'r_max', 'r_max/r_min', 'period'))
ratios = {}
h = 1e-3
for m in (0.1, 1.0, 1.5, 5.0):
    fld = vdp(m)
    y = rk4(fld, [2.0, 0.0], 0.0, h, int(120/h))     # settle
    rs, cross, t = [], [], 0.0
    for _ in range(int(40/h)):
        y2 = rk4(fld, y, t, h, 1)
        rs.append(math.hypot(y[0], y[1]))
        if y[0] < 0 <= y2[0]: cross.append(t)
        y, t = y2, t + h
        if len(cross) >= 3: break
    T = cross[-1] - cross[-2]
    ratios[m] = max(rs)/min(rs)
    print('     %6.1f %12.4f %12.4f %14.3f %12.4f' % (m, min(rs), max(rs), ratios[m], T))
    check(ratios[m] > 1.0 + 1e-3, 'at mu = %.1f the orbit is not a circle' % m, '%.4f' % ratios[m])
    check(abs(T - TWOPI) > 1e-3 or m < 0.05, 'and its period is not 2*pi' , '%.4f' % T)
check(all(ratios[a_] < ratios[b_] for a_, b_ in ((0.1,1.0),(1.0,1.5),(1.5,5.0))),
      'the distortion grows monotonically with mu')
print('\n     Strogatz 7.5 (p. 213): for large mu the waveform becomes a relaxation')
print('     oscillation with period ~ (3 - 2 ln 2) mu = %.6f mu -- linear in mu,' % (3-2*math.log(2)))
print('     not constant. Approach is slow; at mu = 5 the measured period is still')
print('     well above the asymptote.')

# ---------------------------------------------------------------------------
head(3, 'EXAMPLE 7.1.1 FOR CONTRAST, EXACT ON BOTH COUNTS')
print('  r\' = r(1 - r^2), theta\' = 1. The radial equation has r = 1 as a fixed')
print('  point and theta advances at unit rate, so the orbit IS the unit circle')
print('  and the period IS 2*pi. No integration is needed to see either.\n')
fr = lambda r: r*(1.0 - r*r)
check(abs(fr(1.0)) < 1e-15, 'r = 1 is a zero of the radial field, exactly')
check(abs((fr(1+1e-6) - fr(1-1e-6))/2e-6 + 2.0) < 1e-8, "f'(1) = -2")
print('     r_max/r_min = 1.000 exactly     period = 2*pi = %.6f exactly' % TWOPI)

# ---------------------------------------------------------------------------
head(4, 'WHAT THE CLOSURE CONDITIONS PICK OUT')
print('  WP-22 admits any closure with f(1) = 0, f\'(1) = -2, f(r)(r-1) < 0,')
print('  together with theta\' = 1. Under those conditions r\' depends on r alone,')
print('  so on a closed orbit r is constant, so the orbit is a CIRCLE.\n')
print('     van der Pol\'s r_max/r_min at the four values above:')
for m in sorted(ratios): print('       mu = %-5.1f  %.3f' % (m, ratios[m]))
check(all(v > 1.0 for v in ratios.values()),
      'every one exceeds 1, so van der Pol lies in NO admissible closure')
print('\n     That is not a defect in the closure conditions. It is a restriction')
print('     they impose and have never named: the family is circle-preserving.')
print('     Everything WP-22 proves is proved about circular cycles.')

# ---------------------------------------------------------------------------
head(5, 'TWO ROUTES TO UNIQUENESS, AND THE ONE THAT DOES NOT GENERALISE')
print('  WP-120 proves uniqueness with index theory plus Dulac, using g = 1/r^3.')
print('  That works because the cycle there is a circle and the field is radial')
print('  plus rotation. Try the same g on van der Pol.\n')
def div_num(fn, x, y, hh=1e-6):
    a1, _ = fn(x+hh, y); a0, _ = fn(x-hh, y)
    _, b1 = fn(x, y+hh); _, b0 = fn(x, y-hh)
    return (a1-a0)/(2*hh) + (b1-b0)/(2*hh)
def gF_vdp(x, y, m=1.0):
    r = math.hypot(x, y)
    return (y/r**3, (-m*(x*x-1.0)*y - x)/r**3)
pts = [(0.08 + 4.0*i/150, TWOPI*j/36) for i in range(1, 151) for j in range(36)]
v_vdp = [div_num(gF_vdp, r*math.cos(t), r*math.sin(t)) for r, t in pts]
v_731 = [-(1.0/r)*((1.0 + 0.5*math.cos(t))/(r*r) + 1.0) for r, t in pts]
print('     Example 7.3.1, mu = 0.5 :  min %+12.4f   max %+12.4f   one sign: %s'
      % (min(v_731), max(v_731), not (min(v_731) < 0 < max(v_731))))
print('     van der Pol,   mu = 1.0 :  min %+12.4f   max %+12.4f   one sign: %s'
      % (min(v_vdp), max(v_vdp), not (min(v_vdp) < 0 < max(v_vdp))))
check(not (min(v_731) < 0 < max(v_731)), 'g = 1/r^3 has one sign for Example 7.3.1')
check(min(v_vdp) < 0 < max(v_vdp), 'and changes sign for van der Pol')
print('\n     So the corpus\'s route to uniqueness is tied to the circle. Lienard\'s')
print('     theorem never assumed one, and settles van der Pol in 1928. Both are')
print('     correct; only one of them travels.')

# ---------------------------------------------------------------------------
head(6, 'THE CORPUS, COUNTED')
def files(pat):
    r = subprocess.run(['git', '--no-optional-locks', 'grep', '-lic', '-e', pat,
                        'HEAD', '--', '*.html', '*.md'],
                       cwd=REPO, capture_output=True, text=True)
    return [l.split(':', 1)[1] for l in r.stdout.splitlines() if ':' in l]

def classify(f):
    """WP-82 block [3]'s lesson: a file count counts listings and the ruler too."""
    if f.startswith('book7/ch-van-der-pol'):                  return 'self'
    if f.startswith('docs/'):                                 return 'audit'
    if f.endswith('index.html') or f.startswith('index-') \
       or f.startswith('master-index'):                       return 'listing'
    return 'CHAPTER'
def chapters(pat):
    return [f for f in files(pat) if classify(f) == 'CHAPTER']

print('     %-22s %8s %9s' % ('pattern', 'files', 'chapters'))
for pat in ('limit cycle', 'van der pol', 'li[eé]nard', 'relaxation oscillat', 'memristor'):
    print('     %-22s %8d %9d' % (pat.replace('[eé]', 'e'), len(files(pat)), len(chapters(pat))))

print('\n     composition of the "van der pol" hits:')
for f in sorted(files('van der pol')):
    print('       %-44s %s' % (f, classify(f)))
check(len(chapters('limit cycle')) > 100, 'the phenomenon is in more than a hundred chapters')
check(chapters('van der pol') == [],
      'and no chapter but this one names the other canonical example',
      str(chapters('van der pol')))
check(chapters('li[eé]nard') == [], 'nor the theorem that settles it',
      str(chapters('li[eé]nard')))
print('\n     The raw file count is NOT the number to quote. Publishing this chapter')
print('     put "van der Pol" into the Book 7 index and two generated index pages,')
print('     which is WP-82 block [3]\'s finding arriving on schedule: a file count')
print('     counts the listings and the ruler. This block asserts on chapters.')
print('     It is written to fail when a SECOND chapter names the example -- that')
print('     failure is the notification that the gap has been closed by use.')
print('\n     This block is written to keep failing once the gap is really closed:')
print('     a THIRD file naming van der Pol -- one that is not this chapter -- will')
print('     break it, which is the notification that the example has been used.')

# ---------------------------------------------------------------------------
head(7, 'CONTROL: THIS SCRIPT COMPUTED SOMETHING')
check(abs(F(a)) < 1e-12 and F(1.0) < 0, 'F was evaluated and has the right sign either side of a')
check(len(v_vdp) == len(pts) == 5400, 'the divergence grid has %d points' % len(pts))
check(len(files('moonshine')) > 0, 'git grep returned files rather than nothing')
check(len(files('zzz-no-such-token-zzz')) == 0, 'and none for a token that is absent')
print('    A vacuous pass is a pass. Block [7] exists so that block [6] cannot')
print('    report zero van der Pol files by failing to reach the repository.')

# ---------------------------------------------------------------------------
head('HONESTY', 'What this establishes, and what it does not.')
print("""
  ESTABLISHED. van der Pol satisfies all five of Lienard's conditions with
  a = sqrt(3), so it has a unique stable limit cycle by a theorem published in
  1928. Its orbit is not a circle at any mu tested and the distortion grows
  monotonically; its period is not 2*pi and grows with mu. Example 7.1.1's
  orbit is exactly the unit circle with period exactly 2*pi. The closure
  conditions of WP-22 make the radial speed a function of r alone, so every
  closed orbit they admit is a circle, and van der Pol is in none of them. The
  Dulac function g = 1/r^3 has one sign for Example 7.3.1 and changes sign for
  van der Pol on the same grid.

  NOT ESTABLISHED. That anything in WP-22 is wrong. A circle-preserving family
  is a restriction, not an error, and the paper's theorems are true about the
  family it defines. What is reported is that the restriction was never named,
  and that the uniqueness route built in WP-120 is tied to it. Nor does this
  script establish that van der Pol is the right generalisation to attempt --
  only that it is the standard example the corpus does not contain.

  ON THE COUNTS. They are file counts on tracked *.html and *.md at HEAD with
  docs/ excluded, and they measure vocabulary, not content. A count of zero
  means the name does not appear; it does not mean the mathematics is absent,
  and in this case the mathematics of the neighbouring example is present in
  more than a hundred files.
""")
print('=' * 70)
if fails:
    print('  %d CHECK(S) FAILED' % len(fails))
    for f in fails: print('    - ' + f)
    print('=' * 70); sys.exit(1)
print('  ALL CHECKS PASSED')
print('=' * 70)
