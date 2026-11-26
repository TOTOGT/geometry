# Research notes, November 2026 (Principia Orthogona / TOGT / AXLE) — status: analytical and numerical reports, pending independent review
Layout: `atomic/`, `contact-nodal/`, `axle/`, `jurisprudence/`. Nothing here is formally verified (no Lean). Negative results and numerical corrections are kept on purpose. Tags: [A] analytical · [N] numerical · [L] literature · [C] conjectural · [S] specification only.

**Web version:** the research portal is at `research/index.html` (published via GitHub Pages) with MathJax-enabled pages for each report.

## Atomic structure (computational physics) — `atomic/`
- `REVISION3-consolidated.md` — chromium: independent PySCF benchmark, grid-convergence audit (5 settings, all converged), spin-polarized pilot. **The ordering reversal is due to conventional spin-dependent exchange; it is not a TOGT prediction.**
- `REVISION2-report.md` — **dated retraction (2026-11-26)** of the first Thomas–Fermi thresholds (2, 18, 64, 164: roundoff artefact); corrected values p/d/f/g = 7/26/67/135 (Sturm count, grid-independent) with a Langer–WKB cross-check. A bound-state threshold is not an occupied ground-state configuration.
- `Q05b-research-addendum.md` — negative result for the η_k hierarchy as a generator of shell capacities/closings.
- `ORTHOGENESIS-ACCESSIBILITY.md` — open research direction; no selection law distinct from energy minimization found.
- Scripts: `tf_core.py`, `tf_retrodiction.py`, `tf_convergence_wkb.py`, `lda_scf_pilot.py`, `lsda_scf.py`, `pyscf_ref.py`, `cr_convergence_audit.py`; logs `*.log`. (Python 3, numpy/scipy; `pyscf_ref.py` needs PySCF.)

## Contact geometry and nodal analysis (no implication for the Riemann hypothesis) — `contact-nodal/`
- `kk-zeta-lift-analysis.md`, `kk_zeta_lift_checks.py` — Boothby–Wang-type lifts of the zeta plane; includes the erratum: η = dz + Re ζ d Im ζ is smooth through every zero of ζ and **contact only at simple zeros** (η∧dη = |ζ′|² dz∧dσ∧dt).
- `regularized_contact_checks.py` — Jacobian identity and simple/multiple-zero checks.
- `NODAL-THEOREM.md` + `nodal_taylor.py`, `nodal_taylor_numcheck.py`, `nodal_theorem_checks.py`, `nodal_addendum_checks.py` — local nodal structure at z=i. Local symmetry does not constrain the global location of zeros.

## AXLE formalization targets (proposed and untested; no Lean verification) — `axle/`
- `FORMALIZATION-TARGETS.md` — specifications only; Speiser's criterion stays an explicit external hypothesis.

## Computational Jurisprudence (new workstream; Phase I) — `jurisprudence/`
- `PHASE-I-computational-jurisprudence.md` — original research report and plan. The al-Khwārizmī/inheritance connection is **unverified** (not checked against primary or scholarly sources). The 1968 Black's Law Dictionary scan, its OCR text, extracted definitions and the pilot data are **not published** (copyright; kept private). Opus volume: Book XXXI is reserved provisionally for this workstream (see `../book31/index.html`).
