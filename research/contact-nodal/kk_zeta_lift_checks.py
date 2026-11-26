#!/usr/bin/env python3
"""
kk_zeta_lift_checks.py -- verification script for kk-zeta-lift-analysis.md

Checks every identity derived in the write-up, symbolically (sympy, small
exterior-algebra helper) and numerically (mpmath.zeta) on two grids:
  region A: sigma in (1.05, 3),  t in [0.5, 40]
  region B: sigma in (0.3, 0.7), t in [13.6, 14.6]  (around rho_1 = 1/2 + 14.1347i)

Prints PASS/FAIL per check. Exit code 0 iff every check passes.
Nothing here bears on the truth of RH; see the write-up.
"""
import sys
import itertools
import numpy as np
import mpmath as mp
import sympy as sp

mp.mp.dps = 30
RESULTS = []


def report(name, ok, detail=""):
    RESULTS.append((name, bool(ok)))
    print(f"[{'PASS' if ok else 'FAIL'}] {name}" + (f"  -- {detail}" if detail else ""))


# ----------------------------------------------------------------------------
# Tiny exterior algebra: a form is {sorted index tuple: sympy expr}
# ----------------------------------------------------------------------------
def _perm_sign(seq):
    seq = list(seq)
    s = 1
    for i in range(len(seq)):
        for j in range(i + 1, len(seq)):
            if seq[i] > seq[j]:
                s = -s
    return s


def wedge(a, b):
    out = {}
    for ia, ca in a.items():
        for ib, cb in b.items():
            idx = ia + ib
            if len(set(idx)) < len(idx):
                continue
            key = tuple(sorted(idx))
            out[key] = out.get(key, 0) + _perm_sign(idx) * ca * cb
    return {k: sp.simplify(v) for k, v in out.items() if sp.simplify(v) != 0}


def dform(a, coords):
    out = {}
    for ia, ca in a.items():
        for j, x in enumerate(coords):
            if j in ia:
                continue
            dc = sp.diff(ca, x)
            if dc == 0:
                continue
            idx = (j,) + ia
            key = tuple(sorted(idx))
            out[key] = out.get(key, 0) + _perm_sign(idx) * dc
    return {k: sp.simplify(v) for k, v in out.items() if sp.simplify(v) != 0}


def interior(vec, a):
    """i_vec a for a 2-form a (vec: list of components)."""
    out = {}
    for (i, j), c in a.items():
        # c dx_i ^ dx_j :  i_X = c (X^i dx_j - X^j dx_i)
        out[(j,)] = out.get((j,), 0) + c * vec[i]
        out[(i,)] = out.get((i,), 0) - c * vec[j]
    return {k: sp.simplify(v) for k, v in out.items() if sp.simplify(v) != 0}


def eval1(vec, a):
    return sp.simplify(sum(c * vec[k[0]] for k, c in a.items()))


def is_zero_form(a):
    return all(sp.simplify(v) == 0 for v in a.values())


# ----------------------------------------------------------------------------
# S1-S6: symbolic checks
# ----------------------------------------------------------------------------
def symbolic_checks():
    U, V, t = sp.symbols("Ut Vt t", real=True)   # (U~, V~, t), sigma fixed
    co = [U, V, t]
    c = sp.Function("c")(t)
    g = sp.Function("g")(t)
    ct, gt = sp.diff(c, t), sp.diff(g, t)
    W = c * gt - g * ct

    alpha = {(0,): c, (1,): -g}
    dal = dform(alpha, co)
    top = wedge(alpha, dal)
    # expected -W dU~ ^ dt ^ dV~  = +W dU^dV^dt   (dU^dt^dV = -dU^dV^dt)
    exp_coeff = sp.simplify(W)
    ok = set(top.keys()) <= {(0, 1, 2)} and sp.simplify(top.get((0, 1, 2), 0) - exp_coeff) == 0
    report("S1 alpha^dalpha = -W dU~^dt^dV~ (W = c g_t - g c_t)  [Ch11 Prop 11.1]", ok,
           f"coeff of dU~^dV~^dt = {top.get((0,1,2),0)}")

    # Reeb field R = (g_t d_U + c_t d_V)/W
    R = [gt / W, ct / W, 0]
    ok1 = sp.simplify(eval1(R, alpha) - 1) == 0
    ok2 = is_zero_form(interior(R, dal))
    report("S2 Reeb R = (g_t dU~ + c_t dV~)/W : alpha(R)=1, i_R dalpha=0, no d/dt part", ok1 and ok2)

    # uniqueness: general R with alpha(R)=1, i_R dalpha=0 forces R^t = 0 when (c_t,g_t)!=0
    a_, b_, e_ = sp.symbols("a b e")
    eqs = list(interior([a_, b_, e_], dal).values()) + [eval1([a_, b_, e_], alpha) - 1]
    sol = sp.solve(eqs, [a_, b_, e_], dict=True)
    ok3 = len(sol) == 1 and sp.simplify(sol[0][e_]) == 0 and \
        sp.simplify(sol[0][a_] - gt / W) == 0 and sp.simplify(sol[0][b_] - ct / W) == 0
    report("S3 Reeb field unique (generic c,g) and has zero dt component", ok3, str(sol))

    # Darboux / KK chart: z = c U - g V, w = c_t U - g_t V  =>  alpha = dz - w dt
    z = c * U - g * V
    w = ct * U - gt * V
    dz = {(i,): sp.diff(z, x) for i, x in enumerate(co)}
    rhs = {k: v for k, v in dz.items()}
    rhs[(2,)] = rhs.get((2,), 0) - w
    diff = {k: sp.simplify(alpha.get(k, 0) - rhs.get(k, 0)) for k in set(alpha) | set(rhs)}
    jac = sp.Matrix([[sp.diff(z, U), sp.diff(z, V)], [sp.diff(w, U), sp.diff(w, V)]]).det()
    ok = is_zero_form(diff) and sp.simplify(jac + W) == 0
    report("S4 alpha_arith = dz - w dt with z=cU~-gV~, w=c_tU~-g_tV~; Jacobian d(z,w)/d(U~,V~) = -W", ok)

    # rh-paper Def 4.1 one-coefficient form alpha = dV - g(t) dU on (U,V,t): already KK, Reeb = d_V
    a41 = {(1,): sp.Integer(1), (0,): -g}
    d41 = dform(a41, co)
    top41 = wedge(a41, d41)
    ok = sp.simplify(top41.get((0, 1, 2), 0) + gt) == 0 and \
        is_zero_form(interior([0, 1, 0], d41)) and eval1([0, 1, 0], a41) == 1
    report("S5 rh-paper Def4.1 alpha=dV-g dU: alpha^dalpha=-g_t dV^dt^dU, Reeb=d_V, F=-g_t dt^dU", ok)

    # Book 5 KK: eta = dy + k A on 5D, eta^deta^deta = k^2 dy^F^F
    y, x0, x1, x2, x3, k = sp.symbols("y x0 x1 x2 x3 kappa")
    c5 = [y, x0, x1, x2, x3]
    A = {(i + 1,): sp.Function(f"A{i}")(x0, x1, x2, x3) for i in range(4)}
    eta = {(0,): sp.Integer(1)}
    for kk_, v in A.items():
        eta[kk_] = k * v
    de = dform(eta, c5)
    lhs = wedge(eta, wedge(de, de))
    F = dform(A, c5)
    rhs5 = wedge({(0,): k ** 2}, wedge(F, F))
    ok = all(sp.simplify(lhs.get(key, 0) - rhs5.get(key, 0)) == 0 for key in set(lhs) | set(rhs5))
    report("S6 Book5: (dy + k A)^d()^d() = k^2 dy^F^F  (5D, generic A)", ok)

    # pulled-back eta = dz + U~ dV~ on (sigma,t,z): eta^deta = (dU~^dV~ as 2-form) ^ dz, Reeb d_z
    s_, t_, z_ = sp.symbols("s t z", real=True)
    Uf = sp.Function("Uf")(s_, t_)
    Vf = sp.Function("Vf")(s_, t_)
    co3 = [s_, t_, z_]
    eta3 = {(2,): sp.Integer(1), (0,): Uf * sp.diff(Vf, s_), (1,): Uf * sp.diff(Vf, t_)}
    de3 = dform(eta3, co3)
    top3 = wedge(eta3, de3)
    jacUV = sp.diff(Uf, s_) * sp.diff(Vf, t_) - sp.diff(Uf, t_) * sp.diff(Vf, s_)
    ok = sp.simplify(top3.get((0, 1, 2), 0) - jacUV) == 0 and is_zero_form(interior([0, 0, 1], de3))
    report("S7 eta = dz + U~ dV~ : eta^deta = J(U~,V~;sigma,t) dsigma^dt^dz, Reeb = d_z", ok)


# ----------------------------------------------------------------------------
# Numerical helpers
# ----------------------------------------------------------------------------
def L(s):  # zeta'/zeta
    return mp.zeta(s, derivative=1) / mp.zeta(s)


def Lp(s):  # (zeta'/zeta)'
    z0, z1, z2 = mp.zeta(s), mp.zeta(s, derivative=1), mp.zeta(s, derivative=2)
    return z2 / z0 - (z1 / z0) ** 2


def cg(sig, t):
    v = -L(mp.mpc(sig, t))          # -zeta'/zeta = c - i g
    return mp.re(v), -mp.im(v)


def logz_local(s, s0):
    """branch of log zeta continuous near s0 (Re part exact; Im defined up to const)."""
    return mp.log(abs(mp.zeta(s0))) + mp.log(mp.zeta(s) / mp.zeta(s0))


GRID_A = [(mp.mpf(s), mp.mpf(t)) for s in np.linspace(1.05, 3.0, 6) for t in np.linspace(0.5, 40.0, 9)]
GRID_B = [(mp.mpf(s), mp.mpf(t)) for s in np.linspace(0.3, 0.7, 5) for t in np.linspace(13.6, 14.6, 6)]


def relres(a, b):
    return abs(a - b) / max(mp.mpf(1), abs(a), abs(b))


def grid_check(name, grid, fn, tol):
    worst = mp.mpf(0)
    for sig, t in grid:
        worst = max(worst, fn(sig, t))
    report(name, worst < tol, f"max rel. residual {mp.nstr(worst, 3)} (tol {tol:g})")
    return worst


# N1: tangent of lifted curve: (d_t U~, d_t V~) = (-g, -c)
def n1(sig, t):
    s0 = mp.mpc(sig, t)
    Ut = mp.diff(lambda tt: mp.re(logz_local(mp.mpc(sig, tt), s0)), t)
    Vt = mp.diff(lambda tt: mp.im(logz_local(mp.mpc(sig, tt), s0)), t)
    c, g = cg(sig, t)
    return max(relres(Ut, -g), relres(Vt, -c))


# N2: alpha_arith annihilates the curve tangent: c*(-g) - g*(-c) = 0 (trivial algebra) and
#     W = c g_t - g c_t = -Re(conj(L) L')
def n2(sig, t):
    c_t = mp.diff(lambda tt: cg(sig, tt)[0], t)
    g_t = mp.diff(lambda tt: cg(sig, tt)[1], t)
    c, g = cg(sig, t)
    W_fd = c * g_t - g * c_t
    s = mp.mpc(sig, t)
    W_cl = -mp.re(mp.conj(L(s)) * Lp(s))
    return relres(W_fd, W_cl)


# N3: Reeb field numeric: alpha(R)=1, i_R dalpha = 0 with numerical c,g,c_t,g_t
def n3(sig, t):
    c, g = cg(sig, t)
    c_t = mp.diff(lambda tt: cg(sig, tt)[0], t)
    g_t = mp.diff(lambda tt: cg(sig, tt)[1], t)
    W = c * g_t - g * c_t
    a, b = g_t / W, c_t / W
    r1 = abs(c * a - g * b - 1)
    # dalpha = c_t dt^dU - g_t dt^dV ; i_R dalpha (R^t=0) = -(c_t a - g_t b) dt
    r2 = abs(c_t * a - g_t * b) / max(1, abs(c_t * a), abs(g_t * b))
    return max(r1, r2)


# N4: KK curvature of eta = dz + U~ dV~ : dU~^dV~ = |zeta'/zeta|^2 dsigma^dt
def n4(sig, t):
    s0 = mp.mpc(sig, t)
    f = lambda a, b: logz_local(mp.mpc(a, b), s0)
    Us = mp.diff(lambda a: mp.re(f(a, t)), sig)
    Ut = mp.diff(lambda b: mp.re(f(sig, b)), t)
    Vs = mp.diff(lambda a: mp.im(f(a, t)), sig)
    Vt = mp.diff(lambda b: mp.im(f(sig, b)), t)
    J = Us * Vt - Ut * Vs
    return relres(J, abs(L(s0)) ** 2)


# N5: zeta-image KK lift eta' = dz + U dV : dU^dV = |zeta'|^2 dsigma^dt
def n5(sig, t):
    f = lambda a, b: mp.zeta(mp.mpc(a, b))
    Us = mp.diff(lambda a: mp.re(f(a, t)), sig)
    Ut = mp.diff(lambda b: mp.re(f(sig, b)), t)
    Vs = mp.diff(lambda a: mp.im(f(a, t)), sig)
    Vt = mp.diff(lambda b: mp.im(f(sig, b)), t)
    J = Us * Vt - Ut * Vs
    return relres(J, abs(mp.zeta(mp.mpc(sig, t), derivative=1)) ** 2)


# N6: pull-back of the sigma-dependent alpha-hat along Phi(sigma,t) = (log zeta, sigma, t):
#     c dU~ - g dV~  =  -|L|^2 dsigma + 0 dt ; hence F = -(Phi^* alpha-hat) ^ dt
def n6(sig, t):
    s0 = mp.mpc(sig, t)
    f = lambda a, b: logz_local(mp.mpc(a, b), s0)
    Us = mp.diff(lambda a: mp.re(f(a, t)), sig)
    Ut = mp.diff(lambda b: mp.re(f(sig, b)), t)
    Vs = mp.diff(lambda a: mp.im(f(a, t)), sig)
    Vt = mp.diff(lambda b: mp.im(f(sig, b)), t)
    c, g = cg(sig, t)
    L2 = abs(L(s0)) ** 2
    return max(relres(c * Us - g * Vs, -L2), abs(c * Ut - g * Vt) / max(1, L2))


# ----------------------------------------------------------------------------
def series_check():
    """c, g as von Mangoldt series vs -zeta'/zeta, sigma in {2, 2.5, 3} (tail bound shown)."""
    N = 200000
    lam = np.zeros(N + 1)
    sieve = np.ones(N + 1, dtype=bool)
    sieve[:2] = False
    for p in range(2, int(N ** 0.5) + 1):
        if sieve[p]:
            sieve[p * p::p] = False
    for p in np.nonzero(sieve)[0]:
        pk = p
        while pk <= N:
            lam[pk] = np.log(p)
            pk *= p
    n = np.arange(N + 1, dtype=float)
    n[0] = 1
    worst = 0.0
    worst_ratio = 0.0
    for sig in (2.0, 2.5, 3.0):
        tail = N ** (1 - sig) * (np.log(N) / (sig - 1) + 1 / (sig - 1) ** 2)  # >= sum_{n>N} log n / n^sig
        for t in np.linspace(0.5, 40, 9):
            w = lam / n ** sig
            c_s = np.sum(w * np.cos(t * np.log(n)))
            g_s = np.sum(w * np.sin(t * np.log(n)))
            c, g = cg(mp.mpf(sig), mp.mpf(t))
            err = max(abs(c_s - float(c)), abs(g_s - float(g)))
            worst = max(worst, err)
            worst_ratio = max(worst_ratio, err / tail)
    report("N0 c,g = sum Lambda(n) n^-sigma (cos,sin)(t log n) = (Re,-Im)(-zeta'/zeta), sigma in {2,2.5,3}",
           worst_ratio <= 1.0, f"max abs err {worst:.2e}, <= tail bound (ratio {worst_ratio:.2f})")


def sign_change_checks():
    """Reproduces the reasons behind the 2026-10-19 / 2026-11-15 withdrawals: in sigma>1
    (no zeta zeros) both d_t g and W change sign."""
    sig = mp.mpf(2)
    ts = [mp.mpf(x) for x in np.linspace(0, 60, 1201)]
    gt_vals, W_vals = [], []
    for t in ts:
        s = mp.mpc(sig, t)
        Lv, Lpv = L(s), Lp(s)
        # g = Im(L) (since -L = c - i g), g_t = Im(i L') = Re(L')
        gt_vals.append(mp.re(Lpv))
        W_vals.append(-mp.re(mp.conj(Lv) * Lpv))
    gmin, Wmin = min(gt_vals), min(W_vals)
    report("N7 sigma=2: d_t g takes both signs (so dV-g dU is not contact everywhere in sigma>1)",
           gmin < 0 < max(gt_vals), f"min d_t g = {mp.nstr(gmin, 4)}")
    report("N8 sigma=2: W takes both signs (c dU~-g dV~ not contact everywhere in sigma>1)",
           Wmin < 0 < max(W_vals), f"min W on t in [0,60] = {mp.nstr(Wmin, 4)}")


def zeta_prime_zero_check():
    """F of the eta-lift vanishes exactly at zeros of zeta'. One lies in sigma>1 (no zeta zeros there)."""
    r = mp.findroot(lambda s: mp.zeta(s, derivative=1), mp.mpc(2.46, 23.3))
    F = abs(L(r)) ** 2
    report("N9 zero of zeta' found in sigma>1; KK curvature F=|zeta'/zeta|^2 vanishes there",
           mp.re(r) > 1 and F < mp.mpf(10) ** -20, f"rho' = {mp.nstr(r, 10)}, F = {mp.nstr(F, 3)}")

    rho1 = mp.zetazero(1)
    Fz = abs(mp.zeta(rho1, derivative=1)) ** 2
    report("N10 zeta-image lift dz+U dV is contact at rho_1 (F=|zeta'(rho_1)|^2>0); log lift singular there",
           Fz > mp.mpf("0.1") and abs(L(rho1 + mp.mpf("1e-8"))) > 1e7,
           f"rho_1 = {mp.nstr(rho1, 10)}, |zeta'(rho_1)|^2 = {mp.nstr(Fz, 6)}")


def winding_count(f, s_lo, s_hi, t_lo, t_hi, n=1500):
    pts = []
    for k in range(n):
        pts.append(mp.mpc(s_lo + (s_hi - s_lo) * k / n, t_lo))
    for k in range(n):
        pts.append(mp.mpc(s_hi, t_lo + (t_hi - t_lo) * k / n))
    for k in range(n):
        pts.append(mp.mpc(s_hi - (s_hi - s_lo) * k / n, t_hi))
    for k in range(n):
        pts.append(mp.mpc(s_lo, t_hi - (t_hi - t_lo) * k / n))
    pts.append(pts[0])
    vals = [f(p) for p in pts]
    tot = mp.mpf(0)
    maxstep = mp.mpf(0)
    for a, b in zip(vals[:-1], vals[1:]):
        d = mp.arg(b / a)
        maxstep = max(maxstep, abs(d))
        tot += d
    return tot / (2 * mp.pi), maxstep


def speiser_box_check():
    """Finite numerical check consistent with the KNOWN theorem (Speiser 1934): zeta' has no zeros
    in a sample box inside 0<sigma<1/2. A finite box says nothing about RH."""
    mp.mp.dps = 20
    zp = lambda s: mp.zeta(s, derivative=1)
    w_left, st1 = winding_count(zp, mp.mpf("0.05"), mp.mpf("0.45"), mp.mpf(10), mp.mpf(60))
    w_right, st2 = winding_count(zp, mp.mpf("0.55"), mp.mpf(3.0), mp.mpf(10), mp.mpf(60))
    mp.mp.dps = 30
    ok = abs(w_left) < 0.01 and abs(w_right - mp.nint(w_right)) < 0.01 and mp.nint(w_right) >= 1 \
        and st1 < 1 and st2 < 1
    report("N11 winding of zeta': 0 zeros in [0.05,0.45]x[10,60]; >=1 in [0.55,3]x[10,60]", ok,
           f"left {mp.nstr(w_left, 5)}, right {mp.nstr(w_right, 5)}, max arg step {mp.nstr(max(st1, st2), 3)}")


def four_d_check():
    """4D base (s1,s2) -> (log zeta(s1), log L(s2,chi_-4)); omega = dU1^dV1 + dU2^dV2 pulled back.
    omega^omega = 2 Pf(Omega) vol, expected Pf = |zeta'/zeta(s1)|^2 |L'/L(s2)|^2."""
    chi = [0, 1, 0, -1]
    Lchi = lambda s: mp.dirichlet(s, chi)
    worst = mp.mpf(0)
    pts = [((1.5, 5.0), (1.3, 7.0)), ((2.5, 20.0), (1.1, 3.0)), ((0.4, 14.0), (0.6, 6.5)),
           ((0.55, 14.2), (0.45, 10.0)), ((1.05, 0.7), (2.9, 33.0))]
    for (a1, b1), (a2, b2) in pts:
        a1, b1, a2, b2 = map(mp.mpf, (a1, b1, a2, b2))
        s1, s2 = mp.mpc(a1, b1), mp.mpc(a2, b2)
        f1 = lambda a, b: mp.log(mp.zeta(mp.mpc(a, b)) / mp.zeta(s1))
        f2 = lambda a, b: mp.log(Lchi(mp.mpc(a, b)) / Lchi(s2))

        def jac(f, a, b):
            Us = mp.diff(lambda x: mp.re(f(x, b)), a)
            Ut = mp.diff(lambda y: mp.re(f(a, y)), b)
            Vs = mp.diff(lambda x: mp.im(f(x, b)), a)
            Vt = mp.diff(lambda y: mp.im(f(a, y)), b)
            return Us * Vt - Ut * Vs
        J1, J2 = jac(f1, a1, b1), jac(f2, a2, b2)
        # Omega block-diagonal [[0,J1],[-J1,0]] (+) [[0,J2],[-J2,0]] ; Pf = J1*J2
        Om = mp.matrix(4, 4)
        Om[0, 1], Om[1, 0], Om[2, 3], Om[3, 2] = J1, -J1, J2, -J2
        pf = Om[0, 1] * Om[2, 3] - Om[0, 2] * Om[1, 3] + Om[0, 3] * Om[1, 2]
        Lp2 = mp.dirichlet(s2, chi, derivative=1) / Lchi(s2)
        expected = abs(L(s1)) ** 2 * abs(Lp2) ** 2
        worst = max(worst, relres(pf, expected))
    report("N12 4D base (log zeta(s1), log L(s2,chi_-4)): Pf = |zeta'/zeta|^2 |L'/L|^2 > 0 off crit. pts",
           worst < 1e-12, f"max rel. residual {mp.nstr(worst, 3)}")



def main():
    print("== symbolic ==")
    symbolic_checks()
    print("== numeric: region A sigma in (1.05,3), t in [0.5,40];  region B sigma in (0.3,0.7), t in [13.6,14.6] ==")
    series_check()
    for tag, grid in (("A", GRID_A), ("B", GRID_B)):
        grid_check(f"N1{tag} (d_t U~, d_t V~) = (-g, -c)", grid, n1, 1e-15)
        grid_check(f"N2{tag} W = c g_t - g c_t = -Re(conj(L) L')", grid, n2, 1e-15)
        grid_check(f"N3{tag} Reeb (g_t,c_t,0)/W satisfies alpha(R)=1, i_R dalpha=0", grid, n3, 1e-15)
        grid_check(f"N4{tag} eta=dz+U~dV~: F = dU~^dV~ = |zeta'/zeta|^2 dsigma^dt", grid, n4, 1e-15)
        grid_check(f"N5{tag} eta'=dz+U dV: F = dU^dV = |zeta'|^2 dsigma^dt", grid, n5, 1e-15)
        grid_check(f"N6{tag} Phi^*(c dU~ - g dV~) = -|zeta'/zeta|^2 dsigma", grid, n6, 1e-15)
    sign_change_checks()
    zeta_prime_zero_check()
    speiser_box_check()
    four_d_check()
    nfail = sum(1 for _, ok in RESULTS if not ok)
    print(f"\n{len(RESULTS) - nfail}/{len(RESULTS)} checks passed")
    sys.exit(0 if nfail == 0 else 1)


if __name__ == "__main__":
    main()
