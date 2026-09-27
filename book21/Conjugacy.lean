/-
Volume XXI — chapter 2. Topological conjugacy of planar spiral sinks, in polar form.

WHY THIS FILE EXISTS

`book21/Spiral.lean` ends with a section titled WHAT THIS FILE DOES NOT SAY:
"every planar linear spiral sink is topologically conjugate to every other. That
fact is not formalised here." Chapter 2 (ch02-topological-conjugacy.html) built the
conjugacy numerically, following Hirsch, Smale & Devaney (2013) §4.2, p. 66, whose
one-dimensional example is h(x) = x^(λ₂/λ₁). This file is the kernel-checked core of
that construction.

WHAT IS PROVED

In polar coordinates (r, θ) with r > 0, the flow of `spiral μ ω` (Spiral.lean) is
φ_t(r, θ) = (r·e^{μt}, θ + ωt). The map

    H(r, θ) = ( r^(μ'/μ),  θ + (ω' − ω)·log r / μ )

satisfies H ∘ φ_t = ψ_t ∘ H for every t, where ψ is the flow of `spiral μ' ω'`.
That is the conjugacy equation, on the punctured plane.

WHAT IS NOT PROVED HERE

That H extends continuously to the origin and is a homeomorphism of the plane.
Both are true for μ, μ' < 0 (r^(μ'/μ) → 0 as r → 0) and are what HSD's p.66 theorem
supplies; they are left to the text, and the chapter says so.

Toolchain: the repository pin, leanprover/lean4:v4.32.0 with Mathlib v4.32.0.
-/
import Mathlib

namespace Book21

open Real

/-- The one-dimensional core: HSD's h(x) = x^(b/a) turns the flow x·e^{at}
    into the flow x·e^{bt}. -/
theorem rpow_flow (x t a b : ℝ) (hx : 0 < x) (ha : a ≠ 0) :
    (x * exp (a * t)) ^ (b / a) = x ^ (b / a) * exp (b * t) := by
  rw [mul_rpow hx.le (exp_pos _).le, ← exp_mul]
  congr 2
  field_simp

/-- The flow of `spiral μ ω` in polar coordinates (r, θ), r > 0. -/
noncomputable def polarFlow (μ ω t : ℝ) (p : ℝ × ℝ) : ℝ × ℝ :=
  (p.1 * exp (μ * t), p.2 + ω * t)

/-- The conjugacy of Chapter 2, in polar coordinates. -/
noncomputable def H (μ ω μ' ω' : ℝ) (p : ℝ × ℝ) : ℝ × ℝ :=
  (p.1 ^ (μ' / μ), p.2 + (ω' - ω) * log p.1 / μ)

/-- **The conjugacy equation.** H carries the flow of `spiral μ ω` onto the flow of
    `spiral μ' ω'`, at every time, on the punctured plane. -/
theorem conjugacy (μ ω μ' ω' t : ℝ) (p : ℝ × ℝ) (hμ : μ ≠ 0) (hr : 0 < p.1) :
    H μ ω μ' ω' (polarFlow μ ω t p) = polarFlow μ' ω' t (H μ ω μ' ω' p) := by
  obtain ⟨r, θ⟩ := p
  simp only [H, polarFlow] at hr ⊢
  refine Prod.ext ?_ ?_
  · exact rpow_flow r t μ μ' hr hμ
  · simp only
    rw [log_mul hr.ne' (exp_pos _).ne', log_exp]
    field_simp
    ring

/-- The corpus's own pair (Spiral.lean, `immune_is_not_market`): no invertible matrix
    takes the immune spiral (μ = −0.44) to the market spiral (μ = −0.67), yet this
    continuous map does, for any rotation rates ω, ω'. -/
theorem immune_conj_market (ω ω' t : ℝ) (p : ℝ × ℝ) (hr : 0 < p.1) :
    H (-0.44) ω (-0.67) ω' (polarFlow (-0.44) ω t p)
      = polarFlow (-0.67) ω' t (H (-0.44) ω (-0.67) ω' p) :=
  conjugacy _ _ _ _ _ _ (by norm_num) hr

end Book21

#print axioms Book21.rpow_flow
#print axioms Book21.conjugacy
#print axioms Book21.immune_conj_market
