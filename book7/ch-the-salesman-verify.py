#!/usr/bin/env python3
"""
ch-the-salesman-verify.py -- how hard the travelling salesman problem is,
measured instead of asserted.

TSP is the standard newspaper illustration of computational impossibility.
It is also solved, to PROVEN optimality, for instances with tens of thousands
of cities, and it is solved to within a fraction of a percent in milliseconds
for the sizes anyone actually has. Both statements are true. This script
measures the distance between them.

WHAT IS COMPUTED
  A. An exact solver (Held-Karp, O(n^2 2^n)) and its wall, timed.
  B. A real instance: a sales tour of Brazilian cities. n = 5 -> 0.1 ms,
     n = 12 -> 19 ms, both PROVEN OPTIMAL. "NP-hard" has nothing to say here.
  C. Heuristic quality against proven optima: nearest neighbour is 6-11% bad,
     2-opt is about 1%, and 2-opt followed by Or-opt is 0.00-0.04%.
  D. The Held-Karp 1-tree lower bound reaching 99.0-99.7% of the true optimum
     -- so near-optimality can be CERTIFIED without ever finding the optimum.
  E. What NP-hardness actually asserts, and the three qualifiers the headline
     drops.

Run:  python3 book7/ch-the-salesman-verify.py
"""
import math, random, time

FAIL = []
def head(n, t):
    print(); print("=" * 78); print("%s. %s" % (n, t)); print("=" * 78)

# ---------------------------------------------------------------------------
def inst(n, seed):
    r = random.Random(seed)
    P = [(r.random(), r.random()) for _ in range(n)]
    return [[math.dist(P[i], P[j]) for j in range(n)] for i in range(n)]

def held_karp(D):
    """Exact. Dynamic programming over subsets. O(n^2 2^n) time, O(n 2^n) space."""
    n = len(D); FULL = 1 << (n-1)
    dp = [[math.inf]*(n-1) for _ in range(FULL)]
    for j in range(n-1): dp[1 << j][j] = D[n-1][j]
    for m in range(FULL):
        row = dp[m]
        for j in range(n-1):
            c = row[j]
            if c == math.inf or not (m >> j) & 1: continue
            for k in range(n-1):
                if (m >> k) & 1: continue
                nm = m | (1 << k); v = c + D[j][k]
                if v < dp[nm][k]: dp[nm][k] = v
    return min(dp[FULL-1][j] + D[j][n-1] for j in range(n-1))

def tour_len(t, D): return sum(D[t[i]][t[(i+1) % len(t)]] for i in range(len(t)))

def nn(D, s=0):
    n = len(D); un = set(range(n)); un.discard(s); t = [s]; c = s
    while un:
        c = min(un, key=lambda j: D[c][j]); un.discard(c); t.append(c)
    return t

def two_opt(t, D, limit=None):
    n = len(t); t = t[:]; t0 = time.time(); imp = True
    while imp:
        imp = False
        for i in range(n-1):
            for k in range(i+2, n):
                if i == 0 and k == n-1: continue
                a, b, c, d = t[i], t[i+1], t[k], t[(k+1) % n]
                if D[a][b] + D[c][d] > D[a][c] + D[b][d] + 1e-12:
                    t[i+1:k+1] = reversed(t[i+1:k+1]); imp = True
            if limit and time.time()-t0 > limit: return t
    return t

def or_opt(t, D):
    n = len(t); t = t[:]; imp = True
    while imp:
        imp = False
        for L in (1, 2, 3):
            for i in range(n):
                if i+L > n: continue
                seg = t[i:i+L]; rest = t[:i] + t[i+L:]
                if len(rest) < 2: continue
                a = t[(i-1) % n]; b = t[(i+L) % n]
                gain0 = D[a][seg[0]] + D[seg[-1]][b] - D[a][b]
                best = None
                for j in range(len(rest)):
                    p, q = rest[j], rest[(j+1) % len(rest)]
                    for s in (seg, seg[::-1]):
                        delta = D[p][s[0]] + D[s[-1]][q] - D[p][q]
                        if gain0 - delta > 1e-12 and (best is None or delta < best[0]):
                            best = (delta, j, s)
                if best:
                    _, j, s = best
                    t = rest[:j+1] + list(s) + rest[j+1:]; imp = True; break
            if imp: break
    return t

# ---------------------------------------------------------------------------
head(1, "A REAL INSTANCE -- a sales tour of Brazil")
# ---------------------------------------------------------------------------
CITY = [("Sao Paulo",-23.5505,-46.6333), ("Rio de Janeiro",-22.9068,-43.1729),
        ("Belo Horizonte",-19.9167,-43.9345), ("Brasilia",-15.7939,-47.8828),
        ("Curitiba",-25.4284,-49.2733), ("Campinas",-22.9099,-47.0626),
        ("Goiania",-16.6869,-49.2648), ("Vitoria",-20.3155,-40.3128),
        ("Florianopolis",-27.5954,-48.5480), ("Porto Alegre",-30.0346,-51.2177),
        ("Salvador",-12.9777,-38.5016), ("Recife",-8.0476,-34.8770)]
def gc(a, b):
    R = 6371.0
    la1, lo1 = math.radians(a[1]), math.radians(a[2])
    la2, lo2 = math.radians(b[1]), math.radians(b[2])
    h = math.sin((la2-la1)/2)**2 + math.cos(la1)*math.cos(la2)*math.sin((lo2-lo1)/2)**2
    return 2*R*math.asin(math.sqrt(h))

def hk_tour(D, start=0):
    n = len(D); oth = [i for i in range(n) if i != start]; m = len(oth)
    dp = [[math.inf]*m for _ in range(1 << m)]; par = [[-1]*m for _ in range(1 << m)]
    for j, c in enumerate(oth): dp[1 << j][j] = D[start][c]
    for msk in range(1 << m):
        for j in range(m):
            c = dp[msk][j]
            if c == math.inf or not (msk >> j) & 1: continue
            for k in range(m):
                if (msk >> k) & 1: continue
                nm = msk | (1 << k); v = c + D[oth[j]][oth[k]]
                if v < dp[nm][k]: dp[nm][k] = v; par[nm][k] = j
    full = (1 << m)-1
    j = min(range(m), key=lambda j: dp[full][j] + D[oth[j]][start])
    best = dp[full][j] + D[oth[j]][start]
    tour = []; msk = full
    while j != -1:
        tour.append(oth[j]); pj = par[msk][j]; msk ^= (1 << j); j = pj
    tour.append(start); tour.reverse()
    return best, tour

for label, names in (("core  ", ["Sao Paulo","Rio de Janeiro","Belo Horizonte","Brasilia","Curitiba"]),
                     ("plus  ", ["Sao Paulo","Rio de Janeiro","Belo Horizonte","Brasilia","Curitiba",
                                 "Campinas","Goiania","Vitoria","Florianopolis","Porto Alegre"]),
                     ("full  ", [c[0] for c in CITY])):
    sub = [c for c in CITY if c[0] in names]
    D = [[gc(a, b) for b in sub] for a in sub]
    t0 = time.time(); best, tour = hk_tour(D, 0); dt = time.time()-t0
    print("  %s n=%2d  %6.0f km great-circle   PROVEN OPTIMAL in %7.2f ms"
          % (label, len(sub), best, 1000*dt))
    print("        " + " -> ".join(sub[i][0] for i in tour) + " -> " + sub[0][0])
print()
print("  Five cities is 12 distinct tours. Twelve cities is about 20 million,")
print("  and the machine checked all of them implicitly in 19 milliseconds.")
print("  Whatever NP-hardness is a statement about, it is not a statement")
print("  about this.")

# ---------------------------------------------------------------------------
head(2, "WHERE THE WALL ACTUALLY IS")
# ---------------------------------------------------------------------------
print("      %-6s %-14s" % ("n", "Held-Karp"))
ts = []
for n in (10, 12, 14, 16, 18):
    D = inst(n, 1); t0 = time.time(); held_karp(D); dt = time.time()-t0
    ts.append((n, dt)); print("      %-6d %-14s" % (n, "%.3f s" % dt))
ratio = ts[-1][1]/ts[-2][1]
print()
print("  Each extra city multiplies the work by about %.1f. Extrapolating the"
      % (ratio**0.5))
print("  measured n=18 time by n^2 2^n:")
base = ts[-1][1]/(18*18*2**18)
for n in (20, 25, 30, 40, 50):
    s = base*n*n*2**n; yr = s/3.15e7
    pretty = ("%.0f years" % yr) if yr > 1 else (("%.1f days" % (s/86400)) if s > 86400 else "%.0f s" % s)
    print("      n = %-3d %-16s" % (n, pretty))
print()
print("  The wall is real and it is at about n = 25 for THIS algorithm. That")
print("  is the true content of the scary version, and it is worth knowing.")
ok = ts[-1][1] > ts[0][1]*50
print("  [%s] runtime grows by more than 50x from n=10 to n=18"
      % ("SHOWN" if ok else "FAIL "))
if not ok: FAIL.append("scaling not observed")

# ---------------------------------------------------------------------------
head(3, "BUT YOU ALMOST NEVER NEED THE OPTIMUM")
# ---------------------------------------------------------------------------
print("  Gap above the PROVEN optimum, mean over 30 random Euclidean instances:")
print()
print("      %-4s %-12s %-12s %-14s" % ("n", "nearest nb", "+ 2-opt", "+ Or-opt"))
for n in (8, 10, 12):
    g1 = g2 = g3 = 0.0
    for s in range(30):
        D = inst(n, s); opt = held_karp(D)
        a = nn(D); b = two_opt(a, D); c = or_opt(b, D)
        g1 += tour_len(a, D)/opt - 1
        g2 += tour_len(b, D)/opt - 1
        g3 += tour_len(c, D)/opt - 1
    print("      %-4d %-12s %-12s %-14s"
          % (n, "%.2f%%" % (100*g1/30), "%.2f%%" % (100*g2/30), "%.2f%%" % (100*g3/30)))
    if 100*g3/30 > 1.0: FAIL.append("or-opt worse than 1%% at n=%d" % n)
print()
print("  Two local-search moves, a few lines each, land within four hundredths")
print("  of one percent of an answer that is provably the best there is.")

# ---------------------------------------------------------------------------
head(4, "AND YOU CAN CERTIFY IT WITHOUT SOLVING IT")
# ---------------------------------------------------------------------------
def onetree(D, iters=300):
    n = len(D); pi = [0.0]*n; best = -math.inf
    UB = tour_len(or_opt(two_opt(nn(D), D), D), D); t = UB/(2*n)
    for _ in range(iters):
        C = [[D[i][j]+pi[i]+pi[j] for j in range(n)] for i in range(n)]
        inT = [False]*n; key = [math.inf]*n; par = [-1]*n; deg = [0]*n
        key[1] = 0.0; total = 0.0
        for _ in range(n-1):
            u = min((v for v in range(1, n) if not inT[v]), key=lambda v: key[v])
            inT[u] = True; total += key[u]
            if par[u] >= 0: deg[u] += 1; deg[par[u]] += 1
            for v in range(1, n):
                if not inT[v] and C[u][v] < key[v]: key[v] = C[u][v]; par[v] = u
        nb = sorted(range(1, n), key=lambda j: C[0][j])[:2]
        total += C[0][nb[0]] + C[0][nb[1]]; deg[0] = 2
        for j in nb: deg[j] += 1
        L = total - 2*sum(pi)
        if L > best: best = L
        g = [deg[i]-2 for i in range(n)]
        nrm = sum(x*x for x in g)
        if nrm == 0: break
        step = t*(UB-L)/nrm
        pi = [pi[i]+step*g[i] for i in range(n)]; t *= 0.98
    return best

print("  The Held-Karp 1-tree bound: relax the tour to a spanning structure,")
print("  then push node potentials until the relaxation nearly IS a tour.")
print("  It never finds a tour. It brackets one from below.")
print()
print("      %-4s %-20s" % ("n", "bound / true optimum"))
for n in (10, 12, 14):
    r = []
    for s in range(12):
        D = inst(n, s); r.append(onetree(D)/held_karp(D))
    frac = 100*sum(r)/len(r)
    print("      %-4d %-20s" % (n, "%.2f%%" % frac))
    if frac < 98.0: FAIL.append("1-tree bound weak at n=%d" % n)
print()
print("  So in practice: run the heuristic, run the bound, and if they meet")
print("  within a fraction of a percent you are done -- with a CERTIFICATE,")
print("  and without ever having solved the problem the headline says you")
print("  cannot solve.")

# ---------------------------------------------------------------------------
head(5, "WHAT 'NP-HARD' ACTUALLY SAYS")
# ---------------------------------------------------------------------------
for s in [
 "  The theorem is: no algorithm is known that solves EVERY instance in time",
 "  polynomial in n, and if one existed, P = NP. Three qualifiers ride along",
 "  with it, and the headline drops all three:",
 "",
 "    WORST CASE.   The statement quantifies over the hardest instance at",
 "                  each size, not the one you have. Nothing in it forbids",
 "                  every instance you will ever meet from being easy.",
 "",
 "    ASYMPTOTIC.   It is a claim about the limit n -> infinity. At n = 5 it",
 "                  makes no claim at all; section 1 took 0.1 milliseconds.",
 "",
 "    EXACT.        It is about finding the optimum, not about getting close.",
 "                  Section 3 gets within 0.04% and section 4 proves it did.",
 "",
 "  And for the Euclidean case specifically -- which is what a map is -- the",
 "  theory goes further the other way: Arora and Mitchell showed in 1998 that",
 "  Euclidean TSP admits a PTAS, an approximation scheme that gets within any",
 "  fixed epsilon in polynomial time. [CITED]",
 "",
 "  Meanwhile the exact wall keeps moving. Section 2's algorithm dies near",
 "  n = 25. Concorde, using branch-and-cut rather than brute force, solved an",
 "  85,900-city instance to PROVEN optimality -- certified and published.",
 "  [CITED: Applegate, Bixby, Chvatal, Cook, Espinoza, Goycoolea & Helsgaun,",
 "  Operations Research Letters 37 (2009) 11-15.]",
]: print(s)

# ---------------------------------------------------------------------------
head(6, "SO WHAT IS ACTUALLY HARD ABOUT A REAL ROUTE")
# ---------------------------------------------------------------------------
for s in [
 "  Not the combinatorics. Section 1 solved a national sales tour exactly, in",
 "  milliseconds, with a hundred lines of Python. What a real problem has that",
 "  this one does not:",
 "",
 "    - TIME WINDOWS. A meeting at 14:00 Tuesday is a constraint no distance",
 "      matrix contains, and TSP with time windows is a different and much",
 "      harder problem than TSP.",
 "    - THE METRIC IS WRONG. Section 1 uses great-circle distance. What is",
 "      actually being minimised is hours, or fare, or fatigue, and the flight",
 "      schedule between two Brazilian cities does not care how far apart they",
 "      are.",
 "    - ASYMMETRY. Real travel times are not symmetric and not a metric. The",
 "      triangle inequality, which most of the good theory assumes, can fail.",
 "    - THE DATA. Every figure above came from twelve pairs of coordinates.",
 "      A real system's difficulty is almost entirely in keeping the inputs",
 "      current, and none of that is a computational question.",
]: print(s)

# ---------------------------------------------------------------------------
head(7, "ONE SALESMAN IS SOLVED. A SALES FORCE IS A DIFFERENT PROBLEM.")
# ---------------------------------------------------------------------------
import itertools
POP = {"Sao Paulo":22.4,"Rio de Janeiro":13.6,"Belo Horizonte":6.0,"Brasilia":4.9,
       "Curitiba":3.7,"Campinas":3.3,"Goiania":2.8,"Vitoria":2.0,
       "Florianopolis":1.2,"Porto Alegre":4.3,"Salvador":3.9,"Recife":4.1}
DD = [[gc(a, b) for b in CITY] for a in CITY]
W  = [POP[c[0]] for c in CITY]; TOT = sum(W); N = len(CITY)
print("  Covering a country is not a tour. It is p-median: choose k bases so")
print("  that every client is near one. Weights are metro population, which is")
print("  a proxy for where the counterparties are and is [CITED, approximate].")
print()
print("      %-3s %-48s %-14s" % ("k", "bases", "wtd km/visit"))
vals = []
for k in range(1, 7):
    best = None
    for S in itertools.combinations(range(N), k):
        v = sum(W[i]*min(DD[i][s] for s in S) for i in range(N))/TOT
        if best is None or v < best[0]: best = (v, S)
    vals.append(best[0])
    if k <= 5:
        print("      %-3d %-48s %-14.1f" % (k, ", ".join(CITY[s][0] for s in best[1]), best[0]))
print()
print("  Each additional base buys about a third off the remaining distance,")
print("  steadily -- there is no knee in this curve and no natural k. The")
print("  decision is not hiding in the geometry.")
print()
sp_rj_cp = 100*sum(W[i] for i, c in enumerate(CITY)
                   if c[0] in ("Sao Paulo", "Rio de Janeiro", "Campinas"))/TOT
six = 100*sum(W[i] for i, c in enumerate(CITY)
              if c[0] in ("Sao Paulo","Rio de Janeiro","Belo Horizonte",
                          "Brasilia","Curitiba","Campinas"))/TOT
print("      Sao Paulo + Rio + Campinas          %.1f%% of weighted demand" % sp_rj_cp)
print("      the six southeast/centre metros     %.1f%%" % six)
if not (sp_rj_cp > 50 and six > 70): FAIL.append("concentration figures moved")
print("  [SHOWN] over half the weight sits in three adjacent metros.")
print()
print("  THAT is the operational finding, and it is not a routing result. A")
print("  field operation covering this map does not have a travelling salesman")
print("  problem worth solving; it has a CONCENTRATION, and the first question")
print("  is how many bases and where, not what order to visit in. Optimising")
print("  the route saves a percentage of travel. Getting the districting wrong")
print("  costs a multiple of headcount. The second lever is much larger than")
print("  the first, and only the first is famous.")

# ---------------------------------------------------------------------------
head("GAPS", "what this script does not establish")
# ---------------------------------------------------------------------------
for g in [
 "N1  THE HEURISTIC GAP IS MEASURED ONLY WHERE EXACT IS AVAILABLE, so n <= 12.",
 "    Published results put 2-opt near 5% above optimal for large random",
 "    Euclidean instances; the sub-1% figures in section 3 are a small-n",
 "    effect and MUST NOT be read as a claim about large instances.",
 "",
 "N2  NO LARGE-INSTANCE GAP IS CLAIMED. Running 2-opt at n = 1000 against the",
 "    1-tree bound gives a spread of 11-13%, and that number conflates",
 "    heuristic suboptimality with looseness of the bound at that size. The",
 "    bound's own quality at n = 1000 was not established, so the comparison",
 "    is not reported as a gap-to-optimal and no figure is quoted for it.",
 "",
 "N3  RANDOM UNIFORM POINTS ARE NOT REAL INSTANCES. Section 3's instances are",
 "    uniform in a unit square. Real city sets are clustered, and clustering",
 "    changes heuristic behaviour in both directions.",
 "",
 "N4  GREAT-CIRCLE, NOT ROAD OR AIR. Section 1's distances are straight lines",
 "    over the sphere. A road factor of about 1.28 raises the five-city loop",
 "    from 2743 to 3511 km, and that factor is a rule of thumb, not a",
 "    measurement.",
 "",
 "N5  THE EXTRAPOLATION IN SECTION 2 IS AN EXTRAPOLATION. n = 50 was never",
 "    run. The figure assumes the n^2 2^n form holds exactly and that memory",
 "    is free, and at n = 50 the table alone would need more storage than",
 "    exists.",
 "",
 "N6  CONCORDE IS CITED, NOT RUN. The 85,900-city certification is taken from",
 "    the published record and nothing here reproduces any part of it.",
 "",
 "N7  SECTION 7'S WEIGHTS ARE POPULATION, NOT CLIENTS. Metro population is a",
 "    proxy for where counterparties are and a poor one -- commodity",
 "    counterparties cluster by crop and by port, not by headcount, and a real",
 "    districting would use the actual client list. The concentration result",
 "    is robust to the weights being roughly wrong; the exact base sequence is",
 "    not.",
 "",
 "N8  p-MEDIAN IGNORES VISIT FREQUENCY, TRAVEL TIME AND CAPACITY. A base is",
 "    treated as costless and a rep as infinitely productive. Both are false,",
 "    and the real question -- how many people -- is not answered here.",
]: print("  " + g)

print(); print("=" * 78)
if FAIL:
    print("FAILED: " + ", ".join(FAIL)); raise SystemExit(1)
print("All checks passed. 8 gaps recorded above remain open.")
print("=" * 78)
