import Mathlib

/-
NielsenLeptonDeviation.lean -- chapter 8, item C12. UNTESTED: written 2026-10-26 without a toolchain.
Run:  bash tools/leancheck.sh --audit book26/NielsenLeptonDeviation.lean   and report the output unchanged.
What it states: the relative deviation the preprint's own script prints for each charged lepton mass
(0.22%, 0.24%, 0.23%) is larger than the relative PDG uncertainty by the stated factors, so "within PDG
uncertainties" cannot hold for those printed deviations. Rational arithmetic only. It does NOT compute the
masses (that needs exp and zeta(3); see book26/nielsen-lepton-table.py, 40-digit mpmath), and does not show
the printed deviations are the formula's true output.
-/

namespace NielsenLepton

/-- Relative PDG uncertainty of the electron mass: 1.6e-10 / 0.51099895069. -/
def relUncE : ℚ := (16/10^11) / (51099895069/10^11)
/-- Muon: 0.0000023 / 105.6583755. -/
def relUncMu : ℚ := (23/10^7) / (1056583755/10^7)
/-- Tau: 0.09 / 1776.93. -/
def relUncTau : ℚ := (9/100) / (177693/100)

/-- 0.22% exceeds the electron's relative uncertainty by more than a factor 10^6. -/
theorem electron_dev_exceeds : (22:ℚ)/10000 > 10^6 * relUncE := by
  unfold relUncE; norm_num

/-- 0.24% exceeds the muon's relative uncertainty by more than a factor 10^5. -/
theorem muon_dev_exceeds : (24:ℚ)/10000 > 10^5 * relUncMu := by
  unfold relUncMu; norm_num

/-- 0.23% exceeds the tau's relative uncertainty by more than a factor 40. -/
theorem tau_dev_exceeds : (23:ℚ)/10000 > 40 * relUncTau := by
  unfold relUncTau; norm_num

end NielsenLepton

#print axioms NielsenLepton.electron_dev_exceeds
#print axioms NielsenLepton.muon_dev_exceeds
#print axioms NielsenLepton.tau_dev_exceeds
