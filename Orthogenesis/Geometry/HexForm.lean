-- Orthogenesis/Geometry/HexForm.lean
--
-- The quadratic form under the hex grid.
--
-- Candidate linear-algebra floor.  The corpus reasons spectrally in 124 files
-- and states the spectral theorem in two; this file does not close that gap,
-- but it does put the one piece of linear algebra the hex geometry actually
-- rests on under the kernel.
--
-- hexToVec2 sends the axial coordinate (q, r) to (q + r/2, (sqrt 3 / 2) * r).
-- The squared length of that vector is
--
--     Q(q, r) = q^2 + q*r + r^2,
--
-- which is the Eisenstein norm form, equivalently the A2 root lattice form.
-- Its discriminant is 1 - 4 = -3.  Everything the corpus says about hexagonal
-- distance, six-fold symmetry and nearest neighbours is a statement about this
-- one binary form.
--
-- WHAT THIS ESTABLISHES
--   hexToVec2_normSq       : the embedding induces exactly Q.
--   hexForm_nonneg         : Q is positive semidefinite over the integers.
--   hexForm_eq_zero        : Q vanishes only at the origin, so Q is definite.
--   hexNeighbors_form_one  : all six neighbours have Q = 1, so the six-fold
--                            ring is the set of minimal vectors of Q.
--
-- ALREADY IN THE CORPUS, AND THIS FILE DID NOT FIND IT
--   book4/ch21-the-closing-field.html carries
--       T = m^2 + mn + n^2 = N_{Q(omega)/Q}(m + n*omega)
--   as the Caspar-Klug T-number of a closable hexagonal shell, with Goldberg
--   polyhedra and Descartes on total defect.  That is this file's Q, written
--   as the Eisenstein norm.  ch26-kaleidoscope-test.html adds that Jacobi's
--   two-square theorem and "its Eisenstein analogue" are the same statement
--   twice.  This file is the machine-checked floor under those chapters and
--   was written without citing them.
--
-- NOT IN THE CORPUS, AND WORTH ADDING
--   * h(-3) = 1.  The discriminant -3 has class number one, so there is a
--     UNIQUE reduced form of that discriminant.  That is WHY the Eisenstein
--     classification in ch21 is complete rather than merely available, and
--     -3 is one of the nine Heegner discriminants, the list that ends at -163.
--     "class number" and "Heegner" appear in 0 files.
--   * The theta series of this lattice, sum over (q,r) of x^Q(q,r), is a
--     weight-one Eisenstein series of level 3: the count of representations
--     of n is 6*(d_{1,3}(n) - d_{2,3}(n)).  That places the hex lattice inside
--     modular forms.  "theta series" appears in 0 files.
--
-- WHAT IT DOES NOT ESTABLISH
--   * Not that the six neighbours are the ONLY vectors with Q = 1.  That is
--     true and is the statement that the A2 lattice has kissing number 6; it
--     needs a bound argument that is not attempted here.
--   * Nothing about the spectral theorem.  Q being definite is one instance of
--     a general fact this file does not state.
--   * Nothing connecting Q to the Eisenstein integers as a ring.  The forms
--     agree; the ring structure is not built.
--
-- Toolchain: Lean 4 + Mathlib, pinned by lean-toolchain.
-- Axiom report: pending first CI run.  Until it is pasted below with the run
-- number, this file is a claim and not a verification.

import Orthogenesis.Geometry.HexGrid

namespace Orthogenesis.HexForm

open Orthogenesis

/-- The binary quadratic form carried by the axial lattice. -/
def Q (q r : ℤ) : ℤ := q ^ 2 + q * r + r ^ 2

/-- Discriminant of `Q`, in the usual convention `b^2 - 4ac` for
    `a*q^2 + b*q*r + c*r^2`.  Here `a = b = c = 1`. -/
theorem Q_discriminant : (1 : ℤ) ^ 2 - 4 * 1 * 1 = -3 := by norm_num

/-- The Euclidean embedding induces exactly `Q`. -/
theorem hexToVec2_normSq (h : HexCoord) :
    (hexToVec2 h).x ^ 2 + (hexToVec2 h).y ^ 2
      = (h.q : ℝ) ^ 2 + (h.q : ℝ) * (h.r : ℝ) + (h.r : ℝ) ^ 2 := by
  have h3 : Real.sqrt 3 ^ 2 = 3 := Real.sq_sqrt (by norm_num)
  simp only [hexToVec2]
  linear_combination ((h.r : ℝ) ^ 2 / 4) * h3

/-- `Q` is positive semidefinite: `4Q = (2q + r)^2 + 3r^2`. -/
theorem hexForm_nonneg (q r : ℤ) : 0 ≤ Q q r := by
  unfold Q
  nlinarith [sq_nonneg (2 * q + r), sq_nonneg r]

/-- `Q` vanishes only at the origin, so it is positive definite. -/
theorem hexForm_eq_zero (q r : ℤ) (h : Q q r = 0) : q = 0 ∧ r = 0 := by
  unfold Q at h
  have k : (2 * q + r) ^ 2 + 3 * r ^ 2 = 0 := by linear_combination 4 * h
  have hr : r = 0 := by
    have h1 : r * r = 0 := by nlinarith [sq_nonneg (2 * q + r), sq_nonneg r]
    rcases mul_eq_zero.mp h1 with h' | h' <;> exact h'
  subst hr
  have h2 : q * q = 0 := by nlinarith [h]
  rcases mul_eq_zero.mp h2 with h' | h' <;> exact ⟨h', rfl⟩

/-- Every one of the six axial neighbours sits at `Q = 1`: the six-fold ring is
    a set of minimal vectors of the form. -/
theorem hexNeighbors_form_one (h n : HexCoord) (hn : n ∈ hexNeighbors h) :
    Q (n.q - h.q) (n.r - h.r) = 1 := by
  unfold Q
  simp only [hexNeighbors, List.mem_cons, List.not_mem_nil, or_false] at hn
  rcases hn with rfl | rfl | rfl | rfl | rfl | rfl <;> simp <;> ring

end Orthogenesis.HexForm
