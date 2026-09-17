theorem grothendieckAddGroup_nat_equiv_int :
    Nonempty (GrothendieckAddGroup ℕ ≃+ ℤ) := by
  refine ⟨AddEquiv.ofBijective
    (GrothendieckAddGroup.lift (Nat.castAddMonoidHom ℤ)) ⟨?_, ?_⟩⟩
  · rw [injective_iff_map_eq_zero]
    intro x hx
    induction x using AddLocalization.induction_on with
    | H p => simpa [GrothendieckAddGroup.lift_apply, AddLocalization.mk_eq_zero_iff]
               using hx
  · intro n
    obtain ⟨a, b, rfl⟩ : ∃ a b : ℕ, n = (a : ℤ) - b :=
      ⟨n.toNat, (-n).toNat, by omega⟩
    exact ⟨AddLocalization.mk a ⟨b, trivial⟩, by
      simp [GrothendieckAddGroup.lift_apply]⟩
