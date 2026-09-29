# Open Questions — The Swarm Simulator

Status as of Version 3, September 2026. Tracked in the AXLE issue tracker: https://github.com/TOTOGT/AXLE

Every "proved" below is a theorem in `SwarmSimulator.lean` (V3), checked with Lean 4.32.0 and Mathlib v4.32.0, axioms [propext, Classical.choice, Quot.sound], no `sorry`. Every "computed" is checked by `python swarm_simulator.py --check`.

| ID | Question (as asked in V2) | V3 status | What settled it | Lean |
|----|---------------------------|-----------|-----------------|------|
| S1 | Full Banach contraction proof of Theorem 5.1 (G_swarm contracts on R⁴, ℓ¹ norm, when L_I + L_C + L_M < 1) | **Closed by restatement.** Theorem 5.1 as printed is false, and a corrected statement is proved. | The C-update multiplies two state variables (C·I), so G_swarm has no global Lipschitz constant (`no_global_lipschitz`). On the ball ‖X‖₁ ≤ R it has constant λ(R) = max(a(1 + cR), m), which is below 1 exactly for R < (1 − a)/(a·c) (about 3.51 for the default parameters). Uniqueness is proved directly (`fixed_point_zero`), without Mathlib's contraction-mapping theorem. | `step_lipschitz_ball`, `fixed_point_zero`, `no_global_lipschitz`, `default_radius` |
| S2 | Multi-orbit existence (§6): clusters converge to distinct fixed points X*_i | **Refuted as stated for this model.** | Any two parameter sets satisfying the ball condition have the same fixed point 0 in (I, C, M) (`two_clusters`). The clusters of the V2 figure 4 had L = 2.41 and 1.93, so neither satisfied the condition; both ran to 0 numerically. V2's T9 (Inv(S) > max Inv(Oᵢ)) is true by construction, because `systemInv` is defined as the maximum plus 1, and says nothing about the swarm. Distinct fixed points would need a model with a source term. | `two_clusters` |
| S3 | Empirical calibration of the default parameters | **Open.** No data held. | Calibration against Sinhuber et al. (2019) or Nitti et al. (2025) has not been attempted. A calibration would also have to reproduce shared intent that persists, and this model sends I, C, M to 0 (I_t = I₀·0.416^t exactly). | none |
| S4 | Discrete Gronwall bound (Theorem 5.3): ‖X_t − X*‖ ≤ L^t ‖X₀ − X*‖ | **Closed by restatement.** The printed bound fails from large starts and holds from small ones. | Proved: ‖X_t‖ ≤ ρ(R)^t ‖X₀‖ with ρ(R) = max(a, a·c·R, m), for every start in the ball where ρ ≤ 1 (`orbit_nrm_le`). The printed L^t bound holds when ‖X₀‖ ≤ 1 (`paper_bound`). From (100, 10, 1) it fails: one step gives 208.231 against L·111 = 90.2874 (`printed_bound_fails`). | `orbit_nrm_le`, `paper_bound`, `printed_bound_fails` |

## New in V3

| ID | Finding | Status |
|----|---------|--------|
| S5 | The diffusion coordinate F_t = 1 + αt has no upper bound (`diffuse_unbounded`), so G_swarm on all four coordinates has no fixed point. V2's `find_fixedpoint` returned the state after 200 steps, F included. | Closed: the theorems are stated for (I, C, M), and F is reported separately. |
| S6 | V2 `SwarmSimulator.lean` does not compile on Mathlib v4.32.0: nine errors, in T6, T7, T11, `systemInv`/T9 and T12. Several of its "theorems" restate their hypothesis (T5 is `h`; T1 and T2 restate arithmetic facts about L without touching G_swarm). | Closed: replaced by the V3 file. |
| S7 | The paper's text (V1/V2) stated Theorems 5.1–5.3 and the multi-orbit claim in the old form. | **Closed**: the paper is revised in `swarm_simulator_v3.tex` / `.pdf`. |

## Notes on sorry count

`SwarmSimulator.lean` (V3) has 0 `sorry`. Nothing is left as a documented stub: what is not proved is listed above as open (S3).
