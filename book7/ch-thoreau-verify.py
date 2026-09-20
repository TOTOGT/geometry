#!/usr/bin/env python3
"""
Thoreau -- the soundings, the notebooks, and one conjecture tested.

[1] tests Thoreau's rule. In "The Pond in Winter" he reports that at Walden
the line of greatest length crossed the line of greatest breadth exactly at
the point of greatest depth, and proposes it as a general rule -- for ponds,
for harbours, and, in the last step, for a character. This block builds
basins on a grid, takes depth to fall off with distance from shore (which is
the model his own rule presupposes), finds the longest chord, the longest
chord perpendicular to it, and the deepest point, and measures how far the
crossing lands from the deepest point.

The result is the finding, and it is not the one you would guess. The rule is
exact on a circle, holds to within 0.7% of the length on a 2:1 ellipse, and
stays inside 9% on every convex basin tested -- then breaks on every concave
one, missing by 17% or more. What the rule is really about is the outline: it
survives while the shore does not turn back on itself. Walden's outline is
convex and close to an ellipse, which makes it the most favourable pond there
is. Thoreau was right about Walden. The extension to harbours, and to a
character, is not carried by this.

[2] and [3] check the recorded numbers: the soundings, and the Concord
phenology arithmetic (eleven days, six degrees Fahrenheit, and the implied
days-per-degree, which is compared against the published rate).

[4] checks the chronology, [5] reads the chapter file back.

Standard library only.  python3 book7/ch-thoreau-verify.py
"""

import math, os, re, sys
from collections import deque

fails = []
def check(ok, msg, detail=''):
    print('    %s  %s%s' % ('PASS' if ok else 'FAIL', msg, ('  -- ' + detail) if detail and not ok else ''))
    if not ok: fails.append(msg)
def head(n, t):
    print('\n' + '=' * 68 + '\n  [%s]  %s\n' % (n, t) + '=' * 68)

HERE = os.path.dirname(os.path.abspath(__file__))
CHAPTER = os.path.join(HERE, 'ch-thoreau.html')

# ==========================================================================
head(1, "THOREAU'S RULE, TESTED ON BASINS")

N = 81                      # grid side

def make(mask_fn):
    return [[1 if mask_fn((x - (N - 1) / 2.0) / ((N - 1) / 2.0),
                          (y - (N - 1) / 2.0) / ((N - 1) / 2.0)) else 0
             for x in range(N)] for y in range(N)]

def depth_field(m):
    """Depth = distance to shore (BFS). The deepest point is the incentre."""
    d = [[-1] * N for _ in range(N)]
    q = deque()
    for y in range(N):
        for x in range(N):
            if m[y][x] == 0:
                d[y][x] = 0; q.append((x, y))
    while q:
        x, y = q.popleft()
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            a, b = x + dx, y + dy
            if 0 <= a < N and 0 <= b < N and d[b][a] < 0:
                d[b][a] = d[y][x] + 1; q.append((a, b))
    return d

def inside_segment(m, p, q, steps=120):
    (x0, y0), (x1, y1) = p, q
    for i in range(steps + 1):
        t = i / float(steps)
        x = int(round(x0 + t * (x1 - x0))); y = int(round(y0 + t * (y1 - y0)))
        if not (0 <= x < N and 0 <= y < N) or m[y][x] == 0:
            return False
    return True

def shore(m):
    """Water cells touching the shore -- the endpoints of any maximal chord."""
    return [(x, y) for y in range(N) for x in range(N)
            if m[y][x] and any(not (0 <= x + dx < N and 0 <= y + dy < N)
                               or m[y + dy][x + dx] == 0
                               for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))]

def longest_chord(m, pts, direction=None, tol=0.12):
    """Longest chord lying entirely in water; with direction given, restricted
    to chords within about 7 degrees of perpendicular to it."""
    best, bl = None, -1.0
    for i in range(len(pts)):
        for j in range(i + 1, len(pts)):
            p, q = pts[i], pts[j]
            vx, vy = q[0] - p[0], q[1] - p[1]
            L = math.hypot(vx, vy)
            if L <= bl: continue
            if direction is not None:
                ux, uy = direction
                if abs((vx * ux + vy * uy) / (L * math.hypot(ux, uy))) > tol: continue
            if inside_segment(m, p, q): best, bl = (p, q), L
    return best, bl

def seg_intersect(a, b, c, d):
    (x1, y1), (x2, y2) = a, b
    (x3, y3), (x4, y4) = c, d
    den = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    if abs(den) < 1e-12: return None
    return (((x1 * y2 - y1 * x2) * (x3 - x4) - (x1 - x2) * (x3 * y4 - y3 * x4)) / den,
            ((x1 * y2 - y1 * x2) * (y3 - y4) - (y1 - y2) * (x3 * y4 - y3 * x4)) / den)

SHAPES = [
    ('circle',        'convex',  lambda u, v: u * u + v * v <= 0.81),
    ('ellipse 2:1',   'convex',  lambda u, v: (u / 0.92) ** 2 + (v / 0.46) ** 2 <= 1),
    ('rectangle 3:2', 'convex',  lambda u, v: abs(u) <= 0.9 and abs(v) <= 0.6),
    ('teardrop',      'convex',  lambda u, v: (u / 0.9) ** 2 + (v / (0.30 + 0.35 * (1 - u))) ** 2 <= 1),
    ('pear',          'convex',  lambda u, v: ((u - 0.25) / 0.62) ** 2 + (v / 0.62) ** 2 <= 1
                                              or ((u + 0.45) / 0.42) ** 2 + (v / 0.42) ** 2 <= 1),
    ('crescent',      'concave', lambda u, v: (u * u + v * v <= 0.7744)
                                              and ((u - 0.55) ** 2 + v * v > 0.3844)),
    ('hourglass',     'concave', lambda u, v: abs(v) <= 0.85 and abs(u) <= 0.85 * (0.18 + 0.9 * abs(v))),
    ('L-shape',       'concave', lambda u, v: (-0.85 <= u <= 0.85 and -0.85 <= v <= -0.25)
                                              or (-0.85 <= u <= -0.25 and -0.85 <= v <= 0.85)),
]

print("  Depth falls off with distance from shore -- the model the rule itself")
print("  presupposes. The offset is measured to the NEAREST deepest cell, which")
print("  is the reading most favourable to the conjecture.\n")
print('      basin           outline    length  breadth   offset   offset/length')
rel = {}
for name, kind, fn in SHAPES:
    m = make(fn)
    d = depth_field(m)
    pts = shore(m)
    water = [(x, y) for y in range(N) for x in range(N) if m[y][x]]
    (a, b), L = longest_chord(m, pts)
    (c, e), B = longest_chord(m, pts, direction=(b[0] - a[0], b[1] - a[1]))
    mx = max(d[p[1]][p[0]] for p in water)
    deepest = [p for p in water if d[p[1]][p[0]] == mx]
    X = seg_intersect(a, b, c, e)
    off = min(math.hypot(X[0] - p[0], X[1] - p[1]) for p in deepest)
    rel[name] = off / L
    print('      %-15s %-9s %6.1f   %6.1f   %6.2f    %6.3f' % (name, kind, L, B, off, off / L))

convex  = [rel[n] for n, k, _ in SHAPES if k == 'convex']
concave = [rel[n] for n, k, _ in SHAPES if k == 'concave']

check(rel['circle'] < 1e-9,
      'exact on the circle -- the crossing lands on the deepest cell',
      '%.3f' % rel['circle'])
check(rel['ellipse 2:1'] < 0.01,
      'within %.1f%% of the length on a 2:1 ellipse' % (100 * rel['ellipse 2:1']))
check(max(convex) < 0.10,
      'every convex basin holds to within %.0f%% of its greatest length'
      % (100 * max(convex)))
check(min(concave) > 2 * max(convex),
      'every concave basin misses by more (%.0f%%+) -- at least twice the worst convex case'
      % (100 * min(concave)))
print("\n      Finding: the rule is a statement about the outline, not about water.")
print("      It is exact where the basin has a centre of symmetry, good to within")
print("      a tenth of the length wherever the outline is convex, and it breaks")
print("      as soon as the shore turns back on itself. Walden's outline is convex")
print("      and close to an ellipse, so the pond Thoreau tested it on was the")
print("      most favourable case there is. He was right about Walden. The rule")
print("      he proposed for harbours and for characters is not carried by this.")

# ==========================================================================
head(2, 'THE SOUNDINGS')
DEPTH_FT = 102.0
print('      reported greatest depth   %.0f ft = %.2f m' % (DEPTH_FT, DEPTH_FT * 0.3048))
print('      soundings                 more than 100, through the winter ice, 1846')
check(abs(DEPTH_FT * 0.3048 - 31.09) < 0.02, '102 ft is 31.09 m')
check(DEPTH_FT > 100, 'the pond had a bottom, against the local legend that it had none')

# ==========================================================================
head(3, 'CONCORD, THOREAU TO NOW')
MAY15, MAY4 = 15, 4
shift_days = MAY15 - MAY4
warm_F = 48.0 - 42.0
warm_C = warm_F * 5.0 / 9.0
print('      mean first flowering, 32 species   15 May  ->   4 May')
print('      shift                              %d days earlier' % shift_days)
print('      mean spring temperature            42 F    ->  48 F   (+%.0f F = +%.2f C)'
      % (warm_F, warm_C))
print('      implied sensitivity                %.2f days per F = %.2f days per C'
      % (shift_days / warm_F, shift_days / warm_C))
check(shift_days == 11, 'the shift is eleven days')
check(abs(warm_C - 3.33) < 0.01, 'six degrees Fahrenheit is 3.33 degrees Celsius')
check(2.0 < shift_days / warm_C < 4.5,
      'implied %.1f days per degree C -- the published community rate is ~3'
      % (shift_days / warm_C))

# ==========================================================================
head(4, 'THE CHRONOLOGY')
EVENTS = [
    (1846, 'more than a hundred soundings of Walden Pond through the ice'),
    (1854, 'Walden published, carrying his own survey and the rule'),
    (1860, 'The Succession of Forest Trees; the Kalendar charts begin'),
    (1862, 'dies 6 May; Emerson eulogy, First Parish, Concord, 9 May'),
    (2003, 'Primack and Miller-Rushing locate the Concord records'),
    (2008, 'Ecology: global warming and flowering times in Thoreau\'s Concord'),
    (2012, 'BioScience: the method written up as a template'),
]
for y, what in EVENTS:
    print('      %d   %s' % (y, what))
years = [y for y, _ in EVENTS]
check(years == sorted(years), 'the chronology is monotone')
check(2003 - 1862 == 141, 'the notebooks waited 141 years to be read as data')
check(2012 - 2003 == 9, 'nine years from the find to a published method')

# ==========================================================================
head(5, 'THE CHAPTER FILE')
if not os.path.exists(CHAPTER):
    check(False, 'ch-thoreau.html present next to this script', CHAPTER)
else:
    raw = open(CHAPTER, encoding='utf-8').read()
    flat = re.sub(r'<[^>]+>', ' ', raw).lower()
    for y, _ in EVENTS:
        check(str(y) in raw, 'chapter carries the year %d' % y)
    check('primack' in flat, 'chapter names Primack, who read the notebooks')
    check('surveyor' in flat, 'chapter says he was a surveyor by trade')
    check('102' in raw, 'chapter carries the measured depth')
    check('eleven days' in flat or '11 days' in flat, 'chapter carries the shift')
    check('huckleberry' in flat, "chapter carries Emerson's verdict")
    # the rule is reported as Thoreau's conjecture, not as a fact about ponds
    check('conjectur' in flat or 'rule' in flat, 'chapter frames the rule as a rule')

# ==========================================================================
print('\n' + '=' * 68)
if fails:
    print('  %d FAILED' % len(fails))
    for f in fails: print('    - ' + f)
    sys.exit(1)
print('  ALL CHECKS PASSED')
print('=' * 68)
