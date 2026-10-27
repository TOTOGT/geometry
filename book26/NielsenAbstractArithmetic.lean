import Mathlib

/-
NielsenAbstractArithmetic.lean -- exact checks of the abstract's arithmetic, for chapter 8 (item C4).
STATUS: UNTESTED. Written 2026-10-26 without a Lean toolchain; the Python script
nielsen-abstract-arithmetic.py ran and gives the same numbers. Run:
    bash tools/leancheck.sh --audit book26/NielsenAbstractArithmetic.lean
and report the output unchanged. Real.pi_gt_d2 and Real.pi_lt_d2 are from memory; if they do not
exist, try Real.pi_gt_314 and Real.pi_lt_315.
Each theorem says only what it states: arithmetic on numbers printed in the abstract. None says the
formulas follow from the paper's geometry.
-/

namespace NielsenAbstract

/-- The three neutrino masses in the abstract (meV) sum to 59.282 meV. -/
theorem nu_mass_sum : (970:ℚ)/1000 + 8708/1000 + 49604/1000 = 59282/1000 := by norm_num

/-- m2^2 - m1^2 = 74.888364 meV^2, i.e. 7.4888364e-5 eV^2. -/
theorem delta_m21_meV2 : ((8708:ℚ)/1000)^2 - ((970:ℚ)/1000)^2 = 74888364/1000000 := by norm_num

/-- m3^2 - m1^2 = 2459.615916 meV^2, i.e. 2.459615916e-3 eV^2. -/
theorem delta_m31_meV2 : ((49604:ℚ)/1000)^2 - ((970:ℚ)/1000)^2 = 2459615916/1000000 := by norm_num

/-- 1 - (mW/mZ)^2 with the abstract's masses (80.3695 and 91.1878 GeV) lies in (0.22320, 0.22321). -/
theorem onshell_sin2_bounds :
    (22320:ℚ)/100000 < 1 - ((803695:ℚ)/911878)^2 ∧ 1 - ((803695:ℚ)/911878)^2 < 22321/100000 := by
  constructor <;> norm_num

/-- 3/(4 pi) lies in (0.2380, 0.2389). -/
theorem three_over_four_pi_bounds :
    (2380:ℝ)/10000 < 3/(4*Real.pi) ∧ 3/(4*Real.pi) < 2389/10000 := by
  have h1 : (3.14:ℝ) < Real.pi := Real.pi_gt_d2
  have h2 : Real.pi < (3.15:ℝ) := Real.pi_lt_d2
  have hp : 0 < 4*Real.pi := by linarith
  constructor
  · rw [lt_div_iff₀ hp]; linarith
  · rw [div_lt_iff₀ hp]; linarith

/-- The abstract's tree-level on-shell value and its 3/(4 pi) differ by more than 0.0147. -/
theorem threefourpi_vs_onshell_gap :
    (147:ℝ)/10000 < 3/(4*Real.pi) - (1 - ((803695:ℝ)/911878)^2) := by
  have hb := three_over_four_pi_bounds.1
  have ho : (1 - ((803695:ℝ)/911878)^2) < 22321/100000 := by norm_num
  linarith

end NielsenAbstract

#print axioms NielsenAbstract.nu_mass_sum
#print axioms NielsenAbstract.delta_m21_meV2
#print axioms NielsenAbstract.delta_m31_meV2
#print axioms NielsenAbstract.onshell_sin2_bounds
#print axioms NielsenAbstract.three_over_four_pi_bounds
#print axioms NielsenAbstract.threefourpi_vs_onshell_gap
