-- tools/verify-catgt/probe_catgt.lean
--
-- The single tracked probe for catgt/lean/CatGT_Main.lean (2026-09-21). CI runs THIS
-- file; there is no second copy in the workflow.
--
-- Eighteen declarations (5 added 2026-09-23: §4b normalisation of r*). A `#print axioms` line proves the named theorem rests on
-- no sorryAx; it does not prove the theorem says what its name says. In particular
-- `helical_selectivity` is the monotonicity step under Theorem 1(iii), not Theorem 1.

import CatGT_Main

#print axioms ipr_between_zero_and_one
#print axioms criticalRadius_pos
#print axioms criticalRadius_antitone
#print axioms helical_selectivity
#print axioms selectivityFactor_eq
#print axioms dnlsNorm_nonneg
#print axioms reeb_alpha_eq_one
#print axioms reeb_orbit_advances
#print axioms catgt_dm3_disk
#print axioms ensemble_scaling_forms_diverge
#print axioms relaxStep_fixed
#print axioms relaxStep_contracts
#print axioms relax_iterate_dist
#print axioms criticalRadius_eq_fixedAmplitude
#print axioms sech_width_fixed_norm
#print axioms criticalRadiusNorm_pos
#print axioms criticalRadiusNorm_antitone
#print axioms selectivityFactorNorm_eq
