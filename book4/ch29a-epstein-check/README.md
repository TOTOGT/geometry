# Checks behind book4/ch29a-epstein-saddle-and-minimum.html

All numerical; none is a proof.

- `ref.py`: Fourier-Bessel expansion of E(z,s)=sum' y^s/|m+nz|^(2s) in mpmath (40 digits); `python3 ref.py` compares it with a direct lattice sum at s=2,3.
- `ref2.py`: writes `ref.json`, the values and Hessians at i and rho for s=2,3,5 that the page embeds as its independent reference.
- `core.js`: the lattice-sum code the page runs (values, analytic first and second derivatives, tail estimate). `node t.js` compares it with `ref.json`, with mpmath derivatives at a generic point, and scans s in [1.5, 8] (step 0.05, R=300) for the Hessian sign pattern (saddle at i, minimum at rho). Result when written: no exceptions.
Requires: python3 with mpmath, node.
- `field.py`, `mkfig2.py`: the s=2 lattice-sum gradient (disc cutoff 80) and the generator of the local vector-field figure (contours, normalized grid arrows, RK4 integral curves, separatrix checks, d E/dt identity check) embedded in the page. Run from the repo root: `python3 book4/ch29a-epstein-check/mkfig2.py` (needs numpy, scipy, contourpy); it writes `/tmp/fig2.html`.
