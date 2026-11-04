import Mathlib

/-
Book XXIV: "where two or three are gathered" as a minimum condition for there to be a witness.

STATUS: UNTESTED. Written 2026-11-04 without a Lean toolchain (none could be installed in the session). Nothing here is
verified until `lake env lean book24/Witness.lean 2>&1 | tee book24/witness.axioms.txt` has been run and its real output
read. Likeliest to need a fix: the `decide` calls (size of the search, and the Decidable instance for `Agree`), the name
`not_nontrivial_iff_subsingleton`, and `Fintype.one_lt_card_iff_nontrivial`.

THE MODEL, AND WHY IT IS NOT CIRCULAR. The words of the sources are not formalised and cannot be: Deuteronomy 19:15
("one witness shall not rise up ... at the mouth of two witnesses, or at the mouth of three witnesses, shall the matter be
established"), Matthew 18:16 and 18:20 ("where two or three are gathered together in my name, there am I in the midst of
them"). What is formalised is one reading of the first two: a testimony is a profile of reports, one from each party,
about the same matter, and the only check the parties can run on each other is whether their reports agree.
If "witness" were defined as "at least two parties" the theorem below would be true by definition and say nothing.
Instead `Agree` is defined from the reports alone, and the theorems say when that check CAN FAIL.

  agree_of_subsingleton    with at most one party, every report passes the check: nothing can contradict it
  witness_minimum          the check can fail for some profile  iff  there are at least two parties AND the matter
                           admits at least two different reports. This is the minimum condition: below it, a report
                           is unfalsifiable by its own parties, so it cannot be corroborated or contradicted by them.
  witness_minimum_card     the same, with the party count: for a matter with two possible reports (|alpha| >= 2),
                           the check can fail iff the number of parties is at least 2
  majority_three           with three parties and yes/no reports there is always a strict majority value
  no_majority_two          with two parties who disagree there is none: the disagreement is detected, not located

WHAT THIS DOES NOT SAY. It does not say that agreement makes a report true (agreeing parties can all be wrong or can
collude), that three parties are enough for truth, that the parties are independent, or anything about presence, name,
or the theological content of Matthew 18:20. "Two" is the least number at which a check can fail; "three" is the least
number at which a yes/no dispute has a majority. Those are facts about the check, not about the sources.
-/

namespace Book24Wi

/-- Every party reports a value about the same matter; the reports agree when no two differ. -/
def Agree {ι α : Type*} (r : ι → α) : Prop := ∀ i j, r i = r j

instance {ι α : Type*} [Fintype ι] [DecidableEq α] (r : ι → α) : Decidable (Agree r) := by
  unfold Agree; infer_instance

/-- With at most one party, every report passes the cross-check: the check can never fail. -/
theorem agree_of_subsingleton {ι α : Type*} [Subsingleton ι] (r : ι → α) : Agree r :=
  fun i j => by rw [Subsingleton.elim i j]

/-- With at least two parties and at least two possible reports, some profile fails the check. -/
theorem disagree_possible {ι α : Type*} [Nontrivial ι] [Nontrivial α] :
    ∃ r : ι → α, ¬ Agree r := by
  classical
  obtain ⟨i, j, hij⟩ := exists_pair_ne ι
  obtain ⟨a, b, hab⟩ := exists_pair_ne α
  refine ⟨fun k => if k = i then a else b, fun h => hab ?_⟩
  have := h i j
  simpa [hij.symm] using this

/-- THE MINIMUM CONDITION. The cross-check between the parties can fail for some profile of reports exactly when
there are at least two parties and the matter admits at least two different reports. -/
theorem witness_minimum {ι α : Type*} :
    (∃ r : ι → α, ¬ Agree r) ↔ Nontrivial ι ∧ Nontrivial α := by
  constructor
  · rintro ⟨r, hr⟩
    refine ⟨?_, ?_⟩
    · by_contra h
      rw [not_nontrivial_iff_subsingleton] at h
      haveI : Subsingleton ι := h
      exact hr (agree_of_subsingleton r)
    · by_contra h
      rw [not_nontrivial_iff_subsingleton] at h
      haveI : Subsingleton α := h
      exact hr (fun i j => Subsingleton.elim _ _)
  · rintro ⟨_, _⟩
    exact disagree_possible

/-- The same with a count of parties: for a matter with at least two possible reports, the check can fail
iff there are at least two parties. -/
theorem witness_minimum_card {ι α : Type*} [Fintype ι] [Nontrivial α] :
    (∃ r : ι → α, ¬ Agree r) ↔ 2 ≤ Fintype.card ι := by
  rw [witness_minimum, ← Fintype.one_lt_card_iff_nontrivial]
  constructor
  · rintro ⟨h, _⟩
    omega
  · intro h
    exact ⟨by omega, inferInstance⟩

/-- A value `b` is a strict majority of the reports `r` when more than half of the parties report it. -/
def StrictMajority {ι : Type*} [Fintype ι] [DecidableEq ι] (r : ι → Bool) (b : Bool) : Prop :=
  Fintype.card ι < 2 * (Finset.univ.filter (fun i => r i = b)).card

instance {ι : Type*} [Fintype ι] [DecidableEq ι] (r : ι → Bool) (b : Bool) :
    Decidable (StrictMajority r b) := by
  unfold StrictMajority; infer_instance

/-- Three parties, yes/no reports: some value is always a strict majority. -/
theorem majority_three : ∀ r : Fin 3 → Bool, ∃ b : Bool, StrictMajority r b := by
  decide

/-- Two parties who disagree: neither value is a strict majority. The disagreement is detected but not located. -/
theorem no_majority_two : ∀ r : Fin 2 → Bool, ¬ Agree r → ¬ ∃ b : Bool, StrictMajority r b := by
  decide

end Book24Wi

#print axioms Book24Wi.agree_of_subsingleton
#print axioms Book24Wi.disagree_possible
#print axioms Book24Wi.witness_minimum
#print axioms Book24Wi.witness_minimum_card
#print axioms Book24Wi.majority_three
#print axioms Book24Wi.no_majority_two
