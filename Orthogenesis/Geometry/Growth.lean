import Mathlib

namespace Orthogenesis

structure GrowthParams where
  g      : ℝ
  stages : ℕ
  target : ℝ
  rel    : Prop

noncomputable def R (P : GrowthParams) (n : ℕ) : ℝ :=
  P.g ^ (n : ℝ)

/-- Growth is monotone in the phase index when the growth factor exceeds 1
    (the discrete Lyapunov-descent monotonicity). -/
theorem R_mono {P : GrowthParams} {n m : ℕ} (hg : 1 < P.g) (hnm : n ≤ m) :
    R P n ≤ R P m := by
  unfold R
  exact Real.rpow_le_rpow_of_exponent_le (le_of_lt hg) (by exact_mod_cast hnm)

end Orthogenesis
