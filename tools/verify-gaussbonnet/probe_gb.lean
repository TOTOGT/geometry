-- tools/verify-gaussbonnet/probe_gb.lean
--
-- The single tracked probe for the discrete Gauss-Bonnet core.  CI runs THIS
-- file; there is no second copy in the workflow.  Two copies of one instrument
-- drift, and the dm3 probe already paid for that lesson once.
--
-- Three declarations, in dependency order.  tetra_gauss_bonnet is included
-- because the first two are statements about a structure that an empty
-- instance satisfies; the witness is part of the claim.

import Orthogenesis.Geometry.GaussBonnet
import Orthogenesis.Geometry.HexForm

#print axioms Orthogenesis.GaussBonnet.Triangulation.total_defect
#print axioms Orthogenesis.GaussBonnet.Triangulation.discrete_gauss_bonnet
#print axioms Orthogenesis.GaussBonnet.tetra_gauss_bonnet

#print axioms Orthogenesis.HexForm.Q_discriminant
#print axioms Orthogenesis.HexForm.hexToVec2_normSq
#print axioms Orthogenesis.HexForm.hexForm_nonneg
#print axioms Orthogenesis.HexForm.hexForm_eq_zero
#print axioms Orthogenesis.HexForm.hexNeighbors_form_one
