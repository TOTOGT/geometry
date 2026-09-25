-- GATE-DECLARE: sorries = none
-- GATE-REASON: new file 2026-09-25 for the geometry pin (Lean v4.32.0, Mathlib v4.32.0).
-- UNTESTED until the author runs `lake build` on it.
/-
# GenerativeMatrix.lean — Book 3 (Cajueiro edition), Chapter 2 · Generative Matrix (ch2.html)

The chapter models learning as a linear compression map C : W → V from a small
code space W to a surface space V, with Rank(C) = r the learner's compression
depth, and Theorem 2.1: a K event raises Rank(C) from r to r + 1.

  §1  Rank is bounded by the code: Rank(C) ≤ dim W. A rank-33 practitioner needs
      dim W ≥ 33. And if dim W < dim V, C cannot reach every surface form: a
      linear map onto V has rank dim V ≤ dim W. So "dim W ≪ dim V" and "C
      recovers the surface forms" hold together only for a subspace of V.
  §2  §2.1 calls V "a countably infinite set with cardinality ℵ₀" and C a linear
      map into it. A real vector space with a nonzero vector is not countable
      (t ↦ t • v embeds ℝ). V can be a countable set of sentences or a vector
      space, not both; the linear model needs V to be a space that the
      sentences sit inside.
  §3  Theorem 2.1. A K event that adds one pattern is a rank-one update
      C ↦ C + φ ⊗ u. Its rank is at most r + 1; if the new pattern u is already
      in the range of C, the rank does not rise at all; and a rank-one update
      can lower the rank. "From r to r + 1" is the upper bound, reached only
      when u is new (and φ is not cancelled): it is a condition, not a
      consequence of crossing a threshold.

Not formalised: the acquisition ages, the 80%-of-variance figure (no source is
given), the critical-period dynamics, the Legendrian reading of F, the Darboux
remark, and myelination.
-/

import Mathlib

namespace Orthogenesis.GenerativeMatrix

open Module

variable {W V : Type*} [AddCommGroup W] [Module ℝ W] [AddCommGroup V] [Module ℝ V]

/-! ## §1 Rank is bounded by the code space -/

/-- Rank(C) = dim range C ≤ dim W. -/
theorem rank_le_code_dim [FiniteDimensional ℝ W] (C : W →ₗ[ℝ] V) :
    finrank ℝ (LinearMap.range C) ≤ finrank ℝ W :=
  LinearMap.finrank_range_le C

/-- If the code is smaller than the surface, C does not reach every surface form. -/
theorem compression_not_onto [FiniteDimensional ℝ W] [FiniteDimensional ℝ V]
    (C : W →ₗ[ℝ] V) (hdim : finrank ℝ W < finrank ℝ V) : ¬ Function.Surjective C := by
  intro hs
  have h1 := LinearMap.finrank_range_le C
  rw [LinearMap.range_eq_top.mpr hs, finrank_top] at h1
  omega

/-! ## §2 A real vector space is not countable -/

theorem vectorSpace_not_countable {v : V} (hv : v ≠ 0) : ¬ Countable V := by
  intro hV
  have hinj : Function.Injective (fun t : ℝ => t • v) := smul_left_injective ℝ hv
  have : Countable ℝ := hinj.countable
  exact Cardinal.not_countable_real Set.countable_univ

/-! ## §3 Theorem 2.1: a rank-one update -/

/-- A K event adding the pattern u with read-out φ: C ↦ C + φ ⊗ u. -/
def kUpdate (C : W →ₗ[ℝ] V) (φ : W →ₗ[ℝ] ℝ) (u : V) : W →ₗ[ℝ] V :=
  C + φ.smulRight u

theorem kUpdate_range_le (C : W →ₗ[ℝ] V) (φ : W →ₗ[ℝ] ℝ) (u : V) :
    LinearMap.range (kUpdate C φ u) ≤ LinearMap.range C ⊔ Submodule.span ℝ {u} := by
  rintro _ ⟨w, rfl⟩
  simp only [kUpdate, LinearMap.add_apply, LinearMap.smulRight_apply]
  exact Submodule.add_mem_sup ⟨w, rfl⟩ (Submodule.mem_span_singleton.2 ⟨φ w, rfl⟩)

/-- A rank-one update raises the rank by at most one. -/
theorem kUpdate_rank_le [FiniteDimensional ℝ V] (C : W →ₗ[ℝ] V) (φ : W →ₗ[ℝ] ℝ) (u : V) :
    finrank ℝ (LinearMap.range (kUpdate C φ u)) ≤ finrank ℝ (LinearMap.range C) + 1 := by
  have hu : finrank ℝ (Submodule.span ℝ ({u} : Set V)) ≤ 1 :=
    (finrank_span_le_card ({u} : Set V)).trans (by simp)
  calc finrank ℝ (LinearMap.range (kUpdate C φ u))
      ≤ finrank ℝ ↥(LinearMap.range C ⊔ Submodule.span ℝ {u}) :=
        Submodule.finrank_mono (kUpdate_range_le C φ u)
    _ ≤ finrank ℝ (LinearMap.range C) + finrank ℝ (Submodule.span ℝ ({u} : Set V)) :=
        Submodule.finrank_add_le_finrank_add_finrank _ _
    _ ≤ finrank ℝ (LinearMap.range C) + 1 := by omega

/-- If the new pattern is already in the learned surface span, the rank does not rise. -/
theorem kUpdate_no_gain [FiniteDimensional ℝ V] (C : W →ₗ[ℝ] V) (φ : W →ₗ[ℝ] ℝ) {u : V}
    (hu : u ∈ LinearMap.range C) :
    finrank ℝ (LinearMap.range (kUpdate C φ u)) ≤ finrank ℝ (LinearMap.range C) := by
  apply Submodule.finrank_mono
  refine le_trans (kUpdate_range_le C φ u) (sup_le le_rfl ?_)
  rw [Submodule.span_le]
  exact Set.singleton_subset_iff.2 hu

/-- A rank-one update can lower the rank: on ℝ, id + (−id) ⊗ 1 = 0. -/
theorem kUpdate_can_lower :
    finrank ℝ (LinearMap.range (kUpdate (LinearMap.id : ℝ →ₗ[ℝ] ℝ) (-LinearMap.id) 1)) <
      finrank ℝ (LinearMap.range (LinearMap.id : ℝ →ₗ[ℝ] ℝ)) := by
  have h0 : kUpdate (LinearMap.id : ℝ →ₗ[ℝ] ℝ) (-LinearMap.id) 1 = 0 := by
    ext
    simp [kUpdate]
  rw [h0, LinearMap.range_zero, LinearMap.range_id, finrank_bot, finrank_top,
    Module.finrank_self]
  norm_num

end Orthogenesis.GenerativeMatrix

/-! ## Axiom probe -/
#print axioms Orthogenesis.GenerativeMatrix.rank_le_code_dim
#print axioms Orthogenesis.GenerativeMatrix.compression_not_onto
#print axioms Orthogenesis.GenerativeMatrix.vectorSpace_not_countable
#print axioms Orthogenesis.GenerativeMatrix.kUpdate_range_le
#print axioms Orthogenesis.GenerativeMatrix.kUpdate_rank_le
#print axioms Orthogenesis.GenerativeMatrix.kUpdate_no_gain
#print axioms Orthogenesis.GenerativeMatrix.kUpdate_can_lower
