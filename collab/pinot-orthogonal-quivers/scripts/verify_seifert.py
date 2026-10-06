"""Seifert data of the Reeb (Hopf) fibration on S^3/Gamma and the orbifold Euler-characteristic identity
chi_orb(base) = 2/|Gamma_bar|, Gamma_bar = image of Gamma in SO(3) = Gamma/(Gamma ∩ {±1})."""
from fractions import Fraction as F
def chi(cones): return F(2) - sum(1 - F(1, a) for a in cones)
for m in range(2, 30):                     # cyclic Z_m  (A_{m-1})
    gbar = m if m % 2 else m//2
    cones = (m, m) if m % 2 else (m//2, m//2)
    assert chi(cones) == F(2, gbar), m
for k in range(2, 30):                     # binary dihedral order 4k (D_{k+2}), image dihedral of order 2k
    assert chi((2, 2, k)) == F(2, 2*k), k
print("orbifold Euler characteristic identity holds for Z_m (m<30) and BD_4k (k<30)")
# group orders for the corrected table
for n in range(3, 9):
    print(f"n={n}: (D~_2n-2,v): D_{2*n-2}, |Gamma|={4*(2*n-4)} ;  (D~_2n-1,a): D_{2*n-1}, |Gamma|={4*(2*n-3)} ; (A~_2n-1,c): D_{n+2}, |Gamma|={4*n}")
