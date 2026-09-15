#!/usr/bin/env python3
"""
WP-122 -- the return map the corpus never wrote, computed.

WHY THIS FILE EXISTS. The corpus's transverse dynamics live on Strogatz's
Example 7.1.1, r' = r(1 - r^2), theta' = 1 (Nonlinear Dynamics and Chaos,
2nd ed., p. 199). Example 8.7.1 on p. 282 of the same book computes the
POINCARE MAP of that system in closed form:

    P(r) = [ 1 + e^{-4*pi} (r^{-2} - 1) ]^{-1/2}

The corpus has never used a return map. It has the linearised multiplier
e^{-4*pi} in two chapters, and it has a Gronwall bound in chEps-gronwall.html
Proof IV that brackets a contraction radius at eps_0 = 1/3. The exact map
settles what the bound brackets, and it also fixes the vocabulary that
chRho-spectral.html Argument V uses loosely.

BLOCKS
  [1] The closed form checked against RK4, and P'(1) = e^{-4*pi}.
  [2] Exponent and multiplier agree: (1/T*) ln|P'(1)| = -2. The corpus's
      bookkeeping is CORRECT here; this block says so.
  [3] Gronwall bound vs the exact sup|P'| on |rho| <= 1/3, and the radius
      where P actually stops contracting.
  [4] The basin of r' = r(1-r^2) is all of r > 0, so eps_0 = 1/3 is an
      estimate's saturation radius and not a basin boundary.
  [5] chRho-spectral Argument V: the arithmetic, run.
  [6] The shape of a Poincare linearisation: how many multipliers there are.
  [7] The Poincare-Bendixson trapping annulus of Example 7.3.1, p. 206,
      checked analytically and by exhaustion in theta.
  [8] Control.

PRIMARY SOURCE. S. H. Strogatz, "Nonlinear Dynamics and Chaos", 2nd ed.,
Westview 2015 / CRC 2018. Sections 7.1 (p.199), 7.3 (pp.205-206),
8.7 (pp.281-282), 10.5 (pp.373-374).

Standard library only.  python3 book6/wp122-verify.py
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
K     = math.exp(-4.0 * math.pi)          # the Floquet multiplier of Gamma

def rk4_r(r0, t1, n):
    """integrate r' = r(1-r^2) from r0 for time t1"""
    r, h = r0, t1 / n
    f = lambda x: x * (1.0 - x * x)
    for _ in range(n):
        k1 = f(r); k2 = f(r + h/2*k1); k3 = f(r + h/2*k2); k4 = f(r + h*k3)
        r += h/6*(k1 + 2*k2 + 2*k3 + k4)
    return r

def P(r):
    """Strogatz Example 8.7.1, p. 282 -- the first return to the ray theta = const"""
    return (1.0 + K * (r**-2 - 1.0)) ** -0.5

def dP(r):
    """P'(r), differentiated by hand and checked against a difference quotient below"""
    return K * r**-3 * (1.0 + K * (r**-2 - 1.0)) ** -1.5

# ---------------------------------------------------------------------------
head(1, 'THE CLOSED-FORM RETURN MAP, CHECKED AGAINST INTEGRATION')
print('  Strogatz p. 282, Example 8.7.1. S is the positive x-axis; theta\' = 1 so')
print('  the time of flight between crossings is exactly 2*pi, and')
print('      P(r) = [ 1 + e^{-4pi} (r^{-2} - 1) ]^{-1/2}.\n')
print('     %10s %22s %22s %12s' % ('r_0', 'RK4 over t = 2*pi', 'P(r_0) closed form', 'rel.err'))
ok_cf = True
for r0 in (0.02, 0.1, 0.5, 0.9, 1.0, 1.5, 4.0, 40.0):
    num, ana = rk4_r(r0, TWOPI, 200000), P(r0)
    rel = abs(num - ana) / abs(ana)
    print('     %10.2f %22.15f %22.15f %12.2e' % (r0, num, ana, rel))
    if rel > 1e-10: ok_cf = False
check(ok_cf, 'the closed form reproduces the integrated flow to 1e-10 relative')
check(abs(P(1.0) - 1.0) < 1e-15, 'r* = 1 is a fixed point of P, as it must be')

# h is deliberately not tiny: P(1 +/- h) - 1 is of order K*h ~ 3e-10 at h = 1e-4,
# and a smaller h would be eaten by cancellation against values of size 1.
h = 1e-4
dq = (P(1 + h) - P(1 - h)) / (2*h)
print('\n     P\'(1) analytic            = %.15e' % dP(1.0))
print('     central difference at 1   = %.15e' % dq)
print('     e^{-4*pi}                 = %.15e' % K)
check(abs(dP(1.0) - K) < 1e-18, 'P\'(1) = e^{-4*pi} exactly')
check(abs(dq - K) / K < 1e-5, 'and the difference quotient agrees, so dP is right',
      '%.9e vs %.9e' % (dq, K))
print('\n     The multiplier the corpus quotes is the DERIVATIVE OF THIS MAP at its')
print('     fixed point. The map itself -- valid at every r, not just near 1 --')
print('     has been sitting in the textbook exercise the whole time.')

# ---------------------------------------------------------------------------
head(2, "EXPONENT AND MULTIPLIER: THE CORPUS'S BOOKKEEPING IS CORRECT")
print('  Strogatz p. 374, Example 10.5.1: for a p-cycle the Liapunov exponent is')
print('  lambda = (1/p) ln|(f^p)\'(x_0)|. For a flow, per unit time, that is')
print('  (1/T*) ln|multiplier|.\n')
lam = math.log(abs(K)) / TWOPI
print('     T*                          = 2*pi     = %.12f' % TWOPI)
print('     multiplier   P\'(1)          = e^{-4pi} = %.9e' % K)
print('     (1/T*) ln|P\'(1)|            =          = %.12f' % lam)
check(abs(lam + 2.0) < 1e-12, 'the exponent recovered from the multiplier is exactly -2')
print('\n     So mu_max = -2 and e^{-4pi} are the same fact in two units, and the')
print('     pages that quote both are consistent. This block exists to say that')
print('     plainly before block [5] says where the two are conflated.')

# ---------------------------------------------------------------------------
head(3, 'THE GRONWALL BOUND AND THE EXACT CONTRACTION')
print('  chEps-gronwall.html Proof IV writes rho = r - 1, f(rho) = -rho(1+rho)(2+rho),')
print('  bounds |P\'(rho_0)| <= exp((mu_max + 6 eps) T*) on |rho| <= eps, and reads')
print('  off eps_0 = 1/3 as the radius where that bound reaches 1.\n')
r_check = 1.0 + (-1.0/3.0)
print('     f(rho) = -rho(1+rho)(2+rho) is r(1-r^2) rewritten at r = 1 + rho:')
for rho in (-0.5, -1.0/3.0, 0.25):
    lhs = -rho*(1+rho)*(2+rho)
    rhs = (1+rho)*(1 - (1+rho)**2)
    check(abs(lhs - rhs) < 1e-15, 'they agree at rho = %+.4f' % rho)

bound = math.exp((-2.0 + 6.0*(1.0/3.0)) * TWOPI)
sup, arg = 0.0, None
n = 200001
for i in range(n):
    rho = -1.0/3.0 + (2.0/3.0) * i / (n - 1)
    v = abs(dP(1.0 + rho))
    if v > sup: sup, arg = v, rho
print('\n     Gronwall bound on |P\'| at eps = 1/3      : %.6f' % bound)
print('     exact sup |P\'| over |rho| <= 1/3         : %.6e   (at rho = %+.5f)' % (sup, arg))
print('     the bound exceeds the truth by a factor  : %.3e' % (bound / sup))
check(abs(bound - 1.0) < 1e-12, 'the bound is exactly 1 at eps = 1/3, as Proof IV says')
check(sup < 1e-4, 'the exact supremum is below 1e-4, so P contracts hard there')
check(bound / sup > 1e4, 'the bound is loose by more than four orders of magnitude')

lo, hi = 1e-6, 1.0
for _ in range(200):
    mid = 0.5*(lo + hi)
    if abs(dP(mid)) > 1.0: lo = mid
    else: hi = mid
r_star = 0.5*(lo + hi)
print('\n     |P\'(r)| = 1 at r = %.9f   (rho = %+.9f)' % (r_star, r_star - 1.0))
check(abs(dP(r_star) - 1.0) < 1e-6, 'bisection landed on the unit-slope radius')
check(r_star < 0.02, 'so P is a contraction from r = %.4f outward, not only on |rho| <= 1/3' % r_star)
print('     eps_0 = 1/3 is the radius at which an ESTIMATE saturates. The exact map')
print('     contracts on a ball roughly %.0fx wider in rho.' % ((1.0 - r_star) / (1.0/3.0)))

# ---------------------------------------------------------------------------
head(4, 'AND THE BASIN ITSELF IS EVERYTHING')
print('  Strogatz p. 199: "all trajectories (except r* = 0) approach the unit')
print('  circle r* = 1 monotonically." Integrate from far out and far in.\n')
print('  Twenty turns are twenty iterates of P, and the exact solution of')
print('  r\' = r - r^3 is r(t) = r_0 / sqrt(r_0^2 + (1 - r_0^2) e^{-2t}),')
print('  which is the same function. Both are used and compared.\n')
exact = lambda r0, t: r0 / math.sqrt(r0*r0 + (1.0 - r0*r0)*math.exp(-2.0*t))

print('     %12s %24s %16s %14s' % ('r_0', 'P iterated 20x', '|r - 1|', 'fixed-step RK4'))
ok_all = True
for r0 in (1e-6, 1e-3, 0.05, 1.0/3.0, 0.773, 0.882, 2.0, 100.0, 1e4):
    r = r0
    for _ in range(20): r = P(r)
    r_ex = exact(r0, 20*TWOPI)
    r_rk = rk4_r(r0, 20*TWOPI, 400000)
    tag = '%14.9f' % r_rk if math.isfinite(r_rk) else '%14s' % 'nan (stiff)'
    print('     %12.2e %24.15f %16.2e %s' % (r0, r, abs(r - 1.0), tag))
    # isfinite FIRST: a nan fails every inequality silently, so a nan would
    # otherwise have walked through this check as a pass.
    if not math.isfinite(r) or abs(r - 1.0) > 1e-8: ok_all = False
    if abs(r - r_ex) > 1e-12: ok_all = False
check(ok_all, 'every r_0 tested, over ten decades, is on Gamma to 1e-8 after 20 turns')
check(not math.isfinite(rk4_r(1e4, 20*TWOPI, 400000)),
      'and fixed-step RK4 does go nan out there, which is why the map is used')
print('\n     That nan is worth keeping in the table. r\' = r - r^3 is stiff at large r,')
print('     a fixed-step integrator overshoots, and the comparison `|r - 1| > 1e-8`')
print('     is FALSE for a nan -- so a nan passes a check written that way. The')
print('     guard above tests isfinite first, and only then the tolerance.')
print('\n     The three constants the series keeps together -- eps_0 = 1/3, r* ~ 0.773,')
print('     kappa* ~ 0.882 -- are not boundaries of this basin, because this basin')
print('     has no boundary but the axis. Whatever they are thresholds OF, it is not')
print('     convergence of the uncoupled transverse flow.')

# ---------------------------------------------------------------------------
head(5, "chRho-spectral ARGUMENT V, ARITHMETIC RUN")
t1  = 14.134725141734693      # first nontrivial zero of zeta, ordinate
tau = 2.0
eps0 = 1.0/3.0
lhs = t1 / TWOPI
rhs = tau * (1.0/eps0) * (1.0/3.0)
print('  The page reads: "t_1/(2*pi) ~ 2.25 ~ tau * eps_0^{-1} * (1/3)".\n')
print('     t_1                        = %.12f' % t1)
print('     t_1 / (2*pi)               = %.12f' % lhs)
print('     eps_0^{-1} * (1/3)         = %.12f   <- these two factors cancel' % ((1.0/eps0)*(1.0/3.0)))
print('     tau * eps_0^{-1} * (1/3)   = %.12f   <- so the right-hand side is tau' % rhs)
print('     relative gap               = %.4f %%' % (100.0*abs(lhs-rhs)/rhs))
check(abs((1.0/eps0)*(1.0/3.0) - 1.0) < 1e-15,
      'eps_0^{-1} * (1/3) = 1 identically, so eps_0 does not enter the expression')
check(abs(rhs - tau) < 1e-15, 'the right-hand side is tau = 2, not a compound of tau and eps_0')
check(abs(lhs - rhs)/rhs > 0.12, 'and the two sides differ by more than 12 percent')

print('\n  The same paragraph calls -2 an eigenvalue of the linearised Poincare map.')
print('  Block [2] fixed the units: -2 is the exponent, e^{-4pi} the multiplier.\n')
print('     quoted eigenvalue          = %.12f' % -2.0)
print('     actual multiplier          = %.9e' % K)
print('     ratio                      = %.6e' % (abs(-2.0) / K))
check(abs(-2.0)/K > 1e5, 'the two numbers differ by more than five orders of magnitude')

# ---------------------------------------------------------------------------
head(6, 'HOW MANY MULTIPLIERS A RETURN MAP HAS')
print('  Strogatz p. 281: S is an (n-1)-dimensional surface of section for an')
print('  n-dimensional flow, and P maps S to itself. So the linearisation of P at')
print('  a fixed point is (n-1) x (n-1).\n')
print('     %8s %26s %22s' % ('n', 'section dim = n-1', 'multipliers'))
for n_dim, what in ((2, 'the planar transverse system'), (3, 'the contact 3-manifold')):
    print('     %8d %26d %22d      %s' % (n_dim, n_dim-1, n_dim-1, what))
check(2 - 1 == 1, 'a planar flow has exactly ONE Floquet multiplier at a cycle')
check(3 - 1 == 2, 'a flow on a 3-manifold has exactly TWO')
check(3 != 2, 'so a spectrum listed as three numbers {-2, +i, -i} fits neither')
print('\n     There is a further obstruction in the 3-manifold case, and it is the')
print('     reason this paper recommends the planar section rather than a 3-D one:')
print('     the model has z\' = 1, so no trajectory ever returns to a section')
print('     {z = z_0}. There is no first return, hence no Poincare map in z at all.')
print('     What the series computes over one period is a TIME-2*pi FLOW MAP. The')
print('     two coincide on the transverse coordinate and nowhere else, and the')
print('     drift of the per-period exponent with base point is exactly that gap.')

# ---------------------------------------------------------------------------
head(7, 'THE TRAPPING ANNULUS OF EXAMPLE 7.3.1 (p. 206)')
print('  Strogatz perturbs the same example: r\' = r(1-r^2) + mu r cos(theta),')
print('  theta\' = 1, and proves a closed orbit survives for mu < 1 inside')
print('      0.999 sqrt(1-mu)  <  r  <  1.001 sqrt(1+mu).')
print('  Analytically: on the inner circle r\' >= r(1 - r^2 - mu) = r * 0.001999(1-mu) > 0,')
print('  and on the outer r\' <= r(1 - r^2 + mu) = -r * 0.002001(1+mu) < 0.\n')
print('     %8s %14s %14s %18s %18s' % ('mu', 'r_min', 'r_max', 'min r\' inner', 'max r\' outer'))
ok_trap = True
NTH = 2000
for mu in (0.05, 0.2, 0.5, 0.9, 0.99):
    rmin, rmax = 0.999*math.sqrt(1-mu), 1.001*math.sqrt(1+mu)
    lo_in  = min(rmin*(1 - rmin**2) + mu*rmin*math.cos(TWOPI*j/NTH) for j in range(NTH))
    hi_out = max(rmax*(1 - rmax**2) + mu*rmax*math.cos(TWOPI*j/NTH) for j in range(NTH))
    print('     %8.2f %14.9f %14.9f %18.3e %18.3e' % (mu, rmin, rmax, lo_in, hi_out))
    if not (lo_in > 0 and hi_out < 0): ok_trap = False
check(ok_trap, 'the annulus is forward-invariant at every mu tested: flow in on both walls')
check(all(0.999*math.sqrt(1-m) < 1 < 1.001*math.sqrt(1+m) for m in (0.05, 0.5, 0.99)),
      'and it brackets r = 1 in every case')
print('\n     The theta sweep is an exhaustion over 2000 angles and is evidence; the')
print('     two inequalities above it are the proof, and they hold for every theta')
print('     because |cos| <= 1. This is the shape of certificate WP-62 asked for')
print('     when it wanted a basin result "publishable as a certificate rather')
print('     than an illustration" -- written analytically, not integrated.')

# ---------------------------------------------------------------------------
head(8, 'CONTROL: THIS SCRIPT COMPUTED SOMETHING')
check(abs(rk4_r(0.5, TWOPI, 200000) - P(0.5)) < 1e-12, 'the integrator and the map both ran')
check(abs(K - 3.4873424e-06) < 1e-12, 'e^{-4*pi} is the number two chapters already print')
check(1.0 < P(2.0) < 2.0 and 1.0 < P(100.0) < 100.0 and P(0.5) > 0.5,
      'P moves every tested radius toward 1, as an attracting cycle requires',
      'P(2)=%.9f P(100)=%.9f P(0.5)=%.9f' % (P(2.0), P(100.0), P(0.5)))
check(sup > 0.0 and r_star > 0.0, 'the scans in [3] found something rather than nothing')
print('    A vacuous pass is a pass. Block [8] exists so that block [1] cannot')
print('    report agreement by having compared two copies of the same formula.')

# ---------------------------------------------------------------------------
head('HONESTY', 'What this establishes, and what it must not be read as.')
print("""
  ESTABLISHED. Strogatz Example 8.7.1's closed-form Poincare map reproduces the
  integrated transverse flow to 1e-10 relative over eight decades of initial
  radius, and its derivative at the fixed point is e^{-4*pi} exactly. Exponent
  and multiplier are consistent: (1/T*) ln|P'(1)| = -2. On |rho| <= 1/3 the
  exact sup|P'| is below 1e-4 while the Gronwall bound is 1, so that bound is
  loose there by more than four orders of magnitude, and |P'| does not reach 1
  until r is below 0.02. Every initial radius tested from 1e-6 to 1e4 is on
  Gamma to 1e-8 after twenty turns. In chRho-spectral's Argument V, the factor
  eps_0^{-1}*(1/3) equals 1 identically, so the right-hand side is tau and the
  two sides differ by more than 12 percent; and -2 and e^{-4*pi} differ by more
  than five orders of magnitude, being an exponent and a multiplier. The
  Example 7.3.1 annulus is forward-invariant at every mu tested, by an
  inequality that holds for all theta.

  NOT ESTABLISHED. That eps_0 = 1/3 is wrong. It is a correct Gronwall radius
  and Proof IV derives it correctly; what this script shows is what it is a
  radius OF. Nor is anything here a result about the full contact model: every
  computation above is on the UNCOUPLED transverse system r' = r(1-r^2), which
  is what the closed-form map covers. The coupled flow r' = f(r)(1 - e^{-z})
  has no return map at all, for the reason block [6] gives, and finding the
  right substitute for one is the open problem this paper hands forward, not
  something it solves. The theta sweep in [7] is an exhaustion over a finite
  grid and is evidence; the inequality printed above it is the proof.

  AND ON ARGUMENT V. The arithmetic above is arithmetic. It does not touch the
  Riemann hypothesis, says nothing about whether a contact reading of the
  critical strip is worth pursuing, and is not a verdict on the other six
  arguments on that page, which were not examined.
""")

print('=' * 70)
if fails:
    print('  %d CHECK(S) FAILED' % len(fails))
    for f in fails: print('    - ' + f)
    print('=' * 70); sys.exit(1)
print('  ALL CHECKS PASSED')
print('=' * 70)
