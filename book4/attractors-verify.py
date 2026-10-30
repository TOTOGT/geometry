#!/usr/bin/env python3
"""Verifier for book4/attractors.html (strange attractors between dimension 2 and 3).

For each system: integrate with RK4, discard a transient, compute the full Lyapunov spectrum by
the Benettin/QR method (tangent map propagated with RK4, finite-difference Jacobian), the
Kaplan-Yorke dimension, and run these checks:
  * sum of the exponents equals the mean divergence of the vector field (exact for constant divergence)
  * the trajectory stays bounded
  * (Burke-Shaw, Lorenz) the 180-degree rotation symmetry (x,y,z)->(-x,-y,z) holds for the vector field
Usage:  python3 attractors-verify.py [name ...]     (default: all; writes attractors-data.json)
"""
import numpy as np, math, json, sys, time

def lorenz(p=(10.0, 28.0, 8/3)):
    s, r, b = p
    return lambda v: np.array([s*(v[1]-v[0]), r*v[0]-v[1]-v[0]*v[2], v[0]*v[1]-b*v[2]])
def rossler(p=(0.2, 0.2, 5.7)):
    a, b, c = p
    return lambda v: np.array([-v[1]-v[2], v[0]+a*v[1], b+v[2]*(v[0]-c)])
def chen(p=(35.0, 3.0, 28.0)):
    a, b, c = p
    return lambda v: np.array([a*(v[1]-v[0]), (c-a)*v[0]-v[0]*v[2]+c*v[1], v[0]*v[1]-b*v[2]])
def lu(p=(36.0, 3.0, 20.0)):
    a, b, c = p
    return lambda v: np.array([a*(v[1]-v[0]), -v[0]*v[2]+c*v[1], v[0]*v[1]-b*v[2]])
def halvorsen(p=(1.89,)):
    a = p[0]
    return lambda v: np.array([-a*v[0]-4*v[1]-4*v[2]-v[1]**2, -a*v[1]-4*v[2]-4*v[0]-v[2]**2, -a*v[2]-4*v[0]-4*v[1]-v[0]**2])
def aizawa(p=(0.95, 0.7, 0.6, 3.5, 0.25, 0.1)):
    a, b, c, d, e, f = p
    return lambda v: np.array([(v[2]-b)*v[0]-d*v[1], d*v[0]+(v[2]-b)*v[1],
        c+a*v[2]-v[2]**3/3-(v[0]**2+v[1]**2)*(1+e*v[2])+f*v[2]*v[0]**3])
def burkeshaw(p=(10.0, 4.272)):
    s, w = p
    return lambda v: np.array([-s*(v[0]+v[1]), -v[1]-s*v[0]*v[2], s*v[0]*v[1]+w])
def sprottA():
    return lambda v: np.array([v[1], -v[0]+v[1]*v[2], 1-v[1]**2])
def thomas(p=(0.208186,)):
    b = p[0]
    return lambda v: np.array([math.sin(v[1])-b*v[0], math.sin(v[2])-b*v[1], math.sin(v[0])-b*v[2]])

# name: (builder, params text, start, dt, transient, total, constant divergence or None, note)
SYS = {
 "lorenz":    (lorenz, "sigma=10, rho=28, beta=8/3", [1, 1, 1], 0.005, 40, 400, -(10+1+8/3)),
 "rossler":   (rossler, "a=0.2, b=0.2, c=5.7", [1, 1, 1], 0.01, 100, 600, None),
 "chen":      (chen, "a=35, b=3, c=28", [-3, 2, 20], 0.0025, 20, 150, -35+28-3),
 "lu":        (lu, "a=36, b=3, c=20", [1, 1, 1], 0.0025, 20, 150, -36+20-3),
 "halvorsen": (lambda: halvorsen((1.4,)), "a=1.4", [0.88, 0.09, 1.64], 0.005, 40, 400, -3*1.4),
 "halvorsen189": (lambda: halvorsen((1.89,)), "a=1.89", [1.04, 2.46, 0.99], 0.005, 40, 400, -3*1.89),
 "aizawa":    (aizawa, "a=0.95, b=0.7, c=0.6, d=3.5, e=0.25, f=0.1", [-0.28, 1.29, 1.01], 0.01, 100, 1500, None),
 "aizawa_alt": (aizawa, "same parameters, start (0.1, 1, 0.01)", [0.1, 1, 0.01], 0.01, 100, 600, None),
 "burkeshaw": (burkeshaw, "s=10, v=4.272", [1, 1, 1], 0.002, 20, 200, -11.0),
 "sprottA":   (sprottA, "none", [0, 5, 0], 0.01, 100, 800, None),
 "thomas":    (lambda: thomas((0.18,)), "b=0.18", [-4.04, -0.46, -1.73], 0.02, 300, 4000, -3*0.18),
 "thomas208": (lambda: thomas((0.208186,)), "b=0.208186", [-1.14, -0.91, -0.43], 0.02, 300, 3000, -3*0.208186),
}

def jac(f, v, h=1e-7):
    f0 = f(v); J = np.zeros((3, 3))
    for j in range(3):
        w = v.copy(); w[j] += h
        J[:, j] = (f(w) - f0) / h
    return J

def step(f, v, Phi, dt):
    def F(v, P): return f(v), jac(f, v) @ P
    k1v, k1P = F(v, Phi)
    k2v, k2P = F(v + .5*dt*k1v, Phi + .5*dt*k1P)
    k3v, k3P = F(v + .5*dt*k2v, Phi + .5*dt*k2P)
    k4v, k4P = F(v + dt*k3v, Phi + dt*k3P)
    return v + dt*(k1v + 2*k2v + 2*k3v + k4v)/6, Phi + dt*(k1P + 2*k2P + 2*k3P + k4P)/6

def spectrum(f, v0, dt, trans, total, renorm=10):
    v = np.array(v0, float)
    for _ in range(int(trans/dt)):
        k1 = f(v); k2 = f(v+.5*dt*k1); k3 = f(v+.5*dt*k2); k4 = f(v+dt*k3); v = v + dt*(k1+2*k2+2*k3+k4)/6
    P = np.eye(3); sums = np.zeros(3); T = 0.0; vmax = 0.0; div = 0.0; nd = 0
    n = int((total-trans)/dt)
    for i in range(1, n+1):
        v, P = step(f, v, P, dt)
        vmax = max(vmax, float(np.max(np.abs(v))))
        if i % renorm == 0:
            Q, R = np.linalg.qr(P); P = Q
            sums += np.log(np.abs(np.diag(R))); T += renorm*dt
            div += np.trace(jac(f, v)); nd += 1
        if not np.all(np.isfinite(v)): return None
    lam = sums / T
    return lam, vmax, div/nd

def ky(lam):
    l = [0.0 if abs(x) < 0.01 else x for x in sorted(lam, reverse=True)]; s = 0.0   # |lambda|<0.01 counted as zero
    for j in range(3):
        if s + l[j] < 0:
            return j + s/abs(l[j])
        s += l[j]
    return 3.0

if __name__ == "__main__":
    names = sys.argv[1:] or list(SYS)
    try: out = json.load(open("attractors-data.json"))
    except Exception: out = {}
    for nm in names:
        b, ptxt, v0, dt, tr, tot, cdiv = SYS[nm]
        f = b(); t0 = time.time()
        r = spectrum(f, v0, dt, tr, tot)
        if r is None: print(nm, "DIVERGED"); continue
        lam, vmax, mdiv = r
        lam = sorted(lam, reverse=True)
        d = ky(lam)
        rec = {"params": ptxt, "lambda": [round(float(x), 4) for x in lam], "sum": round(float(sum(lam)), 4),
               "mean_div": round(float(mdiv), 4), "KY": round(float(d), 4), "bounded_max_abs": round(vmax, 2),
               "T": tot-tr, "dt": dt}
        if cdiv is not None: rec["exact_div"] = round(cdiv, 4)
        out[nm] = rec
        extra = f"  exact div {cdiv:.4f}" if cdiv is not None else ""
        print(f"{nm:10s} lambda={rec['lambda']}  sum={rec['sum']}  mean div={rec['mean_div']}{extra}  KY={rec['KY']}  max|x|={rec['bounded_max_abs']}  ({time.time()-t0:.0f}s)", flush=True)
    # symmetry checks of the vector fields
    for nm, fld in (("lorenz", lorenz()), ("burkeshaw", burkeshaw())):
        rng = np.random.default_rng(0); bad = 0
        for _ in range(200):
            v = rng.normal(size=3)*5; w = np.array([-v[0], -v[1], v[2]]); a = fld(v); c = fld(w)
            if not np.allclose(c, [-a[0], -a[1], a[2]], atol=1e-9): bad += 1
        print(f"symmetry (x,y,z)->(-x,-y,z) of {nm}: violations {bad}/200")
        out.setdefault(nm, {})["rot180_violations_of_200"] = bad
    json.dump(out, open("attractors-data.json", "w"), indent=1)
