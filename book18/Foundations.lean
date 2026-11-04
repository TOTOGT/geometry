import Mathlib

/-
Book XVIII, chapter 9: foundations of analysis. Lean core.

STATUS: UNTESTED. Written 2026-11-04 without a Lean toolchain; the author has not compiled it. Nothing here is
verified until `lake env lean book18/Foundations.lean 2>&1 | tee book18/foundations.axioms.txt` has been run and
its real output read. Lemma names are from memory of Mathlib; errors are expected to be about names or small
simp/field_simp steps, and are to be fixed against what the compiler actually says.

The statements follow Lebl, Basic Analysis I, v6.3 (printed page = pdf page):
  completeness               Def 1.1.3 p.24: a nonempty set of reals bounded above has a least upper bound
  newton_improves            the heart of Example 1.1.4 (p.24): for a rational u > 0 with u*u > 2, the rational
                             (u*u+2)/(2u) is smaller and still has square > 2, so {x in Q : x^2 < 2} has no
                             least rational upper bound
  control_no_rational_sqrt_two
                             Example 1.1.4's other half: no rational has square 2
  bolzano_weierstrass        Thm 2.3.8 p.78: a bounded real sequence has a convergent subsequence
  extreme_value              Thm 3.3.2 p.130: a continuous function on [a,b] attains a maximum and a minimum
  ivt                        Thm 3.3.8 p.133: Bolzano's intermediate value theorem (non-strict form)
  uniform_limit_continuous   Thm 6.2.2 p.235: a uniform limit of continuous functions is continuous

WHAT THESE PROOFS ARE. completeness, bolzano_weierstrass, extreme_value, ivt and uniform_limit_continuous are
short calls to Mathlib's own theorems (Real.exists_isLUB, tendsto_subseq_of_bounded, IsCompact.exists_isMaxOn and
exists_isMinOn, intermediate_value_Icc, TendstoUniformly.continuous). So once this file compiles it would check
that Lebl's statements are true as formal sentences; it would not re-derive his proofs. newton_improves and
control_no_rational_sqrt_two are proved here from field arithmetic and Mathlib's irrationality of the square root
of 2; they are the part that is not a bare library call.

WHAT IT DOES NOT STATE. Metric spaces and compactness in general, the bisection method, Dini's theorem, the
exchange of limit and integral, and the exact examples on the page (those are in ch09-verify.py).
-/

namespace Book18F

theorem completeness (S : Set ℝ) (hne : S.Nonempty) (hbdd : BddAbove S) : ∃ x, IsLUB S x :=
  Real.exists_isLUB hne hbdd

theorem newton_improves (u : ℚ) (hu : 0 < u) (h2 : 2 < u * u) :
    2 < ((u * u + 2) / (2 * u)) ^ 2 ∧ (u * u + 2) / (2 * u) < u := by
  have hu' : u ≠ 0 := ne_of_gt hu
  constructor
  · have h : ((u * u + 2) / (2 * u)) ^ 2 - 2 = (u * u - 2) ^ 2 / (4 * u * u) := by
      field_simp
      ring
    have hpos : 0 < (u * u - 2) ^ 2 / (4 * u * u) :=
      div_pos (pow_pos (by linarith) 2) (by positivity)
    linarith
  · have h : u - (u * u + 2) / (2 * u) = (u * u - 2) / (2 * u) := by
      field_simp
      ring
    have hpos : 0 < (u * u - 2) / (2 * u) := div_pos (by linarith) (by positivity)
    linarith

theorem control_no_rational_sqrt_two : ¬ ∃ q : ℚ, q * q = 2 := by
  rintro ⟨q, hq⟩
  have hq' : ((q : ℝ)) ^ 2 = 2 := by
    have h : ((q * q : ℚ) : ℝ) = 2 := by exact_mod_cast hq
    push_cast at h
    nlinarith [h]
  refine irrational_sqrt_two ⟨|q|, ?_⟩
  rw [Rat.cast_abs, ← Real.sqrt_sq_eq_abs, hq']

theorem bolzano_weierstrass (x : ℕ → ℝ) (B : ℝ) (hB : ∀ n, |x n| ≤ B) :
    ∃ (L : ℝ) (φ : ℕ → ℕ), StrictMono φ ∧ Filter.Tendsto (x ∘ φ) Filter.atTop (nhds L) := by
  obtain ⟨L, _, φ, hφ, h⟩ :=
    tendsto_subseq_of_bounded (Metric.isBounded_Icc (-B) B) (fun n => abs_le.1 (hB n))
  exact ⟨L, φ, hφ, h⟩

theorem extreme_value (f : ℝ → ℝ) {a b : ℝ} (hab : a ≤ b) (hf : ContinuousOn f (Set.Icc a b)) :
    (∃ c ∈ Set.Icc a b, ∀ x ∈ Set.Icc a b, f x ≤ f c) ∧
    (∃ d ∈ Set.Icc a b, ∀ x ∈ Set.Icc a b, f d ≤ f x) := by
  constructor
  · obtain ⟨c, hc, h⟩ := isCompact_Icc.exists_isMaxOn (Set.nonempty_Icc.2 hab) hf
    exact ⟨c, hc, fun x hx => isMaxOn_iff.1 h x hx⟩
  · obtain ⟨d, hd, h⟩ := isCompact_Icc.exists_isMinOn (Set.nonempty_Icc.2 hab) hf
    exact ⟨d, hd, fun x hx => isMinOn_iff.1 h x hx⟩

theorem ivt (f : ℝ → ℝ) {a b y : ℝ} (hab : a ≤ b) (hf : ContinuousOn f (Set.Icc a b))
    (h1 : f a ≤ y) (h2 : y ≤ f b) : ∃ c ∈ Set.Icc a b, f c = y :=
  intermediate_value_Icc hab hf ⟨h1, h2⟩

theorem uniform_limit_continuous (F : ℕ → ℝ → ℝ) (f : ℝ → ℝ) (hF : ∀ n, Continuous (F n))
    (hu : TendstoUniformly F f Filter.atTop) : Continuous f :=
  hu.continuous (Filter.Eventually.of_forall hF)

end Book18F

#print axioms Book18F.completeness
#print axioms Book18F.newton_improves
#print axioms Book18F.control_no_rational_sqrt_two
#print axioms Book18F.bolzano_weierstrass
#print axioms Book18F.extreme_value
#print axioms Book18F.ivt
#print axioms Book18F.uniform_limit_continuous
