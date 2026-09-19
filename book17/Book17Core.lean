/-
Book XVII, ch. 1 and index: the elementary rows that need no library.

This file imports nothing.  Everything below is the Lean 4 kernel and its
core arithmetic, so a reader can check it with the toolchain alone:

    lean Book17Core.lean

The rows that need Mathlib -- the real square root, the logarithm, and the
probability row -- are in Book17Mathlib.lean.

Toolchain: Lean 4.33.0-rc1.
-/

/-- Natural subtraction truncates: it does not go negative and it does not
    fail.  `decide` closes it because the statement is a closed decidable
    proposition; `rfl` closes it because the two sides are definitionally
    the same numeral. -/
theorem nat_sub_truncates : (3 : Nat) - 5 = 0 := by decide

example : (3 : Nat) - 5 = 0 := rfl

/-- Division by zero is defined, for every natural. -/
theorem nat_div_zero (x : Nat) : x / 0 = 0 := Nat.div_zero x

/-- And for every integer. -/
theorem int_div_zero (x : Int) : x / 0 = 0 := Int.ediv_zero x

theorem nat_div_zero_inst : (7 : Nat) / 0 = 0 := by decide

theorem int_div_zero_inst : (-7 : Int) / 0 = 0 := by decide

/-- `0 ^ 0` has a value, and the value is 1. -/
theorem nat_zero_pow_zero : (0 : Nat) ^ (0 : Nat) = 1 := by decide

theorem int_zero_pow_zero : (0 : Int) ^ (0 : Nat) = 1 := by decide

/-- Integer division is Euclidean, not truncating-toward-zero.  A reader who
    expects `-7 / 2 = -3` from C or from Python's `int()` gets `-4` here, and
    a remainder that is never negative.  This is the row most likely to be
    read past. -/
theorem int_ediv_neg : (-7 : Int) / 2 = -4 := by decide

theorem int_emod_neg : (-7 : Int) % 2 = 1 := by decide

theorem int_ediv_neg_divisor : (7 : Int) / (-2) = -3 := by decide

theorem int_emod_neg_divisor : (7 : Int) % (-2) = 1 := by decide

/-- The remainder is nonnegative whenever the divisor is not zero -- the
    statement the two instances above are instances of. -/
theorem int_emod_nonneg (a b : Int) (hb : b ≠ 0) : 0 ≤ a % b :=
  Int.emod_nonneg a hb

#print axioms nat_sub_truncates
#print axioms nat_div_zero
#print axioms int_div_zero
#print axioms nat_div_zero_inst
#print axioms int_div_zero_inst
#print axioms nat_zero_pow_zero
#print axioms int_zero_pow_zero
#print axioms int_ediv_neg
#print axioms int_emod_neg
#print axioms int_ediv_neg_divisor
#print axioms int_emod_neg_divisor
#print axioms int_emod_nonneg
