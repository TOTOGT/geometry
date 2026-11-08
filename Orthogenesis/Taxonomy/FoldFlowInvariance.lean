-- GATE-DECLARE: sorries = none
-- GATE-REASON: a solution of the scalar gradient flow cannot cross an equilibrium: the sign of q - r is preserved, which is the invariance step that passage-time and basin statements need.
/-
Orthogenesis/Taxonomy/FoldFlowInvariance.lean — equilibria are barriers for the fold flow.

UNTESTED. Written 2026-11-08 without a Lean toolchain; lemma names read from the pinned Mathlib
(rev 81a5d257c8, Lean v4.32.0). Imports `FoldFlow.lean`, which compiled on the author's Mac the same day.

Setting (as in FoldFlow.lean): f(q) = q³ − 3q + a, and a solution is any q : ℝ → ℝ with
  hq : ∀ t, 0 ≤ t → HasDerivAt q (−f(q t)) t.
Existence of solutions is not proved.

Hand derivation. If f(r) = 0, then f(q) = (q − r)·g(q), g(q) = q² + q r + r² − 3. So y = q − r obeys
  y' = −g(q(t))·y,
a linear equation whose coefficient is bounded on every [0,T] (q is continuous on a compact set).
Gronwall then gives: a zero of y at ANY time s ∈ [0,T] forces y ≡ 0 on [0,T] —
forwards from s directly, backwards from s by running the same inequality on u ↦ y(s − u).
So y never vanishes unless it vanishes identically, and a continuous function that never vanishes keeps
its sign (intermediate value theorem).

Statement (`equilibrium_invariance`): for every equilibrium r,
  q 0 = r ⇒ q ≡ r;   r < q 0 ⇒ r < q t for all t ≥ 0;   q 0 < r ⇒ q t < r for all t ≥ 0.
`flow_strictly_decreasing_above_fold` (a > 2): the equilibrium qs of FoldFlow.lean is a barrier, f > 0
above it, hence a solution starting above qs is strictly decreasing on [0,∞).

Why this matters. The passage-time lower bound near the fold (target T3) and the basin statement for
a < 2 (target T4) both need "the trajectory stays on one side of an equilibrium for all t ≥ 0".

NOT proved: T3 or T4 themselves; existence of solutions; anything for the PDE or for other systems.
-/
import Mathlib
import Orthogenesis.Taxonomy.FoldFlow

namespace Orthogenesis.Taxonomy.FoldFlow

open Set Filter Topology Real

/-- If `y` obeys `|y'| ≤ L |y|` on `[0,T]` and vanishes at one time `s ∈ [0,T]`, it vanishes on all of
`[0,T]`. Forward from `s` by Mathlib's Gronwall inequality; backward by Gronwall applied to `u ↦ y (s − u)`. -/
theorem zero_propagates {y y' : ℝ → ℝ} {L T s : ℝ}
    (hd : ∀ t ∈ Icc 0 T, HasDerivAt y (y' t) t)
    (hb : ∀ t ∈ Icc 0 T, |y' t| ≤ L * |y t|)
    (hs : s ∈ Icc 0 T) (hz : y s = 0) : ∀ t ∈ Icc 0 T, y t = 0 := by
  intro t ht
  rcases le_total s t with hst | hts
  · have hmemf : ∀ x, x ∈ Icc s t → x ∈ Icc 0 T := fun x hx =>
      ⟨le_trans hs.1 hx.1, le_trans hx.2 ht.2⟩
    have hcon : ContinuousOn y (Icc s t) := fun x hx =>
      (hd x (hmemf x hx)).continuousAt.continuousWithinAt
    have key := norm_le_gronwallBound_of_norm_deriv_right_le
      (f := y) (f' := y') (δ := 0) (K := L) (ε := 0) (a := s) (b := t) hcon
      (fun x hx => (hd x (hmemf x ⟨hx.1, hx.2.le⟩)).hasDerivWithinAt)
      (by simp [hz])
      (fun x hx => by
        have := hb x (hmemf x ⟨hx.1, hx.2.le⟩)
        simpa [Real.norm_eq_abs] using this)
    simpa [Real.norm_eq_abs, gronwallBound_ε0_δ0] using key t ⟨hst, le_rfl⟩
  · have hmem : ∀ u, u ∈ Icc (0 : ℝ) (s - t) → s - u ∈ Icc (0 : ℝ) T := fun u hu =>
      ⟨by linarith [hu.2, ht.1], by linarith [hu.1, hs.2]⟩
    have hder : ∀ u, u ∈ Icc (0 : ℝ) (s - t) →
        HasDerivAt (fun u => y (s - u)) (-(y' (s - u))) u := by
      intro u hu
      have h1 : HasDerivAt (fun u : ℝ => s - u) (-1) u := (hasDerivAt_id' u).const_sub s
      have h2 := (hd (s - u) (hmem u hu)).comp u h1
      exact h2.congr_deriv (by ring)
    have hcon : ContinuousOn (fun u => y (s - u)) (Icc 0 (s - t)) := fun u hu =>
      (hder u hu).continuousAt.continuousWithinAt
    have key := norm_le_gronwallBound_of_norm_deriv_right_le
      (f := fun u => y (s - u)) (f' := fun u => -(y' (s - u))) (δ := 0) (K := L) (ε := 0)
      (a := 0) (b := s - t) hcon
      (fun x hx => (hder x ⟨hx.1, hx.2.le⟩).hasDerivWithinAt)
      (by simp [hz])
      (fun x hx => by
        have := hb (s - x) (hmem x ⟨hx.1, hx.2.le⟩)
        simpa [Real.norm_eq_abs] using this)
    simpa [Real.norm_eq_abs, gronwallBound_ε0_δ0] using key (s - t) ⟨by linarith [hts], le_rfl⟩

/-- A solution that takes the value of an equilibrium at some time `s ≥ 0` equals it at every time ≥ 0. -/
theorem solution_meets_equilibrium {a r : ℝ} (hr : foldF a r = 0) {q : ℝ → ℝ}
    (hq : ∀ t, 0 ≤ t → HasDerivAt q (-(foldF a (q t))) t) {s : ℝ} (hs : 0 ≤ s) (hqs : q s = r) :
    ∀ t, 0 ≤ t → q t = r := by
  intro t ht
  set T : ℝ := max s t with hT
  have hsT : s ∈ Icc 0 T := ⟨hs, le_max_left _ _⟩
  have htT : t ∈ Icc 0 T := ⟨ht, le_max_right _ _⟩
  have hcont : ContinuousOn q (Icc 0 T) := fun x hx =>
    (hq x hx.1).continuousAt.continuousWithinAt
  obtain ⟨B, hB⟩ := isCompact_Icc.exists_bound_of_continuousOn hcont
  set L : ℝ := B ^ 2 + B * |r| + r ^ 2 + 3 with hL
  have hbound : ∀ x ∈ Icc 0 T,
      |-(foldF a (q x))| ≤ L * |q x - r| := by
    intro x hx
    have hBx : |q x| ≤ B := by simpa [Real.norm_eq_abs] using hB x hx
    have hg : |q x ^ 2 + q x * r + r ^ 2 - 3| ≤ L := by
      obtain ⟨hB1, hB2⟩ := abs_le.1 hBx
      have h1 : q x ^ 2 ≤ B ^ 2 := by
        nlinarith [mul_nonneg (sub_nonneg.2 hB2) (show (0 : ℝ) ≤ q x + B by linarith)]
      have h2 : |q x * r| ≤ B * |r| := by
        rw [abs_mul]; exact mul_le_mul_of_nonneg_right hBx (abs_nonneg r)
      apply abs_le.2
      constructor
      · nlinarith [sq_nonneg (q x), sq_nonneg r, sq_nonneg B, neg_abs_le (q x * r), h2]
      · nlinarith [sq_nonneg (q x), sq_nonneg r, le_abs_self (q x * r), h1, h2]
    rw [abs_neg, foldF_factor hr (q x), abs_mul]
    nlinarith [mul_le_mul_of_nonneg_left hg (abs_nonneg (q x - r))]
  have key := zero_propagates (y := fun x => q x - r) (y' := fun x => -(foldF a (q x)))
    (L := L) (T := T) (s := s)
    (fun x hx => (hq x hx.1).sub_const r) hbound hsT (by simp [hqs]) t htT
  have key' : q t - r = 0 := key
  linarith

/-- **Equilibria are barriers.** For any equilibrium `r` of the flow, a solution keeps the strict sign
of `q 0 − r` for all `t ≥ 0`, and a solution that starts at `r` stays at `r`. -/
theorem equilibrium_invariance {a r : ℝ} (hr : foldF a r = 0) {q : ℝ → ℝ}
    (hq : ∀ t, 0 ≤ t → HasDerivAt q (-(foldF a (q t))) t) :
    (q 0 = r → ∀ t, 0 ≤ t → q t = r) ∧
    (r < q 0 → ∀ t, 0 ≤ t → r < q t) ∧
    (q 0 < r → ∀ t, 0 ≤ t → q t < r) := by
  have hcont : ∀ t, 0 ≤ t → ContinuousOn q (Icc 0 t) := fun t _ x hx =>
    (hq x hx.1).continuousAt.continuousWithinAt
  refine ⟨fun h0 => solution_meets_equilibrium hr hq le_rfl h0, ?_, ?_⟩
  · intro h0 t ht
    by_contra hlt
    have hle : q t ≤ r := not_lt.1 hlt
    obtain ⟨s, hs, hsr⟩ := intermediate_value_Icc' ht (hcont t ht)
      (show r ∈ Icc (q t) (q 0) from ⟨hle, h0.le⟩)
    have := solution_meets_equilibrium hr hq hs.1 hsr 0 le_rfl
    linarith
  · intro h0 t ht
    by_contra hlt
    have hle : r ≤ q t := not_lt.1 hlt
    obtain ⟨s, hs, hsr⟩ := intermediate_value_Icc ht (hcont t ht)
      (show r ∈ Icc (q 0) (q t) from ⟨h0.le, hle⟩)
    have := solution_meets_equilibrium hr hq hs.1 hsr 0 le_rfl
    linarith

/-- **Above the fold the flow is strictly decreasing from any start above `qs`.** With `a > 2`, `qs` the
root from `FoldFlow.lean`: the solution stays above `qs` for all `t ≥ 0` (barrier), `f > 0` there, so
`q' < 0` and `q` is strictly decreasing on `[0, ∞)`. This is the monotonicity that the passage-time
bound (T3) uses; T3 itself is not proved here. -/
theorem flow_strictly_decreasing_above_fold {a qs : ℝ} (hqs : qs < -2) (hz : foldF a qs = 0)
    {q : ℝ → ℝ} (hq : ∀ t, 0 ≤ t → HasDerivAt q (-(foldF a (q t))) t) (h0 : qs < q 0) :
    (∀ t, 0 ≤ t → qs < q t) ∧ StrictAntiOn q (Ici 0) := by
  have habove := (equilibrium_invariance hz hq).2.1 h0
  refine ⟨habove, ?_⟩
  have hcont : ContinuousOn q (Ici 0) := fun x hx =>
    (hq x hx).continuousAt.continuousWithinAt
  refine strictAntiOn_of_deriv_neg (convex_Ici 0) hcont ?_
  intro t ht
  rw [interior_Ici] at ht
  have ht0 : 0 ≤ t := le_of_lt ht
  rw [(hq t ht0).deriv]
  have hpos : 0 < foldF a (q t) := by
    rw [foldF_factor hz (q t)]
    exact mul_pos (sub_pos.2 (habove t ht0))
      (lt_of_lt_of_le (rate_pos hqs) (cofactor_lower (q t)))
  linarith

#print axioms Orthogenesis.Taxonomy.FoldFlow.zero_propagates
#print axioms Orthogenesis.Taxonomy.FoldFlow.solution_meets_equilibrium
#print axioms Orthogenesis.Taxonomy.FoldFlow.equilibrium_invariance
#print axioms Orthogenesis.Taxonomy.FoldFlow.flow_strictly_decreasing_above_fold

end Orthogenesis.Taxonomy.FoldFlow
