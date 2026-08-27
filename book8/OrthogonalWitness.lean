/-
  The Orthogonal Witness Theorem — de Sitter as the closed FRW universe, in Lean 4
  Principia Orthogona · Book 8 · Pablo Nogueira Grossi · G6 LLC · 2026

  STATUS: MACHINE-CHECKED 2026-08-27, leanprover/lean4:v4.32.0 (the toolchain this
          repository pins), via `lake env lean book8/OrthogonalWitness.lean`.
          All four theorems report

              depends on axioms: [propext, Classical.choice, Quot.sound]

          — Mathlib's standard base, no `sorryAx`. See SCOPE below for what those
          four theorems do and do not carry; the tensor pullback is NOT among them.
          It is independently verified in sympy (exact symbolic: the hyperboloid
          parametrization pulls back to the FRW line element with a zero difference
          matrix), which is a separate tool and a separate claim.

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

  SCOPE OF THE FOUR THEOREMS — what is and is not carried by the kernel.
    None of the four is vacuous: no `True`, no unsatisfiable hypothesis, no
    conclusion independent of its hypotheses. They are, however, scalar identities,
    and the reader should know exactly which:

    · `on_hyperboloid` and `proper_time` are the SAME Mathlib fact,
      cosh² − sinh² = 1, in two dresses: the first multiplied by ℓ², the second
      negated. Two names, one content.
    · `on_hyperboloid` states the ω-REDUCED constraint. The S³ factor ‖ω‖² = 1 is
      substituted by hand in the statement, not carried as a hypothesis, so the
      theorem is an identity in two real variables and says nothing about ℝ^{1,4}
      as a space. No metric, manifold, pullback or normal bundle appears anywhere
      in this file.
    · `radius_has_throat` is stated for 0 ≤ ℓ. At ℓ = 0 it is true but empty
      (a 0 τ = 0 ≤ 0), because Lean's τ / 0 = 0. The geometry needs 0 < ℓ; the
      weaker hypothesis costs nothing here but is not the geometric statement.
    · `throat_value` is cosh 0 = 1.

    The tensor pullback — the step that would make "induced metric" a proved
    phrase rather than a docstring phrase — is the sympy result cited above and is
    NOT in the kernel. Cite these four as what they are: the scalar identities the
    embedding must satisfy, machine-checked; not the embedding theorem.
-/
-- Real.one_le_cosh lives in Mathlib/Analysis/SpecialFunctions/Trigonometric/DerivHyp.lean,
-- which Trigonometric.Basic does not reach. Checked against the Mathlib pinned by this
-- repository (v4.32.0) rather than assumed. The full import is a cache hit here.
import Mathlib
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
theorem proper_time (ℓ τ : ℝ) :
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

/-
  **Codimension of the witness.** The witness direction is the normal bundle of
  the embedding dS₄ ↪ ℝ^{1,4}; its rank is the codimension, exactly one.
-/
-- Codimension bookkeeping, NOT a theorem: `5 - 4 = 1` is arithmetic on ℕ literals,
-- closed by `rfl` whether or not anything about normal bundles holds — and truncated
-- subtraction makes statements of this shape true for reasons unrelated to geometry.
-- Stated beside three real analytic identities it would invite the reading that the
-- vocabulary matching means the theorem matches. dim ℝ^{1,4} − dim dS₄ = 5 − 4 = 1 is
-- recorded in the header comment, where a remark belongs.

end OrthogonalWitness

/-
  KERNEL AUDIT. Compiling is not proving: a theorem admitted with `sorry` still
  compiles, and `sorry` is a warning rather than an error. These four lines ask the
  kernel what each proof actually rests on.

  Expected, for each: [propext, Classical.choice, Quot.sound] and nothing else.
  If `sorryAx` appears anywhere below, that declaration is not proved.

  Run from the repository root, which already has Mathlib built:
      lake env lean book8/OrthogonalWitness.lean
-/
#print axioms OrthogonalWitness.on_hyperboloid
#print axioms OrthogonalWitness.proper_time
#print axioms OrthogonalWitness.radius_has_throat
#print axioms OrthogonalWitness.throat_value
