/-
  The Turnaround — the Closed Universe that Recollapses, in Lean 4
  Principia Orthogona · Book 8 · Pablo Nogueira Grossi · G6 LLC · 2026
  Companion to OrthogonalWitness.lean (the de Sitter bounce).

  STATUS: The algebra is independently verified (numeric: the cycloid solves the
          closed-dust Friedmann first integral (da/dt)² = a_max/a − 1 to ~1e−10,
          with a(0)=0, a(π)=a_max, a(2π)=0). The Lean proofs are written to be
          sound but have NOT yet been run through the kernel (compilation deferred
          until a Mathlib build is available). Do not cite as machine-checked
          until `lake build` passes.

  THE PICTURE (classical — Friedmann 1922).
    A closed (k=+1), matter-dominated (dust) universe is the three-sphere S³ whose
    radius follows the cycloid, in conformal time η:

        a(η) = R (1 − cos η),     t(η) = R (η − sin η),     R = a_max / 2.

    It is born at a = 0 (Big Bang, η=0), swells to a greatest sphere a_max at the
    turnaround (η=π), and shrinks back to a = 0 (Big Crunch, η=2π). This is the
    exact mirror of the de Sitter bounce: a HILL with a maximum and two zeros,
    where de Sitter is a VALLEY with a minimum (the throat) and none. Where de
    Sitter had a floor (`radius_has_throat`, a ≥ ℓ), the recollapse has a CEILING
    (a ≤ a_max) and two singular endpoints.

  The cycloid itself is textbook; nothing here is discovered. What is new to this
  corpus is the formalization and the pairing. We set the scalar core: the ceiling
  (turnaround), the floor at zero, the two singular endpoints (Bang and Crunch),
  and the maximum attained at η = π.
-/
import Mathlib.Analysis.SpecialFunctions.Trigonometric.Basic
-- (uses Real.neg_one_le_cos, Real.cos_le_one, Real.cos_zero, Real.cos_pi,
--  Real.cos_two_pi; `import Mathlib` is the safe fallback if a path shifts)

namespace Turnaround

open Real

/-- Cycloid scale factor of the closed dust universe, in conformal time η,
    with R = a_max / 2. -/
noncomputable def a (R η : ℝ) : ℝ := R * (1 - Real.cos η)

/-- **Ceiling (the turnaround).** For R ≥ 0 the radius never exceeds a_max = 2R:
    the universe expands to a greatest sphere and no further. -/
theorem a_le_max (R η : ℝ) (hR : 0 ≤ R) : a R η ≤ 2 * R := by
  have h : 0 ≤ R * (1 + Real.cos η) :=
    mul_nonneg hR (by linarith [Real.neg_one_le_cos η])
  simp only [a]; nlinarith [h]

/-- **Floor at zero.** For R ≥ 0 the radius is never negative: a ≥ 0. -/
theorem a_nonneg (R η : ℝ) (hR : 0 ≤ R) : 0 ≤ a R η := by
  have h : 0 ≤ R * (1 - Real.cos η) :=
    mul_nonneg hR (by linarith [Real.cos_le_one η])
  simpa only [a] using h

/-- **The Big Bang.** At η = 0 the sphere has zero radius. -/
theorem bang (R : ℝ) : a R 0 = 0 := by
  simp only [a, Real.cos_zero]; ring

/-- **The Big Crunch.** At η = 2π the sphere returns to zero radius. -/
theorem crunch (R : ℝ) : a R (2 * π) = 0 := by
  simp only [a, Real.cos_two_pi]; ring

/-- **The turnaround.** At η = π the radius attains its maximum a_max = 2R. -/
theorem turnaround (R : ℝ) : a R π = 2 * R := by
  simp only [a, Real.cos_pi]; ring

/-- The maximum is genuinely attained: the turnaround value equals the ceiling. -/
theorem turnaround_is_ceiling (R : ℝ) : a R π = 2 * R ∧ ∀ η, 0 ≤ R → a R η ≤ a R π := by
  refine ⟨turnaround R, ?_⟩
  intro η hR
  rw [turnaround R]
  exact a_le_max R η hR

end Turnaround
