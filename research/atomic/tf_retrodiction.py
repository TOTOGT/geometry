#!/usr/bin/env python3
"""
Periodic-table retrodiction, standard-physics baseline (NOT the eta_k model).
Part 1: does the Opus eta_k / k-nacci hierarchy generate the shell capacities or the closings?  (pure arithmetic)
Part 2: does a PARAMETER-FREE Thomas-Fermi (+Latter tail) one-electron model derive the Madelung ordering and
        closings 2,10,18,36,54,86,118?  Inputs: Z only.  No fitted constants, no periodic-table data.
Output: PASS/FAIL per check; exit 0 always (these are measurements, not assertions of success).
"""
import numpy as np, itertools, sys
from scipy.integrate import solve_ivp
from scipy.linalg import eigh_tridiagonal

CLOSE = [2,10,18,36,54,86,118]; PERIOD = [2,8,8,18,18,32,32]; CAP = [2,8,18,32]
# ---------------- Part 1: eta_k / k-nacci --------------------------------------------------------------
def knacci(k, n=40):
    a=[0]*(k-1)+[1]
    while len(a)<n: a.append(sum(a[-k:]))
    return a
print("== Part 1: k-nacci / eta_k as generators ==")
targets = {"period lengths 2,8,8,18,18,32,32":PERIOD, "closings 2,10,18,36,54,86,118":CLOSE, "capacities 2,8,18,32":CAP}
found_any=False
for k in range(2,10):
    seq=knacci(k,60); pref=list(itertools.accumulate(seq))
    for name,t in targets.items():
        # (i) appears as consecutive terms of the sequence; (ii) of its prefix sums; (iii) as floor/round of eta^m multiples
        for lab,s in (("terms",seq),("partial sums",pref)):
            for i in range(len(s)-len(t)+1):
                if s[i:i+len(t)]==t: print(f"  k={k}: {name} found as consecutive {lab}"); found_any=True
print("  eta_k-derived integer sequences containing any of the targets as a consecutive block:", "YES" if found_any else "NONE (k=2..9; terms and partial sums)")
fib=knacci(2,14); print("  Fibonacci terms:",fib[:14]); print("  Tribonacci terms:",knacci(3,14))
print("  Note: 2(2l+1) subshell capacities and the n+l rule involve no eta_k; Q.0.5b's 'because n^2 capacities' also fails:")
print("  n^2-type capacities give periods 2,8,18,32 (each once); observed periods repeat: 2,8,8,18,18,32,32.")
# ---------------- Madelung baseline (an ASSUMED ordering) ---------------------------------------------
orb=sorted([(n+l,n,l) for n in range(1,9) for l in range(0,5) if l<n])
tot=0; closings=[]; seq=[]
for nl,n,l in orb:
    tot+=2*(2*l+1); seq.append(f"{n}{'spdfg'[l]}")
cum=list(itertools.accumulate(2*(2*l+1) for _,n,l in orb))
print("\n== Madelung (n+l, then n) is an INPUT, not a derivation ==")
print("  order:",' '.join(seq[:20])); print("  cumulative:",cum[:20])
mc=[c for (nl,n,l),c in zip(orb,cum) if l==0 and n>=1 and (n+l)>=0]
# closings = cumulative count just before each ns with l=0 (n>=2) starts, i.e., after np closes
madel_close=[]
for i,(nl,n,l) in enumerate(orb):
    if l==0 and i>0: madel_close.append(cum[i-1])
print("  closings from Madelung:",madel_close[:8], " observed:",CLOSE)
# ---------------- Part 2: Thomas-Fermi atom ------------------------------------------------------------
print("\n== Part 2: Thomas-Fermi (+Latter) one-electron model, Z only ==")
def _run(s0,X=30.0):
    x0=1e-6                                   # series start: phi = 1 + s x + (4/3) x^1.5 + (2/5) s x^2.5
    ph=1+s0*x0+4/3*x0**1.5+0.4*s0*x0**2.5; dph=s0+2*x0**0.5+s0*x0**1.5
    ev=lambda x,y: y[0]; ev.terminal=True      # phi hits zero  -> slope too steep
    ev2=lambda x,y: y[1]; ev2.terminal=True    # phi' hits zero -> slope too shallow
    f=lambda x,y:[y[1], max(y[0],0)**1.5/np.sqrt(x)]
    return solve_ivp(f,[x0,X],[ph,dph],rtol=1e-13,atol=1e-18,dense_output=True,method="DOP853",events=[ev,ev2])
def tf_phi():
    lo,hi=-1.6,-1.57                          # bisect phi'(0) so the neutral-atom solution decays to x=30 (no fitted constant)
    for _ in range(80):
        mid=(lo+hi)/2
        if len(_run(mid).t_events[0])>0: lo=mid
        else: hi=mid
    return _run((lo+hi)/2)
SOL=tf_phi(); XC=25.0; PHIC=float(SOL.sol(XC)[0])      # trusted to XC; beyond that phi ~ x^-3
print("  TF function check: phi(1),phi(2),phi(5),phi(10) =",[round(float(SOL.sol(x)[0]),4) for x in (1,2,5,10)],"(literature: 0.4240, 0.2430, 0.0788, 0.0243)")
def phi(x):
    x=np.atleast_1d(np.asarray(x,float)); y=SOL.sol(np.minimum(x,XC))[0]
    return np.where(x>XC, PHIC*(XC/np.maximum(x,1e-12))**3, np.maximum(y,0.0))
def levels(Z, lmax=4, nlev=9, N=900, latter=True, rmax=120.0):
    b=0.8853*Z**(-1/3)
    xi=np.linspace(np.log(1e-5/Z), np.log(rmax), N); h=xi[1]-xi[0]; r=np.exp(xi)
    V=-(np.maximum(Z*phi(r/b),1.0) if latter else Z*phi(r/b))/r   # Latter tail (asymptotic charge 1) or pure TF
    out={}
    for l in range(lmax+1):
        d=(1.0/h**2+(l+.5)**2/2)/r**2 + V            # D^-1/2 A D^-1/2 with D = diag(r^2): tridiagonal, symmetric
        o=(-0.5/h**2)/(r[:-1]*r[1:])
        w=eigh_tridiagonal(d,o,select='i',select_range=(0,nlev-1),eigvals_only=True)
        out[l]=[e for e in w if e<0]
    return out
def aufbau(Z):
    lev=levels(Z); orbs=[]
    for l,es in lev.items():
        for k,e in enumerate(es): orbs.append((e,k+l+1,l))
    orbs.sort(); return orbs
def order_at(Z,nshow=24):
    o=aufbau(Z); return [f"{n}{'spdfg'[l]}" for e,n,l in o][:nshow], o
# sanity: hydrogen-like check on the solver (pure Coulomb)
def hyd_check():
    N=1200; xi=np.linspace(np.log(1e-5),np.log(200),N); h=xi[1]-xi[0]; r=np.exp(xi); V=-1.0/r
    out=[]
    for l in (0,1):
        d=(1.0/h**2+(l+.5)**2/2)/r**2+V; o=-0.5/h**2/(r[:-1]*r[1:])
        out.append(eigh_tridiagonal(d,o,select='i',select_range=(0,2),eigvals_only=True))
    return out
hc=hyd_check(); print("  solver sanity, hydrogen: E(1s,2s,3s)=",np.round(hc[0],4),"expected -0.5,-0.125,-0.0556; E(2p,3p)=",np.round(hc[1][:2],4),"expected -0.125,-0.0556")
# energy-ordered subshell sequence and cumulative capacity at several Z
for Z in (18,86,118):
    names,o=order_at(Z,26); cap=list(itertools.accumulate(2*(2*l+1) for e,n,l in o))
    print(f"  Z={Z}: energy order:",' '.join(names)); print("        cumulative capacity:",cap[:26])
# first appearance thresholds with the PURE TF potential (no Latter tail; the Landau-Lifshitz criterion)
print("\n  Thresholds Z_c(l): smallest Z with a bound l-state (E<0) in the pure neutral TF potential  V=-Z phi(r/b)/r")
print("   (observed first occupation of an l-subshell in ground states: p->B(5), d->Sc(21), f->La/Ce(57-58), g: none yet known;")
print("    the classical Landau-Lifshitz/Fermi TF thresholds quoted in the literature are ~5, ~21, ~55, ~121 -- from memory, not re-fetched)")
for l in (1,2,3,4):
    zc=None
    for Z in range(2,260):
        e=levels(Z,lmax=l,nlev=2,N=1400,latter=False,rmax=400.0)[l]
        if e: zc=Z;break
    print(f"   l={l} ('{'spdfg'[l]}'): Z_c={zc}")
