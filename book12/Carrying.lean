/-
Volume XII — chapters 2 and 3. Carrying, and division with its remainder.
Rung 12. Like Counting.lean beside it, this file imports nothing.

Numerals are digit lists, lowest place first ([3, 7, 2] is 273), as in
book11/Bundling.lean.

§1 (chapter 2). Column addition, the way it is done on paper: add the column and
   the incoming carry, write the ones, carry the tens. `addc_correct` proves the
   written answer names the true sum. `carry_small` proves the little one above the
   column is never more than one when two digits are added.
§2 (chapter 3). Division has two answers, not one. The pair (quotient, remainder)
   with the remainder below the divisor is unique (`quot_rem_unique`), so the
   remainder is as much the answer as the quotient.
§3 (chapter 3). Long division's running remainder: carry the remainder down, append
   the next digit, reduce. `remH_correct` proves it ends at the true remainder, for
   any divisor. `nines` proves the old check "cast out nines": a number and the sum
   of its digits leave the same remainder on division by nine.

Toolchain: the repository pin, leanprover/lean4:v4.32.0. No imports.
-/

namespace Book12

/-- The number a digit list names, lowest place first. -/
def val : List Nat → Nat
  | [] => 0
  | d :: ds => d + 10 * val ds

/-! ## §1 · Carrying -/

/-- Column addition with an incoming carry `c`. Missing digits count as zero. -/
def addc : Nat → List Nat → List Nat → List Nat
  | c, [], [] => if c = 0 then [] else [c]
  | c, x :: xs, [] => ((x + c) % 10) :: addc ((x + c) / 10) xs []
  | c, [], y :: ys => ((y + c) % 10) :: addc ((y + c) / 10) [] ys
  | c, x :: xs, y :: ys => ((x + y + c) % 10) :: addc ((x + y + c) / 10) xs ys

/-- The written answer names the true sum. -/
theorem addc_correct : ∀ (c : Nat) (xs ys : List Nat), val (addc c xs ys) = c + val xs + val ys
  | c, [], [] => by
    by_cases h : c = 0
    · simp [addc, val, h]
    · simp [addc, val, h]
  | c, x :: xs, [] => by
    have ih := addc_correct ((x + c) / 10) xs []
    simp only [addc, val] at ih ⊢
    rw [ih]
    omega
  | c, [], y :: ys => by
    have ih := addc_correct ((y + c) / 10) [] ys
    simp only [addc, val] at ih ⊢
    rw [ih]
    omega
  | c, x :: xs, y :: ys => by
    have ih := addc_correct ((x + y + c) / 10) xs ys
    simp only [addc, val] at ih ⊢
    rw [ih]
    omega

/-- The little one above the column: adding two digits and a carry of at most one
    never carries more than one. -/
theorem carry_small (x y c : Nat) (hx : x < 10) (hy : y < 10) (hc : c ≤ 1) :
    (x + y + c) / 10 ≤ 1 := by omega

/-- And the digit written down is always a digit. -/
theorem written_is_digit (x y c : Nat) : (x + y + c) % 10 < 10 := Nat.mod_lt _ (by decide)

-- `addc` is defined by well-founded recursion, so the kernel will not evaluate it
-- by `decide`; the examples are closed through its equation lemmas instead.
example : val (addc 0 [8, 5] [7, 6]) = 58 + 67 := by rw [addc_correct]; simp [val]
example : addc 0 [8, 5] [7, 6] = [5, 2, 1] := by simp [addc]

/-! ## §2 · Division has two answers -/

/-- Quotient and remainder, with the remainder below the divisor, are unique. -/
theorem quot_rem_unique (b q r q' r' : Nat) (hr : r < b) (hr' : r' < b)
    (h : b * q + r = b * q' + r') : q = q' ∧ r = r' := by
  rcases Nat.lt_trichotomy q q' with hlt | heq | hgt
  · exfalso
    have h1 : b * (q + 1) ≤ b * q' := Nat.mul_le_mul_left b hlt
    have h2 : b * (q + 1) = b * q + b := by rw [Nat.mul_add, Nat.mul_one]
    omega
  · subst heq; omega
  · exfalso
    have h1 : b * (q' + 1) ≤ b * q := Nat.mul_le_mul_left b hgt
    have h2 : b * (q' + 1) = b * q' + b := by rw [Nat.mul_add, Nat.mul_one]
    omega

/-- And they exist: the machine's `/` and `%` are that pair. -/
theorem quot_rem_exist (n b : Nat) (hb : 0 < b) : b * (n / b) + n % b = n ∧ n % b < b :=
  ⟨Nat.div_add_mod n b, Nat.mod_lt n hb⟩

/-! ## §3 · Long division's running remainder -/

/-- The number a digit list names, highest place first, as it is written and read. -/
def valH (ds : List Nat) : Nat := ds.foldl (fun acc x => 10 * acc + x) 0

/-- The running remainder of long division by `d`. -/
def remH (d : Nat) (ds : List Nat) : Nat := ds.foldl (fun r x => (10 * r + x) % d) 0

/-- One step: bringing down a digit onto the remainder, or onto the whole number
    so far, leaves the same remainder. -/
theorem rem_step (d a x : Nat) : (10 * (a % d) + x) % d = (10 * a + x) % d := by
  rw [Nat.add_mod, Nat.mul_mod, Nat.mod_mod, ← Nat.mul_mod, ← Nat.add_mod]

theorem remH_gen (d : Nat) : ∀ (ds : List Nat) (a : Nat),
    ds.foldl (fun r x => (10 * r + x) % d) (a % d)
      = (ds.foldl (fun acc x => 10 * acc + x) a) % d
  | [], a => rfl
  | x :: xs, a => by
    simp only [List.foldl]
    rw [rem_step]
    exact remH_gen d xs (10 * a + x)

/-- Long division's running remainder ends at the true remainder, for any divisor. -/
theorem remH_correct (d : Nat) (ds : List Nat) : remH d ds = valH ds % d := by
  have h := remH_gen d ds 0
  rw [Nat.zero_mod] at h
  exact h

/-- The sum of the digits. -/
def dsum : List Nat → Nat
  | [] => 0
  | d :: ds => d + dsum ds

/-- Casting out nines: a number and its digit sum leave the same remainder on
    division by nine. -/
theorem nines : ∀ ds : List Nat, val ds % 9 = dsum ds % 9
  | [] => rfl
  | d :: ds => by
    have ih := nines ds
    simp only [val, dsum]
    omega

example : remH 7 [2, 0, 2, 6] = 2026 % 7 := by decide

end Book12

#print axioms Book12.addc_correct
#print axioms Book12.carry_small
#print axioms Book12.written_is_digit
#print axioms Book12.quot_rem_unique
#print axioms Book12.quot_rem_exist
#print axioms Book12.rem_step
#print axioms Book12.remH_gen
#print axioms Book12.remH_correct
#print axioms Book12.nines
