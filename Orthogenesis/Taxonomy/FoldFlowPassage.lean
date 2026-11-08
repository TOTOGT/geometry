-- GATE-DECLARE: sorries = none
-- GATE-REASON: bottleneck delay at the fold: a lower bound on the time the gradient flow needs to pass from the fold point q = 1 to q = 0 when a = 2 + eps, which diverges as eps goes to 0.
/-
Orthogenesis/Taxonomy/FoldFlowPassage.lean — T3, the passage-time lower bound.

Written 2026-11-08 without a Lean toolchain; lemma names read from the pinned Mathlib
(rev 81a5d257c8, Lean v4.32.0). Compiled on the author's Mac the same day with `lake env lean`: no errors,
both #print axioms report only [propext, Classical.choice, Quot.sound]; one `push_neg` deprecation note, replaced
afterwards by `not_le.1` (that edit is not re-run). Imports `FoldFlowInvariance.lean`.

Setting (as in FoldFlow.lean): a = 2 + ε with ε > 0, f(q) = q³ − 3q + a, and a solution is any q with
  hq : ∀ t, 0 ≤ t → HasDerivAt q (−f(q t)) t.

Hand derivation. Put x = q − 1. Then f(q) = x²(x + 3) + ε.
  1. q 0 = 1 > qs (the root of FoldFlow.lean), so `flow_strictly_decreasing_above_fold` gives q t ≤ 1,
     that is x ≤ 0, for all t ≥ 0.
  2. For x ≤ 0: x³ ≤ 0, so f ≤ 3x² + ε.
  3. Let k = √(3/ε), so ε·k² = 3 and k·ε = √(3ε). Put ψ(t) = arctan(k·x(t)) + k·ε·t. Then
       ψ′ = (k(−f) + kε(1 + k²x²)) / (1 + k²x²),
     and the numerator equals k(ε + 3x² − f) ≥ 0. So ψ is monotone on [0,T].
  4. ψ(0) = arctan 0 = 0 and, if q T = 0, ψ(T) = −arctan k + kεT. Hence arctan k ≤ kεT, that is
       T ≥ arctan(√(3/ε)) / √(3ε).
  5. For 0 < ε ≤ 3 we have k ≥ 1, so arctan k ≥ π/4 and T ≥ π/(4√(3ε)), which diverges as ε → 0⁺.

Statement. `passage_time_lower_bound`: any solution with q 0 = 1 and q T = 0 (T ≥ 0) has
T ≥ arctan(√(3/ε))/√(3ε). `passage_time_diverges`: for 0 < ε ≤ 3, T ≥ π/4 / √(3ε).

What this is. A LOWER bound on the time to travel from q = 1 to q = 0 (a particular excursion), the
quantitative content of the delay near the fold. It does not say a solution reaches q = 0 (existence of
the excursion is a hypothesis), it is not an upper bound, and it does not concern a < 2.
-/
import Mathlib
import Orthogenesis.Taxonomy.FoldFlowInvariance

namespace Orthogenesis.Taxonomy.FoldFlow

open Set Filter Topology Real

/-- **T3.** Passage-time lower bound near the fold. -/
theorem passage_time_lower_bound {ε : ℝ} (hε : 0 < ε) {q : ℝ → ℝ}
    (hq : ∀ t, 0 ≤ t → HasDerivAt q (-(foldF (2 + ε) (q t))) t) (h0 : q 0 = 1)
    {T : ℝ} (hT : 0 ≤ T) (hqT : q T = 0) :
    Real.arctan (Real.sqrt (3 / ε)) / Real.sqrt (3 * ε) ≤ T := by
  obtain ⟨qs, hqs, hz⟩ := root_exists (show (2 : ℝ) < 2 + ε by linarith)
  have hgt : qs < q 0 := by rw [h0]; linarith
  obtain ⟨_, hanti⟩ := flow_strictly_decreasing_above_fold hqs hz hq hgt
  have hle1 : ∀ t, 0 ≤ t → q t ≤ 1 := fun t ht => by
    have := hanti.antitoneOn (Set.mem_Ici.2 le_rfl) (Set.mem_Ici.2 ht) ht
    rwa [h0] at this
  set k : ℝ := Real.sqrt (3 / ε) with hk
  have hkpos : 0 < k := Real.sqrt_pos.2 (by positivity)
  have hk2 : k ^ 2 = 3 / ε := Real.sq_sqrt (by positivity)
  have hek : ε * k ^ 2 = 3 := by rw [hk2]; field_simp
  have hm : Real.sqrt (3 * ε) = k * ε := by
    have h3 : 3 * ε = (k * ε) ^ 2 := by
      rw [mul_pow, hk2]; field_simp
    rw [h3]; exact Real.sqrt_sq (mul_pos hkpos hε).le
  set ψ : ℝ → ℝ := fun t => Real.arctan (k * (q t - 1)) + k * ε * t with hψ
  have hψd : ∀ t, 0 ≤ t → HasDerivAt ψ
      (1 / (1 + (k * (q t - 1)) ^ 2) * (k * (-(foldF (2 + ε) (q t)))) + k * ε) t := by
    intro t ht
    have h1 : HasDerivAt (fun s => k * (q s - 1)) (k * (-(foldF (2 + ε) (q t)))) t :=
      ((hq t ht).sub_const 1).const_mul k
    have h2 := h1.arctan
    have h3 : HasDerivAt (fun s : ℝ => k * ε * s) (k * ε) t :=
      ((hasDerivAt_id' t).const_mul (k * ε)).congr_deriv (mul_one _)
    exact h2.add h3
  have hnonneg : ∀ t, 0 ≤ t →
      0 ≤ 1 / (1 + (k * (q t - 1)) ^ 2) * (k * (-(foldF (2 + ε) (q t)))) + k * ε := by
    intro t ht
    set x : ℝ := q t - 1 with hx
    have hxle : x ≤ 0 := by have := hle1 t ht; linarith
    have hf : foldF (2 + ε) (q t) = x ^ 2 * (x + 3) + ε := by
      unfold foldF; rw [hx]; ring
    have hfle : foldF (2 + ε) (q t) ≤ 3 * x ^ 2 + ε := by
      rw [hf]
      nlinarith [mul_nonneg (sq_nonneg x) (show (0 : ℝ) ≤ -x by linarith)]
    have hD : 0 < 1 + (k * x) ^ 2 := by positivity
    have e : 1 / (1 + (k * x) ^ 2) * (k * (-(foldF (2 + ε) (q t)))) + k * ε
        = (k * (-(foldF (2 + ε) (q t))) + k * ε * (1 + (k * x) ^ 2)) / (1 + (k * x) ^ 2) := by
      field_simp
    rw [e]
    apply div_nonneg _ hD.le
    have h4 : k * (-(foldF (2 + ε) (q t))) + k * ε * (1 + (k * x) ^ 2)
        = k * (ε + 3 * x ^ 2 - foldF (2 + ε) (q t)) := by
      linear_combination (k * x ^ 2) * hek
    rw [h4]
    exact mul_nonneg hkpos.le (by linarith)
  have hcont : ContinuousOn ψ (Icc 0 T) := fun t ht =>
    (hψd t ht.1).continuousAt.continuousWithinAt
  have hdiff : DifferentiableOn ℝ ψ (interior (Icc 0 T)) := by
    intro t ht
    rw [interior_Icc] at ht
    exact (hψd t ht.1.le).differentiableAt.differentiableWithinAt
  have hder : ∀ t ∈ interior (Icc (0 : ℝ) T), 0 ≤ deriv ψ t := by
    intro t ht
    rw [interior_Icc] at ht
    rw [(hψd t ht.1.le).deriv]
    exact hnonneg t ht.1.le
  have hmono := monotoneOn_of_deriv_nonneg (convex_Icc 0 T) hcont hdiff hder
  have hle := hmono (show (0 : ℝ) ∈ Icc 0 T from ⟨le_rfl, hT⟩)
    (show T ∈ Icc 0 T from ⟨hT, le_rfl⟩) hT
  have hψ0 : ψ 0 = 0 := by simp [hψ, h0]
  have hψT : ψ T = -Real.arctan k + k * ε * T := by simp [hψ, hqT, Real.arctan_neg]
  rw [hψ0, hψT] at hle
  rw [hm]
  have hpos : 0 < k * ε := mul_pos hkpos hε
  rw [div_le_iff₀ hpos]
  nlinarith [hle]

/-- **T3, divergence.** For `0 < ε ≤ 3` the passage time is at least `π/4 / √(3ε)`, which grows without
bound as `ε → 0⁺`. -/
theorem passage_time_diverges {ε : ℝ} (hε : 0 < ε) (hε3 : ε ≤ 3) {q : ℝ → ℝ}
    (hq : ∀ t, 0 ≤ t → HasDerivAt q (-(foldF (2 + ε) (q t))) t) (h0 : q 0 = 1)
    {T : ℝ} (hT : 0 ≤ T) (hqT : q T = 0) :
    Real.pi / 4 / Real.sqrt (3 * ε) ≤ T := by
  have hmain := passage_time_lower_bound hε hq h0 hT hqT
  have hmpos : 0 < Real.sqrt (3 * ε) := Real.sqrt_pos.2 (by positivity)
  have h31 : 1 ≤ 3 / ε := by rw [le_div_iff₀ hε]; linarith
  have hk1 : 1 ≤ Real.sqrt (3 / ε) := by
    by_contra hlt
    replace hlt := not_le.1 hlt
    have hsq := Real.sq_sqrt (show 0 ≤ 3 / ε by positivity)
    nlinarith [Real.sqrt_nonneg (3 / ε)]
  have hat : Real.arctan 1 ≤ Real.arctan (Real.sqrt (3 / ε)) :=
    Real.arctan_strictMono.monotone hk1
  rw [Real.arctan_one] at hat
  rw [div_le_iff₀ hmpos] at hmain ⊢
  linarith

#print axioms Orthogenesis.Taxonomy.FoldFlow.passage_time_lower_bound
#print axioms Orthogenesis.Taxonomy.FoldFlow.passage_time_diverges

end Orthogenesis.Taxonomy.FoldFlow
