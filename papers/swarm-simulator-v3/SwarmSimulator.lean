/-
  SwarmSimulator.lean  --  Version 3
  Pablo Nogueira Grossi, G6 LLC.  (V3 corrections and formal checks added with Claude, 2026-09-29)

  What this file proves about the swarm map of Definitions 3.1-3.4, with the three
  coordinates (I, C, M) and the diffusion coordinate F treated separately:

    step_nrm_le          size of the state after one step, on a ball of radius R
    orbit_nrm_le         geometric decay  ||X_n|| <= rho^n ||X_0||, rho = max(a, a c R, m)
    paper_bound          the printed bound  ||X_n|| <= L^n ||X_0||, L = a + a c + m,
                         for starts with ||X_0|| <= 1   (a corrected Theorem 5.3)
    step_lipschitz_ball  a Lipschitz constant on the ball, lambda = max(a (1 + c R), m)
    fixed_point_zero     the only fixed point in the ball is 0            (a corrected Theorem 5.2)
    no_global_lipschitz  there is NO global Lipschitz constant            (why Theorem 5.1 needs a ball)
    printed_bound_fails  the printed bound fails from (100, 10, 1)
    diffuse_unbounded    F_t = 1 + alpha t has no upper bound             (no fixed point in F)
    two_clusters         two parameter sets satisfying the ball condition share the fixed point 0
    default_radius       the default parameters contract exactly for R < 3.5096..., numerically

  Coordinates:  a = f_types f_agents (1 - eta),  c = 1/(1 + D),  m = (1 + beta reuse) avg_quality.
    I' = a I,   C' = C (a I) c,   M' = m M.
-/
import Mathlib

namespace SwarmSimulatorV3

structure S where
  I : ℝ
  C : ℝ
  M : ℝ

def nrm (X : S) : ℝ := |X.I| + |X.C| + |X.M|
def sub (X Y : S) : S := ⟨X.I - Y.I, X.C - Y.C, X.M - Y.M⟩

structure P where
  a : ℝ
  c : ℝ
  m : ℝ
  ha : 0 ≤ a
  hc : 0 ≤ c
  hm : 0 ≤ m

/-- One step of Definitions 3.1-3.3 (the diffusion coordinate F is handled separately). -/
def step (p : P) (X : S) : S := ⟨p.a * X.I, X.C * (p.a * X.I) * p.c, p.m * X.M⟩

def orbit (p : P) (X : S) (n : ℕ) : S := (step p)^[n] X

/-- The three constants come from the paper's parameters. -/
noncomputable def ofParams (ft fa eta D beta reuse q : ℝ) (h1 : 0 ≤ ft * fa * (1 - eta)) (hD : 0 ≤ D)
    (h3 : 0 ≤ (1 + beta * reuse) * q) : P :=
  ⟨ft * fa * (1 - eta), (1 + D)⁻¹, (1 + beta * reuse) * q, h1,
    inv_nonneg.mpr (by linarith), h3⟩

theorem nrm_nonneg (X : S) : 0 ≤ nrm X := by
  unfold nrm; positivity

theorem nrm_eq_zero {X : S} (h : nrm X = 0) : X = ⟨0, 0, 0⟩ := by
  unfold nrm at h
  have h1 := abs_nonneg X.I
  have h2 := abs_nonneg X.C
  have h3 := abs_nonneg X.M
  have e1 : |X.I| = 0 := by linarith
  have e2 : |X.C| = 0 := by linarith
  have e3 : |X.M| = 0 := by linarith
  cases X
  simp_all

/-- The contraction factor on the ball of radius R. -/
noncomputable def rho (p : P) (R : ℝ) : ℝ := max p.a (max (p.a * p.c * R) p.m)

theorem step_nrm_le (p : P) (X : S) (R : ℝ) (hR : nrm X ≤ R) :
    nrm (step p X) ≤ rho p R * nrm X := by
  have ha := p.ha
  have hc := p.hc
  have hm := p.hm
  have hI : |X.I| ≤ R := by
    have := abs_nonneg X.C; have := abs_nonneg X.M
    unfold nrm at hR; linarith
  have e : nrm (step p X) = p.a * |X.I| + |X.C| * (p.a * |X.I| * p.c) + p.m * |X.M| := by
    simp only [nrm, step, abs_mul, abs_of_nonneg ha, abs_of_nonneg hc, abs_of_nonneg hm]
    ring
  have r1 : p.a ≤ rho p R := le_max_left _ _
  have r2 : p.a * p.c * R ≤ rho p R := le_trans (le_max_left _ _) (le_max_right _ _)
  have r3 : p.m ≤ rho p R := le_trans (le_max_right _ _) (le_max_right _ _)
  have h1 : p.a * |X.I| ≤ rho p R * |X.I| := mul_le_mul_of_nonneg_right r1 (abs_nonneg _)
  have h2' : p.a * |X.I| * p.c ≤ p.a * R * p.c := by gcongr
  have h2 : |X.C| * (p.a * |X.I| * p.c) ≤ rho p R * |X.C| := by
    calc |X.C| * (p.a * |X.I| * p.c) ≤ |X.C| * (p.a * R * p.c) :=
          mul_le_mul_of_nonneg_left h2' (abs_nonneg _)
      _ = |X.C| * (p.a * p.c * R) := by ring
      _ ≤ |X.C| * rho p R := mul_le_mul_of_nonneg_left r2 (abs_nonneg _)
      _ = rho p R * |X.C| := by ring
  have h3 : p.m * |X.M| ≤ rho p R * |X.M| := mul_le_mul_of_nonneg_right r3 (abs_nonneg _)
  rw [e]
  calc p.a * |X.I| + |X.C| * (p.a * |X.I| * p.c) + p.m * |X.M|
      ≤ rho p R * |X.I| + rho p R * |X.C| + rho p R * |X.M| := by linarith
    _ = rho p R * nrm X := by unfold nrm; ring

theorem rho_nonneg (p : P) (R : ℝ) : 0 ≤ rho p R :=
  le_trans p.ha (le_max_left _ _)

/-- Geometric decay on the ball, when rho <= 1. -/
theorem orbit_nrm_le (p : P) (X : S) (R : ℝ) (hX : nrm X ≤ R) (hρ : rho p R ≤ 1) :
    ∀ n : ℕ, nrm (orbit p X n) ≤ rho p R ^ n * nrm X := by
  intro n
  induction n with
  | zero => simp [orbit]
  | succ k ih =>
    have hr0 := rho_nonneg p R
    have hk : rho p R ^ k ≤ 1 := pow_le_one₀ hr0 hρ
    have hin : nrm (orbit p X k) ≤ R := by
      calc nrm (orbit p X k) ≤ rho p R ^ k * nrm X := ih
        _ ≤ 1 * nrm X := mul_le_mul_of_nonneg_right hk (nrm_nonneg X)
        _ = nrm X := one_mul _
        _ ≤ R := hX
    have hs : orbit p X (k + 1) = step p (orbit p X k) := by
      unfold orbit; exact Function.iterate_succ_apply' _ _ _
    rw [hs]
    calc nrm (step p (orbit p X k)) ≤ rho p R * nrm (orbit p X k) := step_nrm_le p _ R hin
      _ ≤ rho p R * (rho p R ^ k * nrm X) := mul_le_mul_of_nonneg_left ih hr0
      _ = rho p R ^ (k + 1) * nrm X := by ring

/-- A corrected Theorem 5.3: the printed bound with L = a + a c + m holds for starts with ||X_0|| <= 1. -/
theorem paper_bound (p : P) (hL : p.a + p.a * p.c + p.m < 1) (X : S) (hX : nrm X ≤ 1) (n : ℕ) :
    nrm (orbit p X n) ≤ (p.a + p.a * p.c + p.m) ^ n * nrm X := by
  have ha := p.ha; have hc := p.hc; have hm := p.hm
  have hac : 0 ≤ p.a * p.c := mul_nonneg ha hc
  have hρL : rho p 1 ≤ p.a + p.a * p.c + p.m := by
    unfold rho
    refine max_le (by linarith) (max_le (by linarith) (by linarith))
  have h1 : rho p 1 ≤ 1 := by linarith
  have := orbit_nrm_le p X 1 hX h1 n
  calc nrm (orbit p X n) ≤ rho p 1 ^ n * nrm X := this
    _ ≤ (p.a + p.a * p.c + p.m) ^ n * nrm X :=
        mul_le_mul_of_nonneg_right (pow_le_pow_left₀ (rho_nonneg p 1) hρL n) (nrm_nonneg X)

/-- Lipschitz constant on the ball: the C-update multiplies two state variables, so the constant
    depends on the radius R. -/
theorem step_lipschitz_ball (p : P) (X Y : S) (R : ℝ)
    (hXC : |X.C| ≤ R) (hYI : |Y.I| ≤ R) :
    nrm (sub (step p X) (step p Y)) ≤ max (p.a * (1 + p.c * R)) p.m * nrm (sub X Y) := by
  have ha := p.ha; have hc := p.hc; have hm := p.hm
  have hR : 0 ≤ R := le_trans (abs_nonneg _) hXC
  have key : |X.C * X.I - Y.C * Y.I| ≤ R * |X.I - Y.I| + R * |X.C - Y.C| := by
    have e : X.C * X.I - Y.C * Y.I = X.C * (X.I - Y.I) + Y.I * (X.C - Y.C) := by ring
    rw [e]
    calc |X.C * (X.I - Y.I) + Y.I * (X.C - Y.C)|
        ≤ |X.C * (X.I - Y.I)| + |Y.I * (X.C - Y.C)| := abs_add_le _ _
      _ = |X.C| * |X.I - Y.I| + |Y.I| * |X.C - Y.C| := by rw [abs_mul, abs_mul]
      _ ≤ R * |X.I - Y.I| + R * |X.C - Y.C| := by
          gcongr
  have e : nrm (sub (step p X) (step p Y)) =
      p.a * |X.I - Y.I| + p.a * p.c * |X.C * X.I - Y.C * Y.I| + p.m * |X.M - Y.M| := by
    have e1 : p.a * X.I - p.a * Y.I = p.a * (X.I - Y.I) := by ring
    have e2 : X.C * (p.a * X.I) * p.c - Y.C * (p.a * Y.I) * p.c
        = (p.a * p.c) * (X.C * X.I - Y.C * Y.I) := by ring
    have e3 : p.m * X.M - p.m * Y.M = p.m * (X.M - Y.M) := by ring
    simp only [nrm, sub, step]
    rw [e1, e2, e3]
    simp only [abs_mul, abs_of_nonneg ha, abs_of_nonneg hc, abs_of_nonneg hm]
  rw [e]
  set lam := max (p.a * (1 + p.c * R)) p.m with hlam
  have l1 : p.a * (1 + p.c * R) ≤ lam := le_max_left _ _
  have l2 : p.m ≤ lam := le_max_right _ _
  have hacR : p.a * p.c * R ≤ p.a * (1 + p.c * R) := by
    have : 0 ≤ p.a := ha
    nlinarith [mul_nonneg ha hc, mul_nonneg (mul_nonneg ha hc) hR]
  have t1 : p.a * p.c * |X.C * X.I - Y.C * Y.I|
      ≤ p.a * p.c * (R * |X.I - Y.I| + R * |X.C - Y.C|) :=
    mul_le_mul_of_nonneg_left key (mul_nonneg ha hc)
  have d1 := abs_nonneg (X.I - Y.I)
  have d2 := abs_nonneg (X.C - Y.C)
  have d3 := abs_nonneg (X.M - Y.M)
  have u1 : (p.a + p.a * p.c * R) * |X.I - Y.I| ≤ lam * |X.I - Y.I| := by
    apply mul_le_mul_of_nonneg_right _ d1
    nlinarith
  have u2 : (p.a * p.c * R) * |X.C - Y.C| ≤ lam * |X.C - Y.C| := by
    apply mul_le_mul_of_nonneg_right _ d2
    linarith
  have u3 : p.m * |X.M - Y.M| ≤ lam * |X.M - Y.M| := mul_le_mul_of_nonneg_right l2 d3
  have : nrm (sub X Y) = |X.I - Y.I| + |X.C - Y.C| + |X.M - Y.M| := rfl
  rw [this]
  nlinarith [t1, u1, u2, u3]

/-- A fixed point in the ball is 0 (a corrected Theorem 5.2). -/
theorem step_zero (p : P) : step p ⟨0, 0, 0⟩ = ⟨0, 0, 0⟩ := by
  simp [step]

theorem fixed_point_zero (p : P) (R : ℝ) (hρ : rho p R < 1) (X : S) (hX : nrm X ≤ R)
    (hfix : step p X = X) : X = ⟨0, 0, 0⟩ := by
  have h := step_nrm_le p X R hX
  rw [hfix] at h
  have h0 := nrm_nonneg X
  have : nrm X = 0 := by nlinarith
  exact nrm_eq_zero this

/-- Two clusters that each satisfy the ball condition have the same fixed point, 0. -/
theorem two_clusters (p q : P) (R : ℝ) (hp : rho p R < 1) (hq : rho q R < 1)
    (X Y : S) (hX : nrm X ≤ R) (hY : nrm Y ≤ R) (hfx : step p X = X) (hfy : step q Y = Y) :
    X = Y := by
  rw [fixed_point_zero p R hp X hX hfx, fixed_point_zero q R hq Y hY hfy]

/-- No global Lipschitz constant: the C-update multiplies two state variables. -/
theorem no_global_lipschitz (p : P) (ha : 0 < p.a) (hc : 0 < p.c) (K : ℝ) :
    ∃ X Y : S, K * nrm (sub X Y) < nrm (sub (step p X) (step p Y)) := by
  have hac : 0 < p.a * p.c := mul_pos ha hc
  refine ⟨⟨1, (|K| + 1) / (p.a * p.c), 0⟩, ⟨0, (|K| + 1) / (p.a * p.c), 0⟩, ?_⟩
  have e1 : nrm (sub ⟨1, (|K| + 1) / (p.a * p.c), 0⟩ ⟨0, (|K| + 1) / (p.a * p.c), 0⟩) = 1 := by
    simp [nrm, sub]
  have e2 : nrm (sub (step p ⟨1, (|K| + 1) / (p.a * p.c), 0⟩)
      (step p ⟨0, (|K| + 1) / (p.a * p.c), 0⟩)) = p.a + (|K| + 1) := by
    have : (|K| + 1) / (p.a * p.c) * (p.a * 1) * p.c = |K| + 1 := by
      field_simp
    simp only [nrm, sub, step]
    rw [show p.a * 1 - p.a * 0 = p.a by ring, show p.m * 0 - p.m * 0 = 0 by ring]
    rw [show (|K| + 1) / (p.a * p.c) * (p.a * 1) * p.c - (|K| + 1) / (p.a * p.c) * (p.a * 0) * p.c
        = |K| + 1 by rw [this]; ring]
    rw [abs_of_pos ha, abs_of_pos (by positivity)]
    simp
  rw [e1, e2]
  have := le_abs_self K
  linarith

/-- The diffusion coordinate F_t = 1 + alpha t has no upper bound, so there is no fixed point in F. -/
theorem diffuse_unbounded (α : ℝ) (hα : 0 < α) (B : ℝ) : ∃ t : ℝ, B < 1 + α * t := by
  refine ⟨(|B| + 1) / α, ?_⟩
  have : α * ((|B| + 1) / α) = |B| + 1 := by field_simp
  rw [this]
  have := le_abs_self B
  linarith

/-! ### The default parameters, exactly:  a = 52/125, c = 2/5, m = 231/1000 -/

/-- The printed bound fails from (100, 10, 1): one step gives size 208.231 against L * 111 = 90.2874. -/
theorem printed_bound_fails :
    let a : ℝ := 52 / 125
    let c : ℝ := 2 / 5
    let m : ℝ := 231 / 1000
    let p : P := ⟨a, c, m, by norm_num, by norm_num, by norm_num⟩
    a + a * c + m < 1 ∧
      (a + a * c + m) * nrm ⟨100, 10, 1⟩ < nrm (step p ⟨100, 10, 1⟩) := by
  intro a c m p
  refine ⟨by norm_num, ?_⟩
  simp only [nrm, step, p, a, c, m]
  norm_num [abs_of_nonneg, abs_of_pos]

/-- With the default parameters the Lipschitz constant a (1 + c R) on the ball stays below 1
    for R = 7/2, and is above 1 for R = 4. So contraction holds on a ball of radius about 3.51, not on all of R^3. -/
theorem default_radius :
    (52 / 125 : ℝ) * (1 + (2 / 5) * (7 / 2)) < 1 ∧ 1 < (52 / 125 : ℝ) * (1 + (2 / 5) * 4) := by
  norm_num

end SwarmSimulatorV3

#print axioms SwarmSimulatorV3.orbit_nrm_le
#print axioms SwarmSimulatorV3.paper_bound
#print axioms SwarmSimulatorV3.step_lipschitz_ball
#print axioms SwarmSimulatorV3.fixed_point_zero
#print axioms SwarmSimulatorV3.two_clusters
#print axioms SwarmSimulatorV3.no_global_lipschitz
#print axioms SwarmSimulatorV3.diffuse_unbounded
#print axioms SwarmSimulatorV3.printed_bound_fails
#print axioms SwarmSimulatorV3.default_radius
