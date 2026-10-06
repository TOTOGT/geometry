"""Is SRep(Qbar,d) a quaternionic subspace, and does mu_R land in k^b?  (needed for Prop 4.3 / 3-Sasakian reduction)
Standard signed space (all J_i = identity, real forms), so sigma(v)_a = s(a) * (v_{tau a})^T.
Test quiver: (A~_2, v-a), n=2: vertices 1 (fixed), 2, t2 ; arrows a:1->2, ta:t2->1 (tau a = ta), f:2->t2 (fixed, sign s).
Random dims d=(2,3,3) (symmetric: d_2 = d_t2).  Doubled arrows a*, ta*, f*.
J (quaternionic) on T*Rep: (Jv)_a = -(v_{a*})^dagger, (Jv)_{a*} = (v_a)^dagger  (antilinear)."""
import numpy as np
rng = np.random.default_rng(0)
d = {'1': 2, '2': 3, 't2': 3}
arrows = {'a': ('1', '2'), 'ta': ('t2', '1'), 'f': ('2', 't2')}      # name: (tail, head)
tau = {'a': 'ta', 'ta': 'a', 'f': 'f'}
def rand(t, h): return rng.normal(size=(d[h], d[t])) + 1j*rng.normal(size=(d[h], d[t]))
def random_rep():
    v = {}
    for a, (t, h) in arrows.items():
        v[a] = rand(t, h); v[a+'*'] = rand(h, t)
    return v
def sigma(v, s):
    out = {}
    for a in arrows:
        out[a] = s[a] * v[tau[a]].T
        out[a+'*'] = s[a] * v[tau[a]+'*'].T
    return out
def Jq(v):
    out = {}
    for a in arrows:
        out[a] = -v[a+'*'].conj().T
        out[a+'*'] = v[a].conj().T
    return out
def mu(v, real):
    m = {i: np.zeros((d[i], d[i]), complex) for i in d}
    for a, (t, h) in arrows.items():
        x, y = v[a], v[a+'*']
        if real:
            m[h] += x @ x.conj().T - y.conj().T @ y
            m[t] += y @ y.conj().T - x.conj().T @ x
        else:
            m[h] += x @ y
            m[t] -= y @ x
    return m
taui = {'1': '1', '2': 't2', 't2': '2'}
def in_kb(m):   # varsigma-fixed: theta_i = -(theta_{tau i})^T
    return max(np.abs(m[i] + m[taui[i]].T).max() for i in d)
def dist(u, w): return max(np.abs(u[k] - w[k]).max() for k in u)
for sf in (+1, -1):
    s = {'a': 1, 'ta': 1, 'f': sf}
    v = random_rep(); sv = sigma(v, s)
    v = {k: (v[k] + sv[k]) / 2 for k in v}                       # project to SRep
    assert dist(sigma(v, s), v) < 1e-12
    print(f"s(f)={sf:+d}: sigma∘J - J∘sigma = {dist(sigma(Jq(v), s), Jq(sigma(v, s))):.1e};"
          f"  J(SRep) in SRep: {dist(sigma(Jq(v), s), Jq(v)):.1e};"
          f"  mu_C in k^b: {in_kb(mu(v, False)):.1e};  mu_R in k^b: {in_kb(mu(v, True)):.1e}")
