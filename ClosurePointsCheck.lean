/-
  ClosurePointsCheck.lean -- compiled check of closurePoints_stationary (AXLE issue #6)
  2026-10-01.  Lean leanprover/lean4:v4.32.0, Mathlib v4.32.0 (rev 81a5d257c8e4),
  the same pin as the geometry repository.  Zero errors, zero sorry.  Reproduce:
      lake env lean ClosurePointsCheck.lean
  Axioms reported by #print axioms for every theorem below:
      [propext, Classical.choice, Quot.sound]

  What is shown
    1. main_hypothesis_is_false     : `omega < alpha.card.ord` (lean/Main.lean) does not
                                      make the closure points stationary (alpha = omega_1 + omega).
    2. v8_1_hypothesis_is_false     : `alpha.card.ord = alpha` (AXLE_v8_1.lean) does not
                                      either (alpha = omega_omega).
    3. regularity_free_goal_is_false: the goal in the title of #6 (no hypothesis on
                                      cofinality) is false.
    4. closurePoints_stationary_cof : with `aleph0 < alpha.cof` it holds.
  Definitions are copied unchanged from AXLE_v8_1.lean, Part A.
-/
import Mathlib.SetTheory.Ordinal.Basic
import Mathlib.SetTheory.Ordinal.Arithmetic
import Mathlib.SetTheory.Cardinal.Aleph
import Mathlib.Order.Cofinal
import Mathlib.SetTheory.Cardinal.Cofinality.Ordinal
import Mathlib.SetTheory.Cardinal.Arithmetic
import Mathlib.SetTheory.Ordinal.FixedPoint

open Ordinal Cardinal Set

namespace ClosureCheck

-- Definitions copied from AXLE_v8_1.lean (Part A), unchanged.
def IsUnboundedBelow (S : Set Ordinal) (α : Ordinal) : Prop :=
  ∀ β < α, ∃ γ < α, γ ∈ S ∧ β < γ

def IsOmegaClosedBelow (S : Set Ordinal) (α : Ordinal) : Prop :=
  ∀ c : ℕ → Ordinal,
    (∀ n, c n ∈ S) → (∀ n, c n < α) → StrictMono c →
    (⨆ n, c n) ∈ S

def IsClubBelow (S : Set Ordinal) (α : Ordinal) : Prop :=
  IsUnboundedBelow S α ∧ IsOmegaClosedBelow S α

def IsStationaryBelow (S : Set Ordinal) (α : Ordinal) : Prop :=
  ∀ C : Set Ordinal, IsClubBelow C α → ∃ β ∈ C, β ∈ S

def closurePointsBelow (α : Ordinal) : Set Ordinal :=
  { β | β < α ∧ Order.IsSuccLimit β }

/-- Core lemma. If α is the limit of a strictly increasing ω-sequence of
successor ordinals, then the closure points below α are NOT stationary. -/
theorem not_stationary_of_successor_sequence
    (α : Ordinal.{0}) (f : ℕ → Ordinal.{0}) (hf : StrictMono f)
    (hfs : ∀ n, ¬ Order.IsSuccLimit (f n))
    (hlt : ∀ n, f n < α) (hcof : ∀ β < α, ∃ n, β < f n) :
    ¬ IsStationaryBelow (closurePointsBelow α) α := by
  intro hstat
  let C : Set Ordinal := Set.range f ∪ {α}
  have hunb : IsUnboundedBelow C α := by
    intro β hβ
    obtain ⟨n, hn⟩ := hcof β hβ
    exact ⟨f n, hlt n, Or.inl ⟨n, rfl⟩, hn⟩
  have hclosed : IsOmegaClosedBelow C α := by
    intro s hsC hsα hs
    have hsr : ∀ n, ∃ k, f k = s n := by
      intro n
      rcases hsC n with ⟨k, hk⟩ | h
      · exact ⟨k, hk⟩
      · exact absurd (by simpa using h : s n = α) (ne_of_lt (hsα n))
    choose g hg using hsr
    have hgm : StrictMono g := by
      intro m n hmn
      have : f (g m) < f (g n) := by rw [hg m, hg n]; exact hs hmn
      exact hf.lt_iff_lt.mp this
    have hle : ∀ n, f n ≤ s n := by
      intro n
      rw [← hg n]
      exact hf.monotone (hgm.id_le n)
    have hbdd : BddAbove (Set.range s) := (Ordinal.bddAbove_of_small : BddAbove (Set.range s))
    have h1 : α ≤ ⨆ n, s n := by
      by_contra hcon
      push Not at hcon
      obtain ⟨n, hn⟩ := hcof _ hcon
      exact absurd (lt_of_lt_of_le hn ((hle n).trans (le_ciSup hbdd n))) (lt_irrefl _)
    have h2 : (⨆ n, s n) ≤ α := Ordinal.iSup_le (fun n => (hsα n).le)
    exact Or.inr (by simpa using le_antisymm h2 h1)
  obtain ⟨β, hβC, hβS⟩ := hstat C ⟨hunb, hclosed⟩
  rcases hβC with ⟨k, rfl⟩ | h
  · exact hfs k hβS.2
  · have : β = α := by simpa using h
    exact absurd hβS.1 (by rw [this]; exact lt_irrefl _)

/-- A limit ordinal reached by a strictly increasing ω-sequence below it. -/
theorem isSuccLimit_of_sequence
    (α : Ordinal.{0}) (f : ℕ → Ordinal.{0}) (hf : StrictMono f)
    (hlt : ∀ n, f n < α) (hcof : ∀ β < α, ∃ n, β < f n) :
    Order.IsSuccLimit α := by
  refine ⟨?_, ?_⟩
  · intro hmin
    exact (not_lt_of_ge (hmin.eq_bot ▸ bot_le : α ≤ f 0)) (hlt 0) |>.elim
  · intro b hb
    obtain ⟨n, hn⟩ := hcof b hb.lt
    exact hb.2 hn (hlt n)


/-! ### Counterexample 1: `omega < α.card.ord` is not enough (lean/Main.lean).
  α = ω₁ + ω has cardinality ℵ₁ but cofinality ω. -/

theorem main_hypothesis_is_false :
    ∃ α : Ordinal.{0}, Order.IsSuccLimit α ∧ Ordinal.omega0 < α.card.ord ∧
      ¬ IsStationaryBelow (closurePointsBelow α) α := by
  let a : Ordinal.{0} := ω_ 1
  let f : ℕ → Ordinal.{0} := fun n => Order.succ (a + (n : Ordinal))
  have hfm : StrictMono f := by
    intro m n hmn
    have : (m : Ordinal) < n := by exact_mod_cast hmn
    exact Order.succ_lt_succ_iff.mpr ((add_lt_add_iff_left a).mpr this)
  have hlt : ∀ n, f n < a + Ordinal.omega0 := by
    intro n
    have h : a + ((n + 1 : ℕ) : Ordinal) < a + Ordinal.omega0 :=
      (add_lt_add_iff_left a).mpr (Ordinal.natCast_lt_omega0 _)
    have e : f n = a + ((n + 1 : ℕ) : Ordinal) := by
      simp only [f]; rw [Order.succ_eq_add_one, Nat.cast_succ, add_assoc]
    rw [e]; exact h
  have hcof : ∀ β < a + Ordinal.omega0, ∃ n, β < f n := by
    intro β hβ
    obtain ⟨d, hd, hβd⟩ := (Ordinal.lt_add_iff Ordinal.omega0_ne_zero).mp hβ
    obtain ⟨n, rfl⟩ := Ordinal.lt_omega0.mp hd
    exact ⟨n, lt_of_le_of_lt hβd (Order.lt_succ _)⟩
  have hfs : ∀ n, ¬ Order.IsSuccLimit (f n) := fun n => Order.not_isSuccLimit_succ _
  refine ⟨a + Ordinal.omega0, isSuccLimit_of_sequence _ f hfm hlt hcof, ?_,
    not_stationary_of_successor_sequence _ f hfm hfs hlt hcof⟩
  rw [Cardinal.lt_ord]
  have h1 : a ≤ a + Ordinal.omega0 := le_self_add
  have h2 : Ordinal.omega0.card = Cardinal.aleph0 := Ordinal.card_omega0
  have h3 : a.card = Cardinal.aleph 1 := by
    simp only [a]; rw [← Cardinal.ord_aleph, Cardinal.card_ord]
  have h4 : Cardinal.aleph0 < Cardinal.aleph 1 := by simpa using Cardinal.aleph0_lt_aleph_one
  rw [h2]
  exact lt_of_lt_of_le (h3 ▸ h4) (Ordinal.card_le_card h1)


/-! ### Corrected theorem. Hypothesis: uncountable cofinality (as in PrincipiaVol1).
  Stated with the AXLE_v8_1.lean definitions, current Mathlib API. -/

theorem closurePoints_stationary_cof
    (α : Ordinal.{0}) (hlim : Order.IsSuccLimit α)
    (hcf : Cardinal.aleph0 < α.cof) :
    IsStationaryBelow (closurePointsBelow α) α := by
  classical
  intro C ⟨hunb, hclosed⟩
  have hα0 : (0 : Ordinal) < α := hlim.bot_lt
  let nxt : Ordinal → Ordinal := fun β =>
    if h : β < α then Classical.choose (hunb β h) else 0
  have hnxt : ∀ β < α, nxt β < α ∧ nxt β ∈ C ∧ β < nxt β := by
    intro β hβ
    have := Classical.choose_spec (hunb β hβ)
    simp only [nxt, dif_pos hβ]
    exact ⟨this.1, this.2.1, this.2.2⟩
  let c : ℕ → Ordinal := fun n => nxt^[n + 1] 0
  have hcα : ∀ n, nxt^[n] 0 < α := by
    intro n; induction n with
    | zero => simpa using hα0
    | succ k ih => rw [Function.iterate_succ_apply']; exact (hnxt _ ih).1
  have hclt : ∀ n, c n < α := fun n => hcα (n + 1)
  have hcC : ∀ n, c n ∈ C := by
    intro n
    show nxt^[n + 1] 0 ∈ C
    rw [Function.iterate_succ_apply']
    exact (hnxt _ (hcα n)).2.1
  have hcm : StrictMono c := by
    refine strictMono_nat_of_lt_succ (fun n => ?_)
    show nxt^[n + 1] 0 < nxt^[n + 1 + 1] 0
    rw [Function.iterate_succ_apply' nxt (n + 1)]
    exact (hnxt _ (hcα (n + 1))).2.2
  have hsup_lt : (⨆ n, c n) < α := by
    apply Ordinal.iSup_lt_of_lt_cof _ hclt
    simpa using hcf
  have hbdd : BddAbove (Set.range c) := Ordinal.bddAbove_of_small
  have hlimit : Order.IsSuccLimit (⨆ n, c n) := by
    apply isSuccLimit_of_sequence _ c hcm
    · intro n
      exact lt_of_lt_of_le (hcm (Nat.lt_succ_self n)) (le_ciSup hbdd (n + 1))
    · intro β hβ
      exact (Ordinal.lt_iSup_iff.mp hβ)
  exact ⟨⨆ n, c n, hclosed c hcC hclt hcm, hsup_lt, hlimit⟩


/-! ### Counterexample 2: `α.card.ord = α` is not regularity (AXLE_v8_1.lean).
  α = ω_ω is an initial ordinal of cofinality ω. -/

theorem v8_1_hypothesis_is_false :
    ∃ α : Ordinal.{0}, Order.IsSuccLimit α ∧ α.card.ord = α ∧
      ¬ IsStationaryBelow (closurePointsBelow α) α := by
  let α : Ordinal.{0} := ω_ Ordinal.omega0
  let f : ℕ → Ordinal.{0} := fun n => Order.succ (ω_ ((n + 1 : ℕ) : Ordinal))
  have hωlt : ∀ n : ℕ, ω_ ((n + 1 : ℕ) : Ordinal) < α := by
    intro n
    exact Ordinal.omega_lt_omega.mpr (Ordinal.natCast_lt_omega0 _)
  have hflt : ∀ n, f n < α := by
    intro n
    have h1 : ω_ ((n + 1 : ℕ) : Ordinal) < ω_ ((n + 2 : ℕ) : Ordinal) :=
      Ordinal.omega_lt_omega.mpr (by exact_mod_cast Nat.lt_succ_self _)
    have h2 : ω_ ((n + 2 : ℕ) : Ordinal) < α := by
      exact Ordinal.omega_lt_omega.mpr (Ordinal.natCast_lt_omega0 _)
    have h3 : Order.succ (ω_ ((n + 1 : ℕ) : Ordinal)) < ω_ ((n + 2 : ℕ) : Ordinal) :=
      (Cardinal.isSuccLimit_omega _).succ_lt h1
    exact lt_trans h3 h2
  have hfm : StrictMono f := by
    refine strictMono_nat_of_lt_succ (fun n => ?_)
    have h1 : ω_ ((n + 1 : ℕ) : Ordinal) < ω_ ((n + 1 + 1 : ℕ) : Ordinal) :=
      Ordinal.omega_lt_omega.mpr (by exact_mod_cast Nat.lt_succ_self _)
    have h3 : Order.succ (ω_ ((n + 1 : ℕ) : Ordinal)) < ω_ ((n + 1 + 1 : ℕ) : Ordinal) :=
      (Cardinal.isSuccLimit_omega _).succ_lt h1
    exact lt_trans h3 (Order.lt_succ _)
  have hcof : ∀ β < α, ∃ n, β < f n := by
    intro β hβ
    have := (Ordinal.isNormal_omega.lt_iff_exists_lt Ordinal.isSuccLimit_omega0).mp hβ
    obtain ⟨c, hc, hβc⟩ := this
    obtain ⟨k, rfl⟩ := Ordinal.lt_omega0.mp hc
    refine ⟨k, lt_of_lt_of_le hβc ?_⟩
    have : ω_ (k : Ordinal) ≤ ω_ ((k + 1 : ℕ) : Ordinal) :=
      (Ordinal.omega_lt_omega.mpr (by exact_mod_cast Nat.lt_succ_self _)).le
    exact this.trans (Order.le_succ _)
  have hfs : ∀ n, ¬ Order.IsSuccLimit (f n) := fun n => Order.not_isSuccLimit_succ _
  refine ⟨α, isSuccLimit_of_sequence _ f hfm hflt hcof, ?_,
    not_stationary_of_successor_sequence _ f hfm hfs hflt hcof⟩
  simp only [α]
  rw [← Cardinal.ord_aleph, Cardinal.card_ord]

/-- The regularity-free goal of AXLE issue #6 is false. -/
theorem regularity_free_goal_is_false :
    ¬ ∀ α : Ordinal.{0}, Order.IsSuccLimit α → IsStationaryBelow (closurePointsBelow α) α := by
  intro h
  obtain ⟨α, hα, -, hns⟩ := main_hypothesis_is_false
  exact hns (h α hα)

#print axioms not_stationary_of_successor_sequence
#print axioms main_hypothesis_is_false
#print axioms v8_1_hypothesis_is_false
#print axioms regularity_free_goal_is_false
#print axioms closurePoints_stationary_cof

end ClosureCheck
