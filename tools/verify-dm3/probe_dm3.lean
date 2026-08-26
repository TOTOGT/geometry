-- probe_dm3.lean — the dm³ invariants and the stability radius.
-- Asks the Lean KERNEL which axioms each named theorem actually depends on.
-- A theorem proved with `sorry` reports sorryAx here even though it compiled
-- without error, which is the whole point: compilation is not verification.
--
-- The three open obligations in G6Crystal.lean (S1 Arnold tongue,
-- S2 hexgrid collapse, S3 coord_coverage) are deliberately NOT named.

import Orthogenesis.Architecture.G6Crystal

-- §1 · canonical invariants  (T* = 2π, μ_max = −2, τ = 2)
#print axioms Orthogenesis.G6Crystal.dm3_Tstar_pos
#print axioms Orthogenesis.G6Crystal.dm3_mumax_neg
#print axioms Orthogenesis.G6Crystal.dm3_tau_pos
#print axioms Orthogenesis.G6Crystal.dm3_tau_eq_abs_mumax

-- §2 · the stability radius: value, DERIVATION, monotonicity
#print axioms Orthogenesis.G6Crystal.dm3_epsilon0
#print axioms Orthogenesis.G6Crystal.epsilon0_of_one
#print axioms Orthogenesis.G6Crystal.epsilon0_of_two
#print axioms Orthogenesis.G6Crystal.epsilon0_of_eq_third_iff
#print axioms Orthogenesis.G6Crystal.epsilon0_of_antitone
#print axioms Orthogenesis.G6Crystal.dm3_noise_tolerance
#print axioms Orthogenesis.G6Crystal.dm3_noise_tol_lt_one

-- §3 · dimensional derivation  (66 = 33·τ)
#print axioms Orthogenesis.G6Crystal.aspect_ratio_eq
#print axioms Orthogenesis.G6Crystal.aspect_ratio_encoded
#print axioms Orthogenesis.G6Crystal.layer_height_cubits

-- ToyModel.lean, added 2026-08-26. These are the two declarations
-- vol2-toymodel.html cites on its Lean badges, plus the facts they rest on.
#print axioms Orthogenesis.ToyModel.rdot_on_gamma
#print axioms Orthogenesis.ToyModel.zdot_on_gamma
#print axioms Orthogenesis.ToyModel.transEig_eq_deriv
#print axioms Orthogenesis.ToyModel.eigenvalue_neg_pos_z
#print axioms Orthogenesis.ToyModel.transEig_zero
#print axioms Orthogenesis.ToyModel.transEig_gt_neg_two
#print axioms Orthogenesis.ToyModel.transEig_strictAnti
#print axioms Orthogenesis.ToyModel.transEig_tendsto_muMax
#print axioms Orthogenesis.ToyModel.toyModel_tau
#print axioms Orthogenesis.ToyModel.toyModel_tau_eq_abs_muMax
#print axioms Orthogenesis.ToyModel.eps0_at_hessian_two
#print axioms Orthogenesis.ToyModel.eps0_at_hessian_three
#print axioms Orthogenesis.ToyModel.eps0_eq_third_iff
