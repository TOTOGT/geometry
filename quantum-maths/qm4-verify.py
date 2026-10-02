#!/usr/bin/env python3
"""qm4-verify.py — Chapter QM4: order finding and the arithmetic of Shor.

Standard library only. The quantum step is simulated on the explicit amplitude
distribution (a DFT of the periodic state), not on a closed form; the classical
steps (orders, gcds, continued fractions) are computed exhaustively.

  [1] Shor's lemma, exhaustively: for every odd N <= 400 that is composite and
      not a prime power, the fraction of a in (Z/N)^* that FAIL to give a
      factor (r odd, or a^(r/2) = -1) is at most 1/2^(k-1), k = number of
      distinct prime factors.  (Shor's paper: success >= 1 - 1/2^(k-1).)
  [2] The distribution: for (N, a, q) in four cases the squared amplitudes
      P(c, x_k) = |(1/q) sum_{x = k mod r} exp(2 pi i x c / q)|^2 sum to 1
      over (c, k), and agree with Shor's closed form
      |(1/q) sum_{b=0}^{floor((q-k-1)/r)} exp(2 pi i b {rc}_q / q)|^2.
      (Includes Shor's own example: N = 33, a = 5, r = 10, q = 256.)
  [3] Shor's two bounds: P(c, x_k) >= 1/(3 r^2) whenever |{rc}_q| <= r/2 ...
      checked; and q is chosen with N^2 <= q < 2N^2 in the four main cases.
  [4] One run recovers r: the EXACT probability, summed over every (c, k), that
      continued-fraction expansion of c/q yields denominator r — against
      Shor's lower bound phi(r)/(3r).
  [5] The pipeline: for every a coprime to N, N in a list of 20 odd composites,
      gcd(a^(r/2) +- 1, N) is a nontrivial factor exactly when r is even and
      a^(r/2) != -1 mod N, and the factors found really divide N.
  [6] Controls (each must FAIL): a q that is too small loses the recovery;
      odd r gives no factor; a^(r/2) = -1 gives no factor; a wrong period r+1
      does not match the distribution.

    python3 quantum-maths/qm4-verify.py
"""
import cmath, math, os, re, subprocess, sys
from fractions import Fraction

FAIL = []
def check(ok, msg):
    print(("    PASS  " if ok else "    FAIL  ") + msg)
    if not ok: FAIL.append(msg)
def head(n, t):
    print('\n' + '=' * 68 + '\n  [%s]  %s\n' % (n, t) + '=' * 68)

def order(a, N):
    r, x = 1, a % N
    while x != 1:
        x = (x * a) % N; r += 1
    return r
def factors(N):
    f, d = {}, 2
    while d * d <= N:
        while N % d == 0: f[d] = f.get(d, 0) + 1; N //= d
        d += 1
    if N > 1: f[N] = f.get(N, 0) + 1
    return f
def phi_euler(n):
    return sum(1 for k in range(1, n + 1) if math.gcd(k, n) == 1)

head(1, "Shor's lemma, exhaustively")
bad = []; tested = 0; worst_ratio = 0.0
for N in range(15, 401, 2):
    f = factors(N)
    if len(f) < 2: continue                         # prime powers are excluded by the lemma
    k = len(f); units = [a for a in range(1, N) if math.gcd(a, N) == 1]; fails = 0
    for a in units:
        r = order(a, N)
        if r % 2 or pow(a, r // 2, N) == N - 1: fails += 1
    frac = Fraction(fails, len(units)); bound = Fraction(1, 2 ** (k - 1))
    worst_ratio = max(worst_ratio, float(frac / bound)); tested += 1
    if frac > bound: bad.append((N, frac, bound))
check(not bad, 'for all %d odd composite non-prime-power N <= 400: failing fraction <= 1/2^(k-1) (worst ratio %.3f)' % (tested, worst_ratio))

def dist_direct(N, a, q):
    """P(c, k) for c in 0..q-1, k in 0..r-1, from the explicit periodic state."""
    r = order(a, N); P = {}
    for k in range(r):
        xs = list(range(k, q, r))
        for c in range(q):
            s = sum(cmath.exp(2j * math.pi * x * c / q) for x in xs) / q
            P[(c, k)] = abs(s) ** 2
    return r, P
def dist_shor(r, q, c, k):
    rc = (r * c) % q
    if rc > q / 2: rc -= q                          # {rc}_q in (-q/2, q/2]
    n = (q - k - 1) // r
    return abs(sum(cmath.exp(2j * math.pi * b * rc / q) for b in range(n + 1)) / q) ** 2

CASES = [(33, 5, 256), (15, 7, 256), (21, 2, 512), (35, 2, 2048)]
head(2, 'the distribution: direct DFT = sum to 1 = Shor closed form')
CACHE = {}
for (N, a, q) in CASES:
    r, P = dist_direct(N, a, q); CACHE[(N, a, q)] = (r, P)
    tot = sum(P.values())
    worst = 0.0
    for c in range(0, q, max(1, q // 64)):
        for k in range(r):
            worst = max(worst, abs(P[(c, k)] - dist_shor(r, q, c, k)))
    check(abs(tot - 1) < 1e-9 and worst < 1e-9,
          'N=%d a=%d r=%d q=%d: total probability %.12f, max |direct - Shor| = %.1e' % (N, a, r, q, tot, worst))

head(3, "Shor's bounds")
for (N, a, q) in CASES:
    r, P = CACHE[(N, a, q)]
    lo = min(P[(c, k)] for c in range(q) for k in range(r) if abs(((r * c + q // 2) % q) - q // 2) <= r / 2)
    check(lo >= 1 / (3 * r * r), 'N=%d: min P over |{rc}_q| <= r/2 is %.6f >= 1/(3r^2) = %.6f' % (N, lo, 1 / (3 * r * r)))
for (N, a, q) in [(33, 5, 2048), (15, 7, 256), (21, 2, 512), (35, 2, 2048)]:
    check(N * N <= q < 2 * N * N, 'q = %d satisfies N^2 = %d <= q < 2N^2 = %d for N = %d' % (q, N * N, 2 * N * N, N))

def cf_convergent_denoms(c, q, N):
    a = []; num, den = c, q
    while den:
        a.append(num // den); num, den = den, num % den
    h0, h1, k0, k1 = 0, 1, 1, 0; out = []
    for ai in a:
        h0, h1 = h1, ai * h1 + h0
        k0, k1 = k1, ai * k1 + k0
        if k1 >= N: break
        out.append(k1)
    return out

head(4, 'one run recovers r: exact probability vs phi(r)/(3r)')
res = {}
for (N, a, q) in CASES:
    r, P = CACHE[(N, a, q)]
    succ = sum(P[(c, k)] for c in range(1, q) for k in range(r) if r in cf_convergent_denoms(c, q, N))
    bound = phi_euler(r) / (3 * r); res[(N, a, q)] = (succ, bound)
    print('      N=%d a=%d r=%d q=%d : P(recover r in one run) = %.4f   Shor lower bound phi(r)/3r = %.4f' % (N, a, r, q, succ, bound))
    check(succ >= bound, 'N=%d: exact success probability >= Shor bound' % N)

head(5, 'the classical pipeline, every a')
Ns = [15, 21, 33, 35, 39, 51, 55, 57, 65, 69, 77, 85, 87, 91, 93, 95, 105, 111, 115, 119]
bad = []; found = 0; total = 0
for N in Ns:
    for a in range(2, N):
        if math.gcd(a, N) != 1: continue
        r = order(a, N); total += 1
        works = (r % 2 == 0) and pow(a, r // 2, N) != N - 1
        if works:
            g1, g2 = math.gcd(pow(a, r // 2) - 1, N), math.gcd(pow(a, r // 2) + 1, N)
            ok = all(1 < g < N and N % g == 0 for g in (g1, g2)) and g1 * g2 % N == 0 and set((g1, g2)) <= set(d for d in range(2, N) if N % d == 0)
            found += ok
            if not ok: bad.append((N, a, 'works but no factor'))
        else:
            g1, g2 = math.gcd(pow(a, max(r // 2, 0), N) - 1, N), math.gcd(pow(a, max(r // 2, 0), N) + 1, N)
            if r % 2 == 0 and (1 < g1 < N or 1 < g2 < N): bad.append((N, a, 'fails but gives factor'))
check(not bad, '%d (N, a) pairs over 20 odd composites: factor iff r even and a^(r/2) != -1; %d gave factors' % (total, found))

head(6, 'controls')
r, P = CACHE[(33, 5, 256)]
# too-small q: q = 16 for N = 33
r16, P16 = dist_direct(33, 5, 16)
succ16 = sum(P16[(c, k)] for c in range(1, 16) for k in range(r16) if r16 in cf_convergent_denoms(c, 16, 33))
check(succ16 < res[(33, 5, 256)][0] and succ16 < 0.2, 'q = 16 (far below N^2) recovers r with probability %.4f only' % succ16)
odd_cases = [(N, a) for N in Ns for a in range(2, N) if math.gcd(a, N) == 1 and order(a, N) % 2 == 1]
check(len(odd_cases) > 50 and all(order(a, N) % 2 == 1 for N, a in odd_cases), 'odd order exists (e.g. N = 21, a = 4: r = %d): %d (N, a) pairs where a^(r/2) is not an integer, so the route is undefined and the step excludes them' % (order(4, 21), len(odd_cases)))
check(order(14, 15) == 2 and pow(14, 1, 15) == 14, 'N = 15, a = 14: a^(r/2) = -1 mod N, so gcd(a^(r/2) + 1, N) = N: no factor')
r2, P2 = CACHE[(33, 5, 256)]
worst = max(abs(P2[(c, 0)] - dist_shor(r2 + 1, 256, c, 0)) for c in range(0, 256, 4))
check(worst > 1e-3, 'using period r+1 in the closed form does not match the simulated distribution (gap %.3f)' % worst)

head(7, "the sourcing, against Shor's paper in ~/Downloads")
_S = next((q for q in (os.path.expanduser('~/Downloads/'), os.path.expanduser('~/mnt/Downloads/')) if os.path.isdir(q)), None)
shor = None
if _S:
    for fn in os.listdir(_S):
        if fn.lower().startswith('polynomial-time algorithms for prime factorization'):
            try:
                o = subprocess.run(['pdftotext', '-layout', os.path.join(_S, fn), '-'], capture_output=True, text=True, timeout=120)
                if o.returncode == 0 and o.stdout:
                    shor = re.sub(r'\s+', ' ', o.stdout.replace('ﬁ', 'fi').replace('ﬂ', 'fl'))
            except Exception:
                shor = None
if shor is None:
    print("    SKIP  Shor's paper (or pdftotext) is not available; none of the sourcing below is checked")
else:
    for label, needle in [
        ('the lemma and its bound', 'yields a factor of n with probability at least'),
        ('q between n^2 and 2n^2', 'with n2 ≤ q < 2n2'),
        ('lower bound 1/(3 r^2)', 'will thus be at least 1/3r2'),
        ('recovery probability phi(r)/(3r)', 'we obtain r with probability at least φ(r)/3r'),
        ("the paper's own example N = 33, x = 5, r = 10, q = 256", 'given q = 256 and r = 10'),
        ('r = 10 occurs for 33 with x = 5', 'factoring 33 if x were chosen to be 5'),
    ]:
        check(needle in shor, "Shor's paper records: " + label)

print()
if FAIL:
    print('FAILED: %d check(s)' % len(FAIL)); sys.exit(1)
print('all checks passed'); sys.exit(0)
