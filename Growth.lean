-- Growth.lean
import Mathlib.Analysis.SpecialFunctions.Pow.NNReal

namespace Orthogenesis

structure GrowthParams where
  g      : ℝ
  stages : ℕ
  target : ℝ
  -- rel lives as a hypothesis, not a field
deriving Repr

/-- Geometric radius at stage n: g^n (natural number power). -/
def R (P : GrowthParams) (n : ℕ) : ℝ := P.g ^ n

/-- Monotone growth when g > 1. -/
lemma R_mono (P : GrowthParams) (hg : 1 < P.g) (n m : ℕ) (h : n ≤ m) :
    R P n ≤ R P m := by
  unfold R
  exact pow_le_pow_right (le_of_lt hg) h

end Orthogenesis
