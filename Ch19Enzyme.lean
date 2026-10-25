import Mathlib

/-!
# Ch19Enzyme.lean — what the Chapter 19 "theorems" reduce to

STATUS: UNTESTED. Written 2026-10-25 without a Lean toolchain; the author must run
`lake env lean Ch19Enzyme.lean` and report the output. Do not cite as machine-checked
until it compiles and `#print axioms` is clean.

Two statements, both about the *toy model on the page*, not about any enzyme:

1. Non-commutativity of gating K and fold F (page "Theorem 19.1"). With
   K ψ = ψ if ψ is inside the gating tolerance, else 0, and F ψ = ψ + l·R ψ with R linear,
   K and F fail to commute exactly when F carries ψ across the tolerance boundary
   (and F ψ ≠ 0). Proved here in the direction the page needs: if ψ is inside and
   F ψ is outside and nonzero, then K (F ψ) ≠ F (K ψ).

2. Concentration-tilted fraction (page "Theorem 19.3"). The page's own tilted potential
   Φ_eff = Φ − k_B T ln([L]/K_d)·1_bound gives a free-energy gap that is *linear with
   slope 1 in ln[L]*, in units of k_B T. A Boltzmann fraction with that gap is a Hill
   function of exponent 1, not 2. Exponent 2 needs slope 2 (a further assumption).
-/

namespace Ch19Enzyme

section Gate
variable {V : Type*} [AddCommGroup V] [Module ℝ V]

/-- ψ lies within gating tolerance `cs` of the competent conformation `cb`. -/
def inside (c : V → ℝ) (cb cs : ℝ) (ψ : V) : Prop := |c ψ - cb| ≤ cs

open Classical in
/-- Gating: keep ψ if inside tolerance, else send it to 0. -/
noncomputable def K (c : V → ℝ) (cb cs : ℝ) (ψ : V) : V :=
  if inside c cb cs ψ then ψ else 0

/-- Fold: ψ ↦ ψ + l·R ψ, with R linear. -/
def F (R : V →ₗ[ℝ] V) (l : ℝ) (ψ : V) : V := ψ + l • R ψ

theorem F_zero (R : V →ₗ[ℝ] V) (l : ℝ) : F R l (0 : V) = 0 := by
  simp [F]

theorem FK_of_inside (c : V → ℝ) (cb cs : ℝ) (R : V →ₗ[ℝ] V) (l : ℝ) (ψ : V)
    (h : inside c cb cs ψ) : F R l (K c cb cs ψ) = F R l ψ := by
  simp [K, h]

theorem KF_of_outside (c : V → ℝ) (cb cs : ℝ) (R : V →ₗ[ℝ] V) (l : ℝ) (ψ : V)
    (h : ¬ inside c cb cs (F R l ψ)) : K c cb cs (F R l ψ) = 0 := by
  simp [K, h]

/-- If ψ is inside the tolerance, F ψ is outside it, and F ψ ≠ 0, then K and F do not
    commute at ψ. (Statement about the toy operators above only.) -/
theorem noncomm (c : V → ℝ) (cb cs : ℝ) (R : V →ₗ[ℝ] V) (l : ℝ) (ψ : V)
    (hin : inside c cb cs ψ) (hout : ¬ inside c cb cs (F R l ψ)) (hne : F R l ψ ≠ 0) :
    K c cb cs (F R l ψ) ≠ F R l (K c cb cs ψ) := by
  rw [KF_of_outside c cb cs R l ψ hout, FK_of_inside c cb cs R l ψ hin]
  exact fun h => hne h.symm

end Gate

section Tilt

/-- Boltzmann fraction with free-energy gap `a − ln(L/Kd)` (in units of k_B T), i.e. the
    page's tilt, is a Hill function of exponent 1. -/
theorem tilted_fraction_hill_one (a Kd L : ℝ) (hK : 0 < Kd) (hL : 0 < L) :
    1 / (1 + Real.exp (a - Real.log (L / Kd))) = 1 / (1 + Real.exp a * (Kd / L)) := by
  have hx : 0 < L / Kd := div_pos hL hK
  have h : Real.exp (a - Real.log (L / Kd)) = Real.exp a * (Kd / L) := by
    rw [Real.exp_sub, Real.exp_log hx]
    field_simp
  rw [h]

/-- Exponent 2 needs a gap with slope 2 in ln(L/Kd): an extra assumption. -/
theorem tilted_fraction_hill_two (a Kd L : ℝ) (hK : 0 < Kd) (hL : 0 < L) :
    1 / (1 + Real.exp (a - 2 * Real.log (L / Kd))) =
      1 / (1 + Real.exp a * (Kd / L) ^ 2) := by
  have hx : 0 < L / Kd := div_pos hL hK
  have h : Real.exp (a - 2 * Real.log (L / Kd)) = Real.exp a * (Kd / L) ^ 2 := by
    rw [Real.exp_sub, show (2 : ℝ) * Real.log (L / Kd) = Real.log (L / Kd) + Real.log (L / Kd) by ring,
      Real.exp_add, Real.exp_log hx]
    field_simp
  rw [h]

end Tilt

end Ch19Enzyme
