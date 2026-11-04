import Mathlib

/-
Book XXIV, interlude 2: blow-up, the fold, the virial argument, and the pressure-hull threshold. Lean core.

STATUS: COMPILED on the author's machine, 2026-11-04. It was written without a toolchain. The first compile found
four errors (type mismatches and a closing tactic in toy_quadratic_deriv, fold_tan_deriv, virial_first_derivative
and zoelly_pressure); after the fixes, `lake env lean book24/Interlude2.lean 2>&1 | tee book24/interlude2.axioms.txt`
reports all eighteen theorems depending only on [propext, Classical.choice, Quot.sound], and no sorryAx. Remaining
output is linter warnings about unused fallback tactics.

WHAT THIS FILE IS. It is the real-number arithmetic and calculus AROUND the partial differential equation, and
nothing about the equation itself. In particular it does NOT state or prove: the critical Schroedinger equation, the
conservation of mass and energy, the virial identity y'' = 16 E (the page derives it by scaling and checks it
numerically; here it enters only as a hypothesis), the sharp Gagliardo-Nirenberg inequality (a hypothesis `hGN`),
the blow-up alternative, Glassey's theorem as a statement about solutions, anything of Merle and Raphael, or shell
theory. Mathlib has no theory of this equation, and none is written here.

Page references are to book24/interlude2-frank-merle-blow-up.html.
  toy_quadratic_deriv, toy_quadratic_profile, toy_quadratic_unbounded   part 2: u' = u^2, u = 1/(c - t), u (c - t) = 1
  fold_tan_deriv                                                        part 4: x = s tan(s t) solves x' = s^2 + x^2
  virial_first_derivative, virial_second_derivative                     part 5: y = y0 + y1 t + 8 E t^2 has y'' = 16 E
  virial_collapse, glassey_step                                         part 5: E < 0 makes y negative; so y >= 0 forces E >= 0
  virial_terms, energy_scales_critical                                  part 5: the two coefficients, and the critical scaling
  energy_lower_bound, no_negative_energy_below_threshold,
  negative_energy_forces_mass                                           part 5: the threshold, GN as a hypothesis
  sphere_force_balance                                                  part 6: p pi R^2 = sigma 2 pi R t gives sigma = pR/(2t)
  wrinkle_stress_lower_bound, wrinkle_stress_attained,
  zoelly_algebra, zoelly_pressure                                       part 6: the minimisation and the classical constant
-/

namespace Book24Il2

/-! ### Part 2: the toy u' = u^2 -/

theorem toy_quadratic_deriv (c t : ℝ) (h : c - t ≠ 0) :
    HasDerivAt (fun s => (c - s)⁻¹) (((c - t)⁻¹) ^ 2) t := by
  have h1 : HasDerivAt (fun s : ℝ => c - s) (-1) t := by
    simpa using (hasDerivAt_id t).const_sub c
  have h2 := h1.inv h
  refine h2.congr_deriv ?_
  field_simp

theorem toy_quadratic_profile (c t : ℝ) (h : c - t ≠ 0) : (1 / (c - t)) * (c - t) = 1 := by
  field_simp

theorem toy_quadratic_unbounded (c B : ℝ) : ∃ t : ℝ, t < c ∧ B < 1 / (c - t) := by
  have hpos : 0 < |B| + 1 := by positivity
  refine ⟨c - 1 / (|B| + 1), ?_, ?_⟩
  · have : 0 < 1 / (|B| + 1) := by positivity
    linarith
  · have e : c - (c - 1 / (|B| + 1)) = 1 / (|B| + 1) := by ring
    rw [e, one_div_one_div]
    linarith [le_abs_self B]

/-! ### Part 4: the fold x' = s^2 + x^2 -/

theorem fold_tan_deriv (s t : ℝ) (hc : Real.cos (s * t) ≠ 0) :
    HasDerivAt (fun r => s * Real.tan (s * r)) (s ^ 2 + (s * Real.tan (s * t)) ^ 2) t := by
  have h1 : HasDerivAt (fun r : ℝ => s * r) s t := by
    simpa using (hasDerivAt_id t).const_mul s
  have h2 := ((Real.hasDerivAt_tan hc).comp t h1).const_mul s
  refine h2.congr_deriv ?_
  rw [Real.tan_eq_sin_div_cos]
  have hsin := Real.sin_sq_add_cos_sq (s * t)
  field_simp
  first
  | linear_combination (s ^ 2) * hsin
  | linear_combination (-(s ^ 2)) * hsin
  | nlinarith [hsin, sq_nonneg s]

/-! ### Part 5: the virial parabola -/

theorem virial_first_derivative (y0 y1 E t : ℝ) :
    HasDerivAt (fun r => y0 + y1 * r + 8 * E * r ^ 2) (y1 + 16 * E * t) t := by
  have h1 : HasDerivAt (fun r : ℝ => y1 * r) y1 t := by
    simpa using (hasDerivAt_id t).const_mul y1
  have h2 : HasDerivAt (fun r : ℝ => 8 * E * r ^ 2) (8 * E * (2 * t)) t := by
    simpa using (hasDerivAt_pow 2 t).const_mul (8 * E)
  have h3 := (h1.const_add y0).add h2
  refine h3.congr_deriv ?_
  ring

theorem virial_second_derivative (y1 E t : ℝ) :
    HasDerivAt (fun r => y1 + 16 * E * r) (16 * E) t := by
  simpa using ((hasDerivAt_id t).const_mul (16 * E)).const_add y1

theorem virial_collapse (y0 y1 E : ℝ) (hE : E < 0) :
    ∃ t : ℝ, 0 < t ∧ y0 + y1 * t + 8 * E * t ^ 2 < 0 := by
  obtain ⟨a, ha⟩ : ∃ a : ℝ, a = -8 * E := ⟨_, rfl⟩
  have hapos : 0 < a := by rw [ha]; linarith
  obtain ⟨S, hS⟩ : ∃ S : ℝ, S = |y0| + |y1| + 1 := ⟨_, rfl⟩
  have hSpos : 0 < S := by rw [hS]; positivity
  obtain ⟨t, ht⟩ : ∃ t : ℝ, t = S / a + 1 := ⟨_, rfl⟩
  have hdiv : 0 ≤ S / a := by positivity
  have ht1 : 1 ≤ t := by rw [ht]; linarith
  have hat : a * t = S + a := by rw [ht]; field_simp
  refine ⟨t, by linarith, ?_⟩
  have key : 8 * E * t ^ 2 = -(t * (a * t)) := by rw [ha]; ring
  rw [key, hat, hS]
  nlinarith [mul_nonneg (abs_nonneg y0) (sub_nonneg.2 ht1),
    mul_nonneg (sub_nonneg.2 (le_abs_self y1)) (by linarith : (0 : ℝ) ≤ t),
    mul_pos hapos (by linarith : (0 : ℝ) < t), le_abs_self y0]

/-- The logical step of Glassey's argument, with the virial identity as a HYPOTHESIS: if a size `y` that is
    nonnegative for all t >= 0 follows the parabola, then E >= 0. -/
theorem glassey_step (y : ℝ → ℝ) (y0 y1 E : ℝ)
    (hy : ∀ t : ℝ, 0 ≤ t → y t = y0 + y1 * t + 8 * E * t ^ 2)
    (hpos : ∀ t : ℝ, 0 ≤ t → 0 ≤ y t) : 0 ≤ E := by
  by_contra h
  obtain ⟨t, ht, hneg⟩ := virial_collapse y0 y1 E (not_le.1 h)
  have := hpos t ht.le
  rw [hy t ht.le] at this
  linarith

theorem virial_terms (K P : ℝ) : 16 * (K / 2 - P / 6) = 8 * K - (8 / 3) * P := by ring

/-- Algebra only: GIVEN that the kinetic term K and the nonlinear term P both scale like l^2 under the dilation
    (checked numerically on the page, not proved here), the energy scales like l^2. -/
theorem energy_scales_critical (K P l : ℝ) :
    (l ^ 2 * K) / 2 - (l ^ 2 * P) / 6 = l ^ 2 * (K / 2 - P / 6) := by ring

/-! ### The threshold: Gagliardo-Nirenberg as a hypothesis (`hGN`, with r = M / M_Q) -/

theorem energy_lower_bound (K P r : ℝ) (hGN : P / 6 ≤ (1 / 2) * r ^ 2 * K) :
    (1 / 2) * (1 - r ^ 2) * K ≤ K / 2 - P / 6 := by
  nlinarith [hGN]

theorem no_negative_energy_below_threshold (K P M MQ : ℝ) (hK : 0 ≤ K) (hM : 0 ≤ M) (hMQ : 0 < MQ)
    (hle : M ≤ MQ) (hGN : P / 6 ≤ (1 / 2) * (M / MQ) ^ 2 * K) : 0 ≤ K / 2 - P / 6 := by
  have hr0 : 0 ≤ M / MQ := div_nonneg hM hMQ.le
  have hr1 : M / MQ ≤ 1 := (div_le_one hMQ).2 hle
  have hr2 : (M / MQ) ^ 2 ≤ 1 := by nlinarith
  nlinarith [energy_lower_bound K P (M / MQ) hGN, mul_nonneg (sub_nonneg.2 hr2) hK]

theorem negative_energy_forces_mass (K P M MQ : ℝ) (hK : 0 ≤ K) (hM : 0 ≤ M) (hMQ : 0 < MQ)
    (hGN : P / 6 ≤ (1 / 2) * (M / MQ) ^ 2 * K) (hE : K / 2 - P / 6 < 0) : MQ < M := by
  by_contra h
  exact absurd (no_negative_energy_below_threshold K P M MQ hK hM hMQ (not_lt.1 h) hGN) (not_le.2 hE)

/-! ### Part 6: the pressure hull -/

theorem sphere_force_balance (p σ R t : ℝ) (hR : 0 < R) (ht : 0 < t)
    (h : p * (Real.pi * R ^ 2) = σ * (2 * Real.pi * R * t)) : σ = p * R / (2 * t) := by
  have hpi : 0 < Real.pi := Real.pi_pos
  have h2 : (Real.pi * R) * (p * R) = (Real.pi * R) * (σ * (2 * t)) := by linear_combination h
  have h3 := mul_left_cancel₀ (by positivity : Real.pi * R ≠ 0) h2
  field_simp
  linarith

/-- The stress needed for a wrinkle of squared wavenumber s is D s / t + E / (R^2 s); its square is at least 4 D E / (t R^2). -/
theorem wrinkle_stress_lower_bound (D E t R s : ℝ) (hD : 0 < D) (hE : 0 < E) (ht : 0 < t) (hR : 0 < R)
    (hs : 0 < s) :
    4 * D * E / (t * R ^ 2) ≤ (D * s / t + E / (R ^ 2 * s)) ^ 2 := by
  have ha : 0 < D * s / t := by positivity
  have hb : 0 < E / (R ^ 2 * s) := by positivity
  have hab : (D * s / t) * (E / (R ^ 2 * s)) = D * E / (t * R ^ 2) := by field_simp
  have h4 : 4 * D * E / (t * R ^ 2) = 4 * (D * E / (t * R ^ 2)) := by ring
  nlinarith [sq_nonneg (D * s / t - E / (R ^ 2 * s)), hab, h4]

theorem wrinkle_stress_attained (D E t R s : ℝ) (hD : 0 < D) (hE : 0 < E) (ht : 0 < t) (hR : 0 < R)
    (hs : 0 < s) (hs2 : s ^ 2 = E * t / (D * R ^ 2)) : D * s / t = E / (R ^ 2 * s) := by
  have h : D * R ^ 2 * s ^ 2 = E * t := by rw [hs2]; field_simp
  field_simp
  first
  | linear_combination h
  | nlinarith [h]

theorem zoelly_algebra (E ν t R : ℝ) (hE : 0 < E) (ht : 0 < t) (hR : 0 < R) (hν : ν ^ 2 < 1) :
    4 * (E * t ^ 3 / (12 * (1 - ν ^ 2))) * E / (t * R ^ 2) = (E * t / R) ^ 2 / (3 * (1 - ν ^ 2)) := by
  have h : 1 - ν ^ 2 ≠ 0 := ne_of_gt (by linarith)
  field_simp
  ring

theorem zoelly_pressure (E ν t R σ p : ℝ) (hE : 0 < E) (ht : 0 < t) (hR : 0 < R) (hν : ν ^ 2 < 1)
    (hσ : σ = E * t / (R * Real.sqrt (3 * (1 - ν ^ 2)))) (hp : p = 2 * t * σ / R) :
    p = 2 * E / Real.sqrt (3 * (1 - ν ^ 2)) * (t / R) ^ 2 := by
  have hq : Real.sqrt (3 * (1 - ν ^ 2)) ≠ 0 := (Real.sqrt_pos.2 (by nlinarith)).ne'
  subst hσ
  subst hp
  field_simp
  try ring

end Book24Il2

#print axioms Book24Il2.toy_quadratic_deriv
#print axioms Book24Il2.toy_quadratic_profile
#print axioms Book24Il2.toy_quadratic_unbounded
#print axioms Book24Il2.fold_tan_deriv
#print axioms Book24Il2.virial_first_derivative
#print axioms Book24Il2.virial_second_derivative
#print axioms Book24Il2.virial_collapse
#print axioms Book24Il2.glassey_step
#print axioms Book24Il2.virial_terms
#print axioms Book24Il2.energy_scales_critical
#print axioms Book24Il2.energy_lower_bound
#print axioms Book24Il2.no_negative_energy_below_threshold
#print axioms Book24Il2.negative_energy_forces_mass
#print axioms Book24Il2.sphere_force_balance
#print axioms Book24Il2.wrinkle_stress_lower_bound
#print axioms Book24Il2.wrinkle_stress_attained
#print axioms Book24Il2.zoelly_algebra
#print axioms Book24Il2.zoelly_pressure
