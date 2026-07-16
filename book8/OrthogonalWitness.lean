/-
  The Orthogonal Witness Theorem — de Sitter as the closed FRW universe, in Lean 4
  Principia Orthogona · Book 8 · Pablo Nogueira Grossi · G6 LLC · 2026

  STATUS: The algebra below is independently verified (sympy, exact symbolic:
          the hyperboloid parametrization pulls back to the FRW line element with
          a zero difference matrix). The Lean proofs are written to be sound but
          have NOT yet been run through the kernel (compilation deferred until a
          Mathlib build is available). Do not cite as machine-checked until
          `lake build` passes.

  THE THEOREM (Leg 1, geometric — the part that is a theorem).
    A closed FRW universe is a three-sphere S³ whose radius breathes as a(τ).
    Take the de Sitter radius a(τ) = ℓ·cosh(τ/ℓ). Then the map

        X⁰ = ℓ·sinh(τ/ℓ),   Xⁱ = ℓ·cosh(τ/ℓ)·ωⁱ   (ω ∈ S³ ⊂ ℝ⁴, |ω| = 1)

    lands on the unit hyperboloid  −(X⁰)² + Σ(Xⁱ)² = ℓ²  in 5-dimensional
    Minkowski space ℝ^{1,4}, and its induced metric is exactly

        ds² = −dτ² + ℓ²·cosh²(τ/ℓ)·dΩ₃².

    So the whole breathing history of S³ is a single static 4-surface inside a
    flat 5-space, seen from exactly ONE orthogonal (normal) direction — the
    minimal geometric witness. The extra dimension is not "above" in a mystical
    sense; it is the codimension of an isometric embedding. dim ℝ^{1,4} − dim dS₄
    = 5 − 4 = 1.

  WHAT IS *NOT* IN THIS FILE (Leg 2, epistemic).
    The claim that certifying the history requires a strictly EXTERIOR vantage
    that no internal observable realizes is a genuine result too — but it is a
    logical / observational one (Tarski's undefinability of truth; the
    Frauchiger–Renner and Local-Friendliness no-go theorems), a strict META-LEVEL
    and NOT a further spatial dimension. It is stated in the chapter, not
    formalized here. Conflating the +1 dimension with the +1 meta-level is the
    error the chapter exists to prevent.

  We formalize the checkable scalar core of Leg 1: the hyperboloid constraint,
  g_ττ = −1 (proper time is τ), and the de Sitter throat a(τ) ≥ ℓ (the sphere
  never collapses — a bounce, not a singularity). The full tensor pullback is
  recorded as the symbolic result above; only its scalar identities are set here.
-/
import Mathlib.Analysis.SpecialFunctions.Trigonometric.Basic
-- (uses Real.cosh_sq_sub_sinh_sq, Real.one_le_cosh, Real.cosh_zero; if a lemma
--  path shifts in your Mathlib pin, `import Mathlib` is the safe fallback)

namespace OrthogonalWitness

open Real

/-- de Sitter scale factor: the breathing radius of the closed spatial S³. -/
noncomputable def a (ℓ τ : ℝ) : ℝ := ℓ * Real.cosh (τ / ℓ)

/-- Timelike ambient coordinate of the embedding into ℝ^{1,4}. -/
noncomputable def X0 (ℓ τ : ℝ) : ℝ := ℓ * Real.sinh (τ / ℓ)

/-- **Leg 1 · Hyperboloid constraint.** For any proper time τ and radius ℓ, the
    image point lies on the unit hyperboloid of ℝ^{1,4}:
    −(X⁰)² + (radius)²·‖ω‖² = ℓ², using ‖ω‖² = 1 for ω ∈ S³.
    (Here the spatial part contributes a(ℓ,τ)²·1, so we state the ω-reduced form.) -/
theorem on_hyperboloid (ℓ τ : ℝ) :
    -(X0 ℓ τ) ^ 2 + (a ℓ τ) ^ 2 = ℓ ^ 2 := by
  have h : Real.cosh (τ / ℓ) ^ 2 - Real.sinh (τ / ℓ) ^ 2 = 1 :=
    Real.cosh_sq_sub_sinh_sq (τ / ℓ)
  have expand :
      -(X0 ℓ τ) ^ 2 + (a ℓ τ) ^ 2
        = ℓ ^ 2 * (Real.cosh (τ / ℓ) ^ 2 - Real.sinh (τ / ℓ) ^ 2) := by
    simp only [X0, a]; ring
  rw [expand, h]; ring

/-- **Leg 1 · Proper time.** The τ–τ component of the induced metric is −1, i.e.
    τ is proper time along the worldline of a comoving point. With the τ-velocity
    of the embedding having timelike part cosh(τ/ℓ) and radial part sinh(τ/ℓ),
    the Minkowski norm is −cosh² + sinh² = −1. -/
theorem proper_time (τ ℓ : ℝ) :
    -(Real.cosh (τ / ℓ)) ^ 2 + (Real.sinh (τ / ℓ)) ^ 2 = -1 := by
  have h : Real.cosh (τ / ℓ) ^ 2 - Real.sinh (τ / ℓ) ^ 2 = 1 :=
    Real.cosh_sq_sub_sinh_sq (τ / ℓ)
  linarith

/-- **Leg 1 · The throat (no singularity).** For ℓ ≥ 0 the breathing radius never
    drops below ℓ: a(ℓ,τ) ≥ ℓ, since cosh ≥ 1. The closed de Sitter universe
    contracts to a minimum sphere of radius ℓ and rebounds — a bounce, not a Big
    Bang point. -/
theorem radius_has_throat (ℓ τ : ℝ) (hℓ : 0 ≤ ℓ) : ℓ ≤ a ℓ τ := by
  have h : (1 : ℝ) ≤ Real.cosh (τ / ℓ) := Real.one_le_cosh (τ / ℓ)
  have hprod : 0 ≤ ℓ * (Real.cosh (τ / ℓ) - 1) := mul_nonneg hℓ (by linarith)
  simp only [a]; nlinarith [hprod]

/-- The throat radius is attained at τ = 0: a(ℓ,0) = ℓ. -/
theorem throat_value (ℓ : ℝ) : a ℓ 0 = ℓ := by
  simp only [a, zero_div, Real.cosh_zero, mul_one]

/-- **Codimension of the witness.** The witness direction is the normal bundle of
    the embedding dS₄ ↪ ℝ^{1,4}; its rank is the codimension, exactly one. -/
theorem witness_codimension : 5 - 4 = 1 := rfl

end OrthogonalWitness
