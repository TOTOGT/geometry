# Independent re-run of GS-3 checks (2026-11-28)

`gs3check.py` (python3, mpmath, numpy; ~1 minute) re-derives, from the formulas in the chapter, without the chapter's own scripts:

- phi(s)=Lambda(2s-1)/Lambda(2s) against the closed form sqrt(pi)Gamma(s-1/2)zeta(2s-1)/(Gamma(s)zeta(2s)), and phi(s)phi(1-s)=1, at the chapter's first three test points (30 digits; agreement ~1e-31);
- the residue of phi at s=1 against 3/pi;
- the identity term of the heat trace against (1/12)(1/t-1/12)e^{-t/4} at t=0.1, 0.03, 0.01;
- the shortest closed geodesic length 2 log((3+sqrt5)/2) = 2 arccosh(3/2);
- E*(i,s) = 2 pi^-s Gamma(s) zeta(s) L(s,chi_-4) and E*(rho,s) = 3 (sqrt3/2pi)^s Gamma(s) zeta(s) L(s,chi_-3) at s=2.5 against a direct lattice sum with E*(z,s)=(1/2) pi^-s Gamma(s) sum' y^s/|m+nz|^(2s) (agreement ~1e-11).

Not re-run here: the nodal-distance tables, the first Maass parameter r_1, the resonance growth numbers, and all figures. The chapter's own generator scripts (run_numerics.py, run_i.py, numerics*.json) are not in this repository.
