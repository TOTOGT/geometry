/-
  book14/Brackets.lean — Syntactic Structures, footnote 3 (p. 22), for notation.
  Principia Orthogona, Book XIV ch 1. Pablo Nogueira Grossi, G6 LLC, 2026.

  Chomsky (1957, p. 22, fn 3): "the set of well-formed formulas of any formalized system of
  mathematics or logic will fail to constitute a finite state language, because of paired
  parentheses or equivalent restrictions." On p. 21 he says of the language aⁿbⁿ, (10i),
  "We can easily show" it is not finite state, and does not show it. Pullum (2011, §2)
  argues that SS never proves the corresponding claim for English.

  For brackets the proof is short, and here it is. A finite-state reader is a finite set of
  states σ, a start state, a step function and an accepting test. `no_finite_reader`: no
  such reader accepts exactly the strings of n opening brackets followed by n closing ones,
  i.e. (10i) with a = "(" and b = ")". The proof is the pigeonhole principle: after reading
  0, 1, …, |σ| opening brackets the reader has visited |σ| + 1 states, so two of them are the
  same state, and from then on it cannot tell i open brackets from j.

  SS §3.3 (p. 23) is the other half: cap the nesting at a fixed depth and the language
  becomes finite state again. Book XIV ch 1 measures how deep the corpus's own formulas
  actually nest (book14/ch01-verify.py); that half is a count, not a theorem here.
-/
import Mathlib.Data.Fintype.Pigeonhole

namespace Brackets

/-- A finite-state reader over a two-letter alphabet: `true` = "(", `false` = ")". -/
structure Reader (σ : Type) where
  step : σ → Bool → σ
  start : σ
  accept : σ → Bool

/-- The state reached from `s` after reading `w`. -/
def Reader.run {σ : Type} (M : Reader σ) (s : σ) (w : List Bool) : σ := w.foldl M.step s

/-- n opening brackets followed by m closing ones. -/
def nest (n m : ℕ) : List Bool := List.replicate n true ++ List.replicate m false

theorem run_append {σ : Type} (M : Reader σ) (s : σ) (u v : List Bool) :
    M.run s (u ++ v) = M.run (M.run s u) v := by
  simp [Reader.run, List.foldl_append]

/-- SS p. 21 (10i) and p. 22 fn 3: no finite-state reader accepts exactly the strings
    "(ⁿ )ᵐ" with n = m. -/
theorem no_finite_reader {σ : Type} [Fintype σ] (M : Reader σ) :
    ¬ ∀ n m : ℕ, (M.accept (M.run M.start (nest n m)) = true ↔ n = m) := by
  intro h
  let f : Fin (Fintype.card σ + 1) → σ := fun i => M.run M.start (List.replicate i true)
  obtain ⟨i, j, hij, hf⟩ := Fintype.exists_ne_map_eq_of_card_lt f (by simp)
  have hf' : M.run M.start (List.replicate i true) = M.run M.start (List.replicate j true) := hf
  have key : M.run M.start (nest i i) = M.run M.start (nest j i) := by
    simp only [nest, run_append, hf']
  have h1 := (h i i).2 rfl
  rw [key] at h1
  exact hij (Fin.ext ((h j i).1 h1).symm)

end Brackets

#print axioms Brackets.run_append
#print axioms Brackets.no_finite_reader
