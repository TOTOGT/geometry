-- GATE-DECLARE: sorries = none
-- GATE-REASON: Volume I Theorem 5.1 restated as a conditional Banach theorem for the canonical order U ∘ F ∘ K ∘ C, with an explicit iteration bound; the AXLE file's three non-expansiveness justifications refuted.
/-
Orthogenesis/Vol1/ChainContraction.lean — Volume I §5, Theorem 5.1, CONDITIONAL form.

AXLE/lean/ExistenceWellPosedness.lean proves a contraction bound for R ∘ K ∘ F ∘ C on ℝ with a toy
compression and F, K, R ASSUMED non-expansive; its Banach step is a sorry. Its comments say the
assumptions are "discharged" in FoldOperator.lean, ContactStructure.lean and ResamplingKernel.lean;
no file with those names exists in AXLE or geometry (checked 2026-11-08). The reasons it gives are
also false in general (§1):
  * "K is the unique ODE solution, hence non-expansive": ẋ = x has unique solutions and its
    time-(ln 2) flow is x ↦ 2x.
  * "R is the unique Morse arg-min, hence non-expansive": q ↦ (q − 2x)² has the unique,
    nondegenerate minimiser 2x, and x ↦ 2x expands.
  * "a Whitney fold is non-expansive": x ↦ x² folds, and moves 1, 2 to 1, 4.
These refute the implications, not the conditional theorem.

§2 states the conditional theorem for the canonical chain G = U ∘ F ∘ K ∘ C (the AXLE file composes
R ∘ K ∘ F ∘ C, with F and K in the other order): on a nonempty complete metric space, if the four
maps are Lipschitz with constants whose product is below 1, G has a unique fixed point, every orbit
converges to it, and after n steps the distance is at most L^n/(1 − L) · d(x, Gx). That last bound
is the honest replacement for a fixed cycle count such as "33": the count follows from L, the
starting displacement and the tolerance.

Obligations NOT discharged here (each needs its own system): Lipschitz constants for C, K, F, U of
an actual dm³ construction. Sufficient conditions, for the record: a flow whose symmetric Jacobian
part is ≤ ℓI on a convex invariant set is e^{ℓt}-Lipschitz; a minimiser map with D²_qq V ≥ mI and
‖D²_qx V‖ ≤ B is (B/m)-Lipschitz. Neither is proved in this file.
Hand-derived 2026-11-08; written untested.
-/
import Mathlib

namespace Orthogenesis.Vol1

open Filter Topology NNReal

/-! ## §1  The three routes in the AXLE file do not give non-expansiveness -/

/-- x ↦ 2x is the time-(ln 2) flow of ẋ = x and the minimiser map of q ↦ (q − 2x)²; it is not
non-expansive. -/
theorem double_not_nonexpansive : ¬ LipschitzWith 1 (fun x : ℝ => 2 * x) := by
  intro h
  have := h.dist_le_mul 0 1
  norm_num [Real.dist_eq] at this

/-- 2x is the unique minimiser of q ↦ (q − 2x)², with second derivative 2 > 0. -/
theorem double_is_unique_minimiser (x q : ℝ) :
    (2 * x - 2 * x) ^ 2 ≤ (q - 2 * x) ^ 2 ∧ ((q - 2 * x) ^ 2 = 0 → q = 2 * x) := by
  refine ⟨by nlinarith [sq_nonneg (q - 2 * x)], fun h => ?_⟩
  have : q - 2 * x = 0 := pow_eq_zero_iff (two_ne_zero) |>.mp h
  linarith

/-- The fold map x ↦ x² is not non-expansive (1 ↦ 1, 2 ↦ 4). -/
theorem fold_not_nonexpansive : ¬ LipschitzWith 1 (fun x : ℝ => x ^ 2) := by
  intro h
  have := h.dist_le_mul 1 2
  norm_num [Real.dist_eq] at this

/-! ## §2  The conditional theorem for G = U ∘ F ∘ K ∘ C -/

variable {α : Type*} [MetricSpace α] [Nonempty α] [CompleteSpace α]

/-- If C, K, F, U are Lipschitz with constants whose product is below 1, then G = U ∘ F ∘ K ∘ C
is a contraction. -/
theorem chain_contracting {C K F U : α → α} {lC lK lF lU : ℝ≥0}
    (hC : LipschitzWith lC C) (hK : LipschitzWith lK K) (hF : LipschitzWith lF F)
    (hU : LipschitzWith lU U) (hL : lU * (lF * (lK * lC)) < 1) :
    ContractingWith (lU * (lF * (lK * lC))) (U ∘ F ∘ K ∘ C) :=
  ⟨hL, hU.comp (hF.comp (hK.comp hC))⟩

/-- **Theorem 5.1, conditional form.** Unique fixed point, convergence from every start, and an
explicit a-priori bound after n steps. -/
theorem chain_wellPosed {C K F U : α → α} {lC lK lF lU : ℝ≥0}
    (hC : LipschitzWith lC C) (hK : LipschitzWith lK K) (hF : LipschitzWith lF F)
    (hU : LipschitzWith lU U) (hL : lU * (lF * (lK * lC)) < 1) :
    ∃ xs : α, (U ∘ F ∘ K ∘ C) xs = xs ∧
      (∀ y, (U ∘ F ∘ K ∘ C) y = y → y = xs) ∧
      (∀ x, Tendsto (fun n => (U ∘ F ∘ K ∘ C)^[n] x) atTop (𝓝 xs)) ∧
      (∀ x n, dist ((U ∘ F ∘ K ∘ C)^[n] x) xs ≤
        dist x ((U ∘ F ∘ K ∘ C) x) * ((lU * (lF * (lK * lC)) : ℝ≥0) : ℝ) ^ n
          / (1 - ((lU * (lF * (lK * lC)) : ℝ≥0) : ℝ))) := by
  have hf := chain_contracting hC hK hF hU hL
  refine ⟨ContractingWith.fixedPoint _ hf, hf.fixedPoint_isFixedPt,
    fun y hy => hf.fixedPoint_unique hy, fun x => hf.tendsto_iterate_fixedPoint x,
    fun x n => hf.apriori_dist_iterate_fixedPoint_le x n⟩

end Orthogenesis.Vol1

#print axioms Orthogenesis.Vol1.double_not_nonexpansive
#print axioms Orthogenesis.Vol1.fold_not_nonexpansive
#print axioms Orthogenesis.Vol1.chain_contracting
#print axioms Orthogenesis.Vol1.chain_wellPosed
