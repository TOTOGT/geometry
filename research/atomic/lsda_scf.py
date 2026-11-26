"""Spin-polarized Dirac-exchange (LSDA-x, NO correlation, no empirical parameter) spherical SCF, integer occupations per spin.
E_x[rho_u,rho_d]=1/2(E_x[2rho_u]+E_x[2rho_d]);  v_x,s = -(6 rho_s/pi)^(1/3);  Hartree from total density.
Unpolarized limit (rho_u=rho_d) reproduces lda_scf_pilot.py (checked in __main__).
Energy: E = sum_s sum_i n_is eps_is - E_H - sum_s int rho_s v_xs + E_x.
All numerical conditions (grid, mixing, tolerances) are explicit arguments; defaults = those of lda_scf_pilot.py."""
import numpy as np, sys, scipy.sparse as sps
from scipy.sparse.linalg import eigsh
def scf(Z,occ_u,occ_d,N=2400,rmax=45.0,rmin_fac=1e-6,iters=300,mix=0.35,tol=1e-9,vtol=1e-6):
    r=np.exp(np.linspace(np.log(rmin_fac/Z),np.log(rmax),N)); h=np.log(r[1]/r[0]); dV=4*np.pi*r**3*h
    spins={'u':occ_u,'d':occ_d}
    Vsc={s:np.zeros(N) for s in spins}; rho={s:None for s in spins}
    Vg=-(1.0+(Z-1.0)*np.exp(-r*Z**(1/3)*1.5))/r+Z/r
    for s in spins: Vsc[s]=Vg.copy()
    Eold=0; conv=False
    for it in range(iters):
        rn={}; Eband=0.0; eps={}
        for s,occ in spins.items():
            rhos=np.zeros(N)
            for l in sorted(set(l for (n,l) in occ)):
                nl=max(n-l for (n,ll) in occ if ll==l)
                d=(1/h**2+(l+.5)**2/2)/r**2-Z/r+Vsc[s]; o=(-0.5/h**2)/(r[:-1]*r[1:])
                A=sps.diags([o,d,o],[-1,0,1],format='csc')
                w,y=eigsh(A,k=nl,sigma=-1.5*Z**2-1.0,which='LM'); ix=np.argsort(w); w=w[ix]; y=y[:,ix]
                for k in range(nl):
                    n=k+l+1
                    if (n,l) in occ and occ[(n,l)]>0:
                        P2=y[:,k]**2/r; P2/=(P2*r).sum()*h
                        rhos+=occ[(n,l)]*P2/(4*np.pi*r**2); eps[(s,n,l)]=w[k]; Eband+=occ[(n,l)]*w[k]
            rn[s]=rhos
        for s in spins: rho[s]=rn[s] if it==0 else (1-mix)*rho[s]+mix*rn[s]
        rt=rho['u']+rho['d']
        Q=np.cumsum(rt*dV)-0.5*rt*dV; outer=np.cumsum((4*np.pi*rt*r**2*h)[::-1])[::-1]-0.5*4*np.pi*rt*r**2*h
        VH=Q/r+outer
        err=0; Evx=0; Ex=0
        for s in spins:
            vx=-(6*np.maximum(rho[s],0)/np.pi)**(1/3)
            Vn=VH+vx; err=max(err,np.max(np.abs(Vn-Vsc[s])*r))
            Vsc[s]=Vn if it==0 else (1-mix)*Vsc[s]+mix*Vn
            Evx+=np.sum(rho[s]*vx*dV); Ex+=np.sum(rho[s]*0.75*vx*dV)
        E=Eband-0.5*np.sum(rt*VH*dV)-Evx+Ex
        if it>5 and abs(E-Eold)<tol and err<vtol: conv=True; break
        Eold=E
    nel=(np.sum(rho['u']*dV),np.sum(rho['d']*dV))
    return dict(E=E,it=it,conv=conv,nel=nel,dE=abs(E-Eold),err=err,eps=eps)
AR={(1,0):1,(2,0):1,(2,1):3,(3,0):1,(3,1):3}   # per spin
def cr(extra_u,extra_d,**kw):
    u=dict(AR); u.update(extra_u); d=dict(AR); d.update(extra_d); return scf(24,u,d,**kw)
if __name__=="__main__":
    Ha=27.211386
    r=scf(2,{(1,0):1},{(1,0):1}); print(f"He unpolarized-limit: E={r['E']:.6f}  it={r['it']} conv={r['conv']} nel={r['nel']}")
    r=scf(10,{(1,0):1,(2,0):1,(2,1):3},{(1,0):1,(2,0):1,(2,1):3}); print(f"Ne unpolarized-limit: E={r['E']:.6f}")
    # check against the previous (unpolarized) Cr numbers: 4s2 3d4 = -1040.036663 ; 4s1 3d5 = -1040.033263
    R={}
    cases={'unpol 4s2 3d4 (S=0 avg)':({(4,0):1,(3,2):2},{(4,0):1,(3,2):2}),
           'unpol 4s1 3d5 (S=0 avg)':({(4,0):0.5,(3,2):2.5},{(4,0):0.5,(3,2):2.5}),
           'pol   4s2 3d4  S=2':({(4,0):1,(3,2):4},{(4,0):1}),
           'pol   4s1 3d5  S=3':({(4,0):1,(3,2):5},{}),
           'pol   4s1 3d5  S=3 (check 4s dn=0)':({(4,0):1,(3,2):5},{})}
    for k,(u,d) in list(cases.items())[:4]:
        r=cr(u,d); R[k]=r['E']; print(f"Cr {k:28s} E={r['E']:.6f} Ha  it={r['it']} conv={r['conv']} N_el(u,d)=({r['nel'][0]:.4f},{r['nel'][1]:.4f}) dE_last={r['dE']:.1e} verr={r['err']:.1e}",flush=True)
    a,b=R['unpol 4s2 3d4 (S=0 avg)'],R['unpol 4s1 3d5 (S=0 avg)']
    print(f"UNPOLARIZED:  E(4s1 3d5)-E(4s2 3d4) = {(b-a)*Ha*1000:.2f} meV   (positive => 4s2 3d4 lower)")
    a,b=R['pol   4s2 3d4  S=2'],R['pol   4s1 3d5  S=3']
    print(f"POLARIZED:    E(4s1 3d5,S=3)-E(4s2 3d4,S=2) = {(b-a)*Ha*1000:.2f} meV   (negative => 4s1 3d5 lower, matches experiment)")
