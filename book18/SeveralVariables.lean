import Mathlib

/-
Volume XVIII — chapter 8: several variables. Lean core.

STATUS: UNTESTED. Written without a Lean toolchain; not compiled by anyone. Until the author runs it
and saves the output as severalvariables.axioms.txt, nothing in this file counts as checked. To run:
  lake env lean book18/SeveralVariables.lean 2>&1 | tee book18/severalvariables.axioms.txt

The statements follow Loomis and Sternberg, Advanced Calculus (revised ed., 1990), printed pages:
  directional_derivative_eq_differential   Theorem 7.1 (p.147): a differentiable map has directional
                                           derivative equal to the differential applied to the direction
  differential_is_partials_combination     Theorem 9.2 (p.157), in the plane: dF(a,b) = a F_x + b F_y
  partial_x_eq_differential                the partial derivative F_x is the differential applied to (1,0)
  partial_x_example, partial_y_example     an explicit pair of partial derivatives, by hand
  directional_derivative_le_gradient_norm  the direction of steepest ascent, upper bound (plane)
  directional_derivative_attains           ... and the bound is attained in the direction of the gradient
  second_differential_symmetric            Theorem 16.3 (p.187): the second differential is symmetric
  cf_dx, cf_dy, mixed_partials_differ      control: for f = xy(x^2-y^2)/(x^2+y^2) (f(0,0) = 0), the two mixed
                                           partials at the origin are -1 and +1, so the hypothesis of
                                           Theorem 16.3 (second differential exists) really is needed
  area_scales_by_det                       Theorem 8.1 (p.335): measure of L(A) is |det L| times that of A

WHAT THESE PROOFS ARE. directional_derivative_eq_differential, second_differential_symmetric and
area_scales_by_det call Mathlib's own theorems (the chain rule, symmetry of the second derivative,
the Haar-measure scaling lemma). The statements are restated so that the sentence being checked is the
textbook's, over any normed space for the first two. The control cf_dx / cf_dy / mixed_partials_differ is
proved here by hand and is the one new computation in the file.

WHAT IT DOES NOT STATE.
  - Fubini's theorem (successive integration, LS §12 p.346), the change of variables formula (§11 p.342),
    the implicit function theorem, and the mean value theorem. The page shows exact examples of the first;
    none of them is in this file.
  - Line and surface integrals and Stokes' theorem (LS Chapter 11).
  - Theorem 9.3 (continuous partials imply differentiable).

NAMES MOST LIKELY TO NEED A FIX AGAINST THE REAL COMPILER (flagged in advance, not known to fail):
  HasFDerivAt.comp_hasDerivAt, HasDerivAt.smul_const, ContDiffAt.isSymmSndFDerivAt (and the side condition
  on minSmoothness), MeasureTheory.Measure.addHaar_image_linearMap, hasDerivAt_iff_tendsto_slope,
  slope_def_field, Real.abs_le_sqrt, and the `field_simp` / `simpa` steps.

Toolchain: repository pin, leanprover/lean4:v4.32.0 with Mathlib v4.32.0.
-/

namespace Book18SV

open Filter Topology MeasureTheory

/-- Theorem 7.1: if F is differentiable at p, the directional derivative in direction v exists and is
the differential applied to v. -/
theorem directional_derivative_eq_differential {E : Type*} [NormedAddCommGroup E] [NormedSpace ℝ E]
    {f : E → ℝ} {f' : E →L[ℝ] ℝ} {p : E} (hf : HasFDerivAt f f' p) (v : E) :
    HasDerivAt (fun t : ℝ => f (p + t • v)) (f' v) 0 := by
  have h1 : HasDerivAt (fun t : ℝ => p + t • v) v 0 := by
    simpa using ((hasDerivAt_id (0 : ℝ)).smul_const v).const_add p
  have hf' : HasFDerivAt f f' (p + (0 : ℝ) • v) := by simpa using hf
  exact hf'.comp_hasDerivAt (0 : ℝ) h1

/-- Theorem 9.2 in the plane: a linear map is determined by its two partial values. -/
theorem differential_is_partials_combination (f' : ℝ × ℝ →L[ℝ] ℝ) (a b : ℝ) :
    f' (a, b) = a * f' (1, 0) + b * f' (0, 1) := by
  have h : ((a, b) : ℝ × ℝ) = a • ((1, 0) : ℝ × ℝ) + b • ((0, 1) : ℝ × ℝ) := by
    ext <;> simp
  rw [h, map_add, map_smul, map_smul]
  simp [smul_eq_mul]

/-- The partial derivative in x is the differential applied to (1, 0). -/
theorem partial_x_eq_differential {f : ℝ × ℝ → ℝ} {f' : ℝ × ℝ →L[ℝ] ℝ} {p : ℝ × ℝ}
    (hf : HasFDerivAt f f' p) :
    HasDerivAt (fun t : ℝ => f (p.1 + t, p.2)) (f' (1, 0)) 0 := by
  have h := directional_derivative_eq_differential hf ((1 : ℝ), (0 : ℝ))
  have e : (fun t : ℝ => f (p + t • ((1 : ℝ), (0 : ℝ)))) = fun t : ℝ => f (p.1 + t, p.2) := by
    funext t
    congr 1
    ext <;> simp
  rw [e] at h
  exact h

/-- Example: for f(x, y) = x^2 y + y^3 the partial derivative in x is 2xy. -/
theorem partial_x_example (x y : ℝ) :
    HasDerivAt (fun t : ℝ => t ^ 2 * y + y ^ 3) (2 * x * y) x := by
  simpa using ((hasDerivAt_pow 2 x).mul_const y).add_const (y ^ 3)

/-- Example: for f(x, y) = x^2 y + y^3 the partial derivative in y is x^2 + 3y^2. -/
theorem partial_y_example (x y : ℝ) :
    HasDerivAt (fun t : ℝ => x ^ 2 * t + t ^ 3) (x ^ 2 + 3 * y ^ 2) y := by
  simpa using ((hasDerivAt_id y).const_mul (x ^ 2)).add (hasDerivAt_pow 3 y)

/-- Steepest ascent, upper bound: for a unit vector (u, v), a u + b v <= sqrt(a^2 + b^2). Here (a, b)
is the gradient and a u + b v is the directional derivative. -/
theorem directional_derivative_le_gradient_norm (a b u v : ℝ) (huv : u ^ 2 + v ^ 2 = 1) :
    a * u + b * v ≤ Real.sqrt (a ^ 2 + b ^ 2) := by
  have h1 : (a * u + b * v) ^ 2 + (a * v - b * u) ^ 2 = (a ^ 2 + b ^ 2) * (u ^ 2 + v ^ 2) := by
    ring
  rw [huv, mul_one] at h1
  have h2 : (a * u + b * v) ^ 2 ≤ a ^ 2 + b ^ 2 := by
    nlinarith [sq_nonneg (a * v - b * u)]
  exact le_trans (le_abs_self _) (Real.abs_le_sqrt h2)

/-- Steepest ascent, attained: in the direction of the gradient (a, b) != 0 the bound is an equality,
and that direction has length 1. -/
theorem directional_derivative_attains (a b : ℝ) (h : a ^ 2 + b ^ 2 ≠ 0) :
    (a / Real.sqrt (a ^ 2 + b ^ 2)) ^ 2 + (b / Real.sqrt (a ^ 2 + b ^ 2)) ^ 2 = 1 ∧
      a * (a / Real.sqrt (a ^ 2 + b ^ 2)) + b * (b / Real.sqrt (a ^ 2 + b ^ 2)) =
        Real.sqrt (a ^ 2 + b ^ 2) := by
  have hpos : 0 < a ^ 2 + b ^ 2 := lt_of_le_of_ne (by positivity) (Ne.symm h)
  have hs : 0 < Real.sqrt (a ^ 2 + b ^ 2) := Real.sqrt_pos.2 hpos
  have hss : Real.sqrt (a ^ 2 + b ^ 2) * Real.sqrt (a ^ 2 + b ^ 2) = a ^ 2 + b ^ 2 :=
    Real.mul_self_sqrt hpos.le
  constructor
  · field_simp
    nlinarith [hss]
  · field_simp
    nlinarith [hss]

/-- Theorem 16.3: the second differential is a symmetric function of its two arguments (for a twice
continuously differentiable function; the textbook assumes the second differential exists and is
continuous). -/
theorem second_differential_symmetric {E : Type*} [NormedAddCommGroup E] [NormedSpace ℝ E]
    (f : E → ℝ) (x : E) (hf : ContDiff ℝ 2 f) (v w : E) :
    fderiv ℝ (fderiv ℝ f) x v w = fderiv ℝ (fderiv ℝ f) x w v :=
  (hf.contDiffAt.isSymmSndFDerivAt (by simp [minSmoothness_of_isRCLikeNormedField])) v w

/-- The control function: xy(x^2 - y^2)/(x^2 + y^2), equal to 0 at the origin (Lean's x/0 = 0). -/
noncomputable def cf (x y : ℝ) : ℝ := x * y * (x ^ 2 - y ^ 2) / (x ^ 2 + y ^ 2)

/-- Control, first partial at the origin column: d/dx cf(x, y) at x = 0 equals -y. -/
theorem cf_dx (y : ℝ) : HasDerivAt (fun x => cf x y) (-y) 0 := by
  by_cases hy : y = 0
  · subst hy
    have e : (fun x => cf x 0) = fun _ => (0 : ℝ) := by
      funext x
      simp [cf]
    rw [e]
    simpa using hasDerivAt_const (0 : ℝ) (0 : ℝ)
  · rw [hasDerivAt_iff_tendsto_slope]
    have hc : Continuous fun h : ℝ => y * (h ^ 2 - y ^ 2) / (h ^ 2 + y ^ 2) := by
      apply Continuous.div (by fun_prop) (by fun_prop)
      intro h
      positivity
    have h0 := hc.tendsto 0
    have h1 : y * ((0 : ℝ) ^ 2 - y ^ 2) / ((0 : ℝ) ^ 2 + y ^ 2) = -y := by
      field_simp <;> ring
    rw [h1] at h0
    have ht : Tendsto (fun h : ℝ => y * (h ^ 2 - y ^ 2) / (h ^ 2 + y ^ 2)) (𝓝[≠] 0) (𝓝 (-y)) :=
      h0.mono_left nhdsWithin_le_nhds
    refine ht.congr' ?_
    filter_upwards [self_mem_nhdsWithin] with h hh
    have hh' : h ≠ 0 := hh
    have hd : h ^ 2 + y ^ 2 ≠ 0 := by positivity
    rw [slope_def_field]
    simp only [cf]
    field_simp <;> ring

/-- Control, second: d/dy cf(x, y) at y = 0 equals x. cf is antisymmetric: cf x y = - cf y x. -/
theorem cf_dy (x : ℝ) : HasDerivAt (fun y => cf x y) x 0 := by
  have e : (fun y => cf x y) = fun y => -(cf y x) := by
    funext y
    simp only [cf]
    rw [add_comm (y ^ 2) (x ^ 2)]
    ring
  rw [e]
  simpa using (cf_dx x).neg

/-- Control: the two mixed partials of cf at the origin are -1 and +1, so they differ. The
symmetry theorem needs its hypothesis. -/
theorem mixed_partials_differ :
    deriv (fun y => deriv (fun x => cf x y) 0) 0 = -1 ∧
      deriv (fun x => deriv (fun y => cf x y) 0) 0 = 1 := by
  have hx : ∀ y, deriv (fun x => cf x y) 0 = -y := fun y => (cf_dx y).deriv
  have hy : ∀ x, deriv (fun y => cf x y) 0 = x := fun x => (cf_dy x).deriv
  constructor <;> simp [hx, hy]

/-- Theorem 8.1: a linear map of the plane multiplies area by |det|. Mathlib's Haar-measure scaling
lemma, applied to Lebesgue measure on the plane. -/
theorem area_scales_by_det (L : (Fin 2 → ℝ) →ₗ[ℝ] (Fin 2 → ℝ)) (A : Set (Fin 2 → ℝ)) :
    volume (L '' A) = ENNReal.ofReal |LinearMap.det L| * volume A :=
  MeasureTheory.Measure.addHaar_image_linearMap _ L A

#print axioms directional_derivative_eq_differential
#print axioms differential_is_partials_combination
#print axioms partial_x_eq_differential
#print axioms partial_x_example
#print axioms partial_y_example
#print axioms directional_derivative_le_gradient_norm
#print axioms directional_derivative_attains
#print axioms second_differential_symmetric
#print axioms cf_dx
#print axioms cf_dy
#print axioms mixed_partials_differ
#print axioms area_scales_by_det

end Book18SV
