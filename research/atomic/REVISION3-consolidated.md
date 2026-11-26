# Revision 3 — consolidated report (published 2026-11-26 for review; analytical/numerical, nothing formally verified; Euler CI untouched)
Tags: [A] analytical · [N] numerical · [L] literature · [C] conjectural · [S] specification only · [F] formally verified (none).
Files in this repository: `research/atomic/{lsda_scf.py,pyscf_ref.py,cr_convergence_audit.py,*.log}`, `research/contact-nodal/{NODAL-THEOREM.md,nodal_theorem_checks.py}`, `research/axle/FORMALIZATION-TARGETS.md`, `research/atomic/ORTHOGENESIS-ACCESSIBILITY.md`. Earlier: REVISION2-report.md (TF retraction etc., preserved unchanged).

## A. Chromium controlled experiment
**A1. Independent check of the exchange-only reference energies [N].** Different code (PySCF Gaussian basis, `xc='lda,'` = Dirac exchange, no correlation; `pyscf_ref.py`): He −2.72271 (cc-pVTZ), −2.72350 (aug-QZ), −2.72359 (aug-5Z); Ne −127.46948, −127.48651, −127.49015. My radial code: He −2.723630, Ne −127.490633. Gaussian values approach the radial values monotonically from above with basis size and are within 1e-4 Ha (He) / 5e-4 Ha (Ne) at 5Z, i.e. consistent with the basis-set limit. The recalled literature values (He −2.7236, Ne −127.49) agree.
**A2. Convergence audit of the Cr gap [N]** (`cr_convergence_audit.py`; 4 SCFs per setting; every run converged, electron count error <4e-15):

| setting | unpolarized ΔE = E(4s¹3d⁵) − E(4s²3d⁴) | spin-polarized ΔE (S=3 vs S=2) |
|---|---|---|
| base: N=2400, r_max=45, r_min=1e-6/Z, mix 0.35, tol 1e-9 | +92.54 meV | −2598.55 meV |
| r_max=70 | +92.61 | −2598.49 |
| r_min=1e-7/Z, N=3000 | +92.23 | −2598.84 |
| N=3600 | +91.64 | −2599.38 |
| mix 0.2, E-tol 1e-11, V-tol 1e-8 | +92.54 | −2598.55 |
Final row recorded 2026-11-26: all five settings converged (E-tol 1e-9…1e-11), electron-count error ≤7.1e-15. Spread of ΔE across the five settings ≈ 0.9 meV unpolarized (91.64–92.61) and ≈0.9 meV polarized (−2599.38 to −2598.49), i.e. ≈1%, ≪ the 92 meV gap and ≪ the 2.6 eV polarized shift. The unpolarized 0.093 eV gap is therefore numerically real, not a convergence artefact; it is a property of the model (spin-unpolarized Dirac exchange).
**A3–A5. Spin-polarized pilot [N].** Same code path, same numerics (spin-polarized Dirac exchange, E_x=½(E_x[2ρ↑]+E_x[2ρ↓]), v_xσ=−(6ρσ/π)^{1/3}, Ar-like core with 9 up/9 down core electrons; unpolarized limit reproduces the old energies exactly: He −2.723630, Ne −127.490633, Cr(4s²3d⁴) −1040.036663, Cr(4s¹3d⁵) −1040.033263). Results:
| configuration | spin | N_el (↑,↓) | E (Ha) |
|---|---|---|---|
| 4s²3d⁴ unpolarized | S=0 (avg) | (12,12) | −1040.036663 |
| 4s¹3d⁵ unpolarized | S=0 (avg) | (12,12) | −1040.033263 |
| 4s²3d⁴ polarized | S=2 | (14,10) | −1040.179382 |
| 4s¹3d⁵ polarized | S=3 | (15,9) | −1040.274877 |
Spin polarization stabilises 4s¹3d⁵ by 6.6 eV and 4s²3d⁴ by 3.9 eV (relative to unpolarized), reversing the order: **E(4s¹3d⁵)−E(4s²3d⁴)=−2.60 eV**. A4 answer: **yes, spin polarization reverses the ordering**, matching the known Cr ground configuration. A7: this is conventional spin-dependent exchange (Hund-type), **attributed entirely to conventional physics; not a TOGT result.** Caveats [N/C]:  the magnitude (2.6 eV) is not compared with experiment here: I did not verify an experimental 7S–5D splitting, so no quantitative accuracy is claimed. High-spin over-stabilisation is a commonly reported LSDA tendency [L, recalled, unverified]; spherical averaging ignores multiplet structure of d⁴; one functional only. So: the sign matches the known ground configuration of Cr (4s¹3d⁵); the magnitude is unvalidated; no claim of quantitative accuracy.

## B. Orthogenetic hypothesis — see `ORTHOGENESIS-ACCESSIBILITY.md`
Result: **no selection law distinct from conventional physics emerged.** The accessibility formulation (ẋ=−G∇E; dE/dt=−∇EᵀG∇E≤0) is standard; for isolated-atom ground states accessibility either reduces to argmin or is unconstrained (free G, x(0)). One zero-parameter candidate (Z-continuation / hysteresis selection, fold-loss vs crossing) is specified before testing; I expect it to coincide with argmin because fractional-occupation energies are piecewise linear for the exact functional [L, recalled]; it is **not run**. In the Opus: TOGT's topography/orthogenesis split, DM3 conservative contact flows, a Lyapunov relaxation mechanism and a cubic-fold gradient flow exist; configuration manifold, mobility operator and initial conditions for atoms do not (new assumptions).

## C. Nodal theorem — see `NODAL-THEOREM.md`
(A) Leading term of any nonzero local solution of the eigen-equation with parity and modular symmetry at i is α·Re(w^k) with **k even** [A]. (B) Exceptional case: f₄=c40·Re w⁴ and f₅=−2c40·Im w⁵ [A, symbolic]. (C) For real f with α≠0: exactly k analytic curves through i with tangents at π/(2k)+jπ/k; **c40≠0 suffices for the full local nodal set, not only the leading polynomial** [A: polar blow-up + IFT; N: 8 sign changes in all 10 sample circles]. (D) complex f: statements limited to Re f, Im f separately. Not established: which (k,α) occur at actual zeros; degrees ≥6; μ=10. No constraint on global zero location.

## D. AXLE targets — see `FORMALIZATION-TARGETS.md`
T1 Jacobian=‖f′‖²; T2 contact nondegeneracy at simple zeros (coefficient-level); T3 harmonic polynomial classification (k=2,4 finite linear algebra); T4 quartic reduction lemma; T5 dissipation under PSD mobility. Duplicate check limited to project records (GitHub tree access refused this session). Speiser external/conditional. Lean text not written or run.

## E. Management
Preserved: TF retraction (2026-11-26), η_k negative result, all earlier tags. Final mix-variant row recorded (`cr_audit.log`): 92.54 meV / −2598.55 meV, converged.
