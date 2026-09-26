-- GATE-DECLARE: sorries = none
-- GATE-REASON: ch9 φ — ratio recursion, fixed point, alternation, contraction by 1/φ, exact closed form, golden-angle identities; table entry 13/8 checked.
/-
Orthogenesis/Phi/SubcriticalApproach.lean — Book 3, ch9 (φ · The Subcritical Approach).

  §1  Consecutive Fibonacci ratios r n = F(n+2)/F(n+1) obey r (n+1) = 1 + 1/r n.
  §2  φ is the fixed point of x ↦ 1 + 1/x.
  §3  The iterates alternate around φ: below φ maps above, above maps below.
  §4  For x ≥ 1 the map contracts distance to φ by at least the factor 1/φ ≈ 0.618.
  §5  φ can be written down exactly — (1 + √5)/2 — and is irrational: it is no fraction,
      but it is not "impossible to write".
  §6  Golden angle: 1 − 1/φ = 2 − φ = 1/φ², and 360°·(2 − φ) lies between 137.50° and 137.52°.
  §7  The table's 13/8 entry: the relative error is between 0.43% and 0.431%, not 0.45%.

Operator reading (docstring only): a contraction to a single fixed point has no threshold,
no jump and no history — every start ends at φ. It is U without K or F.
-/
import Mathlib

namespace Orthogenesis.SubcriticalApproach

open Real

/-! ## §1  Ratio recursion -/

noncomputable def r (n : ℕ) : ℝ := (Nat.fib (n + 2) : ℝ) / Nat.fib (n + 1)

theorem ratio_step (n : ℕ) : r (n + 1) = 1 + 1 / r n := by
  have h2 : (0 : ℝ) < Nat.fib (n + 2) := by exact_mod_cast Nat.fib_pos.mpr (by omega)
  have h3 : (Nat.fib (n + 3) : ℝ) = Nat.fib (n + 1) + Nat.fib (n + 2) := by
    have := Nat.fib_add_two (n := n + 1)
    simp only [show n + 1 + 2 = n + 3 from rfl, show n + 1 + 1 = n + 2 from rfl] at this
    exact_mod_cast this
  show (Nat.fib (n + 3) : ℝ) / Nat.fib (n + 2) = 1 + 1 / ((Nat.fib (n + 2) : ℝ) / Nat.fib (n + 1))
  rw [h3, one_div_div, add_div, div_self h2.ne']
  ring

/-! ## §2  Fixed point -/

theorem phi_fixed : 1 + 1 / goldenRatio = goldenRatio := by
  rw [one_div, inv_goldenRatio, ← one_sub_goldenConj]; ring

/-! ## §3  Alternation -/

theorem below_maps_above {x : ℝ} (hx : 0 < x) (h : x < goldenRatio) :
    goldenRatio < 1 + 1 / x := by
  have := one_div_lt_one_div_of_lt hx h
  linarith [phi_fixed]

theorem above_maps_below {x : ℝ} (h : goldenRatio < x) :
    1 + 1 / x < goldenRatio := by
  have := one_div_lt_one_div_of_lt goldenRatio_pos h
  linarith [phi_fixed]

/-! ## §4  Contraction toward φ -/

theorem contraction {x : ℝ} (hx : 1 ≤ x) :
    |(1 + 1 / x) - goldenRatio| ≤ |x - goldenRatio| / goldenRatio := by
  have hp := goldenRatio_pos
  have hx0 : 0 < x := by linarith
  have e : (1 + 1 / x) - goldenRatio = (goldenRatio - x) / (x * goldenRatio) := by
    rw [show (1 + 1 / x) - goldenRatio = 1 / x - 1 / goldenRatio by linarith [phi_fixed],
      div_sub_div _ _ hx0.ne' hp.ne']
    ring
  rw [e, abs_div, abs_of_pos (mul_pos hx0 hp), abs_sub_comm goldenRatio x,
    div_le_div_iff₀ (mul_pos hx0 hp) hp]
  nlinarith [mul_nonneg (mul_nonneg (abs_nonneg (x - goldenRatio)) hp.le) (sub_nonneg.mpr hx)]

/-! ## §5  φ is exact, and irrational -/

theorem phi_exact : goldenRatio = (1 + √5) / 2 ∧ Irrational goldenRatio :=
  ⟨rfl, goldenRatio_irrational⟩

/-! ## §6  Golden angle -/

theorem golden_angle_forms :
    1 - 1 / goldenRatio = 2 - goldenRatio ∧ 2 - goldenRatio = 1 / goldenRatio ^ 2 := by
  refine ⟨by linarith [phi_fixed], ?_⟩
  rw [goldenRatio_sq, eq_div_iff (by positivity)]
  linear_combination (-1 : ℝ) * goldenRatio_sq

lemma sqrt5_lo : (2236 : ℝ) / 1000 < √5 := (Real.lt_sqrt (by norm_num)).mpr (by norm_num)
lemma sqrt5_hi : √5 < 22361 / 10000 := (Real.sqrt_lt' (by norm_num)).mpr (by norm_num)
lemma sqrt5_lo' : (223606 : ℝ) / 100000 < √5 := (Real.lt_sqrt (by norm_num)).mpr (by norm_num)
lemma sqrt5_hi' : √5 < 223607 / 100000 := (Real.sqrt_lt' (by norm_num)).mpr (by norm_num)

theorem golden_angle_value :
    1375 / 10 < 360 * (2 - goldenRatio) ∧ 360 * (2 - goldenRatio) < 13752 / 100 := by
  have e : goldenRatio = (1 + √5) / 2 := rfl
  rw [e]; constructor <;> linarith [sqrt5_lo, sqrt5_hi]

/-! ## §7  The 13/8 row -/

theorem row_13_8 :
    43 / 10000 < (13 / 8 - goldenRatio) / goldenRatio ∧
    (13 / 8 - goldenRatio) / goldenRatio < 431 / 100000 := by
  have hp := goldenRatio_pos
  have e : goldenRatio = (1 + √5) / 2 := rfl
  constructor
  · rw [lt_div_iff₀ hp, e]; linarith [sqrt5_hi']
  · rw [div_lt_iff₀ hp, e]; linarith [sqrt5_lo']

end Orthogenesis.SubcriticalApproach

#print axioms Orthogenesis.SubcriticalApproach.ratio_step
#print axioms Orthogenesis.SubcriticalApproach.phi_fixed
#print axioms Orthogenesis.SubcriticalApproach.below_maps_above
#print axioms Orthogenesis.SubcriticalApproach.contraction
#print axioms Orthogenesis.SubcriticalApproach.phi_exact
#print axioms Orthogenesis.SubcriticalApproach.golden_angle_forms
#print axioms Orthogenesis.SubcriticalApproach.golden_angle_value
#print axioms Orthogenesis.SubcriticalApproach.row_13_8
