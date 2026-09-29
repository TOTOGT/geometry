# CHANGES — Swarm Simulator, V2 → V3 (September 2026)

Author: Pablo Nogueira Grossi, G6 LLC. The corrections and the Lean checks in this version were prepared with Claude (Anthropic); the claims and the deposit are the author's.

## Why a V3

V2 said it added "reproducible simulation code and formal Lean 4 verification". Checking it against the pinned toolchain (Lean 4.32.0, Mathlib v4.32.0, September 2026) found four problems:

1. **The V2 Lean file did not compile**: nine errors (T6, T7, T11, `systemInv`/T9, T12). Names such as `div_le_iff` and the argument order of `mul_le_mul_of_nonneg_right` had changed.
2. **Several V2 "theorems" did not concern the swarm map.** T5 is its own hypothesis; T1 and T2 are arithmetic facts about L; T9 is true by construction (`systemInv` is defined as the maximum plus 1).
3. **Theorem 5.1 as printed is false.** G_swarm has no global Lipschitz constant, because C_{t+1} = C_t · I_{t+1}/(1 + D) multiplies two state variables.
4. **The simulator's figures did not show what they claimed.** Figure 4's two clusters had L = 2.41 and 1.93 (neither contractive) and both converge to 0, so "distinct fixed points" was not what the run showed. `find_fixedpoint` returned the state after 200 steps, F included, and F has no fixed point.

## What V3 contains

| File | Change |
|------|--------|
| `SwarmSimulator.lean` | Rewritten. Fourteen theorems about the actual map, all compiling, no `sorry`. |
| `swarmsimulator.axioms.txt` | The `#print axioms` report: [propext, Classical.choice, Quot.sound] for every theorem. |
| `swarm_simulator.py` | `find_fixedpoint` fixed; ρ(R), λ(R) and the contraction radius added; figures 2–4 redrawn; `--check` mode runs 10 numerical checks of what the Lean file proves. |
| `OPEN_QUESTIONS_SwarmSimulator.md` | Rewritten with the true status of S1–S4 and the new items S5–S7. |
| `ZENODO_DESCRIPTION_SwarmSimulator_V3.md` | Replaces the V2 description; V3 DOI 10.5281/zenodo.23027566. |
| `swarm_simulator_v3.tex`, `swarm_simulator_v3.pdf` | The revised paper, 7 pages, with figures. |

## Replacement statements for the paper (§5 and §6)

Write a = f_types·f_agents·(1 − η), c = 1/(1 + D), m = (1 + β·reuse)·avg_quality, and ‖X‖ = |I| + |C| + |M|. The diffusion coordinate F_t = 1 + αt is time-dependent and unbounded, so the statements below are for (I, C, M). The proofs are in `SwarmSimulator.lean`.

**Theorem 5.1 (Contraction on a ball).** For states X, Y with |X.C| ≤ R and |Y.I| ≤ R,
‖G(X) − G(Y)‖ ≤ λ(R)·‖X − Y‖, with λ(R) = max(a(1 + cR), m).
If a < 1 and m < 1, then λ(R) < 1 exactly when R < (1 − a)/(a·c). There is no global Lipschitz constant. (`step_lipschitz_ball`, `no_global_lipschitz`)

**Theorem 5.2 (Fixed point).** 0 is a fixed point of G. If ρ(R) = max(a, a·c·R, m) < 1, it is the only fixed point in the ball ‖X‖ ≤ R. (`step_zero`, `fixed_point_zero`)

**Theorem 5.3 (Decay).** If ρ(R) ≤ 1 and ‖X₀‖ ≤ R, then ‖X_t‖ ≤ ρ(R)^t ‖X₀‖ for all t. If L = a + a·c + m < 1 and ‖X₀‖ ≤ 1, then ‖X_t‖ ≤ L^t ‖X₀‖. The bound L^t ‖X₀‖ fails for large starts: from (100, 10, 1) with the default parameters. (`orbit_nrm_le`, `paper_bound`, `printed_bound_fails`)

**§6 (Multi-orbit).** Replace the claim of distinct fixed points by: clusters that each satisfy the ball condition share the fixed point 0 and differ only in their decay rates. (`two_clusters`)

## What is not done

- (Done) The paper is rewritten as `swarm_simulator_v3.tex` / `.pdf` from the text of the V1 PDF, because the V1 LaTeX source is not held. The V1 and V2 wording is not reproduced line for line.
- S3 (calibration against data) is open.
- The question "is there a model in this family with nonzero persistent shared intent?" is not addressed. A source term would be needed.
