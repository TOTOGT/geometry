"""Headroom of the Cobeli-Zaharescu bound (arXiv:2610.23467v1, eq. 6.2) toward 11/12.
Pre-registered in docs/prereg-rh-proportion-headroom.md. Needs numpy, scipy. Not a proof of anything."""
import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq

alpha, d = 209/5000, 57/2000
Cpap, CMT = 1.3313394, 1.3274992
def bound(C, a, dd):
    tau = 2 + np.sqrt(2 - 2*a)
    return 1 - 4*(C - 1 - a + dd)/tau**2
print("Q1 reproduction: (6.2) =", bound(Cpap, alpha, d), "  with C=1.33133:", bound(1.33133, alpha, d), "  target 0.88893")

T = 11/12
for lab, C, dd in (("(a) paper C, d", Cpap, d), ("(b) C_MT, d=0", CMT, 0.0)):
    a = brentq(lambda x: bound(C, x, dd) - T, 0, 0.99)
    print("Q2 %s: alpha needed for 11/12 = %.4f  (paper alpha %.4f, ratio %.2f)" % (lab, a, alpha, a/alpha))
# also: with alpha = 0 and d = 0, what does the bare Gram step give
print("Q2 reference: alpha=0,d=0,C=C_MT  ->", bound(CMT, 0, 0), "   (paper's 1.3 union coefficient without remainder; C_MT-based)")

# Q3: rebuild f*, K*
a1, a2, a3 = 2/25, 1/25, -1/200
b = 1/np.sqrt(2)
def f(u): return np.cos(np.sqrt(2)*u)/(np.sqrt(2)*np.sin(b)) + a1*np.cos(2*np.pi*u) + a2*np.cos(4*np.pi*u) + a3*np.cos(6*np.pi*u)
us = np.linspace(-.5, .5, 200001)
print("Q3 control: int f* =", np.trapezoid(f(us), us), " min f* =", f(us).min(), "(paper: 1 and >0.79)")
def sf(z): return np.sinc(np.asarray(z)/np.pi)
def K(x):
    x = np.asarray(x, dtype=float)
    r = b/(2*np.sin(b))*(sf(np.pi*x-b)+sf(np.pi*x+b))
    for k, ak in ((1, a1), (2, a2), (3, a3)):
        r = r + 0.5*ak*(sf(np.pi*(x-k))+sf(np.pi*(x+k)))
    return r
# control: closed form against direct quadrature at three points
for x0 in (0.0, 0.5, 1.7):
    q = quad(lambda u: f(u)*np.cos(2*np.pi*u*x0), -.5, .5)[0]
    print("K* closed form vs quadrature at x=%.1f: %.10f %.10f" % (x0, float(K(x0)), q))
uu = np.linspace(-.5, .5, 3201); du = uu[1]-uu[0]
wq = np.full(uu.size, du); wq[0] = wq[-1] = du/2     # trapezoid weights (rectangle weights gave 1.3322, an error of mine)
F = f(uu)
C = (F**2*wq).sum() + (np.abs(uu[:, None]-uu[None, :])*(F*wq)[:, None]*(F*wq)[None, :]).sum()
print("Q3 control: C(f*) =", C, "(paper 1.3313394)")
print("K*(1/2) =", float(K(0.5)), "(paper: > 2/3)")
def e(s):  # lattice energy per point, truncated at 4000 terms
    ks = np.arange(1, 4001)
    return float(2*np.sum(K(ks*s)**2))
print("lattice energy per point e(s):")
for s_ in (1.0, 1.05, 1.1, 1.15, 1.2, 1.3):
    print("  s=%.2f  e=%.4f" % (s_, e(s_)))
def bound_lattice(nu_grid):
    best = None
    for tau in np.linspace(2.2, 5, 57):
        A = 2*tau - tau**2/2
        worst = max((A-1)*nu - nu*e(1/nu) for nu in nu_grid)
        val = 1 - 4*(Cpap - A + worst)/tau**2
        if best is None or val > best[0]: best = (val, tau)
    return best
print("Q3 lattice-remainder proxy, nu in [0.7,1]: bound, tau =", bound_lattice(np.linspace(0.7, 1.0, 13)))

# ---- Q3b (same session). e(s) is not monotone (smallest near s = 1, where the lattice sits on the zeros of K*),
# and a configuration may mix dense patches with holes. The remainder per unit length of a lattice of
# density rho is E(rho) = rho * e(1/rho). The best a mixture can do is the LOWER CONVEX ENVELOPE of E on
# rho in [0, 1.25]. Using R = N * Env(nu) is an optimistic proxy (lattice patches, not a proof).
rho = np.linspace(1e-3, 1.25, 1250)
E_ = np.array([r*e(1/r) for r in rho])
rho = np.concatenate([[0.0], rho]); E_ = np.concatenate([[0.0], E_])
# lower convex envelope by monotone chain
pts = []
for x, y in zip(rho, E_):
    while len(pts) >= 2 and (pts[-1][1]-pts[-2][1])*(x-pts[-2][0]) >= (y-pts[-2][1])*(pts[-1][0]-pts[-2][0]):
        pts.pop()
    pts.append((x, y))
px, py = zip(*pts)
Env = lambda nu: float(np.interp(nu, px, py))
print("Q3b  E(1)=%.4f  Env(0.89)=%.4f  per point %.4f   (paper's local lemma: alpha*nu - d = %.4f per length at nu=0.89)" % (E_[np.argmin(abs(rho-1))], Env(0.89), Env(0.89)/0.89, alpha*0.89-d))
def bound_env(C=Cpap, scale=1.0):
    best = None
    for tau in np.linspace(2.05, 5, 296):
        A = 2*tau - tau**2/2
        worst = max((A-1)*nu - scale*Env(nu) for nu in np.linspace(0, 1, 201))
        val = 1 - 4*(C - A + worst)/tau**2
        if best is None or val > best[0]: best = (val, tau)
    return best
print("Q3b ceiling with f*, remainder = N*Env(nu):   bound, tau =", bound_env())
print("Q3b same with C = C_MT:                      ", bound_env(CMT))
print("Q3b for reference, remainder switched off:   ", bound_env(scale=0.0))
print("Q3b remainder multiplied by 2 / 4 (not available from the method):", bound_env(scale=2.0)[0], bound_env(scale=4.0)[0])
