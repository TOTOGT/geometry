#!/usr/bin/env python3
"""
Strogatz -- which of the helix's numbers are the textbook's, computed.

WHY THIS FILE EXISTS. The Book 6 helix toy model is built on the flow
    r' = f(r)(1 - e^{-z}),   theta' = 1,   z' = 1
with the closure conditions f(1) = 0, f'(1) = -2, f(r)(r-1) < 0, and the
canonical closure f_cub(r) = r - r^3. That radial field, with theta' = 1,
is Strogatz's Example 7.1.1 (Nonlinear Dynamics and Chaos, 2nd ed., p. 199)
exactly. Strogatz sits in that paper's bibliography and nowhere in its
argument, and the series quotes T* = 2*pi and mu = -2 in several chapters
without saying where they come from. This script separates the numbers the
textbook already fixes from the numbers the contact coupling actually
produces.

BLOCKS
  [1] Example 7.1.1 integrated: the cycle at r = 1, the period 2*pi,
      and d/dr[r - r^3] at r = 1.
  [2] The closure conditions are a normalisation: both canonical closures
      have f'(1) = -2 because they were required to.
  [3] The closed form of the transverse equation, checked against RK4, and
      the exponent mu = -2 with its bounded correction.
  [4] The per-period Floquet data, and the base-point dependence that
      ch-grothendieck already reported.
  [5] Strogatz's Rule of Thumb 1 (p. 254) against the pinned radius: where
      the degeneracy claim is correct.
  [6] The vector field has no zeros anywhere, which is the sense in which
      the Hopf reading is frozen rather than autonomous.
  [7] The paper's own source, read: the bibitem, and its citations.
  [8] Control.

PRIMARY SOURCE. S. H. Strogatz, "Nonlinear Dynamics and Chaos", 2nd ed.,
Westview 2015 / CRC 2018, ISBN 978-0-8133-4910-7. Sections 7.0 (p. 198),
7.1 (p. 199), 8.2 (pp. 251-256).
INTERNAL SOURCE. book6/differential-equations/helix-toy-model/helix_toy_model.tex

Standard library only.  python3 book7/ch-strogatz-verify.py
"""

import math, sys

fails = []
def check(ok, msg, detail=''):
    print('    %s  %s%s' % ('PASS' if ok else 'FAIL', msg,
                            ('  -- ' + detail) if detail and not ok else ''))
    if not ok: fails.append(msg)
def head(n, t):
    print('\n' + '=' * 70 + '\n  [%s]  %s\n' % (n, t) + '=' * 70)

def rk4(field, y0, t0, t1, n):
    y, t, h = list(y0), t0, (t1 - t0) / n
    for _ in range(n):
        k1 = field(t, y)
        k2 = field(t + h/2, [y[i] + h/2*k1[i] for i in range(len(y))])
        k3 = field(t + h/2, [y[i] + h/2*k2[i] for i in range(len(y))])
        k4 = field(t + h,   [y[i] + h*k3[i]   for i in range(len(y))])
        y = [y[i] + h/6*(k1[i] + 2*k2[i] + 2*k3[i] + k4[i]) for i in range(len(y))]
        t += h
    return y

# ---------------------------------------------------------------------------
head(1, 'EXAMPLE 7.1.1, INTEGRATED -- THE CYCLE, THE PERIOD, THE EIGENVALUE')
print('  Strogatz p. 199, Example 7.1.1 "A simple limit cycle":')
print('      r\' = r(1 - r^2),   theta\' = 1,   r >= 0')
print('  He reports: r* = 0 unstable, r* = 1 stable, and the limit cycle')
print('  solution x(t) = cos(t + theta_0). Integrate it and look.\n')

f_cub = lambda r: r - r**3
field_711 = lambda t, y: [f_cub(y[0]), 1.0]

print('     %10s %16s %16s' % ('r(0)', 'r(t=40)', '|r(40) - 1|'))
ok_conv = True
for r0 in (0.05, 0.3, 0.9, 1.4, 3.0, 12.0):
    r_end, th_end = rk4(field_711, [r0, 0.0], 0.0, 40.0, 20000)
    print('     %10.2f %16.12f %16.3e' % (r0, r_end, abs(r_end - 1.0)))
    if abs(r_end - 1.0) > 1e-9: ok_conv = False
check(ok_conv, 'every start off the axis lands on r = 1 to better than 1e-9')

th_end = rk4(field_711, [0.9, 0.0], 0.0, 40.0, 20000)[1]
check(abs(th_end - 40.0) < 1e-9,
      'theta advances at rate 1, so the period on the cycle is exactly 2*pi',
      'theta(40) = %.12f' % th_end)
print('     T* = 2*pi = %.12f  -- this is theta\' = 1 and nothing else.' % (2*math.pi))

# the transverse eigenvalue, by hand and by difference quotient
h = 1e-6
dq = (f_cub(1 + h) - f_cub(1 - h)) / (2*h)
print('\n     d/dr [ r - r^3 ] at r = 1 :  1 - 3r^2 |_{r=1} = 1 - 3 = -2')
check(abs(dq + 2.0) < 1e-8,
      'the central difference quotient agrees: f\'(1) = %.10f' % dq)
print('     So BOTH headline constants of the helix -- T* = 2*pi and mu = -2 --')
print('     are read off Example 7.1.1 before any contact structure appears.')

# ---------------------------------------------------------------------------
head(2, "THE CLOSURE CONDITIONS ARE A NORMALISATION, NOT A FINDING")
print('  helix_toy_model.tex eq. (closure-cond) requires of every closure:')
print('      f(1) = 0,   f\'(1) = -2,   f(r)(r-1) < 0 for r > 0, r != 1')
print('  and offers two that obey it.\n')

f_sat = lambda r: -2.0*(r - 1.0) / (1.0 + (r - 1.0)**2)
for name, f in (('f_cub(r) = r - r^3', f_cub),
                ('f_sat(r) = -2(r-1)/(1+(r-1)^2)', f_sat)):
    v1 = f(1.0)
    d1 = (f(1 + h) - f(1 - h)) / (2*h)
    sign_ok = all(f(r)*(r - 1.0) < 0
                  for r in [0.01 + 0.01*i for i in range(400)] if abs(r - 1.0) > 1e-3)
    print('     %-34s f(1) = %+.1e   f\'(1) = %+.8f' % (name, v1, d1))
    check(abs(v1) < 1e-12 and abs(d1 + 2.0) < 1e-7 and sign_ok,
          '%s satisfies all three closure conditions' % name.split('(')[0])
print('\n     f\'(1) = -2 is a HYPOTHESIS of the model, imposed on every admissible')
print('     closure. A theorem that concludes mu = -2 from it has reported the')
print('     hypothesis back. What that theorem actually establishes is block [3].')

# ---------------------------------------------------------------------------
head(3, 'WHAT THE CONTACT COUPLING DOES: THE CLOSED FORM AND THE BOUNDED ERROR')
print('  Linearising the model about Gamma = {r = 1} with eps := r - 1 gives')
print('      eps\' = f\'(1)(1 - e^{-z}) eps = 2 eps (e^{-z} - 1),   z = z_0 + t')
print('  and the paper solves it:')
print('      eps(t) = eps_0 exp( -2t + 2 e^{-z_0} (1 - e^{-t}) )\n')

def log_closed(t, z0):
    """ln|eps(t)/eps_0| -- kept in log form so large t does not underflow."""
    return -2.0*t + 2.0*math.exp(-z0)*(1.0 - math.exp(-t))
def closed(t, z0, e0=1.0):
    return e0 * math.exp(log_closed(t, z0))

lin = lambda z0: (lambda t, y: [2.0*y[0]*(math.exp(-(z0 + t)) - 1.0)])

print('     %8s %10s %22s %22s %12s' % ('z_0', 't', 'RK4', 'closed form', 'rel.err'))
ok_cf = True
for z0 in (-2.0, 0.0, 1.0, 5.0):
    for t in (1.0, 6.0):
        num = rk4(lin(z0), [1.0], 0.0, t, 40000)[0]
        ana = closed(t, z0)
        rel = abs(num - ana) / abs(ana)
        print('     %8.1f %10.1f %22.14e %22.14e %12.2e' % (z0, t, num, ana, rel))
        if rel > 1e-10: ok_cf = False
check(ok_cf, 'the closed form solves the transverse equation to 1e-10 relative')

print()
print('  The exponent is mu = lim (1/t) ln|eps(t)/eps_0|. The correction term')
print('  2e^{-z_0}(1 - e^{-t}) is bounded by 2e^{-z_0} for all t, so |mu + 2| can')
print('  never exceed 2e^{-z_0}/t -- which is the whole proof, in one line.\n')
print('     %8s %16s %16s %16s' % ('z_0', 'mu at t=1e4', 'mu at t=1e7', 'bound 2e^{-z_0}/t'))
ok_mu = True
for z0 in (-2.0, 0.0, 1.0, 5.0):
    corr = 2.0*math.exp(-z0)
    m4, m7 = log_closed(1e4, z0)/1e4, log_closed(1e7, z0)/1e7
    print('     %8.1f %16.10f %16.10f %16.3e' % (z0, m4, m7, corr/1e7))
    if not (abs(m7 + 2.0) <= corr/1e7 + 1e-15 and abs(m7 + 2.0) < abs(m4 + 2.0)):
        ok_mu = False
check(ok_mu, 'from every base point |mu + 2| stays inside 2e^{-z_0}/t and shrinks')
print('     The correction column is the whole of the e^{-z} contribution, and it')
print('     is bounded in t. THAT is the content of the exponent theorem -- not')
print('     the value -2, which came in with f\'(1). Integrability is the result.')

# ---------------------------------------------------------------------------
head(4, 'PER-PERIOD FLOQUET DATA, AND WHERE IT STOPS BEING A CONSTANT')
mult = math.exp(-4.0*math.pi)
print('  With mu = -2 and T* = 2*pi the per-period exponent is mu T* = -4*pi')
print('  and the transverse multiplier is e^{-4*pi}.\n')
check(abs(-2.0*(2*math.pi) + 4.0*math.pi) < 1e-12, 'mu T* = -4*pi exactly')
print('     e^{-4*pi} = %.9e' % mult)
check(abs(mult - 3.487342e-06) < 1e-11,
      'matches the 3.487342e-06 already printed in ch-feynman', '%.9e' % mult)

print('\n  But that is the saturated value. Over one actual period from z_0 the')
print('  exponent is  int_0^{2pi} 2(e^{-(z_0+t)} - 1) dt = -4pi + 2e^{-z_0}(1 - e^{-2pi}).\n')
print('     %8s %20s %20s' % ('z_0', 'exponent over 2pi', 'multiplier'))
ok_bp = True
prev = None
for z0 in (0.0, 1.0, 2.0, 4.0, 8.0, 16.0):
    ex = -4.0*math.pi + 2.0*math.exp(-z0)*(1.0 - math.exp(-2.0*math.pi))
    # independent numerical integration of the same quantity
    n = 200000
    s = sum(2.0*(math.exp(-(z0 + (i + 0.5)*(2*math.pi)/n)) - 1.0) for i in range(n)) * (2*math.pi)/n
    if abs(s - ex) > 1e-8: ok_bp = False
    print('     %8.1f %20.12f %20.9e' % (z0, ex, math.exp(ex)))
    prev = ex
check(ok_bp, 'the closed-form per-period exponent matches midpoint quadrature')
check(abs(prev - (-4.0*math.pi)) < 1e-6,
      'it tends to -4*pi as z_0 grows, and differs from it at every finite z_0')
print('     This is the base-point dependence ch-grothendieck measured when it')
print('     asked whether the multiplier could be an index. It cannot: an index')
print('     does not move with where you start.')

# ---------------------------------------------------------------------------
head(5, "RULE OF THUMB 1 (STROGATZ p. 254) AGAINST THE PINNED RADIUS")
print('  Strogatz, generic supercritical Hopf: "The size of the limit cycle grows')
print('  continuously from zero, and increases proportional to sqrt(mu - mu_c)."')
print('  For r\' = lambda r - a r^3 the stable radius is sqrt(lambda/a).\n')
print('     %10s %18s %18s' % ('z', 'generic  a = 1', 'model  a = lambda'))
ok_pin = True
for z in (2.0, 1.0, 0.5, 0.1, 0.01, 0.001, 1e-6):
    lam = 1.0 - math.exp(-z)
    generic = math.sqrt(lam / 1.0)
    pinned = math.sqrt(lam / lam)
    print('     %10.2e %18.12f %18.12f' % (z, generic, pinned))
    if abs(pinned - 1.0) > 1e-12: ok_pin = False
check(ok_pin, 'with a(z) = lambda(z) the radius is identically 1, for every z > 0')
check(math.sqrt(1.0 - math.exp(-1e-6)) < 1e-3,
      'while the generic radius does go to 0 at onset, as the rule of thumb says')
print('\n     So the degeneracy claim is CORRECT, and correct by Strogatz\'s own')
print('     criterion: the cycle does not emanate from the origin. What collides')
print('     is the name. Strogatz p. 256 reserves "degenerate Hopf bifurcation"')
print('     for the case with NO limit cycles on either side and a continuous band')
print('     of closed orbits instead -- a nonlinear centre, his damped-pendulum')
print('     example. The helix has an isolated attracting cycle on both sides.')
print('     Two different objects, one term, and both books in one bibliography.')

# ---------------------------------------------------------------------------
head(6, 'THE FIELD HAS NO ZEROS, SO THE HOPF READING IS A FROZEN ONE')
print('  Strogatz opens 8.2 with "Suppose a two-dimensional system has a stable')
print('  fixed point." The model is three-dimensional and z\' = 1 identically,')
print('  so the vector field (r\', theta\', z\') never vanishes.\n')
worst, arg = None, None
for i in range(401):
    r = 0.0 + i*0.01
    for j in range(161):
        z = -4.0 + j*0.05
        v = (f_cub(r)*(1.0 - math.exp(-z)), 1.0, 1.0)
        nrm = math.sqrt(v[0]**2 + v[1]**2 + v[2]**2)
        if worst is None or nrm < worst: worst, arg = nrm, (r, z)
print('     scanned r in [0, 4] x z in [-4, 4] on a 401 x 161 grid')
print('     minimum |(r\', theta\', z\')| = %.12f at (r, z) = (%.2f, %.2f)' % (worst, arg[0], arg[1]))
check(abs(worst - math.sqrt(2.0)) < 1e-9,
      'the minimum is sqrt(2) = %.12f, attained wherever r\' = 0' % math.sqrt(2.0))
check(worst > 1.0, 'and it is bounded away from zero, so there is no equilibrium')
print('\n     The 2x2 Jacobian in the degenerate-Hopf theorem is the Jacobian of the')
print('     (x,y) subsystem at a FROZEN z. In the actual flow z is swept at unit')
print('     rate and every trajectory crosses z = 0 in finite time. The paper says')
print('     this in its exercises ("freeze z"; solution 4 disqualifies the')
print('     codimension-one normal forms). The theorem and the abstract do not.')

# ---------------------------------------------------------------------------
head(7, 'THE SOURCE CHECKED AGAINST ITSELF: THE BIBITEM, AND ITS CITATIONS')
import os
TEX = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'book6',
                   'differential-equations', 'helix-toy-model', 'helix_toy_model.tex')
print('  Reading %s\n' % os.path.normpath(TEX).split('geometry')[-1].lstrip('/'))
if not os.path.exists(TEX):
    check(False, 'the helix toy model source is where the chapter says it is', TEX)
else:
    src = open(TEX, encoding='utf-8', errors='replace').read()
    n_bib  = src.count('\\bibitem{Strogatz}')
    n_cite = src.count('\\cite{Strogatz}') + src.count('cite{Strogatz,') + src.count(',Strogatz}')
    n_ex   = src.count('7.1.1')
    flat   = ' '.join(src.split())
    print('     \\bibitem{Strogatz}   occurrences : %d' % n_bib)
    print('     \\cite{Strogatz}      occurrences : %d   (0 before 2026-09-15)' % n_cite)
    print('     "7.1.1"              occurrences : %d   (0 before 2026-09-15)' % n_ex)
    check(n_bib == 1, 'the textbook is in the bibliography exactly once')
    check(n_cite >= 1, 'and it is now cited in the body, where its data are used', str(n_cite))
    check(n_ex >= 1, 'Example 7.1.1 is now named in the paper that is built on it')
    check("f(1)=0" in src.replace(' ', '') and "f'(1)=-2" in src.replace(' ', ''),
          'the closure conditions f(1) = 0 and f\'(1) = -2 are in the source as stated')
    print()
    for phrase, what in (
            ('no periodic orbit', 'the flow is stated to have no periodic orbit'),
            ('Guckenheimer and Holmes', 'the sense of "degenerate" is attributed'),
            ('p.~256', 'and separated from the Strogatz p. 256 sense'),
            ('frozen', 'the frozen-z reading of Theorem 5.1 is stated'),
            ('Corrections', 'the revision is listed in a Corrections section')):
        check(phrase in flat, what, phrase)
print('\n     This block began life reporting the opposite: one bibitem, zero')
print('     citations, and no mention of 7.1.1 anywhere in the paper built on it.')
print('     The four clauses were carried into the source on 2026-09-15, listed')
print('     there under Corrections, and the block now checks the repaired state.')
print('     Example 7.1.1 is the standard first example of a limit cycle and')
print('     belongs to nobody; what was missing was the pointer, and it is there.')

# ---------------------------------------------------------------------------
head(8, 'CONTROL: THIS SCRIPT COMPUTED SOMETHING')
check(abs(rk4(field_711, [0.3, 0.0], 0.0, 40.0, 20000)[0] - 1.0) < 1e-9,
      'the RK4 integrator ran and converged')
check(abs(closed(0.0, 1.0) - 1.0) < 1e-15, 'the closed form is normalised at t = 0')
check(abs(f_cub(2.0) - (-6.0)) < 1e-12, 'f_cub(2) = 2 - 8 = -6, as arithmetic requires')
print('    A vacuous pass is a pass. Block [8] exists so that block [1] cannot')
print('    report convergence by having integrated nothing.')

# ---------------------------------------------------------------------------
head('HONESTY', 'What this establishes, and what it must not be read as.')
print("""
  ESTABLISHED. The radial field of the Book 6 helix model, in its canonical
  cubic closure, is Strogatz Example 7.1.1. Its cycle radius 1, its period
  2*pi and its transverse eigenvalue -2 are all fixed before the contact
  structure enters: the first two by the example, the third by the closure
  condition f'(1) = -2, which is imposed and not derived. The closed-form
  solution of the transverse equation is correct to 1e-10 against RK4, and
  the exponent returns to -2 from every base point with a correction bounded
  by 2e^{-z_0}. The per-period exponent is -4pi only in the limit; at finite
  z_0 it is -4pi + 2e^{-z_0}(1 - e^{-2pi}). With a(z) = lambda(z) the cycle
  radius is identically 1 where the generic radius would be sqrt(lambda).
  The three-dimensional field has no zero.

  NOT ESTABLISHED. That anything in the helix model is wrong. Every theorem
  checked here is true as stated. The finding was about provenance and about
  one word: numbers the series quotes as results of its own are the textbook
  example's, and "degenerate Hopf" names a different phenomenon in Strogatz
  p. 256 than it does in the paper. Neither is a mathematical error, and this
  script does not make either into one. Nor does it check the closure-
  dependent escape, the contact-Hamiltonian no-go, or the cosmological
  reading -- those are the model's own and are outside its scope.

  THE NAMING IS SETTLED. As of 2026-09-15 the source states the sense --
  Guckenheimer and Holmes', a vanishing first Lyapunov coefficient, not
  Strogatz p. 256's nonlinear centre -- says where z is held fixed in the
  Hopf theorem, says that the flow has no periodic orbit and that T* is the
  period of the (r, theta) projection, and cites Example 7.1.1 at the places
  its data are used. Block [7] checks that state rather than the old one.
""")

print('=' * 70)
if fails:
    print('  %d CHECK(S) FAILED' % len(fails))
    for f in fails: print('    - ' + f)
    print('=' * 70); sys.exit(1)
print('  ALL CHECKS PASSED')
print('=' * 70)
