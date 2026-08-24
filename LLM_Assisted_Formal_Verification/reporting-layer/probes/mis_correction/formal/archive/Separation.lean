-- Separation theorem, scoped statement.
theorem separation_theorem (f : Nat -> Nat) (h : StrictMono f) :
    forall a b, a < b -> f a < f b := by
  sorry
