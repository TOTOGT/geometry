#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Book 33 planning: which closure-type properties do dynamics-induced operators on sets of states have?
Two parts, standard library only.
 A. For ANY deterministic map f on a finite set, tabulate four operators on subsets (always, eventually-always,
    ever, backward saturation) against: monotone, extensive, deflationary, idempotent, preserves finite meets.
    (Random finite maps; this checks the general table, it is not about the dm3 toy.)
 B. On the radial toy r' = r(1 - r^2) (Volume I's drift in rho = r - 1), with return map P = time-2*pi flow:
    eventually-always sends any neighbourhood of Gamma (r = 1) to the whole line r > 0, and sends a set away
    from Gamma to the empty set. Exact flow: r(t) = r0 / sqrt(r0^2 + (1 - r0^2) exp(-2t))."""
import math, random, itertools
random.seed(33)
def subsets(n, k):
    for _ in range(k):
        yield frozenset(i for i in range(n) if random.random() < .5)
def ops(f, n):
    N = 2 * n + 2
    def pre(S, m):  # points whose m-th iterate lies in S
        res = set()
        for x in range(n):
            y = x
            for _ in range(m): y = f[y]
            if y in S: res.add(x)
        return frozenset(res)
    def always(S): return frozenset.intersection(*[pre(S, m) for m in range(N)])
    def ever(S): return frozenset.union(*[pre(S, m) for m in range(N)])
    def ev_always(S):  # eventually always: iterate lies in S for all m >= some m0 (orbits are eventually periodic)
        return frozenset(x for x in range(n) if _ea(f, x, S, N))
    return {'always': always, 'eventually-always': ev_always, 'ever': ever}
def _ea(f, x, S, N):
    y = x
    for _ in range(N): y = f[y]          # past the transient
    seen = []
    for _ in range(N):
        seen.append(y); y = f[y]
    return all(z in S for z in seen)
def table(trials=60, n=7):
    res = {}
    for _ in range(trials):
        f = [random.randrange(n) for _ in range(n)]
        O = ops(f, n); O['backward-saturation'] = O['ever']
        U = frozenset(range(n))
        subs = list(subsets(n, 12))
        for name, op in O.items():
            r = res.setdefault(name, dict(monotone=True, extensive=True, deflationary=True, idempotent=True, meets=True))
            for S in subs:
                if not S <= U: continue
                a = op(S)
                r['extensive'] &= S <= a
                r['deflationary'] &= a <= S
                r['idempotent'] &= op(a) == a
            for S, T in itertools.product(subs[:6], subs[6:12]):
                r['meets'] &= op(S & T) == op(S) & op(T)
                if S <= T: r['monotone'] &= op(S) <= op(T)
    return res
def P(r0, T=2 * math.pi): return r0 / math.sqrt(r0 * r0 + (1 - r0 * r0) * math.exp(-2 * T))
def steps_to_stay(r0, a, b, cap=2000):
    r = r0
    for n in range(cap):
        if a < r < b: return n
        r = P(r)
    return None
def main():
    t = table()
    print('A. general finite maps (a property is listed True only if it held in every random trial)')
    for k, v in t.items(): print(f'   {k:20s}', ' '.join(f'{p}={v[p]}' for p in v))
    exp = {'always': dict(monotone=True, extensive=False, deflationary=True, idempotent=True, meets=True),
           'eventually-always': dict(monotone=True, extensive=False, deflationary=False, idempotent=True, meets=True),
           'ever': dict(monotone=True, extensive=True, deflationary=False, idempotent=True, meets=False)}
    ok = all(t[k][p] == exp[k][p] for k in exp for p in exp[k] if exp[k][p] is True or t[k][p] is True)
    print('   matches the expected table (no operator is both extensive and meet-preserving):', ok)
    nuc = [k for k, v in t.items() if v['extensive'] and v['meets'] and v['idempotent']]
    print('   operators that are nuclei (extensive, idempotent, meet-preserving):', nuc)
    print('B. radial toy, Gamma = {r = 1}')
    pts = [10 ** (e / 10) for e in range(-30, 31)]
    for d in (0.5, 0.1, 0.01):
        a, b = 1 - d, 1 + d
        # the interval is forward invariant: P is monotone, fixes 1, and moves points toward 1
        inv = P(a) > a and P(b) < b
        n = [steps_to_stay(x, a, b) for x in pts]
        print(f'   U=({a:.2f},{b:.2f}) forward invariant={inv}; all {len(pts)} test points enter and stay: {all(v is not None for v in n)}; max steps {max(n)}')
    a, b = 1.5, 2.0
    stays = 0
    for x in pts:
        r = x; inside_forever = True
        for _ in range(300):
            r = P(r)
        inside_forever = a < r < b
        stays += inside_forever
    print(f'   V=({a},{b}) away from Gamma: points whose iterate is in V after 300 returns: {stays} of {len(pts)} (so eventually-always(V) is empty on this grid)')
    allok = ok and not nuc
    print('ALL CHECKS PASSED' if allok else 'CHECK FAILED')
if __name__ == '__main__': main()
