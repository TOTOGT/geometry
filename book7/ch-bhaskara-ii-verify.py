#!/usr/bin/env python3
"""
Bhaskara II -- verifier for book7/ch-bhaskara-ii.html.

CHECKS (exact integer arithmetic):
  1. A chakravala (cyclic method) implementation, written for this page from the standard
     description of the method, run on N = 61, 67, 109: the final (x, y) satisfies x^2 - N y^2 = 1.
  2. The same x, y from an independent route (continued fraction of sqrt(N)), for N = 61, 67, 109,
     and for every non-square N from 2 to 299 (the cyclic method and the continued fraction agree).
  3. N = 61: no y below 2,000,000 gives N*y^2 + 1 a perfect square (a partial check of minimality; the full statement is the continued-fraction theorem, cited).
  4. All solutions are powers of the fundamental one and satisfy s_{k+1} = 2 x1 s_k - s_{k-1}.
  5. The page's table equals the computed values.

DOES NOT ESTABLISH: that the method always terminates (a theorem, cited on the page), anything about
Bhaskara II's life, dates or text, or who knew what before whom. Those are CITED and were not checked.

    python3 book7/ch-bhaskara-ii-verify.py
"""
import os, re, sys
from math import isqrt
HERE = os.path.dirname(os.path.abspath(__file__))
fails = []
def check(ok, msg):
    print('    %s  %s' % ('PASS' if ok else 'FAIL', msg))
    if not ok: fails.append(msg)
def head(n, t): print('\n' + '=' * 70 + '\n  [%s]  %s\n' % (n, t) + '=' * 70)

def cf_solution(N):
    a0 = isqrt(N); m, d, a = 0, 1, a0; h0, h1 = 1, a0; k0, k1 = 0, 1
    while h1 * h1 - N * k1 * k1 != 1:
        m = d * a - m; d = (N - m * m) // d; a = (a0 + m) // d
        h0, h1 = h1, a * h1 + h0; k0, k1 = k1, a * k1 + k0
    return h1, k1

def chakravala(N):
    """Returns (x, y, steps, last_k) with x^2 - N y^2 = 1. Steps count cyclic steps until |k| = 1."""
    a = isqrt(N)
    if abs((a + 1) ** 2 - N) < abs(a * a - N): a += 1
    b, k, steps = 1, a * a - N, 0
    while abs(k) != 1:
        ak = abs(k); m0 = isqrt(N); best = None
        for m in range(max(1, m0 - ak - 2), m0 + ak + 3):
            if (a + b * m) % ak == 0:
                v = abs(m * m - N)
                if best is None or v < best[0]: best = (v, m)
        m = best[1]
        a, b, k = (a * m + N * b) // ak, (a + b * m) // ak, (m * m - N) // k
        steps += 1
        assert steps < 10000, 'no termination for N=%d' % N
    last_k = k
    if k == -1:
        a, b = a * a + N * b * b, 2 * a * b
    return a, b, steps, last_k

head(1, 'CHAKRAVALA RESULTS FOR N = 61, 67, 109')
res = {}
for N in (61, 67, 109):
    x, y, steps, lk = chakravala(N)
    res[N] = (x, y, steps, lk)
    print('    N=%d  x=%d  y=%d  cyclic steps=%d  last k=%d' % (N, x, y, steps, lk))
    check(x * x - N * y * y == 1, 'N=%d: x^2 - %d y^2 = 1 exactly' % (N, N))

head(2, 'AN INDEPENDENT ROUTE: CONTINUED FRACTION OF SQRT(N)')
for N in (61, 67, 109):
    check(cf_solution(N) == res[N][:2], 'N=%d: continued fraction gives the same (x, y)' % N)
bad = [N for N in range(2, 300) if isqrt(N) ** 2 != N and chakravala(N)[:2] != cf_solution(N)]
count = sum(1 for N in range(2, 300) if isqrt(N) ** 2 != N)
check(not bad, 'cyclic method and continued fraction agree on all %d non-square N in 2..299' % count)
check(isqrt(60) ** 2 != 60 and chakravala(60)[:2] == cf_solution(60), 'control: N=60 also agrees')

head(3, 'NO SMALLER SOLUTION BELOW 2,000,000 FOR N = 61 (BRUTE FORCE)')
N = 61
found = [y for y in range(1, 2000000) if isqrt(N * y * y + 1) ** 2 == N * y * y + 1]
check(not found, 'no y < 2,000,000 gives 61 y^2 + 1 a perfect square (the least y is 226153980, far above)')

head(4, 'ALL SOLUTIONS ARE POWERS; THE RECURRENCE')
N = 61; x1, y1 = res[61][:2]
xs, ys = [1, x1], [0, y1]
for _ in range(3):
    xs.append(2 * x1 * xs[-1] - xs[-2]); ys.append(2 * x1 * ys[-1] - ys[-2])
for k in range(len(xs)):
    check(xs[k] * xs[k] - N * ys[k] * ys[k] == 1, 'term %d of the recurrence solves the equation' % k)
a, b = 1, 0
for k in range(1, 4):
    a, b = a * x1 + N * b * y1, a * y1 + b * x1
    check((a, b) == (xs[k], ys[k]), '(x1 + y1 sqrt 61)^%d equals recurrence term %d' % (k, k))

head(5, "THE PAGE'S TABLE")
html = open(os.path.join(HERE, 'ch-bhaskara-ii.html'), encoding='utf-8').read()
rows = {int(m[0]): m for m in re.findall(r'<tr data-n="(\d+)" data-x="(\d+)" data-y="(\d+)" data-steps="(\d+)" data-lastk="(-?\d)"', html)}
check(sorted(rows) == [61, 67, 109], 'page table has rows for 61, 67, 109')
for N in (61, 67, 109):
    r = rows[N]
    check((int(r[1]), int(r[2]), int(r[3]), int(r[4])) == res[N], 'page row N=%d equals computed values' % N)
for lab in ('CITED RESULT', 'CHECKED INSTANCE', 'OPEN QUESTION'):
    check(('<b>%s</b>' % lab) in html, 'visible evidence label %s present' % lab)
check('ch-bhaskara-ii-verify.py' in html, 'page names this verifier')
check('were not checked for this page' in html, 'page states which items were not checked')
check('href="ch-euler.html"' in html, 'link to ch-euler')
print('\n' + '=' * 70)
if fails:
    print('  %d CHECK(S) FAILED:' % len(fails)); [print('    - ' + f) for f in fails]; sys.exit(1)
print('  ALL CHECKS PASSED')
