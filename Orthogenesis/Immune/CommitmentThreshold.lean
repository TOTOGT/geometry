-- GATE-DECLARE: sorries = none
-- GATE-REASON: ch5 Theorem 5.1 made exact on the cusp model: escape at K*, memory as bistability, irreversibility iff the return fold is below zero signal, bottleneck time π/√r.
/-
Orthogenesis/Immune/CommitmentThreshold.lean — Book 3, ch5 (Immune Adaptation), Theorem 5.1.

Theorem 5.1's proof sketch assumes a bistable potential whose "C-well" loses its barrier at K*.
That is a fold. Here it is placed on the proved cusp slice of FoldHysteresis, with signal I and
control a = I − c (c sets where the thresholds sit, in the system's own units):

  §1  The C-well (q > 1) exists iff I < K* := c + 2. Past K* nothing is left near it.
  §2  The F-well (q < −1) exists iff I > c − 2.
  §3  Memory: for c − 2 < I < K* both wells exist. Lowering the signal back under K* does not
      undo commitment. This is the residue.
  §4  Irreversibility for every physical signal (I ≥ 0) holds iff c < 2, i.e. iff the return
      fold c − 2 sits below zero signal. Theorem 5.1's "irreversible" is therefore a claim about
      where the second fold lies, not a consequence of having a threshold.
  §5  τ_min: in the local normal form ẋ = r + x² just past a fold (r > 0 proportional to I − K*),
      the passage time is ∫ dx/(r + x²) = π/√r. Commitment just above threshold is slow, and
      slows as (I − K*)^(−1/2).

Not formalised: that the germinal-centre network reduces to one slow variable (operator C,
centre-manifold reduction); the reduction of the cusp near its fold to r + x² (only the
normal form's integral is proved); any immunological constant.
-/
import Mathlib
import Orthogenesis.Taxonomy.FoldHysteresis

namespace Orthogenesis.CommitmentThreshold

open Orthogenesis.FoldHysteresis

/-- Commitment threshold in signal units. -/
def Kstar (c : ℝ) : ℝ := c + 2

/-! ## §1  The testing well and its end -/

theorem c_well_iff (c I : ℝ) : (∃ q, 1 < q ∧ dW (I - c) q = 0) ↔ I < Kstar c := by
  rw [right_branch_iff]; unfold Kstar; constructor <;> intro h <;> linarith

theorem nothing_near_after_Kstar {c I : ℝ} (h : Kstar c < I) (q : ℝ) (hq : -2 ≤ q) :
    dW (I - c) q ≠ 0 :=
  nothing_near_past_right_fold (by unfold Kstar at h; linarith) q hq

/-! ## §2  The committed well -/

theorem f_well_iff (c I : ℝ) : (∃ q, q < -1 ∧ dW (I - c) q = 0) ↔ c - 2 < I := by
  rw [left_branch_iff]; constructor <;> intro h <;> linarith

/-! ## §3  Memory is bistability -/

theorem memory_window {c I : ℝ} (h1 : c - 2 < I) (h2 : I < Kstar c) :
    ∃ q₁ q₂, q₁ < -1 ∧ 1 < q₂ ∧ dW (I - c) q₁ = 0 ∧ dW (I - c) q₂ = 0 ∧
      0 < d2W q₁ ∧ 0 < d2W q₂ :=
  bistable (by linarith) (by unfold Kstar at h2; linarith)

/-! ## §4  When is commitment irreversible? -/

theorem irreversible_iff (c : ℝ) :
    (∀ I : ℝ, 0 ≤ I → ∃ q, q < -1 ∧ dW (I - c) q = 0) ↔ c < 2 := by
  constructor
  · intro h
    have := (f_well_iff c 0).mp (h 0 le_rfl)
    linarith
  · intro hc I hI
    exact (f_well_iff c I).mpr (by linarith)

/-- If the return fold is at a physical signal, lowering the signal that far erases the
    committed state. -/
theorem reversible_if {c : ℝ} (hc : 2 ≤ c) :
    ∃ I : ℝ, 0 ≤ I ∧ ¬ ∃ q, q < -1 ∧ dW (I - c) q = 0 := by
  refine ⟨c - 2, by linarith, ?_⟩
  rw [f_well_iff]; exact lt_irrefl _

/-! ## §5  Bottleneck time past a fold -/

theorem bottleneck_time (r : ℝ) (hr : 0 < r) : ∫ x : ℝ, (r + x ^ 2)⁻¹ = Real.pi / Real.sqrt r := by
  have hpos : 0 < Real.sqrt r := Real.sqrt_pos.mpr hr
  have e : ∀ x : ℝ, (r + x ^ 2)⁻¹ = r⁻¹ * (1 + (x / Real.sqrt r) ^ 2)⁻¹ := by
    intro x
    have h1 : r + x ^ 2 ≠ 0 := by positivity
    have hr0 : r ≠ 0 := ne_of_gt hr
    rw [div_pow, Real.sq_sqrt hr.le]
    field_simp
  have hc := MeasureTheory.Measure.integral_comp_div (fun y : ℝ => (1 + y ^ 2)⁻¹) (Real.sqrt r)
  beta_reduce at hc
  calc ∫ x : ℝ, (r + x ^ 2)⁻¹ = ∫ x : ℝ, r⁻¹ * (1 + (x / Real.sqrt r) ^ 2)⁻¹ := by
        congr 1; funext x; exact e x
    _ = r⁻¹ * ∫ x : ℝ, (1 + (x / Real.sqrt r) ^ 2)⁻¹ := MeasureTheory.integral_const_mul _ _
    _ = r⁻¹ * (|Real.sqrt r| * Real.pi) := by
        rw [hc, integral_univ_inv_one_add_sq, smul_eq_mul]
    _ = Real.pi / Real.sqrt r := by
        rw [abs_of_nonneg (Real.sqrt_nonneg r), eq_div_iff (ne_of_gt hpos),
          show r⁻¹ * (Real.sqrt r * Real.pi) * Real.sqrt r
            = r⁻¹ * (Real.sqrt r * Real.sqrt r) * Real.pi by ring,
          Real.mul_self_sqrt hr.le, inv_mul_cancel₀ (ne_of_gt hr), one_mul]

end Orthogenesis.CommitmentThreshold

#print axioms Orthogenesis.CommitmentThreshold.c_well_iff
#print axioms Orthogenesis.CommitmentThreshold.f_well_iff
#print axioms Orthogenesis.CommitmentThreshold.memory_window
#print axioms Orthogenesis.CommitmentThreshold.irreversible_iff
#print axioms Orthogenesis.CommitmentThreshold.reversible_if
#print axioms Orthogenesis.CommitmentThreshold.bottleneck_time
