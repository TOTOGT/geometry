"""Computed worked examples for Book XXVII chapters 4-7 (databases, operating systems,
algorithms, programming languages). Imported by b27-verify.py; the pages quote these numbers.
Standard library only."""
import sqlite3, heapq
from collections import deque
from fractions import Fraction as F

# ---------------- Chapter 4: databases ----------------
def fd_closure(attrs, fds):
    c = set(attrs); ch = True
    while ch:
        ch = False
        for l, r in fds:
            if set(l) <= c and not set(r) <= c:
                c |= set(r); ch = True
    return "".join(sorted(c))
FDS = [("A", "B"), ("B", "C"), ("CD", "E")]
R_ATTRS = "ABCDE"
def candidate_keys():
    from itertools import combinations
    keys = []
    for n in range(1, len(R_ATTRS) + 1):
        for comb in combinations(R_ATTRS, n):
            if fd_closure(comb, FDS) == R_ATTRS and not any(set(k) <= set(comb) for k in keys):
                keys.append("".join(comb))
    return keys

def sql_demo():
    db = sqlite3.connect(":memory:"); c = db.cursor()
    c.executescript("""
    CREATE TABLE dept(id INTEGER PRIMARY KEY, name TEXT);
    CREATE TABLE emp(id INTEGER PRIMARY KEY, name TEXT, dept_id INTEGER REFERENCES dept(id), salary INTEGER);
    INSERT INTO dept VALUES (1,'Sales'),(2,'Engineering'),(3,'Legal');
    INSERT INTO emp VALUES (1,'Ana',1,50000),(2,'Bo',2,80000),(3,'Cy',2,90000),(4,'Di',1,60000),(5,'Ed',NULL,40000);
    """)
    out = {}
    out["group"] = c.execute("""SELECT d.name, COUNT(e.id), AVG(e.salary) FROM dept d
        LEFT JOIN emp e ON e.dept_id=d.id GROUP BY d.id ORDER BY d.id""").fetchall()
    out["inner"] = c.execute("SELECT e.name, d.name FROM emp e JOIN dept d ON e.dept_id=d.id ORDER BY e.id").fetchall()
    out["having"] = c.execute("""SELECT d.name FROM dept d JOIN emp e ON e.dept_id=d.id
        GROUP BY d.id HAVING AVG(e.salary) > 70000""").fetchall()
    # atomicity: a transaction that is rolled back leaves no trace
    before = c.execute("SELECT COUNT(*) FROM emp").fetchone()[0]
    c.execute("BEGIN"); c.execute("INSERT INTO emp VALUES (6,'Flo',3,70000)")
    inside = c.execute("SELECT COUNT(*) FROM emp").fetchone()[0]
    db.rollback()
    after = c.execute("SELECT COUNT(*) FROM emp").fetchone()[0]
    out["atomic"] = (before, inside, after)
    return out

def conflict_serializable(schedule):
    """schedule: list of (txn, 'r'|'w', item). Returns (edges, acyclic)."""
    edges = set()
    for i, (t1, o1, x1) in enumerate(schedule):
        for t2, o2, x2 in schedule[i + 1:]:
            if t1 != t2 and x1 == x2 and "w" in (o1, o2):
                edges.add((t1, t2))
    nodes = {t for t, _, _ in schedule}
    # cycle check by Kahn
    indeg = {n: 0 for n in nodes}
    for a, b in edges: indeg[b] += 1
    q = deque(n for n in nodes if indeg[n] == 0); seen = 0
    while q:
        n = q.popleft(); seen += 1
        for a, b in edges:
            if a == n:
                indeg[b] -= 1
                if indeg[b] == 0: q.append(b)
    return sorted(edges), seen == len(nodes)
S1 = [(1,'r','X'),(1,'w','X'),(2,'r','X'),(2,'w','X'),(1,'r','Y'),(1,'w','Y'),(2,'r','Y'),(2,'w','Y')]
S2 = [(1,'r','X'),(2,'r','X'),(1,'w','X'),(2,'w','X')]

# ---------------- Chapter 5: operating systems ----------------
PROCS = [("P1", 0, 5), ("P2", 1, 3), ("P3", 2, 8), ("P4", 3, 6)]
def sched_metrics(finish):
    wt = {p: finish[p] - a - b for p, a, b in PROCS}
    tat = {p: finish[p] - a for p, a, b in PROCS}
    n = len(PROCS)
    return F(sum(wt.values()), n), F(sum(tat.values()), n)
def fcfs():
    t = 0; fin = {}
    for p, a, b in sorted(PROCS, key=lambda x: x[1]):
        t = max(t, a) + b; fin[p] = t
    return sched_metrics(fin)
def sjf():
    t = 0; fin = {}; left = list(PROCS)
    while left:
        ready = [x for x in left if x[1] <= t] or [min(left, key=lambda x: x[1])]
        p, a, b = min(ready, key=lambda x: (x[2], x[1]))
        t = max(t, a) + b; fin[p] = t; left.remove((p, a, b))
    return sched_metrics(fin)
def rr(q=4):
    t = 0; rem = {p: b for p, a, b in PROCS}; fin = {}
    arr = {p: a for p, a, b in PROCS}; queue = deque(); added = set()
    def admit(upto):
        for p, a, b in sorted(PROCS, key=lambda x: x[1]):
            if a <= upto and p not in added:
                queue.append(p); added.add(p)
    admit(0)
    while queue or len(added) < len(PROCS):
        if not queue:
            t = min(a for p, a, b in PROCS if p not in added); admit(t); continue
        p = queue.popleft(); run = min(q, rem[p]); t += run; rem[p] -= run
        admit(t)
        if rem[p] > 0: queue.append(p)
        else: fin[p] = t
    return sched_metrics(fin)
REFS = [7,0,1,2,0,3,0,4,2,3,0,3,2,1,2,0,1,7,0,1]
def fifo_faults(refs, k):
    frames = deque(); f = 0
    for r in refs:
        if r not in frames:
            f += 1
            if len(frames) == k: frames.popleft()
            frames.append(r)
    return f
def lru_faults(refs, k):
    frames = []; f = 0
    for r in refs:
        if r in frames: frames.remove(r)
        else:
            f += 1
            if len(frames) == k: frames.pop(0)
        frames.append(r)
    return f
def opt_faults(refs, k):
    frames = []; f = 0
    for i, r in enumerate(refs):
        if r in frames: continue
        f += 1
        if len(frames) < k: frames.append(r); continue
        def nxt(x):
            for j in range(i + 1, len(refs)):
                if refs[j] == x: return j
            return 10**9
        frames.remove(max(frames, key=nxt)); frames.append(r)
    return f
AVAIL = (3, 3, 2)
ALLOC = {"P0": (0,1,0), "P1": (2,0,0), "P2": (3,0,2), "P3": (2,1,1), "P4": (0,0,2)}
MAXD = {"P0": (7,5,3), "P1": (3,2,2), "P2": (9,0,2), "P3": (2,2,2), "P4": (4,3,3)}
def banker():
    work = list(AVAIL); done = []; need = {p: tuple(m - a for m, a in zip(MAXD[p], ALLOC[p])) for p in ALLOC}
    left = list(ALLOC)
    progress = True
    while left and progress:
        progress = False
        for p in list(left):
            if all(n <= w for n, w in zip(need[p], work)):
                work = [w + a for w, a in zip(work, ALLOC[p])]; done.append(p); left.remove(p); progress = True
    return need, done, not left
PAGE = 4096
def translate(vaddr): return vaddr // PAGE, vaddr % PAGE

# ---------------- Chapter 6: algorithms ----------------
def merge_sort_comparisons(a):
    cnt = [0]
    def ms(x):
        if len(x) <= 1: return x
        m = len(x) // 2; l, r = ms(x[:m]), ms(x[m:]); out = []; i = j = 0
        while i < len(l) and j < len(r):
            cnt[0] += 1
            if l[i] <= r[j]: out.append(l[i]); i += 1
            else: out.append(r[j]); j += 1
        return out + l[i:] + r[j:]
    return ms(list(a)), cnt[0]
MS_INPUT = [38, 27, 43, 3, 9, 82, 10, 5]
def binary_search_steps(a, x):
    lo, hi, steps = 0, len(a) - 1, 0
    while lo <= hi:
        steps += 1; mid = (lo + hi) // 2
        if a[mid] == x: return mid, steps
        if a[mid] < x: lo = mid + 1
        else: hi = mid - 1
    return -1, steps
def hash_chains(keys, m):
    t = [[] for _ in range(m)]
    for k in keys: t[k % m].append(k)
    return t
HASH_KEYS = [50, 700, 76, 85, 92, 73, 101]
GRAPH = {"S": [("A", 7), ("B", 2)], "A": [("C", 1)], "B": [("A", 3), ("C", 8), ("D", 5)], "C": [("T", 4)], "D": [("C", 2), ("T", 9)], "T": []}
def dijkstra(g, s):
    dist = {v: float("inf") for v in g}; dist[s] = 0; pq = [(0, s)]; prev = {}
    while pq:
        d, u = heapq.heappop(pq)
        if d > dist[u]: continue
        for v, w in g[u]:
            if d + w < dist[v]: dist[v] = d + w; prev[v] = u; heapq.heappush(pq, (dist[v], v))
    return dist, prev
def path_to(prev, t):
    p = [t]
    while p[-1] in prev: p.append(prev[p[-1]])
    return p[::-1]
def kmp_table(p):
    t = [0] * len(p); k = 0
    for i in range(1, len(p)):
        while k and p[i] != p[k]: k = t[k - 1]
        if p[i] == p[k]: k += 1
        t[i] = k
    return t
def kmp_search(text, p):
    t = kmp_table(p); k = 0; hits = []
    for i, ch in enumerate(text):
        while k and ch != p[k]: k = t[k - 1]
        if ch == p[k]: k += 1
        if k == len(p): hits.append(i - k + 1); k = t[k - 1]
    return hits

# ---------------- Chapter 7: programming languages ----------------
def tokenize(s):
    out = []; i = 0
    while i < len(s):
        ch = s[i]
        if ch.isspace(): i += 1
        elif ch.isdigit():
            j = i
            while j < len(s) and s[j].isdigit(): j += 1
            out.append(int(s[i:j])); i = j
        else: out.append(ch); i += 1
    return out
def parse(tokens):
    pos = [0]
    def peek(): return tokens[pos[0]] if pos[0] < len(tokens) else None
    def eat(): pos[0] += 1; return tokens[pos[0] - 1]
    def expr():
        n = term()
        while peek() in ("+", "-"): op = eat(); n = (op, n, term())
        return n
    def term():
        n = factor()
        while peek() in ("*", "/"): op = eat(); n = (op, n, factor())
        return n
    def factor():
        t = eat()
        if t == "(": n = expr(); eat(); return n
        return t
    return expr()
def show(n):
    return str(n) if isinstance(n, int) else "(" + n[0] + " " + show(n[1]) + " " + show(n[2]) + ")"
def ev(n):
    if isinstance(n, int): return n
    a, b = ev(n[1]), ev(n[2])
    return {"+": a + b, "-": a - b, "*": a * b, "/": a // b}[n[0]]
EXPR = "2 + 3 * (4 - 1)"
def eval_strategies():
    """f(x) = x + x, argument is an 'expensive' expression counted when evaluated."""
    count = {"v": 0, "n": 0, "need": 0}
    def arg(key): count[key] += 1; return 21
    # by value: argument evaluated once before the call
    x = arg("v"); by_value = x + x
    # by name: re-evaluated at each use
    by_name = arg("n") + arg("n")
    # by need: evaluated at first use, then cached
    cache = []
    def thunk():
        if not cache: cache.append(arg("need"))
        return cache[0]
    by_need = thunk() + thunk()
    return count, (by_value, by_name, by_need)
def counter_closure():
    def make():
        n = 0
        def inc():
            nonlocal n; n += 1; return n
        return inc
    a, b = make(), make()
    return [a(), a(), b(), a()]

# ---------------- Chapters 8-12: ML, SE, HCI, security, capstone ----------------
import math, hashlib
ML_X = [1, 2, 3, 4, 5]; ML_Y = [2, 4, 5, 4, 5]
def linreg(x, y):
    n = len(x); mx = F(sum(x), n); my = F(sum(y), n)
    sxy = sum((a - mx) * (b - my) for a, b in zip(x, y)); sxx = sum((a - mx) ** 2 for a in x)
    w = sxy / sxx; b0 = my - w * mx
    sse = sum((b - (b0 + w * a)) ** 2 for a, b in zip(x, y))
    sst = sum((b - my) ** 2 for b in y)
    return w, b0, 1 - sse / sst
def gd_step(w, b, x, y, lr):
    n = len(x); gw = sum(2 * ((w * a + b) - t) * a for a, t in zip(x, y)) / n
    gb = sum(2 * ((w * a + b) - t) for a, t in zip(x, y)) / n
    return w - lr * gw, b - lr * gb
CONF = dict(tp=40, fp=10, fn=20, tn=30)
def clf_metrics(tp, fp, fn, tn):
    n = tp + fp + fn + tn
    p = F(tp, tp + fp); r = F(tp, tp + fn)
    return dict(acc=F(tp + tn, n), prec=p, rec=r, f1=2 * p * r / (p + r))
KM_PTS = [1, 2, 9, 10, 20]
def kmeans_1d(pts, cents, iters=10):
    cents = list(map(float, cents))
    for _ in range(iters):
        cl = [[] for _ in cents]
        for p in pts: cl[min(range(len(cents)), key=lambda i: abs(p - cents[i]))].append(p)
        new = [sum(c) / len(c) if c else cents[i] for i, c in enumerate(cl)]
        if new == cents: break
        cents = new
    return cents, cl
def cyclomatic(edges, nodes, comps=1): return edges - nodes + 2 * comps
CFG_E, CFG_N = 9, 8   # if/else inside a while loop with a break-out
def cocomo_organic(kloc): return 2.4 * kloc ** 1.05, 2.5 * (2.4 * kloc ** 1.05) ** 0.38
def fitts(a, b, d, w): return a + b * math.log2(d / w + 1)
def hick(b, n): return b * math.log2(n + 1)
def entropy_bits(alphabet, length): return length * math.log2(alphabet)
def sha256_hex(s): return hashlib.sha256(s.encode()).hexdigest()
def bit_diff(h1, h2): return bin(int(h1, 16) ^ int(h2, 16)).count("1")
def risk_score(likelihood, impact): return likelihood * impact
CAP_WEIGHTS = dict(discussion=15, portfolio=34, identity=6, report=20, presentation=25)
CFG_EDGES = [(1,2),(2,3),(2,7),(3,4),(3,5),(4,6),(5,6),(6,2),(7,8)]
CFG_NODES = 8

# ---------------- Chapter 0 / 0b: pre-MSIT math and cryptography math ----------------
from math import comb, factorial, gcd
def implies_table():
    return [(p, q, (not p) or q) for p in (True, False) for q in (True, False)]
def bayes(prev, sens, fpr):
    tp = prev * sens; fp = (1 - prev) * fpr
    return tp / (tp + fp)
def matmul(A, B): return [[sum(a * b for a, b in zip(r, c)) for c in zip(*B)] for r in A]
def det2(M): return M[0][0] * M[1][1] - M[0][1] * M[1][0]
def mse_grad_w(w, b, x, y):
    return sum(2 * ((w * a + b) - t) * a for a, t in zip(x, y)) / len(x)
def numeric_grad_w(w, b, x, y, h=1e-6):
    f = lambda ww: sum(((ww * a + b) - t) ** 2 for a, t in zip(x, y)) / len(x)
    return (f(w + h) - f(w - h)) / (2 * h)
def handshake_ok(deg): return sum(deg) % 2 == 0 and sum(deg) // 2
def ext_gcd(a, b):
    if b == 0: return a, 1, 0
    g, x, y = ext_gcd(b, a % b); return g, y, x - (a // b) * y
def mod_inv(a, m):
    g, x, _ = ext_gcd(a, m)
    return x % m if g == 1 else None
def phi(n): return sum(1 for k in range(1, n + 1) if gcd(k, n) == 1)
def modexp_steps(base, exp, mod):
    r, b, mults = 1, base % mod, 0
    while exp:
        if exp & 1: r = r * b % mod; mults += 1
        exp >>= 1
        if exp: b = b * b % mod; mults += 1
    return r, mults
RSA = dict(p=61, q=53, e=17, m=65)
def rsa_toy():
    p, q, e, m = RSA["p"], RSA["q"], RSA["e"], RSA["m"]
    n = p * q; lam = (p - 1) * (q - 1); d = mod_inv(e, lam)
    cph = pow(m, e, n); back = pow(cph, d, n)
    return n, lam, d, cph, back
DH = dict(p=23, g=5, a=6, b=15)
def dh_toy():
    p, g, a, b = DH["p"], DH["g"], DH["a"], DH["b"]
    A, B = pow(g, a, p), pow(g, b, p)
    return A, B, pow(B, a, p), pow(A, b, p)
def birthday(n, days=365):
    p = 1.0
    for i in range(n): p *= (days - i) / days
    return 1 - p
def xor_demo():
    m = 0b01001000; k = 0b10110101; c = m ^ k
    return m, k, c, c ^ k
