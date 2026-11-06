/-
  pcf/PCFCore.lean -- UNTESTED (written 2026-11-06 without a Lean toolchain; not yet run).

  Source: Dupuy-Levy-Tucker-Wang, "PCF all the way down", arXiv:2611.06106v1.

  WHAT THIS FILE IS. The abstract, set-level skeleton of that paper's dynamics, with no geometry:
  a type `D` stands in for "integral effective divisors", `f : D -> D` for the induced map on them.
    1. branch_iterate          paper Prop 5.3(1):  Branch(f^(m+1)) = U_{i<=m} f^i(Branch f),
                               DERIVED from the tower formula (paper Lemma 5.2) taken as a HYPOTHESIS.
    2. pcf_iff_preperiodic     paper Prop 5.1 (1) <-> (2): PC(f) finite iff every branch divisor
                               is preperiodic (Branch f finite).
    3. pc_subset_of_uniform_bound / pcf_of_uniform_bound
                               the skeleton of paper Thm 7.1: if every Branch(g^m) lies in ONE finite
                               set Sig, and g^n(D) lies in Branch(g^(n+1)), the postcritical set is finite.
  WHAT IT IS NOT. Nothing here touches ramification, normalization, Zariski-Nagata purity or
  Abhyankar's lemma. The tower formula (Lemma 5.2) and the uniform bound (Thm 6.4, with its
  exceptional set Sig) are ASSUMED as hypotheses, not proved. All of the paper's mathematical content
  is in proving those two hypotheses; this file only checks that, once they hold, the dynamical
  bookkeeping goes through. Item 3 in particular is nearly a one-liner for that reason, and its
  name does not claim more than "uniform bound => finite".

  Needs Mathlib (Set.Finite). Run:  cd ~/Desktop/geometry && lake env lean pcf/PCFCore.lean
-/
import Mathlib

namespace PCFCore

variable {D : Type}

/-- Postcritical set: all forward images `f^n d` of divisors `d ∈ B` (paper Def 3.1). -/
def PC (f : D → D) (B : Set D) : Set D := {x | ∃ d ∈ B, ∃ n : ℕ, f^[n] d = x}

/-- Paper Prop 5.3(1), from the tower formula (Lemma 5.2) as a hypothesis. -/
theorem branch_iterate (BR : (D → D) → Set D)
    (tower : ∀ f g : D → D, BR (g ∘ f) = BR g ∪ g '' BR f) (f : D → D) :
    ∀ m : ℕ, BR (f^[m+1]) = {x | ∃ i, i ≤ m ∧ ∃ y ∈ BR f, f^[i] y = x} := by
  intro m
  induction m with
  | zero =>
    rw [show (0:ℕ) + 1 = 1 from rfl, Function.iterate_one]
    ext x
    constructor
    · intro hx
      exact ⟨0, le_refl _, x, hx, rfl⟩
    · rintro ⟨i, hi, y, hy, rfl⟩
      have h0 : i = 0 := Nat.le_zero.mp hi
      subst h0
      simpa using hy
  | succ m ih =>
    rw [Function.iterate_succ' f (m+1), tower, ih]
    ext x
    constructor
    · rintro (hx | ⟨z, ⟨i, hi, y, hy, rfl⟩, rfl⟩)
      · exact ⟨0, Nat.zero_le _, x, hx, rfl⟩
      · exact ⟨i+1, by omega, y, hy, Function.iterate_succ_apply' f i y⟩
    · rintro ⟨i, hi, y, hy, rfl⟩
      rcases i with _ | i
      · left
        simpa using hy
      · right
        exact ⟨f^[i] y, ⟨i, by omega, y, hy, rfl⟩, (Function.iterate_succ_apply' f i y).symm⟩

/-- A finite orbit is preperiodic: two iterates coincide. -/
theorem preperiodic_of_orbit_finite (f : D → D) (d : D)
    (h : {x | ∃ n : ℕ, f^[n] d = x}.Finite) :
    ∃ r s : ℕ, 1 ≤ s ∧ f^[r+s] d = f^[r] d := by
  have hni : ¬ Function.Injective (fun n : ℕ => f^[n] d) := by
    intro hinj
    apply Set.infinite_range_of_injective hinj
    exact h
  unfold Function.Injective at hni
  push_neg at hni
  obtain ⟨m, n, hmn, hne⟩ := hni
  rcases Nat.lt_or_gt_of_ne hne with hlt | hlt
  · exact ⟨m, n - m, by omega, by rw [show m + (n - m) = n by omega]; exact hmn.symm⟩
  · exact ⟨n, m - n, by omega, by rw [show n + (m - n) = m by omega]; exact hmn⟩

/-- A preperiodic point has a finite orbit. -/
theorem orbit_finite_of_preperiodic (f : D → D) (d : D) (r s : ℕ) (hs : 1 ≤ s)
    (h : f^[r+s] d = f^[r] d) : {x | ∃ n : ℕ, f^[n] d = x}.Finite := by
  have key : ∀ n : ℕ, ∃ i, i < r + s ∧ f^[i] d = f^[n] d := by
    intro n
    refine Nat.strong_induction_on n ?_
    intro n ih
    by_cases hn : n < r + s
    · exact ⟨n, hn, rfl⟩
    · push_neg at hn
      obtain ⟨i, hi, hi'⟩ := ih (n - s) (by omega)
      refine ⟨i, hi, ?_⟩
      rw [hi']
      have h1 : f^[n] d = f^[n - (r+s)] (f^[r+s] d) := by
        rw [← Function.iterate_add_apply]
        congr 1
        omega
      have h2 : f^[n - s] d = f^[n - (r+s)] (f^[r] d) := by
        rw [← Function.iterate_add_apply]
        congr 1
        omega
      rw [h2, h1, h]
  refine ((Set.finite_Iio (r+s)).image (fun i => f^[i] d)).subset ?_
  rintro x ⟨n, rfl⟩
  obtain ⟨i, hi, hi'⟩ := key n
  exact ⟨i, hi, hi'⟩

/-- Paper Prop 5.1 (1) <-> (2): PCF iff every branch divisor is preperiodic (Branch finite). -/
theorem pcf_iff_preperiodic (f : D → D) (B : Set D) (hB : B.Finite) :
    (PC f B).Finite ↔ ∀ d ∈ B, ∃ r s : ℕ, 1 ≤ s ∧ f^[r+s] d = f^[r] d := by
  constructor
  · intro h d hd
    apply preperiodic_of_orbit_finite
    refine h.subset ?_
    rintro x ⟨n, rfl⟩
    exact ⟨d, hd, n, rfl⟩
  · intro h
    have hsub : PC f B ⊆ ⋃ d ∈ B, {x | ∃ n : ℕ, f^[n] d = x} := by
      rintro x ⟨d, hd, n, rfl⟩
      simp only [Set.mem_iUnion]
      exact ⟨d, hd, n, rfl⟩
    refine Set.Finite.subset ?_ hsub
    refine hB.biUnion ?_
    intro d hd
    obtain ⟨r, s, hs, e⟩ := h d hd
    exact orbit_finite_of_preperiodic f d r s hs e

/-- Skeleton of paper Thm 7.1. `Br m` models Branch(g^m); `Sig` the uniform exceptional set of
    Thm 6.4. Both hypotheses are ASSUMED here, not proved. -/
theorem pc_subset_of_uniform_bound (g : D → D) (Br : ℕ → Set D) (Sig : Set D)
    (hbr : ∀ d ∈ Br 1, ∀ n : ℕ, g^[n] d ∈ Br (n+1))
    (hbound : ∀ m : ℕ, Br m ⊆ Sig) : PC g (Br 1) ⊆ Sig := by
  rintro x ⟨d, hd, n, rfl⟩
  exact hbound (n+1) (hbr d hd n)

theorem pcf_of_uniform_bound (g : D → D) (Br : ℕ → Set D) (Sig : Set D) (hSig : Sig.Finite)
    (hbr : ∀ d ∈ Br 1, ∀ n : ℕ, g^[n] d ∈ Br (n+1))
    (hbound : ∀ m : ℕ, Br m ⊆ Sig) : (PC g (Br 1)).Finite :=
  hSig.subset (pc_subset_of_uniform_bound g Br Sig hbr hbound)

end PCFCore

#print axioms PCFCore.branch_iterate
#print axioms PCFCore.preperiodic_of_orbit_finite
#print axioms PCFCore.orbit_finite_of_preperiodic
#print axioms PCFCore.pcf_iff_preperiodic
#print axioms PCFCore.pc_subset_of_uniform_bound
#print axioms PCFCore.pcf_of_uniform_bound
