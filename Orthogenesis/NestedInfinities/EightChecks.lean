-- Orthogenesis/NestedInfinities/EightChecks.lean
-- Checks for Chapter 8 (ch8-nested-infinities.html).
--
-- GATE-DECLARE: sorries = none
-- GATE-REASON: three statements, each the formal content of a claim the
--   chapter made in prose. No theorem concludes `True`; no unused hypotheses.
--   Author's lake build 2026-10-01 (Lean 4.32.0 / Mathlib): 9/9, all nine
--   #print axioms probes on [propext, Classical.choice, Quot.sound], no
--   sorryAx, no warnings.
--
-- WHAT THIS IS FOR. Chapter 8 built its central pedagogical claim on a
-- cardinality step: vocabulary at aleph-0, grammar at aleph-1, and K as the
-- only crossing. The step does not exist. A sentence is a finite string over
-- a finite alphabet, and there are countably many of those. §1 is that fact.
--
-- §2 separates the two ladders the chapter had merged. The alephs are the
-- uncountable cardinals in order; the beths are iterated power sets.
-- beth-1 = aleph-1 is the Continuum Hypothesis, which is INDEPENDENT of ZFC
-- (Goedel 1940, Cohen 1963) -- not open, and not provable here. What IS
-- provable is the inequality, and that is all the chapter needs.
--
-- §3 is a counterexample to a claim in the Mandelbrot table: that a boundary
-- orbit "never escapes, never settles". At c = 1/4, the cusp of the main
-- cardioid and a boundary point, the orbit of 0 is increasing and bounded
-- above by 1/2 -- it converges to the parabolic fixed point.
--
-- Toolchain: Lean 4 + Mathlib
-- Chapter: ch8-nested-infinities.html (Book 3)

import Mathlib

namespace Orthogenesis.EightChecks

open Cardinal

/-! ## §1  Sentences over a finite vocabulary are countable -/

/-- A sentence is a finite string over the vocabulary. For any countable
    vocabulary -- a finite one in particular -- there are countably many. -/
instance sentences_countable (V : Type) [Countable V] : Countable (List V) :=
  inferInstance

/-- Stated as the chapter needs it: a finite vocabulary yields countably many
    sentences, so the set of sentences is not uncountable. -/
theorem sentence_set_not_uncountable (V : Type) [Finite V] :
    Countable (List V) := by
  have : Countable V := Finite.to_countable
  infer_instance

/-- The step the chapter actually wants is one level further out: a *language*
    is a set of sentences, and there are continuum-many of those. -/
theorem languages_have_continuum_many (V : Type) [Finite V] [Nonempty V] :
    #(Set (List V)) = 2 ^ ℵ₀ := by
  -- `simp` closes this from `Cardinal.mk_set` plus the list cardinality,
  -- which it finds itself; an explicit `#(List V) = ℵ₀` hypothesis was in
  -- the first draft and the linter reported it unused. Removed rather than
  -- silenced: an unused hypothesis is the shape a vacuous theorem takes.
  -- Both instances are load-bearing -- drop `Nonempty` and V may be empty,
  -- drop `Finite` and the list set need not be countable.
  simp [Cardinal.mk_set]

/-! ## §2  The beth ladder needs no Continuum Hypothesis -/

/-- Cantor: every cardinal is strictly below its power. This is the rung
    step, and it is unconditional. -/
theorem rung_is_strict (a : Cardinal) : a < 2 ^ a := Cardinal.cantor a

/-- beth-1 is the continuum, by definition of the beth ladder. -/
theorem beth_one_is_continuum : (2 : Cardinal) ^ ℵ₀ = continuum :=
  (Cardinal.two_power_aleph0).symm ▸ rfl

/-- What ZFC gives: aleph-1 is at most the continuum. Equality is the
    Continuum Hypothesis and is not provable here -- which is precisely why
    the chapter's ladder is a beth ladder and not an aleph ladder. -/
theorem aleph_one_le_continuum_only : aleph 1 ≤ continuum :=
  Cardinal.aleph_one_le_continuum

/-- And the continuum is strictly above the countable, unconditionally. -/
theorem continuum_above_countable : ℵ₀ < continuum := Cardinal.aleph0_lt_continuum

/-! ## §3  A boundary orbit that settles: c = 1/4 -/

/-- The quadratic orbit of 0 at parameter c. -/
noncomputable def orbit (c : ℝ) : ℕ → ℝ
  | 0 => 0
  | n + 1 => (orbit c n) ^ 2 + c

/-- At c = 1/4 the orbit stays in [0, 1/2].

    NOTE, and it is the point of writing this down. The first version of this
    file carried only the upper bound, `orbit (1/4) n ≤ 1/2`, and the kernel
    refused it. Correctly: `x ≤ 1/2` says nothing about how negative x is, and
    the step needs `x^2 ≤ 1/4`, which needs |x| ≤ 1/2. At x = -10 the step is
    simply false. The invariant has to be two-sided; the proof was wrong, not
    the tactic. -/
theorem orbit_quarter_bounds :
    ∀ n, 0 ≤ orbit (1/4) n ∧ orbit (1/4) n ≤ 1/2 := by
  intro n
  induction n with
  | zero => constructor <;> norm_num [orbit]
  | succ k ih =>
    obtain ⟨hlo, hhi⟩ := ih
    show 0 ≤ (orbit (1/4) k) ^ 2 + 1/4 ∧ (orbit (1/4) k) ^ 2 + 1/4 ≤ 1/2
    constructor
    · nlinarith [sq_nonneg (orbit (1/4) k)]
    · nlinarith [mul_nonneg (by linarith : (0:ℝ) ≤ 1/2 - orbit (1/4) k)
                            (by linarith : (0:ℝ) ≤ 1/2 + orbit (1/4) k)]

theorem orbit_quarter_le_half (n : ℕ) : orbit (1/4) n ≤ 1/2 :=
  (orbit_quarter_bounds n).2

theorem orbit_quarter_nonneg (n : ℕ) : 0 ≤ orbit (1/4) n :=
  (orbit_quarter_bounds n).1

/-- And it never decreases. -/
theorem orbit_quarter_mono : ∀ n, orbit (1/4) n ≤ orbit (1/4) (n + 1) := by
  intro n
  show orbit (1/4) n ≤ (orbit (1/4) n) ^ 2 + 1/4
  nlinarith [sq_nonneg (orbit (1/4) n - 1/2)]

/-- So the orbit at the boundary point c = 1/4 is bounded and monotone: it
    settles. The chapter's table said boundary orbits never do. -/
theorem boundary_orbit_can_settle :
    (∀ n, 0 ≤ orbit (1/4) n ∧ orbit (1/4) n ≤ 1/2) ∧
    (∀ n, orbit (1/4) n ≤ orbit (1/4) (n + 1)) :=
  ⟨orbit_quarter_bounds, orbit_quarter_mono⟩

-- ── Axiom probes ────────────────────────────────────────────────────────────
#print axioms sentence_set_not_uncountable
#print axioms languages_have_continuum_many
#print axioms rung_is_strict
#print axioms aleph_one_le_continuum_only
#print axioms continuum_above_countable
#print axioms orbit_quarter_bounds
#print axioms orbit_quarter_le_half
#print axioms orbit_quarter_mono
#print axioms boundary_orbit_can_settle

end Orthogenesis.EightChecks
