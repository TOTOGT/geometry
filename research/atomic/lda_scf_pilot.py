"""Pilot: spherical, non-relativistic, parameter-free SCF with Hartree + Dirac (Slater, alpha=1... i.e. LDA-exchange-only) potential.
It is NOT Hartree-Fock (no exact exchange, self-interaction uncorrected, no correlation, no spin polarization, no relativity).
Purpose: use a TOTAL-ENERGY functional E[occupations] to test whether 'preferred configuration' ordering for 3d vs 4s
comes out of the functional rather than being inserted. Compares fixed integer-occupation configurations."""
import numpy as np, sys
import scipy.sparse as sps
from scipy.sparse.linalg import eigsh
def scf(Z,occ,N=2400,rmax=45.0,iters=200,mix=0.35,tol=1e-9):
    r=np.exp(np.linspace(np.log(1e-6/Z),np.log(rmax),N)); h=np.log(r[1]/r[0])
    lmax=max(l for (n,l) in occ); need={l:max(n-l for (n,ll) in occ if ll==l) for l in range(lmax+1) if any(ll==l for (_,ll) in occ)}
    rho=None; Vsc=np.zeros(N); Eold=0
    # start: screened hydrogenic guess
    Vsc=-(1.0+(Z-1.0)*np.exp(-r*Z**(1/3)*1.5))/r+ Z/r  # added to -Z/r below => Vtot = -Zeff(r)/r
    for it in range(iters):
        Vt=-Z/r+Vsc
        rhon=np.zeros(N); eps={}; Eband=0.0
        for l,nl in need.items():
            d=(1/h**2+(l+.5)**2/2)/r**2+Vt; o=(-0.5/h**2)/(r[:-1]*r[1:])
            A=sps.diags([o,d,o],[-1,0,1],format='csc'); w,y=eigsh(A,k=nl,sigma=-1.5*Z**2-1.0,which='LM'); ix=np.argsort(w); w=w[ix]; y=y[:,ix]
            for k in range(nl):
                n=k+l+1
                if (n,l) in occ:
                    P2=(y[:,k]**2)/r; P2/= (P2*r).sum()*h      # int P^2 dr = sum P2 r h
                    rhon+=occ[(n,l)]*P2/(4*np.pi*r**2); eps[(n,l)]=w[k]; Eband+=occ[(n,l)]*w[k]
        rho=rhon if rho is None else (1-mix)*rho+mix*rhon
        dV=4*np.pi*r**3*h       # 4 pi r^2 dr
        Q=np.cumsum(rho*4*np.pi*r**3*h); Q-=0.5*rho*4*np.pi*r**3*h
        outer=np.cumsum((4*np.pi*rho*r**2*h)[::-1])[::-1]-0.5*(4*np.pi*rho*r**2*h)   # int_r^inf 4 pi rho r' dr' = sum 4pi rho r'^2 dxi
        VH=Q/r+outer
        vx=-(3*np.maximum(rho,0)/np.pi)**(1/3); ex=0.75*vx
        Vnew=VH+vx
        err=np.max(np.abs(Vnew-Vsc)*r) ; Vsc=(1-mix)*Vsc+mix*Vnew if it>0 else Vnew
        # total energy with density rho (consistent at convergence)
        EH=0.5*np.sum(rho*VH*dV); Ex=np.sum(rho*ex*dV); Evx=np.sum(rho*vx*dV)
        E=Eband-EH-Evx+Ex - (0)   # Eband used the (Vsc) potential: eigenvalues include int rho(VH+vx)
        if it>5 and abs(E-Eold)<tol and err<1e-6: break
        Eold=E
    return E,eps,it,np.sum(rho*dV)
CORE_AR={(1,0):2,(2,0):2,(2,1):6,(3,0):2,(3,1):6}
def cfg(base,**kw):
    c=dict(base); c.update({k:v for k,v in kw.items()}); return c
def run(Z,label,conf):
    E,eps,it,nel=scf(Z,conf); print(f"  Z={Z:2d} {label:28s} E={E:12.6f} Ha  (iters {it}, N_el={nel:.4f})",flush=True); return E
if __name__=="__main__":
    print("sanity: He (exchange-only LDA; exact HF is -2.8617 Ha):"); run(2,"1s2",{(1,0):2})
    print("sanity: Ne"); run(10,"1s2 2s2 2p6",{(1,0):2,(2,0):2,(2,1):6})
    Ar=CORE_AR; res={}
    tests=[ (19,"K",[("4s1",{(4,0):1}),("3d1",{(3,2):1})]),
            (20,"Ca",[("4s2",{(4,0):2}),("4s1 3d1",{(4,0):1,(3,2):1}),("3d2",{(3,2):2})]),
            (21,"Sc",[("4s2 3d1",{(4,0):2,(3,2):1}),("4s1 3d2",{(4,0):1,(3,2):2}),("3d3",{(3,2):3})]),
            (24,"Cr",[("4s2 3d4",{(4,0):2,(3,2):4}),("4s1 3d5",{(4,0):1,(3,2):5})]),
            (29,"Cu",[("4s2 3d9",{(4,0):2,(3,2):9}),("4s1 3d10",{(4,0):1,(3,2):10})]),
            (30,"Zn",[("4s2 3d10",{(4,0):2,(3,2):10}),("4s1 3d10 4p1",{(4,0):1,(3,2):10,(4,1):1})]) ]
    for Z,name,cs in tests:
        print(name); Es=[]
        for lab,extra in cs:
            c=dict(Ar); c.update(extra); Es.append((run(Z,lab,c),lab))
        Es.sort(); print(f"   -> lowest-energy configuration in this functional: {Es[0][1]}   (gap to next: {(Es[1][0]-Es[0][0])*27.2114:.3f} eV)")
