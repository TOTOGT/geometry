#!/usr/bin/env python3
"""
Mandelbrot -- verifier for book7/ch-mandelbrot.html.

CHECKS:
  1. For a distribution p over ranks 1..N with p_r proportional to exp(-alpha c_r), c_r = ln(r + beta)
     (the Zipf-Mandelbrot form (r+beta)^(-alpha)), and ANY other distribution p' over the same ranks with the
     same mean cost, the entropy gap H(p) - H(p') equals the Kullback-Leibler divergence KL(p' || p) >= 0.
     This is the whole proof that p is the entropy maximizer at fixed mean cost; the identity is checked to 1e-12
     on 200 seeded perturbations that keep total probability and mean cost fixed, and every gap is positive.
  2. In the random-typing model of ch-zipf (k letters), the word of rank r has length L with
     log_k(1 + r(k-1)/k) <= L < log_k(1 + r(k-1)/k) + 1, so its cost in characters is log_k r up to one
     character. Checked for every r up to 300,000 with k = 26.
  3. The page's figures (entropy, mean cost) equal the computed values.

DOES NOT ESTABLISH: that real word costs are logarithmic in rank, that speakers minimize cost per unit of
information, or that natural-language vocabularies follow (r+beta)^(-alpha). The 1953 derivation is described
on the page as cited; it was not re-read. beta = 2.7 and alpha = 1.1 are arbitrary illustrative values.

    python3 book7/ch-mandelbrot-verify.py
"""
import math, os, random, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
fails = []
def check(ok, msg):
    print('    %s  %s' % ('PASS' if ok else 'FAIL', msg))
    if not ok: fails.append(msg)
def head(n, t): print('\n' + '=' * 70 + '\n  [%s]  %s\n' % (n, t) + '=' * 70)

N, ALPHA, BETA = 1000, 1.1, 2.7
c = [math.log(r + BETA) for r in range(1, N + 1)]
w = [math.exp(-ALPHA * x) for x in c]; Z = sum(w); p = [x / Z for x in w]
H = lambda q: -sum(x * math.log(x) for x in q if x > 0)
E = lambda q: sum(x * y for x, y in zip(q, c))
Hp, Ep = H(p), E(p)

head(1, 'ENTROPY GAP EQUALS KL DIVERGENCE FOR EQUAL-MEAN-COST COMPETITORS')
print('    N=%d alpha=%.1f beta=%.1f  H(p)=%.4f nats  mean cost E(p)=%.4f nats' % (N, ALPHA, BETA, Hp, Ep))
rng = random.Random(20261117)
worst_id = 0.0; min_gap = 1e9; ok_all = True
for _ in range(200):
    d = [rng.uniform(-1, 1) for _ in range(N)]
    # remove components along the constraints: sum d = 0 and sum c d = 0 (Gram-Schmidt on [1, c])
    n1 = math.sqrt(N); u1 = [1 / n1] * N
    cc = [x - sum(a * b for a, b in zip(c, u1)) * u for x, u in zip(c, u1)]
    nc = math.sqrt(sum(x * x for x in cc)); u2 = [x / nc for x in cc]
    for u in (u1, u2):
        dot = sum(a * b for a, b in zip(d, u)); d = [a - dot * b for a, b in zip(d, u)]
    m = min(p[i] / abs(d[i]) for i in range(N) if d[i] != 0)
    eps = 0.9 * m * rng.random()
    q = [p[i] + eps * d[i] for i in range(N)]
    assert abs(sum(q) - 1) < 1e-12 and abs(E(q) - Ep) < 1e-10
    gap = Hp - H(q); kl = sum(x * math.log(x / y) for x, y in zip(q, p) if x > 0)
    worst_id = max(worst_id, abs(gap - kl)); min_gap = min(min_gap, gap)
check(worst_id < 1e-12, 'entropy gap equals KL(p\' || p) to %.1e on 200 perturbations' % worst_id)
check(min_gap > 0, 'every perturbed distribution has strictly lower entropy (smallest gap %.2e)' % min_gap)

head(2, 'RANK-r WORD LENGTH IS LOG_K(r) UP TO ONE CHARACTER (RANDOM TYPING)')
K = 26
def length_of_rank(r):
    L, tot = 0, 0
    while tot < r:
        L += 1; tot += K ** L
    return L
bad = 0
for r in range(1, 300001):
    L = length_of_rank(r); lo = math.log(1 + r * (K - 1) / K, K)
    if not (lo - 1e-12 <= L < lo + 1): bad += 1
check(bad == 0, 'for all r <= 300,000: log_26(1 + 25r/26) <= length < that + 1')

head(3, "THE PAGE'S FIGURES")
html = open(os.path.join(HERE, 'ch-mandelbrot.html'), encoding='utf-8').read()
m = re.search(r'data-H="([0-9.]+)" data-E="([0-9.]+)"', html)
check(bool(m) and m.group(1) == '%.4f' % Hp and m.group(2) == '%.4f' % Ep, 'page states H = %.4f and mean cost = %.4f' % (Hp, Ep))
for lab in ('CITED RESULT', 'CHECKED INSTANCE', 'OPEN QUESTION', 'THEOREM'):
    check(('<b>%s</b>' % lab) in html, 'visible evidence label %s present' % lab)
check('ch-mandelbrot-verify.py' in html, 'page names this verifier')
check('were not checked for this page' in html, 'page states which items were not checked')
check('href="ch-zipf.html"' in html, 'link to ch-zipf')
print('\n' + '=' * 70)
if fails:
    print('  %d CHECK(S) FAILED:' % len(fails)); [print('    - ' + f) for f in fails]; sys.exit(1)
print('  ALL CHECKS PASSED')
