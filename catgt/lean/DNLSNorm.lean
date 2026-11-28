/-
  DNLSNorm.lean -- Worker 1: continuous-time norm conservation for the CatGT DNLS chain.
  Written 2026-11-28. STATUS: NOT YET COMPILED. No Lean toolchain is reachable from the
  authoring sandbox; the first kernel verdict is the CI run on the commit that adds this file.
  Do not cite as verified until `#print axioms` for the declarations in
  tools/verify-catgt/probe_dnlsnorm.lean has been read from a real run.

  THE ACTUAL EQUATION (from CatGT_Main.lean §5, `dnlsStep`):
      i ψ̇_n = -J(ψ_{n+1} + ψ_{n-1}) - λ |ψ_n|² ψ_n,   periodic chain of N sites,
  i.e. ψ̇ = -i H(ψ) ψ with H(ψ) = -J(S + S⁻¹) - λ diag|ψ_n|², H(ψ) Hermitian for every ψ
  (S = cyclic shift, J, λ real). So the norm IS conserved by the continuous flow, and the
  hand derivation is
      d/dt Σ|ψ_n|² = 2 Re Σ conj(ψ_n) ψ̇_n = 2 Im ⟨ψ, H(ψ) ψ⟩ = 0.
  The nonlinear term drops because conj(ψ)·|ψ|²ψ = |ψ|⁴ is real, so i·λ·|ψ|⁴ has real part 0;
  the hopping term drops because the shift and its inverse contribute opposite
  antisymmetric terms c(n,σn) and c(n,τn) = -c(σ⁻¹…), cancelling under reindexing.

  WHAT THIS FILE PROVES (statements; see each docstring):
   1. `drift_zero`            Σ_n Re(conj ψ_n · F(ψ)_n) = 0 for every ψ (the algebraic core).
   2. `dnls_norm_hasDerivAt`  along any solution, d/dt Σ normSq ψ_n = 0.
   3. `dnls_norm_conserved`   ‖ψ(t)‖² = ‖ψ(0)‖² for all t (solution on all of ℝ).
   4. `euler_norm_sq`         EXACT law for the explicit Euler step used by `dnlsStep`:
                              ‖ψ + dt·F(ψ)‖² = ‖ψ‖² + dt²‖F(ψ)‖². It GROWS unless F(ψ)=0,
                              so the iterator in §5 of CatGT_Main does not conserve the norm.
  SCOPE, stated plainly: (a) the chain is the finite periodic one (a system of ODEs on ℂ^N),
  not the continuum PDE; (b) existence of solutions is a hypothesis, not proved here;
  (c) the link "σ, τ here = the index maps inside dnlsStep" is the lemma
  `periodic_shift_inverse` below, which is proved separately and is the likeliest place for a
  first compiler error; (d) nothing here touches the sech/width results of §4b-§4d.
-/
import Mathlib

open Complex

namespace CatGTNorm

variable {N : ℕ}

/-- Right-hand side of the DNLS equation, ψ̇ = F ψ, with neighbour maps σ (next), τ (prev):
    F(φ)_n = i (J (φ_{σ n} + φ_{τ n}) + λ |φ_n|² φ_n). -/
noncomputable def F (σ τ : Fin N → Fin N) (J lam : ℝ) (φ : Fin N → ℂ) (n : Fin N) : ℂ :=
  Complex.I * ((J : ℂ) * (φ (σ n) + φ (τ n)) + ((lam * Complex.normSq (φ n) : ℝ) : ℂ) * φ n)

/-- antisymmetric pairing c(m,k) = Re φ_m · Im φ_k - Im φ_m · Re φ_k. -/
def cc (φ : Fin N → ℂ) (m k : Fin N) : ℝ := (φ m).re * (φ k).im - (φ m).im * (φ k).re

theorem cc_antisymm (φ : Fin N → ℂ) (m k : Fin N) : cc φ m k = - cc φ k m := by
  unfold cc; ring

/-- per-site drift 2 Re φ · Re Fφ + 2 Im φ · Im Fφ = 2 Re(conj φ · Fφ). -/
theorem site_drift (σ τ : Fin N → Fin N) (J lam : ℝ) (φ : Fin N → ℂ) (n : Fin N) :
    2 * (φ n).re * (F σ τ J lam φ n).re + 2 * (φ n).im * (F σ τ J lam φ n).im
      = -2 * J * (cc φ n (σ n) + cc φ n (τ n)) := by
  simp only [F, cc, Complex.mul_re, Complex.mul_im, Complex.add_re, Complex.add_im,
    Complex.I_re, Complex.I_im, Complex.ofReal_re, Complex.ofReal_im, Complex.normSq_apply]
  ring

/-- Algebraic core: the total drift Σ_n 2 Re(conj φ_n (Fφ)_n) vanishes, for ANY φ,
    provided σ and τ are mutually inverse (a cyclic shift and its inverse). -/
theorem drift_zero (σ τ : Fin N → Fin N) (hστ : ∀ n, τ (σ n) = n) (hτσ : ∀ n, σ (τ n) = n)
    (J lam : ℝ) (φ : Fin N → ℂ) :
    ∑ n, (2 * (φ n).re * (F σ τ J lam φ n).re + 2 * (φ n).im * (F σ τ J lam φ n).im) = 0 := by
  let e : Fin N ≃ Fin N := ⟨σ, τ, hστ, hτσ⟩
  have hsum : ∑ n, cc φ n (τ n) = - ∑ n, cc φ n (σ n) := by
    have h1 : ∑ m, cc φ (e m) (τ (e m)) = ∑ n, cc φ n (τ n) :=
      Equiv.sum_comp e (fun n => cc φ n (τ n))
    have h2 : ∀ m, cc φ (e m) (τ (e m)) = - cc φ m (σ m) := by
      intro m
      show cc φ (σ m) (τ (σ m)) = - cc φ m (σ m)
      rw [hστ m, cc_antisymm φ (σ m) m]
    rw [← h1]
    simp only [h2, Finset.sum_neg_distrib]
  simp only [site_drift, ← Finset.mul_sum, Finset.sum_add_distrib, hsum]
  ring

/-- value-level derivative of normSq along a curve in ℂ. -/
theorem hasDerivAt_normSq {f : ℝ → ℂ} {f' : ℂ} {t : ℝ} (h : HasDerivAt f f' t) :
    HasDerivAt (fun s => Complex.normSq (f s))
      (2 * (f t).re * f'.re + 2 * (f t).im * f'.im) t := by
  have hre : HasDerivAt (fun s => (f s).re) f'.re t := by
    simpa using Complex.reCLM.hasFDerivAt.comp_hasDerivAt t h
  have him : HasDerivAt (fun s => (f s).im) f'.im t := by
    simpa using Complex.imCLM.hasFDerivAt.comp_hasDerivAt t h
  have := (hre.mul hre).add (him.mul him)
  convert this using 1
  · funext s; simp [Complex.normSq_apply]
  · ring

/-- **Continuous-time norm balance.** If every component of ψ(·) has derivative F(ψ(t))_n,
    then d/dt Σ_n normSq ψ_n = 0. -/
theorem dnls_norm_hasDerivAt (σ τ : Fin N → Fin N) (hστ : ∀ n, τ (σ n) = n)
    (hτσ : ∀ n, σ (τ n) = n) (J lam : ℝ) (ψ : ℝ → Fin N → ℂ)
    (hψ : ∀ t n, HasDerivAt (fun s => ψ s n) (F σ τ J lam (ψ t) n) t) (t : ℝ) :
    HasDerivAt (fun s => ∑ n, Complex.normSq (ψ s n)) 0 t := by
  have h := HasDerivAt.sum (u := Finset.univ) (fun n _ => hasDerivAt_normSq (hψ t n))
  have h0 := drift_zero σ τ hστ hτσ J lam (ψ t)
  rw [← h0]
  simpa using h

/-- **Norm conservation for the CatGT DNLS chain (continuous time).**
    For a solution on all of ℝ, ‖ψ(t)‖² = ‖ψ(0)‖² for every t. -/
theorem dnls_norm_conserved (σ τ : Fin N → Fin N) (hστ : ∀ n, τ (σ n) = n)
    (hτσ : ∀ n, σ (τ n) = n) (J lam : ℝ) (ψ : ℝ → Fin N → ℂ)
    (hψ : ∀ t n, HasDerivAt (fun s => ψ s n) (F σ τ J lam (ψ t) n) t) (t : ℝ) :
    ∑ n, ‖ψ t n‖ ^ 2 = ∑ n, ‖ψ 0 n‖ ^ 2 := by
  have hd := dnls_norm_hasDerivAt σ τ hστ hτσ J lam ψ hψ
  have hconst : ∑ n, Complex.normSq (ψ t n) = ∑ n, Complex.normSq (ψ 0 n) :=
    is_const_of_deriv_eq_zero (fun s => (hd s).differentiableAt) (fun s => (hd s).deriv) t 0
  simpa [Complex.normSq_eq_norm_sq] using hconst

/-- **Exact norm law for the explicit Euler step** ψ ↦ ψ + dt·F(ψ), the form `dnlsStep` uses:
    Σ normSq (ψ+dt·Fψ)_n = Σ normSq ψ_n + dt² Σ normSq (Fψ)_n.
    The cross term is dt times the drift, which `drift_zero` kills; the quadratic term is
    positive unless Fψ = 0. This is the derived obstruction for the §5 iterator. -/
theorem euler_norm_sq (σ τ : Fin N → Fin N) (hστ : ∀ n, τ (σ n) = n)
    (hτσ : ∀ n, σ (τ n) = n) (J lam dt : ℝ) (φ : Fin N → ℂ) :
    ∑ n, Complex.normSq (φ n + (dt : ℂ) * F σ τ J lam φ n)
      = ∑ n, Complex.normSq (φ n) + dt ^ 2 * ∑ n, Complex.normSq (F σ τ J lam φ n) := by
  have h0 := drift_zero σ τ hστ hτσ J lam φ
  have hpt : ∀ n, Complex.normSq (φ n + (dt : ℂ) * F σ τ J lam φ n)
      = Complex.normSq (φ n)
        + dt * (2 * (φ n).re * (F σ τ J lam φ n).re + 2 * (φ n).im * (F σ τ J lam φ n).im)
        + dt ^ 2 * Complex.normSq (F σ τ J lam φ n) := by
    intro n
    simp only [Complex.normSq_apply, Complex.add_re, Complex.add_im, Complex.mul_re,
      Complex.mul_im, Complex.ofReal_re, Complex.ofReal_im]
    ring
  simp only [hpt, Finset.sum_add_distrib, ← Finset.mul_sum, h0]
  ring

/-- The periodic neighbour maps used by `dnlsStep` are mutually inverse (N > 0). -/
theorem periodic_shift_inverse (hN : 0 < N) :
    (∀ n : Fin N, (⟨((⟨(n.val + N - 1) % N, Nat.mod_lt _ hN⟩ : Fin N).val + 1) % N,
        Nat.mod_lt _ hN⟩ : Fin N) = n) := by
  intro n
  apply Fin.ext
  have hn := n.isLt
  show ((n.val + N - 1) % N + 1) % N = n.val
  rcases Nat.eq_zero_or_pos n.val with h0 | hpos
  · rw [h0]
    have : (0 + N - 1) % N = N - 1 := Nat.mod_eq_of_lt (by omega)
    rw [this, Nat.sub_add_cancel hN, Nat.mod_self]
  · have : (n.val + N - 1) % N = n.val - 1 := by
      have e : n.val + N - 1 = (n.val - 1) + N := by omega
      rw [e, Nat.add_mod_right]
      exact Nat.mod_eq_of_lt (by omega)
    rw [this, Nat.sub_add_cancel hpos]
    exact Nat.mod_eq_of_lt hn

end CatGTNorm
