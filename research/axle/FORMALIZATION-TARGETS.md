# AXLE minimal formalization targets — PROPOSED AND UNTESTED (specification only: nothing written, nothing compiled, nothing Lean-verified)
Duplicate check (2026-11-26): GitHub tree access for TOTOGT repos was refused this session ("repository access not enabled"), so I could **not** re-list the repos. Basis = project records: the 2026-09-21 Reeb session note and the Ch 14 review ("TOTOGT/AXLE 133 files, TOTOGT/geometry 197 files, checked by filename and declaration names"). Present there: `ReebFlow.lean` (alphaCat, reeb_alpha_eq_one, reeb_interior_dAlpha, reebFlow_preserves_alpha, contactVol), `ReebFlowExtDeriv.lean`, `ReebWedge.lean` (contactVol_eq_wedge12), `ReebUnique.lean`, `ReebNoAttractor.lean`, `Orthogenesis/Taxonomy/FoldFlow.lean` (gradient flow of a cubic fold), `Orthogenesis/Figure8/A1Node.lean` (nodes of plane curves). **Not found** there: Cauchy–Riemann/Jacobian identity, contact test for η=dz+u dv, harmonic-polynomial classification, dissipation lemma. Before writing: re-grep those names (esp. A1Node.lean for overlap with the nodal items) and check Mathlib (Complex.det…, Polynomial/MvPolynomial harmonic) — Mathlib names below are UNCHECKED. Repo note (memory): AXLE is a site/book repo; the Lean project belongs in its own folder.
Style rule from this project: each statement names its hypotheses and a non-vacuous conclusion; no `∃ x, True`-type conclusions.

## T1 — Regularized contact Jacobian (core identity)
Statement: for f : ℂ → ℂ, `HasDerivAt f f' s` ⇒ the real Jacobian determinant of (σ,t) ↦ (Re f(σ+it), Im f(σ+it)) at s equals ‖f'‖² (= `Complex.normSq f'`).
Needs: `HasDerivAt.hasFDerivAt` over ℝ (restrict scalars), the matrix of ℝ-linear map z↦f'·z in basis (1,i) is [[Re f', −Im f'],[Im f', Re f']] with det = (Re f')²+(Im f')². Pure algebra after that. CR equations u_σ=v_t, u_t=−v_σ as corollary.
## T2 — Contact nondegeneracy (coefficient level, avoiding Mathlib differential forms)
Define `contactCoeff (u v : ℝ×ℝ → ℝ) p := u_σ·v_t − u_t·v_σ` (the coefficient of dz∧dσ∧dt in η∧dη for η = dz + u dv; also dη = (u_σ v_t − u_t v_σ) dσ∧dt).
 - `contactCoeff_eq : contactCoeff (re∘f) (im∘f) = ‖deriv f s‖²` (from T1).
 - `contact_iff : contactCoeff ≠ 0 ↔ deriv f s ≠ 0`.
 - `simple_zero_contact : f s = 0 → deriv f s ≠ 0 → contactCoeff ≠ 0` (hypothesis names both parts: zero **and** simple; conclusion nonvacuous).
 - `multiple_zero_not_contact : AnalyticAt ℂ f s → f s = 0 → order ≥ 2 → contactCoeff = 0` (Mathlib: `AnalyticAt.order`, `AnalyticAt.deriv…` unchecked).
 - Reeb: `η(∂_z)=1`, `ι_{∂_z}dη=0` as coefficient-vector identities (reuse the pattern of `reeb_alpha_eq_one`, `reeb_interior_dAlpha`).
 - ζ-instance: any statement using `riemannZeta` must take Speiser as an explicit hypothesis: `def Speiser : Prop := RiemannHypothesis ↔ ∀ s : ℂ, 0 < s.re → s.re < 1/2 → deriv riemannZeta s ≠ 0` — never an axiom, never used in T1–T5. Differentiability of ζ off s=1 is in Mathlib.
## T3 — Homogeneous harmonic polynomial classification (finite linear algebra, `ring`/`linarith`-level)
 - `harm2 : P = αx²+βxv+γv², Δ P = 0 ⇒ γ = −α` (so P = α(x²−v²)+βxv).
 - `harm2_even_sigma : harmonic, even in x ⇒ P = α(x²−v²)` (β=0).
 - `harm4_even_sigma : P=Σ_{j=0}^4 c_j x^{4−j}v^j harmonic, P(−x,v)=P(x,v), P(−x,−v)=P ⇒ ∃ c, P = c(x⁴−6x²v²+v⁴)`. (Equations: c₁=c₃=0 (evenness), c₀·12+2c₂=0, 2c₂+12c₄=0 ⇒ c₂=−6c₀, c₄=c₀.) Conclusion is an explicit polynomial identity, not an existential over a free class.
 - `odd_degree_excluded : harmonic, even in x, odd degree k, P(−x,−v)=P ⇒ P = 0` for k=1,3,5.
 - Optional later (heavier): general k via Re/Im (w^k); order-2k nodal count via IVT + simple roots of cos kθ (the full theorem (C) needs the implicit function theorem plus polar blow-up: not a minimal target).
## T4 — Quartic reduction lemma (algebra only)
Given the three linear constraint systems of `nodal_taylor.py` as hypotheses on coefficients c_{jk} (degrees ≤5), conclude `a = 4(10c40+c41)/(μ−10)` and, if a=0, c41 = −10c40 with degree-4 part c40(x⁴−6x²v²+v⁴) and degree-5 part −2c40(5x⁴v−10x²v³+v⁵). Pure `field_simp; ring`. Hypotheses must include μ≠10.
## T5 — Energy dissipation under a positive-semidefinite mobility
Statement: E : (Fin n → ℝ) → ℝ differentiable, x : ℝ → (Fin n → ℝ) differentiable with x'(t) = −G·∇E(x(t)), G : Matrix (Fin n)(Fin n) ℝ with ∀ y, 0 ≤ y ⬝ᵥ (G *ᵥ y). Then `HasDerivAt (E ∘ x) (−(∇E(x t)) ⬝ᵥ (G *ᵥ ∇E(x t))) t` and hence `deriv (E∘x) t ≤ 0`; equality iff G∇E=0 when G is PSD (G∇E=0 ⇔ ∇Eᵀ G ∇E = 0 requires PSD: Cauchy–Schwarz for PSD). Standard mathematics; no TOGT content. Use `HasFDerivAt.comp_hasDerivAt`. The "gradient" must be a stated Euclidean gradient (`toDual`) or the statement stays in terms of `fderiv E (x t) (x' t)`, which avoids the metric.
## Priority
T3 and T4 (decidable, cheap), then T1→T2 (the contact result), T5. Speiser stays external and conditional.
