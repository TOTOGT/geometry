-- tools/verify-catgt/probe_reeb.lean
--
-- Probe for catgt/lean/ReebFlow.lean, ReebFlowExtDeriv.lean and ReebBridge.lean
-- (added 2026-11-11). Twenty-one declarations: 8 + 11 + 2. A `#print axioms` line
-- proves the named theorem rests on no sorryAx; it does not prove it says what its name
-- says. In particular `reebOrbit_hasDerivAt` says the curve t |-> reebOrbit r0 th0 z0 t has
-- velocity `reebR` at every time. It does not prove uniqueness of integral curves.

import ReebBridge
import ReebFlowExtDeriv

#print axioms ReebFlow.reebFlow_zero
#print axioms ReebFlow.reebFlow_add
#print axioms ReebFlow.reebFlow_hasDerivAt
#print axioms ReebFlow.reebFlow_fderiv
#print axioms ReebFlow.reebFlow_preserves_alpha
#print axioms ReebFlow.reeb_interior_dAlpha
#print axioms ReebFlow.dAlpha_reebFlow
#print axioms ReebFlow.reebFlow_preserves_contactVol
#print axioms ReebFlowExt.deriv_line
#print axioms ReebFlowExt.dAlpha_formula
#print axioms ReebFlowExt.alphaLin_apply
#print axioms ReebFlowExt.omega_apply
#print axioms ReebFlowExt.omega_differentiableAt
#print axioms ReebFlowExt.hasFDerivAt_alphaCat
#print axioms ReebFlowExt.extDeriv_omega
#print axioms ReebFlowExt.dAlpha_eq_extDeriv
#print axioms ReebFlowExt.dAlpha_dr_dtheta
#print axioms ReebFlowExt.extDeriv_omega_dr_dtheta
#print axioms ReebFlowExt.contactVol_frame
#print axioms reebOrbit_eq_reebFlow
#print axioms reebOrbit_hasDerivAt
