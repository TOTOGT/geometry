/-!
# PolarPolygonCommonRefinement.lean

Can a wavenumber-6 and a wavenumber-10 pattern be two symmetries of one field?

Saturn carries a sixfold polygonal jet at its north pole, stable across forty
years, and — reported 2 September 2026 from Hubble OPAL imagery — a tenfold
pattern at its south pole, strengthening rather than steady. The tempting move
is to treat the pair as a single resonant structure. This file asks what that
would require and answers it in the negative.

## The setting

Put both patterns on their common refinement. A sixfold pattern and a tenfold
pattern share a sector grid of lcm(6, 10) = 30. On thirty sectors:

* a **sixfold** pattern repeats every 30 / 6 = **5** sectors;
* a **tenfold** pattern repeats every 30 / 10 = **3** sectors.

A field carrying both symmetries is therefore periodic with period 5 and with
period 3 at once. Since gcd(5, 3) = 1, it is periodic with period 1 — constant.

## What is proved

* `periodic_sub` — periods subtract: from periods `a` and `b` with `b ≤ a`, the
  field is periodic with period `a - b`. The Euclidean step, done by hand.
* `hex_and_dec_forces_constant` — **a field with both sixfold and tenfold
  symmetry on the common refinement is constant.** Two applications of
  `periodic_sub` (5, 3 → 2; 3, 2 → 1) and an induction.
* `constant_is_bisymmetric` — the converse direction, so the theorem is not
  vacuous: the constant field does carry both symmetries.
* `sixfold_alone_permits_structure` — one symmetry alone does not force
  constancy, exhibited by a concrete non-constant field of period 5. The
  hypothesis pair is load-bearing.

## What this means, and what it does not

It means the hexagon and the decagon **cannot be two symmetries of a single
field**. Anything shared between them is not a common symmetry, because the
only field admitting both is the trivial one. Any coupling therefore has to be
dynamical — a named transport mechanism between the hemispheres — and cannot
be obtained from the geometry of the two wavenumbers.

That is a constraint on theories of the pair, not a claim about Saturn. Nothing
here says the two polygons are related, or unrelated. The competing account —
that each polar jet organises independently under local instability, the
southern one now reorganising under changing insolation after the 2025 equinox
— is untouched by anything proved here, and remains the explanation to beat.

Mathlib-free: core Lean 4 only. Companion to `SaturnHexagon.lean`, which models
the sixfold case concretely as `Fin 6 → ℝ`.

## VERIFICATION STATUS — 2026-09-05. CLEAN, RUN AND RECORDED.

Elaborated twice on the repository pin, `leanprover/lean4:v4.32.0`, on two
machines and two operating systems, with identical output both times:

* bare `lean` on Linux, x86_64, container;
* bare `lean` and then `lake build` on macOS, the author's machine.

`lake build PolarTriadClosure PolarPolygonCommonRefinement` completed
successfully, five jobs. Both files are declared default targets in
`lakefile.lean`, so a later toolchain or Mathlib change fails the build rather
than passing unnoticed — the gap `SaturnHexagon.lean` lived in until 2026-08-21.

Per declaration:

```
    periodic_sub                  [propext, Quot.sound]
    periodic_one_const            does not depend on any axioms
    hex_and_dec_forces_constant   [propext, Quot.sound]
    constant_is_bisymmetric       does not depend on any axioms
    sawtooth_periodic_five        [propext]
    sixfold_alone_permits_structure [propext]
```

No `sorryAx`. No `Classical.choice`. The two axioms that do appear are Lean's
own and arrive through the induction on an inductive `Prop`.

A run dates from the day it was run and says nothing about any later day. The
target declaration is what carries it forward; this block is what makes the
claim checkable against the file rather than asserted over it.
-/

namespace PolarPolygonCommonRefinement

/-- A field on the sector grid is periodic with period `p` when shifting by `p`
    changes nothing. Sectors are indexed by `Nat`; the finite circle is recovered
    by also imposing the period of the full grid. -/
def Periodic {α : Type _} (v : Nat → α) (p : Nat) : Prop :=
  ∀ k, v (k + p) = v k

/-- **Periods subtract.** The Euclidean step, written out rather than imported. -/
theorem periodic_sub {α : Type _} (v : Nat → α) (a b : Nat)
    (ha : Periodic v a) (hb : Periodic v b) (hba : b ≤ a) :
    Periodic v (a - b) := by
  intro k
  have hsum : k + (a - b) + b = k + a := by omega
  have h1 : v (k + (a - b) + b) = v (k + (a - b)) := hb (k + (a - b))
  rw [hsum] at h1
  rw [← h1]
  exact ha k

/-- Period one means constant. -/
theorem periodic_one_const {α : Type _} (v : Nat → α) (h : Periodic v 1) :
    ∀ k, v k = v 0 := by
  intro k
  induction k with
  | zero => rfl
  | succ n ih =>
      have := h n
      rw [show n + 1 = n + 1 from rfl] at this
      rw [this]; exact ih

/-- **The result.** On the common refinement of thirty sectors, a sixfold
    pattern has period 5 and a tenfold pattern has period 3. A field carrying
    both is constant: 5 and 3 are coprime, so the two symmetries generate the
    whole rotation group of the grid.

    The hexagon and the decagon cannot be two symmetries of one field. -/
theorem hex_and_dec_forces_constant {α : Type _} (v : Nat → α)
    (h6 : Periodic v 5) (h10 : Periodic v 3) :
    ∀ k, v k = v 0 := by
  have p2 : Periodic v 2 := by
    have := periodic_sub v 5 3 h6 h10 (by omega)
    simpa using this
  have p1 : Periodic v 1 := by
    have := periodic_sub v 3 2 h10 p2 (by omega)
    simpa using this
  exact periodic_one_const v p1

/-- The converse, so the theorem is not vacuously about an empty class: the
    constant field does carry both symmetries. -/
theorem constant_is_bisymmetric {α : Type _} (c : α) :
    Periodic (fun _ => c) 5 ∧ Periodic (fun _ => c) 3 :=
  ⟨fun _ => rfl, fun _ => rfl⟩

/-! ## Both hypotheses are load-bearing

Sixfold symmetry alone leaves plenty of structure. The field `k ↦ k % 5` has
period 5 and is not constant, so `hex_and_dec_forces_constant` genuinely needs
the tenfold hypothesis and is not a statement about period 5 on its own.
-/

/-- A non-constant field of period 5. -/
def sawtooth : Nat → Nat := fun k => k % 5

theorem sawtooth_periodic_five : Periodic sawtooth 5 := by
  intro k
  simp [sawtooth, Nat.add_mod_right]

theorem sawtooth_not_constant : sawtooth 1 ≠ sawtooth 0 := by decide

theorem sixfold_alone_permits_structure :
    ¬ (∀ (v : Nat → Nat), Periodic v 5 → ∀ k, v k = v 0) := by
  intro h
  exact sawtooth_not_constant (h sawtooth sawtooth_periodic_five 1)

/-!
## The thirty-sector grid was doing work the theorem did not admit

STATUS: KERNEL-AUDITED 2026-09-05, v4.32.0. 15 declarations in this file, 0
trusting sorryAx, none resting on anything outside propext / Classical.choice /
Quot.sound — and five resting on no axiom whatever. Report at
tools/verify-audit/2026-09-05/PolarPolygonCommonRefinement.axioms.txt, written
by the run, not typed.

`hex_and_dec_forces_constant` is true and stays true. What overreached was the
sentence written around it — "the only field admitting both a hexagon and a
decagon is the trivial one" — which quietly carried the choice of a
THIRTY-sector refinement inside it as though it were a fact about six and ten.

It is not. Take sixty sectors instead. A sixfold pattern then repeats every
sixty-sixths = ten sectors, a tenfold every six, and `gcd(10, 6) = 2`, not 1.
So a field carrying both symmetries is forced only to have period two — and
`alt` below is exactly that field: non-constant, sixfold, tenfold, on sixty
sectors. The forcing-to-constant is an artefact of taking the MINIMAL common
refinement, where the generated subgroup happens to exhaust the grid.

WHAT IS ACTUALLY TRUE, on every grid. Rotations of order 6 and order 10
generate rotation of order `lcm 6 10 = 30`. On a grid of `N` sectors a field
carrying both is periodic with period `N / 30` — that is, it is invariant under
C₃₀ and no more. At `N = 30` that reads "constant" because `N / 30 = 1`; at
`N = 60` it reads "period two"; it never reads "hexagon and decagon coexisting".

The physical reading survives and gets sharper rather than weaker. A single
field carrying both symmetries does not show a hexagon and does not show a
decagon. It shows a THIRTY-sided pattern. Nobody has photographed a
triacontagon on Saturn — so the two polygons are still two rings, and the claim
now names what would refute it, which "the field is trivial" never did.

Found by asking what base sixty would do to the arithmetic. Base is notation
and changes no number; sixty as a NUMBER OF SECTORS changes the answer, and the
instinct behind the question — that sixty has room where thirty does not,
because 60/6 and 60/10 still share a factor — was correct.
-/

/-- The alternating field on the sixty-sector grid: non-constant, and carrying
both symmetries. This is the counterexample to the sentence, not to the theorem. -/
def alt : Nat → Nat := fun k => k % 2

theorem alt_periodic_ten : Periodic alt 10 := by
  intro k
  simp [alt, Nat.add_mod]

theorem alt_periodic_six : Periodic alt 6 := by
  intro k
  simp [alt, Nat.add_mod]

theorem alt_not_constant : alt 1 ≠ alt 0 := by decide

/-- On sixty sectors, sixfold repeats every ten and tenfold every six — and
those two together do NOT force a constant. -/
theorem sixty_sectors_permit_structure :
    ¬ (∀ (v : Nat → Nat), Periodic v 10 → Periodic v 6 → ∀ k, v k = v 0) := by
  intro h
  exact alt_not_constant (h alt alt_periodic_ten alt_periodic_six 1)

/-- Two periods give their sum. -/
theorem periodic_add {α : Type _} (v : Nat → α) (a b : Nat)
    (ha : Periodic v a) (hb : Periodic v b) : Periodic v (a + b) := by
  intro k
  rw [← Nat.add_assoc, hb, ha]

/-- Two periods give every multiple of either. -/
theorem periodic_mul {α : Type _} (v : Nat → α) (a : Nat) (ha : Periodic v a) :
    ∀ n, Periodic v (a * n)
  | 0 => by intro k; simp
  | (n + 1) => by
      have h := periodic_add v (a * n) a (periodic_mul v a ha n) ha
      rwa [← Nat.mul_succ] at h

/-- Two periods give the remainder of one by the other. Euclid's step. -/
theorem periodic_mod {α : Type _} (v : Nat → α) (a b : Nat)
    (ha : Periodic v a) (hb : Periodic v b) : Periodic v (b % a) := by
  have hdm : a * (b / a) + b % a = b := Nat.div_add_mod b a
  have hle : a * (b / a) ≤ b := Nat.le.intro hdm
  have hsub : b - a * (b / a) = b % a :=
    Nat.sub_eq_of_eq_add (hdm.symm.trans (Nat.add_comm _ _))
  have := periodic_sub v b (a * (b / a)) hb (periodic_mul v a ha (b / a)) hle
  rwa [hsub] at this

/-- THE GENERAL STATEMENT. Two periods give their greatest common divisor, and
nothing smaller. `hex_and_dec_forces_constant` is the case `gcd 5 3 = 1`; the
sixty-sector case is `gcd 10 6 = 2`, which is why `alt` exists. -/
theorem periodic_gcd {α : Type _} (v : Nat → α) :
    ∀ a b, Periodic v a → Periodic v b → Periodic v (Nat.gcd a b)
  | 0, b, _, hb => by rwa [Nat.gcd_zero_left]
  | (a + 1), b, ha, hb => by
      rw [Nat.gcd_succ]
      exact periodic_gcd v (b % (a + 1)) (a + 1) (periodic_mod v (a + 1) b ha hb) ha
  termination_by a _ _ _ => a
  decreasing_by exact Nat.mod_lt _ (Nat.succ_pos a)

-- Kernel gate. Every theorem in the file, so `lake build` alone reports the
-- whole set; leancheck's --audit probe generates its own copy of these lines,
-- which is why a leancheck report on this file lists each declaration twice.
-- Harmless: every consumer of a gate report deduplicates by name.
--
-- sawtooth_not_constant was missing from this block until 2026-09-05 and was
-- therefore outside Tier 1 while the file around it was inside. A theorem is in
-- the tier because a line here names it, not because it sits in an audited file.
#print axioms periodic_sub
#print axioms periodic_one_const
#print axioms hex_and_dec_forces_constant
#print axioms constant_is_bisymmetric
#print axioms sawtooth_periodic_five
#print axioms sawtooth_not_constant
#print axioms sixfold_alone_permits_structure
#print axioms alt_periodic_ten
#print axioms alt_periodic_six
#print axioms alt_not_constant
#print axioms sixty_sectors_permit_structure
#print axioms periodic_add
#print axioms periodic_mul
#print axioms periodic_mod
#print axioms periodic_gcd

end PolarPolygonCommonRefinement
