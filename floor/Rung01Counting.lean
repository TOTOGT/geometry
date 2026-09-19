/-
THE FLOOR · Rung 1 — Counting, and the first thing that goes wrong.

HOW TO READ THIS FILE

Not upward. Each section opens with one general statement — the top of the
slope, already reached, handed to you — and then comes down it in short steps
you can check by hand. The general statement is the hill. The `example`s under
it are what you do on the way down. You are not being asked to climb anything.

A reader who skips to the end of a section finds the payload, because the
payload is put last on purpose.

WHAT THIS FILE NEEDS

Nothing. No imports, no library, no downloads. The Lean toolchain alone:

    lean Rung01Counting.lean

Every line below is checked by the kernel. Where it says `by decide`, the
machine computed it; where it says `by omega`, the machine did the arithmetic
reasoning; where a name appears, that name is a theorem already in Lean's core
and the `#print axioms` block at the foot says what the whole file rests on.

Toolchain: Lean 4.33.0-rc1.
-/

/-! ## 1 · Every number is zero, or one more than another

That sentence is the whole of counting. Everything else on this rung is a
consequence of it, and Lean's `Nat` is *defined* by it: `zero`, and `succ`.
-/

/-- The top of the slope: there is nothing else a natural number can be. -/
theorem zero_or_succ (n : Nat) : n = 0 ∨ ∃ m, n = m + 1 := by
  cases n with
  | zero => exact Or.inl rfl
  | succ m => exact Or.inr ⟨m, rfl⟩

-- Coming down it. Three is three ones.
example : 3 = 0 + 1 + 1 + 1 := by decide
example : (7 : Nat) = 6 + 1 := by decide

/-- The payload of this section: counting never stops, and you can say why in
    one line — whatever number you name, that number plus one is bigger. -/
theorem no_largest (n : Nat) : n < n + 1 := Nat.lt_succ_self n

/-! ## 2 · Order does not matter, and neither does grouping

Two facts a child discovers with blocks and is then never told are theorems.
-/

/-- Top of the slope. -/
theorem add_comm' (a b : Nat) : a + b = b + a := Nat.add_comm a b

-- Down it.
example : 2 + 3 = 3 + 2 := by decide
example : 91 + 8 = 8 + 91 := by decide

/-- Top of the next slope. -/
theorem add_assoc' (a b c : Nat) : (a + b) + c = a + (b + c) := Nat.add_assoc a b c

-- Down it: this is why nobody writes the brackets.
example : (2 + 3) + 4 = 2 + (3 + 4) := by decide

/-- The payload: because both hold, a sum of any list of numbers has one value,
    no matter the order you add them or where you put the brackets. Here it is
    for four numbers, all in one go. -/
theorem sum_of_four (a b c d : Nat) :
    a + b + c + d = d + c + b + a := by omega

/-! ## 3 · Multiplying is adding, and that is why the ten-times table is free -/

/-- Top of the slope: the distributive law. -/
theorem left_distrib' (a b c : Nat) : a * (b + c) = a * b + a * c :=
  Nat.left_distrib a b c

-- Down it. This is not a trick; it is the law above, used once.
example : 7 * 12 = 7 * 10 + 7 * 2 := by decide
example : 7 * 12 = 84 := by decide
example : 23 * 101 = 23 * 100 + 23 := by decide

/-- The payload: any two-digit multiplication splits into a ten-times table and
    a small one. Stated once, for every number. -/
theorem split_at_ten (a t u : Nat) : a * (10 * t + u) = 10 * (a * t) + a * u := by
  rw [Nat.left_distrib, Nat.mul_left_comm]

/-! ## 4 · Place value, said exactly once

"37 means three tens and seven" is a rule taught by example and never stated.
Here it is stated, for every number at once, and it is a theorem of core Lean.
-/

/-- Top of the slope: `Nat.div_add_mod`. -/
theorem place_value (n : Nat) : 10 * (n / 10) + n % 10 = n := Nat.div_add_mod n 10

-- Down it.
example : 10 * (37 / 10) + 37 % 10 = 37 := by decide
example : 37 / 10 = 3 := by decide
example : 37 % 10 = 7 := by decide

/-- The payload: the same sentence works in any base, which is the fact that
    makes place value an idea rather than a habit about the number ten. -/
theorem place_value_base (n b : Nat) : b * (n / b) + n % b = n :=
  Nat.div_add_mod n b

-- Note what is missing from that statement: there is no condition on `b`. It
-- holds for `b = 0` as well, because in Lean `n / 0 = 0` and `n % 0 = n`, so
-- the equation reads `0 + n = n`. Division by zero is not forbidden here; it is
-- given a value, and the value was chosen so that sentences like this one stay
-- true without an exception clause bolted on.
example (n : Nat) : 0 * (n / 0) + n % 0 = n := Nat.div_add_mod n 0

example : 2 * (37 / 2) + 37 % 2 = 37 := by decide   -- binary
example : 60 * (137 / 60) + 137 % 60 = 137 := by decide  -- minutes in 137 minutes

/-! ## 5 · The first thing that goes wrong

Everything above worked. This is where the floor gives way, and it gives way at
a place nobody is warned about: **subtraction is not the opposite of addition.**

It is the opposite of addition only when you are allowed to take the smaller
from the larger. On the counting numbers, that is a condition, not a rule.
-/

/-- Top of the slope, and it is an `if and only if`: taking `b` away and putting
    it back gets you home **exactly when** `b` was no bigger than `a`. -/
theorem sub_add_cancel_iff (a b : Nat) : a - b + b = a ↔ b ≤ a := by
  constructor
  · intro h; omega
  · intro h; omega

-- Down it, on the side where it works.
example : 9 - 4 + 4 = 9 := by decide

-- Down it, on the side where it does not. `3 - 5` is not negative here.
-- It is zero, and the machine says so without complaining.
example : (3 : Nat) - 5 = 0 := by decide
example : (3 : Nat) - 5 + 5 = 5 := by decide

/-- The payload, and the reason the next rung exists: on the counting numbers
    there are pairs you cannot get back from. Five taken from three, then put
    back, leaves you at five, not at three. Nothing is broken and nothing is
    hidden — the counting numbers simply do not contain an answer to "three
    take away five", so the machine returns the nearest one they do contain.

    The integers are not a harder subject. They are the repair for this one
    line, and you have now seen exactly what needed repairing. -/
theorem subtraction_is_not_inverse : ∃ a b : Nat, a - b + b ≠ a :=
  ⟨3, 5, by decide⟩

#print axioms zero_or_succ
#print axioms no_largest
#print axioms add_comm'
#print axioms add_assoc'
#print axioms sum_of_four
#print axioms left_distrib'
#print axioms split_at_ten
#print axioms place_value
#print axioms place_value_base
#print axioms sub_add_cancel_iff
#print axioms subtraction_is_not_inverse
