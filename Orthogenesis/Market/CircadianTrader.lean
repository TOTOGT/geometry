-- GATE-DECLARE: sorries = none
-- GATE-REASON: new file 2026-09-25 for the geometry pin (Lean v4.32.0, Mathlib v4.32.0).
-- UNTESTED until the author runs `lake build` on it.
/-
# CircadianTrader.lean — Book 3 (Cajueiro edition), Ch 3c · The Circadian Trader
# (ch3c-econophysics.html, off the taught-path roster)

  §1  The T operator, T(n) = log 3 − v₂(n)·log 2. It does not depend on
      wall-clock time at all — which is why Theorem 2.1 (timezone
      independence) holds, and also why T cannot carry the 24 h / 29.5 d /
      365 d periods §1.1 attributes to it. It is not a time reparametrisation
      either: it is not monotone (T(4) < T(3)) and takes negative values
      (T(4) = log 3 − 2 log 2 < 0), so it cannot "count Reeb orbit cycles".
  §2  The bot's signal (§3.1). With dz = p·Δp and dq = Δp − Δp_prev, the code's
      Λ = |dz + p·dq| equals |p|·|Δp + dq|, and it vanishes (p ≠ 0) exactly when
      Δp = Δp_prev / 2: the entry fires when the last price change is half the
      previous one. The accumulated history z is computed and never used; the
      rule is a momentum-decay filter, not a geometric condition.
  §3  The standstill arithmetic of the analemma interlude: 23.4 + 5.1 = 28.5 and
      23.4 − 5.1 = 18.3, as printed.

CircadianReeb.lean (chapter 3) already covers the contact model used here:
α = dz + p dq has Reeb field ∂/∂z, whose flow has no closed orbit and no
attractor in these coordinates — so "the Reeb orbit is the periodic attractor"
(§2.1) does not hold in the chapter's own model.

Not formalised: Theorem 2.2 (the expected value of a position is not defined in
the model). As of 2026-09-25, `AXLE/MarketThreshold.lean`, the theorem
`legendrian_entry_ev`, and `bot.py` are not in the local TOTOGT/AXLE or
TOTOGT/geometry repositories.
-/

import Mathlib

namespace Orthogenesis.CircadianTrader

open Real

/-! ## §1 The T operator -/

/-- T(n) = log 3 − v₂(n)·log 2. -/
noncomputable def Tclock (n : ℕ) : ℝ := Real.log 3 - (padicValNat 2 n : ℝ) * Real.log 2

/-- T depends on the process index only: a shift of wall-clock time changes nothing,
    because wall-clock time does not enter T at all. -/
theorem T_ignores_clock (n : ℕ) (t Δ : ℝ) :
    (fun _ : ℝ => Tclock n) (t + Δ) = (fun _ : ℝ => Tclock n) t := rfl

theorem v2_three : padicValNat 2 3 = 0 :=
  padicValNat.eq_zero_of_not_dvd (by norm_num)

theorem v2_four : padicValNat 2 4 = 2 := by
  rw [show (4 : ℕ) = 2 ^ 2 by norm_num]
  exact padicValNat.prime_pow 2

/-- T is not monotone: T(4) < T(3). -/
theorem T_not_monotone : Tclock 4 < Tclock 3 := by
  unfold Tclock
  rw [v2_three, v2_four]
  have := Real.log_pos (by norm_num : (1 : ℝ) < 2)
  push_cast
  linarith

/-- T takes negative values: T(4) = log 3 − 2 log 2 < 0. -/
theorem T_four_neg : Tclock 4 < 0 := by
  unfold Tclock
  rw [v2_four]
  have h : Real.log 3 < Real.log 4 := Real.log_lt_log (by norm_num) (by norm_num)
  have h4 : Real.log 4 = 2 * Real.log 2 := by
    rw [show (4 : ℝ) = 2 ^ 2 by norm_num, Real.log_pow]
    push_cast
    ring
  push_cast
  linarith

/-! ## §2 The bot's alignment quantity -/

/-- The code's Λ = |dz + p·dq| with dz = p·Δp. -/
def lam (p dp dq : ℝ) : ℝ := |p * dp + p * dq|

theorem lam_factor (p dp dq : ℝ) : lam p dp dq = |p| * |dp + dq| := by
  unfold lam
  rw [← mul_add, abs_mul]

/-- With dq = Δp − Δp_prev, Λ = 0 exactly when p = 0 or Δp = Δp_prev / 2. -/
theorem lam_zero_iff (p dp dp₀ : ℝ) :
    lam p dp (dp - dp₀) = 0 ↔ p = 0 ∨ dp = dp₀ / 2 := by
  unfold lam
  rw [← mul_add, abs_eq_zero, mul_eq_zero]
  constructor
  · rintro (h | h)
    · exact Or.inl h
    · right; linarith
  · rintro (h | h)
    · exact Or.inl h
    · right; linarith

/-! ## §3 Lunar standstill arithmetic -/

theorem standstills : (23.4 : ℝ) + 5.1 = 28.5 ∧ (23.4 : ℝ) - 5.1 = 18.3 := by norm_num

end Orthogenesis.CircadianTrader

/-! ## Axiom probe -/
#print axioms Orthogenesis.CircadianTrader.T_ignores_clock
#print axioms Orthogenesis.CircadianTrader.v2_three
#print axioms Orthogenesis.CircadianTrader.v2_four
#print axioms Orthogenesis.CircadianTrader.T_not_monotone
#print axioms Orthogenesis.CircadianTrader.T_four_neg
#print axioms Orthogenesis.CircadianTrader.lam_factor
#print axioms Orthogenesis.CircadianTrader.lam_zero_iff
#print axioms Orthogenesis.CircadianTrader.standstills
