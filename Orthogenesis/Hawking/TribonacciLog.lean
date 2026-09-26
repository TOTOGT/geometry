/-
  TribonacciLog.lean
  Principia Orthogona · Orthogenesis · Hawking
  Closing the chain from the tribonacci constant to `tribonacci_factor`.

  WHY THIS FILE EXISTS
  --------------------
  `HawkingConstants.tribonacci_factor` reads

      theorem tribonacci_factor (l : ℝ) (hl : 0.60937 < l ∧ l < 0.60939) :
          1.0969 < 1 + l / (2 * π) ∧ 1 + l / (2 * π) < 1.0971

  It is true and it is kernel-checked. It is also a statement about ANY real
  number in a numeric window. Nothing in it says `l = Real.log η`, nothing says
  η is the tribonacci constant, and nothing connects η to x³ = x² + x + 1.
  The identification lives in prose, so the kernel never sees the step that
  carries the meaning. That is the same shape as `mu_dm3_neg`, which proves
  `(-2 : ℝ) < 0` while a docstring asserts the -2 is μmax.

  This file supplies the missing link: η enters by its DEFINING EQUATION and
  comes out as a bound on `Real.log η`, which is exactly `tribonacci_factor`'s
  hypothesis.

  WHAT IS PROVED HERE
    §1  η is bracketed by its cubic:            1.83928 < η < 1.83929
    §2  those brackets give the log bounds, GIVEN two numeric exp facts
    §3  the composite: cubic in, 1.0969–1.0971 out

  WHAT IS NOT PROVED HERE, AND IS VISIBLE AS A HYPOTHESIS
    exp 0.60937 < 1.83928   and   1.83929 < exp 0.60939
  Both are true — to eighteen digits,
      exp 0.60937 = 1.839272292157329
      η           = 1.839286755214161
      exp 0.60939 = 1.839309077971029
  — with margins 7.71e-6 below and 1.91e-5 above. Discharging them in Lean
  needs `Real.exp_bound` and a Taylor sandwich, which is a separate piece of
  work. They are carried as named hypotheses rather than asserted, so the
  kernel shows what the result rests on. Same treatment as
  `epsilon0_eq_third_iff` in book2/lean/StabilityRadius.lean.

  STATUS: NOT BUILT. No Lean toolchain on the desk that wrote it. The §1
  `nlinarith` calls are the part most likely to need hint tuning; the numbers
  they are asked to prove are correct.
-/
import Mathlib.Analysis.SpecialFunctions.Log.Basic
-- §3 applies `tribonacci_factor`, which lives in HawkingConstants.lean.
-- If that file declares it outside `Orthogenesis.HawkingConstants`, either
-- drop the `namespace` line below or qualify the call in §3.
import Orthogenesis.Hawking.HawkingConstants

namespace Orthogenesis.HawkingConstants

open Real

/-! ## §1  The tribonacci constant, by its cubic

`p x = x³ - x² - x - 1` has `p' x = 3x² - 2x - 1 = (3x + 1)(x - 1)`, which is
strictly positive for `x > 1`. So `p` is strictly increasing there and the root
above 1 is unique. The brackets follow from `p 1.83928 < 0 < p 1.83929`. -/

/-- The defining property, stated once so it cannot drift. -/
def IsTribonacci (η : ℝ) : Prop := 1 < η ∧ η ^ 3 = η ^ 2 + η + 1

theorem tribonacci_gt {η : ℝ} (h : IsTribonacci η) : 1.83928 < η := by
  obtain ⟨h1, hc⟩ := h
  by_contra hle
  push_neg at hle
  -- 1 < η ≤ 1.83928 and η³ = η² + η + 1 are inconsistent, because p is
  -- increasing on (1, ∞) and p 1.83928 < 0.
  nlinarith [hc, h1, hle, sq_nonneg (η - 1), sq_nonneg (η - 1.83928),
             mul_pos (show (0:ℝ) < η - 1 by linarith)
                     (show (0:ℝ) < 3 * η + 1 by linarith)]

theorem tribonacci_lt {η : ℝ} (h : IsTribonacci η) : η < 1.83929 := by
  obtain ⟨h1, hc⟩ := h
  by_contra hge
  push_neg at hge
  nlinarith [hc, h1, hge, sq_nonneg (η - 1), sq_nonneg (η - 1.83929),
             mul_pos (show (0:ℝ) < η - 1 by linarith)
                     (show (0:ℝ) < 3 * η + 1 by linarith)]

theorem tribonacci_bracket {η : ℝ} (h : IsTribonacci η) :
    1.83928 < η ∧ η < 1.83929 :=
  ⟨tribonacci_gt h, tribonacci_lt h⟩

theorem tribonacci_pos {η : ℝ} (h : IsTribonacci η) : 0 < η := by
  have := h.1; linarith

/-! ## §2  From the bracket to the log bounds

`Real.lt_log_iff_exp_lt` and `Real.log_lt_iff_lt_exp` turn the goal into the two
numeric exp facts, which are carried as hypotheses. -/

/-- **The missing link.** With η pinned by its cubic, `Real.log η` lands in
exactly the window `tribonacci_factor` assumes.

The two `exp` hypotheses are the only inputs: both are true, neither is
discharged here, and both are stated in the header with their values. -/
theorem log_tribonacci_bounds {η : ℝ} (h : IsTribonacci η)
    (hlo : Real.exp 0.60937 < 1.83928)
    (hhi : (1.83929 : ℝ) < Real.exp 0.60939) :
    0.60937 < Real.log η ∧ Real.log η < 0.60939 := by
  obtain ⟨hb1, hb2⟩ := tribonacci_bracket h
  have hpos : 0 < η := tribonacci_pos h
  constructor
  · rw [Real.lt_log_iff_exp_lt hpos]
    linarith
  · rw [Real.log_lt_iff_lt_exp hpos]
    linarith

/-! ## §3  The composite

This is what `ch-hawking` should cite. η goes in as a root of its cubic; the
bound comes out. Nothing between them is asserted in prose. -/

theorem tribonacci_factor_of_cubic {η : ℝ} (h : IsTribonacci η)
    (hlo : Real.exp 0.60937 < 1.83928)
    (hhi : (1.83929 : ℝ) < Real.exp 0.60939) :
    1.0969 < 1 + Real.log η / (2 * π) ∧ 1 + Real.log η / (2 * π) < 1.0971 :=
  tribonacci_factor (Real.log η) (log_tribonacci_bounds h hlo hhi)

/-- The tribonacci constant exists and is unique above 1. Recorded so that
`IsTribonacci` is not vacuous — a hypothesis nothing satisfies proves anything,
which is the failure mode R20 exists to catch. -/
theorem isTribonacci_nonvacuous : ∃ η : ℝ, IsTribonacci η := by
  set f : ℝ → ℝ := fun x => x ^ 3 - x ^ 2 - x - 1 with hf_def
  have hcont : ContinuousOn f (Set.Icc 1 2) := (by continuity : Continuous f).continuousOn
  -- Pin the target value (0) down BEFORE applying the subset proof, as an
  -- explicit membership fact -- the earlier version left it as a metavariable,
  -- which is what "linarith failed to find a contradiction" was reporting.
  have hmem : (0 : ℝ) ∈ Set.Ioo (f 1) (f 2) := by
    constructor <;> simp only [hf_def] <;> norm_num
  obtain ⟨x, hx, hfx⟩ :=
    intermediate_value_Ioo (by norm_num : (1:ℝ) ≤ 2) hcont hmem
  refine ⟨x, hx.1, ?_⟩
  have hfx' : x ^ 3 - x ^ 2 - x - 1 = 0 := hfx
  linarith

end Orthogenesis.HawkingConstants
