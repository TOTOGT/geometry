/-
  CycleCoupling.lean — SaturnHexagon.lean's angular coupling, at every n.

  WHY THIS FILE EXISTS.  `SaturnHexagon.lean` proves five theorems, cleanly, on
  `Fin 6`.  Reading them closely, none of the five is about six.  `angCoupling`
  there is

      (angCoupling v) i = v (i-1) + v (i+1)

  which is the adjacency operator of the cycle graph C₆, and `hex c` is its
  constant eigenvector at eigenvalue 2.  Those facts hold for the cycle on any
  number of sectors.  `Fin 6` is an instance, not a consequence.

  This file states the same three results over `ZMod (n+1)`.  If they go through
  — and the point of writing them is that they should — then SaturnHexagon.lean
  cannot be read as selecting wavenumber six, because its content is available
  at every wavenumber.  That is a negative result about this corpus, and it is
  the honest content of WP-104.

  WHAT IS NOT HERE.  The spectrum of C_n is 2·cos(2πk/n), and it is integral
  exactly for n ∈ {3,4,6} (Harary & Schwenk 1974, "Which graphs have integral
  spectra?").  That is the observation WP-104 raises as a *proposal* for why
  six.  It is NOT proved here: it needs circulant diagonalisation over ℂ, which
  is a real development and not a corollary of anything below.  Do not cite
  this file for it.

  VERIFICATION STATUS — 2026-09-06.  **CLEAN, RUN AND RECORDED.**

      cd ~/Desktop/geometry && lake env lean CycleCoupling.lean

  under leanprover/lean4:v4.32.0 with the mathlib build in that tree, reports
  for each of the three theorems:

      CycleCoupling.coupling_unif        [propext, Classical.choice, Quot.sound]
      CycleCoupling.unif_rot_invariant   [propext, Classical.choice, Quot.sound]
      CycleCoupling.rot_commutes         [propext, Classical.choice, Quot.sound]

  No sorryAx.  No errors.  The three `example` blocks specialising to six
  typecheck, which is the point of the file: the `Fin 6` results of
  SaturnHexagon.lean are corollaries of statements that never mention six.

  ONE PROVENANCE NOTE.  SaturnHexagon.lean's own clean run was recorded in the
  ~/Desktop/orthogenesis tree under v4.33.0-rc1.  This file was verified in
  ~/Desktop/geometry under **v4.32.0** — a different toolchain.  That is stated
  because SaturnHexagon.lean's header is a catalogue of exactly this kind of
  drift, and because the orthogenesis tree currently has mathlib cloned but not
  built, so nothing can be run there without `lake exe cache get` first.


  TWO PLACES IT MAY FAIL, both anticipated.

  (1) `coupling_unif` reduces to `c + c = 2 * c`.  SaturnHexagon.lean's header
      records that exact goal left unsolved under v4.14.0 in
      `hex_coupling_uniform`.  It is discharged here by `two_mul` explicitly
      rather than left to `ring`, for that reason.

  (2) `rot_commutes` needs `i - 1 + 1 = i` and `i + 1 - 1 = i`.  Two attempts
      failed on exactly these two lines, and both are recorded because the
      failures are this file's provenance:

        over `Fin (n+1)`, `abel`  ->  "abel_nf made no progress"
        over `Fin (n+1)`, `simp`  ->  "simp made no progress"

      Neither engaged `Fin (n+1)`'s additive structure.  The fix was not a
      third tactic but a change of index type.  The vertex set of a cycle IS
      Z/n, and `ZMod (n+1)` is a genuine `CommRing` in Mathlib, so `ring`
      discharges both goals with no dependence on lemma names that move
      between releases.  `Fin (n+1)` and `ZMod (n+1)` agree here, so nothing
      about the mathematics changed — only the type it is stated over, and
      arguably it is now stated over the right one.
-/
import Mathlib.Data.Real.Basic
import Mathlib.Data.ZMod.Basic
import Mathlib.Tactic.Ring

namespace CycleCoupling

variable {n : ℕ}

/-- Angular coupling on `n+1` sectors: the adjacency operator of the cycle
    graph.  Identical in form to `SaturnHexagon.angCoupling`, with the six
    replaced by a variable. -/
def angCoupling (v : ZMod (n + 1) → ℝ) : ZMod (n + 1) → ℝ :=
  fun i => v (i - 1) + v (i + 1)

/-- The uniform configuration: equal amplitude in every sector.
    `SaturnHexagon.hex` is this at `n + 1 = 6`. -/
def unif (c : ℝ) : ZMod (n + 1) → ℝ := fun _ => c

/-- Rotation by one sector.  `SaturnHexagon.rot` is this at `n + 1 = 6`. -/
def rot (v : ZMod (n + 1) → ℝ) : ZMod (n + 1) → ℝ := fun i => v (i - 1)

/-- The uniform configuration is an eigenvector of the coupling with
    eigenvalue 2 — **at every n**, not only at six. -/
theorem coupling_unif (c : ℝ) :
    angCoupling (unif c : ZMod (n + 1) → ℝ) = unif (2 * c) := by
  funext i
  simp only [angCoupling, unif]
  exact (two_mul c).symm

/-- The uniform configuration is rotation-invariant — **at every n**. -/
theorem unif_rot_invariant (c : ℝ) :
    rot (unif c : ZMod (n + 1) → ℝ) = unif c := by
  funext i
  simp only [rot, unif]

/-- Rotation commutes with the angular coupling — **at every n**. -/
theorem rot_commutes (v : ZMod (n + 1) → ℝ) :
    rot (angCoupling v) = angCoupling (rot v) := by
  funext i
  have h1 : i - 1 + 1 = i := by ring
  have h2 : i + 1 - 1 = i := by ring
  simp only [rot, angCoupling, h1, h2]

/-- The three results above, specialised to six.  If this typechecks, the
    `Fin 6` statements of `SaturnHexagon.lean` are corollaries of statements
    that never mention six.  (`ZMod (n+1)` reduces to `Fin (n+1)` in Mathlib,
    so `ZMod 6` here and `Fin 6` there are the same type.) -/
example (c : ℝ) : angCoupling (unif c : ZMod 6 → ℝ) = unif (2 * c) :=
  coupling_unif c

example (c : ℝ) : rot (unif c : ZMod 6 → ℝ) = unif c :=
  unif_rot_invariant c

example (v : ZMod 6 → ℝ) : rot (angCoupling v) = angCoupling (rot v) :=
  rot_commutes v

/-- Nothing in this namespace distinguishes six from any other sector count.
    Kept as a marker: if a later theorem here *does* single out six, it will
    need a hypothesis this file does not currently have. -/
theorem no_six_anywhere : True := trivial

end CycleCoupling

#print axioms CycleCoupling.coupling_unif
#print axioms CycleCoupling.unif_rot_invariant
#print axioms CycleCoupling.rot_commutes
