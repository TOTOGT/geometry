# DM3QUIVERS — verification bundle (v0.2, 5 Oct 2026)

Companion to *Affine orthogonal quiver varieties at δ and 2δ, and their contact links* (P. N. Grossi), written on
V. Pinot, *Quiver varieties for affine orthogonal quivers*, arXiv:2609.39434.

Requirements: Python 3 with numpy, scipy, sympy (`python3 -m pip install numpy scipy sympy`); Lean 4 (core only, no Mathlib).

| file | checks | runtime |
|---|---|---|
| verify_Dtilde_relation_numeric.py | Prop. 3.4: samples mu^{-1}(0) ∩ SRep for (D~_{2n-1},a) and (D~_{2n-2},v), n=3,4,5, and finds the relation among x=det C3, y=tr(C1C2), z=tr(C1C2C3) by SVD. Saved output: .out | ~10 min |
| verify_ade_types.py | Milnor numbers of the D~-row polynomials; homogeneity defect of the printed (D~_{2n-1},a) relation | seconds |
| verify_2delta_index2.py | Prop. 4.2: invariant-ring identities for the involutions iota_1, iota_2 | seconds |
| verify_quaternionic_SRep.py | Lemma 5.2: sigma commutes with J; mu_R, mu_C land in k^b | seconds |
| verify_seifert.py | Table 2: orbifold Euler characteristic identity; group orders | seconds |
| DM3Quivers_Check.lean | `lean DM3Quivers_Check.lean`: arithmetic skeleton (weights, Milnor–Orlik numerator, orders). No geometric statement. | 2 s |

Conventions: standard signed space (all J_i = identity), sigma(v)_a = s(a) v_{tau a}^T; moment map
mu_i = sum_{h(a)=i} v_a v_{a*} - sum_{t(a)=i} v_{a*} v_a, as in Pinot, Def. 2.9.
Numerical results are evidence, not proofs.
