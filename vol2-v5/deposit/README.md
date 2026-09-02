# Principia Orthogona · Volume Two · V5

Contact Realization of Generative Transitions
Pablo Nogueira Grossi · G6 LLC · Newark, New Jersey
ORCID 0009-0000-6496-2186 · DOI 10.5281/zenodo.22117968
Supersedes V4 (10.5281/zenodo.21148424)

--------------------------------------------------------------------------
WHAT V5 CHANGES
--------------------------------------------------------------------------

1. Appendix A is generated from the Lean file rather than maintained beside
   it. Six of the twelve entries in the V4 table named declarations that have
   never existed in any version of VolumeTwo.lean -- two of them in the
   "proved" column. The file was in no lakefile target until 26 August 2026,
   so nothing had ever elaborated it; its first build reported eight errors,
   three in theorems the table listed as proved. It now builds, and all
   nineteen declarations are kernel-checked.

2. Main result (C) is restated as a SURJECTION. Four bifurcations map onto
   three Whitney types, two-to-one at A1. That is not a bijection, and
   section 5.2's own table said so while the abstract and Proposition 5.1
   said otherwise. The A_k indexing convention is now declared explicitly,
   because Arnold's convention places the fold at A2 rather than A1.

3. The Lean file path is corrected. The path cited in V2a-V4,
   AXLE/lean/VolumeTwo.lean, does not resolve.

4. New section 5.3 records the D6-equivariant DNLS results of Working
   Paper 77 and uses them to SHARPEN, not to discharge, the Neimark-Sacker
   obligation. WP-77 declines a ring-to-sphere bridge; the same gap separates
   the ring from the dm3 resonant orbit.

5. The reproducibility bundle dropped between V3 and V4 is restored.

--------------------------------------------------------------------------
FILES
--------------------------------------------------------------------------

principia_v5.pdf     The paper, 12 pages.
principia_v5.tex     Source. XeLaTeX; DejaVu Serif/Sans/Mono. Run twice.

VolumeTwo.lean       The Lean 4 file, as it stands at AXLE commit e44e8d1.
                     NOT the 11 kB skeleton deposited with V2a and V3.
verify-vol2.zip      run.sh, probe_vol2.lean, axiom_gate.py and its fixtures.

figures.py           Regenerates the figures from the exact section 4.3
                     equations.
certify_rstar.py     Numerical certificate for the inner-basin boundary
                     r* = 0.77594059 (DOP853, rtol 1e-12, atol 1e-14,
                     bisection tolerance 1e-7).
dashboard.html       Interactive exploration of the dm3 figures. RK4 integrator
                     over the exact section 4.3 equations, d3 rendering.

                     This is the copy served at
                     totogt.github.io/geometry/vol2-dashboard.html and is the
                     canonical one. Two other files carried the same name and
                     differed from it; they are being pointed at this one.

                     Its Lean status panel was corrected for V5. It had shown a
                     red OPEN badge on eigenvalue_limit -- a theorem that is
                     proved -- and displayed a proof body reading ":= by sorry"
                     that no longer exists in the file. It also named
                     thm_A_contact_realization, which is not a declaration; the
                     real one is thm_A_contact_realization_fold, whose
                     conclusion is True rather than a sorry.

--------------------------------------------------------------------------
REPRODUCING THE VERIFICATION
--------------------------------------------------------------------------

    git clone https://github.com/TOTOGT/AXLE && cd AXLE
    git checkout e44e8d1
    bash tools/verify-vol2/run.sh

This runs the gate's own fixtures first (an unchecked gate is not evidence),
builds the PrincipiaVol2 target at Lean v4.14.0 with Mathlib v4.14.0, asks
the kernel for the axiom dependencies of all nineteen declarations, and
refuses on sorryAx or on any axiom outside
{propext, Classical.choice, Quot.sound}. It also fails on an empty probe:
silence is not a pass.

Expected: GREEN, 19 declarations. Two of them -- thm_C_A1_surjective and
thm_C_not_bijective -- report "does not depend on any axioms".

The commit is pinned deliberately. A link to a branch resolves to whatever
is there today; a link to a commit resolves to what was checked when this
was written.

--------------------------------------------------------------------------
WHAT THE GATE CANNOT SEE
--------------------------------------------------------------------------

Passing an axiom check is necessary and not sufficient. A theorem whose
conclusion is True, or whose hypotheses already contain its conclusion, is a
true theorem and reports clean axioms. Three such are marked in Appendix A
and are named here so they cannot be missed:

  thm_A_contact_realization_fold   conclusion is True. Not a sorry -- which
                                   matters, because a sorry fails a kernel
                                   gate and True := by trivial passes one.
                                   Left in place with its OPEN comment.
  thm_B_threshold_equivalence      the biconditional is proved from
                                   assumptions on both sides; mu_max < 0 is
                                   a field of the DM3System structure.
  epsilon_zero_waddington          statement identical to toyModel_epsilon0.

Open with stated reasons rather than silence: Theorem B's real direction
(tau finite implies mu_max < 0) needs Has'minskii-style stochastic
stability; the Gronwall asymmetry needs the DOP853 numerics carried into the
kernel; integrability Levels 2d and 2d+t need Lie brackets of vector fields,
which a pointwise model cannot express at all.

--------------------------------------------------------------------------
SERIES
--------------------------------------------------------------------------

Series concept DOI      10.5281/zenodo.19379472  (all versions of Volume II)
Volume One              10.5281/zenodo.21146416  (V6)
dm3 Toy Model           10.5281/zenodo.21147306  (V3)
AXLE                    github.com/TOTOGT/AXLE
Reading copy            totogt.github.io/geometry/vol2-contact.html

License CC BY-NC-ND 4.0 · (C) 2026 Pablo Nogueira Grossi — G6 LLC
