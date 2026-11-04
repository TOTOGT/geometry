import Mathlib

/-
Book XXIV, chapter 4: basis and dimension. Lean core.

STATUS: UNTESTED. Written without a Lean toolchain; not yet compiled by anyone. Until the author
runs it and the output is saved as basisdimension.axioms.txt, nothing in this file counts as
checked. To run:
  lake env lean book24/BasisDimension.lean 2>&1 | tee book24/basisdimension.axioms.txt

The statements follow Lax, Linear Algebra and Its Applications (2nd ed.), Chapter 1, pp.5-11:
  indep_ne_zero                  Exercise 10 (p.5):  an independent family has no zero member
  lemma1                         Lemma 1 (p.5):  n vectors span, j are independent, so j <= n
  single_vector_not_span_plane   an application of lemma1: one vector never spans the rational plane
  control_dependent_family       a control: without independence the conclusion of lemma1 is lost
  lemma2                         Lemma 2 (p.5):  a space with a finite spanning list has a finite basis
  theorem3                       Theorem 3 (p.5):  two finite bases have the same number of vectors
  theorem5a                      Theorem 5(a) (p.6):  a subspace of a finite-dimensional space is
                                 finite dimensional
  theorem5b                      Theorem 5(b) (p.6):  a subspace has a complement: every x splits
                                 uniquely as y + z, and the dimensions add
  theorem6                       Theorem 6 (p.8):  dim Y + dim (X/Y) = dim X
  corollary6                     Corollary 6' (p.9):  a subspace of full dimension is the whole space
  theorem7                       Theorem 7 (p.10):  dim X = dim U + dim V - dim (U cap V) when X = U + V
  exercise12                     Exercise 12 (p.7):  an n-dimensional space is isomorphic to K^n
  exercise18                     Exercise 18 (p.11):  dim of the Cartesian sum is the sum of the dims
  exercise19                     Exercise 19 (p.11):  Y x (X/Y) is isomorphic to X

WHAT THESE PROOFS ARE. lemma1, theorem3 and the uniqueness half of theorem5b are written out here;
the rest are short calls to Mathlib's theorems about Module.finrank, restated so that the sentence
being checked is Lax's. So this file checks that Lax's statements, as formal sentences over any
field K, are true. It does not re-derive his replacement argument for Lemma 1 or his
drop-a-vector argument for Lemma 2: lemma1 is Mathlib's counting lemma for spanning finsets, and
lemma2 builds the basis from Mathlib's finBasis.

WHAT IT DOES NOT STATE.
  - Theorem 4 (an independent list can be completed to a basis): not in this file.
  - Exercise 11 (dimension of a direct sum of m subspaces), and the non-uniqueness half of
    Exercise 12.
  - Exercise 16 (polynomials vanishing at points) and Exercise 17 (the proof of Corollary 6').
  - Linear independence is stated for indexed families (Mathlib's LinearIndependent), where Lax
    speaks of sets of vectors. For lists without repeated entries the two agree.
-/

namespace Book24Basis

variable {K V : Type*} [Field K] [AddCommGroup V] [Module K V]

/-- Exercise 10: a linearly independent family has no zero member. -/
theorem indep_ne_zero {ι : Type*} {y : ι → V} (h : LinearIndependent K y) (i : ι) : y i ≠ 0 :=
  h.ne_zero i

/-- Lemma 1 (exchange): if n vectors span V and j vectors are linearly independent, then j <= n.
Proved here by Mathlib's counting lemma for spanning finsets, not by Lax's replacement argument. -/
theorem lemma1 {n j : ℕ} (x : Fin n → V) (y : Fin j → V)
    (hx : Submodule.span K (Set.range x) = ⊤) (hy : LinearIndependent K y) : j ≤ n := by
  classical
  have h := linearIndependent_le_span_finset y hy (Finset.univ.image x) (by simpa using hx)
  have h2 : (Finset.univ.image x).card ≤ n := by
    simpa using Finset.card_image_le (s := (Finset.univ : Finset (Fin n))) (f := x)
  simp at h
  omega

/-- An application: one vector cannot span the rational plane, because two independent vectors
(the standard basis) exist in it. -/
theorem single_vector_not_span_plane (x : Fin 1 → (Fin 2 → ℚ)) :
    Submodule.span ℚ (Set.range x) ≠ ⊤ := fun hx => by
  have h := lemma1 x (Pi.basisFun ℚ (Fin 2)) hx (Pi.basisFun ℚ (Fin 2)).linearIndependent
  omega

/-- Control: independence is doing real work in Lemma 1. A family of three vectors in the rational
plane, which is spanned by two, exists but is not independent (the zero family). -/
theorem control_dependent_family :
    ∃ y : Fin 3 → (Fin 2 → ℚ), ¬ LinearIndependent ℚ y := by
  refine ⟨fun _ => 0, fun h => ?_⟩
  exact h.ne_zero 0 rfl

/-- Lemma 2: a space with a finite spanning list has a finite basis (indexed by some Fin m). -/
theorem lemma2 {n : ℕ} (x : Fin n → V) (hx : Submodule.span K (Set.range x) = ⊤) :
    ∃ m : ℕ, Nonempty (Module.Basis (Fin m) K V) := by
  classical
  haveI : Module.Finite K V := ⟨⟨Finset.univ.image x, by simpa using hx⟩⟩
  exact ⟨_, ⟨Module.finBasis K V⟩⟩

/-- Theorem 3: two bases of V, indexed by Fin m and Fin n, have m = n. Both directions are
Lemma 1: each basis spans and is independent. -/
theorem theorem3 {m n : ℕ} (b : Module.Basis (Fin m) K V) (c : Module.Basis (Fin n) K V) :
    m = n :=
  le_antisymm (lemma1 c b c.span_eq b.linearIndependent) (lemma1 b c b.span_eq c.linearIndependent)

/-- Theorem 5(a): a subspace of a finite-dimensional space is finite dimensional. -/
theorem theorem5a [FiniteDimensional K V] (Y : Submodule K V) :
    ∃ m : ℕ, Nonempty (Module.Basis (Fin m) K Y) :=
  ⟨_, ⟨Module.finBasis K Y⟩⟩

/-- Theorem 5(b): Y has a complement Z. Every x in V is y + z with y in Y and z in Z for exactly
one pair (y, z), and dim V = dim Y + dim Z. -/
theorem theorem5b [FiniteDimensional K V] (Y : Submodule K V) :
    ∃ Z : Submodule K V,
      (∀ x : V, ∃! p : V × V, p.1 ∈ Y ∧ p.2 ∈ Z ∧ p.1 + p.2 = x) ∧
        Module.finrank K V = Module.finrank K Y + Module.finrank K Z := by
  obtain ⟨Z, hZ⟩ := Submodule.exists_isCompl Y
  refine ⟨Z, ?_, (Submodule.finrank_add_eq_of_isCompl hZ).symm⟩
  intro x
  have hx : x ∈ Y ⊔ Z := by
    rw [hZ.sup_eq_top]
    trivial
  obtain ⟨y, hy, z, hz, hyz⟩ := Submodule.mem_sup.mp hx
  refine ⟨(y, z), ⟨hy, hz, hyz⟩, ?_⟩
  rintro ⟨y', z'⟩ ⟨hy', hz', h'⟩
  simp only at hy' hz' h'
  have e : y - y' = z' - z := by
    have h0 : (y + z) - (y' + z') = 0 := sub_eq_zero.mpr (hyz.trans h'.symm)
    calc y - y' = ((y + z) - (y' + z')) + (z' - z) := by abel
      _ = z' - z := by rw [h0, zero_add]
  have h1 : y - y' ∈ Y := Y.sub_mem hy hy'
  have h2 : y - y' ∈ Z := by
    rw [e]
    exact Z.sub_mem hz' hz
  have h3 : y - y' ∈ Y ⊓ Z := Submodule.mem_inf.mpr ⟨h1, h2⟩
  rw [hZ.inf_eq_bot, Submodule.mem_bot] at h3
  have hyy : y' = y := (sub_eq_zero.mp h3).symm
  have hzz : z' = z := by
    have : z' - z = 0 := by rw [← e]; exact h3
    exact sub_eq_zero.mp this
  rw [hyy, hzz]

/-- Theorem 6: dim Y + dim (V / Y) = dim V. -/
theorem theorem6 [FiniteDimensional K V] (Y : Submodule K V) :
    Module.finrank K Y + Module.finrank K (V ⧸ Y) = Module.finrank K V := by
  have h := Submodule.finrank_quotient_add_finrank Y
  omega

/-- Corollary 6': a subspace whose dimension equals that of V is all of V. -/
theorem corollary6 [FiniteDimensional K V] (Y : Submodule K V)
    (h : Module.finrank K Y = Module.finrank K V) : Y = ⊤ :=
  Submodule.eq_top_of_finrank_eq h

/-- Theorem 7: if V = U + W then dim V + dim (U cap W) = dim U + dim W. The text writes this
as dim V = dim U + dim W - dim (U cap W). -/
theorem theorem7 [FiniteDimensional K V] (U W : Submodule K V) (h : U ⊔ W = ⊤) :
    Module.finrank K V + Module.finrank K ↥(U ⊓ W) =
      Module.finrank K U + Module.finrank K W := by
  have h1 := Submodule.finrank_sup_add_finrank_inf_eq U W
  rw [h, finrank_top] at h1
  exact h1

/-- Exercise 12: a finite-dimensional space of dimension n is isomorphic to K^n. -/
theorem exercise12 [FiniteDimensional K V] {n : ℕ} (h : Module.finrank K V = n) :
    Nonempty (V ≃ₗ[K] (Fin n → K)) := by
  refine ⟨LinearEquiv.ofFinrankEq _ _ ?_⟩
  simp [h]

/-- Exercise 18: the Cartesian sum has dimension the sum of the dimensions. -/
theorem exercise18 {W : Type*} [AddCommGroup W] [Module K W] [FiniteDimensional K V]
    [FiniteDimensional K W] :
    Module.finrank K (V × W) = Module.finrank K V + Module.finrank K W :=
  Module.finrank_prod

/-- Exercise 19: Y x (V / Y) is isomorphic to V. -/
theorem exercise19 [FiniteDimensional K V] (Y : Submodule K V) :
    Nonempty ((Y × (V ⧸ Y)) ≃ₗ[K] V) := by
  refine ⟨LinearEquiv.ofFinrankEq _ _ ?_⟩
  rw [Module.finrank_prod]
  exact theorem6 Y

#print axioms indep_ne_zero
#print axioms lemma1
#print axioms single_vector_not_span_plane
#print axioms control_dependent_family
#print axioms lemma2
#print axioms theorem3
#print axioms theorem5a
#print axioms theorem5b
#print axioms theorem6
#print axioms corollary6
#print axioms theorem7
#print axioms exercise12
#print axioms exercise18
#print axioms exercise19

end Book24Basis
