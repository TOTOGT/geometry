/-
  AXLE targets T1, T2, T5 and coefficient-level T3 (k = 2, 4).
  STATUS: UNTESTED. Written 2026-11-26 without a Lean toolchain or Mathlib build.
  Nothing here is machine-verified. Pin: Mathlib 81a5d257c8e410db227a6665ed08f64fea08e997, Lean v4.32.0.
  Lemma signatures used from Mathlib were read from the raw files at that rev:
    HasDerivAt.complexToReal_fderiv : HasDerivAt f f' x -> HasFDerivAt f (f' • (1 : ℂ →L[ℝ] ℂ)) x
    HasFDerivAt.comp_hasDerivAt, hasGradientAt_iff_hasFDerivAt (Iff.rfl onto toDual).
  Names NOT confirmed by reading: Complex.coe_basisOneI_repr, Complex.coe_basisOneI,
  InnerProductSpace.toDual_apply_apply. If a simp call fails, report the exact error.
-/
import Mathlib

open Complex

namespace AXLE.Contact

/-! ## T1. det of multiplication by c on ℂ = ℝ² is normSq c -/

/-- T1 (algebraic form). The real determinant of `w ↦ c * w` equals `Complex.normSq c`. -/
theorem det_mulLeft_complex (c : ℂ) :
    LinearMap.det (LinearMap.mulLeft ℝ c) = Complex.normSq c := by
  rw [← LinearMap.det_toMatrix Complex.basisOneI, Matrix.det_fin_two]
  simp [LinearMap.toMatrix_apply, Complex.normSq_apply, Complex.coe_basisOneI,
    Complex.coe_basisOneI_repr] <;> ring

/-- T1 (derivative form). If `f` has complex derivative `f'` at `z`, the real Fréchet
derivative of `f` at `z` has determinant `normSq f'` (= Jacobian `‖f'‖²`).
Hypothesis is `HasDerivAt f f' z` only; it does not mention the determinant. -/
theorem det_real_fderiv {f : ℂ → ℂ} {f' z : ℂ} (h : HasDerivAt f f' z) :
    LinearMap.det ((fderiv ℝ f z : ℂ →L[ℝ] ℂ) : ℂ →ₗ[ℝ] ℂ) = Complex.normSq f' := by
  have h1 := h.complexToReal_fderiv
  have h2 : ((f' • (1 : ℂ →L[ℝ] ℂ) : ℂ →L[ℝ] ℂ) : ℂ →ₗ[ℝ] ℂ) = LinearMap.mulLeft ℝ f' := by
    ext w
    simp
  rw [h1.fderiv, h2]
  exact det_mulLeft_complex f'

/-! ## T2. Contact coefficient of η = dz + u dv, (u,v) = (Re f, Im f), in coordinates (z, σ, t)

Hand derivation: dη = du ∧ dv = (u_σ v_t - u_t v_σ) dσ∧dt, and
η ∧ dη = dz∧du∧dv + u dv∧du∧dv = (u_σ v_t - u_t v_σ) dz∧dσ∧dt  (second term has dv twice).
We formalize ONLY the scalar coefficient `u_σ v_t - u_t v_σ`, not differential forms. -/

/-- Coefficient of `dz ∧ dσ ∧ dt` in `η ∧ dη`, from the real partial derivatives of `f`
at `s`: `u_σ = Re (Df 1)`, `u_t = Re (Df i)`, `v_σ = Im (Df 1)`, `v_t = Im (Df i)`. -/
noncomputable def contactCoeff (f : ℂ → ℂ) (s : ℂ) : ℝ :=
  ((fderiv ℝ f s) 1).re * ((fderiv ℝ f s) Complex.I).im
    - ((fderiv ℝ f s) Complex.I).re * ((fderiv ℝ f s) 1).im

/-- Cauchy–Riemann form of the coefficient: it equals `normSq f'`. -/
theorem contactCoeff_eq_normSq {f : ℂ → ℂ} {f' s : ℂ} (h : HasDerivAt f f' s) :
    contactCoeff f s = Complex.normSq f' := by
  have h1 := h.complexToReal_fderiv
  rw [contactCoeff, h1.fderiv]
  simp [Complex.normSq_apply] <;> ring

/-- T2. The coefficient is nonzero exactly when `f' ≠ 0`. -/
theorem contactCoeff_ne_zero_iff {f : ℂ → ℂ} {f' s : ℂ} (h : HasDerivAt f f' s) :
    contactCoeff f s ≠ 0 ↔ f' ≠ 0 := by
  rw [contactCoeff_eq_normSq h]
  simp only [ne_eq, Complex.normSq_eq_zero]

/-- T2 at a simple zero: `f s = 0` and `f' ≠ 0` give a nondegenerate contact coefficient.
NOTE: `hz` is not needed for the nonvanishing; it only places `s` on the zero set. The
statement that the coefficient vanishes at a multiple zero is the next lemma. -/
theorem contact_nondegenerate_simple_zero {f : ℂ → ℂ} {f' s : ℂ}
    (_hz : f s = 0) (h : HasDerivAt f f' s) (hf' : f' ≠ 0) :
    contactCoeff f s ≠ 0 :=
  (contactCoeff_ne_zero_iff h).2 hf'

/-- Multiple zero (first-order degenerate): `f s = 0` and `f' = 0` give coefficient `0`. -/
theorem contact_degenerate_multiple_zero {f : ℂ → ℂ} {s : ℂ}
    (_hz : f s = 0) (h : HasDerivAt f 0 s) :
    contactCoeff f s = 0 := by
  rw [contactCoeff_eq_normSq h]
  simp

/-- Cross-check: the T2 coefficient is the T1 determinant. -/
theorem contactCoeff_eq_det {f : ℂ → ℂ} {f' s : ℂ} (h : HasDerivAt f f' s) :
    contactCoeff f s = LinearMap.det ((fderiv ℝ f s : ℂ →L[ℝ] ℂ) : ℂ →ₗ[ℝ] ℂ) := by
  rw [contactCoeff_eq_normSq h, det_real_fderiv h]

/-! ## T5. Dissipation along a flow with positive-semidefinite mobility

Operator form (no matrices): `M : F →L[ℝ] F` with `0 ≤ ⟪v, M v⟫` for all v.
For a symmetric PSD matrix this is `Matrix.PosSemidef` read through `dotProduct_mulVec_nonneg`;
that bridge is NOT formalized here (open obligation). Symmetry of M is not needed for the
inequality, so it is not assumed. -/

section T5
variable {F : Type*} [NormedAddCommGroup F] [InnerProductSpace ℝ F] [CompleteSpace F]

/-- T5. If `x' = -M ∇E(x)` at `t`, with `E` having gradient `g` at `x t` and `M` PSD, then
`d/dt E(x t) = -⟪g, M g⟫ ≤ 0`. The flow equation is a hypothesis about `x`; the conclusion
is about `E ∘ x`; the conclusion is not among the hypotheses. -/
theorem energy_dissipation (E : F → ℝ) (x : ℝ → F) (M : F →L[ℝ] F)
    (hM : ∀ v, 0 ≤ inner ℝ v (M v)) {t : ℝ} {g : F}
    (hE : HasGradientAt E g (x t)) (hx : HasDerivAt x (-(M g)) t) :
    HasDerivAt (E ∘ x) (-(inner ℝ g (M g))) t ∧ deriv (E ∘ x) t ≤ 0 := by
  have h1 : HasFDerivAt E (InnerProductSpace.toDual ℝ F g) (x t) :=
    hasGradientAt_iff_hasFDerivAt.mp hE
  have h2 := h1.comp_hasDerivAt (x := t) hx
  have h3 : InnerProductSpace.toDual ℝ F g (-(M g)) = -(inner ℝ g (M g)) := by
    first
      | simp [inner_neg_right]
      | simp [InnerProductSpace.toDual_apply_apply, inner_neg_right]
  rw [h3] at h2
  refine ⟨h2, ?_⟩
  rw [h2.deriv]
  have := hM g
  linarith

end T5

/-! ## T3 coefficient level, k = 2 and k = 4

`lap2`, `lap4` are the Laplacian coefficients computed BY HAND (not via Mathlib's `laplacian`);
the bridge to Mathlib's `laplacian`/`HarmonicAt` is an open obligation. -/

/-- Laplacian of `a x² + b x y + c y²` is the constant `2a + 2c`. -/
def lap2 (a _b c : ℝ) : ℝ := 2 * a + 2 * c

/-- Re(w²) = x² - y², Im(w²) = 2xy. A real quadratic with `lap2 = 0` is `a Re w² + (b/2) Im w²`. -/
theorem harmonic_quadratic (a b c x y : ℝ) (h : lap2 a b c = 0) :
    a * x ^ 2 + b * x * y + c * y ^ 2
      = a * (x ^ 2 - y ^ 2) + (b / 2) * (2 * x * y) := by
  unfold lap2 at h
  have hc : c = -a := by linarith
  subst hc
  ring

/-- Laplacian coefficients of `c0 x⁴ + c1 x³y + c2 x²y² + c3 xy³ + c4 y⁴`:
`(12 c0 + 2 c2) x² + (6 c1 + 6 c3) x y + (2 c2 + 12 c4) y²`. -/
def lap4 (c0 c1 c2 c3 c4 : ℝ) : ℝ × ℝ × ℝ :=
  (12 * c0 + 2 * c2, 6 * c1 + 6 * c3, 2 * c2 + 12 * c4)

/-- Re(w⁴) = x⁴ - 6x²y² + y⁴, Im(w⁴) = 4x³y - 4xy³. -/
theorem harmonic_quartic (c0 c1 c2 c3 c4 x y : ℝ)
    (h : lap4 c0 c1 c2 c3 c4 = (0, 0, 0)) :
    c0 * x ^ 4 + c1 * x ^ 3 * y + c2 * x ^ 2 * y ^ 2 + c3 * x * y ^ 3 + c4 * y ^ 4
      = c0 * (x ^ 4 - 6 * x ^ 2 * y ^ 2 + y ^ 4) + (c1 / 4) * (4 * x ^ 3 * y - 4 * x * y ^ 3) := by
  unfold lap4 at h
  simp only [Prod.mk.injEq] at h
  obtain ⟨h1, h2, h3⟩ := h
  have e2 : c2 = -6 * c0 := by linarith
  have e3 : c3 = -c1 := by linarith
  have e4 : c4 = c0 := by linarith
  subst e2 e3 e4
  ring

end AXLE.Contact
