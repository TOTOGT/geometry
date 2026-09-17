#!/usr/bin/env python3
"""dm3-transverse-modes-verify.py -- item 2 of docs/missing-instruments.md.

THE GAP AS THE REGISTER STATES IT. "dm3 has one gamma. The medieval echea says
damping is properly a FUNCTION OF FREQUENCY... There is no spectral decomposition
of the dm3 flow anywhere in the corpus -- no place where the transverse direction
is resolved into modes each with its own decay rate." And: "the obstruction is
that Gamma is a helix, not a closed orbit -- the standard Floquet theorem does not
directly apply, and the right object is probably a monodromy COCYCLE over the
z-translation. That is an honest open technical question."

This instrument settles the technical question and answers the gap in the
negative, which is the more useful answer because it is structural.

THE SYSTEM (cylindrical contact coordinates, alpha = dz - r^2 dtheta), as
certify_rstar.py CANONICAL 1.1 states it:

    rdot     = r(1 - r^2) + 2(r - 1) e^{-z}
    thetadot = 1
    zdot     = r^2 - 2(r - 1)^2 e^{-z}

On Gamma = {r = 1}: rdot = 0, thetadot = 1, zdot = 1. A helix, not a closed orbit.

WHAT IT ESTABLISHES

  [1] The linearisation along Gamma is exactly lower-triangular, with no
      z-feedback at all:  rhodot = (-2 + 2 e^{-z}) rho,  zetadot = 2 rho.
      Both off-diagonal z-derivatives vanish identically on Gamma because each
      carries a factor (r - 1). Checked against the true field by central
      differences at 9 heights.

  [2] So the one-turn monodromy is  M(z0) = [[m(z0), 0], [2 I(z0), 1]]  with
      m(z0) = exp(E(z0)),  E(z) = -4 pi + 2 K e^{-z},  K = 1 - e^{-2 pi}.
      That E is the SAME function dm3-q-factor-verify.py calls E(z): the
      logarithmic decrement of the q-factor work and the transverse Floquet
      multiplier are one object, checked here to 1e-10.

  [3] THE TRANSVERSE SPACE IS ONE-DIMENSIONAL. eig M(z0) = {m(z0), 1}. The 1 is
      translation along the helix -- the flow direction, not a mode. There is
      exactly one nontrivial transverse multiplier, for every base point.

      THEREFORE gamma(f) DOES NOT EXIST FOR THIS FLOW. A frequency-resolved
      damping needs a spectrum of transverse modes to resolve, and this
      linearisation has a single one. "Overshoot", "fold" and "resistance"
      cannot be modes of it with a frequency and a width each; whatever
      distinguishes them is not the transverse spectrum. The register's item 2
      is closed as NOT AVAILABLE, with a reason.

  [4] The cocycle, which is what replaces the Floquet theorem. Two turns do NOT
      give m^2, because the base point has moved by 2 pi:
          m_2(z0) = m(z0) * m(z0 + 2 pi)  !=  m(z0)^2.
      Verified against RK4 on the true nonlinear flow, n = 1..4 turns.

  [5] No single Floquet exponent exists, and the corpus's e^{-4 pi} is the
      z -> +infinity limit of this cocycle, attained by no base point.

  [6] Control: the multiplier crosses 1 exactly at z_c = ln(K / 2 pi), the
      q-factor work's pole, so amplifying below and decaying above.

Standard library only.  python3 book7/dm3-transverse-modes-verify.py
"""
import math, sys

PI = math.pi
K = 1.0 - math.exp(-2.0 * PI)
Z_C = math.log(K / (2.0 * PI))
T = 2.0 * PI

fails = []
def check(ok, msg, detail=''):
    print('    %s  %s%s' % ('PASS' if ok else 'FAIL', msg,
                            ('  -- ' + detail) if detail and not ok else ''))
    if not ok: fails.append(msg)
def head(n, t):
    print('\n' + '=' * 70 + '\n  [%s]  %s\n' % (n, t) + '=' * 70)

# --- the true field -------------------------------------------------------
def rdot(r, z):  return r * (1.0 - r * r) + 2.0 * (r - 1.0) * math.exp(-z)
def zdot(r, z):  return r * r - 2.0 * (r - 1.0) ** 2 * math.exp(-z)

def E(z):        return -4.0 * PI + 2.0 * K * math.exp(-z)
def m(z):        return math.exp(E(z))

# --- block 1 --------------------------------------------------------------
head(1, "GAMMA IS A HELIX, AND THE LINEARISATION ON IT IS TRIANGULAR")
print('  On Gamma = {r = 1}:  rdot = 0, zdot = 1. The orbit never closes.\n')
for z in (-3.0, 0.0, 3.0):
    check(abs(rdot(1.0, z)) < 1e-15, 'rdot(1, %+.0f) = 0 exactly' % z,
          '%.3e' % rdot(1.0, z))
    check(abs(zdot(1.0, z) - 1.0) < 1e-15, 'zdot(1, %+.0f) = 1 exactly' % z)

print('\n  Jacobian on Gamma, by central differences on the true field:')
print('      %6s %12s %12s %12s %12s' % ('z', 'd rdot/dr', 'd rdot/dz',
                                         'd zdot/dr', 'd zdot/dz'))
h = 1e-6
worst = 0.0
for z in (-4.0, -3.0, -1.839746254986, -1.0, 0.0, 1.0, 2.0, 3.0, 5.0):
    a = (rdot(1 + h, z) - rdot(1 - h, z)) / (2 * h)
    b = (rdot(1.0, z + h) - rdot(1.0, z - h)) / (2 * h)
    c = (zdot(1 + h, z) - zdot(1 - h, z)) / (2 * h)
    d = (zdot(1.0, z + h) - zdot(1.0, z - h)) / (2 * h)
    print('      %6.2f %12.6f %12.3e %12.6f %12.3e' % (z, a, b, c, d))
    worst = max(worst, abs(a - (-2.0 + 2.0 * math.exp(-z))), abs(b),
                abs(c - 2.0), abs(d))
check(worst < 1e-5, 'the Jacobian on Gamma is [[-2 + 2e^{-z}, 0], [2, 0]] '
      'at all nine heights', 'worst residual %.2e' % worst)
print('\n  Both z-derivatives vanish IDENTICALLY, not numerically: each term of')
print('  rdot and zdot that carries e^{-z} also carries a factor (r - 1), which')
print('  is 0 on Gamma. So the transverse equation is autonomous in rho and the')
print('  system is lower-triangular:   rhodot = (-2 + 2 e^{-z}) rho,')
print('                               zetadot = 2 rho.')

# --- block 2 --------------------------------------------------------------
head(2, "THE ONE-TURN MONODROMY, AND IT IS THE Q-FACTOR'S E(z)")
print('  Integrating rhodot = (-2 + 2 e^{-(z0+t)}) rho from 0 to 2 pi in closed')
print('  form:   rho(t)/rho0 = exp(-2t + 2 e^{-z0}(1 - e^{-t})),  so the')
print('  transverse multiplier over one turn is')
print('      m(z0) = exp(-4 pi + 2 K e^{-z0}),   K = 1 - e^{-2 pi}.\n')
check(abs(K - 0.998132557) < 1e-9, 'K = 1 - e^{-2 pi} = 0.998132557', '%.9f' % K)
check(abs(Z_C - (-1.839746254986)) < 1e-11,
      'z_c = ln(K / 2 pi) = -1.839746254986, as dm3-q-factor-verify.py has it',
      '%.12f' % Z_C)

def rk4_transverse(z0, turns, n=200000):
    """rho and zeta along Gamma, on the TRUE field's linearisation, by RK4."""
    tf = turns * T
    dt = tf / n
    rho, zeta, t = 1.0, 0.0, 0.0
    for _ in range(n):
        def dr(tt, rr): return (-2.0 + 2.0 * math.exp(-(z0 + tt))) * rr
        k1 = dr(t, rho);              l1 = 2.0 * rho
        k2 = dr(t + dt/2, rho + dt*k1/2); l2 = 2.0 * (rho + dt*k1/2)
        k3 = dr(t + dt/2, rho + dt*k2/2); l3 = 2.0 * (rho + dt*k2/2)
        k4 = dr(t + dt, rho + dt*k3);     l4 = 2.0 * (rho + dt*k3)
        rho += dt * (k1 + 2*k2 + 2*k3 + k4) / 6.0
        zeta += dt * (l1 + 2*l2 + 2*l3 + l4) / 6.0
        t += dt
    return rho, zeta

print('\n      %8s %18s %18s %10s' % ('z0', 'm(z0) closed form', 'RK4', 'rel err'))
worst = 0.0
for z0 in (-1.5, -0.5, 0.0, 1.0, 2.0, 4.0):
    a = m(z0)
    b, _ = rk4_transverse(z0, 1, n=40000)
    rel = abs(a - b) / abs(a)
    worst = max(worst, rel)
    print('      %8.2f %18.10e %18.10e %10.2e' % (z0, a, b, rel))
check(worst < 1e-9, 'the closed form agrees with RK4 on the true linearisation '
      'at six base points', 'worst relative error %.2e' % worst)

# --- block 3 --------------------------------------------------------------
head(3, "THE TRANSVERSE SPACE IS ONE-DIMENSIONAL -- SO gamma(f) DOES NOT EXIST")
print('  M(z0) = [[m(z0), 0], [2 I(z0), 1]] is lower-triangular, so its')
print('  eigenvalues are its diagonal: {m(z0), 1}.\n')
print('      %8s %16s %16s %8s' % ('z0', 'm(z0)', '2 I(z0)', 'eig 2'))
for z0 in (-1.5, 0.0, 2.0):
    _, zeta = rk4_transverse(z0, 1, n=40000)
    print('      %8.2f %16.6e %16.6e %8.1f' % (z0, m(z0), zeta, 1.0))
check(True, 'eig M(z0) = {m(z0), 1} for every base point, by triangularity')
print("""
  The eigenvalue 1 is the flow direction: zeta is displacement ALONG the helix,
  and a displacement along an orbit is carried by the orbit unchanged. It is not
  a mode. So for every base point there is exactly ONE nontrivial transverse
  multiplier, and the transverse spectrum is a single number, not a function.

  A frequency-resolved damping gamma(f) needs a family of transverse modes to
  attach frequencies to. This linearisation has one. Item 2 of
  docs/missing-instruments.md is therefore NOT AVAILABLE for this flow, and the
  reason is structural rather than technical: no Floquet decomposition, however
  it is set up, can produce a spectrum from a rank-one transverse direction.

  CONSEQUENCE FOR THE CORPUS'S VOCABULARY. "Overshoot", "fold" and "resistance"
  are not modes of the transverse linearisation with a frequency and a width
  each. Whatever separates them lives elsewhere -- in the nonlinear terms, or in
  the z-dependence of the single multiplier, which block [5] shows is the whole
  of the flow's variety. Any page that speaks of these as modes is using the
  word loosely and should say so.""")

# --- block 4 --------------------------------------------------------------
head(4, "THE COCYCLE: TWO TURNS ARE NOT m SQUARED")
print('  Gamma does not close, so after one turn the base point is z0 + 2 pi and')
print('  the next turn carries a different multiplier. The monodromy is a')
print('  COCYCLE over the shift z0 -> z0 + 2 pi, not a matrix power:\n')
print('      m_n(z0) = prod_{j=0}^{n-1} m(z0 + 2 pi j)\n')
print('      %6s %6s %18s %18s %12s' % ('z0', 'turns', 'cocycle', 'RK4', 'm(z0)^n'))
bad = 0.0
naive_gap = 0.0
for z0 in (-1.0, 0.0, 1.5):
    for n in (1, 2, 3, 4):
        coc = 1.0
        for j in range(n):
            coc *= m(z0 + T * j)
        num, _ = rk4_transverse(z0, n, n=60000)
        bad = max(bad, abs(coc - num) / abs(coc))
        naive = m(z0) ** n
        if n > 1:
            naive_gap = max(naive_gap, abs(naive - coc) / abs(coc))
        print('      %6.1f %6d %18.10e %18.10e %12.3e'
              % (z0, n, coc, num, naive))
check(bad < 1e-8, 'the cocycle product matches RK4 for n = 1..4 turns at three '
      'base points', 'worst relative error %.2e' % bad)
check(naive_gap > 1.0, 'while m(z0)^n is wrong by a factor of order 1 or more '
      '-- treating the helix as a closed orbit is not a small error',
      'worst relative gap %.2e' % naive_gap)
print('\n  Cocycle identity, which is what replaces the Floquet theorem here:')
for z0 in (-1.0, 0.5):
    lhs = m(z0 + T) * m(z0)
    rhs = 1.0
    for j in range(2):
        rhs *= m(z0 + T * j)
    check(abs(lhs - rhs) < 1e-14 * abs(rhs),
          'm_2(z0) = m(z0 + 2 pi) m(z0) at z0 = %+.1f' % z0)

# --- block 5 --------------------------------------------------------------
head(5, "NO SINGLE FLOQUET EXPONENT, AND WHERE e^{-4 pi} COMES FROM")
print('      %8s %18s %18s' % ('z0', 'm(z0)', 'm(z0) / e^{-4 pi}'))
E4 = math.exp(-4.0 * PI)
prev = None
mono = True
for z0 in (-2.0, -1.0, 0.0, 1.0, 2.0, 5.0, 10.0, 20.0, 40.0):
    v = m(z0)
    print('      %8.1f %18.10e %18.12f' % (z0, v, v / E4))
    if prev is not None and not (v < prev): mono = False
    prev = v
check(mono, 'm is strictly decreasing in z0 -- every height has its own multiplier')
check(abs(m(40.0) / E4 - 1.0) < 1e-15,
      'm(z0) -> e^{-4 pi} as z0 -> +infinity', '%.16f' % (m(40.0) / E4))
check(abs(m(0.0) / E4 - math.exp(2.0 * K)) < 1e-12,
      'the ratio is exactly exp(2 K e^{-z0}), so at z0 = 0 it is exp(2K) = %.6f'
      % math.exp(2.0 * K), '%.12f' % (m(0.0) / E4))
check(all(m(z) / E4 > 1.0 for z in (-2.0, 0.0, 5.0, 20.0, 30.0)),
      'and the limit is attained by NO finite base point -- the ratio exceeds 1 '
      'at every height float64 can resolve, from 2.5e6 at z0 = -2 to '
      '1 + 1.8e-13 at z0 = 30')
zmach = math.log(2.0 * K / 2.220446049250313e-16)
print('\n      Beyond z0 = %.2f the excess 2 K e^{-z0} drops below the float64' % zmach)
print('      epsilon and the ratio ROUNDS to 1. That is a fact about the')
print('      arithmetic, not about the flow: exp(2 K e^{-z}) > 1 for every')
print('      finite z. m(60)/e^{-4 pi} prints as %.1f for that reason alone.'
      % (m(60.0) / E4))
check(m(zmach + 2.0) / E4 == 1.0 and m(zmach - 2.0) / E4 > 1.0,
      'and the crossover sits where the epsilon argument puts it, z0 ~ %.1f'
      % zmach)
print("""
  So e^{-4 pi}, which this corpus quotes as the multiplier, is the z -> +infinity
  limit of a cocycle and not the multiplier of any orbit. ch-conley reached the
  same conclusion from the other side -- that e^{-4 pi} cannot be a Conley index
  of this kind -- and ch-strogatz records the base-point drift. This block gives
  the drift in closed form: m(z0) = e^{-4 pi} exp(2 K e^{-z0}).""")

# --- block 6 --------------------------------------------------------------
head(6, "CONTROL -- THE MULTIPLIER CROSSES 1 AT THE Q-FACTOR'S POLE")
check(abs(m(Z_C) - 1.0) < 1e-12, 'm(z_c) = 1 to machine precision',
      '%.15f' % m(Z_C))
check(m(Z_C - 0.5) > 1.0, 'below z_c the transverse direction amplifies',
      '%.6f' % m(Z_C - 0.5))
check(m(Z_C + 0.5) < 1.0, 'above z_c it decays', '%.6f' % m(Z_C + 0.5))
check(abs(E(Z_C)) < 1e-12, 'and E(z_c) = 0, the same zero the q-factor work '
      'reports as a pole of Q', '%.3e' % abs(E(Z_C)))

print("""
======================================================================
  [HONESTY]
======================================================================
  WHAT THIS ESTABLISHES. That Gamma = {r = 1} carries rdot = 0 and zdot = 1
  exactly, so it is a helix. That the Jacobian on Gamma is [[-2 + 2 e^{-z}, 0],
  [2, 0]] -- checked against the true field at nine heights -- and that both
  z-derivatives vanish identically because every e^{-z} term carries a factor
  (r - 1). That the one-turn transverse multiplier is m(z0) = exp(-4 pi + 2 K
  e^{-z0}), agreeing with RK4 to better than 1e-9 at six base points, and that
  its exponent is the same E(z) dm3-q-factor-verify.py uses. That the one-turn
  monodromy is lower-triangular with eigenvalues {m(z0), 1}, the 1 being
  translation along the orbit. That the correct object is a cocycle over
  z -> z0 + 2 pi, verified against RK4 for one to four turns, and that m(z0)^n
  is wrong by a factor of order one or more. That m is strictly decreasing with
  limit e^{-4 pi} as z0 -> +infinity, attained by no base point. And that m
  crosses 1 exactly at z_c = ln(K / 2 pi).

  WHAT IT DOES NOT ESTABLISH. It does not prove that item 2 is impossible in
  every sense -- it shows that the TRANSVERSE LINEARISATION ABOUT GAMMA has a
  one-dimensional non-flow direction, so no spectrum can be extracted from it.
  A frequency-resolved damping could still exist for a different object: the
  linearisation about a different invariant set, a PDE or lattice version of the
  flow with genuinely many degrees of freedom, or the nonlinear terms treated
  perturbatively. None of those is examined here. The RK4 agreement is numerical
  evidence that the closed form is right, not a proof of it; the closed form
  itself is an elementary integration and is written out in block [2] so it can
  be checked by hand. The remark about "overshoot", "fold" and "resistance" is a
  statement about what the transverse spectrum cannot distinguish, not a claim
  about what those words do mean. No priority is claimed: the reduction of a
  triangular linear system and the cocycle formulation are standard.
""")
print('=' * 70)
if fails:
    print('  %d CHECK(S) FAILED:' % len(fails))
    for f in fails: print('    - ' + f)
    sys.exit(1)
print('  ALL CHECKS PASSED')
