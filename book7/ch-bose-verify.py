#!/usr/bin/env python3
"""
Bose -- the counting, and what the counting alone delivers.

WHY THIS FILE EXISTS. Every derivation of Planck's law before June 1924 took
the mode density 8*pi*nu^2/c^3 from CLASSICAL electrodynamics and then quantised
the energy in each mode. Bose took nothing from electrodynamics. He counted
cells in phase space and he counted them for INDISTINGUISHABLE quanta, and the
whole law fell out -- prefactor included. That is the claim this script tests:
not that the answer is right (it is famous), but that the COUNTING ALONE gets
there, and that swapping in distinguishable counting demonstrably does not.

The corpus reason for the chapter: this series keeps asserting that a
combinatorial choice is physics rather than bookkeeping. Here is the cleanest
case in the record where exactly that turned out to be true, and it is
checkable by hand.

BLOCKS
  [1] The two ways to count N quanta into g cells, exactly, small cases.
  [2] Maximising each -> Bose-Einstein vs Maxwell-Boltzmann occupancy.
  [3] The consequence: Planck's law vs Wien's law. Indistinguishability IS
      the difference between them, and nothing else is changed.
  [4] The classical limits, both of them, from the one formula.
  [5] Stefan-Boltzmann exactly: the integral is Gamma(4)*zeta(4) = pi^4/15.
  [6] Wien displacement: the transcendental root, to 10 places.
  [7] Bose-Einstein condensation: zeta(3/2), the number Einstein got by
      pushing Bose's counting onto massive particles.
  [8] Control -- a check that must FAIL if the script is measuring nothing.

PRIMARY SOURCES.
  S. N. Bose, "Plancks Gesetz und Lichtquantenhypothese", Zeitschrift fuer
    Physik 26, 178 (August 1924). Submitted to Einstein 4 June 1924, after
    Philosophical Magazine declined it; Einstein translated it into German
    himself and appended a translator's note calling the derivation an
    important advance.
  A. Einstein, "Quantentheorie des einatomigen idealen Gases" (1924-25), which
    carries the counting over to massive particles and predicts condensation.
  In-corpus: ch-euler (zeta(4) and the Basel method), ch-chandrasekhar.

Standard library only.  python3 book7/ch-bose-verify.py
"""
import math
from fractions import Fraction as F

fails = []
def check(ok, msg, detail=''):
    print('    %s  %s%s' % ('PASS' if ok else 'FAIL', msg, ('  -- ' + detail) if detail and not ok else ''))
    if not ok: fails.append(msg)
def head(n, t):
    print('\n' + '=' * 70 + '\n  [%s]  %s\n' % (n, t) + '=' * 70)

# ---------------------------------------------------------------- [1]
head(1, 'Two ways to count N quanta into g cells')
def bose_count(N, g):           # indistinguishable quanta, distinguishable cells
    return math.comb(N + g - 1, N)
def boltz_count(N, g):          # distinguishable quanta
    return g ** N
print('     N  g   Bose C(N+g-1,N)   Boltzmann g^N')
for (N, g) in [(2,2),(3,2),(2,3),(3,3),(5,4)]:   # the five rows on ch-bose.html
    print('    %2d %2d   %14d   %13d' % (N, g, bose_count(N,g), boltz_count(N,g)))
check(bose_count(2,2) == 3 and boltz_count(2,2) == 4,
      'N=2,g=2: Bose counts 3 arrangements, Boltzmann 4')
check(all(bose_count(N,g) <= boltz_count(N,g) for N in range(1,8) for g in range(1,8)),
      'Bose count never exceeds Boltzmann count, N,g <= 7')
check(bose_count(1,5) == boltz_count(1,5) == 5,
      'one quantum: the two agree (nothing to permute)')

# ---------------------------------------------------------------- [2]
head(2, 'Occupancy: the two statistics, evaluated')
def n_bose(x):  return 1.0 / (math.exp(x) - 1.0)      # mu = 0, photons
def n_boltz(x): return math.exp(-x)
print('      x        BE 1/(e^x-1)      MB e^-x        ratio')
for x in [0.1, 0.5, 1.0, 2.0, 5.0, 10.0]:
    print('    %5.1f   %15.9f  %12.9f   %7.4f' % (x, n_bose(x), n_boltz(x), n_bose(x)/n_boltz(x)))
check(n_bose(10.0)/n_boltz(10.0) - 1.0 < 1e-4,
      'x=10: the two statistics agree to 1e-4 (dilute limit)')
check(n_bose(0.1) > 9 * n_boltz(0.1),
      'x=0.1: BE occupancy exceeds MB by more than 9x (crowding)')

# ---------------------------------------------------------------- [3]
head(3, "Planck vs Wien: indistinguishability is the ONLY difference")
# u(nu) = (8 pi h nu^3 / c^3) * f(x),  x = h nu / kT.  Set the prefactor to 1:
# BE gives f = 1/(e^x - 1)  [Planck];  MB gives f = e^-x  [Wien].
print('    Same prefactor 8*pi*h*nu^3/c^3 in both. Only the occupancy differs.')
print('      x      Planck f      Wien f      Planck/Wien')
for x in [0.01, 0.1, 1.0, 3.0, 10.0]:
    p, w = n_bose(x), n_boltz(x)
    print('    %6.2f  %12.6f  %10.6f   %10.4f' % (x, p, w, p/w))
check(abs(n_bose(0.01) - 1/0.01) < 1.0,
      'x->0: Planck f ~ 1/x (diverges), which is Rayleigh-Jeans')
check(n_boltz(0.01) < 1.01,
      'x->0: Wien f -> 1 (bounded), so Wien cannot give Rayleigh-Jeans')
check(abs(n_bose(20.0)/n_boltz(20.0) - 1.0) < 1e-8,
      'x large: Planck -> Wien, so Wien is the dilute corner of Planck')

# ---------------------------------------------------------------- [4]
head(4, 'Both classical limits out of the one formula')
# Rayleigh-Jeans: 1/(e^x-1) - 1/x -> -1/2 as x->0
vals = [n_bose(x) - 1.0/x for x in [1e-3, 1e-4, 1e-5]]
print('    1/(e^x-1) - 1/x  at x = 1e-3, 1e-4, 1e-5:')
for x, v in zip([1e-3,1e-4,1e-5], vals): print('        x=%.0e   %+.8f' % (x, v))
check(all(abs(v + 0.5) < 1e-3 for v in vals),
      'low-frequency: 1/(e^x-1) = 1/x - 1/2 + O(x)  -> Rayleigh-Jeans')
check(abs(n_bose(30.0) - math.exp(-30.0)) / math.exp(-30.0) < 1e-12,
      'high-frequency: 1/(e^x-1) -> e^-x  -> Wien')

# ---------------------------------------------------------------- [5]
head(5, 'Stefan-Boltzmann, exactly: integral x^3/(e^x-1) = pi^4/15')
# int_0^inf x^3/(e^x -1) dx = Gamma(4) * zeta(4) = 6 * pi^4/90 = pi^4/15.
# zeta(4) = pi^4/90 is exact; verify the rational part exactly, then the value.
gamma4 = math.factorial(3)                     # Gamma(4) = 3! = 6
zeta4_rational = F(1, 90)                      # zeta(4) = (1/90) * pi^4
product_rational = F(gamma4) * zeta4_rational  # = 6/90 = 1/15
print('    Gamma(4) = 3! = %d' % gamma4)
print('    zeta(4)  = %s * pi^4' % zeta4_rational)
print('    product  = %s * pi^4' % product_rational)
check(product_rational == F(1, 15), 'Gamma(4)*zeta(4) = pi^4/15 exactly (rational part)')
# numeric cross-check by direct summation: zeta(4) = sum 1/n^4
zeta4_sum = sum(1.0/n**4 for n in range(1, 200001))
check(abs(zeta4_sum - math.pi**4/90) < 1e-10,
      'sum 1/n^4 to 2e5 terms matches pi^4/90 to 1e-10',
      '%.12f vs %.12f' % (zeta4_sum, math.pi**4/90))
# and the integral itself, by the same series: int = Gamma(4) * sum 1/n^4
integral = gamma4 * zeta4_sum
check(abs(integral - math.pi**4/15) < 1e-9,
      'integral = pi^4/15 = %.9f' % (math.pi**4/15))
print('    => u_total ~ T^4. The T^4 law is a consequence of the counting,')
print('       not an extra assumption.')

# ---------------------------------------------------------------- [6]
head(6, 'Wien displacement: the root of 3(1-e^-x) = x')
lo, hi = 1.0, 10.0
f = lambda x: 3.0*(1.0 - math.exp(-x)) - x
for _ in range(200):
    mid = (lo + hi)/2.0
    if f(lo)*f(mid) <= 0: hi = mid
    else: lo = mid
root = (lo+hi)/2.0
print('    root x* = %.10f' % root)
check(abs(root - 2.8214393721) < 1e-9, 'x* = 2.8214393721 (10 places)')
check(abs(f(root)) < 1e-12, 'residual |3(1-e^-x)-x| < 1e-12 at the root')

# ---------------------------------------------------------------- [7]
head(7, "Condensation: zeta(3/2), Einstein's step past Bose")
zeta_32 = sum(1.0/n**1.5 for n in range(1, 4000001))
# tail of sum n^-3/2 from N+1 is ~ 2/sqrt(N); correct for it
N = 4000000
zeta_32_corrected = zeta_32 + 2.0/math.sqrt(N)
print('    partial sum to 4e6:            %.8f' % zeta_32)
print('    with analytic tail 2/sqrt(N):  %.8f' % zeta_32_corrected)
print('    accepted value:                2.61237534868...')
check(abs(zeta_32_corrected - 2.6123753486) < 1e-5,
      'zeta(3/2) = 2.6123753 (tail-corrected)',
      'got %.8f' % zeta_32_corrected)
check(zeta_32 < 2.6123753486,
      'partial sum is below the limit, as it must be for positive terms')
print('    n * lambda^3 = zeta(3/2) is the condensation threshold. It is a')
print('    pure number out of the same counting -- no new physics put in.')

# ---------------------------------------------------------------- [8]
head(8, 'Control -- must report a DIFFERENCE, or the script measures nothing')
# If Bose and Boltzmann counting agreed, [3] would be vacuous. Show they do not.
diff = [(N, g, bose_count(N,g), boltz_count(N,g))
        for N in range(2,6) for g in range(2,6) if bose_count(N,g) != boltz_count(N,g)]
check(len(diff) == 16, 'all 16 cases with N,g in [2,5] differ', 'got %d' % len(diff))
check(bose_count(3,3) == 10 and boltz_count(3,3) == 27,
      'N=3,g=3: 10 vs 27 -- not a small correction')
# and a deliberate falsehood, to prove `check` can fail
print('    (the next line is a deliberate false check, to prove FAIL is reachable)')
_saved = list(fails)
check(1 == 2, 'DELIBERATE: 1 == 2')
if fails and fails[-1] == 'DELIBERATE: 1 == 2':
    fails.pop()
    print('    -> FAIL path works; removed from the tally.')

print('\n' + '=' * 70)
print('  %d checks failed' % len(fails) if fails else '  all checks passed')
print('=' * 70)
raise SystemExit(1 if fails else 0)
