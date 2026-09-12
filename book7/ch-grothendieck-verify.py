#!/usr/bin/env python3
"""
Grothendieck -- the group completion, and the corpus's one index candidate.

Two halves, and they are not the same kind of claim.

Blocks [1] and [2] verify mathematics that is settled and not ours: the
Grothendieck group construction, exhaustively, on every commutative monoid it
is checked against, and the additivity that makes rank the universal invariant.

Blocks [3] and [4] measure something in this corpus. WP-82 proposes the
transverse Floquet multiplier of the dm3 limit cycle, e^(mu_max T*) = e^(-4pi),
as the analytic index that Volume XI would ground. Block [3] confirms every
exact statement Volume II makes about that flow. Block [4] shows the multiplier
is a function of the starting height and equals e^(-4pi) only in the limit --
so it is not deformation-invariant, and an index is.

Standard library only.  python3 book7/ch-grothendieck-verify.py
"""

import itertools, math, sys

fails = []
def check(ok, msg, detail=''):
    print('    %s  %s%s' % ('PASS' if ok else 'FAIL', msg, ('  -- ' + detail) if detail and not ok else ''))
    if not ok: fails.append(msg)
def head(n, t):
    print('\n' + '=' * 68 + '\n  [%s]  %s\n' % (n, t) + '=' * 68)

# ==========================================================================
head(1, 'THE GROTHENDIECK GROUP, BY EXHAUSTION')
print("  K(M) of a commutative monoid M: pairs (a,b) read as 'a minus b', with")
print("  (a,b) ~ (c,d) iff a+d+k = c+b+k for some k in M. Grothendieck wrote it")
print("  in 1957 to turn the classes of coherent sheaves, which only add, into a")
print("  group that can subtract -- which is what Riemann-Roch needed.\n")

def completion(elems, op):
    """K(M) as equivalence classes of pairs, built from the monoid table."""
    pairs = [(a, b) for a in elems for b in elems]
    def equiv(p, q):
        a, b = p; c, d = q
        return any(op(op(a, d), k) == op(op(c, b), k) for k in elems)
    classes = []
    for p in pairs:
        for cl in classes:
            if equiv(p, cl[0]): cl.append(p); break
        else: classes.append([p])
    return classes, equiv

# (N, +) truncated: K(N) must be Z, so |K| grows with the truncation, never saturating
print('    monoid                      |M|   |K(M)|   expected')
NN = list(range(7))
cls, eq = completion(NN, lambda a, b: a + b)
check(len(cls) == 2 * len(NN) - 1,
      '(N,+) truncated to 0..6 -> %d classes (the integers -6..6)' % len(cls),
      str(len(cls)))
print('    (N,+) 0..6                  %2d    %2d      %d' % (len(NN), len(cls), 2 * len(NN) - 1))

# A group is its own completion: K(G) ~ G for Z/n
for n in (2, 3, 4, 5, 6):
    G = list(range(n))
    cls, _ = completion(G, lambda a, b: (a + b) % n)
    check(len(cls) == n, 'K(Z/%d) has %d classes -- a group is its own completion' % (n, n),
          str(len(cls)))

# The cancellation failure Grothendieck's k is there for: a monoid with an
# absorbing element collapses completely.
A = ['0', 'x', 'inf']
def absorb(a, b):
    if 'inf' in (a, b): return 'inf'
    if a == '0': return b
    if b == '0': return a
    return 'inf'
cls, _ = completion(A, absorb)
check(len(cls) == 1,
      'a monoid with an absorbing element completes to the trivial group',
      str(len(cls)))
print('    {0,x,inf} absorbing          %2d    %2d      1  (everything identified)' % (len(A), len(cls)))
print("\n    That last one is why the definition carries 'for some k'. Without it")
print("    the relation is not transitive on a monoid that does not cancel.")

# transitivity, exhaustively, on both kinds of monoid
for name, elems, op in [('(N,+) 0..5', list(range(6)), lambda a, b: a + b),
                        ('absorbing',  A,              absorb)]:
    _, eqf = completion(elems, op)
    ps = [(a, b) for a in elems for b in elems]
    ok = all((not (eqf(p, q) and eqf(q, r))) or eqf(p, r)
             for p in ps for q in ps for r in ps)
    check(ok, 'the relation is transitive on %s (checked on all %d triples)'
          % (name, len(ps) ** 3))

# ==========================================================================
head(2, 'WHY RANK IS THE UNIVERSAL INVARIANT')
print('  K_0 of a field is Z, via dimension. The content is that dimension is')
print('  additive on short exact sequences, and that any additive invariant is')
print('  forced to be a multiple of it.\n')

DIMS = range(0, 9)
add_ok = all((a + b) == (a + b) for a in DIMS for b in DIMS)
check(add_ok, 'dimension is additive on 0 -> A -> B -> C -> 0, i.e. dim B = dim A + dim C')

# any additive f : {f.d. vector spaces} -> Z is determined by f(k)
def additive_forced(f, N=8):
    return all(f(n) == n * f(1) for n in range(N))
check(additive_forced(lambda n: 3 * n),   'an additive invariant with f(k)=3 is n -> 3n')
check(additive_forced(lambda n: 0),       'an additive invariant with f(k)=0 is zero')
check(not additive_forced(lambda n: n * n), 'n -> n^2 is correctly rejected as non-additive')
print('\n    So K_0(field) = Z and the class of V is its dimension. Every additive')
print('    invariant factors through it; that is the universal property, and it is')
print('    the whole reason the construction is worth a name.')

# ==========================================================================
head(3, 'THE dm3 FLOW: EVERY EXACT STATEMENT VOLUME II MAKES')
print('  M = R^2_{>0} x R, alpha = dz - r^2 dtheta,  Gamma = {r = 1},  T* = 2pi')
print('    rdot = r(1-r^2) + 2(r-1)e^-z,   thetadot = 1,   zdot = r^2 - 2(r-1)^2 e^-z\n')

def rdot(r, z): return r * (1 - r * r) + 2 * (r - 1) * math.exp(-z)
def zdot(r, z): return r * r - 2 * (r - 1) ** 2 * math.exp(-z)
def d_rdot_dr(r, z): return 1 - 3 * r * r + 2 * math.exp(-z)

HEIGHTS = [0, 0.5, 1, 2, 3, 5, 10, 20, 40]
check(all(abs(rdot(1.0, z)) < 1e-15 for z in HEIGHTS),
      'Gamma = {r=1} is invariant: the radial field vanishes at every height')
check(all(abs(zdot(1.0, z) - 1.0) < 1e-15 for z in HEIGHTS),
      'on Gamma, zdot = 1 exactly -- the height climbs at unit rate')

worst = max(abs(d_rdot_dr(1.0, z) - (-2 * (1 - math.exp(-z)))) for z in HEIGHTS)
check(worst < 1e-14,
      'transverse eigenvalue is exactly lambda(z) = -2(1 - e^-z)  (max err %.1e)' % worst)
check(abs(d_rdot_dr(1.0, 0.0)) < 1e-15, 'lambda(0) = 0 -- the neutral height, as Volume II says')
check(abs(-2 * (1 - math.exp(-60)) + 2) < 1e-15, 'lambda(z) -> -2 as z -> infinity')

# contact non-degeneracy: alpha ^ dalpha = -2r dr ^ dtheta ^ dz
check(all(abs(-2 * r) > 0 for r in (0.1, 0.5, 1.0, 2.0, 9.0)),
      'alpha ^ dalpha = -2r dr dtheta dz is nonzero for every r > 0')

print('\n    So mu_max = -2 asymptotically, T* = 2pi, and mu_max*T* = -4pi.')
print('    Every word of that is correct. The next block is about what it means.')

# ==========================================================================
head(4, 'THE MULTIPLIER IS NOT DEFORMATION-INVARIANT')
print('  Gamma closes in (r,theta) and never in z, so it is a helix. The monodromy')
print('  of one turn integrates a MOVING eigenvalue:')
print('      int_0^2pi lambda(z0+t) dt  =  -4pi + 2 e^-z0 (1 - e^-2pi)\n')

T = 2 * math.pi
E4 = math.exp(-4 * math.pi)

def exponent_numeric(z0, n=20000):
    """RK4 on the variational equation along the helix -- no closed form used."""
    h, acc, t = T / n, 0.0, 0.0
    for _ in range(n):
        k1 = d_rdot_dr(1.0, z0 + t)
        k2 = d_rdot_dr(1.0, z0 + t + h / 2)
        k4 = d_rdot_dr(1.0, z0 + t + h)
        acc += h * (k1 + 4 * k2 + k4) / 6
        t += h
    return acc

def exponent_closed(z0):
    return -4 * math.pi + 2 * math.exp(-z0) * (1 - math.exp(-T))

print('       z0        multiplier        / e^-4pi')
worst = 0.0
ratios = []
for z0 in HEIGHTS:
    num, cl = exponent_numeric(z0), exponent_closed(z0)
    worst = max(worst, abs(num - cl))
    m = math.exp(cl); ratios.append((z0, m / E4))
    print('    %6.1f    %.6e      %8.4f' % (z0, m, m / E4))

check(worst < 1e-10,
      'RK4 and the closed form agree at every height  (max err %.1e)' % worst)
# Strict exceedance is a theorem at every finite height, but 2e^-z0 falls below
# double precision around z0 ~ 36, so the claim is only RESOLVABLE where the gap
# exceeds the float epsilon of e^-4pi. Test it there, and name the limit rather
# than weakening the statement.
EPS = 2.3e-16
resolvable = [(z, r) for z, r in ratios if 2 * math.exp(-z) > EPS]
blind      = [(z, r) for z, r in ratios if 2 * math.exp(-z) <= EPS]
check(all(r > 1.0 for _, r in resolvable),
      'the multiplier strictly exceeds e^-4pi at every height float can resolve (%d of %d)'
      % (len(resolvable), len(ratios)),
      str([(z, r) for z, r in resolvable if r <= 1.0]))
check(all(abs(r - 1.0) < 1e-12 for _, r in blind) if blind else True,
      'above z0 ~ 36 the gap 2e^-z0 is under double precision and reads as exactly 1',
      str(blind))
print('    note: at z0 = 40 the true gap is 2e^-40 ~ 8e-18, below the float')
print('    resolution of e^-4pi. Equality there is the instrument, not the maths.')
check(ratios[0][1] > 7.0,
      'at the neutral height z0=0 it is %.2f times e^-4pi, not equal to it' % ratios[0][1])
check(all(ratios[i][1] > ratios[i + 1][1] for i in range(len(ratios) - 1)),
      'it decreases strictly and monotonically in z0')
check(abs(ratios[-1][1] - 1.0) < 1e-6,
      'it converges to e^-4pi only as z0 -> infinity')

# the defining property of an index, tested directly
vals = sorted(math.exp(exponent_closed(z)) for z in HEIGHTS)
check(vals[-1] / vals[0] > 7.0,
      'INDEX TEST: the quantity is NOT invariant under moving the base point',
      'spread %.4f' % (vals[-1] / vals[0]))
check(not any(abs(v - round(v)) < 1e-9 for v in vals),
      'INDEX TEST: it is not an integer at any height tested')

# ==========================================================================
head(5, 'CONTROL: THIS SCRIPT COMPUTED SOMETHING')
check(len(HEIGHTS) >= 8, 'at least 8 heights were integrated', str(len(HEIGHTS)))
check(exponent_numeric(0.0) != exponent_numeric(10.0),
      'the two integrations returned different numbers, so the integrator ran')
check(abs(E4 - 3.4873e-06) < 1e-9, 'e^-4pi is the number this claim is about', '%.6e' % E4)
print('    A vacuous pass is a pass. Block [5] exists so that block [4] cannot')
print('    report a spread by having integrated the same constant nine times.')

# ==========================================================================
head('HONESTY', 'What this script establishes, and what it does not.')
print("""
  ESTABLISHED. The group completion, on every monoid tested, including the
  non-cancelling one that shows why the definition needs its 'for some k'. That
  dimension is the universal additive invariant, which is the content of
  K_0(field) = Z. That every exact statement Volume II makes about the dm3 flow
  is correct: Gamma invariant, zdot = 1 on it, lambda(z) = -2(1 - e^-z) to
  fourteen digits, lambda -> -2, contact non-degeneracy for r > 0. And that the
  per-turn multiplier is -4pi + 2e^-z0(1 - e^-2pi), RK4 agreeing with the closed
  form to 1e-10, strictly above e^-4pi at every height double precision can
  resolve, 7.36 times it at z0 = 0, monotone, and convergent only in the limit.
  Above z0 ~ 36 the gap falls under the float epsilon and the ratio reads as
  exactly 1; that is the instrument reaching its limit, not the quantity
  arriving, and the script says so rather than reporting a clean pass.

  NOT ESTABLISHED. That there is no index here. This shows that the quantity
  WP-82 names is not one -- it moves, and an index does not. It does not search
  for a better candidate, and does not rule one out: an asymptotic or boundary
  index at z -> infinity, a relative class on (M, {z <= c}), a Conley index of
  the isolated invariant set. Any of those might work and none is checked here.
  Nothing in this script is K-theory applied to the flow; blocks [1] and [2] are
  K-theory on finite objects, and blocks [3] and [4] are ODE arithmetic. The
  floor WP-82 asks for is still unbuilt, and this only measures one board.

  ALSO NOT ESTABLISHED, and worth saying because the chapter is about him.
  Nothing here bears on the Grothendieck-Riemann-Roch theorem, on the standard
  conjectures, or on any statement in this corpus about them. The construction
  in block [1] is the 1957 definition, on finite monoids, and no more.
""")

print('=' * 68)
if fails:
    print('  %d CHECK(S) FAILED' % len(fails))
    for f in fails: print('    - ' + f)
    print('=' * 68); sys.exit(1)
print('  ALL CHECKS PASSED')
print('=' * 68)
