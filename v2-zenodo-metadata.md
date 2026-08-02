# Zenodo deposit metadata — v2

**Record:** 10.5281/zenodo.21753025
**File:** `Grossi_2026_Positional_Dominance_v2.pdf` (13 pp.)

---

## Basic fields

| Field | Value |
|---|---|
| Resource type | Publication → **Preprint** |
| Title | Positional Dominance in Network Games: Equilibrium Conditions for Strategic Abstention from Velocity Competition |
| Publication date | *(deposit date)* |
| Version | **2.0** |
| Language | English (eng) |
| License | Creative Commons Attribution 4.0 International (CC BY 4.0) |
| Access | Open |

**Creator**
Grossi, Pablo Nogueira · ORCID 0009-0000-6496-2186 · Affiliation: G6 LLC, Newark, New Jersey, USA

---

## Description (abstract) — revised for v2

> We study a two-player infinite-horizon stochastic game on a capacitated linear distribution network in which one player commits capital to control key nodes — pipelines and storage hubs — while the rival invests in low-latency execution infrastructure. Using Markov Perfect Equilibrium with supply–demand shocks governed by a two-state volatility Markov chain, we establish the existence of a threshold σ* above which the positional player's equilibrium payoff strictly exceeds that of the velocity-optimizing player. The advantage arises from private inventory signals and flow-redirection optionality that reaction speed cannot replicate in high-volatility regimes.
>
> In this version, existence and uniqueness of σ* are proved directly for the equilibrium value functions, without any value-function approximation. Existence follows from equilibrium existence in finite-state discounted stochastic games together with continuity in σ, an exact sign condition at zero volatility, and divergence — the last requiring a strictly positive private-signal parameter γ > 0. Uniqueness follows from a Bellman convexity-preservation lemma combined with the fact that the velocity player's payoff becomes exactly affine once its latency cap binds, under a checkable condition on primitives. The result therefore carries an explicit scope: positional dominance requires that holding position **cost** something, that it **inform**, and that the rival's expenditure cannot **transfer** it.
>
> Value iteration on a calibrated 8×8×8 state grid yields σ* ∈ [0.30, 0.36]. Under U.S. energy midstream calibration, historical Permian–Cushing volatility of 0.35–0.42 exceeds this interval in approximately 68% of months over 2015–2024. Sensitivity analysis places σ* over [0.24, 0.43] under ±20% parameter variation, which we read as evidence that σ* is a property of a particular network under particular carrying costs rather than a constant.
>
> This version supersedes v1 (10.5281/zenodo.21013066). The analytical threshold σ* ≈ 0.665 reported there is corrected: v1's Section 3 and Appendix A stated two different functions, each a partial truncation of the paper's own value-function ansatz, and the intercept was justified by velocity rents that are identically zero at σ = 0. Restoring the dropped terms gives ΔV(σ) = aσ² + mσ − b with b identified as the capitalised fixed cost of holding position; the earlier value is an upper bound rather than an estimate. The correction factor ψ ≈ 0.50 and its attribution to storage optionality and Markov persistence are withdrawn pending direct measurement of the omitted linear term. The addendum's cross-domain evidence table is corrected: two supporting Lean 4 results are theorems of the form `rfl` on a definition and a third holds for every closed interval, so while machine-checked they carry no information about the value 1/3. The 1/3 recurrence is accordingly withdrawn as evidence and retained only as an open question.

---

## Additional notes (Zenodo "Additional notes" field)

> **Changes in version 2.**
> 1. Section 3.0 (new) — existence of σ* proved for the equilibrium value functions without the quadratic ansatz.
> 2. Section 3.0.1 (new) — uniqueness proved via Bellman convexity preservation plus affinity of the velocity payoff above saturation, under condition (C).
> 3. Proposition 1 replaced by Proposition 1′; the value gap restored to aσ² + mσ − b; intercept identified as capitalised carrying cost c_K/(1−δ).
> 4. Correction factor ψ ≈ 0.50 and its 25/25 attribution withdrawn; identification test specified in §3.3.
> 5. Addendum Table A.1 status column corrected; cross-domain clustering withdrawn as evidence; conjecture retained as open.
> 6. A near-miss coincidence (σ̄ = 0.3277 against σ* = 0.33) is recorded and refuted in §3.0.1 rather than deleted, together with the unit-consistency test that refutes it.
> 7. Numerical results unchanged — the value iteration never used the truncated expression.
>
> Open problems remaining: direct measurement of the linear coefficient m; uniqueness for the genuine two-state Markov chain; multi-player and multi-node extension.

---

## Related identifiers

| Relation | Identifier | Type |
|---|---|---|
| **is new version of** | 10.5281/zenodo.21013066 | DOI |
| is part of | 10.5281/zenodo.19117399 | DOI |
| is supplemented by | https://github.com/TOTOGT/geometry | URL |
| references | https://totogt.github.io/geometry/book6/wp38-positional-dominance.html | URL |

**Also edit v1's metadata** (permitted on published records without a new version): add
`is previous version of → 10.5281/zenodo.21753025`, and prepend to its description:
*"Superseded by v2, DOI 10.5281/zenodo.21753025, which corrects the derivation of the analytical threshold."*

---

## Subjects

**JEL** — C73 (Stochastic and Dynamic Games) · C72 (Noncooperative Games) · D43 (Market Structure: Oligopoly) · L13 (Oligopoly and Imperfect Markets) · L95 (Gas Utilities, Pipelines) · G13 (Contingent Pricing, Futures) · Q41 (Energy Demand and Supply)

*Change from v1:* C73 added — the model is a discounted stochastic game, and C73 is the more precise primary code. G13 and L95 added for the real-options and pipeline dimensions.

**MSC 2020** — 91A15 (Stochastic games) · 91A25 (Dynamic games) · 91B26 (Market models, auctions) · 90C39 (Dynamic programming)

*Change from v1:* 53D10 (contact manifolds) **dropped**. It entered via the addendum's cross-domain claim, which v2 withdraws as evidence; retaining it would assert a connection the paper no longer supports. 91B84 and 91G80 replaced by the game-theoretic and dynamic-programming codes that describe what the paper actually does.

---

## Keywords

network games · Markov perfect equilibrium · stochastic games · positional dominance · velocity competition · strategic abstention · real options · option value of waiting · preemption · bottleneck control · commodity markets · energy midstream · Cushing · high-frequency trading

*Change from v1:* "contact geometry" removed, for the same reason as MSC 53D10.

---

## Suggested citation

Grossi, P. N. (2026). *Positional Dominance in Network Games: Equilibrium Conditions for Strategic Abstention from Velocity Competition* (Version 2). Zenodo. https://doi.org/10.5281/zenodo.21753025

---

## One caution before depositing

The abstract above states that uniqueness is proved. It is proved **for the comparative-static reading**, in which σ is held fixed — which is the reading under which a threshold in the level of volatility is defined. It is **not** proved for the genuine two-state chain. The body says so in §3.0.1; if you would rather the abstract carry the qualifier too, insert "for the comparative-static formulation" after "Uniqueness follows from".
