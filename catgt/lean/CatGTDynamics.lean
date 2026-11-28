import Mathlib

/-!
# CatGTDynamics.lean   (UNTESTED: never compiled; CI is the only compiler)

Target location in TOTOGT/geometry: `catgt/lean/CatGTDynamics.lean`, as a separate non-default
`lean_lib`, gated by `verify-catgtdyn.yml` (draft next to this file).

What this file is, read against the statements and not the names:

* §A  General norm law.  For a complex inner-product space `E` and a trajectory `ψ : ℝ → E` with
      `HasDerivAt ψ (F (ψ t)) t` at every `t`:  d/dt ‖ψ t‖² = 2 Re ⟪ψ t, F (ψ t)⟫.
      Consequence, `norm_conserved_iff`:  ‖ψ t‖ is constant on all of ℝ  ↔  Re⟪ψ t, F (ψ t)⟫ = 0
      for every `t`.  This is an iff for the whole trajectory.  Re⟪ψ t₀, F (ψ t₀)⟫ = 0 at ONE time
      only says the derivative of ‖ψ‖² vanishes at t₀ (`deriv_normSq_eq_zero_iff`); it does not
      give conservation.
* §B  Gradient-plus-remainder law.  For a real inner-product space `H`, `E : H → ℝ` with gradient
      `g` at `x t`, and `HasDerivAt x (-g + K) t`:   d/dt E (x t) = -‖g‖² + ⟪g, K⟫.
      Corollaries: if ⟪g, K⟫ = 0 the energy is non-increasing; if K = S g with S skew
      (⟪v, S v⟫ = 0) then ⟪g, K⟫ = 0.
* §C  The continuous relaxation ṙ = -k (r - r*) behind `relaxStep` of CatGT_Main §9: the exact
      solution, and d/dt (r - r*)² = -2k (r - r*)².

NOT established here, and not claimed:
* The DNLS vector field of CatGT_Main §5 / DNLSNorm.lean is an instance of §A with
  Re⟪ψ, Fψ⟫ = 0; that instance is `CatGTNorm.drift_zero` / `dnls_norm_conserved` in DNLSNorm.lean
  (CI-green, run on main).  It is not re-proved here.
* No energy / Hamiltonian conservation for DNLS is proved in this file.
* The repository defines NO combined dissipative+DNLS vector field: §9 (`relaxStep`, a scalar
  radius map) and §5 (the DNLS chain) are separate systems, so the cross term ⟪∇E, K⟫ for "the
  CatGT model" has no definition to evaluate.  §B only states when the cross term vanishes.
Mathlib names not checked (no toolchain): `HasDerivAt.inner`, `inner_self_eq_norm_sq`,
`is_const_of_deriv_eq_zero`, `HasGradientAt.hasFDerivAt`, `InnerProductSpace.toDual_apply`.
-/

open Complex

namespace CatGTDyn

/-! ## §A  Norm law for ψ' = F ψ in a complex inner-product space -/

section A

variable {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℂ E]

/-- d/dt ‖ψ‖² = 2 Re ⟪ψ, ψ'⟫. -/
theorem hasDerivAt_normSq {ψ : ℝ → E} {ψ' : E} {t : ℝ} (h : HasDerivAt ψ ψ' t) :
    HasDerivAt (fun s => ‖ψ s‖ ^ 2) (2 * (inner ℂ (ψ t) ψ').re) t := by
  have h1 : HasDerivAt (fun s => inner ℂ (ψ s) (ψ s))
      (inner ℂ (ψ t) ψ' + inner ℂ ψ' (ψ t)) t := by
    first
      | exact h.inner ℂ h
      | exact HasDerivAt.inner ℂ h h
      | exact h.inner h
  have h2 : HasDerivAt (fun s => (inner ℂ (ψ s) (ψ s)).re)
      (inner ℂ (ψ t) ψ' + inner ℂ ψ' (ψ t)).re t :=
    Complex.reCLM.hasFDerivAt.comp_hasDerivAt t h1
  have hfun : (fun s => (inner ℂ (ψ s) (ψ s)).re) = fun s => ‖ψ s‖ ^ 2 := by
    funext s
    first
      | exact inner_self_eq_norm_sq (𝕜 := ℂ) (ψ s)
      | simp [inner_self_eq_norm_sq_to_K, ← Complex.ofReal_pow]
  have hval : (inner ℂ (ψ t) ψ' + inner ℂ ψ' (ψ t)).re = 2 * (inner ℂ (ψ t) ψ').re := by
    have hc : inner ℂ ψ' (ψ t) = (starRingEnd ℂ) (inner ℂ (ψ t) ψ') := (inner_conj_symm _ _).symm
    rw [hc, Complex.add_re, Complex.conj_re]; ring
  rw [hfun] at h2
  rw [hval] at h2
  exact h2

/-- Instantaneous statement: the derivative of ‖ψ‖² at `t` vanishes iff Re⟪ψ t, ψ'⟫ = 0. -/
theorem deriv_normSq_eq_zero_iff {ψ : ℝ → E} {ψ' : E} {t : ℝ} (h : HasDerivAt ψ ψ' t) :
    deriv (fun s => ‖ψ s‖ ^ 2) t = 0 ↔ (inner ℂ (ψ t) ψ').re = 0 := by
  rw [(hasDerivAt_normSq h).deriv]
  constructor
  · intro h0; linarith
  · intro h0; rw [h0]; ring

/-- **Necessary and sufficient condition for norm conservation along a global solution.**
For `ψ` with `HasDerivAt ψ (F (ψ t)) t` for every `t`:
`‖ψ t‖ = ‖ψ 0‖` for all `t`  ↔  `Re ⟪ψ t, F (ψ t)⟫ = 0` for all `t`. -/
theorem norm_conserved_iff (F : E → E) {ψ : ℝ → E}
    (hψ : ∀ t, HasDerivAt ψ (F (ψ t)) t) :
    (∀ t, ‖ψ t‖ = ‖ψ 0‖) ↔ ∀ t, (inner ℂ (ψ t) (F (ψ t))).re = 0 := by
  have hd : ∀ t, HasDerivAt (fun s => ‖ψ s‖ ^ 2) (2 * (inner ℂ (ψ t) (F (ψ t))).re) t :=
    fun t => hasDerivAt_normSq (hψ t)
  constructor
  · intro hc t
    have hconst : (fun s => ‖ψ s‖ ^ 2) = fun _ => ‖ψ 0‖ ^ 2 := by
      funext s; rw [hc s]
    have h0 : HasDerivAt (fun s => ‖ψ s‖ ^ 2) 0 t := by
      rw [hconst]; exact hasDerivAt_const t _
    have := (hd t).unique h0
    linarith
  · intro hre t
    have hdz : ∀ s, deriv (fun r => ‖ψ r‖ ^ 2) s = 0 := by
      intro s; rw [(hd s).deriv, hre s]; ring
    have hdiff : Differentiable ℝ (fun s => ‖ψ s‖ ^ 2) := fun s => (hd s).differentiableAt
    have heq := is_const_of_deriv_eq_zero hdiff hdz t 0
    have h2 : ‖ψ t‖ ^ 2 = ‖ψ 0‖ ^ 2 := heq
    have := sq_eq_sq₀ (norm_nonneg _) (norm_nonneg _) |>.1 h2
    exact this

end A

/-! ## §B  Gradient flow with a remainder field -/

section B

variable {H : Type*} [NormedAddCommGroup H] [InnerProductSpace ℝ H] [CompleteSpace H]

/-- d/dt E(x) = -‖∇E‖² + ⟪∇E, K⟫ along `ẋ = -∇E(x) + K(x)`. -/
theorem energy_derivative {E : H → ℝ} {x : ℝ → H} {g K : H} {t : ℝ}
    (hE : HasGradientAt E g (x t)) (hx : HasDerivAt x (-g + K) t) :
    HasDerivAt (fun s => E (x s)) (-‖g‖ ^ 2 + inner ℝ g K) t := by
  have h1 : HasDerivAt (fun s => E (x s))
      ((InnerProductSpace.toDual ℝ H g) (-g + K)) t :=
    hE.hasFDerivAt.comp_hasDerivAt t hx
  have h2 : (InnerProductSpace.toDual ℝ H g) (-g + K) = -‖g‖ ^ 2 + inner ℝ g K := by
    rw [InnerProductSpace.toDual_apply_apply, inner_add_right, inner_neg_right,
      real_inner_self_eq_norm_sq]
  rw [h2] at h1
  exact h1

/-- If the remainder is orthogonal to the gradient, the energy decreases at rate ‖∇E‖². -/
theorem energy_derivative_of_orth {E : H → ℝ} {x : ℝ → H} {g K : H} {t : ℝ}
    (hE : HasGradientAt E g (x t)) (hx : HasDerivAt x (-g + K) t) (hK : inner ℝ g K = 0) :
    HasDerivAt (fun s => E (x s)) (-‖g‖ ^ 2) t := by
  have := energy_derivative hE hx
  rwa [hK, add_zero] at this

/-- A skew remainder `K = S g` is orthogonal to the gradient. -/
theorem orth_of_skew (S : H →ₗ[ℝ] H) (hS : ∀ v, inner ℝ v (S v) = 0) (g : H) :
    inner ℝ g (S g) = 0 := hS g

end B

/-! ## §C  Continuous relaxation behind `relaxStep` -/

section C

/-- d/dt (r - r*)² = -2k (r - r*)² along ṙ = -k (r - r*). -/
theorem relax_flow_lyapunov {r : ℝ → ℝ} {k rstar t : ℝ}
    (h : HasDerivAt r (-k * (r t - rstar)) t) :
    HasDerivAt (fun s => (r s - rstar) ^ 2) (-2 * k * (r t - rstar) ^ 2) t := by
  have h1 : HasDerivAt (fun s => r s - rstar) (-k * (r t - rstar)) t := h.sub_const rstar
  have h2 := h1.pow 2
  convert h2 using 1
  simp
  ring

/-- Explicit solution r(t) = r* + (r₀ - r*) e^{-k t}. -/
theorem relax_solution (k rstar r0 t : ℝ) :
    HasDerivAt (fun s => rstar + (r0 - rstar) * Real.exp (-k * s))
      (-k * ((rstar + (r0 - rstar) * Real.exp (-k * t)) - rstar)) t := by
  have h1 : HasDerivAt (fun s : ℝ => -k * s) (-k) t := by
    simpa using (hasDerivAt_id t).const_mul (-k)
  have h2 := (h1.exp).const_mul (r0 - rstar)
  have h3 := h2.const_add rstar
  convert h3 using 1
  ring

end C

end CatGTDyn

#print axioms CatGTDyn.hasDerivAt_normSq
#print axioms CatGTDyn.deriv_normSq_eq_zero_iff
#print axioms CatGTDyn.norm_conserved_iff
#print axioms CatGTDyn.energy_derivative
#print axioms CatGTDyn.energy_derivative_of_orth
#print axioms CatGTDyn.orth_of_skew
#print axioms CatGTDyn.relax_flow_lyapunov
#print axioms CatGTDyn.relax_solution
