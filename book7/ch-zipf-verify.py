#!/usr/bin/env python3
"""
Zipf -- verifier for book7/ch-zipf.html.

CHECKS:
  1. The random-typing ("monkey") model: k equiprobable letters and a space of probability s. A given word of
     length L then has relative frequency proportional to q^L with q = (1-s)/k, and there are k^L words of length L.
     Ranking all words by frequency, the words of length L fill ranks N(L-1)+1 .. N(L), N(L) = k + ... + k^L.
     The slope of log-frequency against log-rank between consecutive length blocks is computed exactly (floating
     point logs of exact integers) and compared with the limit  alpha = 1 + ln(1/(1-s)) / ln k.
  2. The page's table of block slopes equals the computed values.
  3. A seeded simulation of 3,000,000 typed characters (k = 26, s = 0.2): the least-squares slope of log f against
     log rank over ranks 1..1000. The tolerance, 0.15 around alpha, was fixed before the run.
  4. Control: a uniform distribution over 1000 words has fitted slope 0 (the fit code does not manufacture a slope).

DOES NOT ESTABLISH: that any natural language follows Zipf's law (a cited empirical claim, not checked here: no
corpus is used), that Zipf's explanation (least effort) is right, or any biographical statement. Those are CITED.

    python3 book7/ch-zipf-verify.py
"""
import math, os, random, re, sys
from collections import Counter
HERE = os.path.dirname(os.path.abspath(__file__))
fails = []
def check(ok, msg):
    print('    %s  %s' % ('PASS' if ok else 'FAIL', msg))
    if not ok: fails.append(msg)
def head(n, t): print('\n' + '=' * 70 + '\n  [%s]  %s\n' % (n, t) + '=' * 70)

K, S = 26, 0.2
Q = (1 - S) / K
ALPHA = 1 + math.log(1 / (1 - S)) / math.log(K)

def N(L): return sum(K ** i for i in range(1, L + 1))
def slopes(maxL):
    out = []
    for L in range(1, maxL):
        r1 = math.sqrt((N(L - 1) + 1) * N(L)); r2 = math.sqrt((N(L) + 1) * N(L + 1))
        out.append((L, math.log(Q ** L / Q ** (L + 1)) / math.log(r2 / r1)))
    return out

def ls_slope(freqs):
    xs = [math.log(i + 1) for i in range(len(freqs))]; ys = [math.log(f) for f in freqs]
    mx = sum(xs) / len(xs); my = sum(ys) / len(ys)
    return sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sum((x - mx) ** 2 for x in xs)

head(1, 'BLOCK SLOPES OF THE RANDOM-TYPING MODEL (k=26, s=0.2)')
print('    alpha = 1 + ln(1/(1-s))/ln k = %.6f' % ALPHA)
sl = slopes(8)
for L, v in sl: print('    between length %d and %d: slope %.4f' % (L, L + 1, v))
check(abs(sl[-1][1] - ALPHA) < 0.01, 'the slope between lengths 7 and 8 is within 0.01 of alpha')
check(all(abs(sl[i + 1][1] - ALPHA) <= abs(sl[i][1] - ALPHA) + 1e-12 for i in range(len(sl) - 1)), 'the slopes approach alpha monotonically')
check(ALPHA > 1, 'alpha > 1 for every s > 0 (the model gives an exponent above 1)')

head(2, "THE PAGE'S TABLE")
html = open(os.path.join(HERE, 'ch-zipf.html'), encoding='utf-8').read()
rows = {int(a): b for a, b in re.findall(r'<tr data-L="(\d+)" data-slope="([0-9.]+)"', html)}
check(sorted(rows) == list(range(1, 8)), 'page table has rows for L = 1..7')
for L, v in sl:
    check(rows.get(L) == '%.4f' % v, 'page row L=%d equals computed slope %.4f' % (L, v))
m = re.search(r'data-alpha="([0-9.]+)"', html)
check(bool(m) and m.group(1) == '%.4f' % ALPHA, 'page states alpha = %.4f' % ALPHA)

head(3, 'SEEDED SIMULATION: 3,000,000 TYPED CHARACTERS')
rng = random.Random(20261117)
letters = 'abcdefghijklmnopqrstuvwxyz'
chars = [' ' if rng.random() < S else letters[rng.randrange(K)] for _ in range(3000000)]
words = [w for w in ''.join(chars).split(' ') if w]
cnt = Counter(words)
freqs = sorted(cnt.values(), reverse=True)[:1000]
sim = ls_slope(freqs)
print('    distinct words %d, tokens %d, least-squares slope over ranks 1..1000: %.4f (|slope| vs alpha %.4f)' % (len(cnt), len(words), -sim, ALPHA))
check(abs(-sim - ALPHA) < 0.15, 'fitted |slope| is within 0.15 of alpha (tolerance fixed before the run)')
sm = re.search(r'data-sim="([0-9.]+)"', html)
check(bool(sm) and sm.group(1) == '%.4f' % (-sim), 'page states the simulated slope %.4f' % (-sim))

head(4, 'CONTROL: UNIFORM FREQUENCIES')
check(abs(ls_slope([1.0] * 1000)) < 1e-12, 'uniform frequencies give slope 0')

for lab in ('CITED RESULT', 'CHECKED INSTANCE', 'OPEN QUESTION'):
    check(('<b>%s</b>' % lab) in html, 'visible evidence label %s present' % lab)
check('ch-zipf-verify.py' in html, 'page names this verifier')
check('were not checked for this page' in html, 'page states which items were not checked')
print('\n' + '=' * 70)
if fails:
    print('  %d CHECK(S) FAILED:' % len(fails)); [print('    - ' + f) for f in fails]; sys.exit(1)
print('  ALL CHECKS PASSED')
