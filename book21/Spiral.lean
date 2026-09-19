/-
Volume XXI — rung 21. The classification of planar linear systems, and what
"the same system" is allowed to mean.

WHY THIS FILE EXISTS

On 2026-09-19 the corpus withdrew, on eleven pages, the claim that six or more
domains are related by "exact mathematical identity, not analogy". The
withdrawal rested on a computation: across the bridge rows carrying both μ and
ω, no two are linearly similar — 0 similar pairs out of 55. A computation over
eleven rows is evidence about eleven rows. This file is the theorem the
computation was an instance of, so the conclusion no longer depends on the
table being read correctly.

Two pieces, in the order Strogatz puts them. The source is
`Nonlinear_Dynamics_and_Chaos_2018_Steven_H._Strogatz.pdf`, sha256
e4c3681c…, 532 pages, listed in docs/floor-texts.tsv, §5.2 "Classification of
Linear Systems", printed pp. 129–138: the discriminant τ² − 4Δ on pp. 132 and
135, and the classification diagram at Figure 5.2.8, p. 138. Located by
book21/spiral-pages-verify.py against that file, not quoted from memory.

(The common name "the trace–determinant plane" is not used in this printing.
Strogatz gives the diagram without naming the plane, so this file does not put
the phrase in his mouth.)

  1. A planar linear system with eigenvalues μ ± iω, ω ≠ 0, is automatically a
     SPIRAL — the discriminant τ² − 4Δ equals −4ω², which is negative without
     any further assumption — and it is a SINK exactly when μ < 0. So being a
     spiral sink says only: μ < 0 and ω ≠ 0. It is a very weak description,
     and eleven systems satisfying it have almost nothing in common.

  2. Similar matrices have the same trace and the same determinant. Since
     τ = 2μ and Δ = μ² + ω², the pair (μ, ω²) is an INVARIANT of the system.
     Two spiral sinks with different μ, or different ω², are therefore not
     the same map in different coordinates — not approximately, not up to
     anything. They are different.

That second theorem is what "0 out of 55" was measuring. It is proved here in
the direction that the falsification actually needs: different invariants
forbid similarity. The converse — same invariants imply similarity, which
needs rational canonical form — is NOT proved here, and is not needed: it
would only be required to show two of the rows ARE the same, and none are.

WHAT THIS FILE DOES NOT SAY

Nothing here forbids the eleven systems from sharing a qualitative picture.
They do share one: every planar linear spiral sink is topologically conjugate
to every other. That fact is not formalised here, and it is also the reason
the shared picture carries no information — it would hold for eleven damped
oscillators picked at random.

Toolchain: Lean 4.33.0-rc1. Mathlib: tag v4.33.0-rc1.
-/
import Mathlib.LinearAlgebra.Matrix.Trace
import Mathlib.LinearAlgebra.Matrix.NonsingularInverse
import Mathlib.Analysis.SpecialFunctions.Pow.Real

open Matrix

/-- The real normal form of a planar system with eigenvalues `μ ± iω`:
    rotation by `ω` scaled by `μ`. -/
def spiral (μ ω : ℝ) : Matrix (Fin 2) (Fin 2) ℝ :=
  !![μ, -ω; ω, μ]

@[simp] theorem trace_spiral (μ ω : ℝ) : (spiral μ ω).trace = 2 * μ := by
  simp [spiral, Matrix.trace_fin_two]; ring

@[simp] theorem det_spiral (μ ω : ℝ) : (spiral μ ω).det = μ ^ 2 + ω ^ 2 := by
  simp [spiral, Matrix.det_fin_two]; ring

/-- **Strogatz §5.2, the discriminant.** For a planar system the character of
    the fixed point is read off `τ² − 4Δ`. With eigenvalues `μ ± iω` that
    quantity is `−4ω²` — so as soon as `ω ≠ 0` the system spirals, and no
    further hypothesis is available to make it do anything else. -/
theorem discriminant (μ ω : ℝ) :
    (spiral μ ω).trace ^ 2 - 4 * (spiral μ ω).det = -(4 * ω ^ 2) := by
  simp; ring

theorem is_spiral (μ ω : ℝ) (hω : ω ≠ 0) :
    (spiral μ ω).trace ^ 2 - 4 * (spiral μ ω).det < 0 := by
  rw [discriminant]
  have : 0 < ω ^ 2 := by positivity
  linarith

theorem is_sink_iff (μ ω : ℝ) : (spiral μ ω).trace < 0 ↔ μ < 0 := by
  rw [trace_spiral]
  constructor <;> intro h <;> linarith

/-! ### Similarity cannot change the invariants -/

/-- Conjugating by an invertible `P` leaves the trace alone. -/
theorem trace_of_conj (A P : Matrix (Fin 2) (Fin 2) ℝ) (hP : IsUnit P.det) :
    (P⁻¹ * A * P).trace = A.trace := by
  rw [Matrix.trace_mul_comm, ← Matrix.mul_assoc, Matrix.mul_nonsing_inv P hP,
    Matrix.one_mul]

/-- And the determinant. -/
theorem det_of_conj (A P : Matrix (Fin 2) (Fin 2) ℝ) (hP : IsUnit P.det) :
    (P⁻¹ * A * P).det = A.det := by
  rw [Matrix.det_mul, Matrix.det_mul, Matrix.det_nonsing_inv]
  have h1 : Ring.inverse P.det * P.det = 1 := Ring.inverse_mul_cancel _ hP
  calc Ring.inverse P.det * A.det * P.det
      = A.det * (Ring.inverse P.det * P.det) := by ring
    _ = A.det := by rw [h1, mul_one]

/-- **The theorem the falsification needs.** If two planar spiral systems are
    the same map written in different coordinates, then their `μ` agree and
    their `ω` agree up to sign. Equivalently: `μ` and `ω²` are invariants, and
    a table of `(μ, ω)` pairs that are not equal is a table of systems that are
    not the same. -/
theorem similar_forces_same_invariants
    (μ ω μ' ω' : ℝ) (P : Matrix (Fin 2) (Fin 2) ℝ) (hP : IsUnit P.det)
    (h : P⁻¹ * spiral μ ω * P = spiral μ' ω') :
    μ = μ' ∧ ω ^ 2 = ω' ^ 2 := by
  have ht : (spiral μ ω).trace = (spiral μ' ω').trace := by
    rw [← h, trace_of_conj _ _ hP]
  have hd : (spiral μ ω).det = (spiral μ' ω').det := by
    rw [← h, det_of_conj _ _ hP]
  rw [trace_spiral, trace_spiral] at ht
  rw [det_spiral, det_spiral] at hd
  constructor
  · linarith
  · have : μ = μ' := by linarith
    subst this
    linarith

/-- The contrapositive, which is the form used against the table: different
    `μ` means the two systems are not conjugate by any invertible matrix
    whatsoever. -/
theorem different_mu_not_similar
    (μ ω μ' ω' : ℝ) (hμ : μ ≠ μ') :
    ¬ ∃ P : Matrix (Fin 2) (Fin 2) ℝ, IsUnit P.det ∧
        P⁻¹ * spiral μ ω * P = spiral μ' ω' := by
  rintro ⟨P, hP, h⟩
  exact hμ (similar_forces_same_invariants μ ω μ' ω' P hP h).1

/-- The closest pair in the corpus's own table, named. Immune adaptation sits
    at μ = −0.44 and Market volatility at μ = −0.67. They are not equal, so by
    the theorem above no change of coordinates takes one to the other. This is
    the whole of "0 out of 55", for one pair, with no arithmetic left to
    trust. -/
theorem immune_is_not_market (ω ω' : ℝ) :
    ¬ ∃ P : Matrix (Fin 2) (Fin 2) ℝ, IsUnit P.det ∧
        P⁻¹ * spiral (-0.44) ω * P = spiral (-0.67) ω' :=
  different_mu_not_similar _ _ _ _ (by norm_num)

#print axioms trace_spiral
#print axioms det_spiral
#print axioms discriminant
#print axioms is_spiral
#print axioms is_sink_iff
#print axioms trace_of_conj
#print axioms det_of_conj
#print axioms similar_forces_same_invariants
#print axioms different_mu_not_similar
#print axioms immune_is_not_market
