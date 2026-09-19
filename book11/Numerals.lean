/-
Volume XI — rung 11.

WHAT THIS FILE IS, AND WHAT IT IS NOT

It is not the floor. It is the certificate that the floor is sound.

An adult meeting written numbers for the first time does not read Lean, and no
amount of gentle wording changes that. The mistake this file replaces was
exactly that mistake: an earlier draft wrote the same facts using lists, type
variables and `zip`, which is elementary *content* dressed in college
*notation*. Lowering the content is not lowering the floor.

So the split is stated here rather than blurred:

  - The learner works with marks, stones, rows and the numerals themselves.
  - The teacher needs to know the rules being taught are the true ones, with
    no exception waiting further along to embarrass them.
  - This file is for the second reader. Everything in it is about counting
    numbers and nothing else — no sets, no lists, no letters standing for
    types, no notation that is not `+`, `-`, `×`, `<` and `=`.

If a statement here cannot be demonstrated on a table with stones, it does not
belong on this rung, and the comment under it says how to do the demonstration.

WHAT IT NEEDS

Nothing. No library, no download:

    lean Numerals.lean

Toolchain: Lean 4.33.0-rc1.
-/

/-! ## 1 · Same size, decided without counting

Two rows are the same size when they pair off and nobody is left standing.
You do not have to know how many there are.

On the table: a row of stones, a row of cups, one stone to a cup.
-/

/-- Neither row is longer than the other — that is all "the same size" says. -/
theorem same_size (n m : Nat) : n = m ↔ (n ≤ m ∧ m ≤ n) := by omega

/-- If the first row is longer, something is left standing on its side, and the
    number left standing is the difference.

    On the table: pair them off, then count only what is left over. -/
theorem left_over (n m : Nat) (h : m < n) : 0 < n - m := by omega

/-- The payload: pairing off and counting never disagree. Whatever the two rows
    are, exactly one of three things is true — the first is longer, the second
    is longer, or they match. There is no fourth case and no undecided case. -/
theorem one_of_three (n m : Nat) : m < n ∨ n < m ∨ n = m := by omega

/-! ## 2 · A numeral is a name for how many

The marks `III` and the numeral `3` name the same row. One is shorter to write.
-/

/-- Adding one mark makes the name go up by one, every time, forever. That is
    the whole of counting.

    On the table: lay down one more stone, say the next word. -/
theorem one_more (n : Nat) : n < n + 1 := Nat.lt_succ_self n

/-- The payload of this section: there is a name for having none. Most number
    systems in history did not have one, and everything after this rung needs
    it.

    On the table: the empty space in front of you is a number of stones. -/
theorem none_is_a_number : 0 + 0 = 0 := rfl

example : 0 < 1 := by decide
example : 5 < 6 := by decide

/-! ## 3 · Where a digit sits is part of its name

`12` and `21` are written with the same two marks and are not the same number.
Nothing in the marks says so. The *place* says so.

On the table: two heaps, one of ten-bundles and one of loose stones. Swap which
heap is which and count again.
-/

/-- Reading a two-digit numeral: so many tens, and so many ones. -/
theorem reading (t u : Nat) : 10 * t + u = 10 * t + u := rfl

example : 10 * 1 + 2 = 12 := by decide
example : 10 * 2 + 1 = 21 := by decide
example : (12 : Nat) ≠ 21 := by decide

/-- The payload, and the reason the whole system can be trusted: two different
    two-digit numerals never name the same number. If `ab` and `cd` come out
    equal, then `a` is `c` and `b` is `d`.

    This is not obvious and it is not free. It holds because every digit is
    smaller than ten. A system that allowed a digit of ten would break it — and
    a learner who has been shown the break understands place value, while one
    who has only been shown examples has memorised a habit. -/
theorem no_two_numerals_collide (a b c d : Nat)
    (hb : b < 10) (hd : d < 10)
    (h : 10 * a + b = 10 * c + d) : a = c ∧ b = d := by
  omega

-- Worth noticing what is NOT in that statement. There is no condition on `a`
-- or `c`, the tens digits. Only the ones digits have to stay below ten. A
-- first draft assumed all four were needed; the machine accepted the proof
-- without two of them, which is how the missing idea was found: a digit has to
-- be small enough only at the place where it competes with the next bundle up.
-- "27 tens and 3" is a perfectly unambiguous name for 273.
example : 10 * 27 + 3 = 273 := by decide

/-- Here is the break, stated as a theorem rather than a warning. Allow a digit
    to reach ten and two different numerals name one number: "one ten and ten
    ones" and "two tens and none" are both twenty.

    On the table: this is why you bundle at ten and not at eleven. -/
theorem the_break : 10 * 1 + 10 = 10 * 2 + 0 := by decide

/-- And it is not about ten. Bundling works in any size, so long as no digit
    reaches the size you bundle at. Ten is a fact about hands. This is the fact
    underneath it. -/
theorem no_collision_in_any_base (base a b c d : Nat)
    (hb : b < base) (hd : d < base)
    (h : base * a + b = base * c + d) : a = c ∧ b = d := by
  rcases Nat.lt_trichotomy a c with hlt | heq | hgt
  · exfalso
    have h1 : base * (a + 1) ≤ base * c := Nat.mul_le_mul_left base hlt
    have h2 : base * (a + 1) = base * a + base := by
      rw [Nat.mul_add, Nat.mul_one]
    omega
  · subst heq; omega
  · exfalso
    have h1 : base * (c + 1) ≤ base * a := Nat.mul_le_mul_left base hgt
    have h2 : base * (c + 1) = base * c + base := by
      rw [Nat.mul_add, Nat.mul_one]
    omega

#print axioms same_size
#print axioms left_over
#print axioms one_of_three
#print axioms one_more
#print axioms none_is_a_number
#print axioms reading
#print axioms no_two_numerals_collide
#print axioms the_break
#print axioms no_collision_in_any_base
