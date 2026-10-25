# Pre-registration: how far is 11/12 from the Cobeli-Zaharescu method? (written before the run)

Date: 2026-10-25 (US Eastern). Source: arXiv:2610.23467v1 (Downloads/2610.23467v1.pdf), eq. (6.2).
Question asked by the editor: can the proportion of zeta zeros that are simple or on the line be
pushed from 0.88893 to 11/12 = 55/60 = 0.91667 (a gain of 0.0277)?

This is not an attempt to prove anything. It measures headroom inside the paper's own framework.

Q1 (reproduction). Recompute (6.2) from the paper's stated constants: alpha = 209/5000, d = 57/2000,
   tau = 2 + sqrt(2 - 2 alpha), C = 1.3313394 (their Remark 5.1), bound = 1 - 4(C-1-alpha+d)/tau^2.
   Pass: 0.88893 to five places. If it does not reproduce, nothing below is used.
Q2 (what 11/12 would take). Holding the form of (6.2) fixed, solve for the remainder coefficient alpha
   needed for 11/12 at (a) the paper's C and d, (b) C = C_MT = 1.3274992 and d = 0. Report the ratio to
   the paper's alpha = 0.0418.
Q3 (ideal-remainder proxy, heuristic). Rebuild K*(x) from the paper's f* (5.1). Check C(f*) = 1.3313394
   and f* >= 0.79 on I (control for the reconstruction). Then replace the local lemma's remainder by the
   lattice value n*e(s), e(s) = 2*sum_{k>=1} K*(ks)^2, s = L/n, and recompute the bound over the density
   nu = n/N. The lattice is NOT shown to minimise the remainder, so Q3 is a proxy for the headroom of
   better local analysis with the same f*, never a bound.
Outcome rule: report each number as computed. No conclusion beyond "what the arithmetic says".
