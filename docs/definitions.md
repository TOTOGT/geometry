# Definitions — Principia Orthogona corpus

Started 2026-09-30. One place for the definitions the author has decided, so they are not re-explained each session.
Status: **DECIDED** (author said so) · **VERIFIED** (recomputed by script, cited) · **OPEN** (author's call; nothing invented here).
Add a line, never overwrite one without a dated note. Sources are the files read on 2026-09-30 (Vol I v7 TeX, Vol II TeX, toy-model V4 draft, gcm-framework.html, Book 4 ch10, Downloads copies); the GCM PDF (Zenodo 20230610) is not held locally.

## Radii and basins (Book 4 chapter 10 is the authority)

| Symbol | Definition | Status | Notes |
|---|---|---|---|
| ε₀ | Gronwall stability radius, ε₀ = \|μ_max\| / [2(1 + sup‖Hess V‖)]; toy model gives 1/3. The estimate suggested by the literature. | DECIDED: coarse | Author: it was "the" radius until found coarse. A perturbation size, not a set. |
| B(Γ) | Basin of attraction of Γ: initial conditions whose orbits converge to Γ. | OPEN wording | Vol I writes "the Gronwall basin ε₀ = 1/3", mixing a radius with a set. |
| r\* | Sharp inner-basin boundary (Whitney fold threshold), a **radial position**: r\* = 0.77594058 (bisection, tol 1e-7, Book 4 ch10). Displacement from Γ is 1 − r\* ≈ 0.224. | DECIDED + VERIFIED | Recomputed 0.775941 at z(0)=0 (r0=0.70 escapes, 0.80 converges). State z(0). Closed form OPEN. |
| r_s | Saddle: unique root in (0,1) of r³ − r² − 2r + 1 = 0, r_s = 2cos(3π/7) ≈ 0.4450. | VERIFIED | Closed form; cubic residual ~1e-16. |

Known wording errors to fix when the text is next edited: Vol I "ε₀ = 1/3 lies strictly inside the inner boundary" and Lean `1/3 < 0.77594` compare a displacement with a radius (should read 1 − r\* < ε₀); Book 4 ch10 caption says r\* is "further from the attractor" (it is nearer); Vol II caption says all three radii are closed form (r\* is not).

## Exponents and thresholds

| Symbol | Definition | Status | Notes |
|---|---|---|---|
| μ_max | Floquet exponent of Γ (Vol II Lemma 3.1 cites Vol I Thm 3.3 for μ_max < 0); in the regularized limit. Toy value −2. | OPEN wording | Linearization at r=1 is −2 + 2e^(−z); −2 holds as z → ∞ (Book 4 ch10: "μ → −2 as z → ∞"). |
| τ | Embodiment threshold: τ = √(c/κ_noise), from the stochastic Lyapunov condition LV ≤ −cV + κ_noise‖σ‖², with κ_noise = ½ sup‖Hess V‖. The noise amplitude below which the system is stochastically stable. Toy value 2. | DEFINED in the papers + VERIFIED (toy value) | Source: Vol II Thm 3.2 (citing GCM Def 3.4); Vol I §2 states τ = √(c/κ). Toy with V = ρ²: c = 4, Hess V = 2, κ_noise = 1, τ = 2 (recomputed). **OPEN detail:** Vol I says c = 1, κ = 1/4 (same ratio 4, different split); with its own W = ½ρ² the recomputed τ is 2.83, not 2. Which V is canonical is the author's call. *Correction 2026-09-30:* this row first said OPEN / no formula found. Wrong — my term scan missed a definition written as a formula. |
| τ normalization | τ is not invariant under rescaling V: for V → λV, c is unchanged, κ_noise scales by λ, so τ → τ/√λ (τ·√λ = 2 for every λ in the toy model). | VERIFIED (script, 2026-09-30) | Explains 2 versus 2.83: W = ½ρ² is λ = ½, so τ = 2√2. Consequence: "σ < τ" has no intrinsic meaning until V is fixed. **PROPOSED, awaiting author:** fix V = ρ² (Vol II Thm 3.2 / GCM Def 3.4; gives τ = 2) and state the rule, with a one-line erratum in Vol I. Vol I's split (c, κ) = (1, 1/4) is still unexplained: c = 4 for every λρ², so no rescaling of V produces c = 1. |
| τ₁₂ | Threshold of a unified system. | OPEN | GCM page Def 3.1 (√(μ₁²+μ₂²)/max κ) disagrees with the paper's proof (√(c₁₂/κ₁₂)); the page version can contradict Theorem B. |
| κ\* | Critical curvature, √(7/9) ≈ 0.882 (dm³ marker). | OPEN | Book 4 ch10: "derivation open". |
| κ chain | ≤ √(5/9) ≈ 0.745 (Vol IV recursion). | OPEN | Derivation status not checked. |
| W(Γ) | Winding integral. GCM: ∮ r² dθ, claimed integer. | OPEN | Equals 2πr₀², not an integer; normalization (e.g. 1/2π) is the author's call. |

## Operator chain

| Symbol | Definition | Status | Notes |
|---|---|---|---|
| C, K, F, U | Compression, Curvature (threshold), Fold, Unfolding: G = U∘F∘K∘C. | DECIDED | Canonical U for Book 3 is Unfolding (first four GCM papers, Zenodo 19117400). |
| U family | U₁ unification (pushout), U₂ translation (correspondence), U₃ unfolding (= exp(−∇d²)). Siblings of one family. | DECIDED | Per the 2026-09-29 audit entry; Institutional Edition App. A g–L–R–U is a different set of objects. |
| dm³ system | Axiomatic quintuple (M, g, Γ, V, ξ) with eight axioms (GCM page). | OPEN naming | Vol I / toy model also use "dm³" for the concrete 3-D canonical model. Proposal: "dm³ system" = class, "canonical dm³ model" = the ODE. |

## Terms used but not defined (candidates)
"reduced system", "contact class of α", "multi-scale coherence" (GCM page); "Coherence Bridge" (Vol I figure). Define or remove.
