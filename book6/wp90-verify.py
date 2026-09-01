#!/usr/bin/env python3
"""
wp90-verify.py — every number printed in book6/wp90-the-metric-on-the-restricted-fibre.html

Checks the claims of WP-90 against Pernambuco & Céleri, "Geometry of restricted
information: the case of quantum thermodynamics", arXiv:2602.06716v1 (6 Feb 2026).

Run:  python3 book6/wp90-verify.py
Deps: numpy, scipy.  Deterministic (seeded).  Runtime ~15 s.

Each block prints  [OK] / [FAIL]  and the figure quoted on the page.
"""
import numpy as np
from scipy.linalg import expm, polar
from scipy.optimize import minimize

FAILED = []
def check(name, ok, detail=""):
    print(("[OK]   " if ok else "[FAIL] ") + name + ("   " + detail if detail else ""))
    if not ok: FAILED.append(name)

# ------------------------------------------------------------------ helpers
def rand_unitary(rng, d):
    z = (rng.normal(size=(d, d)) + 1j*rng.normal(size=(d, d)))/np.sqrt(2)
    q, r = np.linalg.qr(z)
    return q @ np.diag(np.diag(r)/abs(np.diag(r)))

def herm(M):  return (M + M.conj().T)/2
def anti(M):  return (M - M.conj().T)/2

def sq(a):
    w, v = np.linalg.eigh(a); w = np.clip(w, 0, None)
    return v @ np.diag(np.sqrt(w)) @ v.conj().T

def logm(a):
    w, v = np.linalg.eigh(a); w = np.clip(w, 1e-300, None)
    return v @ np.diag(np.log(w)) @ v.conj().T

def relent(r, s):
    return float((np.trace(r @ logm(r)) - np.trace(r @ logm(s))).real)

def root_fidelity(r, s):
    """Tr sqrt( sqrt(r) s sqrt(r) )  —  this is sqrt(F) in the Deffner-Lutz convention."""
    sr = sq(r)
    return float(np.trace(sq(sr @ s @ sr)).real)

def bures_angle(r, s):
    return float(np.arccos(np.clip(root_fidelity(r, s), -1, 1)))

def vN(r):
    w = np.linalg.eigvalsh(r); w = w[w > 1e-14]
    return float(-(w*np.log(w)).sum())

def bures_norm2(r, X):
    """g^B_r(X,X) = (1/2) sum_jk |<j|X|k>|^2 / (l_j + l_k)  (quantum Fisher / 4)."""
    w, v = np.linalg.eigh(r); Y = v.conj().T @ X @ v; d = len(w)
    return float(0.5*sum(abs(Y[j, k])**2/(w[j] + w[k])
                         for j in range(d) for k in range(d) if w[j] + w[k] > 1e-12))

print("=" * 74)
print("PART 1 — the fluctuation theorem of arXiv:2602.06716, Eqs. (5)-(8), (44)")
print("=" * 74)

rng = np.random.default_rng(7)
d, beta = 6, 1/0.5
b0, bT = rand_unitary(rng, d), rand_unitary(rng, d)
e0, n0 = [-1.0, 0.3, 2.0], [3, 2, 1]            # spectrum + degeneracies at t = 0
eT, nT = [-0.5, 0.8, 1.5, 3.0], [2, 1, 2, 1]    # ... and at t = tau (degeneracies change)

def projectors(evals, degs, basis):
    Ps, i = [], 0
    for e, n in zip(evals, degs):
        P = np.zeros((d, d), complex)
        for j in range(i, i + n):
            v = basis[:, j:j+1]; P += v @ v.conj().T
        Ps.append(P); i += n
    return Ps

P0, PT = projectors(e0, n0, b0), projectors(eT, nT, bT)
U = rand_unitary(rng, d)

Z0 = sum(n*np.exp(-beta*e) for e, n in zip(e0, n0))
ZT = sum(n*np.exp(-beta*e) for e, n in zip(eT, nT))
pF = np.array([n*np.exp(-beta*e)/Z0 for e, n in zip(e0, n0)])
pR = np.array([n*np.exp(-beta*e)/ZT for e, n in zip(eT, nT)])

# conditional probabilities from the gauge-twirled conditional states rho_k = Pi_k / n_k
pfwd = np.array([[np.trace(PT[l] @ U @ (P0[k]/n0[k]) @ U.conj().T).real
                  for l in range(len(eT))] for k in range(len(e0))])          # p(l|k)
prev = np.array([[np.trace(P0[k] @ U.conj().T @ (PT[l]/nT[l]) @ U).real
                  for k in range(len(e0))] for l in range(len(eT))])          # p(k|l)
check("conditional distributions normalised",
      np.allclose(pfwd.sum(1), 1) and np.allclose(prev.sum(1), 1))

# microreversibility  n_0^k p(l|k) = n_tau^l p(k|l) = Tr(Pi^l U Pi^k U^dag)
T_lk = np.array([[np.trace(PT[l] @ U @ P0[k] @ U.conj().T).real
                  for l in range(len(eT))] for k in range(len(e0))])
check("microreversibility  n_0^k p(l|k) = n_tau^l p(k|l)",
      np.allclose(np.array(n0)[:, None]*pfwd, T_lk) and
      np.allclose(np.array(nT)[None, :]*prev.T, T_lk))

jF = pF[:, None]*pfwd            # p_F(k,l)
jR = pR[:, None]*prev            # p_R(l,k), indexed [l,k]
sig = np.array([[np.log(nT[l]/pR[l]) - np.log(n0[k]/pF[k])
                 for l in range(len(eT))] for k in range(len(e0))])   # Eq. (6)

ift = float((jF*np.exp(-sig)).sum())
check("Eq. (7)  <e^-sigma_inv> = 1", abs(ift - 1) < 1e-12, f"got {ift:.15f}")

check("detailed FT  sigma_inv = ln[ p_F(k,l) / p_R(l,k) ]  (WP-90 Prop. 4)",
      abs(sig - np.log(jF/jR.T)).max() < 1e-12,
      f"max dev {abs(sig - np.log(jF/jR.T)).max():.2e}")

SG = lambda p, n: float(-(p*np.log(p)).sum() + (p*np.log(np.array(n, float))).sum())
avg = float((jF*sig).sum())
eq8_rhs = SG(pR, nT) - SG(pF, n0)
ptau = jF.sum(0)
eq44 = SG(ptau, nT) - SG(pF, n0) + float((ptau*np.log(ptau/pR)).sum())
klj = float((jF*np.log(jF/jR.T)).sum())
print(f"       <sigma_inv>                          = {avg:.4f}")
print(f"       Eq. (8) middle term  S_G(rho_R)-S_G(rho_F) = {eq8_rhs:.4f}   <-- NEGATIVE")
print(f"       Eq. (44) RHS  Delta S_G + D(p_tau||p_R)    = {eq44:.4f}")
print(f"       D_KL( p_F(k,l) || p_R(l,k) )               = {klj:.4f}")
check("Eq. (8) middle term is NOT <sigma_inv>  (WP-90 finding D1)",
      abs(avg - eq8_rhs) > 1e-3 and eq8_rhs < 0)
check("Eq. (44) and the joint KL both equal <sigma_inv>",
      abs(avg - eq44) < 1e-12 and abs(avg - klj) < 1e-12)

print()
print("=" * 74)
print("PART 2 — Bures geometry on the gauge-reduced space (WP-90 Prop. 2, 3)")
print("=" * 74)

rng = np.random.default_rng(11)
basis, degs = rand_unitary(rng, 6), [3, 2, 1]
def proj(k):
    i = sum(degs[:k]); P = np.zeros((6, 6), complex)
    for j in range(i, i + degs[k]):
        v = basis[:, j:j+1]; P += v @ v.conj().T
    return P
Ps = [proj(k) for k in range(3)]
gstate = lambda p: sum(pi/n*P for pi, n, P in zip(p, degs, Ps))
twirl  = lambda r: sum(np.trace(P @ r).real/n*P for P, n in zip(Ps, degs))

p, q = np.array([.5, .3, .2]), np.array([.2, .15, .65])
r0, r1 = gstate(p), gstate(q)
check("Bures angle between gauge-invariant states = Bhattacharyya angle "
      "arccos sum_k sqrt(p_k q_k)",
      abs(bures_angle(r0, r1) - np.arccos(np.sqrt(p*q).sum())) < 1e-12,
      f"{bures_angle(r0,r1):.12f}")

# Fix(G_T) is totally geodesic: the Bures geodesic between two of its points stays in it
W0 = sq(r0); Upol, _ = polar(sq(r0) @ sq(r1)); W1 = sq(r1) @ Upol.conj().T
th = bures_angle(r0, r1)
worst = max(abs((lambda W: W @ W.conj().T)((np.sin((1-s)*th)*W0 + np.sin(s*th)*W1)/np.sin(th))
                - twirl((lambda W: W @ W.conj().T)((np.sin((1-s)*th)*W0 + np.sin(s*th)*W1)/np.sin(th)))).max()
            for s in np.linspace(0, 1, 21))
check("Fix(G_T) totally geodesic: Bures geodesic stays gauge-invariant",
      worst < 1e-12, f"max deviation {worst:.2e}")

pts = [(lambda W: W @ W.conj().T)((np.sin((1-s)*th)*W0 + np.sin(s*th)*W1)/np.sin(th))
       for s in np.linspace(0, 1, 2001)]
L = sum(bures_angle(pts[i], pts[i+1]) for i in range(len(pts)-1))
check("that geodesic realises the Bures distance", abs(L - th) < 1e-6,
      f"length {L:.9f} vs angle {th:.9f}")

# Eq. (30) is the Pythagorean identity  C_rel + S_Gamma = S(rho || rho^E)
rng2 = np.random.default_rng(23)
X = rng2.normal(size=(6, 6)) + 1j*rng2.normal(size=(6, 6))
rho_ = X @ X.conj().T; rho_ /= np.trace(rho_).real
rE_ = twirl(rho_)
check("Eq. (30):  S_G[rho] - S_vN[rho] = S(rho || rho^E) = C_rel + S_Gamma",
      abs((vN(rE_) - vN(rho_)) - relent(rho_, rE_)) < 1e-10,
      f"{relent(rho_, rE_):.10f}")
best = min(relent(rho_, gstate(rng2.dirichlet(np.ones(3)))) for _ in range(20000))
check("rho^E is the relative-entropy projection onto Fix(G_T)",
      best >= relent(rho_, rE_) - 1e-12, f"random min {best:.6f} >= {relent(rho_,rE_):.6f}")

# ... but NOT the Bures-nearest point (WP-90 caveat C1)
f = lambda x: bures_angle(rho_, gstate(np.exp(x)/np.exp(x).sum()))
res = minimize(f, np.zeros(3), method="Nelder-Mead",
               options=dict(xatol=1e-11, fatol=1e-13, maxiter=40000, maxfev=40000))
w_near = np.exp(res.x)/np.exp(res.x).sum()
w_twirl = np.array([np.trace(P @ rho_).real for P in Ps])
check("rho^E is NOT the Bures-nearest gauge-invariant state (WP-90 caveat C1)",
      bures_angle(rho_, rE_) - res.fun > 1e-4,
      f"Bures dist to nearest {res.fun:.6f} < to twirl {bures_angle(rho_, rE_):.6f}")
print(f"       Bures-nearest weights {np.round(w_near,4)}   twirl weights {np.round(w_twirl,4)}")

print()
print("=" * 74)
print("PART 3 — the Deffner-Lutz bound as printed in Eq. (49)-(50)  (finding D2)")
print("=" * 74)

rng3 = np.random.default_rng(5)
bad_correct = bad_printed = 0; N = 4000
for _ in range(N):
    ra, rb = gstate(rng3.dirichlet(np.ones(3))), gstate(rng3.dirichlet(np.ones(3)))
    S = relent(ra, rb); rf = root_fidelity(ra, rb)
    Lc = np.arccos(np.clip(rf, -1, 1))        # arccos(sqrt F)  — Deffner-Lutz Bures angle
    Lp = np.arccos(np.clip(rf**2, -1, 1))     # arccos(F)       — Eq. (49) as printed
    if S < 8/np.pi**2*Lc**2 - 1e-12: bad_correct += 1
    if S < 8/np.pi**2*Lp**2 - 1e-12: bad_printed += 1
print(f"       violations of  S >= (8/pi^2) arccos^2(sqrt F) : {bad_correct} / {N}")
print(f"       violations of  S >= (8/pi^2) arccos^2(F)      : {bad_printed} / {N}")
check("bound holds with the Bures angle arccos(sqrt F)", bad_correct == 0)
check("bound FAILS with Eq. (49) as printed, arccos(F)  (finding D2)", bad_printed > 0,
      f"{bad_printed} counterexamples")

print()
print("=" * 74)
print("PART 4 — gauge covariance of the vertical velocity (WP-90 Prop. 1)")
print("=" * 74)

rng4 = np.random.default_rng(5); d = 6
X = rng4.normal(size=(d, d)) + 1j*rng4.normal(size=(d, d))
rho = X @ X.conj().T; rho /= np.trace(rho).real
rdot = herm(rng4.normal(size=(d, d)) + 1j*rng4.normal(size=(d, d)))
rdot -= np.trace(rdot).real/d*np.eye(d)
A = anti(rng4.normal(size=(d, d)) + 1j*rng4.normal(size=(d, d)))
nab = rdot + (A @ rho - rho @ A)
V = rand_unitary(rng4, d)
Om = anti(rng4.normal(size=(d, d)) + 1j*rng4.normal(size=(d, d)))*0.4
Vd = Om @ V
rho_g  = V @ rho @ V.conj().T
rdot_g = Vd @ rho @ V.conj().T + V @ rdot @ V.conj().T + V @ rho @ Vd.conj().T
A_g    = V @ A @ V.conj().T - Vd @ V.conj().T          # inhomogeneous connection rule
nab_g  = rdot_g + (A_g @ rho_g - rho_g @ A_g)
check("nabla_t rho transforms in the adjoint",
      abs(nab_g - V @ nab @ V.conj().T).max() < 1e-12,
      f"max dev {abs(nab_g - V @ nab @ V.conj().T).max():.2e}")
check("its Bures norm is gauge invariant",
      abs(bures_norm2(rho, nab) - bures_norm2(rho_g, nab_g)) < 1e-6,
      f"{bures_norm2(rho, nab):.6f}")

print()
print("=" * 74)
print("PART 5 — Q_c, W_inv, and Eq. (3) as printed  (finding D3)")
print("=" * 74)

rng5 = np.random.default_rng(3); d = 4
D_ = np.diag([-1.0, 0.2, 0.7, 2.0])
G_ = herm(rng5.normal(size=(d, d)) + 1j*rng5.normal(size=(d, d)))
u  = lambda t: expm(-1j*G_*t)                 # u_t diagonalises H_t:  u H u^dag = D
H  = lambda t: u(t).conj().T @ D_ @ u(t)      # spectrum constant, eigenbasis rotates
X = rng5.normal(size=(d, d)) + 1j*rng5.normal(size=(d, d))
r0_ = X @ X.conj().T; r0_ /= np.trace(r0_).real

def rho_t(t, n=4000):
    T = np.linspace(0, t, n); r = r0_.copy()
    for i in range(len(T)-1):
        dt = T[i+1]-T[i]; Ut = expm(-1j*H(T[i]+dt/2)*dt); r = Ut @ r @ Ut.conj().T
    return r

def twirl_t(t, r):                             # nondegenerate: diagonal in the H_t eigenbasis
    Ut = u(t); return Ut.conj().T @ np.diag(np.diag(Ut @ r @ Ut.conj().T)) @ Ut

t0, h = 0.6, 1e-5
A_t   = (u(t0+h) - u(t0-h))/(2*h) @ u(t0).conj().T
rE_t  = lambda t: twirl_t(t, rho_t(t))
rEdot = (rE_t(t0+h) - rE_t(t0-h))/(2*h)
rdot_ = (rho_t(t0+h) - rho_t(t0-h))/(2*h)
Hdot  = (H(t0+h) - H(t0-h))/(2*h)

lhs = float(np.trace(rho_t(t0) @ (H(t0) @ A_t - A_t @ H(t0))).real)   # Eq. (2), closed system
rhs = float(np.trace(rEdot @ H(t0)).real)                             # Eq. (13)/(24)
check("Eqs. (2) and (13) agree:  Tr(rho[H,A]) = Tr(H d/dt rho^E)",
      abs(lhs - rhs) < 1e-6, f"{lhs:.9f} vs {rhs:.9f}  (diff {abs(lhs-rhs):.1e})")
check("Q_u = 0 for the closed system",
      abs(float(np.trace(rdot_ @ H(t0)).real)) < 1e-7)
check("W_inv = 0 when the spectrum is constant (WP-90 Remark 5)",
      abs(float(np.trace(rE_t(t0) @ Hdot).real)) < 1e-7,
      f"W_inv rate {float(np.trace(rE_t(t0) @ Hdot).real):.3e}; "
      f"W_u rate {float(np.trace(rho_t(t0) @ Hdot).real):.9f} is all coherent heat")

udot = (u(t0+h) - u(t0-h))/(2*h)
ht   = u(t0) @ H(t0) @ u(t0).conj().T                       # h_t = u_t H_t u_t^dag, as stated
eq3  = float(np.trace(rho_t(t0) @ (udot @ ht @ u(t0).conj().T
                                   + u(t0) @ ht @ udot.conj().T)).real)
eq3b = float(np.trace(rho_t(t0) @ (udot.conj().T @ D_ @ u(t0)
                                   + u(t0).conj().T @ D_ @ udot)).real)
print(f"       Eq. (3) as printed          = {eq3:.9f}")
print(f"       with u <-> u^dag exchanged  = {eq3b:.9f}   (= Q_c rate {rhs:.9f})")
check("Eq. (3) as printed does not equal the Q_c it defines  (finding D3)",
      abs(eq3 - rhs) > 1e-3)
check("exchanging u and u^dag repairs it", abs(eq3b - rhs) < 1e-6)

print()
print("=" * 74)
print("ALL CHECKS PASSED" if not FAILED else "FAILURES: " + "; ".join(FAILED))
print("=" * 74)
raise SystemExit(1 if FAILED else 0)
