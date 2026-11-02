import Mathlib

/-!
# GCM V2, Theorem D″ (radial scalar case): persistence with an explicit radius

STATUS: UNTESTED (written 2026-11-02, no local toolchain); the author compiles it.

Read each statement for what it says, not what its name promises:

* `persistence_1d` : if g = f + F is strictly decreasing on [-ρ, ρ] with g(ρ) < 0 < g(-ρ), then g has
  exactly one zero in [-ρ, ρ]. Pure real analysis (intermediate value theorem + injectivity).
* `persistence_1d_of_bounds` : the same conclusion from the explicit hypotheses
  f' ≤ -m on [-ρ,ρ], |F'| < m, and f(ρ) + |F(ρ)| < 0 < f(-ρ) - |F(-ρ)|. That is the Lean form of
  "the radius is min((c/2)ρ, m)". It is a statement about ONE-DIMENSIONAL functions only: it says
  a zero (an equilibrium of ẋ = f(x)+F(x)) persists. It does not mention cycles, the angle θ,
  Lyapunov functions, or higher dimension; the passage from "equilibrium of the radial equation"
  to "hyperbolic limit cycle of the flow on the cylinder" is the hand argument in the paper.
* `lyapunov_endpoint` : x·f(x) ≤ -(c/2)x² at x = ρ > 0 gives f(ρ) ≤ -(c/2)ρ. Arithmetic only.
-/

theorem persistence_1d (g : ℝ → ℝ) (ρ : ℝ) (hρ : 0 < ρ) (hcont : Continuous g)
    (hanti : StrictAntiOn g (Set.Icc (-ρ) ρ)) (hneg : g ρ < 0) (hpos : 0 < g (-ρ)) :
    ∃! x, x ∈ Set.Icc (-ρ) ρ ∧ g x = 0 := by
  have hle : -ρ ≤ ρ := by linarith
  have hmem : (0 : ℝ) ∈ Set.Icc (g ρ) (g (-ρ)) := ⟨hneg.le, hpos.le⟩
  obtain ⟨x, hx, hx0⟩ := intermediate_value_Icc' hle hcont.continuousOn hmem
  refine ⟨x, ⟨hx, hx0⟩, ?_⟩
  rintro y ⟨hy, hy0⟩
  exact hanti.injOn hy hx (hy0.trans hx0.symm)

theorem persistence_1d_of_bounds (f F : ℝ → ℝ) (m ρ : ℝ) (hρ : 0 < ρ)
    (hdf : Differentiable ℝ f) (hdF : Differentiable ℝ F)
    (hm : ∀ x ∈ Set.Icc (-ρ) ρ, deriv f x ≤ -m)
    (hFd : ∀ x ∈ Set.Icc (-ρ) ρ, |deriv F x| < m)
    (h1 : f ρ + |F ρ| < 0) (h2 : 0 < f (-ρ) - |F (-ρ)|) :
    ∃! x, x ∈ Set.Icc (-ρ) ρ ∧ f x + F x = 0 := by
  have hg : Differentiable ℝ (fun x => f x + F x) := hdf.add hdF
  have hderiv : ∀ x ∈ Set.Icc (-ρ) ρ, deriv (fun x => f x + F x) x < 0 := by
    intro x hx
    rw [deriv_add (hdf x) (hdF x)]
    have h3 := hm x hx
    have h4 := (abs_lt.mp (hFd x hx)).2
    linarith
  have hanti : StrictAntiOn (fun x => f x + F x) (Set.Icc (-ρ) ρ) :=
    strictAntiOn_of_deriv_neg (convex_Icc _ _) hg.continuous.continuousOn
      (fun x hx => hderiv x (interior_subset hx))
  refine persistence_1d (fun x => f x + F x) ρ hρ hg.continuous hanti ?_ ?_
  · have := le_abs_self (F ρ)
    show f ρ + F ρ < 0
    linarith
  · have := neg_abs_le (F (-ρ))
    show 0 < f (-ρ) + F (-ρ)
    linarith

theorem lyapunov_endpoint (f : ℝ → ℝ) (c ρ : ℝ) (hρ : 0 < ρ) (h : ρ * f ρ ≤ -(c / 2) * ρ ^ 2) :
    f ρ ≤ -(c / 2) * ρ := by
  by_contra hcon
  push_neg at hcon
  have : ρ * (-(c / 2) * ρ) < ρ * f ρ := mul_lt_mul_of_pos_left hcon hρ
  nlinarith
