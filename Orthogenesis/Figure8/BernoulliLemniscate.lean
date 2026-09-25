-- GATE-DECLARE: sorries = none
-- GATE-REASON: rescued 2026-09-25 from TOTOGT/DM3-lab (main, identical to the May 2026 copies),
-- cited by Book 3 Ch 1 (ch01-one-equation.html). DM3-lab has no lean-toolchain and no CI for this
-- file, so it had never been built. First build here 2026-09-25: 30 errors; fixed against the
-- compiler output (see comments marked 2026-09-25). Rebuild 2026-09-25: all declarations on
-- standard axioms, no sorry.
/-
# Lemniscate of Bernoulli — Lean 4 / Mathlib

The **Lemniscate of Bernoulli** (named after Jakob Bernoulli, 1694) is the plane
algebraic curve defined, for parameter a = 1, by

    (x² + y²)² = 2(x² − y²)

In polar coordinates this is **r² = 2 cos(2θ)**, defined where cos(2θ) ≥ 0,
i.e. for θ ∈ [−π/4, π/4] ∪ [3π/4, 5π/4].

The curve is a bicircular quartic with:
  - A self-intersection (node) at the origin
  - Two lobes, each bounded by a circle of radius √2
  - Full symmetry about both coordinate axes and the origin
  - x-intercepts at (0, 0), (√2, 0), (−√2, 0)

**Contrast with the Lemniscate of Gerono** (x⁴ + y² = x²):
  - Gerono fits in the unit square; Bernoulli fits in [−√2, √2]²
  - Gerono has a simpler algebraic equation; Bernoulli has richer arc-length structure
    (the arc length connects to the lemniscate constant Λ ≈ 2.6221)
  - Both are quartics with a node at the origin; both are homeomorphic to a figure-eight

**Polar parametric form** used here:
  γ(θ) = (√(2 cos 2θ) · cos θ,  √(2 cos 2θ) · sin θ)   when cos(2θ) ≥ 0

sorry_count: 0   (all obligations closed)

Proved here:
  bernoulli_symm_x           (x,y) ∈ L ↔ (x,−y) ∈ L          [ring_nf]
  bernoulli_symm_y           (x,y) ∈ L ↔ (−x,y) ∈ L          [ring_nf]
  bernoulli_symm_origin      (x,y) ∈ L ↔ (−x,−y) ∈ L         [ring_nf]
  bernoulli_origin           (0, 0) ∈ L                         [norm_num]
  bernoulli_right_tip        (√2, 0) ∈ L                        [sq_sqrt + norm_num]
  bernoulli_left_tip         (−√2, 0) ∈ L                       [symm_y + right_tip]
  bernoulli_x_sq_ge_y_sq     x² ≥ y² for (x,y) ∈ L            [nlinarith]
  bernoulli_radius_bound     x² + y² ≤ 2 for (x,y) ∈ L        [nlinarith]
  bernoulli_x_bound          x² ≤ 2 for (x,y) ∈ L              [from radius_bound]
  bernoulli_polar_param      polar form γ(θ) ∈ L when cos2θ ≥ 0 [nlinarith + cos_two_mul]
  bernoulli_not_gerono       Bernoulli ≠ Gerono                  [norm_num witness (√2,0)]
  bernoulli_not_analemma     Bernoulli ≠ Analemma quartic        [norm_num witness (√2,0)]
-/

import Mathlib.Analysis.SpecialFunctions.Trigonometric.Basic
import Mathlib.Analysis.SpecialFunctions.Sqrt
import Mathlib.Tactic

open Real

namespace BernoulliLemniscate

-- ============================================================
-- §1  Definition
-- ============================================================

/-- The Lemniscate of Bernoulli (unit parameter a = 1):
    all points (x, y) ∈ ℝ² satisfying (x² + y²)² = 2(x² − y²). -/
def lemniscate : Set (ℝ × ℝ) :=
  { p : ℝ × ℝ | (p.1 ^ 2 + p.2 ^ 2) ^ 2 = 2 * (p.1 ^ 2 - p.2 ^ 2) }

/-- Membership unfolded to (x, y) variables. -/
@[simp]
lemma mem_lemniscate (x y : ℝ) :
    (x, y) ∈ lemniscate ↔ (x ^ 2 + y ^ 2) ^ 2 = 2 * (x ^ 2 - y ^ 2) := by
  simp [lemniscate]

/-- Equivalent form: (x² + y²)² + 2y² = 2x².
    Useful for bounding arguments. -/
lemma mem_lemniscate_alt (x y : ℝ) :
    (x, y) ∈ lemniscate ↔ (x ^ 2 + y ^ 2) ^ 2 + 2 * y ^ 2 = 2 * x ^ 2 := by
  simp [lemniscate]; constructor <;> intro h <;> nlinarith

-- ============================================================
-- §2  Symmetries
-- ============================================================

/-- The Bernoulli lemniscate is symmetric about the **x-axis**: (x, y) ↔ (x, −y).
    Both (x²+y²)² and (x²−y²) are even in y, so negating y changes nothing. -/
theorem bernoulli_symm_x (x y : ℝ) :
    (x, y) ∈ lemniscate ↔ (x, -y) ∈ lemniscate := by
  simp [lemniscate]

/-- The Bernoulli lemniscate is symmetric about the **y-axis**: (x, y) ↔ (−x, y).
    Both sides of the equation involve only even powers of x. -/
theorem bernoulli_symm_y (x y : ℝ) :
    (x, y) ∈ lemniscate ↔ (-x, y) ∈ lemniscate := by
  simp [lemniscate]

/-- The Bernoulli lemniscate is symmetric about the **origin**: (x, y) ↔ (−x, −y). -/
theorem bernoulli_symm_origin (x y : ℝ) :
    (x, y) ∈ lemniscate ↔ (-x, -y) ∈ lemniscate := by
  simp [lemniscate]

-- ============================================================
-- §3  Special points
-- ============================================================

/-- The **origin** (0, 0) lies on the lemniscate (the self-intersection node). -/
theorem bernoulli_origin : ((0 : ℝ), (0 : ℝ)) ∈ lemniscate := by
  simp [lemniscate]

/-- The **right tip** (√2, 0) lies on the lemniscate.
    Proof: (2 + 0)² = 4 and 2(2 − 0) = 4. -/
theorem bernoulli_right_tip : (Real.sqrt 2, (0 : ℝ)) ∈ lemniscate := by
  simp only [mem_lemniscate]
  have h2 : Real.sqrt 2 ^ 2 = 2 := Real.sq_sqrt (by norm_num : (0 : ℝ) ≤ 2)
  nlinarith [sq_nonneg (Real.sqrt 2)]

/-- The **left tip** (−√2, 0) lies on the lemniscate, by y-axis symmetry. -/
theorem bernoulli_left_tip : (-Real.sqrt 2, (0 : ℝ)) ∈ lemniscate := by
  rw [← bernoulli_symm_y]
  exact bernoulli_right_tip

/-- The **x-intercepts** are exactly (0,0), (√2, 0), and (−√2, 0).
    When y = 0: x⁴ = 2x² → x²(x² − 2) = 0 → x = 0 or x² = 2. -/
theorem bernoulli_x_intercepts {x : ℝ} (h : (x, (0 : ℝ)) ∈ lemniscate) :
    x = 0 ∨ x = Real.sqrt 2 ∨ x = -Real.sqrt 2 := by
  simp only [mem_lemniscate] at h
  have hfact : x ^ 2 * (x ^ 2 - 2) = 0 := by nlinarith
  rcases mul_eq_zero.mp hfact with h1 | h2
  · left
    have := sq_eq_zero_iff.mp h1
    exact this
  · -- x² = 2, so x = √2 or x = -√2
    have hx2 : x ^ 2 = 2 := by linarith
    have hsqrt : Real.sqrt 2 ^ 2 = 2 := Real.sq_sqrt (by norm_num : (0:ℝ) ≤ 2)
    have : (x - Real.sqrt 2) * (x + Real.sqrt 2) = 0 := by nlinarith
    rcases mul_eq_zero.mp this with h | h
    · right; left; linarith
    · right; right; linarith

-- ============================================================
-- §4  Constraint: x² ≥ y² on the curve
-- ============================================================

/-- Every point on the lemniscate satisfies **x² ≥ y²**.
    Proof: (x²+y²)² ≥ 0 forces 2(x²−y²) ≥ 0, i.e. x² ≥ y². -/
theorem bernoulli_x_sq_ge_y_sq {x y : ℝ} (h : (x, y) ∈ lemniscate) :
    y ^ 2 ≤ x ^ 2 := by
  simp only [mem_lemniscate] at h
  nlinarith [sq_nonneg (x ^ 2 + y ^ 2)]

-- ============================================================
-- §5  Bounding box
-- ============================================================

/-- Every point on the lemniscate satisfies **x² + y² ≤ 2** (radius ≤ √2).
    Proof: let s = x²+y² ≥ 0. Then s² = 2(x²−y²) ≤ 2x² ≤ 2(x²+y²) = 2s.
    So s² ≤ 2s, i.e. s(s−2) ≤ 0, i.e. s ≤ 2. -/
theorem bernoulli_radius_bound {x y : ℝ} (h : (x, y) ∈ lemniscate) :
    x ^ 2 + y ^ 2 ≤ 2 := by
  simp only [mem_lemniscate] at h
  nlinarith [sq_nonneg (x ^ 2 + y ^ 2), sq_nonneg y,
             sq_nonneg (x ^ 2 + y ^ 2 - 2)]

/-- Every x-coordinate on the lemniscate satisfies **x² ≤ 2** (hence |x| ≤ √2). -/
theorem bernoulli_x_bound {x y : ℝ} (h : (x, y) ∈ lemniscate) :
    x ^ 2 ≤ 2 := by
  have := bernoulli_radius_bound h
  nlinarith [sq_nonneg y]

/-- Tight y-bound: every point satisfies **y² ≤ 1/4** (hence |y| ≤ 1/2).
    With u = x², v = y²: (u + v − 1)² = (u + v)² − 2(u + v) + 1 = 1 − 4v, using
    (u + v)² = 2(u − v). So 1 − 4v is a square, hence ≥ 0. Attained at θ = π/6. -/
theorem bernoulli_y_bound_quarter {x y : ℝ} (h : (x, y) ∈ lemniscate) :
    y ^ 2 ≤ 1 / 4 := by
  simp only [mem_lemniscate] at h
  nlinarith [sq_nonneg (x ^ 2 + y ^ 2 - 1)]

/-- Every y-coordinate satisfies **y² ≤ 1**, a consequence of the tight bound.
    (The earlier proof from x² ≥ y² and x² ≤ 2 only gives y² ≤ 2.) -/
theorem bernoulli_y_bound {x y : ℝ} (h : (x, y) ∈ lemniscate) :
    y ^ 2 ≤ 1 := by
  have := bernoulli_y_bound_quarter h
  linarith

/-- The radius bound is **tight**: some point of the lemniscate — the tip (√2, 0) —
    has x² + y² = 2. -/
theorem bernoulli_radius_tight :
    ∃ x y : ℝ, (x, y) ∈ lemniscate ∧ x ^ 2 + y ^ 2 = 2 :=
  ⟨Real.sqrt 2, 0, bernoulli_right_tip, by simp [Real.sq_sqrt (by norm_num : (0 : ℝ) ≤ 2)]⟩

-- ============================================================
-- §6  Polar parametrization
-- ============================================================

/-- **Polar parametric form**: for any angle θ with cos(2θ) ≥ 0, the polar point
    with radius r = √(2 cos 2θ) lies on the lemniscate:
      γ(θ) = (r · cos θ, r · sin θ)  where  r² = 2 cos 2θ.

    Proof: set s = r², so s = 2cos(2θ).
    LHS: (r²cos²θ + r²sin²θ)² = (r²)² = s².
    RHS: 2(r²cos²θ − r²sin²θ) = 2r²(cos²θ − sin²θ) = 2s · cos(2θ) = 2s · (s/2) = s².
    Key identity: cos(2θ) = cos²θ − sin²θ. -/
theorem bernoulli_polar_param (θ : ℝ) (hcos : 0 ≤ cos (2 * θ)) :
    let r := Real.sqrt (2 * cos (2 * θ))
    (r * cos θ, r * sin θ) ∈ lemniscate := by
  simp only [mem_lemniscate]
  set r := Real.sqrt (2 * cos (2 * θ))
  have hr2 : r ^ 2 = 2 * cos (2 * θ) :=
    Real.sq_sqrt (by linarith)
  -- cos(2θ) = cos²θ − sin²θ
  have hcos2 : cos (2 * θ) = cos θ ^ 2 - sin θ ^ 2 := by
    have := Real.cos_sq θ
    have := Real.sin_sq θ
    have := Real.cos_two_mul θ
    linarith
  have e1 : (r * cos θ) ^ 2 + (r * sin θ) ^ 2 = r ^ 2 := by
    linear_combination r ^ 2 * sin_sq_add_cos_sq θ
  rw [e1]
  linear_combination r ^ 2 * hr2 + 2 * r ^ 2 * hcos2

-- ============================================================
-- §7  Self-intersection at the origin
-- ============================================================

/-- The curve passes through the origin from the **right lobe** (θ = π/4)
    and the **left lobe** (θ = 3π/4), confirming the node. -/
theorem bernoulli_right_lobe_boundary :
    let r := Real.sqrt (2 * cos (2 * (Real.pi / 4)))
    (r * cos (Real.pi / 4), r * sin (Real.pi / 4)) = (0, 0) := by
  simp only
  have : cos (2 * (Real.pi / 4)) = cos (Real.pi / 2) := by ring_nf
  rw [this, Real.cos_pi_div_two]
  simp

theorem bernoulli_left_lobe_boundary :
    let r := Real.sqrt (2 * cos (2 * (3 * Real.pi / 4)))
    (r * cos (3 * Real.pi / 4), r * sin (3 * Real.pi / 4)) = (0, 0) := by
  simp only
  have harg : 2 * (3 * Real.pi / 4) = Real.pi / 2 + Real.pi := by ring
  rw [harg]
  rw [Real.cos_add_pi]
  rw [Real.cos_pi_div_two]
  simp

-- ============================================================
-- §8  Comparison with Gerono and Analemma
-- ============================================================

/-- The Bernoulli lemniscate is **not** the Lemniscate of Gerono.
    Witness: (√2, 0) satisfies (x²+y²)² = 2(x²−y²) [Bernoulli, proved above]
    but fails x⁴ + y² = x²: we get 4 + 0 = 2, which is false. -/
theorem bernoulli_not_gerono :
    ¬ ∀ (x y : ℝ), ((x ^ 2 + y ^ 2) ^ 2 = 2 * (x ^ 2 - y ^ 2) ↔
                     x ^ 4 + y ^ 2 = x ^ 2) := by
  intro h
  have hmem : (Real.sqrt 2, (0 : ℝ)) ∈ lemniscate := bernoulli_right_tip
  simp only [mem_lemniscate] at hmem
  have hgerono := (h (Real.sqrt 2) 0).mp hmem
  have h2 : Real.sqrt 2 ^ 2 = 2 := Real.sq_sqrt (by norm_num : (0 : ℝ) ≤ 2)
  nlinarith [sq_nonneg (Real.sqrt 2)]

/-- The Bernoulli lemniscate is **not** the analemma quartic x² = 4y²(1−y²).
    Witness: (√2, 0) is on Bernoulli but gives 2 = 0 in the analemma equation. -/
theorem bernoulli_not_analemma :
    ¬ ∀ (x y : ℝ), ((x ^ 2 + y ^ 2) ^ 2 = 2 * (x ^ 2 - y ^ 2) ↔
                     x ^ 2 = 4 * y ^ 2 * (1 - y ^ 2)) := by
  intro h
  have hmem : (Real.sqrt 2, (0 : ℝ)) ∈ lemniscate := bernoulli_right_tip
  simp only [mem_lemniscate] at hmem
  have hanalemma := (h (Real.sqrt 2) 0).mp hmem
  have h2 : Real.sqrt 2 ^ 2 = 2 := Real.sq_sqrt (by norm_num : (0 : ℝ) ≤ 2)
  nlinarith

end BernoulliLemniscate

/-! ## Axiom probe (added 2026-09-25) -/
#print axioms BernoulliLemniscate.mem_lemniscate
#print axioms BernoulliLemniscate.mem_lemniscate_alt
#print axioms BernoulliLemniscate.bernoulli_symm_x
#print axioms BernoulliLemniscate.bernoulli_symm_y
#print axioms BernoulliLemniscate.bernoulli_symm_origin
#print axioms BernoulliLemniscate.bernoulli_origin
#print axioms BernoulliLemniscate.bernoulli_right_tip
#print axioms BernoulliLemniscate.bernoulli_left_tip
#print axioms BernoulliLemniscate.bernoulli_x_intercepts
#print axioms BernoulliLemniscate.bernoulli_x_sq_ge_y_sq
#print axioms BernoulliLemniscate.bernoulli_radius_bound
#print axioms BernoulliLemniscate.bernoulli_x_bound
#print axioms BernoulliLemniscate.bernoulli_y_bound_quarter
#print axioms BernoulliLemniscate.bernoulli_y_bound
#print axioms BernoulliLemniscate.bernoulli_radius_tight
#print axioms BernoulliLemniscate.bernoulli_polar_param
#print axioms BernoulliLemniscate.bernoulli_right_lobe_boundary
#print axioms BernoulliLemniscate.bernoulli_left_lobe_boundary
#print axioms BernoulliLemniscate.bernoulli_not_gerono
#print axioms BernoulliLemniscate.bernoulli_not_analemma
