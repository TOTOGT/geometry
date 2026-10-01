#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Book 33 planning: Baaz's Kripke semantics for da Costa's logic C-omega, tested, then applied to the dm3 radial toy.

Semantics implemented exactly as printed in Baskent (hal-01094786, 2014), section 1, the Baaz clauses:
  model: partial order <=, valuation of atoms by UPSETS, T(w) = set of negated formulas, monotone in <=.
  w |= p        iff every v >= w has v |= p          (atoms are upsets, so this is w in V(p))
  w |= a & b, a | b : as usual
  w |= a > b    iff for all v >= w, v |= a implies v |= b
  w |= ~a       iff ~a in T(w), or some v <= w has v |/= a          (negation looks BACKWARD)
  w |= ~~..a    : the printed clause for iterated negation.
Part 1 checks the implementation against the paper: axioms 1-10 valid, explosion and the substitution
principle for negated formulas not valid. Part 2 uses the reachability order of the radial toy
r' = r(1 - r^2) (Volume I's drift in rho = r - 1) with T empty, so any glut comes from the order alone."""
import itertools, math, random
random.seed(7)
P_, Q_, R_ = ('p',), ('q',), ('r',)
def N(f): return ('not', f)
def A(a, b): return ('and', a, b)
def O(a, b): return ('or', a, b)
def I(a, b): return ('imp', a, b)
class Model:
    def __init__(s, n, leq, val, T): s.n, s.leq, s.val, s.T, s.memo = n, leq, val, T, {}
    def up(s, w): return [v for v in range(s.n) if s.leq[w][v]]
    def down(s, w): return [v for v in range(s.n) if s.leq[v][w]]
    def sat(s, w, f):
        k = (w, f)
        if k in s.memo: return s.memo[k]
        t = f[0]
        if t in ('p', 'q', 'r'): r = all(w2 in s.val[t] for w2 in s.up(w))
        elif t == 'and': r = s.sat(w, f[1]) and s.sat(w, f[2])
        elif t == 'or': r = s.sat(w, f[1]) or s.sat(w, f[2])
        elif t == 'imp': r = all((not s.sat(v, f[1])) or s.sat(v, f[2]) for v in s.up(w))
        else:
            depth, base = 0, f
            while base[0] == 'not': depth += 1; base = base[1]
            def neg(g, m):
                for _ in range(m): g = N(g)
                return g
            if depth == 1: r = (f in s.T[w]) or any(not s.sat(v, base) for v in s.down(w))
            else: r = ((f in s.T[w]) and s.sat(w, neg(base, depth - 2))) or any(not s.sat(v, neg(base, depth - 1)) for v in s.down(w))
        s.memo[k] = r; return r
def rand_model(n=5):
    leq = [[i == j for j in range(n)] for i in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            if random.random() < .45: leq[i][j] = True      # i < j in index order: a partial order after closure
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if leq[i][k] and leq[k][j]: leq[i][j] = True
    def upset_from(seed):
        S = set(seed)
        return {v for u in S for v in range(n) if leq[u][v]} | S
    val = {a: upset_from([w for w in range(n) if random.random() < .35]) for a in ('p', 'q', 'r')}
    pool = [N(P_), N(Q_), N(R_), N(N(P_)), N(N(Q_)), N(A(P_, P_)), N(O(P_, Q_))]
    T = [set() for _ in range(n)]
    for f in pool:
        S = upset_from([w for w in range(n) if random.random() < .25])
        for w in S: T[w].add(f)                                  # monotone: each formula's worlds form an upset
    return Model(n, leq, val, T)
AX = {
 1: I(P_, I(Q_, P_)), 2: I(I(P_, Q_), I(I(P_, I(Q_, R_)), I(P_, R_))), 3: I(A(P_, Q_), P_), 4: I(A(P_, Q_), Q_),
 5: I(P_, I(Q_, A(P_, Q_))), 6: I(P_, O(P_, Q_)), 7: I(Q_, O(P_, Q_)),
 8: I(I(P_, R_), I(I(Q_, R_), I(O(P_, Q_), R_))), 9: O(P_, N(P_)), 10: I(N(N(P_)), P_)}
NOT_VALID = {'explosion p>(~p>q)': I(P_, I(N(P_), Q_)), 'no-contradiction ~(p&~p)': N(A(P_, N(P_))),
             'substitution ~p <-> ~(p&p) (one direction)': I(N(P_), N(A(P_, P_)))}
def part1(trials=1500):
    models = [rand_model() for _ in range(trials)]
    ok = True
    for k, f in AX.items():
        bad = sum(1 for m in models for w in range(m.n) if not m.sat(w, f))
        print(f'   axiom {k:2d} valid on all {trials} random models: {bad == 0}'); ok &= bad == 0
    mp_bad = 0
    for m in models:                                           # modus ponens preserves truth at every world
        for w in range(m.n):
            for a, b in ((P_, Q_), (O(P_, Q_), N(R_))):
                if m.sat(w, a) and m.sat(w, I(a, b)) and not m.sat(w, b): mp_bad += 1
    print('   modus ponens preserves truth:', mp_bad == 0); ok &= mp_bad == 0
    for name, f in NOT_VALID.items():
        cnt = sum(1 for m in models for w in range(m.n) if not m.sat(w, f))
        print(f'   {name}: refuted in {cnt} world(s) -> not valid: {cnt > 0}'); ok &= cnt > 0
    glut = sum(1 for m in models for w in range(m.n) if m.sat(w, A(P_, N(P_))))
    print(f'   gluts (p and ~p at one world) occur with T arbitrary: {glut > 0} ({glut} worlds)')
    return ok
# ---- Part 2: the toy. Exact flow of r' = r(1-r^2): r(t) = r0 / sqrt(r0^2 + (1-r0^2) exp(-2t))
def flow(r0, t):
    d = r0 * r0 + (1 - r0 * r0) * math.exp(-2 * t)
    return None if d <= 0 else r0 / math.sqrt(d)
def part2():
    ok = True
    h, K = 0.5, 80
    seeds = [0.05, 0.2, 0.5, 0.9, 1.0, 1.1, 1.5, 3.0]
    for (a, b) in ((0.9, 1.1), (0.99, 1.01), (0.5, 2.0)):
        # frame: one chain per seed r0 (states = r(k h), k = -K..K while defined); Gamma (r = 1) is one state
        states, leq, chain_of = [], {}, []
        for r0 in seeds:
            ch = []
            for k in range(-K, K + 1):
                r = flow(r0, k * h)
                if r is not None and 1e-12 < r < 1e12: ch.append(r)
            chain_of.append(ch)
        n = sum(len(c) for c in chain_of); idx = 0; L = [[False] * n for _ in range(n)]; spans = []
        for ch in chain_of:
            spans.append((idx, idx + len(ch)))
            for i in range(len(ch)):
                for j in range(i, len(ch)): L[idx + i][idx + j] = True   # earlier state <= later state
            idx += len(ch)
        rs = [r for ch in chain_of for r in ch]
        inU = {i for i, r in enumerate(rs) if a < r < b}
        up = {v for u in inU for v in range(n) if L[u][v]}
        m = Model(n, L, {'p': up, 'q': set(), 'r': set()}, [set() for _ in range(n)])
        glut = {i for i in range(n) if m.sat(i, A(P_, N(P_)))}
        # prediction: p holds where the whole future stays in U (forward invariant, so = in U); a glut where some earlier state is outside
        pred = {i for i in inU if any(rs[j] <= a or rs[j] >= b for j in range(n) if L[j][i])}
        g0, g1 = spans[seeds.index(1.0)]; gamma = set(range(g0, g1))                  # the orbit that IS Gamma (r0 = 1)
        near = {i for i in range(n) if i not in gamma and abs(rs[i] - 1) < 1e-9 and i in glut}
        print(f'   U=({a},{b}): states {n}; p true at {len(up)}; glut at {len(glut)}; glut set equals "in U with an earlier state outside U": {glut == pred}; '
              f'Gamma states glut-free: {not (glut & gamma)}; states of other orbits within 1e-9 of Gamma that are gluts: {len(near)}')
        ok &= glut == pred and not (glut & gamma)
    return ok
if __name__ == '__main__':
    print('1. Baaz semantics against the paper'); a = part1()
    print('2. dm3 radial toy: reachability order, T empty'); b = part2()
    print('ALL CHECKS PASSED' if a and b else 'CHECK FAILED')
