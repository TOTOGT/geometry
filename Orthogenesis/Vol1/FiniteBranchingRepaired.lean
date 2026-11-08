-- GATE-DECLARE: sorries = none
-- GATE-REASON: Volume I Theorem 5.5 (finite branching): the AXLE statement refuted, a repaired statement proved, and the branch-count bridge made an explicit hypothesis.
/-
Orthogenesis/Vol1/FiniteBranchingRepaired.lean — Volume I §5, Theorem 5.5.

AXLE/lean/FiniteBranching.lean (2026-07-03, three sorries, never in a build target) states:
  U open, [a,b] ⊆ U, g analytic on U, g not identically zero on U  ⟹  g⁻¹{0} ∩ [a,b] finite.
That is false: U need not be connected (§1 below). Its suggested shortcut "countable + compact ⟹
finite" is also false ({0} ∪ {1/n} is countable, compact and infinite); isolation of every point
is what is needed.

§2 proves the repaired statement (U preconnected): an infinite zero set in [a,b] has an
accumulation point there; it lies in U; the identity theorem then forces g ≡ 0 on U.

§3 is the bridge to branches. Finitely many event times give finitely many branches only if each
event has finitely many branches; that is stated as a hypothesis, not assumed silently.

What this does NOT do: connect g to the curvature condition |κ_K| = κ* of Theorem 5.5 on the
Volume I page. That needs the operators defined on a state space (open, see the project ledger).
Hand-derived 2026-11-08; written untested; review by an outside reader the same day.
-/
import Mathlib

namespace Orthogenesis.Vol1

open Set Filter Topology

/-! ## §1  The AXLE statement is false -/

/-- The counterexample function: 0 below 5/2, 1 above. -/
noncomputable def gStep (x : ℝ) : ℝ := if x < 5 / 2 then 0 else 1

/-- The open set with two components. -/
def U2 : Set ℝ := Ioo (-1) 2 ∪ Ioo 3 4

theorem gStep_analyticOnNhds : AnalyticOnNhds ℝ gStep U2 := by
  intro x hx
  rcases hx with h | h
  · refine (analyticAt_const (v := (0 : ℝ))).congr ?_
    filter_upwards [Iio_mem_nhds (show x < 5 / 2 by linarith [h.2])] with y hy
    have hy' : y < 5 / 2 := hy
    simp [gStep, hy']
  · refine (analyticAt_const (v := (1 : ℝ))).congr ?_
    filter_upwards [Ioi_mem_nhds (show (5 : ℝ) / 2 < x by linarith [h.1])] with y hy
    have hy' : ¬ y < 5 / 2 := not_lt.mpr (le_of_lt hy)
    simp [gStep, hy']

/-- The statement in AXLE/lean/FiniteBranching.lean (`finiteBranching`, with a = 0, b = 1) is false. -/
theorem axle_finiteBranching_false :
    ¬ (∀ (U : Set ℝ) (g : ℝ → ℝ), IsOpen U → Icc (0 : ℝ) 1 ⊆ U → AnalyticOn ℝ g U →
        (¬ ∀ x ∈ U, g x = 0) → (g ⁻¹' {0} ∩ Icc (0 : ℝ) 1).Finite) := by
  intro H
  have hopen : IsOpen U2 := isOpen_Ioo.union isOpen_Ioo
  have hsub : Icc (0 : ℝ) 1 ⊆ U2 := fun x hx => Or.inl ⟨by linarith [hx.1], by linarith [hx.2]⟩
  have hne : ¬ ∀ x ∈ U2, gStep x = 0 := by
    intro h
    have h35 := h (7 / 2) (Or.inr ⟨by norm_num, by norm_num⟩)
    norm_num [gStep] at h35
  have hfin := H U2 gStep hopen hsub gStep_analyticOnNhds.analyticOn hne
  have hinf : (gStep ⁻¹' {0} ∩ Icc (0 : ℝ) 1).Infinite := by
    refine (Set.Icc_infinite (by norm_num : (0 : ℝ) < 1)).mono ?_
    intro x hx
    refine ⟨?_, hx⟩
    show gStep x = 0
    have hx' : x < 5 / 2 := by linarith [hx.2]
    simp [gStep, hx']
  exact hinf hfin

/-! ## §2  The repaired statement -/

/-- **Finite zeros (repaired Theorem 5.5 core).** If `U` is preconnected, `[a,b] ⊆ U`, `g` is
analytic on a neighbourhood of every point of `U`, and `g` is not identically zero on `U`, then
`g` has finitely many zeros in `[a,b]`. -/
theorem finite_zeros {U : Set ℝ} {g : ℝ → ℝ} {a b : ℝ}
    (hU : IsPreconnected U) (hab : Icc a b ⊆ U) (hg : AnalyticOnNhds ℝ g U)
    (hne : ∃ x ∈ U, g x ≠ 0) : (g ⁻¹' {0} ∩ Icc a b).Finite := by
  by_contra hinf
  have hinf' : (g ⁻¹' {0} ∩ Icc a b).Infinite := hinf
  obtain ⟨x, hxK, hacc⟩ :=
    hinf'.exists_accPt_of_subset_isCompact isCompact_Icc inter_subset_right
  have hfreq : ∃ᶠ z in 𝓝[≠] x, g z = 0 := by
    rw [accPt_iff_frequently] at hacc
    rw [frequently_nhdsWithin_iff]
    exact hacc.mono fun z hz => ⟨hz.2.1, hz.1⟩
  have h0 := hg.eqOn_zero_of_preconnected_of_frequently_eq_zero hU (hab hxK) hfreq
  obtain ⟨y, hyU, hy⟩ := hne
  exact hy (h0 hyU)

/-- The zeros can be listed: `Fin n ↪ ℝ` onto the zero set. -/
theorem finite_zeros_indexed {U : Set ℝ} {g : ℝ → ℝ} {a b : ℝ}
    (hU : IsPreconnected U) (hab : Icc a b ⊆ U) (hg : AnalyticOnNhds ℝ g U)
    (hne : ∃ x ∈ U, g x ≠ 0) :
    ∃ n : ℕ, ∃ e : Fin n ↪ ℝ, range e = g ⁻¹' {0} ∩ Icc a b :=
  (finite_zeros hU hab hg hne).fin_embedding

/-! ## §3  From event times to branches -/

/-- Finitely many events, each with finitely many branches, give finitely many branches in all.
The second hypothesis is the one Theorem 5.5 needs and does not state. -/
theorem finite_branches {β : Type*} {S : Set ℝ} (B : ℝ → Set β)
    (hS : S.Finite) (hB : ∀ t ∈ S, (B t).Finite) : (⋃ t ∈ S, B t).Finite :=
  hS.biUnion hB

end Orthogenesis.Vol1

#print axioms Orthogenesis.Vol1.axle_finiteBranching_false
#print axioms Orthogenesis.Vol1.finite_zeros
#print axioms Orthogenesis.Vol1.finite_zeros_indexed
#print axioms Orthogenesis.Vol1.finite_branches
