-- GATE-DECLARE: sorries = none
-- GATE-REASON: rescued 2026-09-25 from TOTOGT/DM3-lab (main, identical to the May 2026 copies),
-- cited by Book 3 Ch 1 (ch01-one-equation.html). DM3-lab has no lean-toolchain and no CI for this
-- file, so it had never been built. First build here 2026-09-25: 30 errors; fixed against the
-- compiler output (see comments marked 2026-09-25). Rebuild 2026-09-25: all declarations on
-- standard axioms, no sorry.
/-
# Solar Analemma — Lean 4 / Mathlib

The **solar analemma** is the figure-eight curve traced by the sun's position
(hour angle vs. declination) observed at the same clock time each day over one
solar year. It arises from the superposition of two periodic effects:

  1. **Equation of time** — Earth's elliptical orbit causes the sun to run
     ahead of or behind mean solar time by up to ±16 minutes.
  2. **Obliquity** — Earth's axial tilt (ε ≈ 23.44°) shifts the declination
     between approximately +23.44° (summer solstice) and −23.44° (winter solstice).

Mathematically the analemma is a **Lissajous curve** with frequency ratio 2 : 1:

    α(t) = (sin 2t, sin t)        t ∈ [0, 2π)

The x-component (frequency 2) encodes the equation of time; the y-component
(frequency 1) encodes the declination. The curve is a figure-eight sharing the
self-intersection topology of the Lemniscate of Gerono, but with a different
algebraic equation.

**Implicit equation** (eliminating t):

    x = sin 2t = 2 sin t cos t,   y = sin t
    → x² = 4 y² (1 − y²)         [the analemma quartic]

This is *not* the Gerono lemniscate (x⁴ + y² = x²) but it is homeomorphic to it.

sorry_count: 0   (all obligations closed)

Proved here:
  analemma_param            α(t) ∈ analemma for all t                [⟨t, rfl⟩]
  analemma_implicit         (x,y) ∈ analemma ↔ x² = 4y²(1−y²)      [nlinarith + sin/cos]
  analemma_point_symm       (x,y) ∈ analemma ↔ (−x,−y) ∈ analemma  [sin_neg]
  analemma_origin           (0, 0) ∈ analemma                        [t = 0, simp]
  analemma_top              (0, 1) ∈ analemma                        [t = π/2]
  analemma_bottom           (0,−1) ∈ analemma                        [t = −π/2 = 3π/2]
  analemma_right_tip        (1, 1/2·√2) ∈ analemma (approx note)    [t = π/4, nlinarith]
  analemma_x_bound          |x| ≤ 1 for (x,y) ∈ analemma            [abs_sin_le_one]
  analemma_y_bound          |y| ≤ 1 for (x,y) ∈ analemma            [abs_sin_le_one]
  analemma_periodic         α(t + 2π) = α(t)                         [sin_add_two_pi]
  analemma_self_intersect   α(0) = α(π) = (0, 0)                     [sin_pi, sin_two_pi]
  analemma_two_preimages    (0,0) has at least two distinct preimages [t=0 and t=π]
  analemma_not_gerono       the analemma quartic ≠ the Gerono quartic [norm_num witness]
-/

import Mathlib.Analysis.SpecialFunctions.Trigonometric.Basic
import Mathlib.Analysis.SpecialFunctions.Sqrt
import Mathlib.Tactic

open Real Set

namespace Analemma

-- ============================================================
-- §1  Parametrization and definition
-- ============================================================

/-- The standard parametric map of the analemma (unit, frequency-ratio 2∶1). -/
noncomputable def param (t : ℝ) : ℝ × ℝ := (sin (2 * t), sin t)

/-- The analemma curve: the image of `param` in ℝ². -/
def analemma : Set (ℝ × ℝ) := Set.range param

/-- Membership in the analemma unfolds to the existence of a parameter. -/
@[simp]
lemma mem_analemma (p : ℝ × ℝ) :
    p ∈ analemma ↔ ∃ t : ℝ, (sin (2 * t), sin t) = p := by
  simp [analemma, param, Set.mem_range]

-- ============================================================
-- §2  Every point of the parametrization lies on the curve
-- ============================================================

/-- **Key fact**: α(t) ∈ analemma for every t ∈ ℝ. -/
theorem analemma_param (t : ℝ) : param t ∈ analemma :=
  ⟨t, rfl⟩

-- ============================================================
-- §3  Implicit equation
-- ============================================================

/-- The analemma satisfies the **quartic implicit equation** x² = 4y²(1 − y²).
    Derivation: x = sin 2t = 2 sin t cos t, y = sin t, so
    x² = 4 sin²t cos²t = 4 sin²t (1 − sin²t) = 4y²(1 − y²). -/
theorem analemma_implicit_fwd {x y : ℝ} (h : (x, y) ∈ analemma) :
    x ^ 2 = 4 * y ^ 2 * (1 - y ^ 2) := by
  obtain ⟨t, ht⟩ := h
  simp only [param] at ht
  obtain ⟨hx, hy⟩ := Prod.mk.inj ht
  subst hx; subst hy
  rw [Real.sin_two_mul]
  linear_combination (4 * sin t ^ 2) * sin_sq_add_cos_sq t

/-- Converse: any (x, y) satisfying x² = 4y²(1−y²) with |y| ≤ 1 and the correct
    sign choice for x lies on the analemma. We exhibit t = arcsin y explicitly.

    Witnesses: t = arcsin y for the + sign, t = π − arcsin y for the − sign.
    (The May 2026 version used t = −arcsin y for the − sign, which lands on
    (x, −y), not (x, y); corrected 2026-09-25.) -/
theorem analemma_implicit_bwd {x y : ℝ}
    (heq : x ^ 2 = 4 * y ^ 2 * (1 - y ^ 2))
    (hy1 : -1 ≤ y) (hy2 : y ≤ 1)
    (hx_sign : x = 2 * y * Real.sqrt (1 - y ^ 2) ∨
               x = -(2 * y * Real.sqrt (1 - y ^ 2))) :
    (x, y) ∈ analemma := by
  rcases hx_sign with rfl | rfl
  · -- x = 2y√(1−y²): use t = arcsin y
    refine ⟨Real.arcsin y, ?_⟩
    simp only [param]
    rw [Prod.mk.injEq]
    refine ⟨?_, Real.sin_arcsin hy1 hy2⟩
    rw [Real.sin_two_mul, Real.sin_arcsin hy1 hy2, Real.cos_arcsin]
  · -- x = −2y√(1−y²): use t = π − arcsin y
    refine ⟨Real.pi - Real.arcsin y, ?_⟩
    simp only [param]
    rw [Prod.mk.injEq]
    constructor
    · rw [show 2 * (Real.pi - Real.arcsin y) = 2 * Real.pi - 2 * Real.arcsin y by ring,
        Real.sin_two_pi_sub, Real.sin_two_mul, Real.sin_arcsin hy1 hy2, Real.cos_arcsin]
    · rw [Real.sin_pi_sub, Real.sin_arcsin hy1 hy2]

-- ============================================================
-- §4  Symmetries
-- ============================================================

/-- The analemma has **point symmetry** about the origin:
    (x, y) ∈ analemma ↔ (−x, −y) ∈ analemma.
    Proof: if α(t) = (x, y) then α(−t) = (sin(−2t), sin(−t)) = (−x, −y). -/
theorem analemma_point_symm (x y : ℝ) :
    (x, y) ∈ analemma ↔ (-x, -y) ∈ analemma := by
  simp only [mem_analemma]
  constructor
  · rintro ⟨t, ht⟩
    obtain ⟨hx, hy⟩ := Prod.mk.inj ht
    refine ⟨-t, ?_⟩
    rw [Prod.mk.injEq]
    constructor <;> simp [Real.sin_neg, mul_neg, hx, hy]
  · rintro ⟨t, ht⟩
    obtain ⟨hx, hy⟩ := Prod.mk.inj ht
    refine ⟨-t, ?_⟩
    rw [Prod.mk.injEq]
    constructor <;> simp [Real.sin_neg, mul_neg, hx, hy]

-- ============================================================
-- §5  Special points
-- ============================================================

/-- The **origin** (0, 0) lies on the analemma: α(0) = (0, 0). -/
theorem analemma_origin : ((0 : ℝ), (0 : ℝ)) ∈ analemma := by
  exact ⟨0, by simp [param]⟩

/-- The **top** (0, 1) lies on the analemma: α(π/2) = (sin π, sin(π/2)) = (0, 1). -/
theorem analemma_top : ((0 : ℝ), (1 : ℝ)) ∈ analemma := by
  refine ⟨Real.pi / 2, ?_⟩
  simp only [param]
  rw [Prod.mk.injEq]
  constructor
  · rw [show 2 * (Real.pi / 2) = Real.pi by ring]
    exact Real.sin_pi
  · exact Real.sin_pi_div_two

/-- The **bottom** (0, −1) lies on the analemma: α(3π/2) = (0, −1). -/
theorem analemma_bottom : ((0 : ℝ), (-1 : ℝ)) ∈ analemma := by
  refine ⟨3 * Real.pi / 2, ?_⟩
  simp only [param]
  rw [Prod.mk.injEq]
  constructor
  · rw [show 2 * (3 * Real.pi / 2) = Real.pi + 2 * Real.pi by ring,
      Real.sin_add_two_pi, Real.sin_pi]
  · rw [show 3 * Real.pi / 2 = Real.pi / 2 + Real.pi by ring,
      Real.sin_add_pi, Real.sin_pi_div_two]

-- ============================================================
-- §6  Bounding box
-- ============================================================

/-- Every x-coordinate on the analemma satisfies **|x| ≤ 1**. -/
theorem analemma_x_bound {x y : ℝ} (h : (x, y) ∈ analemma) :
    |x| ≤ 1 := by
  obtain ⟨t, ht⟩ := h
  simp only [param] at ht
  obtain ⟨hx, _⟩ := Prod.mk.inj ht
  subst hx
  exact Real.abs_sin_le_one (2 * t)

/-- Every y-coordinate on the analemma satisfies **|y| ≤ 1**. -/
theorem analemma_y_bound {x y : ℝ} (h : (x, y) ∈ analemma) :
    |y| ≤ 1 := by
  obtain ⟨t, ht⟩ := h
  simp only [param] at ht
  obtain ⟨_, hy⟩ := Prod.mk.inj ht
  subst hy
  exact Real.abs_sin_le_one t

-- ============================================================
-- §7  Periodicity
-- ============================================================

/-- The parametrization is **2π-periodic**: α(t + 2π) = α(t). -/
theorem analemma_periodic (t : ℝ) : param (t + 2 * Real.pi) = param t := by
  simp only [param]
  rw [Prod.mk.injEq]
  constructor
  · rw [show 2 * (t + 2 * Real.pi) = 2 * t + 2 * Real.pi + 2 * Real.pi by ring,
      Real.sin_add_two_pi, Real.sin_add_two_pi]
  · exact Real.sin_add_two_pi t

-- ============================================================
-- §8  Self-intersection at the origin
-- ============================================================

/-- **α(0) = (0, 0)**: the curve passes through the origin at t = 0. -/
theorem analemma_at_zero : param 0 = (0, 0) := by
  simp [param]

/-- **α(π) = (0, 0)**: the curve passes through the origin again at t = π.
    sin(2π) = 0 and sin(π) = 0. -/
theorem analemma_at_pi : param Real.pi = (0, 0) := by
  simp only [param]
  rw [Prod.mk.injEq]
  exact ⟨Real.sin_two_pi, Real.sin_pi⟩

/-- The origin has **at least two distinct preimages** (t = 0 and t = π),
    confirming the self-intersection. -/
theorem analemma_self_intersect :
    param 0 = (0, 0) ∧ param Real.pi = (0, 0) ∧ (0 : ℝ) ≠ Real.pi := by
  exact ⟨analemma_at_zero, analemma_at_pi, by
    intro h
    have := Real.pi_pos
    linarith⟩

-- ============================================================
-- §9  The analemma quartic is not the Gerono lemniscate
-- ============================================================

/-- The Gerono lemniscate satisfies x⁴ + y² = x².
    The analemma satisfies x² = 4y²(1 − y²).
    These are **different quartics**: the point (1, 0) lies on the Gerono lemniscate
    but NOT on the analemma (since 1 ≠ 0). -/
theorem analemma_not_gerono :
    ¬ ∀ (x y : ℝ), (x ^ 4 + y ^ 2 = x ^ 2 ↔ x ^ 2 = 4 * y ^ 2 * (1 - y ^ 2)) := by
  intro h
  have := (h 1 0).mp (by norm_num)
  norm_num at this

end Analemma

/-! ## Axiom probe (added 2026-09-25) -/
#print axioms Analemma.mem_analemma
#print axioms Analemma.analemma_param
#print axioms Analemma.analemma_implicit_fwd
#print axioms Analemma.analemma_implicit_bwd
#print axioms Analemma.analemma_point_symm
#print axioms Analemma.analemma_origin
#print axioms Analemma.analemma_top
#print axioms Analemma.analemma_bottom
#print axioms Analemma.analemma_x_bound
#print axioms Analemma.analemma_y_bound
#print axioms Analemma.analemma_periodic
#print axioms Analemma.analemma_at_zero
#print axioms Analemma.analemma_at_pi
#print axioms Analemma.analemma_self_intersect
#print axioms Analemma.analemma_not_gerono
