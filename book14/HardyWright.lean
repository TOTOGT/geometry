/-
  book14/HardyWright.lean — the six-line proof, sentence by sentence.
  Principia Orthogona, Book XIV ch 8. Pablo Nogueira Grossi, G6 LLC, 2026.

  Kahle, "Towards the Structure of Mathematical Proof", quotes the proof from Hardy & Wright
  that Wiedijk (2006) used as the test for seventeen provers:

    "The traditional proof ascribed to Pythagoras runs as follows. If √2 is rational, then the
     equation a² = 2b² is soluble in integers a, b with (a, b) = 1. Hence a² is even, and
     therefore a is even. If a = 2c, then 4c² = 2b², 2c² = b², and b is also even, contrary
     to the hypothesis that (a, b) = 1."

  Wiedijk: "Ideally, a computer should be able to take this text as input and check it for its
  correctness. We clearly are not yet there." Kahle asks for the *structure* of the proof,
  independent of any one prover.

  This file keeps the structure. Every step of the proof below is tagged `-- HW(k)` with the
  sentence of Hardy & Wright it carries out, so book14/ch08-verify.py can check that each
  sentence has at least one step and count what the machine needed per sentence. Stated over
  ℕ, as Hardy & Wright do ("soluble in integers … with (a, b) = 1").
-/
import Mathlib.Data.Nat.Prime.Basic
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Ring

namespace HardyWright

/-- Hardy & Wright, p. 39f: a² = 2b² has no solution with (a, b) = 1. -/
theorem no_coprime_solution (a b : ℕ) (hab : Nat.Coprime a b) (h : a ^ 2 = 2 * b ^ 2) : False := by
  -- HW(1) "the equation a² = 2b² is soluble in integers a, b with (a, b) = 1" : the hypotheses
  -- HW(2) "Hence a² is even"
  have ha2 : 2 ∣ a ^ 2 := ⟨b ^ 2, h⟩
  -- HW(3) "and therefore a is even"
  have ha : 2 ∣ a := Nat.prime_two.dvd_of_dvd_pow ha2
  -- HW(4) "If a = 2c, then 4c² = 2b², 2c² = b²"
  obtain ⟨c, rfl⟩ := ha
  have hc : b ^ 2 = 2 * c ^ 2 := by nlinarith [h]
  -- HW(5) "and b is also even"
  have hb : 2 ∣ b := Nat.prime_two.dvd_of_dvd_pow ⟨c ^ 2, hc⟩
  -- HW(6) "contrary to the hypothesis that (a, b) = 1"
  have h2b : Nat.Coprime 2 b := Nat.Coprime.coprime_dvd_left (dvd_mul_right 2 c) hab
  exact (Nat.Prime.coprime_iff_not_dvd Nat.prime_two).1 h2b hb

end HardyWright

#print axioms HardyWright.no_coprime_solution
