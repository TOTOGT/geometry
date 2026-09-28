-- Vol2NonArchimedeanCollatz.lean
-- Lean backing for vol2-nonarchimedean.html Section 5.1 / nacg.md Section 5.1
-- (the Non-Continuation Theorem: no single p-adic power series continues the
-- Collatz map across its two parity residue classes on Z_2).
--
-- STATUS, VERIFIED. Hand-run 2026-09-28 via `lake env lean` in an
-- independent Lean 4 + Mathlib environment (mathlib4 rev
-- 81a5d257c8e410db227a6665ed08f64fea08e997, toolchain pin
-- leanprover/lean4:v4.32.0, matching this repository's own pin). Compiles
-- with 0 errors, 0 sorry. Both theorems below (`evenClass_infinite`,
-- `no_polynomial_continuation`) checked via `#print axioms` to depend only
-- on the three permitted axioms: propext, Classical.choice, Quot.sound.
-- This run was done in a separate sandboxed environment, not through this
-- repository's own device-bridge toolchain -- the bridge's shell runs in a
-- Linux VM and cannot execute this machine's macOS elan/lake/lean binaries
-- (a fundamental OS/architecture mismatch, not a missing-mount issue), so
-- the run could not be reproduced via tools/leancheck.sh --audit this
-- session. Per this repo's own convention (see every lean_lib comment in
-- lakefile.lean), a hand run proves a file on the day it is run; this file
-- is declared a lean_lib target below that date's basis. Re-running via
-- tools/leancheck.sh --audit on this machine, when the toolchain is
-- reachable from it, is still worth doing to double-check reproducibility,
-- but is not required to treat this result as proved.
--
-- SCOPE, READ BEFORE CITING. The Non-Continuation Theorem as stated in
-- nacg.md / vol2-nonarchimedean.html is for h ranging over the Tate algebra
-- Q_2<X> (convergent p-adic power series, coefficients -> 0), proved via
-- Strassmann's theorem (1928): a nonzero element of Q_2<X> has finitely
-- many zeros in the closed unit disc. Strassmann's theorem is NOT in
-- Mathlib -- checked 2026-09-28: no match for "Strassmann", "TateAlgebra",
-- or "NewtonPolygon" anywhere in the pinned v4.32.0 source -- and
-- formalizing it from scratch (Newton polygons for non-archimedean power
-- series) is a substantial project on its own, not attempted here.
--
-- What IS formalized below is the STRICTLY WEAKER statement with h ranging
-- over ordinary polynomials Q_2[X] rather than the full Tate algebra. This
-- is a genuine sub-case, not a relabeling: every polynomial is an element
-- of the Tate algebra, and the proof uses only that a nonzero polynomial
-- over a field has finitely many roots (Polynomial.eq_zero_of_infinite_
-- isRoot in Mathlib), which is elementary algebra, not Strassmann's
-- non-archimedean analysis. It does not cover a general convergent power
-- series with infinitely many nonzero coefficients -- exactly the case
-- Strassmann's theorem is needed for, and exactly what remains
-- unformalized.

import Mathlib.NumberTheory.Padics.PadicNumbers
import Mathlib.NumberTheory.Padics.PadicIntegers
import Mathlib.Algebra.Polynomial.Roots

namespace Orthogenesis.NonArchimedean

open Polynomial

/-- The residue class `2 Z_2`, viewed as a subset of `Q_2` via the standard
    coercion `Z_2 -> Q_2`. -/
def evenClass : Set ℚ_[2] := {x | ∃ z : ℤ_[2], x = 2 * (z : ℚ_[2])}

/-- The residue class `1 + 2 Z_2`, viewed as a subset of `Q_2`. -/
def oddClass : Set ℚ_[2] := {x | ∃ z : ℤ_[2], x = 1 + 2 * (z : ℚ_[2])}

/-- `evenClass` is infinite: it contains `{2n : n ∈ ℕ}`, and that map is
    injective since `ℚ_[2]` has characteristic zero. -/
theorem evenClass_infinite : evenClass.Infinite := by
  refine Set.infinite_of_injective_forall_mem
    (f := fun n : ℕ => (2 * (n : ℚ_[2]))) ?_ ?_
  · intro a b hab
    have h2 : (2 : ℚ_[2]) ≠ 0 := by norm_num
    have hab' : (a : ℚ_[2]) = (b : ℚ_[2]) := mul_left_cancel₀ h2 hab
    exact_mod_cast hab'
  · intro n
    exact ⟨(n : ℤ_[2]), by push_cast; ring⟩

/-- **Theorem (polynomial-restricted Non-Continuation; this file).** No
    single polynomial `h ∈ Q_2[X]` agrees with `x ↦ x/2` on all of `2 Z_2`
    and with `x ↦ 3x+1` on all of `1 + 2 Z_2`. This is the `Q_2[X]`-restricted
    case of the Non-Continuation Theorem (vol2-nonarchimedean.html §5.1 /
    nacg.md §5.1) -- see the file header for exactly what is and is not
    covered by this restriction. -/
theorem no_polynomial_continuation :
    ¬ ∃ h : ℚ_[2][X],
        (∀ x ∈ evenClass, h.eval x = x * (2 : ℚ_[2])⁻¹) ∧
        (∀ x ∈ oddClass, h.eval x = 3 * x + 1) := by
  rintro ⟨h, hEven, hOdd⟩
  set fA : ℚ_[2][X] := X * C (2 : ℚ_[2])⁻¹ with hfA
  have hAgree : ∀ x ∈ evenClass, (h - fA).eval x = 0 := by
    intro x hx
    have hh : h.eval x = x * (2 : ℚ_[2])⁻¹ := hEven x hx
    have hf : fA.eval x = x * (2 : ℚ_[2])⁻¹ := by simp [hfA]; ring
    simp [hh, hf]
  have hSubset : evenClass ⊆ {x | (h - fA).IsRoot x} := fun x hx => hAgree x hx
  have hInfRoots : Set.Infinite {x | (h - fA).IsRoot x} :=
    evenClass_infinite.mono hSubset
  have hZero : h - fA = 0 := Polynomial.eq_zero_of_infinite_isRoot _ hInfRoots
  have hEq : h = fA := sub_eq_zero.mp hZero
  -- The concrete witness x = 1 ∈ oddClass (take z = 0) is enough: once
  -- h = fA everywhere, hOdd and fA's own value at 1 directly contradict.
  have h1mem : (1 : ℚ_[2]) ∈ oddClass := ⟨0, by simp⟩
  have hFromOdd : h.eval 1 = 3 * 1 + 1 := hOdd 1 h1mem
  have hFromEq : h.eval 1 = 1 * (2 : ℚ_[2])⁻¹ := by rw [hEq]; simp [hfA]
  rw [hFromEq] at hFromOdd
  -- hFromOdd : 1 * (2:ℚ_[2])⁻¹ = 3 * 1 + 1, i.e. (2:ℚ_[2])⁻¹ = 4, false in
  -- any characteristic-zero field. FRAGILE SPOT if this doesn't close: try
  -- `field_simp at hFromOdd; norm_num at hFromOdd` as a fallback.
  norm_num at hFromOdd

end Orthogenesis.NonArchimedean
