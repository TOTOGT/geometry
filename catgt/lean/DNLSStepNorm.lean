/-
  DNLSStepNorm.lean -- Worker 1, step 2 (2026-11-28). STATUS: NOT YET COMPILED when written;
  see the CI run on the commit that adds it. Ties DNLSNorm.lean to the ACTUAL `dnlsStep` of
  CatGT_Main.lean.

  Statement proved here (once the kernel agrees):
      dnlsNorm (dnlsStep hN c dt) = dnlsNorm c + dt^2 * Σ_n normSq (F ... c.ψ n)
  i.e. the explicit-Euler iterator of CatGT_Main §5 does NOT conserve the norm: it adds
  dt² ‖F(ψ)‖² every step, and the continuous flow does conserve it (DNLSNorm.lean).
  `nextIdx`/`prevIdx` are the index maps written inside `dnlsStep`.
-/
import Mathlib
import CatGT_Main
import DNLSNorm

open Complex

namespace CatGTNorm

variable {N : ℕ}

/-- the "next" site used inside `dnlsStep` -/
def nextIdx (hN : 0 < N) (n : Fin N) : Fin N := ⟨(n.val + 1) % N, Nat.mod_lt _ hN⟩

/-- the "previous" site used inside `dnlsStep` -/
def prevIdx (hN : 0 < N) (n : Fin N) : Fin N := ⟨(n.val + N - 1) % N, Nat.mod_lt _ hN⟩

theorem next_prev (hN : 0 < N) (n : Fin N) : nextIdx hN (prevIdx hN n) = n :=
  periodic_shift_inverse hN n

theorem prev_next (hN : 0 < N) (n : Fin N) : prevIdx hN (nextIdx hN n) = n := by
  apply Fin.ext
  have hn := n.isLt
  show ((n.val + 1) % N + N - 1) % N = n.val
  rcases Nat.lt_or_ge (n.val + 1) N with h | h
  · rw [Nat.mod_eq_of_lt h]
    have e : n.val + 1 + N - 1 = n.val + N := by omega
    rw [e, Nat.add_mod_right]
    exact Nat.mod_eq_of_lt hn
  · have e : n.val + 1 = N := by omega
    rw [e, Nat.mod_self]
    have e2 : 0 + N - 1 = n.val := by omega
    rw [e2]
    exact Nat.mod_eq_of_lt hn

/-- One `dnlsStep` is exactly the Euler step `ψ ↦ ψ + dt·F ψ` for the neighbour maps above. -/
theorem dnlsStep_eq_euler (hN : 0 < N) (c : DNLSChain N) (dt : ℝ) (n : Fin N) :
    (dnlsStep hN c dt).ψ n
      = c.ψ n + (dt : ℂ) * F (nextIdx hN) (prevIdx hN) c.J c.lam c.ψ n := by
  simp only [dnlsStep, F, nextIdx, prevIdx]
  have h2 : ((‖c.ψ n‖ : ℝ) : ℂ) ^ 2 = ((Complex.normSq (c.ψ n) : ℝ) : ℂ) := by
    rw [Complex.normSq_eq_norm_sq]; push_cast; ring
  rw [h2]
  push_cast
  ring

/-- **Exact norm law for the CatGT iterator.** -/
theorem dnlsStep_norm_sq (hN : 0 < N) (c : DNLSChain N) (dt : ℝ) :
    dnlsNorm (dnlsStep hN c dt)
      = dnlsNorm c
        + dt ^ 2 * ∑ n, Complex.normSq (F (nextIdx hN) (prevIdx hN) c.J c.lam c.ψ n) := by
  have h1 : dnlsNorm (dnlsStep hN c dt)
      = ∑ n, Complex.normSq ((dnlsStep hN c dt).ψ n) := by
    unfold dnlsNorm; simp only [Complex.normSq_eq_norm_sq]
  have h2 : dnlsNorm c = ∑ n, Complex.normSq (c.ψ n) := by
    unfold dnlsNorm; simp only [Complex.normSq_eq_norm_sq]
  rw [h1, h2]
  simp only [dnlsStep_eq_euler]
  exact euler_norm_sq (nextIdx hN) (prevIdx hN) (prev_next hN) (next_prev hN) c.J c.lam dt c.ψ

/-- The iterator never decreases the norm. -/
theorem dnlsStep_norm_ge (hN : 0 < N) (c : DNLSChain N) (dt : ℝ) :
    dnlsNorm c ≤ dnlsNorm (dnlsStep hN c dt) := by
  rw [dnlsStep_norm_sq]
  have : 0 ≤ dt ^ 2 * ∑ n, Complex.normSq (F (nextIdx hN) (prevIdx hN) c.J c.lam c.ψ n) :=
    mul_nonneg (sq_nonneg dt) (Finset.sum_nonneg (fun n _ => Complex.normSq_nonneg _))
  linarith

end CatGTNorm
