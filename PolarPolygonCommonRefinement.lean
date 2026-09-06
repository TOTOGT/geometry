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

-- Kernel gate.
#print axioms periodic_sub
#print axioms periodic_one_const
#print axioms hex_and_dec_forces_constant
#print axioms constant_is_bisymmetric
#print axioms sawtooth_periodic_five
#print axioms sixfold_alone_permits_structure

end PolarPolygonCommonRefinement
