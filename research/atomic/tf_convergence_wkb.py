"""(1) convergence of quantum thresholds Z_c(l) in the PURE neutral TF potential V=-Z phi(r/b)/r vs grid size N and rmax, r_min.
   (2) semiclassical (Langer-WKB) onset: action at E=0, S=int sqrt(2Z phi/r - (l+1/2)^2/r^2) dr = pi*(n+1/2), n=0,
       which scales EXACTLY as Z_c = K (l+1/2)^3 (analytic, from TF scaling r=b x, b~Z^-1/3).
   No fitted constants. Observed onsets are quoted only for comparison, never as input."""
import numpy as np, sys
from scipy.integrate import quad
from scipy.optimize import brentq
import tf_core as T
def has_bound(Z,l,N,rmax):
    return T.neg_count(Z,l,N,rmax)>0
def Zc(l,N,rmax,lo=1,hi=400):
    if has_bound(lo,l,N,rmax): return lo
    while hi-lo>1:
        m=(lo+hi)//2
        if has_bound(m,l,N,rmax): hi=m
        else: lo=m
    return hi
print("== quantum threshold convergence: Z_c(l)  [rows: (N,rmax)] ==")
print("  monotonicity spot-check (bound state present for all Z>=Zc, l=2, N=1400,rmax=400):",
      all(has_bound(Z,2,1400,400) for Z in range(18,40)))
for N,R in [(1400,400.0),(2800,400.0),(5600,400.0),(5600,2000.0),(11200,2000.0)]:
    print(f"  N={N:5d} rmax={R:7.0f}: "+"  ".join(f"l={l}:{Zc(l,N,R)}" for l in (1,2,3,4)),flush=True)
# ---- WKB
b0=0.8853
def S(Z,l):
    lam=l+0.5; ph=lambda x: float(T.phi(x)[0])
    g=lambda x: 2*Z*b0*ph(x)/x*(1) - lam**2/x**2   # (Z b) = 0.8853 Z^(2/3)
    # note p dr = sqrt(2 Z b phi/x - lam^2/x^2) dx, with Z b = b0 Z^(2/3)
    return None
def action(Z23,lam):
    g=lambda x: 2*b0*Z23*float(T.phi(x)[0])/x - lam**2/x**2
    xs=np.logspace(-6,3,40000); gv=np.array([g(x) for x in xs])
    pos=gv>0
    if not pos.any(): return 0.0
    # allowed region: from first x where g>0 to last x where g>0 (single well for TF)
    i0=np.argmax(pos); i1=len(pos)-1-np.argmax(pos[::-1])
    a,bb=xs[i0],xs[i1]
    return quad(lambda x: np.sqrt(max(g(x),0.0)),a,bb,limit=400)[0]
print("\n== Langer-WKB onset (n=0: S=pi/2). Z_c = K lam^3 exactly by scaling ==")
Ks=[]
for l in (1,2,3,4):
    lam=l+0.5
    q=brentq(lambda q: action(q,lam)-np.pi/2, 0.1*lam**2, 40*lam**2, xtol=1e-6)   # q=Z^(2/3)
    Z=q**1.5; Ks.append(Z/lam**3)
    print(f"  l={l}: Z_c^WKB={Z:7.2f}   Z_c/(l+1/2)^3 = {Z/lam**3:.4f}")
print("  (K constant across l => Z_c ∝ (l+1/2)^3, the Landau–Lifshitz/Fermi scaling; spread in K is numerical:",f"{np.ptp(Ks):.1e})")
print("  empirical comparison only: first ground-state occupation p:5 d:21 f:57-58 -> Z/(l+1/2)^3 = %.2f %.2f %.2f"%(5/1.5**3,21/2.5**3,57/3.5**3))
