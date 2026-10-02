#!/usr/bin/env python3
"""ch-the-provers-verify.py — what the provers' machinery outputs, at a size
a reader can compute.

Verification companion to ch-the-provers.html. Standard library only.

The three proofs on the chapter's slate (L. Lafforgue, GL(n) over function
fields; Ngo, the fundamental lemma; Gaitsgory-Raskin et al., geometric
Langlands) are not reproducible here. What is reproducible is the smallest
object they all feed on: a rank-2 object over finite fields whose Frobenius
traces have a proved size. Kloosterman sums

    Kl(a; p) = sum_{x in F_p^*}  exp(2 pi i (x + a/x) / p)

are the traces of Frobenius on the rank-2 Kloosterman sheaf on G_m (Deligne,
Katz). Deligne's theorem (Weil II) gives |Kl| <= 2 sqrt(p): the
Ramanujan-Petersson-type bound that the function-field GL(n) correspondence
also delivers. Every statement below is EXHAUSTIVE over a in F_p^*, for every
prime listed.

  [1] Kl(a; p) is real and |Kl| <= 2 sqrt(p), all a, all primes 3..127.
  [2] Second moment: sum_a Kl(a;p)^2 = p^2 - p - 1, exact (to 1e-6).
  [3] Fourth moment of Kl/sqrt(p) approaches 2 (the SU(2) / Sato-Tate value),
      by averaging over a — an approach, not a proof; the error is printed.
  [4] The Hitchin base for SL_2 on a genus-g curve: h^0(K^2) = 3g-3 by
      Riemann-Roch, so the Hitchin space has dimension 2(3g-3) = 6g-6 =
      2 dim Bun_SL2. (Integers, g = 2..12.)
  [5] Controls — each must FAIL: a bound of sqrt(p) is violated; a wrong
      second-moment value does not match; the sum with x + a*x in place of
      x + a/x breaks the bound (it shares the second moment, so the moment
      cannot distinguish it).

    python3 book7/ch-the-provers-verify.py
"""
import math, sys

FAIL = []
def check(cond, msg):
    print(("    PASS  " if cond else "    FAIL  ") + msg)
    if not cond: FAIL.append(msg)
def head(n, t):
    print('\n' + '=' * 68 + '\n  [%s]  %s\n' % (n, t) + '=' * 68)

def primes_between(lo, hi):
    return [n for n in range(lo, hi + 1)
            if n > 1 and all(n % d for d in range(2, int(n ** 0.5) + 1))]

def kl_all(p, wrong=False):
    """Kl(a;p) for every a in 1..p-1; returns list of (real, imag)."""
    inv = [0] * p
    for x in range(1, p):
        inv[x] = pow(x, p - 2, p)
    cs = [math.cos(2 * math.pi * k / p) for k in range(p)]
    sn = [math.sin(2 * math.pi * k / p) for k in range(p)]
    out = []
    for a in range(1, p):
        re = im = 0.0
        for x in range(1, p):
            k = (x + (a * x if wrong else a * inv[x])) % p
            re += cs[k]; im += sn[k]
        out.append((re, im))
    return out

PS = primes_between(3, 127)

head(1, 'Deligne: Kl is real and |Kl| <= 2 sqrt(p)')
worst = 0.0; worst_imag = 0.0; viol = []
data = {}
for p in PS:
    d = kl_all(p); data[p] = d
    for (re, im) in d:
        worst_imag = max(worst_imag, abs(im))
        if abs(re) > 2 * math.sqrt(p) + 1e-9: viol.append(p)
        worst = max(worst, abs(re) / math.sqrt(p))
check(worst_imag < 1e-9, 'imaginary part is zero (largest %.1e), all %d primes' % (worst_imag, len(PS)))
check(not viol, '|Kl| <= 2 sqrt(p) for every a and every prime in %d..%d' % (PS[0], PS[-1]))
print('    largest |Kl|/sqrt(p) seen: %.6f   (bound 2)' % worst)

head(2, 'second moment: sum_a Kl^2 = p^2 - p - 1')
bad = [p for p in PS if abs(sum(re * re for re, _ in data[p]) - (p * p - p - 1)) > 1e-6]
check(not bad, 'identity holds for all %d primes' % len(PS))

head(3, 'fourth moment of Kl/sqrt(p) tends to 2 (the SU(2) value)')
for p in (31, 61, 101, 127):
    m4 = sum((re / math.sqrt(p)) ** 4 for re, _ in data[p]) / (p - 1)
    print('    p = %3d :  mean (Kl/sqrt p)^4 = %.4f' % (p, m4))
m4_big = sum((re / math.sqrt(127)) ** 4 for re, _ in data[127]) / 126
check(abs(m4_big - 2) < 0.25, 'p=127: fourth moment within 0.25 of 2 (observed %.4f)' % m4_big)

head(4, 'Hitchin base for SL_2: h^0(K^2) = 3g-3, so dim = 6g-6 = 2 dim Bun')
for g in range(2, 13):
    h0 = 2 * (2 * g - 2) - g + 1          # Riemann-Roch, deg K^2 = 4g-4 > 2g-2
    dimBun = 3 * g - 3                     # (g-1) dim SL_2
    ok = (h0 == 3 * g - 3) and (2 * h0 == 6 * g - 6) and (2 * dimBun == 2 * h0)
    if not ok: FAIL.append('hitchin g=%d' % g)
check(not any(f.startswith('hitchin') for f in FAIL), 'g = 2..12: base 3g-3, total 6g-6 = 2 dim Bun_SL2')

head(5, 'controls: each must fail')
p = 127
check(any(abs(re) > math.sqrt(p) for re, _ in data[p]), 'a bound of sqrt(p) is violated (bound is not loose by accident)')
check(abs(sum(re * re for re, _ in data[p]) - (p * p - p)) > 0.5, 'p^2-p does not match the second moment')
wr = kl_all(p, wrong=True)
# NB: the second moment of the no-inverse sum is ALSO p^2-p-1 (a = -1 gives
# p-1, every other a gives -1), so that identity cannot tell the two apart.
# The bound can: the no-inverse sum reaches p-1 at a = -1.
check(max(abs(re) for re, _ in wr) > 2 * math.sqrt(p), "the no-inverse sum x + a*x breaks |S| <= 2 sqrt(p)")

print()
if FAIL:
    print('FAILED: %d check(s)' % len(FAIL)); sys.exit(1)
print('all checks passed'); sys.exit(0)
