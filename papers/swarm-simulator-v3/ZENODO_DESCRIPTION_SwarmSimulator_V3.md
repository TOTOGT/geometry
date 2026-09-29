# ZENODO_DESCRIPTION_SwarmSimulator_V3.md
# Paste this into the Zenodo description field for the V3 upload.

---

## The Swarm Simulator: A Dynamical Systems Model of Collective Intelligence Using the TO/TOGT Operator Pipeline
### Version 3 — September 2026 (corrections and formal checks)

**Pablo Nogueira Grossi · G6 LLC, Newark NJ · ORCID: 0009-0000-6496-2186**
V1: 10.5281/zenodo.19208284 · V2: 10.5281/zenodo.20230613 · **V3 (this deposit): 10.5281/zenodo.23027566** · Series root: https://doi.org/10.5281/zenodo.19117399
AXLE: https://github.com/TOTOGT/AXLE

---

### What this deposit is

A multi-agent dynamical system built on the operator pipeline G = U ∘ F ∘ K ∘ C of TO/TOGT, with four collective quantities: shared-intent stability I_t, coordination efficiency C_t, type-propagation multiplier M_t and diffusion factor F_t.

### Why V3

Checking V2 against Lean 4.32.0 and Mathlib v4.32.0 showed that its Lean file did not compile, that several of its theorems did not concern the swarm map, that Theorem 5.1 as printed is false, and that figure 4's clusters were not contractive. V3 replaces the Lean file, the simulator and the open-questions table, and gives corrected statements of Theorems 5.1–5.3 and of §6. The details are in `CHANGES_SwarmSimulator_V3.md`.

### What V3 proves (Lean 4.32.0, Mathlib v4.32.0, axioms propext / Classical.choice / Quot.sound, no sorry)

With a = f_types·f_agents·(1 − η), c = 1/(1 + D), m = (1 + β·reuse)·avg_quality:

- **No global contraction.** G_swarm has no global Lipschitz constant, since C_{t+1} = C_t · I_{t+1}/(1 + D) multiplies two state variables (`no_global_lipschitz`).
- **Contraction on a ball.** On ‖X‖ ≤ R, the Lipschitz constant is λ(R) = max(a(1 + cR), m), below 1 for R < (1 − a)/(a·c). For the default parameters the radius is about 3.51 (`step_lipschitz_ball`, `default_radius`).
- **Decay.** ‖X_t‖ ≤ ρ(R)^t ‖X₀‖ with ρ(R) = max(a, a·c·R, m); the printed bound L^t ‖X₀‖ holds for ‖X₀‖ ≤ 1 and fails from (100, 10, 1) (`orbit_nrm_le`, `paper_bound`, `printed_bound_fails`).
- **Fixed point.** The only fixed point of (I, C, M) in the ball is 0, and two clusters satisfying the ball condition share it (`fixed_point_zero`, `two_clusters`).
- **Diffusion.** F_t = 1 + αt has no upper bound, so the four-coordinate system has no fixed point (`diffuse_unbounded`).

In this model shared intent decays as I_t = I₀·a^t. It is the same law as a chain of steps each holding with probability a.

### What V3 does not do

- (Done, for the record) The paper is revised (`swarm_simulator_v3.pdf` and its LaTeX source): §5–§6 are rewritten with proofs, and the Lean statements are tabulated. The V1 and V2 texts are superseded.
- Empirical calibration (S3) is open. No data have been fitted.
- The multi-orbit claim of distinct fixed points is refuted for this model; a model with a source term would be needed.

### Files

- `swarm_simulator_v3.pdf`, `swarm_simulator_v3.tex` — the revised paper (with `figures/`)
- `SwarmSimulator.lean` — Lean 4 proofs (build: `lake build SwarmSimulator`)
- `swarmsimulator.axioms.txt` — `#print axioms` report
- `swarm_simulator.py` — simulator and figures; `python swarm_simulator.py --check` runs the numerical checks
- `OPEN_QUESTIONS_SwarmSimulator.md`, `CHANGES_SwarmSimulator_V3.md`
- fig1–fig4 (PDF, PNG), regenerated

**MSC codes:** 37C25, 37D10, 47H10, 68T99
**Keywords:** swarm simulator · collective intelligence · TO/TOGT · contraction on a ball · fixed point · Lean 4
**License:** CC BY-NC-ND 4.0 (paper) · MIT (code)
**Copyright:** © 2026 Pablo Nogueira Grossi, G6 LLC
