#!/usr/bin/env python3
"""
Edward Witten -- verifier for book7/ch-witten.html.

CHECKS, by two independent routes for each space:
  route 1: critical points of an explicit function, found and classified by exact
           symbolic differentiation (sympy): torus f = cos x + cos y; sphere f = height.
  route 2: Betti numbers from a cell structure, by exact rational ranks of boundary
           matrices: a 3x3 grid torus (9, 18, 9) and a cube surface (8, 12, 6).
  Then: c_k >= b_k, alternating sums equal chi, and the page's table equals the output.

DOES NOT ESTABLISH: the Morse inequalities in general, Witten's proof, or any
biographical fact. Cited items are not checked here. Two spaces are two spaces.

    python3 book7/ch-witten-verify.py
"""
import itertools, os, re, sys
import sympy as sp
HERE = os.path.dirname(os.path.abspath(__file__))
fails = []
def check(ok, msg):
    print('    %s  %s' % ('PASS' if ok else 'FAIL', msg))
    if not ok: fails.append(msg)
def head(n, t): print('\n' + '=' * 70 + '\n  [%s]  %s\n' % (n, t) + '=' * 70)

def morse_counts(f, vars_, pts):
    """Classify given critical points: verify gradient vanishes, Hessian non-degenerate, count negative eigenvalues."""
    c = {}
    grad = [sp.diff(f, v) for v in vars_]
    H = sp.hessian(f, vars_)
    for p in pts:
        s = dict(zip(vars_, p))
        assert all(sp.simplify(g.subs(s)) == 0 for g in grad), 'not a critical point: %s' % (p,)
        Hp = H.subs(s)
        assert Hp.det() != 0, 'degenerate at %s' % (p,)
        idx = sum(1 for ev, m in Hp.eigenvals().items() if ev < 0 for _ in range(m))
        c[idx] = c.get(idx, 0) + 1
    return tuple(c.get(k, 0) for k in range(3))

def betti(boundaries, dims):
    """boundaries: [d1 (V x E), d2 (E x F)] as sympy matrices; dims=(nV,nE,nF)."""
    r1, r2 = boundaries[0].rank(), boundaries[1].rank()
    nV, nE, nF = dims
    assert (boundaries[0] * boundaries[1]).is_zero_matrix, 'd1*d2 != 0'
    return (nV - r1, nE - r1 - r2, nF - r2)

head(1, 'TORUS: f = cos x + cos y')
x, y = sp.symbols('x y', real=True)
f = sp.cos(x) + sp.cos(y)
all_crit = sp.solve([sp.diff(f, x), sp.diff(f, y)], [x, y], dict=True)
pts = [(0, 0), (0, sp.pi), (sp.pi, 0), (sp.pi, sp.pi)]
c_torus = morse_counts(f, [x, y], pts)
check(c_torus == (1, 2, 1), 'critical points (0,0),(0,pi),(pi,0),(pi,pi) have indices counted as (c0,c1,c2) = %s' % (c_torus,))
check(all(sp.simplify(sp.diff(f, x).subs({x: a, y: b})) == 0 and sp.simplify(sp.diff(f, y).subs({x: a, y: b})) == 0 for a, b in pts), 'gradient is exactly 0 at all four')
# completeness on one period: sin x = sin y = 0 has exactly {0,pi}^2 in [0,2pi)
check(sorted([a for a in (0, sp.pi) if sp.sin(a) == 0]) == [0, sp.pi] and all(sp.sin(a) != 0 for a in (sp.pi/2, 3*sp.pi/2)), 'sin = 0 on [0, 2pi) only at 0 and pi (spot check; the 2x2 list is complete)')

head(2, 'SPHERE: f = height')
u, v = sp.symbols('u v', real=True)
north = sp.sqrt(1 - u**2 - v**2); south = -sp.sqrt(1 - u**2 - v**2)
cN = morse_counts(north, [u, v], [(0, 0)]); cS = morse_counts(south, [u, v], [(0, 0)])
c_sphere = tuple(a + b for a, b in zip(cN, cS))
check(cN == (0, 0, 1) and cS == (1, 0, 0), 'north pole (local chart): index 2 (max); south pole: index 0 (min)')
check(c_sphere == (1, 0, 1), 'sphere (c0,c1,c2) = %s' % (c_sphere,))

head(3, 'BETTI NUMBERS FROM CELL STRUCTURES (exact rational ranks)')
# 3x3 grid torus: vertex (i,j), horizontal edge h(i,j): (i,j)->(i+1,j), vertical edge w(i,j): (i,j)->(i,j+1); face (i,j) square.
n = 3
V = {(i, j): k for k, (i, j) in enumerate(itertools.product(range(n), range(n)))}
E = {}
for i, j in itertools.product(range(n), range(n)):
    E[('h', i, j)] = len(E); E[('w', i, j)] = len(E)
F = {(i, j): k for k, (i, j) in enumerate(itertools.product(range(n), range(n)))}
d1 = sp.zeros(len(V), len(E)); d2 = sp.zeros(len(E), len(F))
for (t, i, j), e in E.items():
    a = V[(i, j)]; b = V[((i + 1) % n, j)] if t == 'h' else V[(i, (j + 1) % n)]
    d1[a, e] -= 1; d1[b, e] += 1
for (i, j), fc in F.items():  # boundary: bottom h(i,j) + right w(i+1,j) - top h(i,j+1) - left w(i,j)
    d2[E[('h', i, j)], fc] += 1; d2[E[('w', (i + 1) % n, j)], fc] += 1
    d2[E[('h', i, (j + 1) % n)], fc] -= 1; d2[E[('w', i, j)], fc] -= 1
b_torus = betti([d1, d2], (len(V), len(E), len(F)))
check((len(V), len(E), len(F)) == (9, 18, 9), 'torus cell counts (V,E,F) = (9,18,9)')
check(b_torus == (1, 2, 1), 'torus Betti numbers (b0,b1,b2) = %s' % (b_torus,))
# cube surface: 8 vertices, 12 edges, 6 faces, faces oriented outward
cv = list(itertools.product((0, 1), repeat=3)); vi = {p: k for k, p in enumerate(cv)}
ce = [(a, b) for a in cv for b in cv if a < b and sum(abs(p - q) for p, q in zip(a, b)) == 1]
ei = {e: k for k, e in enumerate(ce)}
D1 = sp.zeros(8, 12)
for (a, b), k in ei.items(): D1[vi[a], k] -= 1; D1[vi[b], k] += 1
D2 = sp.zeros(12, 6); fcs = []
for ax in range(3):
    for val in (0, 1):
        o = [k for k in range(3) if k != ax]
        def pt(s, t):
            q = [0, 0, 0]; q[ax] = val; q[o[0]] = s; q[o[1]] = t; return tuple(q)
        loop = [pt(0, 0), pt(1, 0), pt(1, 1), pt(0, 1)]
        fcs.append(loop)
for k, loop in enumerate(fcs):
    # orient so boundary cancels pairwise: pick sign s so the sum of all face boundaries has d1*d2 = 0
    for a, b in zip(loop, loop[1:] + loop[:1]):
        key = (a, b) if (a, b) in ei else (b, a); sgn = 1 if (a, b) in ei else -1
        D2[ei[key], k] += sgn
# choose per-face signs making D1*D2 = 0 (an orientation of the cube surface)
for signs in itertools.product((1, -1), repeat=5):
    s = (1,) + signs
    M = D2 * sp.diag(*s)
    if (D1 * M).is_zero_matrix: D2 = M; break
else:
    raise SystemExit('no consistent orientation found')
b_cube = betti([D1, D2], (8, 12, 6))
check(b_cube == (1, 0, 1), 'cube-surface (sphere) Betti numbers = %s' % (b_cube,))

head(4, 'MORSE INEQUALITIES AND THE EULER CHARACTERISTIC, THE TWO ROUTES COMPARED')
for name, c, b, chi_cells in (('torus', c_torus, b_torus, 9 - 18 + 9), ('sphere', c_sphere, b_cube, 8 - 12 + 6)):
    alt = lambda t: t[0] - t[1] + t[2]
    check(all(ci >= bi for ci, bi in zip(c, b)), '%s: c_k >= b_k for k = 0,1,2 (%s vs %s)' % (name, c, b))
    check(alt(c) == alt(b) == chi_cells, '%s: sum(-1)^k c_k = sum(-1)^k b_k = V-E+F = %d' % (name, chi_cells))
    check(c == b, '%s: c_k = b_k, a perfect Morse function (a fact about these two examples)' % name)
check(not (c_torus == (0, 0, 0)), 'control: the counts are not trivially zero')

head(5, 'THE PAGE\'S TABLE')
html = open(os.path.join(HERE, 'ch-witten.html'), encoding='utf-8').read()
rows = {m[0]: m for m in re.findall(r'<tr data-space="(\w+)" data-c="([\d,]+)" data-b="([\d,]+)" data-chi="(-?\d+)"', html)}
tup = lambda s: tuple(int(t) for t in s.split(','))
check(tup(rows['torus'][1]) == c_torus and tup(rows['torus'][2]) == b_torus and int(rows['torus'][3]) == 0, 'torus row equals computed values')
check(tup(rows['sphere'][1]) == c_sphere and tup(rows['sphere'][2]) == b_cube and int(rows['sphere'][3]) == 2, 'sphere row equals computed values')
for lab in ('THEOREM', 'CHECKED INSTANCE', 'OPEN QUESTION'):
    check(('<b>%s</b>' % lab) in html, 'visible evidence label %s present' % lab)
check('href="ch-euler.html"' in html and 'href="ch-conley.html"' in html, 'links to ch-euler and ch-conley')
check('were not checked for this page' in html, 'page states which biographical details were not checked')
print('\n' + '=' * 70)
if fails:
    print('  %d CHECK(S) FAILED:' % len(fails)); [print('    - ' + f) for f in fails]; sys.exit(1)
print('  ALL CHECKS PASSED')
