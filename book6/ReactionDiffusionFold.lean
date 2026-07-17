/-
  Reaction–Diffusion Fold — rigour of the single-mode reduction, in Lean 4
  Principia Orthogona · Book 6 · ch-reaction-diffusion-fold · G6 LLC · Newark NJ · 2026

  STATUS: The algebraic / spectral core below — the cubic mode-coupling identity,
          the spectral gap, and the fold-locus discriminant — is written to be
          sound but has NOT yet been run through the kernel (compilation deferred).
          The center-manifold / inertial-manifold *existence* and the O(a⁵)
          asymptotic feedback bound are standard theorems; invoked, not formalized
          here. Do not cite as machine-checked until `lake build` passes.

  Tilted Chafee–Infante:  u_t = u_xx + λu − u³ + h  on (0,1), Dirichlet.
  Mode k = sin(kπx); linear growth rate μ_k = λ − k²π² = r − (k²−1)π²,  r := λ − π².
  Single-mode reduction:  ȧ = h + r a − (3/4) a³;  fold at h* = ±(4/9) r^{3/2}.
-/
import Mathlib.Analysis.SpecialFunctions.Trigonometric.Basic

namespace RDFold

/-- **Cubic mode-coupling identity.** sin³t = (3 sin t − sin 3t)/4. The mode-1
    self-interaction feeds mode 1 (coefficient 3/4) and *drives mode 3*
    (coefficient −1/4): this is the source term that slaves the higher mode. -/
theorem sin_cube (t : ℝ) : Real.sin t ^ 3 = (3 * Real.sin t - Real.sin (3 * t)) / 4 := by
  have h := Real.sin_three_mul t
  linarith [h]

/-- **Spectral gap.** With growth rate μ_k = r − (k²−1)π², every mode k ≥ 2 lies at
    least 3π² below the critical first mode: μ_k ≤ r − 3π². This is the gap under
    which the center-manifold theorem slaves the higher modes to the first. -/
theorem spectral_gap (r : ℝ) (k : ℕ) (hk : 2 ≤ k) :
    r - ((k : ℝ) ^ 2 - 1) * Real.pi ^ 2 ≤ r - 3 * Real.pi ^ 2 := by
  have hk2 : (4 : ℝ) ≤ (k : ℝ) ^ 2 := by
    have : (2 : ℝ) ≤ (k : ℝ) := by exact_mod_cast hk
    nlinarith [this]
  have key : 0 ≤ ((k : ℝ) ^ 2 - 4) * Real.pi ^ 2 :=
    mul_nonneg (by linarith) (sq_nonneg _)
  nlinarith [key]

/-- **Fold locus (discriminant).** Equilibria solve (3/4)a³ − r a − h = 0. The
    saddle-node (double-root) condition is the vanishing of the discriminant; cleared
    of denominators (× 27) it reads 256 r³ − 1296 h² = 0, equivalently 81 h² = 16 r³,
    i.e. h = ±(4/9) r^{3/2}. -/
theorem fold_locus (r h : ℝ) :
    (256 * r ^ 3 - 1296 * h ^ 2 = 0) ↔ (81 * h ^ 2 = 16 * r ^ 3) := by
  constructor <;> intro H <;> linarith [H]

end RDFold
