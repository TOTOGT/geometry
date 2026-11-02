import Mathlib

/-!
# GCM V2, Theorem A(ii): the adapted Lyapunov function, by several routes

STATUS: compiled by the author 2026-11-02 (Lean v4.32.0 + Mathlib), no errors, no warnings (empty output). Mathlib v4.32.0 has no Lyapunov-equation
lemma (searched .lake/packages/mathlib), so these are independent routes, each with its own scope.
Read each statement for what it says:

* Route A `scalar_adapted_deriv` : x' = -μ x, V = x·x has V' = -2μ V. Scalar only. This is the whole
  transverse story when dim S = 2.
* Route B `nonnormal_adapted_*`  : for A = [[-1,10],[0,-1]] (eigenvalues -1,-1) the explicit
  Q = [[1,10],[10,201]] gives V = xᵀQx with V' = -(x²+y²) - V ≤ -V along x' = A x. Hand-solved
  (sympy-checked) for κ = 1/2. One matrix, one κ: NOT a general theorem.
* Route D `adaptedNorm_*`        : for any linear semigroup E with ‖E s‖ ≤ K e^{-μ s}, the norm
  N x = sup_{s≥0} e^{κ s}‖E s x‖ (κ ≤ μ) satisfies N(E t x) ≤ e^{-κ t} N x and ‖x‖ ≤ N x.
  This is the general adapted-norm statement, but N is NOT smooth, so it gives the DECAY RATE of an
  adapted norm, not a C¹ Lyapunov function V with V' ≤ -cV. Smoothness is still open.
-/

open Real

/-! ### Route A: scalar -/

theorem scalar_adapted_deriv (μ x0 t : ℝ) :
    HasDerivAt (fun s : ℝ => (x0 * Real.exp (-μ * s)) * (x0 * Real.exp (-μ * s)))
      (-2 * μ * ((x0 * Real.exp (-μ * t)) * (x0 * Real.exp (-μ * t)))) t := by
  have h1 : HasDerivAt (fun s : ℝ => x0 * Real.exp (-μ * s))
      (x0 * (Real.exp (-μ * t) * (-μ))) t := by
    have := (((hasDerivAt_id t).const_mul (-μ)).exp).const_mul x0
    simpa using this
  refine (h1.mul h1).congr_deriv ?_
  ring

/-! ### Route B: the non-normal 2×2 example, explicit Q -/

theorem nonnormal_adapted_identity (x y : ℝ) :
    2 * ((x + 10 * y) * (-x + 10 * y) + (10 * x + 201 * y) * (-y))
      = -(x ^ 2 + y ^ 2) - (x ^ 2 + 20 * x * y + 201 * y ^ 2) := by
  ring

theorem nonnormal_adapted_posdef (x y : ℝ) :
    x ^ 2 + 20 * x * y + 201 * y ^ 2 = (x + 10 * y) ^ 2 + 101 * y ^ 2 := by
  ring

theorem nonnormal_adapted_decay (x y : ℝ) :
    2 * ((x + 10 * y) * (-x + 10 * y) + (10 * x + 201 * y) * (-y))
      ≤ -(x ^ 2 + 20 * x * y + 201 * y ^ 2) := by
  rw [nonnormal_adapted_identity]
  nlinarith [sq_nonneg x, sq_nonneg y]

/-! ### Route D: general linear semigroup, sup-type adapted norm -/

section Semigroup

variable {V : Type*} [NormedAddCommGroup V] [NormedSpace ℝ V]

noncomputable def adaptedNorm (E : ℝ → V →L[ℝ] V) (κ : ℝ) (x : V) : ℝ :=
  ⨆ s : Set.Ici (0 : ℝ), Real.exp (κ * s) * ‖E s x‖

theorem adaptedNorm_bddAbove (E : ℝ → V →L[ℝ] V) (K μ κ : ℝ) (hK : 0 ≤ K) (hκ : κ ≤ μ)
    (hE : ∀ s : ℝ, 0 ≤ s → ‖E s‖ ≤ K * Real.exp (-μ * s)) (x : V) :
    BddAbove (Set.range fun s : Set.Ici (0 : ℝ) => Real.exp (κ * s) * ‖E s x‖) := by
  refine ⟨K * ‖x‖, ?_⟩
  rintro _ ⟨s, rfl⟩
  have hs : (0 : ℝ) ≤ s := s.2
  have h1 : ‖E s x‖ ≤ ‖E s‖ * ‖x‖ := (E s).le_opNorm x
  have h2 : ‖E s‖ * ‖x‖ ≤ (K * Real.exp (-μ * s)) * ‖x‖ :=
    mul_le_mul_of_nonneg_right (hE s hs) (norm_nonneg x)
  have h3 : Real.exp (κ * s) * Real.exp (-μ * s) ≤ 1 := by
    rw [← Real.exp_add]
    apply Real.exp_le_one_iff.mpr
    nlinarith
  calc Real.exp (κ * s) * ‖E s x‖
      ≤ Real.exp (κ * s) * ((K * Real.exp (-μ * s)) * ‖x‖) :=
        mul_le_mul_of_nonneg_left (h1.trans h2) (Real.exp_nonneg _)
    _ = (K * ‖x‖) * (Real.exp (κ * s) * Real.exp (-μ * s)) := by ring
    _ ≤ (K * ‖x‖) * 1 :=
        mul_le_mul_of_nonneg_left h3 (mul_nonneg hK (norm_nonneg x))
    _ = K * ‖x‖ := by ring

theorem adaptedNorm_ge (E : ℝ → V →L[ℝ] V) (K μ κ : ℝ) (hK : 0 ≤ K) (hκ : κ ≤ μ)
    (hE : ∀ s : ℝ, 0 ≤ s → ‖E s‖ ≤ K * Real.exp (-μ * s))
    (h0 : E 0 = ContinuousLinearMap.id ℝ V) (x : V) :
    ‖x‖ ≤ adaptedNorm E κ x := by
  have hb := adaptedNorm_bddAbove E K μ κ hK hκ hE x
  have := le_ciSup hb (⟨0, Set.self_mem_Ici⟩ : Set.Ici (0 : ℝ))
  unfold adaptedNorm
  simpa [h0] using this

theorem adaptedNorm_decay (E : ℝ → V →L[ℝ] V) (K μ κ : ℝ) (hK : 0 ≤ K) (hκ : κ ≤ μ)
    (hE : ∀ s : ℝ, 0 ≤ s → ‖E s‖ ≤ K * Real.exp (-μ * s))
    (hsemi : ∀ s t : ℝ, 0 ≤ s → 0 ≤ t → E (s + t) = (E s).comp (E t))
    (x : V) (t : ℝ) (ht : 0 ≤ t) :
    adaptedNorm E κ (E t x) ≤ Real.exp (-κ * t) * adaptedNorm E κ x := by
  have hb := adaptedNorm_bddAbove E K μ κ hK hκ hE x
  haveI : Nonempty (Set.Ici (0 : ℝ)) := ⟨⟨0, Set.self_mem_Ici⟩⟩
  unfold adaptedNorm
  apply ciSup_le
  intro s
  have hs : (0 : ℝ) ≤ s := s.2
  have h1 : E (s + t) x = E s (E t x) := by
    rw [hsemi s t hs ht]; rfl
  have hexp : -κ * t + κ * (s + t) = κ * s := by ring
  have h2 : Real.exp (κ * s) * ‖E s (E t x)‖
      = Real.exp (-κ * t) * (Real.exp (κ * (s + t)) * ‖E (s + t) x‖) := by
    rw [h1, ← mul_assoc, ← Real.exp_add, hexp]
  rw [h2]
  exact mul_le_mul_of_nonneg_left
    (le_ciSup hb (⟨s + t, Set.mem_Ici.mpr (by linarith)⟩ : Set.Ici (0 : ℝ))) (Real.exp_nonneg _)

end Semigroup
