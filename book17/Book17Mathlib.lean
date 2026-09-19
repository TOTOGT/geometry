/-
Volume XVII — rung 17. The elementary rows, checked.

Book XVII's index and chapter 1 print these as facts about how a
total-function kernel behaves. Here they are as theorems.

Every claim below is one the two pages print.  Each is stated here as a
theorem and closed; the `#print axioms` block at the foot is the report the
gate reads.  Mathlib is required for the four real-analysis rows and for the
probability row; the rows that need no library at all are in Book17Core.lean,
which imports nothing.

Toolchain: Lean 4.33.0-rc1.  Mathlib: tag v4.33.0-rc1.
-/
import Mathlib.Analysis.SpecialFunctions.Sqrt
import Mathlib.Analysis.SpecialFunctions.Log.Basic
import Mathlib.Probability.Moments.Variance
import Mathlib.Order.Filter.Basic

open MeasureTheory ProbabilityTheory

/-- The page prints `√(−1) = 0`. -/
theorem sqrt_neg_one : Real.sqrt (-1) = 0 := by
  simpa using Real.sqrt_eq_zero_of_nonpos (by norm_num : (-1:ℝ) ≤ 0)

/-- Not an accident of the argument −1: the square root is total on ℝ and
    takes the value 0 on the whole negative ray. -/
theorem sqrt_any_neg (x : ℝ) (h : x < 0) : Real.sqrt x = 0 :=
  Real.sqrt_eq_zero_of_nonpos (le_of_lt h)

/-- `x / 0 = 0` survives into the field of real numbers. -/
theorem real_div_zero (x : ℝ) : x / 0 = 0 := div_zero x

theorem real_inv_zero : (0 : ℝ)⁻¹ = 0 := inv_zero

theorem real_zero_pow_zero : (0 : ℝ) ^ (0 : ℕ) = 1 := pow_zero 0

/-- The same convention reaches the logarithm, where it is less advertised. -/
theorem real_log_zero : Real.log 0 = 0 := Real.log_zero

theorem real_log_neg : Real.log (-1) = 0 := by
  rw [Real.log_neg_eq_log, Real.log_one]

/-- The index page says "limits are filters".  Not a metaphor and not a
    reformulation: `Tendsto` unfolds, definitionally, to an inequality
    between two filters, which is why `Iff.rfl` closes it. -/
theorem tendsto_is_filter_le {α β : Type} (f : α → β) (l₁ : Filter α) (l₂ : Filter β) :
    Filter.Tendsto f l₁ l₂ ↔ Filter.map f l₁ ≤ l₂ := Iff.rfl

/-- The index page says "let X be a random variable" is a measurable-space
    instance with side conditions.  Here is the side condition with a price
    on it: a variable with no second moment does not make `variance`
    undefined -- it makes it zero, silently, and the zero is a theorem. -/
theorem variance_is_total {Ω : Type} [MeasurableSpace Ω] (μ : Measure Ω)
    [IsFiniteMeasure μ] (X : Ω → ℝ)
    (hX : AEStronglyMeasurable X μ) (hX2 : ¬ MemLp X 2 μ) :
    variance X μ = 0 :=
  variance_of_not_memLp hX hX2

#print axioms sqrt_neg_one
#print axioms sqrt_any_neg
#print axioms real_div_zero
#print axioms real_inv_zero
#print axioms real_zero_pow_zero
#print axioms real_log_zero
#print axioms real_log_neg
#print axioms tendsto_is_filter_le
#print axioms variance_is_total
