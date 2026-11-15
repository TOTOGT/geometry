#!/usr/bin/env python3
"""Audit evidence for book4/ch18-seismic-lattice.html (2026-11-14). Read-only: edits nothing.

[A] Caption FIG 18.1: "The 1/6 figure is the mathematical minimum for a convex tile that
    fills the plane" (also sec 18.1 "most neighbours of any tile that fills the plane").
    Counterexample: a monohedral tiling by 1x3 rectangles in which a tile has 8 edge-neighbours.
[B] Q1 row: no_straight_continuation : forall d : Fin 6, d != d+2 and d != d+4.
    Does that statement separate the hexagonal tiling from the square grid? Compare with the
    statement that does encode "no straight continuation", and with real coordinates.
[C] Page/Lean bookkeeping: counts and open/proved wording.
Exit code 0 = every check behaved as recorded below; the findings are in the printed lines.
"""
import itertools, math, re, sys, pathlib
HERE = pathlib.Path(__file__).resolve().parent
fails = 0
def check(name, ok):
    global fails
    print(("PASS " if ok else "FAIL ") + name); fails += (not ok)

# ---------- [A] brick tiling ----------
W, H = 12, 8                      # torus; pattern period is 3 x 4
tile = {}                         # cell -> tile id
tiles = {}
def put(tid, cells):
    for c in cells:
        c = (c[0] % W, c[1] % H)
        assert c not in tile, "overlap"
        tile[c] = tid
    tiles[tid] = cells
for y0 in range(0, H, 4):
    for x0 in range(0, W, 3):                       # row A: horizontal 3x1 bricks
        put(('h', x0, y0), [(x0 + i, y0) for i in range(3)])
    for x0 in range(W):                             # band B: vertical 1x3 bricks
        put(('v', x0, y0 + 1), [(x0, y0 + 1 + j) for j in range(3)])
check("[A] the 1x3 bricks cover the torus exactly once (a tiling by one convex tile)",
      len(tile) == W * H and all(len(c) == 3 for c in tiles.values()))
nbrs = {t: set() for t in tiles}
for (x, y), t in tile.items():
    for dx, dy in ((1, 0), (0, 1)):                 # shared unit edge = positive-length contact
        u = tile[((x + dx) % W, (y + dy) % H)]
        if u != t:
            nbrs[t].add(u); nbrs[u].add(t)
counts = sorted({(t[0], len(n)) for t, n in nbrs.items()})
print("    edge-neighbour counts by brick type:", counts)
mx = max(len(n) for n in nbrs.values())
check("[A] some tile has more than 6 edge-neighbours (found %d): equal split gives 1/%d < 1/6" % (mx, mx), mx > 6)
avg = sum(len(n) for n in nbrs.values()) / len(nbrs)
check("[A] mean neighbour count is still <= 6 (%.2f): the bound that survives is on the average" % avg, avg <= 6)
# control: the regular hexagonal tiling has exactly 6 for every tile (axial coords on a torus)
N = 6
hexn = {(q, r): {((q + a) % N, (r + b) % N) for a, b in ((1,0),(-1,0),(0,1),(0,-1),(1,-1),(-1,1))} for q in range(N) for r in range(N)}
check("[A] control: every hexagon in the regular tiling has exactly 6", all(len(v) == 6 for v in hexn.values()))

# ---------- [B] Q1 ----------
def lean_statement(n, others):           # "d != d+k for the other edge directions k"
    return all((d % n) != ((d + k) % n) for d in range(n) for k in others)
def straight_exists(n, others):          # arriving along the edge whose outgoing ray is d, travel direction is d + n/2
    return any(((d + n // 2) % n) == ((d + k) % n) for d in range(n) for k in others)
check("[B] Lean statement as written holds for the hexagonal vertex (Fin 6, others +2,+4)", lean_statement(6, (2, 4)))
check("[B] the same form of statement ALSO holds for the square grid (Fin 4, others +1,+2,+3)", lean_statement(4, (1, 2, 3)))
check("[B] yet the square grid has a straight continuation", straight_exists(4, (1, 2, 3)))
check("[B] and the hexagonal vertex has none (d+3 not in {d+2, d+4})", not straight_exists(6, (2, 4)))
print("    => 'd != d+2 and d != d+4' says the other two edges differ from the arrival edge;")
print("       it does not distinguish hexagon from square. The statement that does is d+3 != d+2 and d+3 != d+4.")
# coordinates: honeycomb vertices and edges, test every pair of edges at every vertex for collinearity
def honeycomb(n=6):
    V = {}; E = set()
    a1 = (math.sqrt(3), 0.0); a2 = (math.sqrt(3) / 2, 1.5)
    for i, j in itertools.product(range(n), repeat=2):
        ox = i * a1[0] + j * a2[0]; oy = i * a1[1] + j * a2[1]
        A = (round(ox, 9), round(oy, 9)); B = (round(ox, 9), round(oy + 1.0, 9))
        E.add((A, B))
        for (di, dj) in ((0, -1), (1, -1)):       # B(i,j) also joins A(i,j+1), A(i-1,j+1): store from A side
            pass
        for (di, dj) in ((0, 1), (-1, 1)):
            ii, jj = i + di, j + dj
            if 0 <= ii < n and 0 <= jj < n:
                A2 = (round(ii * a1[0] + jj * a2[0], 9), round(ii * a1[1] + jj * a2[1], 9))
                E.add((B, A2))
    return E
def collinear_pairs(E):
    inc = {}
    for p, q in E:
        inc.setdefault(p, []).append(q); inc.setdefault(q, []).append(p)
    n = 0; deg3 = 0
    for v, ns in inc.items():
        deg3 += (len(ns) == 3)
        for p, q in itertools.combinations(ns, 2):
            ax, ay = p[0] - v[0], p[1] - v[1]; bx, by = q[0] - v[0], q[1] - v[1]
            if abs(ax * by - ay * bx) < 1e-7 and ax * bx + ay * by < 0: n += 1
    return n, deg3
E = honeycomb(); n, deg3 = collinear_pairs(E)
edge_len_ok = all(abs(math.dist(p, q) - 1.0) < 1e-6 for p, q in E)
check("[B] honeycomb built correctly (unit edges, %d interior degree-3 vertices)" % deg3, edge_len_ok and deg3 > 20)
check("[B] honeycomb: no vertex has two collinear incident edges (0 found)", n == 0)
S = {((x, y), (x + 1, y)) for x in range(5) for y in range(6)} | {((x, y), (x, y + 1)) for x in range(6) for y in range(5)}
check("[B] control: the square grid has collinear pairs (%d found)" % collinear_pairs(S)[0], collinear_pairs(S)[0] > 0)

# ---------- [C] bookkeeping ----------
page = (HERE / "ch18-seismic-lattice.html").read_text(encoding="utf8")
lean = (HERE.parent / "Orthogenesis/Architecture/SeismicLattice.lean").read_text(encoding="utf8")
txt = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", page))
thms = re.findall(r"^theorem\s+(\S+)", lean, re.M)
code = re.sub(r"(?s)/-.*?-/", "", lean); code = re.sub(r"--.*", "", code)
print("    Lean: %d theorems; 'sorry' in code (comments stripped): %d" % (len(thms), len(re.findall(r"\bsorry\b", code))))
check("[C] Lean file has no sorry in code", not re.search(r"\bsorry\b", code))
print("    page says Q1 is 'left open' in sec 18.2:", "left open, because a faithful proof" in txt)
print("    page table marks no_straight_continuation proved:", bool(re.search(r"no_straight_continuation\s*✓ proved", txt)))
print("    page says 'three hard obligations are named and open':", "three hard obligations are named and open" in txt)
print("    page 'What is not claimed' still lists Q1 and Q2 as unproved:", "(Q1)" in txt and "(Q2)" in txt)
print("    Lean closing summary still says 'Q2 response-spectrum detuning (sorry)':", "detuning (sorry)" in lean)
print("    placeholder with conclusion True:", [t for t in thms if "placeholder" in t])
sys.exit(1 if fails else 0)
