/-!
# PolarTriadClosure.lean

What a wavenumber-6 and wavenumber-10 pair can and cannot generate.

Saturn carries a wavenumber-6 polygonal jet pattern at its north pole, stable
across more than forty years of observation, and — reported 2 September 2026
from Hubble OPAL imagery — a wavenumber-10 pattern at its south pole, which is
strengthening rather than steady.

If two such patterns interact at all, the interaction is through resonant
triads: two wavenumbers m and n exchange energy with |m - n| and m + n. This
file formalises the arithmetic consequence of that rule and nothing else.

## What is proved

* `partners_six_ten` — the immediate triad partners of 6 and 10 are 4 and 16.
* `Reach` — the closure of a wavenumber pair under triad interaction.
* `reach_even` — **every wavenumber reachable from two even seeds is even.**
  A 6-10 cascade can therefore never produce an odd-wavenumber feature.
* `seven_not_reachable`, `nine_not_reachable` — two explicit consequences.
* `odd_seeds_reach_odd` — the evenness hypothesis is load-bearing, not
  decorative: from odd seeds the conclusion fails.

## What is NOT proved, and cannot be

Nothing here says Saturn's two polar patterns interact. Nothing here says the
hexagon and the decagon share a mechanism, a mode, or a cause. Whether any
coupling exists between the hemispheres is a physical question about a planet,
settled by observation and by a named transport mechanism, and no proof
assistant can reach it.

What this file supplies is the *falsifiable consequence* of assuming the
coupling: if the two polygons are triad-partners, the accessible wavenumber
lattice is the even integers. A confirmed odd-wavenumber polar feature arising
from this pair would refute the assumption. That is the whole of the content,
and the reason the file is short.

The competing explanation — that each polar jet organises independently under
local instability, the southern one now reorganising under changing seasonal
insolation after the 2025 equinox — is not addressed here and is not weakened
by anything proved here.

Mathlib-free: core Lean 4 only.
-/

namespace PolarTriadClosure

/-- The immediate resonant partners of two wavenumbers: the difference and the
    sum. Stated on `Nat` with truncated subtraction, which is harmless here
    because the difference is taken larger-minus-smaller. -/
def partners (m n : Nat) : Nat × Nat :=
  (max m n - min m n, m + n)

/-- The observed pair. Saturn's north polygon is wavenumber 6; the south
    polygon reported in 2026 is wavenumber 10. Their triad partners are 4 and 16. -/
theorem partners_six_ten : partners 6 10 = (4, 16) := by decide

/-- Wavenumbers reachable from the seeds `a` and `b` by repeated triad
    interaction: each seed is reachable, and sums and differences of reachable
    wavenumbers are reachable. -/
inductive Reach (a b : Nat) : Nat → Prop
  | seed_left  : Reach a b a
  | seed_right : Reach a b b
  | sum  {m n : Nat} : Reach a b m → Reach a b n → Reach a b (m + n)
  | diff {m n : Nat} : Reach a b m → Reach a b n → Reach a b (m - n)

/-- **The closure theorem.** From two even seeds, every reachable wavenumber is
    even. The triad cascade cannot leave the even lattice. -/
theorem reach_even {a b : Nat} (ha : a % 2 = 0) (hb : b % 2 = 0) :
    ∀ n, Reach a b n → n % 2 = 0 := by
  intro n h
  induction h with
  | seed_left => exact ha
  | seed_right => exact hb
  | sum _ _ ihm ihn => omega
  | diff _ _ ihm ihn => omega

/-- 6 and 10 are even. -/
theorem six_even : 6 % 2 = 0 := by decide
theorem ten_even : 10 % 2 = 0 := by decide

/-- **A prediction.** No wavenumber-7 feature can arise from a 6-10 triad
    cascade. Observing one would refute the coupling assumption. -/
theorem seven_not_reachable : ¬ Reach 6 10 7 := by
  intro h
  have := reach_even six_even ten_even 7 h
  omega

/-- The same for wavenumber 9. -/
theorem nine_not_reachable : ¬ Reach 6 10 9 := by
  intro h
  have := reach_even six_even ten_even 9 h
  omega

/-- 4 and 16 are reachable, as `partners_six_ten` says they should be. -/
theorem four_reachable : Reach 6 10 4 := by
  have h : (10 : Nat) - 6 = 4 := by decide
  have := Reach.diff (Reach.seed_right : Reach 6 10 10) (Reach.seed_left : Reach 6 10 6)
  rwa [h] at this

theorem sixteen_reachable : Reach 6 10 16 := by
  have h : (6 : Nat) + 10 = 16 := by decide
  have := Reach.sum (Reach.seed_left : Reach 6 10 6) (Reach.seed_right : Reach 6 10 10)
  rwa [h] at this

/-! ## The hypothesis is load-bearing

`reach_even` assumes both seeds are even. Dropped, the conclusion is false: an
odd seed is itself an odd reachable wavenumber. This is recorded so that the
evenness assumption is visibly doing work rather than sitting idle in the
binder list.
-/

theorem odd_seeds_reach_odd :
    ¬ (∀ (a b n : Nat), Reach a b n → n % 2 = 0) := by
  intro h
  have := h 3 5 3 Reach.seed_left
  omega

-- Kernel gate.
#print axioms partners_six_ten
#print axioms reach_even
#print axioms seven_not_reachable
#print axioms nine_not_reachable
#print axioms four_reachable
#print axioms sixteen_reachable
#print axioms odd_seeds_reach_odd

end PolarTriadClosure
