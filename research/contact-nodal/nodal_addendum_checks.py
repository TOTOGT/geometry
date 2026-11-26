#!/usr/bin/env python3
"""Numerical checks for the draft addendum "A Local Nodal Theorem at z = i" (Book 4, after Ch 14).
NUMERICAL CHECKS ONLY. Nothing here proves or implies the Riemann Hypothesis.
Exit code 0 iff every check passes. Writes nodal_data.json (sign-change table + numbers) beside itself.
f(z) = E*(z,s) = xi(2s) E(z,s), s = 1/2 + i t, xi(2s) = pi^-s Gamma(s) zeta(2s).
"""
import json, os, sys
import mpmath as mp

mp.mp.dps = 30
NTERMS = 30
CHI4 = [0, 1, 0, -1]          # chi_{-4} mod 4
results = []

def check(name, ok, detail=""):
    results.append((name, bool(ok), detail))
    print(("PASS " if ok else "FAIL ") + name + ("  | " + detail if detail else ""))

def xi2(w):                     # xi(w) = pi^{-w/2} Gamma(w/2) zeta(w)
    return mp.pi**(-w/2) * mp.gamma(w/2) * mp.zeta(w)

def sigma(n, a):
    return mp.fsum(mp.mpf(d)**a for d in range(1, n+1) if n % d == 0)

def f_fourier(x, y, t, N=NTERMS):
    s = mp.mpf(1)/2 + 1j*mp.mpf(t)
    x, y = mp.mpf(x), mp.mpf(y)
    val = xi2(2*s)*y**s + xi2(2*s-1)*y**(1-s)
    acc = 0
    for n in range(1, N+1):
        acc += mp.mpf(n)**(s-mp.mpf(1)/2) * sigma(n, 1-2*s) * mp.besselk(s-mp.mpf(1)/2, 2*mp.pi*n*y) * mp.cos(2*mp.pi*n*x)
    return val + 4*mp.sqrt(y)*acc

def F_fact(t):                  # 2 Lambda_{Q(i)}(1/2+it)
    s = mp.mpf(1)/2 + 1j*mp.mpf(t)
    return 2 * mp.pi**(-s) * mp.gamma(s) * mp.zeta(s) * mp.dirichlet(s, CHI4)

def F_norm(t):                  # F(t)/|pi^-s Gamma(s)|: same sign as F, O(1) size (for root finding)
    s = mp.mpf(1)/2 + 1j*mp.mpf(t)
    return (F_fact(t) / abs(mp.pi**(-s)*mp.gamma(s))).real

def a_coef(t, N=NTERMS):        # f_xx(i) = -16 pi^2 sum n^{s+3/2} sigma_{1-2s}(n) K_{s-1/2}(2 pi n)
    s = mp.mpf(1)/2 + 1j*mp.mpf(t)
    return -16*mp.pi**2 * mp.fsum(mp.mpf(n)**(s+mp.mpf(3)/2)*sigma(n, 1-2*s)*mp.besselk(s-mp.mpf(1)/2, 2*mp.pi*n) for n in range(1, N+1))

# 1. Epstein factorization identity at three heights, 12 digits
for t in ["6.02", "14.1347", "20"]:
    A = f_fourier(0, 1, t); B = F_fact(t)
    rel = abs(A-B)/abs(B)
    check(f"identity Fourier vs 2*Lambda_Q(i) at t={t}", rel < 1e-12, f"F={mp.nstr(B.real,10)}, rel diff={mp.nstr(rel,3)}")

# 2. realness on the critical line (at i and off i)
mx = 0
for (x, y, t) in [(0, 1, 6.02), (0.1, 0.95, 14.1347), (0.3, 1.4, 20), (-0.2, 0.9, 9.0)]:
    v = f_fourier(x, y, t); mx = max(mx, abs(v.imag)/abs(v))
check("f real on the critical line (|Im f|/|f|)", mx < 1e-20, f"max ratio {mp.nstr(mx,3)}")

# 2b. modular invariance f(-1/z) = f(z) and reflection f(-x+iy) = f(x+iy) at a generic point (Step 3a/3b)
z = mp.mpc("0.13", "0.9"); w = -1/z
d1 = abs(f_fourier(w.real, w.imag, 14.1347) - f_fourier(z.real, z.imag, 14.1347))/abs(f_fourier(z.real, z.imag, 14.1347))
check("f(-1/z) = f(z) at z=0.13+0.9i (sigma-invariance, Step 3a)", d1 < 1e-20, mp.nstr(d1, 3))
d2 = abs(f_fourier(-0.13, 0.9, 14.1347) - f_fourier(0.13, 0.9, 14.1347))
check("f(-x+iy) = f(x+iy) (Step 3b; structural: cos is even)", d2 == 0)

# 3. sign changes of F on (0, 40]
mp.mp.dps = 20
h = mp.mpf("0.01"); T = 40
ts = [h*k for k in range(1, int(T/h)+1)]
vals = [F_norm(t) for t in ts]
roots = []
for k in range(len(ts)-1):
    if vals[k] == 0 or vals[k]*vals[k+1] < 0:
        r = mp.findroot(F_norm, (ts[k], ts[k+1]), solver="anderson")
        roots.append(r)
zz = [mp.zetazero(k).imag for k in range(1, 8)]
zz = [z for z in zz if z < T]
table = []
for r in roots:
    dz = min(abs(r - z) for z in zz)
    Lval = abs(mp.dirichlet(mp.mpf(1)/2 + 1j*r, CHI4)); Zval = abs(mp.zeta(mp.mpf(1)/2 + 1j*r))
    src = "zeta" if dz < 1e-6 else "L(chi_-4)"
    table.append({"t": float(r), "source": src, "abs_zeta": float(Zval), "abs_L": float(Lval)})
nz = sum(1 for e in table if e["source"] == "zeta"); nL = len(table) - nz
check("20 sign changes of F up to T=40", len(table) == 20, f"found {len(table)}")
check("split 6 zeta + 14 L(chi_-4)", (nz, nL) == (6, 14), f"{nz} zeta, {nL} L")
check("L-classified roots are L zeros (|L|<1e-8) and not zeta zeros",
      all((e['abs_L'] < 1e-8 and e['abs_zeta'] > 1e-3) if e['source'] != 'zeta' else (e['abs_zeta'] < 1e-8 and e['abs_L'] > 1e-3) for e in table))
expected_zeta = [14.1347, 21.0220, 25.0109, 30.4249, 32.9351, 37.5862]
got_zeta = [e["t"] for e in table if e["source"] == "zeta"]
check("zeta heights match 14.1347,...,37.5862", len(got_zeta) == 6 and all(abs(g-e) < 1e-4 for g, e in zip(got_zeta, expected_zeta)))
check("first L zero near 6.0209", abs([e for e in table if e['source'] != 'zeta'][0]['t'] - 6.0209) < 1e-3)

# 4. local structure at t1
mp.mp.dps = 30
t1 = mp.mpf("14.1347251417")
fr = lambda x, y: f_fourier(x, y, t1).real
a = a_coef(t1).real
fxx = mp.diff(lambda x: fr(x, 1), 0, 2)
fyy = mp.diff(lambda y: fr(0, y), 1, 2)
fxy = mp.diff(lambda x, y: fr(x, y), (0, 1), (1, 1))
gx = mp.diff(lambda x: fr(x, 1), 0); gy = mp.diff(lambda y: fr(0, y), 1)
Ft1 = F_fact(t1).real
Fp = mp.diff(lambda u: F_fact(u).real, t1)
print(f"  t1={t1}: F={mp.nstr(Ft1,5)} a={mp.nstr(a,8)} fxx(num)={mp.nstr(fxx,8)} fyy={mp.nstr(fyy,8)} fxy={mp.nstr(fxy,3)} grad=({mp.nstr(gx,3)},{mp.nstr(gy,3)}) F'={mp.nstr(Fp,6)}")
check("a(t1) = 2.41476e-7 (series)", abs(a/mp.mpf("2.41476e-7") - 1) < 1e-5, mp.nstr(a, 8))
check("series a agrees with numerical f_xx(i)", abs(a - fxx)/abs(a) < 1e-10)
check("f_yy(i) = -2.41476e-7", abs(fyy/mp.mpf("-2.41476e-7") - 1) < 1e-5, mp.nstr(fyy, 8))
check("trace f_xx+f_yy ~ 0 at a zero (|trace| < 1e-15)", abs(fxx+fyy) < 1e-15, mp.nstr(fxx+fyy, 3))
check("f_xy(i) = 0", abs(fxy) < 1e-20, mp.nstr(fxy, 3))
check("grad f(i) = 0 (< 1e-15)", max(abs(gx), abs(gy)) < 1e-15, f"{mp.nstr(gx,3)}, {mp.nstr(gy,3)}")
check("F(t1) ~ 0", abs(Ft1) < 1e-15, mp.nstr(Ft1, 3))
check("F'(t1) = -1.1386e-9", abs(Fp/mp.mpf("-1.1386e-9") - 1) < 1e-4, mp.nstr(Fp, 6))
# grad zero away from zeros too (Step 3a holds for every t)
g2 = max(abs(mp.diff(lambda x: f_fourier(x, 1, 9.0).real, 0)), abs(mp.diff(lambda y: f_fourier(0, y, 9.0).real, 1)))
check("grad f(i) = 0 also at non-zero height t=9 (relative)", g2/abs(F_fact(9).real) < 1e-15, mp.nstr(g2, 3))

# 5. nodal directions of the Hessian quadratic form: Q(theta)=fxx c^2 + 2 fxy c s + fyy s^2 = 0
import math
A_, B_, C_ = float(fxx), float(fxy), float(fyy)
# solve C tan^2 + 2B tan + A = 0
disc = B_*B_ - A_*C_
tans = [(-B_ + math.sqrt(disc))/C_, (-B_ - math.sqrt(disc))/C_]
angs = sorted(math.degrees(math.atan(u)) for u in tans)
check("nodal tangents at +-45 deg (y-1 = +-x), orthogonal", abs(angs[0]+45) < 1e-6 and abs(angs[1]-45) < 1e-6 and abs(angs[1]-angs[0]-90) < 1e-6, f"{angs}")

out = {"sign_changes": table, "t1": str(t1), "a": float(a), "fyy": float(fyy), "trace": float(fxx+fyy),
       "fxy": float(fxy), "grad": [float(gx), float(gy)], "Fprime_t1": float(Fp)}
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "nodal_data.json"), "w") as fh:
    json.dump(out, fh, indent=1)
nfail = sum(1 for r in results if not r[1])
print(f"\n{len(results)-nfail}/{len(results)} checks passed")
sys.exit(1 if nfail else 0)
