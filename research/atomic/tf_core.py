"""extracted from tf_retrodiction.py: TF function + radial solver (no Part 1/2 prints other than the phi check)"""
import numpy as np, itertools, sys
from scipy.integrate import solve_ivp
from scipy.linalg import eigh_tridiagonal
import scipy.sparse as sps
from scipy.sparse.linalg import eigsh
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
        # NOTE: eigh_tridiagonal(select='i') has abs. error ~ eps*||A|| ~ 1e-3..10 Ha on a log grid (||A||~1/(h r_min)^2): UNRELIABLE.
        # shift-invert Lanczos is accurate (hydrogen check: <1e-5 Ha).
        A=sps.diags([o,d,o],[-1,0,1],format='csc')
        w=np.sort(eigsh(A,k=nlev,sigma=-1.5*Z**2-1.0,which='LM',return_eigenvectors=False))
        out[l]=[e for e in w if e<0]
    return out

def neg_count(Z,l,N=2800,rmax=400.0,rmin_fac=1e-5):
    """Number of bound (E<0) radial states of angular momentum l in the PURE neutral TF potential: exact Sturm/inertia count of the
    tridiagonal operator (Sylvester's law; no eigenvalue solve, no roundoff sensitivity to ||A||)."""
    b=0.8853*Z**(-1/3)
    xi=np.linspace(np.log(rmin_fac/Z), np.log(rmax), N); h=xi[1]-xi[0]; r=np.exp(xi)
    V=-Z*phi(r/b)/r
    d=(1.0/h**2+(l+.5)**2/2)/r**2+V; o=(-0.5/h**2)/(r[:-1]*r[1:])
    q=d[0]; cnt=int(q<0)
    for i in range(1,N):
        if q==0: q=1e-300
        q=d[i]-o[i-1]**2/q; cnt+=int(q<0)
    return cnt
