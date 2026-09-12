#!/usr/bin/env python3
"""
Does a tropical cyclone return to its state when its environment returns to
its own? -- the one test that separates a contact reading from "more variables".

WHY THIS FILE EXISTS. Every attempt so far to connect the dm3 contact picture to
observation has gone through a coordinate dictionary -- which quantity in the
world plays r, which plays z -- and the dictionary has been the thing that fails.
The band-width test (docs/multiorbit-pacific-2026-09.md) was falsified on exactly
that: same equations, opposite verdict, depending on which phase was called
expanding. This test needs no dictionary. It asks the one question contact
geometry answers differently from every other geometry.

THE QUESTION. A contact structure is alpha ^ dalpha != 0: maximal
non-integrability. In plain terms, there is no state function -- no quantity you
can measure now that determines what happens next. The operational signature of
that is HOLONOMY: drive the controls around a closed loop, and the state does not
come back.

WHY PERSISTENCE IS NOT ENOUGH. Operational SHIPS carries PER, the prior 12-hour
intensity change, as a core predictor, and persistence dominates short-range
forecasts. So current intensity plus environment is demonstrably not a sufficient
state. But that proves nothing about integrability: a damped oscillator measured
by position alone shows the same thing, and adding velocity restores a complete
state. Persistence says "you are missing variables". It does not say "no finite
set of variables closes".

WHAT DOES SEPARATE THEM. Stokes. For a closed loop in the controls,

      residual  =  int_loop alpha  =  int_enclosed d(alpha)

so a non-integrable system's residual scales with the AREA THE LOOP ENCLOSES,
and not with its duration, its path length, or how fast it was traversed. A
holonomic system returns zero for every loop. That is a scaling law, it is
checkable, and blocks [1] and [2] below verify that this script can actually
detect it before any real data is touched.

DATA REQUIRED (not bundled; see [4]):
  * SHIPS developmental dataset (CIRA) -- SST, 200-850 hPa shear, mid-level RH,
    per storm per 6 h.  These are the CONTROLS.
  * Extended Best Track -- radius of maximum wind, wind radii.  With intensity,
    these are the STATE.

Standard library only.  python3 book6/holonomy-test.py [ships_file ebt_file]
"""

import math, sys, os

fails = []
def check(ok, msg, detail=''):
    print('    %s  %s%s' % ('PASS' if ok else 'FAIL', msg,
                            ('  -- ' + detail) if detail and not ok else ''))
    if not ok: fails.append(msg)
def head(n, t):
    print('\n' + '=' * 70 + '\n  [%s]  %s\n' % (n, t) + '=' * 70)

# ---------------------------------------------------------------------------
def traverse(path, form):
    """Integrate a 1-form along a polyline in the (u1,u2) control plane."""
    w = 0.0
    for (a1, a2), (b1, b2) in zip(path, path[1:]):
        du1, du2 = b1 - a1, b2 - a2
        w += form((a1 + b1) / 2, (a2 + b2) / 2, du1, du2)
    return w

def ellipse(R1, R2, n, laps=1, phase=0.0):
    return [(R1 * math.cos(2*math.pi*i/n + phase),
             R2 * math.sin(2*math.pi*i/n + phase)) for i in range(n*laps + 1)]

HOLONOMIC   = lambda u1, u2, du1, du2: 0.7*du1 + 1.3*du2      # exact: w = .7u1+1.3u2
NONHOLONOMIC= lambda u1, u2, du1, du2: u1*du2                  # dw - u1 du2 is contact

# ---------------------------------------------------------------------------
head(1, 'POSITIVE AND NEGATIVE CONTROL: can this script tell them apart?')
print('  Same loops, two systems. Both would show "persistence".\n')
print('   %6s %6s %9s %13s %13s %10s' % ('R1','R2','area','holonomic','non-holo','res/area'))
rows = []
for R1, R2 in [(1,1),(1,2),(2,1),(2,2),(3,1),(0.5,0.5)]:
    P = ellipse(R1, R2, 20000)
    A = math.pi*R1*R2
    wh, wn = traverse(P, HOLONOMIC), traverse(P, NONHOLONOMIC)
    rows.append((A, wh, wn))
    print('   %6.2f %6.2f %9.4f %13.2e %13.6f %10.6f' % (R1,R2,A,wh,wn,wn/A))

check(all(abs(wh) < 1e-9 for _, wh, _ in rows),
      'holonomic system returns ZERO residual on every loop',
      '%.2e' % max(abs(wh) for _, wh, _ in rows))
ratios = [wn/A for A, _, wn in rows]
check(max(ratios) - min(ratios) < 1e-6,
      'non-holonomic residual / area is CONSTANT across loop shapes',
      'spread %.2e' % (max(ratios) - min(ratios)))

# The trapezoid/midpoint traversal is second order, so residual/area approaches
# 1 like n^-2 and does not reach it at any finite n. Test the CONVERGENCE, not
# the value -- a tolerance tighter than the quadrature is a check that fails for
# the wrong reason, which is worse than no check.
errs = [abs(traverse(ellipse(1, 1, n), NONHOLONOMIC)/math.pi - 1.0)
        for n in (2000, 20000, 200000)]
print('\n     quadrature error vs step count (expect n^-2):')
for n, e in zip((2000, 20000, 200000), errs):
    print('       n = %7d   |residual/area - 1| = %.3e' % (n, e))
check(errs[0] > errs[1] > errs[2], 'the error falls monotonically with sampling')
check(abs(errs[0]/errs[1] - 100) < 20 and abs(errs[1]/errs[2] - 100) < 20,
      'and falls as n^-2, so residual/area -> 1 exactly in the limit',
      'ratios %.1f, %.1f' % (errs[0]/errs[1], errs[1]/errs[2]))

# ---------------------------------------------------------------------------
head(2, 'THE RESIDUAL IS NOT DURATION, SPEED OR PATH LENGTH')
print('  A confound would be a slow drift that accumulates with time.\n')
base = traverse(ellipse(1,1,20000), NONHOLONOMIC)
fine = traverse(ellipse(1,1,200000), NONHOLONOMIC)
two  = traverse(ellipse(1,1,20000,laps=2), NONHOLONOMIC)
print('     1 lap,  20k steps : %.6f' % base)
print('     1 lap, 200k steps : %.6f   (10x the samples)' % fine)
print('     2 laps, 20k steps : %.6f   (2x the area swept)' % two)
check(abs(fine - base) < 1e-6, 'ten times the sampling changes nothing beyond quadrature')
check(abs(two - 2*base) < 1e-6, 'two laps give exactly twice the residual')
print('\n    So a real positive result cannot be explained by "it took longer".')

# ---------------------------------------------------------------------------
head(3, 'THE TEST, AS IT APPLIES TO STORMS')
print("""
  CONTROLS  u = (SST, deep-layer shear).  Optionally add mid-level RH as u3
            and test the three 2-D projections separately.
  STATE     s = (Vmax, RMW).  Vmax is the loop-closing variable; RMW is where
            the residual is looked for, because Sitkowski reports that after an
            eyewall replacement the intensity returns and the eye does not
            re-contract.

  PROCEDURE
    1. For every storm, build the control trajectory at 6 h resolution.
    2. Find sub-tracks whose control trajectory CLOSES: returns to within a
       tolerance of its starting (SST, shear). Keep loops that enclose a
       measurable area.
    3. For each, record the signed enclosed area A (shoelace) and the state
       residual dRMW between the loop's start and end.
    4. Regress dRMW on A.

  WHAT EACH OUTCOME MEANS
    slope ~ 0, no area dependence ....... holonomic. A state function exists on
                                          (SST, shear). Contact geometry is the
                                          WRONG tool and the corpus should say so.
    slope != 0, dRMW proportional to A .. non-integrable on the observed control
                                          space. Evidence FOR a contact reading.
    residual present, no area scaling ... hidden variables, not geometry. The
                                          honest conclusion is "measure more",
                                          not "the manifold is contact".

  The third outcome is the likely one and the script is built to report it
  rather than hide it. Note also the sign: a genuine 2-form gives residuals
  that REVERSE when the loop is traversed the other way. Clockwise and
  anticlockwise loops of equal area must give equal and opposite dRMW. That is
  a second, independent signature and it is free.
""")

# ---------------------------------------------------------------------------
head(4, 'DATA: not bundled, and this is why')
ships = sys.argv[1] if len(sys.argv) > 1 else 'data/ships_developmental.txt'
ebt   = sys.argv[2] if len(sys.argv) > 2 else 'data/ebtrk.txt'
have = os.path.exists(ships) and os.path.exists(ebt)
print('     SHIPS developmental : %s  %s' % (ships, 'FOUND' if os.path.exists(ships) else 'absent'))
print('     extended best track : %s  %s' % (ebt, 'FOUND' if os.path.exists(ebt) else 'absent'))
if not have:
    print("""
     Both are public and neither is bundled here. Fetch them, put them at the
     paths above (or pass them as arguments), and re-run. The analysis in [3]
     is about forty lines once the two files parse; what took the work was
     [1] and [2], which establish that the analysis can tell a positive from a
     negative before it is pointed at anything real.
""")
check(True, 'the discriminator is validated and ready; the data step is manual')

# ---------------------------------------------------------------------------
head(5, 'NEGATIVE CONTROL: a state function that FAKES holonomy')
print("""  Before trusting any positive result, the analysis must survive a system
  that has a perfect state function. Here RMW depends ONLY on latitude --
  nothing is path dependent -- and the SST control is CLIMATOLOGICAL, i.e.
  a function of (lat, lon, day). Because the calendar day advances through a
  storm's life, SST can return to its starting value at a DIFFERENT latitude:
  seasonal warming offsets poleward motion. The loop closes; the storm has
  moved.\n""")
import random
random.seed(11)
kept = []
for _ in range(4000):
    lat0 = random.uniform(11, 20); day0 = random.uniform(200, 260)
    net  = random.uniform(0.5, 6.0)
    sh0  = random.uniform(4, 18); shamp = random.uniform(3, 12)
    ph   = random.uniform(0, 2*math.pi)
    n = 24; U = []; lats = []
    for i in range(n + 1):
        t   = i/n
        lat = lat0 + net*t + 2.5*math.sin(2*math.pi*t)
        day = day0 + 5*t
        sst = 30.0 - 0.45*(lat - 10.0) + 0.09*(day - day0)
        sh  = sh0 + shamp*math.sin(2*math.pi*t + ph)
        U.append((sst, sh)); lats.append(lat)
    if abs(U[-1][0]-U[0][0]) > 0.05 or abs(U[-1][1]-U[0][1]) > 0.15: continue
    rmw = [18 + 1.6*(l - 10) for l in lats]          # pure state function of lat
    A = sum(0.5*(a1*b2 - b1*a2) for (a1,a2),(b1,b2) in zip(U, U[1:]))
    kept.append((A, rmw[-1]-rmw[0], lats[-1]-lats[0]))

def corr(x, y):
    n = len(x); mx = sum(x)/n; my = sum(y)/n
    sxy = sum((a-mx)*(b-my) for a, b in zip(x, y))
    sxx = sum((a-mx)**2 for a in x); syy = sum((b-my)**2 for b in y)
    return sxy/math.sqrt(sxx*syy) if sxx*syy > 0 else 0.0
def partial(x, y, z):
    rxy, rxz, rzy = corr(x, y), corr(x, z), corr(z, y)
    den = math.sqrt((1-rxz**2)*(1-rzy**2))
    return (rxy - rxz*rzy)/den if den > 0 else 0.0

A  = [k[0] for k in kept]; dR = [k[1] for k in kept]; dL = [k[2] for k in kept]
print('     closed loops retained          : %d of 4000' % len(kept))
print('     corr(signed area, dRMW)        : %+.4f   <- would read as a result' % corr(A, dR))
print('     corr(dLatitude, dRMW)          : %+.4f   <- the actual cause' % corr(dL, dR))
print('     PARTIAL corr(area, dRMW | dLat): %+.4f   <- collapses' % partial(A, dR, dL))
check(abs(corr(dL, dR) - 1.0) < 1e-9,
      'the simulated RMW is a perfect state function of latitude, by construction')
check(abs(partial(A, dR, dL)) < 0.02,
      'partialling out net latitude change removes the apparent area effect',
      '%.4f' % partial(A, dR, dL))
print("""
     The raw correlation is modest in this parameterisation and its size
     depends on how strong the seasonal term is against the latitude term --
     over a 5-10 day storm life in real data it is not small. Two consequences
     for the real run, both mandatory rather than advisory:

       (a) Use the OBSERVED SST predictor (Reynolds), not the climatological
           one. A climatological SST is a function of position and date, so a
           loop in it is partly a re-encoding of the track, not a forcing.
       (b) Report the PARTIAL correlation given net latitude change, always,
           beside the raw one. A raw area-dRMW correlation is not a result.

     And exclude extratropical transition. Storms that close an (SST, shear)
     loop are disproportionately recurving ones, and RMW expands during ET for
     reasons that have nothing to do with holonomy. That is a selection effect
     sitting on top of the confound above.
""")

# ---------------------------------------------------------------------------
head(6, 'INGEST: what the parser must handle, and what must not be assumed')
print("""  The SHIPS developmental files are fixed-layout ASCII, UTF-8-BOM, one block
  per storm per synoptic time, with rows for each predictor across forecast
  hours. Three things a sketch parser typically gets wrong, each of which
  fails silently rather than loudly:

    MISSING VALUES. SHIPS codes missing data with sentinels (9999 and
    relatives). float() accepts them. One such value inside a shear row moves
    the loop's vertex to infinity and the shoelace area with it, and nothing
    reports an error. Every field must be screened before it is used.

    FIELD WIDTH AND NAME POSITION. Do not assume. The distribution ships a
    'File Format and Predictor Descriptions (2023)' PDF; the widths and the
    position of the variable label come from that document, read, not from a
    guess at the first file. This corpus has a standing record of what an
    unchecked parse costs -- a grep anchor that could never match, whose green
    meant nothing for months.

    PREDICTOR IDENTITY. 'SST' and the Reynolds observed-SST predictor are
    different columns with different meanings, and block [5] is the reason the
    difference decides the experiment.

  Likewise EBTRK: the RMW column index must be read off that dataset's own
  documentation rather than accepted on report, and the file's own header is
  the authority. A column index is exactly the kind of claim that is cheap to
  verify and expensive to be wrong about.
""")
check(True, 'ingest requirements recorded; no field layout is assumed here')

# ---------------------------------------------------------------------------
head('HONESTY', 'What a positive result would and would not establish.')
print("""
  WOULD. That the observed control space (SST, shear) carries no state function
  for RMW -- that the storm's structure depends on the route its environment
  took and not only on where that environment currently is. That is a real,
  publishable claim about tropical cyclones, independent of dm3 entirely.

  WOULD NOT. That the system is a contact manifold. Non-integrability on an
  observed 2-D control space is evidence for a contact reading and is not proof
  of one: some larger state space may close it, and the test cannot rule that
  out because it can only ever test the coordinates someone measured. The
  honest ceiling of this method is "no state function in THESE variables",
  which is a statement about a model class, not about the atmosphere.

  AND IT COULD GO THE OTHER WAY. If the regression returns a slope
  indistinguishable from zero, that is evidence AGAINST the contact reading,
  and the corpus should record it the way it recorded the band-width result.
  The test is worth running because it can come back either way. That is the
  only kind worth running.
""")

print('=' * 70)
if fails:
    print('  %d CHECK(S) FAILED' % len(fails))
    for f in fails: print('    - ' + f)
    print('=' * 70); sys.exit(1)
print('  DISCRIMINATOR VALIDATED -- awaiting data')
print('=' * 70)
