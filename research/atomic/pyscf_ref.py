"""Independent check of exchange-only LDA total energies (different code: PySCF Gaussian basis; basis-limited, expect ~1e-3..1e-2 Ha above the basis-set-limit)."""
from pyscf import gto, dft
for atom,spin,name in (("He",0,"He"),("Ne",0,"Ne")):
    for basis in ("cc-pVTZ","aug-cc-pVQZ","aug-cc-pV5Z"):
        try:
            m=gto.M(atom=atom,basis=basis,spin=spin,verbose=0); mf=dft.RKS(m); mf.xc='lda,'; mf.grids.level=9; mf.conv_tol=1e-11
            e=mf.kernel(); print(f"{name} LDA exchange-only (xc='lda,') {basis:12s} E={e:.6f} Ha  converged={mf.converged}",flush=True)
        except Exception as ex: print(name,basis,"ERR",ex)
