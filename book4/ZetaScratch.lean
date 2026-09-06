import Mathlib.Analysis.SpecialFunctions.Gamma.Digamma
import Mathlib.Analysis.Calculus.Deriv.Star

namespace Scratch
open Complex ComplexConjugate

noncomputable def chiLog (s : ℂ) : ℂ :=
  (Real.log Real.pi : ℂ) - digamma (s / 2) / 2 - digamma ((1 - s) / 2) / 2

theorem conj_Gamma_conj_eq : conj ∘ Gamma ∘ conj = Gamma := by
  funext z
  simp [Function.comp_def, Gamma_conj]

theorem deriv_Gamma_conj (s : ℂ) :
    deriv Gamma (conj s) = conj (deriv Gamma s) := by
  have h : deriv Gamma = conj ∘ deriv Gamma ∘ conj := by
    conv_lhs => rw [← conj_Gamma_conj_eq]
    rw [deriv_conj_conj]
  calc deriv Gamma (conj s)
      = (conj ∘ deriv Gamma ∘ conj) (conj s) := by rw [← h]
    _ = conj (deriv Gamma s) := by simp [Function.comp_def]

theorem digamma_conj (s : ℂ) : digamma (conj s) = conj (digamma s) := by
  simp only [digamma_def, logDeriv_apply, deriv_Gamma_conj, Gamma_conj, map_div₀]

theorem one_sub_conj (t : ℝ) : (1 : ℂ) - ⟨1/2, t⟩ = conj (⟨1/2, t⟩ : ℂ) := by
  simp [Complex.ext_iff] <;> norm_num

theorem chiLog_real_on_critical_line (t : ℝ) :
    (chiLog ⟨1/2, t⟩).im = 0 := by
  have hhalf : (1 - (⟨1/2, t⟩ : ℂ)) / 2 = conj ((⟨1/2, t⟩ : ℂ) / 2) := by
    rw [map_div₀, Complex.conj_ofNat, one_sub_conj]
  have hd : digamma ((1 - (⟨1/2, t⟩ : ℂ)) / 2)
      = conj (digamma ((⟨1/2, t⟩ : ℂ) / 2)) := by
    rw [hhalf, digamma_conj]
  rw [← Complex.conj_eq_iff_im]
  simp only [chiLog, hd, map_sub, map_div₀, Complex.conj_ofNat, Complex.conj_conj,
             Complex.conj_ofReal]
  ring

end Scratch
