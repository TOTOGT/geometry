/-
Volume XI — chapters 2 and 3. Bundling at any size, and what the digit zero is for.
Rung 11. Like Numerals.lean beside it, this file imports nothing: it checks with the
bare `lean` binary and cannot drift with a library bump.

A numeral is a list of digits. Written here lowest place first, so [3, 7, 2] is 273:

    val b [d₀, d₁, d₂, …] = d₀ + b·(d₁ + b·(d₂ + …))

§1 (chapter 2). In any base b, two digit lists OF THE SAME LENGTH with every digit
   below b name the same number only if they are the same list. Ten is not special.
§2 (chapter 3). Without the same-length condition this fails, and zero is why: a
   zero on the high end changes nothing, so [3] and [3, 0] both name 3.
§3 (chapter 3). The standard digit is a remainder: the lowest digit of a numeral is
   what is left when you divide by the base. Zero is the name for "nothing left over".
§4 (chapter 3). And zero is not needed for unambiguous names. With digits 1 … b and
   no zero ("bijective" numeration) every number has at most one name, at any length.
   What zero buys is §3, not uniqueness.

Toolchain: the repository pin, leanprover/lean4:v4.32.0. No imports.
-/

namespace Book11

/-- The number a digit list names, lowest place first. -/
def val (b : Nat) : List Nat → Nat
  | [] => 0
  | d :: ds => d + b * val b ds

/-- Numerals.lean's `no_collision_in_any_base`, restated in the order `val` uses. -/
theorem split (b d d' x x' : Nat) (hd : d < b) (hd' : d' < b)
    (h : d + b * x = d' + b * x') : d = d' ∧ x = x' := by
  rcases Nat.lt_trichotomy x x' with hlt | heq | hgt
  · exfalso
    have h1 : b * (x + 1) ≤ b * x' := Nat.mul_le_mul_left b hlt
    have h2 : b * (x + 1) = b * x + b := by rw [Nat.mul_add, Nat.mul_one]
    omega
  · subst heq; omega
  · exfalso
    have h1 : b * (x' + 1) ≤ b * x := Nat.mul_le_mul_left b hgt
    have h2 : b * (x' + 1) = b * x' + b := by rw [Nat.mul_add, Nat.mul_one]
    omega

/-! ## §1 · Chapter 2: bundling works at any size -/

/-- Same length, every digit below the base: equal values force equal numerals. -/
theorem unique_same_length (b : Nat) :
    ∀ (ds es : List Nat), ds.length = es.length →
      (∀ d ∈ ds, d < b) → (∀ e ∈ es, e < b) → val b ds = val b es → ds = es
  | [], [], _, _, _, _ => rfl
  | [], _ :: _, hl, _, _, _ => by simp at hl
  | _ :: _, [], hl, _, _, _ => by simp at hl
  | d :: ds, e :: es, hl, hds, hes, hv => by
    simp only [val] at hv
    have hd : d < b := hds d (List.mem_cons_self ..)
    have he : e < b := hes e (List.mem_cons_self ..)
    obtain ⟨h1, h2⟩ := split b d e (val b ds) (val b es) hd he hv
    have hl' : ds.length = es.length := by simpa using hl
    have ih := unique_same_length b ds es hl'
      (fun x hx => hds x (List.mem_cons_of_mem _ hx))
      (fun x hx => hes x (List.mem_cons_of_mem _ hx)) h2
    rw [h1, ih]

/-- The same in base ten, for the reader who came from Numerals.lean. -/
theorem unique_base_ten (ds es : List Nat) (hl : ds.length = es.length)
    (hds : ∀ d ∈ ds, d < 10) (hes : ∀ e ∈ es, e < 10)
    (hv : val 10 ds = val 10 es) : ds = es :=
  unique_same_length 10 ds es hl hds hes hv

/-! ## §2 · Chapter 3: a zero on the high end changes nothing -/

theorem high_zero (b : Nat) : ∀ ds : List Nat, val b (ds ++ [0]) = val b ds
  | [] => by simp [val]
  | d :: ds => by simp [val, high_zero b ds]

/-- So without a length condition, one number has two names: [3] and [3, 0]. -/
theorem two_names : val 10 [3] = val 10 [3, 0] ∧ [3] ≠ ([3, 0] : List Nat) := by
  refine ⟨by decide, by decide⟩

/-! ## §3 · Chapter 3: the digit is a remainder -/

theorem low_digit_is_remainder (b d : Nat) (ds : List Nat) (hd : d < b) :
    val b (d :: ds) % b = d := by
  simp only [val]
  rw [Nat.add_mul_mod_self_left, Nat.mod_eq_of_lt hd]

/-- A multiple of the base ends in zero: nothing left over. -/
theorem multiple_ends_in_zero (b : Nat) (ds : List Nat) (hb : 0 < b) :
    val b (0 :: ds) % b = 0 := low_digit_is_remainder b 0 ds hb

/-! ## §4 · Chapter 3: no zero, and still no two names -/

/-- Bijective numeration: digits 1 … b, no zero. Every number has at most one name,
    at any length at all. -/
theorem bijective_unique (b : Nat) :
    ∀ (ds es : List Nat), (∀ d ∈ ds, 1 ≤ d ∧ d ≤ b) → (∀ e ∈ es, 1 ≤ e ∧ e ≤ b) →
      val b ds = val b es → ds = es
  | [], [], _, _, _ => rfl
  | [], e :: es, _, hes, hv => by
    have := (hes e (List.mem_cons_self ..)).1
    simp only [val] at hv
    omega
  | d :: ds, [], hds, _, hv => by
    have := (hds d (List.mem_cons_self ..)).1
    simp only [val] at hv
    omega
  | d :: ds, e :: es, hds, hes, hv => by
    simp only [val] at hv
    have hd := hds d (List.mem_cons_self ..)
    have he := hes e (List.mem_cons_self ..)
    have hv' : (d - 1) + b * val b ds = (e - 1) + b * val b es := by omega
    obtain ⟨h1, h2⟩ := split b (d - 1) (e - 1) (val b ds) (val b es) (by omega) (by omega) hv'
    have ih := bijective_unique b ds es
      (fun x hx => hds x (List.mem_cons_of_mem _ hx))
      (fun x hx => hes x (List.mem_cons_of_mem _ hx)) h2
    have : d = e := by omega
    rw [this, ih]

/-- Ten in bijective base ten is a single digit (written A, say), twenty is [A, 1]:
    ten ones and one ten. No zero anywhere. -/
example : val 10 [10] = 10 ∧ val 10 [10, 1] = 20 := by decide

end Book11

#print axioms Book11.split
#print axioms Book11.unique_same_length
#print axioms Book11.unique_base_ten
#print axioms Book11.high_zero
#print axioms Book11.two_names
#print axioms Book11.low_digit_is_remainder
#print axioms Book11.multiple_ends_in_zero
#print axioms Book11.bijective_unique
