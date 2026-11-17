#!/usr/bin/env python3
"""
Shannon -- verifier for book7/ch-shannon.html.

CHECKS:
  1. Source coding bound: for 200 seeded random distributions on 2..12 symbols, a Huffman code (written for this
     page) satisfies the Kraft sum = 1 and  H(p) <= average length < H(p) + 1  (bits). Control: the dyadic
     distribution (1/2, 1/4, 1/8, 1/8) has H = 1.75 = average length exactly.
  2. Binary symmetric channel with crossover probability 0.11: the mutual information I(X;Y) over input
     distributions (P(X=1) = t, grid step 1/1000) is largest at t = 1/2 and equals 1 - H2(0.11) there.
     Capacity C = 1 - H2(0.11), printed to four decimals.
  3. The page's figures equal the computed values.

DOES NOT ESTABLISH: the source-coding or channel-coding THEOREMS in general (cited: Shannon 1948), anything about
the entropy of English (no text is used here), or any biographical statement. Those are CITED and were not checked.

    python3 book7/ch-shannon-verify.py
"""
import heapq, math, os, random, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
fails = []
def check(ok, msg):
    print('    %s  %s' % ('PASS' if ok else 'FAIL', msg))
    if not ok: fails.append(msg)
def head(n, t): print('\n' + '=' * 70 + '\n  [%s]  %s\n' % (n, t) + '=' * 70)
def Hb(ps): return -sum(x * math.log2(x) for x in ps if x > 0)

def huffman_lengths(p):
    heap = [(x, i, [i]) for i, x in enumerate(p)]; heapq.heapify(heap)
    lens = [0] * len(p); cnt = len(p)
    while len(heap) > 1:
        a = heapq.heappop(heap); b = heapq.heappop(heap)
        for i in a[2] + b[2]: lens[i] += 1
        heapq.heappush(heap, (a[0] + b[0], cnt, a[2] + b[2])); cnt += 1
    return lens

head(1, 'HUFFMAN CODES MEET THE SOURCE-CODING BOUND')
rng = random.Random(20261117); worst_lo = 1e9; worst_hi = -1e9; kraft_ok = True
for _ in range(200):
    n = rng.randint(2, 12); w = [rng.random() + 1e-3 for _ in range(n)]; s = sum(w); p = [x / s for x in w]
    lens = huffman_lengths(p); L = sum(x * l for x, l in zip(p, lens)); H = Hb(p)
    if abs(sum(2.0 ** -l for l in lens) - 1) > 1e-12: kraft_ok = False
    worst_lo = min(worst_lo, L - H); worst_hi = max(worst_hi, L - H)
check(kraft_ok, 'Kraft sum equals 1 for every code')
check(worst_lo >= -1e-12, 'average length >= entropy on all 200 (smallest L - H = %.2e)' % worst_lo)
check(worst_hi < 1, 'average length < entropy + 1 on all 200 (largest L - H = %.4f)' % worst_hi)
dy = [0.5, 0.25, 0.125, 0.125]; ld = huffman_lengths(dy)
check(abs(sum(x * l for x, l in zip(dy, ld)) - 1.75) < 1e-12 and abs(Hb(dy) - 1.75) < 1e-12, 'control: dyadic source has H = 1.75 = average length')

head(2, 'BINARY SYMMETRIC CHANNEL, CROSSOVER 0.11')
e = 0.11
def I(t):
    py1 = t * (1 - e) + (1 - t) * e
    return Hb([py1, 1 - py1]) - Hb([e, 1 - e])
best = max(range(0, 1001), key=lambda i: I(i / 1000))
C = 1 - Hb([e, 1 - e])
print('    H2(0.11) = %.4f  capacity C = %.4f bits per use  argmax t = %.3f' % (Hb([e, 1 - e]), C, best / 1000))
check(best == 500, 'mutual information is largest at t = 1/2')
check(abs(I(0.5) - C) < 1e-12, 'I(X;Y) at t = 1/2 equals 1 - H2(0.11)')
check(all(I(i / 1000) <= C + 1e-12 for i in range(1001)), 'no input distribution on the grid exceeds C')

head(3, "THE PAGE'S FIGURES")
html = open(os.path.join(HERE, 'ch-shannon.html'), encoding='utf-8').read()
m = re.search(r'data-C="([0-9.]+)"', html)
check(bool(m) and m.group(1) == '%.4f' % C, 'page states C = %.4f' % C)
for lab in ('CITED RESULT', 'CHECKED INSTANCE', 'OPEN QUESTION', 'THEOREM'):
    check(('<b>%s</b>' % lab) in html, 'visible evidence label %s present' % lab)
check('ch-shannon-verify.py' in html, 'page names this verifier')
check('were not checked for this page' in html, 'page states which items were not checked')
check('href="ch-zipf.html"' in html, 'link to ch-zipf')
print('\n' + '=' * 70)
if fails:
    print('  %d CHECK(S) FAILED:' % len(fails)); [print('    - ' + f) for f in fails]; sys.exit(1)
print('  ALL CHECKS PASSED')
