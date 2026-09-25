-- GATE-DECLARE: sorries = none
-- GATE-REASON: new file 2026-09-25 for the geometry pin (Lean v4.32.0, Mathlib v4.32.0).
-- UNTESTED until the author runs `lake build` on it.
/-
# CircadianReeb.lean — Book 3, Chapter 3 · Circadian Regulation (taught path 29,
# ch3-circadian.html; the same page serves the Cajueiro edition)

The chapter's model: coordinates (q, p, z), contact form α = dz + q dp, Reeb field R.
Vectors and points are triples (q, p, z).

  §1  Exercises 3.1–3.2, confirmed. α ∧ dα equals the determinant dq ∧ dp ∧ dz at
      every point (so it is nowhere zero), and R = ∂/∂z is the unique field with
      α(R) = 1 and ι_R dα = 0.
  §2  The Reeb flow of this model is z ↦ z + t. It has no closed orbit, and it
      keeps the difference of any two states constant, so no orbit approaches
      another. Two consequences for the chapter: Taubes' theorem (Theorem 3.1)
      needs a CLOSED 3-manifold — the chapter's own local model has no periodic
      orbit — and a Reeb flow has no attractor (it preserves α ∧ dα), so the
      "circadian attractor" is not a Reeb orbit. §3.2's "the only long-run
      behaviours are periodic orbits or quasi-periodic tori" fails here too.
  §3  Exercise 3.4 and the Falsifiability box. The Reeb field of c·α is R / c,
      so its closed orbits take c times as long: rescaling α changes the period.
      For any autonomous system, running all rates c times faster turns a
      solution x(t) into x(c t), and x(c ·) has period S exactly when x has
      period c·S: doubling every rate halves the period. The chapter predicts
      the opposite ("should leave T approximately constant"). Temperature
      compensation is a mechanism that keeps T fixed while rates change
      unequally — it is not uniform rescaling.
  §4  Exercise 3.3. For q = cos ωt, p = sin ωt, the Legendrian condition
      ż = −q ṗ gives z(t) = −(ωt/2 + sin(2ωt)/4), and after one lap
      z(2π/ω) = z(0) − π. A process that runs round a loop in (q, p) is not a
      closed Legendrian curve: z drifts by the enclosed area each cycle.

Not formalised: Taubes' theorem itself, Legendrian isotopy, the coupled
circadian–thalamocortical flow, and the biology.
-/

import Mathlib

namespace Orthogenesis.Circadian

open Real

/-- Points and tangent vectors in (q, p, z) coordinates. -/
abbrev P := ℝ × ℝ × ℝ

/-- α = dz + q dp at the point x, applied to the vector v. -/
def alpha (x v : P) : ℝ := v.2.2 + x.1 * v.2.1

/-- dα = dq ∧ dp. -/
def dalpha (u v : P) : ℝ := u.1 * v.2.1 - u.2.1 * v.1

/-! ## §1 The contact condition and the Reeb field -/

/-- (α ∧ dα)(u, v, w). -/
def contactVol (x u v w : P) : ℝ :=
  alpha x u * dalpha v w - alpha x v * dalpha u w + alpha x w * dalpha u v

/-- det of the rows u, v, w in the columns q, p, z: the volume form dq ∧ dp ∧ dz. -/
def det3 (u v w : P) : ℝ :=
  u.1 * (v.2.1 * w.2.2 - v.2.2 * w.2.1) - u.2.1 * (v.1 * w.2.2 - v.2.2 * w.1)
    + u.2.2 * (v.1 * w.2.1 - v.2.1 * w.1)

/-- Exercise 3.1: α ∧ dα = dq ∧ dp ∧ dz at every point. -/
theorem contactVol_eq_det (x u v w : P) : contactVol x u v w = det3 u v w := by
  simp only [contactVol, det3, alpha, dalpha]
  ring

theorem contact_condition (x : P) : contactVol x (1, 0, 0) (0, 1, 0) (0, 0, 1) = 1 := by
  rw [contactVol_eq_det]
  norm_num [det3]

/-- R = ∂/∂z. -/
def reeb : P := (0, 0, 1)

/-- Exercise 3.2: α(R) = 1 and ι_R dα = 0. -/
theorem reeb_spec (x : P) : alpha x reeb = 1 ∧ ∀ v, dalpha reeb v = 0 :=
  ⟨by simp [alpha, reeb], fun v => by simp [dalpha, reeb]⟩

/-- … and R is the only such field. -/
theorem reeb_unique (x R : P) (h1 : alpha x R = 1) (h2 : ∀ v, dalpha R v = 0) : R = reeb := by
  obtain ⟨a, b, c⟩ := R
  have ha := h2 (0, 1, 0)
  have hb := h2 (1, 0, 0)
  simp [dalpha] at ha hb
  simp [alpha, hb] at h1
  simp [reeb, ha, hb, h1]

/-! ## §2 The Reeb flow of the model: no closed orbit, no attraction -/

/-- The flow of R = ∂/∂z. -/
def flow (t : ℝ) (x : P) : P := (x.1, x.2.1, x.2.2 + t)

theorem flow_eq (t : ℝ) (x : P) : flow t x = x + t • reeb := by
  ext <;> simp [flow, reeb]

/-- No state returns to itself: the local model has no periodic Reeb orbit. -/
theorem flow_no_periodic (x : P) {t : ℝ} (h : flow t x = x) : t = 0 := by
  have := congrArg (fun y : P => y.2.2) h
  simpa [flow] using this

/-- The flow keeps the difference of two states fixed: no orbit approaches another. -/
theorem flow_preserves_diff (t : ℝ) (x y : P) : flow t x - flow t y = x - y := by
  ext <;> simp [flow]

/-! ## §3 Rescaling changes the period -/

/-- The Reeb field of c·α is R / c. -/
theorem reeb_scaled {c : ℝ} (hc : c ≠ 0) (x : P) :
    c * alpha x (0, 0, 1 / c) = 1 ∧ ∀ v, c * dalpha (0, 0, 1 / c) v = 0 :=
  ⟨by simp [alpha, hc], fun v => by simp [dalpha]⟩

/-- Running every rate c times faster: x(t) ↦ x(c t) solves ẏ = c · f(y). -/
theorem time_rescale {E : Type*} [NormedAddCommGroup E] [NormedSpace ℝ E] (f : E → E)
    (x : ℝ → E) (hx : ∀ t, HasDerivAt x (f (x t)) t) (c t : ℝ) :
    HasDerivAt (fun s => x (c * s)) (c • f (x (c * t))) t := by
  have hl : HasDerivAt (fun s : ℝ => c * s) c t := by
    simpa using (hasDerivAt_id t).const_mul c
  exact (hx (c * t)).scomp t hl

/-- x(c ·) has period S exactly when x has period c·S. -/
theorem periodic_rescale_iff {α : Type*} (x : ℝ → α) {c : ℝ} (hc : c ≠ 0) (S : ℝ) :
    Function.Periodic (fun s => x (c * s)) S ↔ Function.Periodic x (c * S) := by
  constructor
  · intro h t
    have hcc : c * (t / c) = t := by
      rw [mul_div_assoc', mul_div_right_comm, div_self hc, one_mul]
    have := h (t / c)
    simp only at this
    rw [mul_add, hcc] at this
    exact this
  · intro h t
    show x (c * (t + S)) = x (c * t)
    rw [mul_add]
    exact h (c * t)

/-! ## §4 Exercise 3.3: the Legendrian lift of a loop does not close -/

/-- z(t) = −(ωt/2 + sin(2ωt)/4). -/
noncomputable def zLift (ω t : ℝ) : ℝ := -(ω * t / 2 + Real.sin (2 * ω * t) / 4)

/-- ż = −q ṗ with q = cos ωt, ṗ = ω cos ωt: the curve is Legendrian. -/
theorem zLift_legendrian (ω t : ℝ) :
    HasDerivAt (zLift ω) (-(Real.cos (ω * t)) * (ω * Real.cos (ω * t))) t := by
  have h1 : HasDerivAt (fun t => 2 * ω * t) (2 * ω) t := by
    simpa using (hasDerivAt_id t).const_mul (2 * ω)
  have h2 := (Real.hasDerivAt_sin (2 * ω * t)).comp t h1
  have h3 : HasDerivAt (fun t => ω * t / 2) (ω / 2) t := by
    simpa using ((hasDerivAt_id t).const_mul ω).div_const 2
  have h4 := (h3.add (h2.div_const 4)).neg
  have hc := Real.cos_sq (ω * t)
  rw [show 2 * (ω * t) = 2 * ω * t by ring] at hc
  refine h4.congr_deriv ?_
  linear_combination ω * hc

/-- After one lap (t = 2π/ω), z has dropped by π: the lift is not closed. -/
theorem zLift_not_closed {ω : ℝ} (hω : ω ≠ 0) : zLift ω (2 * π / ω) = zLift ω 0 - π := by
  have h1 : ω * (2 * π / ω) / 2 = π := by
    rw [show ω * (2 * π / ω) / 2 = π * (ω / ω) by ring, div_self hω, mul_one]
  have h2 : 2 * ω * (2 * π / ω) = ((4 : ℕ) : ℝ) * π := by
    rw [show 2 * ω * (2 * π / ω) = 4 * π * (ω / ω) by ring, div_self hω, mul_one]
    norm_num
  simp only [zLift]
  rw [h1, h2, Real.sin_nat_mul_pi]
  simp

end Orthogenesis.Circadian

/-! ## Axiom probe -/
#print axioms Orthogenesis.Circadian.contactVol_eq_det
#print axioms Orthogenesis.Circadian.contact_condition
#print axioms Orthogenesis.Circadian.reeb_spec
#print axioms Orthogenesis.Circadian.reeb_unique
#print axioms Orthogenesis.Circadian.flow_eq
#print axioms Orthogenesis.Circadian.flow_no_periodic
#print axioms Orthogenesis.Circadian.flow_preserves_diff
#print axioms Orthogenesis.Circadian.reeb_scaled
#print axioms Orthogenesis.Circadian.time_rescale
#print axioms Orthogenesis.Circadian.periodic_rescale_iff
#print axioms Orthogenesis.Circadian.zLift_legendrian
#print axioms Orthogenesis.Circadian.zLift_not_closed
