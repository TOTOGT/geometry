#!/usr/bin/env python3
"""ch-grover-verify.py — Deutsch, Deutsch-Jozsa, Bernstein-Vazirani and Grover,
simulated exactly, against their formulas.

Verification companion to ch-grover.html. Standard library only (math).

A Grover iteration on N = 2^n basis states with M marked is: flip the sign of
the marked amplitudes (the oracle), then reflect every amplitude about the mean
(diffusion, 2|s><s| - I). This script runs that on an explicit amplitude vector
— the real object, no closed form — and compares the result with the formula
    P(k) = sin^2( (2k+1) theta ),   theta = arcsin( sqrt(M/N) ).

  [1] Simulation = formula, to 1e-12, over n = 2..11, M = 1, 2, 3, every k up
      to a full period.
  [2] Unitarity: the amplitude vector keeps norm 1 at every step.
  [3] Optimal k = floor(pi / (4 theta)): for M = 1, N = 4 the success
      probability is exactly 1 after ONE iteration; in general P >= 1 - 1/N.
  [4] Scaling: optimal k grows like sqrt(N): log2(k_opt)/n -> 1/2.
  [5] Overshoot: running past the optimum LOWERS the success probability
      (twice the optimal k almost never finds the item).
  [6] Controls — each must FAIL: the oracle without the sign flip, diffusion
      without the reflection, and the wrong formula sin^2(k theta).

  [7] Bernstein-Vazirani: for f(x) = s.x mod 2, Hadamard - phase oracle -
      Hadamard returns |s> with probability 1 after ONE query. Every s for
      n = 1..8 (all 2^n of them, exhaustively), against an explicit
      Walsh-Hadamard transform of the amplitude vector.
  [8] The classical side: any q < n queries leave at least two consistent
      strings s, because the answers are linear in s (exhaustive over every
      query set for n = 2..5); so n queries are necessary, and n suffice.
  [9] Controls for 7-8: an oracle for a NON-linear f does not return a single
      basis state; and a query set of size n that spans leaves exactly one s.

  [10] Deutsch (n = 1): all four functions {0,1} -> {0,1}; one query tells
       constant from balanced, with certainty.
  [11] Deutsch-Jozsa: for every constant function and EVERY balanced function
       (n = 1..4; 2 + C(2^n, 2^(n-1)) functions) the probability of measuring
       0...0 is exactly 1 (constant) or exactly 0 (balanced), after one query.
  [12] The classical side. Deterministic and exact: 2^(n-1) queries cannot
       decide and 2^(n-1)+1 always can — tested against every promise
       function as an explicit truth table, every query set, n = 2, 3.
       Randomised with bounded error: k random queries err with probability
       2^(1-k) at most — computed exactly. The exponential gap is against
       the exact deterministic classical algorithm ONLY.
  [13] Controls: a function that breaks the promise gives a probability
       strictly between 0 and 1; dropping the final Hadamards destroys it.

What it does not show: the lower bound. That no quantum algorithm can do
better than order sqrt(N) queries is a theorem (Bennett-Bernstein-Brassard-
Vazirani 1997; exact constant by Zalka 1999). It is cited, not checked.

    python3 book7/ch-grover-verify.py
"""
import math, sys

FAIL = []
def check(ok, msg):
    print(("    PASS  " if ok else "    FAIL  ") + msg)
    if not ok: FAIL.append(msg)
def head(n, t):
    print('\n' + '=' * 68 + '\n  [%s]  %s\n' % (n, t) + '=' * 68)

def grover_probs(n, M, steps, oracle_flip=True, diffuse=True):
    """Return (probabilities of 'marked' after each k = 0..steps, max norm error)."""
    N = 2 ** n
    amp = [1 / math.sqrt(N)] * N
    marked = set(range(M))                 # which items are marked is arbitrary
    out = []; nerr = 0.0
    for k in range(steps + 1):
        out.append(sum(amp[i] ** 2 for i in marked))
        nerr = max(nerr, abs(sum(a * a for a in amp) - 1))
        if oracle_flip:
            for i in marked: amp[i] = -amp[i]
        if diffuse:
            mean = sum(amp) / N
            amp = [2 * mean - a for a in amp]
    return out, nerr

def theory(n, M, k):
    th = math.asin(math.sqrt(M / 2 ** n))
    return math.sin((2 * k + 1) * th) ** 2

head(1, 'simulation = sin^2((2k+1) theta)')
worst = 0.0; cases = 0
for n in range(2, 12):
    for M in (1, 2, 3):
        if M >= 2 ** n // 2: continue
        th = math.asin(math.sqrt(M / 2 ** n))
        steps = int(math.pi / (2 * th)) + 2        # a full period of P(k)
        sim, _ = grover_probs(n, M, steps)
        for k, p in enumerate(sim):
            worst = max(worst, abs(p - theory(n, M, k))); cases += 1
check(worst < 1e-12, '%d (n, M, k) cases; largest |simulation - formula| = %.2e' % (cases, worst))

head(2, 'unitarity: norm stays 1')
nerrs = [grover_probs(n, 1, 60)[1] for n in (3, 6, 9)]
check(max(nerrs) < 1e-12, 'norm error over 60 iterations, n = 3, 6, 9: %.2e' % max(nerrs))

head(3, 'optimal k; N = 4 is exact after one iteration')
p4, _ = grover_probs(2, 1, 1)
check(abs(p4[1] - 1) < 1e-12, 'N = 4, one marked: P(1) = %.15f' % p4[1])
bad = []
for n in range(2, 12):
    th = math.asin(math.sqrt(1 / 2 ** n))
    k = int(math.pi / (4 * th))
    sim, _ = grover_probs(n, 1, k)
    if sim[k] < 1 - 1 / 2 ** n - 1e-12: bad.append((n, sim[k]))
check(not bad, 'at k = floor(pi/(4 theta)), P >= 1 - 1/N for n = 2..11 (M = 1)')

head(4, 'scaling: k_opt ~ sqrt(N)')
ratios = []
for n in (4, 8, 12, 16, 20, 24):
    th = math.asin(math.sqrt(1 / 2 ** n)); k = int(math.pi / (4 * th))
    ratios.append((n, k, math.log2(k) / n))
    print('    n = %2d  N = 2^%-2d  k_opt = %6d   log2(k)/n = %.3f   classical mean (N+1)/2 = %d'
          % (n, n, k, math.log2(k) / n, (2 ** n + 1) // 2))
check(abs(ratios[-1][2] - 0.5) < 0.05, 'log2(k_opt)/n -> 1/2 (observed %.3f at n = 24)' % ratios[-1][2])

head(5, 'overshoot')
n = 10; th = math.asin(math.sqrt(1 / 2 ** n)); kopt = int(math.pi / (4 * th))
sim, _ = grover_probs(n, 1, 2 * kopt)
print('    n = 10: P(k_opt = %d) = %.4f,  P(2 k_opt) = %.4f' % (kopt, sim[kopt], sim[2 * kopt]))
check(sim[2 * kopt] < 0.01 and sim[kopt] > 0.99, 'twice the optimum finds the item with probability < 1%')

head(6, 'controls: each must fail')
sim_ok, _ = grover_probs(6, 1, 8)
no_flip, _ = grover_probs(6, 1, 8, oracle_flip=False)
no_diff, _ = grover_probs(6, 1, 8, diffuse=False)
check(max(abs(a - theory(6, 1, k)) for k, a in enumerate(no_flip)) > 0.01, 'without the oracle sign flip, the formula fails')
check(max(abs(a - theory(6, 1, k)) for k, a in enumerate(no_diff)) > 0.01, 'without the diffusion reflection, the formula fails')
th6 = math.asin(math.sqrt(1 / 64))
check(max(abs(a - math.sin(k * th6) ** 2) for k, a in enumerate(sim_ok)) > 0.01, 'the wrong formula sin^2(k theta) does not match')

def wht(v):
    v = v[:]; h = 1
    while h < len(v):
        for i in range(0, len(v), 2 * h):
            for j in range(i, i + h):
                a, b = v[j], v[j + h]; v[j], v[j + h] = a + b, a - b
        h *= 2
    return v

def bv_probs(n, f):
    N = 2 ** n
    amp = [1 / math.sqrt(N)] * N                 # after the first Hadamard layer
    amp = [a * (-1) ** f(x) for x, a in enumerate(amp)]   # ONE phase-oracle query
    amp = [a / math.sqrt(N) for a in wht(amp)]   # second Hadamard layer
    return [a * a for a in amp]

dot = lambda s, x: bin(s & x).count('1') & 1

head(7, 'Bernstein-Vazirani: one query returns the hidden string')
worst = 1.0; total = 0
for n in range(1, 9):
    for sec in range(2 ** n):
        pr = bv_probs(n, lambda x, sec=sec: dot(sec, x))
        worst = min(worst, pr[sec]); total += 1
check(worst > 1 - 1e-12, 'all %d secrets, n = 1..8: P(measure s) >= %.15f' % (total, worst))

head(8, 'classical: fewer than n queries cannot determine s')
import itertools
def consistent(n, queries, sec):
    return [t for t in range(2 ** n) if all(dot(t, x) == dot(sec, x) for x in queries)]
ok = True; sets = 0
for n in range(2, 6):
    for q in range(1, n):
        for qs in itertools.combinations(range(1, 2 ** n), q):
            sets += 1
            if len(consistent(n, qs, 0)) < 2: ok = False
check(ok, 'every set of q < n queries leaves >= 2 consistent strings (%d query sets, n = 2..5)' % sets)
check(len(consistent(4, (1, 2, 4, 8), 0b1011)) == 1, 'the n unit-vector queries determine s uniquely (n = 4)')

head(9, 'controls for 7-8')
pr = bv_probs(4, lambda x: (x & 1) & ((x >> 1) & 1))      # AND of two bits: not linear
check(max(pr) < 0.99, 'a non-linear f does not return a single basis state (max P = %.3f)' % max(pr))
check(len(consistent(4, (1, 2, 3), 0b1011)) >= 2, 'a dependent query set (1, 2, 3) of size n-1 leaves ambiguity')

head(10, 'Deutsch, n = 1')
ok = True
for f0 in (0, 1):
    for f1 in (0, 1):
        pr = bv_probs(1, lambda x, a=f0, b=f1: (a, b)[x])
        want0 = 1.0 if f0 == f1 else 0.0          # P(measure 0): 1 iff constant
        ok &= abs(pr[0] - want0) < 1e-12
check(ok, 'all 4 functions: P(0) = 1 if f(0) = f(1), else 0, after one query')

head(11, 'Deutsch-Jozsa: every constant and every balanced function, n = 1..4')
from math import comb
counts = {}
for n in range(1, 5):
    N = 2 ** n; bal = 0; cst = 0; worst = 0.0
    for f0 in (0, 1):                               # constants
        pr = bv_probs(n, lambda x, c=f0: c); worst = max(worst, abs(pr[0] - 1)); cst += 1
    for ones in itertools.combinations(range(N), N // 2):     # balanced
        S = set(ones)
        pr = bv_probs(n, lambda x, S=S: 1 if x in S else 0)
        worst = max(worst, abs(pr[0])); bal += 1
    counts[n] = (cst, bal, worst)
    print('    n = %d : %d constant + %d balanced functions (C(%d,%d) = %d); worst deviation %.1e'
          % (n, cst, bal, N, N // 2, comb(N, N // 2), worst))
check(all(w < 1e-12 for _, _, w in counts.values()) and all(b == comb(2 ** n, 2 ** n // 2) for n, (_, b, _) in counts.items()),
      'P(0...0) is exactly 1 for constant, exactly 0 for balanced -- no exceptions, every function enumerated')

head(12, 'classical deterministic and randomised')
# Enumerate every function satisfying the promise (as truth tables) and test
# the adversary argument against them, not against a construction of mine.
ok_half = True; ok_plus = True; sets_half = 0; sets_plus = 0
for n in (2, 3):
    N = 2 ** n
    promise = [tuple([c] * N) for c in (0, 1)]
    for ones in itertools.combinations(range(N), N // 2):
        promise.append(tuple(1 if x in ones else 0 for x in range(N)))
    for Q in itertools.combinations(range(N), N // 2):          # 2^(n-1) queries
        sets_half += 1
        # some answer vector must be consistent with BOTH a constant and a balanced f
        ans_c = {tuple(f[x] for x in Q) for f in promise if len(set(f)) == 1}
        ans_b = {tuple(f[x] for x in Q) for f in promise if len(set(f)) == 2}
        if not (ans_c & ans_b): ok_half = False
    for Q in itertools.combinations(range(N), N // 2 + 1):      # 2^(n-1)+1 queries
        sets_plus += 1
        ans_c = {tuple(f[x] for x in Q) for f in promise if len(set(f)) == 1}
        ans_b = {tuple(f[x] for x in Q) for f in promise if len(set(f)) == 2}
        if ans_c & ans_b: ok_plus = False
check(ok_half, '2^(n-1) queries cannot decide: an ambiguous answer vector exists for all %d query sets, n = 2, 3' % sets_half)
check(ok_plus, '2^(n-1)+1 queries always decide: no answer vector is shared, all %d query sets, n = 2, 3' % sets_plus)
from fractions import Fraction as Fr
err_ok = True
for n in (3, 5, 8):
    N = 2 ** n
    for k in range(2, 7):
        # balanced f, k distinct random points all equal: 2 * C(N/2,k) / C(N,k)
        pe = Fr(2 * comb(N // 2, k), comb(N, k))
        if pe > Fr(1, 2 ** (k - 1)): err_ok = False
check(err_ok, 'k random queries err with probability <= 2^(1-k): exact, n = 3, 5, 8, k = 2..6')
print('    n = 8, k = 5: error = %s (= %.4f)' % (Fr(2 * comb(128, 5), comb(256, 5)), float(Fr(2 * comb(128, 5), comb(256, 5)))))

head(13, 'controls for 10-12')
pr = bv_probs(2, lambda x: 1 if x == 0 else 0)             # one 1 of four: breaks the promise
check(0.01 < pr[0] < 0.99, 'a function outside the promise: P(0..0) = %.4f, strictly between 0 and 1' % pr[0])
N4 = 4; amp = [1 / math.sqrt(N4)] * N4
amp = [a * (-1) ** (1 if x in (0, 1) else 0) for x, a in enumerate(amp)]   # balanced, no final Hadamards
check(abs(amp[0] ** 2 - 1) > 0.01 and abs(amp[0] ** 2) > 0.01, 'without the final Hadamards a balanced function does not read out as 0')

print()
if FAIL:
    print('FAILED: %d check(s)' % len(FAIL)); sys.exit(1)
print('all checks passed'); sys.exit(0)
