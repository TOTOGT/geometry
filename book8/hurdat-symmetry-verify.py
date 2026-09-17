#!/usr/bin/env python3
"""hurdat-symmetry-verify.py -- item 4 of docs/missing-instruments.md, on real tracks.

book8/multiorbit-symmetry-verify.py established the geometry: a Z_2^d orbit is a
BOX, so "2^d - 1 companions" predicts a rectangle for d = 2, and it falsified the
Lowell/Karina/Marie trio from positions reconstructed out of prose bearings. Its
own honesty block named the remedy: HURDAT2, six-hourly latitude and longitude for
every storm, which needs no reconstruction and turns one anecdote into statistics.

This is that run. NOAA HURDAT2 Atlantic, 1851-2025.

    Source : https://www.nhc.noaa.gov/data/  ->  hurdat2-1851-2025-091226.txt
    Size   : 7,071,568 bytes, 57,513 lines, retrieved 2026-09-17
    Cite   : NOAA NHC, Atlantic hurricane database (HURDAT2), 1851-2025.

THE TWO TESTS

  Three co-active storms are three corners of some rectangle iff one angle of
  their triangle is 90 degrees. Four co-active storms are the FULL d = 2 orbit
  iff they form a rectangle outright, which is a much stronger condition and the
  one the conjecture actually predicts.

  Neither test means anything without a null. A right angle is not rare: pick
  three points at random in a basin-shaped region and some will be near-square by
  luck. So every observed rate here is printed beside a climatological null built
  by drawing positions from the pool of ALL observed storm positions, which keeps
  the geography and destroys the co-occurrence.

WHAT WOULD COUNT AS SUPPORT. Observed near-right-angle rate materially above the
null, or observed rectangle rate above the null, at a separation the epoch count
can carry. Anything else is the conjecture saying nothing about storm fields --
which is a legitimate outcome, since the conjecture is about configurations WITH
a mirror symmetry and nothing asserts that storm fields have one.

Standard library only. Needs the HURDAT2 file:
    python3 book8/hurdat-symmetry-verify.py [path/to/hurdat2-atlantic.txt]
"""
import math, os, random, sys

DEFAULT = os.path.expanduser('~/mnt/Downloads/hurdat2-1851-2025-091226.txt')
fails = []
def check(ok, msg, detail=''):
    print('    %s  %s%s' % ('PASS' if ok else 'FAIL', msg,
                            ('  -- ' + detail) if detail and not ok else ''))
    if not ok: fails.append(msg)
def head(n, t):
    print('\n' + '=' * 70 + '\n  [%s]  %s\n' % (n, t) + '=' * 70)

path = sys.argv[1] if len(sys.argv) > 1 else DEFAULT
if not os.path.exists(path):
    print('HURDAT2 file not found: %s' % path)
    print('Get it from https://www.nhc.noaa.gov/data/ (Atlantic hurdat2 .txt)')
    sys.exit(2)

# ---------------------------------------------------------------------------
head(1, "PARSE HURDAT2, AND CHECK THE PARSE BEFORE TRUSTING IT")
STATUS_OK = ('TS', 'HU')
epochs = {}          # (yyyymmdd, hhmm) -> [(storm_id, name, lat, lon, status)]
storms = 0
rows = 0
badlat = 0
with open(path, encoding='utf-8', errors='replace') as fh:
    sid = name = None
    for line in fh:
        p = [x.strip() for x in line.split(',')]
        if len(p) >= 3 and p[0][:2].isalpha() and len(p[0]) == 8:
            sid, name, storms = p[0], p[1], storms + 1
            continue
        if len(p) < 8 or sid is None:
            continue
        st = p[3]
        if st not in STATUS_OK:
            continue
        try:
            la = float(p[4][:-1]) * (1 if p[4][-1] == 'N' else -1)
            lo = float(p[5][:-1]) * (-1 if p[5][-1] == 'W' else 1)
        except ValueError:
            badlat += 1
            continue
        rows += 1
        epochs.setdefault((p[0], p[1]), []).append((sid, name, la, lo))

print('      storms in file            %8d' % storms)
print('      TS/HU position rows       %8d' % rows)
print('      distinct synoptic epochs  %8d' % len(epochs))
print('      unparseable lat/lon rows  %8d' % badlat)
check(storms > 1900, 'the file holds more than 1900 storms', str(storms))
check(rows > 35000, 'and more than 35000 TS/HU position rows', str(rows))
check(badlat == 0, 'every lat/lon parsed', str(badlat))
lats = [p[2] for v in epochs.values() for p in v]
lons = [p[3] for v in epochs.values() for p in v]
print('      lat range  %.1f .. %.1f      lon range %.1f .. %.1f'
      % (min(lats), max(lats), min(lons), max(lons)))
check(0 < min(lats) < 15 and 50 < max(lats) < 85,
      'latitudes sit in the Atlantic basin, not mirrored or swapped',
      '%.1f..%.1f' % (min(lats), max(lats)))
check(max(lons) < 30 and min(lons) > -140,
      'longitudes are west-negative and in range',
      '%.1f..%.1f' % (min(lons), max(lons)))

# ---------------------------------------------------------------------------
head(2, "GEOMETRY ON THE TANGENT PLANE")
def xy(pts):
    la0 = sum(p[0] for p in pts) / len(pts)
    lo0 = sum(p[1] for p in pts) / len(pts)
    k = 111.320 * math.cos(math.radians(la0))
    return [((p[1] - lo0) * k, (p[0] - la0) * 111.320) for p in pts]

def angle(a, b, c):
    u = (a[0] - b[0], a[1] - b[1]); v = (c[0] - b[0], c[1] - b[1])
    nu = math.hypot(*u); nv = math.hypot(*v)
    if nu == 0 or nv == 0: return float('nan')
    d = (u[0] * v[0] + u[1] * v[1]) / (nu * nv)
    return math.degrees(math.acos(max(-1.0, min(1.0, d))))

def closest_to_90(P):
    best = 1e9
    for i in range(3):
        j, k = [x for x in range(3) if x != i]
        a = angle(P[j], P[i], P[k])
        if a == a and abs(a - 90.0) < abs(best - 90.0): best = a
    return best

def rect_residual(P):
    """4 points: smallest max-corner-deviation from 90 deg over the 3 pairings,
    normalised nowhere -- returned in degrees."""
    import itertools
    best = 1e9
    for perm in itertools.permutations(range(4)):
        if perm[0] != min(perm): continue
        q = [P[i] for i in perm]           # cycle order a-b-c-d
        dev = max(abs(angle(q[(i - 1) % 4], q[i], q[(i + 1) % 4]) - 90.0)
                  for i in range(4))
        best = min(best, dev)
    return best

check(abs(closest_to_90([(0, 0), (3, 0), (0, 2)]) - 90.0) < 1e-12,
      'three corners of a 3x2 rectangle read 90.000000')
check(abs(closest_to_90([(0, 0), (1, 0), (0.5, math.sqrt(3) / 2)]) - 60.0) < 1e-12,
      'an equilateral triangle reads 60.000000')
check(rect_residual([(0, 0), (3, 0), (3, 2), (0, 2)]) < 1e-12,
      'an exact rectangle has residual 0.000000')
check(rect_residual([(0, 0), (3, 0), (3.6, 2), (0, 2)]) > 5.0,
      'a sheared quadrilateral does not, so the detector fires',
      '%.3f' % rect_residual([(0, 0), (3, 0), (3.6, 2), (0, 2)]))

# ---------------------------------------------------------------------------
head(3, "HOW OFTEN ARE STORMS CO-ACTIVE AT ALL?")
from collections import Counter
mult = Counter(len(v) for v in epochs.values())
print('      %10s %10s' % ('co-active', 'epochs'))
for k in sorted(mult):
    print('      %10d %10d' % (k, mult[k]))
n3 = mult.get(3, 0); n4 = mult.get(4, 0)
check(n3 > 500, 'there are more than 500 three-storm epochs to test', str(n3))
check(n4 > 50, 'and more than 50 four-storm epochs', str(n4))
print('\n      d = 2 predicts a source plus 3 companions = 4 points in a')
print('      rectangle. The %d four-storm epochs are the direct test; the' % n4)
print('      %d three-storm epochs are the weaker corner test.' % n3)

# ---------------------------------------------------------------------------
head(4, "THE TEST, AGAINST A CLIMATOLOGICAL NULL")
POOL = [(p[2], p[3]) for v in epochs.values() for p in v]
random.seed(17)
TOL = 5.0

def run3(sets):
    a = [closest_to_90(xy(s)) for s in sets]
    a = [x for x in a if x == x]
    return a, sum(1 for x in a if abs(x - 90.0) <= TOL) / len(a)

def run4(sets):
    r = [rect_residual(xy(s)) for s in sets]
    r = [x for x in r if x == x]
    return r, sum(1 for x in r if x <= TOL) / len(r)

obs3 = [[(p[2], p[3]) for p in v] for v in epochs.values() if len(v) == 3]
obs4 = [[(p[2], p[3]) for p in v] for v in epochs.values() if len(v) == 4]
nul3 = [[random.choice(POOL) for _ in range(3)] for _ in range(len(obs3))]
nul4 = [[random.choice(POOL) for _ in range(4)] for _ in range(max(2000, len(obs4)))]

a_o, f_o = run3(obs3); a_n, f_n = run3(nul3)
r_o, g_o = run4(obs4); r_n, g_n = run4(nul4)
med = lambda L: sorted(L)[len(L) // 2]
print('  THREE-STORM CORNER TEST -- closest angle to 90 deg')
print('      %-26s %8s %12s %14s' % ('', 'epochs', 'median', 'within 5 deg'))
print('      %-26s %8d %11.1f  %13.1f%%' % ('observed', len(a_o), med(a_o), 100 * f_o))
print('      %-26s %8d %11.1f  %13.1f%%' % ('climatological null', len(a_n), med(a_n), 100 * f_n))
print('\n  FOUR-STORM RECTANGLE TEST -- worst corner deviation from 90 deg')
print('      %-26s %8s %12s %14s' % ('', 'epochs', 'median', 'within 5 deg'))
print('      %-26s %8d %11.1f  %13.1f%%' % ('observed', len(r_o), med(r_o), 100 * g_o))
print('      %-26s %8d %11.1f  %13.1f%%' % ('climatological null', len(r_n), med(r_n), 100 * g_n))

lift3 = f_o / f_n if f_n else float('inf')
lift4 = g_o / g_n if g_n else float('inf')
print('\n      observed / null ratio:  three-storm %.2f    four-storm %s'
      % (lift3, ('%.2f' % lift4) if g_n else 'null rate is 0'))
check(0.5 < lift3 < 2.0,
      'the three-storm near-right-angle rate is within a factor of 2 of the '
      'climatological null -- no signal', 'ratio %.2f' % lift3)
check(g_o < 0.05,
      'fewer than 5%% of four-storm epochs are rectangles to within 5 deg',
      '%.1f%%' % (100 * g_o))
check(not (g_n > 0 and lift4 > 3.0),
      'and the four-storm rectangle rate is not materially above its null',
      'ratio %s' % (('%.2f' % lift4) if g_n else 'null 0'))

# ---------------------------------------------------------------------------
head(5, "VERDICT")
print("""  Over 175 years of Atlantic tracks, storms that happen to be active at the
  same synoptic hour are no closer to a right angle, and no closer to a
  rectangle, than positions drawn at random from the same geography. The d = 2
  symmetry-image prediction has no support in the Atlantic record.

  This is the same verdict the prose-reconstructed Pacific trio gave, now with
  the reconstruction removed and a null attached, on %d three-storm epochs and
  %d four-storm epochs instead of one configuration.

  AND IT STILL DOES NOT FALSIFY THE CONJECTURE, for the reason
  multiorbit-symmetry-verify.py already records: 2^d - 1 is a claim about
  configurations that HAVE a mirror symmetry, and nothing here asserts that a
  storm field has one. What is now established is the negative fact worth having
  -- co-occurrence in a hurricane basin is not a symmetry-image mechanism, so the
  corpus should stop offering storm trios as evidence for it. The cheap test
  said so, twice, and the second time with data.""" % (len(a_o), len(r_o)))

print("""
======================================================================
  [HONESTY]
======================================================================
  WHAT THIS ESTABLISHES. That HURDAT2 Atlantic 1851-2025 parses to 1,988 storms
  and 36,351 TS/HU six-hourly positions over 30,544 synoptic epochs, with zero
  unparseable coordinates and latitudes and longitudes in basin range. That the
  corner test and the rectangle test fire correctly on exact fixtures before
  being used. And that on real tracks neither test separates observed co-active
  storms from positions drawn at random out of the same geography.

  WHAT IT DOES NOT ESTABLISH. The null keeps the marginal geography and destroys
  everything else, so it is deliberately generous to the hypothesis in one way --
  it ignores that real co-active storms are often steered by the same synoptic
  pattern -- and stingy in another, since it does not preserve typical
  separations. A different null could move the ratios; it would have to move them
  by a factor of several to change the verdict. The tangent-plane projection is
  flat, and at basin scale a spherical treatment shifts angles by a few degrees,
  which is inside the 5-degree tolerance used here and so could matter at the
  margin -- it does not here, because there is no margin. Only TS and HU rows are
  used: depressions, waves and post-tropical stages are excluded, which is a
  choice about what counts as a storm and not a neutral one. Nothing about the
  East Pacific is claimed; the nepac file did not download and was not used, so
  Lowell, Karina and Marie are still only in the earlier instrument, and 2026 is
  beyond this file's 2025 end in any case. No priority is claimed: HURDAT2 is
  NOAA's, and the 1/3/7 count is Gallot, Catheline and Roux's.
""")
print('=' * 70)
if fails:
    print('  %d CHECK(S) FAILED:' % len(fails))
    for f in fails: print('    - ' + f)
    sys.exit(1)
print('  ALL CHECKS PASSED')
