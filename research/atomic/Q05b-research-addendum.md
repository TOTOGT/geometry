# Q.0.5b research addendum — does the η_k hierarchy generate the periodic table?
Status: research note published 2026-11-26, for review. Everything below is a retrodiction test, not a prediction method.
Script: `tf_retrodiction.py` (this folder). All numbers are from that script unless marked "from memory".

## 1. Question
Q.0.5b states that the periodic table "is a table of η_k hierarchies". Test: does the original model, with its definitions and no inserted data, generate (i) shell capacities, (ii) filling order, (iii) the closings 2, 10, 18, 36, 54, 86, 118?

## 2. Original model: result NEGATIVE
- η_k = largest root of λ^k = λ^{k-1}+…+1 (k-nacci constant; 1.618, 1.839, 1.928, …, →2). It is asserted from a "Planck-scale recurrence", not derived.
- Tested every k = 2..9: no integer sequence built from η_k (floors, ceilings, rounded multiples, k-nacci integers, partial sums) contains the period lengths 2,8,8,18,18,32,32, the capacities 2,6,10,14, or the closings as a consecutive block. (Part 1 of the script.)
- The explanation in Q.0.5b for period lengths via n² capacities is wrong as stated: shell n holds 2n² electrons only in the hydrogenic picture, whereas periods are 2,8,8,18,18,32,32 — each repeated, which n² does not produce. This is an untagged claim in the source and should be tagged or removed.
- Conclusion: the η_k hierarchy as defined has no generator for shell capacities or filling order. Preserved as a negative result.

## 3. Thomas–Fermi baseline (NEW MODEL, not the Opus) — CORRECTED 2026-11-26 (Revision 2)
**The thresholds in the first version of this section (2, 18, 64, 164) are RETRACTED**: they were roundoff artefacts of `eigh_tridiagonal` on a log grid (error ~eps·||A|| ≫ near-threshold energies; hydrogen test failed). With an exact Sturm/inertia count the thresholds are grid-independent (N=1400…11200, r_max=400…2000):

| l | model Z_c (converged) | Langer–WKB | observed first ground-state occupation |
|---|---|---|---|
| p | 7 | 6.8 | B (5) |
| d | 26 | 26.3 | Sc (21) |
| f | 67 | 66.5 | La/Ce (57–58) |
| g | 135 | 134.9 | none observed; 5g is a theoretical candidate (see §5) |

Numerical error is not the source of the gap; it is physics-model limits: existence of a bound l-state in the neutral potential is not occupation in the ground state (He already has bound 2p), plus missing exchange and relativity (untested individually). Full derivations, the LDA pilot (K–Zn total-energy comparisons; Cr is a 0.09 eV near-tie), status tags and scripts: `REVISION2-report.md`.

## 4. Distinctions required
- Orbital capacity (2(2l+1)): kinematic, from angular momentum; not an η_k outcome.
- Occupancy/ground configuration: needs electron–electron screening; TF one-electron levels do not settle the Madelung exceptions (Cr, Cu, Pd, La, Ce, …).
- Atomic stability: a chemical statement; unrelated to nuclear stability.
- Nuclear stability: governed by nuclear shell structure and Coulomb fission barriers, not by the electron-shell closings. Nothing here says Z ≥ 119 nuclei exist long enough to be atoms.

## 5. Z ≥ 119 (checked against primary pages 2026-11-26)
Not predicted by this work. Pyykkö, PCCP 13, 161 (2011): extended-average-level Dirac–Fock; rough filling order 8s < 5g ≤ 8p1/2 < 6f < 7d < 9s < 9p1/2 < 8p3/2; ranges quoted from earlier Dirac–Slater work (8p1/2+5g ≈121–143, 6f 144–154, 7d 155–164, 165–172 for 9s/9p1/2/8p3/2); QED dropped above Z=137; lifetimes above 118 too short for chemistry. Savelyev et al., arXiv:2301.01740: only partly read; where 5g begins is NOT verified. Electronic-configuration predictions are not predictions of nuclear existence. g-shell appearances are never observed.

## 6. Verdict
- Original η_k model: fails to generate capacities, order or closings. Negative result retained.
- Any extension (TF, Hartree–Fock, relativistic) is a new model and should be labelled so; it is established physics, not an orthogenetic derivation.
- Open: whether an orthogenetic selection principle can *select* the Madelung order from a landscape. No candidate is on the table.
