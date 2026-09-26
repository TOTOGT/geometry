-- GATE-DECLARE: sorries = none
-- GATE-REASON: new file 2026-09-25 for the geometry pin (Lean v4.32.0, Mathlib v4.32.0).
-- UNTESTED until the author runs `lake build` on it.
/-
# CajueiroPrinciple.lean — Book 3 (Cajueiro edition), Ch 1 · The Cajueiro Principle
# (ch1.html, off the taught-path roster)

Theorem 1.1 asks, for any system, for a compression map C : W → V with
(i) dim W < dim V, (ii) C surjective onto the observed outputs V_obs,
(iii) C not injective, (iv) recovery of W needing Rank(C) K-crossings.
Read with C linear (as chapter 2 does):

  §1  As an existence claim it is vacuous: for any W with a nonzero vector,
      C = 0 is non-injective and reaches the observed set {0}. With V_obs left
      unconstrained, (ii) and (iii) hold for every system — the statement
      needs V_obs to be the outputs actually observed and to be large.
  §2  If V_obs is all of V, (i) and (ii) cannot both hold: a linear map onto V
      needs dim W ≥ dim V (GenerativeMatrix.compression_not_onto).
  §3  (iii) does not follow from (i): x ↦ (x, 0) from ℝ to ℝ² has dim W < dim V
      and is injective. Non-injectivity is a separate assumption about C.

(iv) is not a mathematical statement until "K-crossing" and "recovery" are
defined; it is not formalised.

  §4  The original chapter (Ponto de Entrada, Ch 1 §1.5) has no Theorem 1.1; its
      mathematics is g⁶ = 33 via n_min = ⌈log₂(3!)·4⌉ = 11 and 3 × 11 = 33. The
      arithmetic is right (2¹⁰ < 6⁴ ≤ 2¹¹ puts log₂6·4 in (10, 11]). The factors
      log₂(3!), 4 and 3 are the chapter's stated assumptions — it calls the
      derivation "a reconstruction path" — and are not derived here.
-/

import Orthogenesis.Matrix.GenerativeMatrix

namespace Orthogenesis.CajueiroPrinciple

/-! ## §1 The existence claim is met by C = 0 -/

theorem theorem11_vacuous {W V : Type*} [AddCommGroup W] [Module ℝ W]
    [AddCommGroup V] [Module ℝ V] {w : W} (hw : w ≠ 0) :
    ∃ C : W →ₗ[ℝ] V, ({0} : Set V) ⊆ Set.range C ∧ ¬ Function.Injective C := by
  refine ⟨0, ?_, ?_⟩
  · intro v hv
    rw [Set.mem_singleton_iff] at hv
    exact ⟨0, by simp [hv]⟩
  · intro h
    apply hw
    apply h
    simp

/-! ## §2 Onto all of V is impossible when dim W < dim V -/

theorem theorem11_onto_V_impossible {W V : Type*} [AddCommGroup W] [Module ℝ W]
    [FiniteDimensional ℝ W] [AddCommGroup V] [Module ℝ V] [FiniteDimensional ℝ V]
    (C : W →ₗ[ℝ] V) (hdim : Module.finrank ℝ W < Module.finrank ℝ V) :
    ¬ Function.Surjective C :=
  Orthogenesis.GenerativeMatrix.compression_not_onto C hdim

/-! ## §3 A smaller code space can still map injectively -/

theorem small_code_injective :
    Module.finrank ℝ ℝ < Module.finrank ℝ (ℝ × ℝ) ∧
      Function.Injective (LinearMap.inl ℝ ℝ ℝ) := by
  refine ⟨?_, LinearMap.inl_injective⟩
  rw [Module.finrank_self, Module.finrank_prod, Module.finrank_self]
  norm_num

/-! ## §4 The original chapter's arithmetic -/

theorem nmin_eq_eleven : ⌈Real.logb 2 6 * 4⌉₊ = 11 := by
  have h2 : 0 < Real.log 2 := Real.log_pos (by norm_num)
  have hA : 10 * Real.log 2 < 4 * Real.log 6 := by
    have := Real.log_lt_log (by norm_num : (0 : ℝ) < 2 ^ 10) (by norm_num : (2 : ℝ) ^ 10 < 6 ^ 4)
    rw [Real.log_pow, Real.log_pow] at this
    push_cast at this
    linarith
  have hB : 4 * Real.log 6 ≤ 11 * Real.log 2 := by
    have := Real.log_le_log (by norm_num : (0 : ℝ) < 6 ^ 4) (by norm_num : (6 : ℝ) ^ 4 ≤ 2 ^ 11)
    rw [Real.log_pow, Real.log_pow] at this
    push_cast at this
    linarith
  rw [Nat.ceil_eq_iff (by norm_num)]
  unfold Real.logb
  constructor
  · rw [show ((11 - 1 : ℕ) : ℝ) = 10 by norm_num, div_mul_eq_mul_div, lt_div_iff₀ h2]
    linarith
  · rw [div_mul_eq_mul_div, div_le_iff₀ h2]
    push_cast
    linarith

theorem g6_eq : 3 * 11 = 33 := rfl

end Orthogenesis.CajueiroPrinciple

/-! ## Axiom probe -/
#print axioms Orthogenesis.CajueiroPrinciple.theorem11_vacuous
#print axioms Orthogenesis.CajueiroPrinciple.theorem11_onto_V_impossible
#print axioms Orthogenesis.CajueiroPrinciple.small_code_injective
#print axioms Orthogenesis.CajueiroPrinciple.nmin_eq_eleven
#print axioms Orthogenesis.CajueiroPrinciple.g6_eq
