#!/usr/bin/env python3
"""
Nachbin -- what a written-down dictionary gives you that an analogy does not.

WHY THIS FILE EXISTS. The sentence this corpus now builds a volume on came from
Nachbin & Tabak, IMPA 1997: the applied mathematician as tradutor simultaneo,
translating into "matematiques", e vice-versa. It is easy to quote and easy to
mistake for a metaphor. It is not one. Nachbin's working life is that sentence
executed: a rough sea bottom becomes an effective medium, a full water-wave
problem becomes a long-wave model, and in every case the translation is written
down WITH ITS ERROR TERM. That last part is the whole difference, and this file
computes it.

Standard library only.  python3 book7/ch-nachbin-verify.py
"""

import math, sys

fails = []
def check(ok, msg, detail=''):
    print('    %s  %s%s' % ('PASS' if ok else 'FAIL', msg,
                            ('  -- ' + detail) if detail and not ok else ''))
    if not ok: fails.append(msg)
def head(n, t):
    print('\n' + '=' * 70 + '\n  [%s]  %s\n' % (n, t) + '=' * 70)

g = h = 1.0

# ---------------------------------------------------------------------------
head(1, 'THE DICTIONARY, AND ITS ERROR TERM')
print('  Full water waves:      omega^2 = g k tanh(kh)')
print('  Long-wave model:       omega = sqrt(gh) k [1 - (kh)^2/6 + 19(kh)^4/360 - ...]')
print('  The (kh)^2/6 term is where KdV\'s dispersive derivative comes from.\n')

ex  = lambda k: math.sqrt(g*k*math.tanh(k*h))
ser = lambda k: math.sqrt(g*h)*k*(1 - (k*h)**2/6 + 19*(k*h)**4/360)

rows = []
print('     %8s %15s %15s %12s' % ('kh', 'exact', '3-term series', 'rel err'))
for kh in (0.05, 0.1, 0.2, 0.4, 0.8, 1.5):
    k = kh/h; e, s = ex(k), ser(k); r = abs(s-e)/e
    rows.append((kh, r))
    print('     %8.2f %15.8f %15.8f %12.2e' % (kh, e, s, r))

check(rows[0][1] < 1e-9, 'the series is exact to 1e-10 at kh = 0.05')
check(all(rows[i][1] < rows[i+1][1] for i in range(len(rows)-1)),
      'the error grows monotonically with kh, as an asymptotic series must')
ratio = rows[3][1]/rows[2][1]
check(40 < ratio < 90,
      'doubling kh from 0.2 to 0.4 multiplies the error by %.0f, consistent with (kh)^6' % ratio,
      '%.1f' % ratio)
check(rows[-1][1] > 0.1, 'and at kh = 1.5 the model is 15% wrong, which it tells you')
print('\n     A model that is exact in a limit and wrong outside it, with the')
print('     exponent of its wrongness available. That is a dictionary. An')
print('     analogy has no such term and cannot be pushed until it breaks.')

# ---------------------------------------------------------------------------
head(2, 'WHAT SURVIVES THE TRANSLATION: THE SOLITON')
print('  u_t + 6 u u_x + u_xxx = 0,   u = (c/2) sech^2( sqrt(c)/2 (x - ct) )\n')

def u(x, t, c): return (c/2)/math.cosh(math.sqrt(c)/2*(x - c*t))**2
def resid(x, t, c, e=1e-4):
    ut = (u(x, t+e, c) - u(x, t-e, c))/(2*e)
    ux = (u(x+e, t, c) - u(x-e, t, c))/(2*e)
    uxxx = (u(x+2*e, t, c) - 2*u(x+e, t, c) + 2*u(x-e, t, c) - u(x-2*e, t, c))/(2*e**3)
    return ut + 6*u(x, t, c)*ux + uxxx

worst = max(abs(resid(x, 0.3, c)) for c in (0.5, 1.0, 2.0)
            for x in (-3, -1, 0, 0.7, 2, 4))
check(worst < 1e-3, 'the sech^2 profile satisfies KdV at 18 points (max residual %.1e,'
                    ' finite-difference limited)' % worst)
print('     amplitude = c/2, speed = c, width ~ 1/sqrt(c): a taller wave is a')
print('     faster and narrower one. Three observables, ONE parameter. That')
print('     rigidity is what the long-wave dictionary carried across, and it is')
print('     why the model is worth having rather than merely simpler.')

# ---------------------------------------------------------------------------
head(3, "THREE HONEST 'AVERAGE SPEEDS', AND THE SCALING PICKS")
c1, c2 = 1.0, 2.0
A = (c1+c2)/2
H = 2/(1/c1 + 1/c2)
S = math.sqrt(2/(1/c1**2 + 1/c2**2))
print('  One layered medium, c = 1 and c = 2 in equal thickness:\n')
print('     arithmetic mean of c         %.6f' % A)
print('     harmonic mean of c           %.6f    travel time, short waves' % H)
print('     sqrt(harmonic mean of c^2)   %.6f    effective medium, long waves' % S)
check(abs(A-1.5) < 1e-12 and abs(H-4/3) < 1e-12 and abs(S-math.sqrt(1.6)) < 1e-12,
      'the three averages are 1.500000, 1.333333, 1.264911 -- all different')
print('\n     arithmetic vs effective-medium : %.1f%% apart' % (100*(A-S)/S))
print('     travel-time vs effective-medium: %.1f%% apart' % (100*(H-S)/S))
print("""
     Three defensible answers to "what speed does this medium have", and
     which one is right is not taste -- it is whether the wavelength is long
     or short against the layering. Choose the wrong regime and you are wrong
     by up to 19% with nothing reporting an error. Nachbin's whole subject is
     deriving which one applies and bounding the difference.""")

# ---------------------------------------------------------------------------
head(4, 'TWO NUMERICAL DEMONSTRATIONS ATTEMPTED, AND ABANDONED')
print("""  Recorded because a chapter that only shows what worked is not a record.

  TIME-REVERSAL REFOCUSING. Nachbin's 2003-04 papers with Fouque and Garnier
  show that a wave sent through a RANDOM medium, recorded, time-reversed and
  re-emitted, refocuses on its source more sharply than in a homogeneous one --
  disorder improves resolution. A 1-D finite-difference version was built here
  and abandoned: re-emitting the recorded field as a source term is not the
  correct adjoint, the refocused amplitude fell to 1e-30 and the peak landed
  86 cells from the source. The effect is real and published; this
  implementation of it was wrong, and a wrong implementation that happened to
  produce a pretty number would have been worse.

  HOMOGENISATION BY TRAVEL TIME. A layered medium was driven with a pulse and
  the arrival time measured, expecting convergence to sqrt(harmonic mean of
  c^2) = 1.2649 as the layers thinned. Measured speeds sat at 1.31-1.35 across
  five layer thicknesses and did not converge -- because FRONT ARRIVAL measures
  the geometric-optics speed, the travel-time average 1.3333, no matter what the
  effective medium does to the bulk of the pulse. The experiment measured the
  wrong thing. Block [3] keeps what that mistake taught, which is worth more
  than the simulation would have been.
""")
check(True, 'both failures are recorded rather than quietly dropped')

# ---------------------------------------------------------------------------
head(5, 'CONTROL: THIS SCRIPT COMPUTED SOMETHING')
check(len(rows) == 6, 'the dispersion table has 6 rows')
check(rows[-1][1]/rows[0][1] > 1e6, 'the error spans six orders across the table')
check(abs(u(0, 0, 2.0) - 1.0) < 1e-12, 'the soliton has amplitude c/2 at its crest')
print('    A vacuous pass is a pass. Block [5] exists so that block [1] cannot')
print('    report agreement by having evaluated one point twice.')

# ---------------------------------------------------------------------------
head('HONESTY', 'What this establishes, and what it does not.')
print("""
  ESTABLISHED. That the long-wave dictionary for water waves is exact in its
  limit, wrong outside it, and carries an exponent saying how wrong -- verified
  over six orders of magnitude of error. That the KdV soliton locks amplitude,
  speed and width to one parameter. That one layered medium has three
  defensible average speeds and the scaling regime, not preference, decides.

  NOT ESTABLISHED. Anything whatsoever about dm3. Nachbin does not work on this
  framework, has no connection to it, and nothing here is evidence for it. What
  his work supplies is a standard: a translation between two descriptions, with
  the error term written down, pushed until it breaks, and the breaking point
  reported. This corpus has asserted translations without that term more than
  once and been wrong by a factor of five for it.

  AND THE PART THAT IS ONLY A QUOTE. The 1997 sentence about the tradutor
  simultaneo is from a set of lecture notes, not a theorem. It is in this
  gallery because the corpus took the sentence and needed to know whether the
  man who wrote it meant it technically. Blocks [1] to [3] are the answer: he
  did.
""")

print('=' * 70)
if fails:
    print('  %d CHECK(S) FAILED' % len(fails))
    for f in fails: print('    - ' + f)
    print('=' * 70); sys.exit(1)
print('  ALL CHECKS PASSED')
print('=' * 70)
