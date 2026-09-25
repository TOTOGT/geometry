-- GATE-DECLARE: sorries = none
-- GATE-REASON: new file 2026-09-25 for the geometry pin (Lean v4.32.0, Mathlib v4.32.0).
-- Author's build 2026-09-25: 25/25 on standard axioms (after adding the trig-derivative import).
/-
# A1Node.lean — the shared node of the figure-eight curves (Book 3, Ch 1)
# ======================================================================
# ch01-one-equation.html says the Gerono and Bernoulli lemniscates and the solar
# analemma share an A₁ singularity (an ordinary double point) at the origin, and
# that this is "verified in each Lean file via the self-intersection theorems".
# Those theorems only show that two parameter values reach the origin. This file
# supplies what an A₁ node actually requires, for the three curves and for the
# lunar analemma.
#
#   §1  The implicit polynomials F and their zero sets (linked to the curve files).
#   §2  Exact scaling F(s·x, s·y) = s²·Q(x, y) + s⁴·R(x, y): F and its gradient vanish
#       at the origin and its second-order part is Q.
#   §3  Q is non-degenerate and indefinite (det < 0).
#   §4  F takes both signs in every neighbourhood of the origin (a saddle, not an
#       extremum).
#   §5  The two parametrised branches through the origin cross transversally
#       (independent velocity vectors) — Gerono, solar and lunar analemma.
#   §6  The parameters that reach the origin are exactly t = kπ.
#
# What is NOT here: the Morse lemma (not in Mathlib), which is the step from
# "critical point with non-degenerate indefinite Hessian" to "locally two smooth
# transverse branches". §2–§4 are its hypotheses; §5 checks the conclusion directly
# for the parametrised curves.
-/

import Orthogenesis.Figure8.GeronoLemniscate
import Orthogenesis.Figure8.BernoulliLemniscate
import Orthogenesis.Figure8.Analemma
import Orthogenesis.Figure8.LunarAnalemma
import Mathlib.Analysis.SpecialFunctions.Trigonometric.Deriv

namespace Figure8

open Real

/-! ## §1 Implicit polynomials -/

def geronoF (x y : ℝ) : ℝ := x ^ 4 + y ^ 2 - x ^ 2
def bernoulliF (x y : ℝ) : ℝ := (x ^ 2 + y ^ 2) ^ 2 - 2 * (x ^ 2 - y ^ 2)
def solarF (x y : ℝ) : ℝ := x ^ 2 - 4 * y ^ 2 * (1 - y ^ 2)
def lunarF (x y : ℝ) : ℝ := x ^ 2 - 2 * y ^ 2 * (1 - y ^ 2)

theorem gerono_zero_set (x y : ℝ) :
    (x, y) ∈ GeronoLemniscate.lemniscate ↔ geronoF x y = 0 := by
  rw [GeronoLemniscate.mem_lemniscate, geronoF]
  constructor <;> intro h <;> linarith

theorem bernoulli_zero_set (x y : ℝ) :
    (x, y) ∈ BernoulliLemniscate.lemniscate ↔ bernoulliF x y = 0 := by
  rw [BernoulliLemniscate.mem_lemniscate, bernoulliF]
  constructor <;> intro h <;> linarith

theorem solar_on_zero_set {x y : ℝ} (h : (x, y) ∈ Analemma.analemma) : solarF x y = 0 := by
  rw [solarF, Analemma.analemma_implicit_fwd h]
  ring

theorem lunar_on_zero_set {x y : ℝ} (h : (x, y) ∈ LunarAnalemma.lunar) : lunarF x y = 0 := by
  rw [lunarF, LunarAnalemma.lunar_implicit_fwd h]
  ring

/-! ## §2 Exact scaling: second-order part Q, remainder of order four -/

theorem gerono_scaling (s x y : ℝ) :
    geronoF (s * x) (s * y) = s ^ 2 * (-x ^ 2 + y ^ 2) + s ^ 4 * x ^ 4 := by
  simp only [geronoF]; ring

theorem bernoulli_scaling (s x y : ℝ) :
    bernoulliF (s * x) (s * y) = s ^ 2 * (-2 * x ^ 2 + 2 * y ^ 2) + s ^ 4 * (x ^ 2 + y ^ 2) ^ 2 := by
  simp only [bernoulliF]; ring

theorem solar_scaling (s x y : ℝ) :
    solarF (s * x) (s * y) = s ^ 2 * (x ^ 2 - 4 * y ^ 2) + s ^ 4 * (4 * y ^ 4) := by
  simp only [solarF]; ring

theorem lunar_scaling (s x y : ℝ) :
    lunarF (s * x) (s * y) = s ^ 2 * (x ^ 2 - 2 * y ^ 2) + s ^ 4 * (2 * y ^ 4) := by
  simp only [lunarF]; ring

/-! ## §3 The quadratic parts are non-degenerate and indefinite

Q(x, y) = a·x² + c·y² has symmetric matrix diag(a, c); det = a·c. -/

theorem diag_det (a c : ℝ) : (!![a, 0; 0, c] : Matrix (Fin 2) (Fin 2) ℝ).det = a * c := by
  rw [Matrix.det_fin_two_of]; ring

theorem gerono_Q_indefinite : (!![-1, 0; 0, 1] : Matrix (Fin 2) (Fin 2) ℝ).det < 0 := by
  rw [diag_det]; norm_num
theorem bernoulli_Q_indefinite : (!![-2, 0; 0, 2] : Matrix (Fin 2) (Fin 2) ℝ).det < 0 := by
  rw [diag_det]; norm_num
theorem solar_Q_indefinite : (!![1, 0; 0, -4] : Matrix (Fin 2) (Fin 2) ℝ).det < 0 := by
  rw [diag_det]; norm_num
theorem lunar_Q_indefinite : (!![1, 0; 0, -2] : Matrix (Fin 2) (Fin 2) ℝ).det < 0 := by
  rw [diag_det]; norm_num

/-! ## §4 Saddle: F changes sign in every neighbourhood of the origin -/

lemma small_t {ε : ℝ} (hε : 0 < ε) : ∃ t : ℝ, 0 < t ∧ t < ε ∧ t ^ 4 < t ^ 2 := by
  have h0 : 0 < min (ε / 2) (1 / 2) := lt_min (by linarith) (by norm_num)
  have h1 : min (ε / 2) (1 / 2) ≤ 1 / 2 := min_le_right _ _
  have h2 : min (ε / 2) (1 / 2) < ε := lt_of_le_of_lt (min_le_left _ _) (by linarith)
  refine ⟨min (ε / 2) (1 / 2), h0, h2, ?_⟩
  set t := min (ε / 2) (1 / 2)
  have h3 : (0 : ℝ) < 1 - t ^ 2 := by nlinarith
  nlinarith [mul_pos (pow_pos h0 2) h3]

theorem gerono_saddle {ε : ℝ} (hε : 0 < ε) :
    ∃ t : ℝ, 0 < t ∧ t < ε ∧ geronoF t 0 < 0 ∧ 0 < geronoF 0 t := by
  obtain ⟨t, h0, htε, h4⟩ := small_t hε
  refine ⟨t, h0, htε, ?_, ?_⟩ <;> simp only [geronoF] <;> nlinarith [mul_pos h0 h0]

theorem bernoulli_saddle {ε : ℝ} (hε : 0 < ε) :
    ∃ t : ℝ, 0 < t ∧ t < ε ∧ bernoulliF t 0 < 0 ∧ 0 < bernoulliF 0 t := by
  obtain ⟨t, h0, htε, h4⟩ := small_t hε
  refine ⟨t, h0, htε, ?_, ?_⟩ <;> simp only [bernoulliF] <;> nlinarith [mul_pos h0 h0]

theorem solar_saddle {ε : ℝ} (hε : 0 < ε) :
    ∃ t : ℝ, 0 < t ∧ t < ε ∧ 0 < solarF t 0 ∧ solarF 0 t < 0 := by
  obtain ⟨t, h0, htε, h4⟩ := small_t hε
  refine ⟨t, h0, htε, ?_, ?_⟩ <;> simp only [solarF] <;> nlinarith [mul_pos h0 h0]

theorem lunar_saddle {ε : ℝ} (hε : 0 < ε) :
    ∃ t : ℝ, 0 < t ∧ t < ε ∧ 0 < lunarF t 0 ∧ lunarF 0 t < 0 := by
  obtain ⟨t, h0, htε, h4⟩ := small_t hε
  refine ⟨t, h0, htε, ?_, ?_⟩ <;> simp only [lunarF] <;> nlinarith [mul_pos h0 h0]

/-! ## §5 Transverse crossing of the parametrised branches -/

/-- 2×2 cross product: nonzero iff the two vectors are linearly independent. -/
def cross (a b : ℝ × ℝ) : ℝ := a.1 * b.2 - a.2 * b.1

/-- Velocity of γ(t) = (sin t, sin t · cos t). -/
noncomputable def geronoVel (t : ℝ) : ℝ × ℝ := (cos t, cos t * cos t + sin t * -sin t)

theorem gerono_hasDeriv (t : ℝ) :
    HasDerivAt (fun s => sin s) (geronoVel t).1 t ∧
      HasDerivAt (fun s => sin s * cos s) (geronoVel t).2 t :=
  ⟨Real.hasDerivAt_sin t, (Real.hasDerivAt_sin t).mul (Real.hasDerivAt_cos t)⟩

theorem gerono_transverse : cross (geronoVel 0) (geronoVel π) = 2 := by
  simp only [cross, geronoVel, Real.cos_zero, Real.sin_zero, Real.cos_pi, Real.sin_pi]
  norm_num

/-- Velocity of α(t) = (sin 2t, sin t). -/
noncomputable def solarVel (t : ℝ) : ℝ × ℝ := (cos (2 * t) * 2, cos t)

theorem solar_hasDeriv (t : ℝ) :
    HasDerivAt (fun s => sin (2 * s)) (solarVel t).1 t ∧
      HasDerivAt (fun s => sin s) (solarVel t).2 t := by
  refine ⟨?_, Real.hasDerivAt_sin t⟩
  simpa [solarVel] using ((hasDerivAt_id t).const_mul 2).sin

theorem solar_transverse : cross (solarVel 0) (solarVel π) = -4 := by
  simp only [cross, solarVel, mul_zero, Real.cos_zero, Real.cos_two_pi, Real.cos_pi]
  norm_num

/-- Velocity of α☽(t) = (sin 2t / √2, sin t). -/
noncomputable def lunarVel (t : ℝ) : ℝ × ℝ := (cos (2 * t) * 2 / Real.sqrt 2, cos t)

theorem lunar_hasDeriv (t : ℝ) :
    HasDerivAt (fun s => sin (2 * s) / Real.sqrt 2) (lunarVel t).1 t ∧
      HasDerivAt (fun s => sin s) (lunarVel t).2 t := by
  refine ⟨?_, Real.hasDerivAt_sin t⟩
  simpa [lunarVel] using (((hasDerivAt_id t).const_mul 2).sin).div_const (Real.sqrt 2)

theorem lunar_transverse : cross (lunarVel 0) (lunarVel π) ≠ 0 := by
  have h2 : (0 : ℝ) < Real.sqrt 2 := Real.sqrt_pos.mpr (by norm_num)
  have e : cross (lunarVel 0) (lunarVel π) = -(4 / Real.sqrt 2) := by
    simp only [cross, lunarVel, mul_zero, Real.cos_zero, Real.cos_two_pi, Real.cos_pi]
    ring
  rw [e]
  exact neg_ne_zero.mpr (by positivity)

/-! ## §6 The parameters reaching the origin are exactly kπ -/

theorem gerono_origin_iff (t : ℝ) :
    (sin t, sin t * cos t) = ((0 : ℝ), (0 : ℝ)) ↔ ∃ n : ℤ, (n : ℝ) * π = t := by
  rw [← Real.sin_eq_zero_iff, Prod.mk.injEq]
  constructor
  · rintro ⟨h, _⟩; exact h
  · intro h; exact ⟨h, by rw [h, zero_mul]⟩

theorem solar_origin_iff (t : ℝ) :
    Analemma.param t = (0, 0) ↔ ∃ n : ℤ, (n : ℝ) * π = t := by
  rw [← Real.sin_eq_zero_iff]
  simp only [Analemma.param, Prod.mk.injEq]
  constructor
  · rintro ⟨_, h⟩; exact h
  · intro h; exact ⟨by rw [Real.sin_two_mul, h]; ring, h⟩

theorem lunar_origin_iff (t : ℝ) :
    LunarAnalemma.param t = (0, 0) ↔ ∃ n : ℤ, (n : ℝ) * π = t := by
  rw [← Real.sin_eq_zero_iff]
  simp only [LunarAnalemma.param, Prod.mk.injEq]
  constructor
  · rintro ⟨_, h⟩; exact h
  · intro h; exact ⟨by rw [Real.sin_two_mul, h]; simp, h⟩

end Figure8

/-! ## Axiom probe -/
#print axioms Figure8.gerono_zero_set
#print axioms Figure8.bernoulli_zero_set
#print axioms Figure8.solar_on_zero_set
#print axioms Figure8.lunar_on_zero_set
#print axioms Figure8.gerono_scaling
#print axioms Figure8.bernoulli_scaling
#print axioms Figure8.solar_scaling
#print axioms Figure8.lunar_scaling
#print axioms Figure8.gerono_Q_indefinite
#print axioms Figure8.bernoulli_Q_indefinite
#print axioms Figure8.solar_Q_indefinite
#print axioms Figure8.lunar_Q_indefinite
#print axioms Figure8.gerono_saddle
#print axioms Figure8.bernoulli_saddle
#print axioms Figure8.solar_saddle
#print axioms Figure8.lunar_saddle
#print axioms Figure8.gerono_hasDeriv
#print axioms Figure8.gerono_transverse
#print axioms Figure8.solar_hasDeriv
#print axioms Figure8.solar_transverse
#print axioms Figure8.lunar_hasDeriv
#print axioms Figure8.lunar_transverse
#print axioms Figure8.gerono_origin_iff
#print axioms Figure8.solar_origin_iff
#print axioms Figure8.lunar_origin_iff
