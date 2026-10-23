/-
  NuclearControl.lean   -- UNTESTED. Written without a Lean toolchain (2026-10-22).
  Run:  bash ~/Desktop/geometry/tools/leancheck.sh --audit ~/Downloads/NuclearControl.lean
  Fix errors against what the compiler says, not by guessing.

  WHAT THIS FILE IS FOR
  ---------------------
  The negative-control chapter (ch-togt-strong-interactions) reads the April 2026
  nuclear paper and its Lean companion, grossi-ops/cajueiro/lean/NuclearPhysicsB/.
  Two statements in that companion are checked here, with the companion's
  definitions restated VERBATIM from Operators.lean and FoldEvents.lean
  (the companion is outside geometry, R22, so it cannot be imported):

    1. UnfoldOp.stable_branch  (Operators.lean)
         ∀ x, ∃ n, IsFixedPt (map^[n]) (map x)
       is satisfied by n = 0 for EVERY map, so it carries no content.
       (The same defect was fixed in Theorem53NonCommutativity.lean, which now
       requires n > 0.)   -> `stable_branch_vacuous`

    2. stability_at_threshold  (FoldEvents.lean, currently `sorry`)
         every G-orbit reaches a fixed point within g_threshold = 33 generations.
       It is FALSE as stated: on ℕ, with C = K = U = id and F swapping 0 and 1
       and sending 2 to 0, every hypothesis of the structures holds and the
       orbit of 2 is 2, 0, 1, 0, 1, ... and never reaches a fixed point.
       -> `stability_at_threshold_false`

    3. The weights η^{-k} sum to a partition of unity: η⁻¹ + η⁻² + η⁻³ = 1,
       so the self-similar measure with ratios η⁻¹, η⁻², η⁻³ and mass = length
       is Lebesgue measure on [0,1]. This file proves only the identity.
       -> `trib_inv_sum`

  WHAT IS NOT PROVED HERE
  -----------------------
  That the companion's other structures are consistent, that the paper's physics
  is wrong, or anything about a fractal measure. A counterexample to a Lean
  statement is a statement about that Lean statement.
-/

import Mathlib

namespace NuclearControl

open Set Function

-- ===== restated verbatim from NuclearPhysicsB/Operators.lean =====

structure GenerativeManifold where
  carrier : Type*
  [metric : MetricSpace carrier]
  Phi     : carrier → ℝ
  field   : carrier → carrier

-- DEVIATION from the companion's text: under Lean v4.32.0 the verbatim structure does not
-- elaborate `dist` on `M.carrier` (error: failed to synthesize `Dist M.carrier`, 2026-10-22 run),
-- because an instance-implicit structure field is not a global instance. This line fixes that.
attribute [instance] GenerativeManifold.metric

structure CompressionOp (M : GenerativeManifold) where
  map         : M.carrier → M.carrier
  contractive : ∀ x y, dist (map x) (map y) ≤ dist x y
  injective   : Function.Injective map

structure CurvatureOp (M : GenerativeManifold) where
  map              : M.carrier → M.carrier
  kappa_star       : ℝ
  drives_threshold : ∀ x, M.Phi (map x) ≤ M.Phi x

structure FoldOp (M : GenerativeManifold) where
  map           : M.carrier → M.carrier
  has_fold      : ∃ x y : M.carrier, x ≠ y ∧ map x = map y
  finite_branch : Set.Finite {p : M.carrier | ∃ q, q ≠ p ∧ map q = map p}

structure UnfoldOp (M : GenerativeManifold) where
  map           : M.carrier → M.carrier
  decreases_Phi : ∀ x, M.Phi (map x) ≤ M.Phi x
  stable_branch : ∀ x, ∃ n : ℕ, Function.IsFixedPt (map^[n]) (map x)

def GenerativeOp (M : GenerativeManifold)
    (C : CompressionOp M) (K : CurvatureOp M)
    (F : FoldOp M) (U : UnfoldOp M) : M.carrier → M.carrier :=
  U.map ∘ F.map ∘ K.map ∘ C.map

-- ===== restated from NuclearPhysicsB/TribonacciMeasure.lean and FoldEvents.lean =====

def g_threshold : ℕ := 33

/-- The statement of `stability_at_threshold` in FoldEvents.lean, which ends in `sorry` there. -/
def StabilityAtThreshold : Prop :=
  ∀ (M : GenerativeManifold.{0}) (C : CompressionOp M) (K : CurvatureOp M)
    (F : FoldOp M) (U : UnfoldOp M) (x₀ : M.carrier),
    ∃ g : ℕ, g ≤ g_threshold ∧
      Function.IsFixedPt (GenerativeOp M C K F U) ((GenerativeOp M C K F U)^[g] x₀)

-- ===== 1. stable_branch carries no content =====

/-- For ANY map `f`, `n = 0` witnesses the shape of `UnfoldOp.stable_branch`. -/
theorem stable_branch_vacuous {α : Type*} (f : α → α) :
    ∀ x, ∃ n : ℕ, Function.IsFixedPt (f^[n]) (f x) :=
  fun _ => ⟨0, rfl⟩

-- ===== 2. stability_at_threshold is false as stated =====

/-- Swap 0 and 1; send 2 to 0; fix everything else. -/
def Fmap : ℕ → ℕ := fun n => if n = 0 then 1 else if n = 1 then 0 else if n = 2 then 0 else n

lemma Fmap_mem : ∀ n, n ≤ 2 → Fmap n ≤ 2 := by
  intro n hn
  interval_cases n <;> simp [Fmap]

lemma Fmap_ne : ∀ n, n ≤ 2 → Fmap n ≠ n := by
  intro n hn
  interval_cases n <;> simp [Fmap]

lemma iter_mem (g : ℕ) : Fmap^[g] 2 ≤ 2 := by
  induction g with
  | zero => simp
  | succ g ih =>
    rw [Function.iterate_succ_apply']
    exact Fmap_mem _ ih

abbrev Mℕ : GenerativeManifold.{0} :=
  GenerativeManifold.mk ℕ (fun n : ℕ => (n : ℝ)) id

def Cid : CompressionOp Mℕ where
  map := id
  contractive := fun _ _ => le_rfl
  injective := Function.injective_id

def Kid : CurvatureOp Mℕ where
  map := id
  kappa_star := 0
  drives_threshold := fun _ => le_rfl

def Uid : UnfoldOp Mℕ where
  map := id
  decreases_Phi := fun _ => le_rfl
  stable_branch := fun _ => ⟨0, rfl⟩

/-- Stated on plain ℕ so `omega` sees the types (it cannot see through `Mℕ.carrier`). -/
lemma Fmap_branch : ∀ p q : ℕ, q ≠ p → Fmap q = Fmap p → p = 1 ∨ p = 2 := by
  intro p q hq h
  unfold Fmap at h
  split_ifs at h <;> omega

def Ffold : FoldOp Mℕ where
  map := Fmap
  has_fold := ⟨(1 : ℕ), (2 : ℕ), by show (1 : ℕ) ≠ 2; decide, by show Fmap 1 = Fmap 2; simp [Fmap]⟩
  finite_branch := by
    apply Set.Finite.subset (Set.toFinite ({1, 2} : Set ℕ))
    intro p hp
    obtain ⟨q, hq, h⟩ := hp
    rcases Fmap_branch p q hq h with e | e <;> simp [e]

theorem stability_at_threshold_false : ¬ StabilityAtThreshold := by
  intro h
  unfold StabilityAtThreshold at h
  obtain ⟨g, -, hg⟩ := h Mℕ Cid Kid Ffold Uid (2 : ℕ)
  have hG : GenerativeOp Mℕ Cid Kid Ffold Uid = Fmap := rfl
  rw [hG] at hg
  exact Fmap_ne _ (iter_mem g) hg

-- ===== 3. the weights eta^-k partition unity =====

theorem trib_inv_sum {η : ℝ} (h : 1 < η ∧ η ^ 3 = η ^ 2 + η + 1) :
    η⁻¹ + (η⁻¹) ^ 2 + (η⁻¹) ^ 3 = 1 := by
  have h0 : η ≠ 0 := by
    have : 0 < η := by linarith [h.1]
    exact this.ne'
  have e : η⁻¹ + (η⁻¹) ^ 2 + (η⁻¹) ^ 3 = (η ^ 2 + η + 1) / η ^ 3 := by
    field_simp
  rw [e, ← h.2]
  field_simp

#print axioms stable_branch_vacuous
#print axioms stability_at_threshold_false
#print axioms trib_inv_sum

end NuclearControl
