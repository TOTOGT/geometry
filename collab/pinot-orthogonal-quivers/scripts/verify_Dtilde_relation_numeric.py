"""Independent numerical determination of the relation defining M_delta for Pinot's orthogonal quivers
(D~_{2n-1}, a) [fixed arrow n -> tau n, sign s] and (D~_{2n-2}, v) [fixed vertex n, O(V_n)].

Method (does not use Pinot's algebra):
 1. Parametrise SRep(Qbar, delta) with the standard signed space (all J_i = id): v_{tau a} = s(a) v_a^T.
 2. Find many random points of mu^{-1}(0) in SRep by Gauss-Newton from random starts (mu is quadratic).
 3. Evaluate x = det C3, y = tr(C1 C2), z = tr(C1 C2 C3) at vertex 3 (Pinot p.18 cycles).
 4. Find all linear relations among monomials x^a y^b z^c of weight <= 4L+8 (weights 4, 2L+2, 2L+4) by SVD.
Then read off the type: the relation z^2 + alpha z x^(n-1) + beta x y^2 + gamma x^(2n-2) (a-row) or
z^2 + beta x y^2 + alpha x^(n-1) y + gamma x^(2n-3) (v-row), and its discriminant."""
import numpy as np, itertools, sys
rng = np.random.default_rng(7)

def build(row, n, s=+1):
    # vertices: leaves 1,2 ; chain 3..n ; mirror tau-chain ; leaves t1,t2.  dims: leaves 1, others 2.
    if row == 'a':   # chain 3..n, fixed arrow n->tn, then tn..t3
        left = [('1', '3'), ('2', '3')] + [(str(i), str(i+1)) for i in range(3, n)]
        fixed = [('%d' % n, 't%d' % n)]
        verts = ['1', '2'] + [str(i) for i in range(3, n+1)] + ['t%d' % i for i in range(3, n+1)] + ['t1', 't2']
    else:            # 'v': chain 3..n (n fixed vertex), then n -> t(n-1) .. t3
        left = [('1', '3'), ('2', '3')] + [(str(i), str(i+1)) for i in range(3, n)]
        fixed = []
        verts = ['1', '2'] + [str(i) for i in range(3, n+1)] + ['t%d' % i for i in range(3, n)] + ['t1', 't2']
    tv = lambda u: u if (row == 'v' and u == str(n)) else (u[1:] if u.startswith('t') else 't' + u)
    dim = {u: (1 if u.lstrip('t') in ('1', '2') else 2) for u in verts}
    # arrows of Q: left arrows a:(t,h); their tau-images tau a : (tau h -> tau t)
    arrows = {}
    for k, (t, h) in enumerate(left):
        arrows['L%d' % k] = (t, h); arrows['R%d' % k] = (tv(h), tv(t))
    for k, (t, h) in enumerate(fixed):
        arrows['F%d' % k] = (t, h)
    return verts, dim, arrows, left, fixed, tv

def unpack(theta, row, n, s, struct):
    verts, dim, arrows, left, fixed, tv = struct
    v = {}; i = 0
    def take(r, c):
        nonlocal i
        M = theta[i:i+r*c].reshape(r, c); i += r*c; return M
    for k, (t, h) in enumerate(left):
        A = take(dim[h], dim[t]); B = take(dim[t], dim[h])            # a and a*
        v['L%d' % k] = A; v['L%d*' % k] = B
        v['R%d' % k] = A.T.copy(); v['R%d*' % k] = B.T.copy()          # sign +1 on unfixed arrows
    for k, (t, h) in enumerate(fixed):
        d = dim[t]
        S = take(d, d); T = take(d, d)
        v['F%d' % k] = S + s * S.T; v['F%d*' % k] = T + s * T.T          # symmetric (s=+1) / antisym (s=-1)
    return v, i

def mu(v, struct):
    verts, dim, arrows, *_ = struct
    m = {u: np.zeros((dim[u], dim[u]), complex) for u in verts}
    for a, (t, h) in arrows.items():
        m[h] += v[a] @ v[a + '*']; m[t] -= v[a + '*'] @ v[a]
    return np.concatenate([m[u].ravel() for u in verts])

def sample_point(row, n, s, struct, nvar):
    for attempt in range(50):
        th = (rng.normal(size=nvar) + 1j * rng.normal(size=nvar))
        for it in range(200):
            v, _ = unpack(th, row, n, s, struct); r = mu(v, struct)
            if np.linalg.norm(r) < 1e-13 * max(1, np.linalg.norm(th))**2: break
            Jm = np.zeros((r.size, nvar), complex); h = 1e-3
            for k in range(nvar):
                e = np.zeros(nvar, complex); e[k] = h
                Jm[:, k] = (mu(unpack(th + e, row, n, s, struct)[0], struct) - mu(unpack(th - e, row, n, s, struct)[0], struct)) / (2*h)
            th = th - np.linalg.lstsq(Jm, r, rcond=None)[0]
        if np.linalg.norm(r) < 1e-10:
            return unpack(th, row, n, s, struct)[0]
    raise RuntimeError('no convergence')

def invariants(v, row, n, struct):
    verts, dim, arrows, left, fixed, tv = struct
    C1 = v['L0'] @ v['L0*']                                      # 3 -> 1 -> 3
    C1p = v['L1'] @ v['L1*']                                     # 3 -> 2 -> 3
    target = tv('3')
    chain = []; cur = '3'
    while cur != target:
        nxt = [a for a, (t, h) in arrows.items() if t == cur and h.lstrip('t') not in ('1', '2') and a not in chain]
        a = nxt[0]; chain.append(a); cur = arrows[a][1]
    # short loop at 3 toward the chain; = C1 + C1' by the moment relation at 3 (Pinot Lemma 3.25);
    # in the exceptional case n = tau n = 3 Pinot *defines* C3 = C1 + C1'
    C3 = v[chain[0] + '*'] @ v[chain[0]] if chain else C1 + C1p
    P = np.eye(2, dtype=complex)
    for a in chain: P = v[a] @ P                                 # V3 -> V_t3
    B = np.eye(2, dtype=complex)
    for a in chain: B = B @ v[a + '*']                           # V_t3 -> V3 (back along starred arrows)
    loop = v['R0*'] @ v['R0']                                    # R0 : t3 -> t1 ; loop t3 -> t1 -> t3
    C2 = B @ loop @ P
    x = np.linalg.det(C3); y = np.trace(C1 @ C2); z = np.trace(C1 @ C2 @ C3)
    L = len(chain) + 1
    return x, y, z, L

def run(row, n, s=+1, N=80):
    struct = build(row, n, s)
    _, nvar = unpack(np.zeros(100000, complex), row, n, s, struct)
    pts = []
    for _ in range(N):
        v = sample_point(row, n, s, struct, nvar)
        x, y, z, L = invariants(v, row, n, struct)
        pts.append((x, y, z))
    pts = np.array(pts)
    wx, wy, wz, d = 4, 2*L + 2, 2*L + 4, 4*L + 8
    mons = [(a, b, c) for a in range(d//wx + 1) for b in range(d//wy + 1) for c in range(d//wz + 1)
            if 0 < a*wx + b*wy + c*wz <= d]
    # rescale each point along the C*-orbit so |x|=1 (relation is weighted homogeneous; this improves conditioning)
    scale = np.max(np.abs(pts), axis=None)
    if scale < 1e-8:
        return L, [], 0.0, 0.0, {'all invariants vanish (M_delta is a point)': 0}
    rho = np.maximum.reduce([np.abs(pts[:, 0])**(1/4), np.abs(pts[:, 1])**(1/wy), np.abs(pts[:, 2])**(1/wz)])
    keep = rho > 1e-6 * rho.max(); pts = pts[keep]; rho = rho[keep]
    t = 1 / rho                                                    # weighted normalisation onto the 'unit sphere'
    X, Y, Z = pts[:, 0]*t**4, pts[:, 1]*t**wy, pts[:, 2]*t**wz
    A = np.array([[X[i]**a * Y[i]**b * Z[i]**c for (a, b, c) in mons] for i in range(len(X))])
    U, S, Vh = np.linalg.svd(A)
    rel = Vh[-1].conj(); smin = S[-1] / S[0]; snext = S[-2] / S[0]
    terms = {m: rel[k] for k, m in enumerate(mons) if abs(rel[k]) > 1e-6 * np.abs(rel).max()}
    # normalise so the z^2 coefficient is 1
    kz = terms.get((0, 0, 2), None)
    terms = {m: c / kz for m, c in terms.items()} if kz else terms
    return L, mons, smin, snext, terms

if __name__ == '__main__':
    for row, n, s in [('a', 3, +1), ('a', 4, +1), ('a', 5, +1), ('v', 3, +1), ('v', 4, +1), ('v', 5, +1), ('a', 3, -1), ('a', 4, -1)]:
        L, mons, smin, snext, terms = run(row, n, s)
        name = f"(D~_{2*n-1}, a), s={s:+d}" if row == 'a' else f"(D~_{2*n-2}, v)"
        print(f"\n{name}, n={n}: L={L}, weights (4,{2*L+2},{2*L+4}), degree {4*L+8}; monomials tested: {len(mons)}")
        print(f"  smallest / next singular value (relative): {smin:.1e} / {snext:.1e}   -> one relation iff first tiny, second not")
        if not mons:
            print("  all invariants vanish: M_delta is a point (as in Pinot)"); continue
        pretty = ' + '.join(f"({c.real:+.4f}{c.imag:+.4f}i) x^{a} y^{b} z^{cc}" for (a, b, cc), c in sorted(terms.items()))
        print("  relation:", pretty)
        if row == 'a':
            al = terms.get((n-1, 0, 1), 0); be = terms.get((1, 2, 0), 0); ga = terms.get((2*n-2, 0, 0), 0)
            print(f"  beta={be:.4f}, gamma - alpha^2/4 = {ga - al**2/4:.4f}  -> D_{2*n-1} iff both nonzero;"
                  f" printed term x^(n-1)y present: {(n-1, 1, 0) in terms}")
        else:
            al = terms.get((n-1, 1, 0), 0); be = terms.get((1, 2, 0), 0); ga = terms.get((2*n-3, 0, 0), 0)
            disc = ga - (al**2/(4*be) if abs(be) > 1e-9 else np.inf)
            print(f"  beta={be:.4f}, gamma - alpha^2/(4 beta) = {disc:.4f}  -> D_{2*n-2} iff both nonzero")
