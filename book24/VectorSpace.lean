import Mathlib

/-
Book XXIV, chapter 3 (planned): fields and vector spaces. Lean core.

STATUS: UNTESTED. Written without a Lean toolchain; not yet compiled by anyone. Until the author
runs it and the output is saved as vectorspace.axioms.txt, nothing in this file counts as checked.
To run:
  lake env lean book24/VectorSpace.lean

The statements follow Lax, Linear Algebra and Its Applications (2nd ed.), Chapter 1:
  zero_unique            Exercise 1 (p.2):  the zero of vector addition is unique
  zero_smul_axioms       equation (10), p.2:  0 x = 0, derived from the axioms
  neg_one_smul_eq_neg    p.3:  (-1) x = -x, derived from the axioms
  inter_isSub            Exercise 7 (p.4):  an intersection of subspaces is a subspace
  sum_isSub              Exercise 6 (p.4):  a sum of subspaces is a subspace
  trivial_isSub          Exercise 8 (p.4):  {0} is a subspace
  cong_refl/symm/trans   Exercise 13 (p.7):  congruence mod Y is an equivalence relation
  cong_add, cong_smul    Exercise 15 (p.8):  the quotient operations do not depend on the
                         chosen representatives
  control_cong_not_trans a control: for Y = {0, 1} in the reals (not a subspace), congruence mod Y
                         is NOT transitive, so closure under addition is doing real work

A subspace is defined here by Lax's own words (contains 0, closed under sums and scalar multiples),
not by Mathlib's Submodule, so the statement can be read against the book. The vector space is
Mathlib's Module K V over a field K; the field is not restricted to the reals or complexes.

What this does NOT state: the quotient space as a type, dimension, or Theorem 6 (dim Y + dim X/Y
= dim X). Those come with chapter 4.
-/

namespace Book24VS

/-- Lax's definition: a subset closed under sums and scalar multiples (and containing 0). -/
structure IsSub (K : Type*) {V : Type*} [Field K] [AddCommGroup V] [Module K V] (S : Set V) :
    Prop where
  zero_mem : (0 : V) ∈ S
  add_mem : ∀ {x y : V}, x ∈ S → y ∈ S → x + y ∈ S
  smul_mem : ∀ (k : K) {x : V}, x ∈ S → k • x ∈ S

/-- Y + Z: all vectors y + z with y in Y, z in Z. -/
def sumSet {V : Type*} [AddCommGroup V] (Y Z : Set V) : Set V :=
  {x | ∃ y ∈ Y, ∃ z ∈ Z, y + z = x}

/-- x is congruent to y modulo Y when x - y lies in Y. -/
def Cong {V : Type*} [AddCommGroup V] (Y : Set V) (x y : V) : Prop := x - y ∈ Y

variable {K V : Type*} [Field K] [AddCommGroup V] [Module K V]

/-- Exercise 1: if z behaves as a zero for addition, then z is 0. -/
theorem zero_unique (z : V) (h : ∀ x : V, x + z = x) : z = 0 := by
  have h0 := h 0
  rwa [zero_add] at h0

/-- Equation (10): 0 x = 0, using only the distributive law and cancellation. -/
theorem zero_smul_axioms (x : V) : (0 : K) • x = 0 := by
  have h : (0 : K) • x + (0 : K) • x = (0 : K) • x + 0 := by
    rw [← add_smul]
    simp
  exact add_left_cancel h

/-- (-1) x = -x, from (1 + (-1)) x = 0 x = 0. -/
theorem neg_one_smul_eq_neg (x : V) : (-1 : K) • x = -x := by
  have h : x + (-1 : K) • x = 0 := by
    calc x + (-1 : K) • x = (1 : K) • x + (-1 : K) • x := by rw [one_smul]
      _ = ((1 : K) + -1) • x := by rw [← add_smul]
      _ = (0 : K) • x := by simp
      _ = 0 := zero_smul_axioms x
  first
    | exact eq_neg_of_add_eq_zero_right h
    | exact (neg_eq_of_add_eq_zero_right h).symm
    | exact eq_neg_iff_add_eq_zero.mpr (by rw [add_comm]; exact h)

theorem inter_isSub {Y Z : Set V} (hY : IsSub K Y) (hZ : IsSub K Z) : IsSub K (Y ∩ Z) :=
  ⟨⟨hY.zero_mem, hZ.zero_mem⟩,
   fun hx hy => ⟨hY.add_mem hx.1 hy.1, hZ.add_mem hx.2 hy.2⟩,
   fun k hx => ⟨hY.smul_mem k hx.1, hZ.smul_mem k hx.2⟩⟩

theorem sum_isSub {Y Z : Set V} (hY : IsSub K Y) (hZ : IsSub K Z) : IsSub K (sumSet Y Z) := by
  refine ⟨⟨0, hY.zero_mem, 0, hZ.zero_mem, add_zero 0⟩, ?_, ?_⟩
  · rintro x x' ⟨y, hy, z, hz, rfl⟩ ⟨y', hy', z', hz', rfl⟩
    exact ⟨y + y', hY.add_mem hy hy', z + z', hZ.add_mem hz hz', by abel⟩
  · rintro k x ⟨y, hy, z, hz, rfl⟩
    exact ⟨k • y, hY.smul_mem k hy, k • z, hZ.smul_mem k hz, (smul_add k y z).symm⟩

theorem trivial_isSub : IsSub K ({0} : Set V) := by
  refine ⟨Set.mem_singleton 0, ?_, ?_⟩
  · intro x y hx hy
    simp only [Set.mem_singleton_iff] at hx hy ⊢
    rw [hx, hy, add_zero]
  · intro k x hx
    simp only [Set.mem_singleton_iff] at hx ⊢
    rw [hx, smul_zero]

theorem cong_refl {Y : Set V} (hY : IsSub K Y) (x : V) : Cong Y x x := by
  unfold Cong
  rw [sub_self]
  exact hY.zero_mem

theorem cong_symm {Y : Set V} (hY : IsSub K Y) {x y : V} (h : Cong Y x y) : Cong Y y x := by
  unfold Cong at *
  have h1 := hY.smul_mem (-1 : K) h
  rwa [neg_one_smul_eq_neg, neg_sub] at h1

theorem cong_trans {Y : Set V} (hY : IsSub K Y) {x y z : V} (h1 : Cong Y x y) (h2 : Cong Y y z) :
    Cong Y x z := by
  unfold Cong at *
  have h3 := hY.add_mem h1 h2
  rwa [sub_add_sub_cancel] at h3

theorem cong_add {Y : Set V} (hY : IsSub K Y) {x₁ x₂ z₁ z₂ : V}
    (hx : Cong Y x₁ x₂) (hz : Cong Y z₁ z₂) : Cong Y (x₁ + z₁) (x₂ + z₂) := by
  unfold Cong at *
  have e : (x₁ + z₁) - (x₂ + z₂) = (x₁ - x₂) + (z₁ - z₂) := by abel
  rw [e]
  exact hY.add_mem hx hz

theorem cong_smul {Y : Set V} (hY : IsSub K Y) (k : K) {x₁ x₂ : V}
    (hx : Cong Y x₁ x₂) : Cong Y (k • x₁) (k • x₂) := by
  unfold Cong at *
  rw [← smul_sub]
  exact hY.smul_mem k hx

/-- Control: {0, 1} is not a subspace of the reals, and congruence modulo it is not transitive
(2 ~ 1 and 1 ~ 0, but 2 - 0 = 2 is not in {0, 1}). -/
theorem control_cong_not_trans :
    ∃ x y z : ℝ, Cong ({0, 1} : Set ℝ) x y ∧ Cong ({0, 1} : Set ℝ) y z ∧
      ¬ Cong ({0, 1} : Set ℝ) x z := by
  refine ⟨2, 1, 0, ?_, ?_, ?_⟩ <;> norm_num [Cong]

#print axioms zero_unique
#print axioms zero_smul_axioms
#print axioms neg_one_smul_eq_neg
#print axioms inter_isSub
#print axioms sum_isSub
#print axioms trivial_isSub
#print axioms cong_refl
#print axioms cong_symm
#print axioms cong_trans
#print axioms cong_add
#print axioms cong_smul
#print axioms control_cong_not_trans

end Book24VS
