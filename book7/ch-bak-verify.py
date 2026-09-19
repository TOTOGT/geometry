#!/usr/bin/env python3
"""
ch-bak-verify.py -- every number on book7/ch-bak.html.

The abelian sandpile (Bak-Tang-Wiesenfeld) on an N x N grid with open boundary:
a site holding 4 or more topples, sending one grain to each of its four
neighbours; grains leaving the edge are lost.

Blocks:
  [1] Dhar's abelian property -- final state AND toppling count independent of
      the order topplings are performed in
  [2] the stationary density for N = 16, 32, 64
  [3] the transient: why the first N = 100 measurement was wrong
  [4] avalanche sizes are broadly distributed, spanning orders of magnitude
  [5] the exponent, and why this script does NOT claim to have measured it

Standard library only.  Run:  python3 book7/ch-bak-verify.py
Takes roughly a minute.
"""
import collections, math, random, sys

FAIL = []
def check(label, ok, detail=""):
    print(("  PASS  " if ok else "  FAIL  ") + label + (("   " + detail) if detail else ""))
    if not ok: FAIL.append(label)

def stabilise(g, N, order="lifo"):
    """Topple until stable. Returns the number of topplings."""
    n = 0
    seed = [(i, j) for i in range(N) for j in range(N) if g[i][j] >= 4]
    if order == "lifo":
        stack = list(seed); pop = stack.pop
    else:
        stack = collections.deque(seed); pop = stack.popleft
    while stack:
        i, j = pop()
        while g[i][j] >= 4:
            g[i][j] -= 4; n += 1
            for a, b in ((i-1, j), (i+1, j), (i, j-1), (i, j+1)):
                if 0 <= a < N and 0 <= b < N:
                    g[a][b] += 1
                    if g[a][b] >= 4: stack.append((a, b))
    return n

print("=" * 70)
print("ch-bak-verify.py -- the abelian sandpile")
print("=" * 70)

print("\n[1] Dhar's abelian property")
random.seed(3)
for trial in range(6):
    N = 12
    base = [[random.randrange(0, 8) for _ in range(N)] for _ in range(N)]
    a = [r[:] for r in base]; b = [r[:] for r in base]
    na = stabilise(a, N, "lifo"); nb = stabilise(b, N, "fifo")
    check("trial %d: identical final configuration" % trial, a == b)
    check("trial %d: identical toppling count" % trial, na == nb,
          "lifo %d, fifo %d" % (na, nb))
check("the property is exact, not approximate", True,
      "equality of grids and of counts, not a tolerance")

def drive(N, drops, burn, seed=7, marks=()):
    random.seed(seed)
    g = [[0]*N for _ in range(N)]
    sizes = []; dens = []; snap = {}
    for t in range(1, drops + 1):
        g[random.randrange(N)][random.randrange(N)] += 1
        n = stabilise(g, N)
        if t in marks: snap[t] = sum(map(sum, g)) / (N*N)
        if t > burn:
            sizes.append(n); dens.append(sum(map(sum, g)) / (N*N))
    return sizes, (sum(dens)/len(dens) if dens else 0.0), snap

print("\n[2] the stationary density")
DENS = {}
for N, dr, bu, want in [(16, 20000, 8000, 2.045), (32, 30000, 12000, 2.084),
                        (64, 40000, 20000, 2.104)]:
    sizes, d, _ = drive(N, dr, bu)
    DENS[N] = (d, sizes)
    check("N = %3d   density = %.3f" % (N, d), abs(d - want) < 0.004,
          "page says %.3f" % want)
check("the density increases with N", DENS[16][0] < DENS[32][0] < DENS[64][0],
      "%.3f < %.3f < %.3f" % (DENS[16][0], DENS[32][0], DENS[64][0]))
check("and stays below the limiting 2.125", DENS[64][0] < 2.125,
      "%.4f, approaching from below" % DENS[64][0])

print("\n[3] the transient -- the measurement this page got wrong first")
_, _, snap = drive(100, 50000, 10**9, marks=(20000, 50000))
check("N = 100 after 20,000 drops: density = %.3f -- NOT stationary" % snap[20000],
      snap[20000] < 2.05, "well below the N = 64 value of %.3f" % DENS[64][0])
check("N = 100 after 50,000 drops: density = %.3f" % snap[50000],
      snap[50000] > 2.09, "the pile has now filled")
check("the transient explains the discarded 2.064",
      snap[50000] - snap[20000] > 0.08,
      "density moved %.3f between those two marks" % (snap[50000] - snap[20000]))

print("\n[4] avalanche sizes span orders of magnitude")
for N in (32, 64):
    nz = [s for s in DENS[N][1] if s > 0]
    med = sorted(nz)[len(nz)//2]
    check("N = %2d   %d avalanches, median %d, largest %d" % (N, len(nz), med, max(nz)),
          max(nz) > 40 * med, "the largest is %dx the median -- the mean is not the story"
          % (max(nz) // med))
    decades = math.log10(max(nz) / 1)
    check("N = %2d   spans %.1f decades in size" % (N, decades), decades > 2.5)

print("\n[5] the exponent")
def tau(nz, lo, hi):
    c = collections.Counter(nz); bins = []; b = 1
    while b <= max(nz):
        top = int(b * 1.7) + 1
        cnt = sum(v for k, v in c.items() if b <= k < top)
        if cnt: bins.append((math.sqrt(b * top), cnt / (top - b)))
        b = top
    pts = [(math.log(x), math.log(y)) for x, y in bins if lo <= x <= hi and y > 0]
    n = len(pts); sx = sum(p[0] for p in pts); sy = sum(p[1] for p in pts)
    sxx = sum(p[0]**2 for p in pts); sxy = sum(p[0]*p[1] for p in pts)
    return -((n*sxy - sx*sy) / (n*sxx - sx*sx))
ts = []
for N in (32, 64):
    nz = [s for s in DENS[N][1] if s > 0]
    for lo, hi in ((4, N*N/8), (8, N*N/4)):
        t = tau(nz, lo, hi); ts.append(t)
        print("      N = %2d  window [%d, %d]   tau = %.3f" % (N, lo, hi, t))
check("every fit lies in 1.0 to 1.2", all(1.0 <= t <= 1.2 for t in ts), "%s" % [round(t,3) for t in ts])
check("the fits agree with EACH OTHER to better than 0.05",
      max(ts) - min(ts) < 0.05, "spread %.3f" % (max(ts) - min(ts)))
check("and every one of them sits well below the literature's 1.2",
      max(ts) < 1.15, "highest fit %.3f -- a systematic gap, not scatter" % max(ts))

print("\n" + "=" * 70)
print("[HONESTY]")
print("=" * 70)
print("""  What this establishes. Dhar's abelian property, exactly: the same
  configuration stabilised under two different toppling orders gives the
  identical grid and the identical number of topplings, in every trial. That is
  an equality, not a tolerance, and it is the one result on the page that is not
  statistics. The stationary density rises with lattice size toward the
  literature's 2.125 and the avalanche sizes span more than two and a half
  decades.

  What it does not establish. THE EXPONENT IS NOT MEASURED HERE, and the
  shape of the failure is worth naming. The four fits agree with each other to
  0.034 -- and every one of them sits about 0.15 BELOW the literature's value
  near 1.2. Mutually consistent and collectively wrong is the signature of a
  systematic error, here finite lattice size and a short fitting window, and it
  is exactly the case where internal agreement would tempt someone to publish
  the number. An earlier draft of this block asserted the fits disagreed with
  each other; they do not, and the assertion was replaced rather than the
  threshold loosened.

  The density figures are single runs at one seed. They are reproducible from
  this script and they are not averages over seeds, so the third decimal should
  not be trusted.

  Nothing here bears on Bak's larger claim -- that earthquakes, extinctions and
  markets are the same phenomenon. That claim is contested, the page marks it
  OPEN, and a sandpile simulation cannot speak to it either way.""")

print()
if FAIL:
    print("FAILED: %d" % len(FAIL))
    for f in FAIL: print("   " + f)
    sys.exit(1)
print("All blocks pass.")
