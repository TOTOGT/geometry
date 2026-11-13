/-
  Ch19MultistabilityAlgebra.lean
  Companion to book26/ch19-a-toy-for-cycles-with-several-stable-states.html, section "The model".

  STATUS: compiled with no errors or warnings on the author's Mac on 2026-11-13 (`lake env lean
  Ch19MultistabilityAlgebra.lean`, Lean v4.32.0 / Mathlib v4.32.0). `#print axioms` on all 14 theorems
  lists only propext, Classical.choice and Quot.sound. Written without a toolchain; the first compile
  needed no fixes. Compile and axiom outputs were read by hand and are not stored in the repo.

  WHAT THIS FILE STATES (the SYMMETRIC case only: both nodes have the same growth rate, mB = 1)
    dxA = xA - xA^3 + k (xB - xA)        dxB = xB - xB^3 + k (xA - xB),   k >= 0 the coupling.

    1. mixed fixed points (x, -x) with x != 0 exist  iff  k < 1/2, and then x^2 = 1 - 2k.
    2. the partial derivatives of the drift are the Jacobian entries the chapter uses
       (so the Jacobian is not just asserted: it is tied to the drift by HasDerivAt).
    3. a 2x2 matrix [[d,k],[k,d]] has exactly the eigenvalues d+k and d-k.
    4. at a mixed fixed point the eigenvalues are -2+6k and -2+4k; both are negative iff k < 1/3;
       for 1/3 < k < 1/2 one is positive (saddle).
    5. at the aligned fixed points (1,1), (-1,-1) the eigenvalues are -2 and -2-2k.

  WHAT IT DOES NOT STATE
    - The chapter's toy uses mB = 0.6 (asymmetric). Nothing here covers that case.
    - "Both eigenvalues negative => the fixed point is stable" is the standard linearisation
      theorem. It is NOT formalised here; the file proves the signs of the eigenvalues only.
    - The noise, the Gaussian-mixture BIC test, Ashman's D and the power numbers are
      measurements, done in tools/multistability_toy.py, and are not touched by this file.
    - The B-row of the Jacobian is proved at the entries used; no general matrix object is built.
-/
import Mathlib

namespace Ch19Multistability

/-- Drift of node A. -/
def driftA (a b k : ℝ) : ℝ := a - a ^ 3 + k * (b - a)

/-- Drift of node B (same form, roles swapped). -/
def driftB (a b k : ℝ) : ℝ := b - b ^ 3 + k * (a - b)

/-! ### 1. Mixed fixed points -/

theorem driftA_mixed (x k : ℝ) : driftA x (-x) k = x * (1 - 2 * k - x ^ 2) := by
  unfold driftA; ring

theorem driftB_mixed (x k : ℝ) : driftB x (-x) k = -(x * (1 - 2 * k - x ^ 2)) := by
  unfold driftB; ring

/-- For x ≠ 0, (x, -x) is a fixed point of node A's equation iff x² = 1 - 2k. -/
theorem mixed_fixed_iff (x k : ℝ) (hx : x ≠ 0) :
    driftA x (-x) k = 0 ↔ x ^ 2 = 1 - 2 * k := by
  rw [driftA_mixed]
  constructor
  · intro h
    rcases mul_eq_zero.mp h with h0 | h0
    · exact absurd h0 hx
    · linarith
  · intro h
    have : 1 - 2 * k - x ^ 2 = 0 := by linarith
    rw [this]; ring

/-- (x, -x) is a fixed point of both equations iff A's equation holds (B's is its negative). -/
theorem mixed_fixed_both (x k : ℝ) :
    (driftA x (-x) k = 0 ∧ driftB x (-x) k = 0) ↔ driftA x (-x) k = 0 := by
  constructor
  · exact fun h => h.1
  · intro h
    refine ⟨h, ?_⟩
    rw [driftB_mixed]
    rw [driftA_mixed] at h
    rw [h]; ring

/-- A nonzero mixed fixed point exists iff k < 1/2. -/
theorem mixed_exists_iff (k : ℝ) :
    (∃ x : ℝ, x ≠ 0 ∧ driftA x (-x) k = 0) ↔ k < 1 / 2 := by
  constructor
  · rintro ⟨x, hx, h⟩
    rw [mixed_fixed_iff x k hx] at h
    have hpos : 0 < x ^ 2 := by positivity
    linarith
  · intro hk
    have hpos : 0 < 1 - 2 * k := by linarith
    refine ⟨Real.sqrt (1 - 2 * k), (Real.sqrt_pos.mpr hpos).ne', ?_⟩
    rw [mixed_fixed_iff _ _ (Real.sqrt_pos.mpr hpos).ne']
    exact Real.sq_sqrt hpos.le

/-! ### 5. Aligned fixed points -/

theorem aligned_fixed (k : ℝ) :
    driftA 1 1 k = 0 ∧ driftB 1 1 k = 0 ∧ driftA (-1) (-1) k = 0 ∧ driftB (-1) (-1) k = 0 := by
  unfold driftA driftB
  refine ⟨?_, ?_, ?_, ?_⟩ <;> ring

/-! ### 2. The Jacobian entries are the partial derivatives of the drift -/

theorem partialA_a (a b k : ℝ) :
    HasDerivAt (fun a => driftA a b k) (1 - 3 * a ^ 2 - k) a := by
  unfold driftA
  have h1 : HasDerivAt (fun a : ℝ => a) 1 a := hasDerivAt_id a
  have h3 : HasDerivAt (fun a : ℝ => a ^ 3) (3 * a ^ 2) a := by
    simpa using hasDerivAt_pow 3 a
  have h4 : HasDerivAt (fun a : ℝ => k * (b - a)) (k * (-1)) a :=
    ((hasDerivAt_id a).const_sub b).const_mul k
  exact ((h1.sub h3).add h4).congr_deriv (by ring)

theorem partialA_b (a b k : ℝ) :
    HasDerivAt (fun b => driftA a b k) k b := by
  unfold driftA
  have h4 : HasDerivAt (fun b : ℝ => k * (b - a)) (k * 1) b :=
    ((hasDerivAt_id b).sub_const a).const_mul k
  exact (h4.const_add (a - a ^ 3)).congr_deriv (by ring)

theorem partialB_b (a b k : ℝ) :
    HasDerivAt (fun b => driftB a b k) (1 - 3 * b ^ 2 - k) b := by
  unfold driftB
  have h1 : HasDerivAt (fun b : ℝ => b) 1 b := hasDerivAt_id b
  have h3 : HasDerivAt (fun b : ℝ => b ^ 3) (3 * b ^ 2) b := by
    simpa using hasDerivAt_pow 3 b
  have h4 : HasDerivAt (fun b : ℝ => k * (a - b)) (k * (-1)) b :=
    ((hasDerivAt_id b).const_sub a).const_mul k
  exact ((h1.sub h3).add h4).congr_deriv (by ring)

theorem partialB_a (a b k : ℝ) :
    HasDerivAt (fun a => driftB a b k) k a := by
  unfold driftB
  have h4 : HasDerivAt (fun a : ℝ => k * (a - b)) (k * 1) a :=
    ((hasDerivAt_id a).sub_const b).const_mul k
  exact (h4.const_add (b - b ^ 3)).congr_deriv (by ring)

/-! ### 3. Eigenvalues of [[d, k], [k, d]] -/

/-- λ is an eigenvalue of [[d,k],[k,d]] (a nonzero vector (p,q) with M(p,q) = λ(p,q))
    iff λ = d + k or λ = d - k. -/
theorem eig2 (d k lam : ℝ) :
    (∃ p q : ℝ, (p ≠ 0 ∨ q ≠ 0) ∧ d * p + k * q = lam * p ∧ k * p + d * q = lam * q)
      ↔ (lam = d + k ∨ lam = d - k) := by
  constructor
  · rintro ⟨p, q, hv, h1, h2⟩
    have hs : (d + k - lam) * (p + q) = 0 := by linear_combination h1 + h2
    have hd : (d - k - lam) * (p - q) = 0 := by linear_combination h1 - h2
    rcases mul_eq_zero.mp hs with h | h
    · left; linarith
    · right
      have hne : p - q ≠ 0 := by
        rcases hv with hp | hq
        · intro h0; apply hp; linarith
        · intro h0; apply hq; linarith
      rcases mul_eq_zero.mp hd with h' | h'
      · linarith
      · exact absurd h' hne
  · rintro (h | h)
    · exact ⟨1, 1, Or.inl one_ne_zero, by subst h; ring, by subst h; ring⟩
    · exact ⟨1, -1, Or.inl one_ne_zero, by subst h; ring, by subst h; ring⟩

/-! ### 4. Eigenvalues at the mixed state, and the stability thresholds -/

/-- Diagonal Jacobian entry at (x, -x): d = 1 - 3x² - k. At x² = 1 - 2k the two eigenvalues
    d + k and d - k are -2 + 6k and -2 + 4k. -/
theorem mixed_eigenvalues (x k : ℝ) (h : x ^ 2 = 1 - 2 * k) :
    (1 - 3 * x ^ 2 - k) + k = -2 + 6 * k ∧ (1 - 3 * x ^ 2 - k) - k = -2 + 4 * k := by
  constructor <;> linarith

theorem mixed_both_negative_iff (k : ℝ) :
    (-2 + 6 * k < 0 ∧ -2 + 4 * k < 0) ↔ k < 1 / 3 := by
  constructor
  · rintro ⟨h, _⟩; linarith
  · intro h; constructor <;> linarith

theorem mixed_saddle (k : ℝ) (h1 : 1 / 3 < k) (h2 : k < 1 / 2) :
    0 < -2 + 6 * k ∧ -2 + 4 * k < 0 := by
  constructor <;> linarith

/-- Aligned fixed points (1,1): d = 1 - 3 - k; eigenvalues d + k = -2 and d - k = -2 - 2k. -/
theorem aligned_eigenvalues (k : ℝ) :
    (1 - 3 * (1 : ℝ) ^ 2 - k) + k = -2 ∧ (1 - 3 * (1 : ℝ) ^ 2 - k) - k = -2 - 2 * k := by
  constructor <;> ring

theorem aligned_both_negative (k : ℝ) (hk : 0 ≤ k) : (-2 : ℝ) < 0 ∧ -2 - 2 * k < 0 := by
  constructor <;> linarith

end Ch19Multistability
