/-
  Cardiac Hopf — center-manifold reduction of the SA-node dm³ oscillator, in Lean 4
  Principia Orthogona · Book 3 · ch6b-cardiac · Pablo Nogueira Grossi · G6 LLC · Newark NJ · 2026

  STATUS: The algebraic core below — the reduced radial dynamics on the center
          manifold, the limit-cycle amplitude, the supercritical (first Lyapunov)
          sign, and the contrast with the bare one-mode ansatz — is written to be
          sound but has NOT yet been run through the kernel (compilation deferred
          until a Mathlib build is available). The *existence* of the center
          manifold is the standard center-manifold theorem; it is invoked, not
          formalized here. Do not cite as machine-checked until `lake build` passes.

  Model (μ, ω the Hopf data; L = λ > 0 the stable-mode decay rate — λ is Lean's
  lambda, so it is written L here):
      ẋ = μx − ωy − x·u,   ẏ = ωx + μy − y·u,   u̇ = −L·u + (x²+y²).
  On the leading-order center manifold u = (x²+y²)/L the radial dynamics reduce to
      ṙ = μ r − r³/L        (verified symbolically; see ch6b-cardiac.html).
-/
import Mathlib.Tactic

namespace CardiacHopf

variable (μ ω L x y r : ℝ)

/-- Stable mode slaved to the oscillation on the leading-order center manifold. -/
noncomputable def uc (L x y : ℝ) : ℝ := (x ^ 2 + y ^ 2) / L

/-- Center-manifold vector field, x-component:  ẋ = μx − ωy − x·u. -/
noncomputable def fx (μ ω L x y : ℝ) : ℝ := μ * x - ω * y - x * uc L x y
/-- y-component:  ẏ = ωx + μy − y·u. -/
noncomputable def fy (μ ω L x y : ℝ) : ℝ := ω * x + μ * y - y * uc L x y

/-- **Reduced radial dynamics.** On the center manifold,
    x·ẋ + y·ẏ = μ(x²+y²) − (x²+y²)²/L, i.e. r·ṙ = μr² − r⁴/L, hence ṙ = μr − r³/L. -/
theorem radial_reduction (hL : L ≠ 0) :
    x * fx μ ω L x y + y * fy μ ω L x y = μ * (x ^ 2 + y ^ 2) - (x ^ 2 + y ^ 2) ^ 2 / L := by
  simp only [fx, fy, uc]; field_simp; ring

/-- **Limit-cycle amplitude.** r² = L·μ is a non-trivial zero of the reduced radial
    field ṙ = μr − r³/L — the sinus-rhythm limit cycle of amplitude r* = √(Lμ). -/
theorem limit_cycle (hL : L ≠ 0) (h : r ^ 2 = L * μ) : μ * r - r ^ 3 / L = 0 := by
  have hr : r ^ 3 = r * r ^ 2 := by ring
  rw [hr, h]; field_simp; ring

/-- Sign of −1/L. NOTE, 2026-09-12: this statement mentions no vector field. It
    says that a positive real has a negative negative-reciprocal, and nothing
    more. Reading −1/L as the cubic (first Lyapunov) coefficient of the reduced
    field is an identification made in prose and not seen by the kernel; the
    axiom gate cannot report that, because it reports axioms. The supercriticality
    content is `radial_deriv_at_cycle` below. Kept under this name because the
    name is cited elsewhere. -/
theorem supercritical (hL : 0 < L) : -(1 / L) < 0 := by
  have : 0 < 1 / L := one_div_pos.mpr hL
  linarith

/-- **The bare one-mode ansatz misses the saturation.** Setting u = 0 gives
    x·ẋ + y·ẏ = μ(x²+y²): no cubic term, so the amplitude is unbounded for μ > 0 and
    there is no limit cycle. The saturation comes *only* from the slaved mode. -/
theorem one_mode_no_saturation :
    x * (μ * x - ω * y) + y * (ω * x + μ * y) = μ * (x ^ 2 + y ^ 2) := by ring


/-- **Supercritical, as a statement about the reduced field.** At the limit cycle
    r² = Lμ the derivative of ṙ = μr − r³/L is exactly −2μ, so for μ > 0 the cycle
    attracts. This is what `supercritical` is named for and does not say. -/
theorem radial_deriv_at_cycle (hL : 0 < L) (h : r ^ 2 = L * μ) :
    μ - 3 * r ^ 2 / L = -(2 * μ) := by
  have hL' : L ≠ 0 := ne_of_gt hL
  rw [h]
  field_simp
  try ring

end CardiacHopf
