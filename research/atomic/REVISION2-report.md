# Revision 2 — periodic-table model, regularized KK contact form, nodal Taylor expansion
Published 2026-11-26 for review. Euler CI untouched. Status tags: **[A]** analytical (hand-derived) · **[N]** numerical · **[L]** literature-supported · **[C]** conjectural · **[F]** formally verified (Lean). **No item below is [F]**; no Lean was written or run.
Reproduce: `research/atomic/{tf_convergence_wkb,lda_scf_pilot}.py`, `research/contact-nodal/{nodal_taylor,nodal_taylor_numcheck,regularized_contact_checks}.py`.

## 0. Correction of my own earlier numbers (important)
The first TF thresholds I reported (p,d,f,g = 2, 18, 64, 164) were **numerical artefacts and are retracted**. Cause: `eigh_tridiagonal(select='i')` on a log grid has absolute error ~ eps·‖A‖ with ‖A‖~1/(h r_min)² ≈ 1e13, i.e. 1e-3…10 Ha, larger than the near-threshold energies. Evidence: the thresholds moved from 2→8→4 for p between grids, and a hydrogen test gave −3.78 Ha instead of −2. Fix: (i) exact Sturm/inertia count of negative eigenvalues (no eigenvalue solve) for thresholds; (ii) shift-invert Lanczos for orbitals (hydrogen test now <1e-5 Ha). Also retracted: my statement that the WKB onset scales *exactly* as (l+½)³ — it does not (K below drifts 2.02→1.48).

## 1. Thomas–Fermi baseline — what is established
Model [A,N]: neutral TF potential V=−Zφ(r/b)/r, b=0.8853Z^(−1/3), φ from the TF ODE with φ'(0) found by bisection (φ(1,2,5,10)=0.424, 0.243, 0.0788, 0.0243 match the literature). Threshold definition: Z_c(l)=smallest integer Z for which the radial Schrödinger operator for angular momentum l has ≥1 bound state (E<0). No Latter tail (it adds a spurious −1/r tail binding Rydberg states of every l).

Convergence [N] (Sturm count; grid points N, outer radius r_max in bohr, r_min=1e-5/Z):

| N | r_max | p | d | f | g |
|---|---|---|---|---|---|
| 1400 | 400 | 7 | 26 | 67 | 135 |
| 2800 | 400 | 7 | 26 | 67 | 135 |
| 5600 | 400 | 7 | 26 | 67 | 135 |
| 5600 | 2000 | 7 | 26 | 67 | 135 |
| 11200 | 2000 | 7 | 26 | 67 | 135 |

Independent Langer–WKB onset [A+N] (action at E=0 equals π/2, no fit): 6.82, 26.29, 66.47, 134.86 — agrees with the quantum values to <0.2 (one integer). Z_c/(l+½)³ = 2.02, 1.68, 1.55, 1.48 (Landau–Lifshitz/Fermi ∝(l+½)³ is only asymptotic).
Numerical error is therefore not the explanation of the discrepancy. Comparison data (validation only, not fitted): first ground-state occupation p→B(5), d→Sc(21), f→La/Ce(57–58); g: not observed [L: Savelyev et al. list 5g as a candidate valence shell from about Z≈124 — see §5].
Residuals (model − observed): +2, +5, ≈+10, g n/a. Mechanisms, ordered by what I can support:
1. [A] **Existence ≠ occupation.** The criterion is whether an l-state is *bound* in the neutral-atom potential, not whether it is *occupied in the ground state*. Example: He already has bound 2p states though p is first occupied at B. So an overshoot of onset or an undershoot is expected even for an exact potential. This is a definitional gap, not an error that can be tuned away.
2. [C] No exchange/self-interaction treatment, no shell oscillations (TF density is smooth) — would change the potential at r~b.
3. [C] Relativistic contraction/expansion (matters for f,g, i.e. Z>57).
Not tested: (2),(3) individually.

## 2. Self-consistent pilot (what functional exactly)
[N] Spherical, non-relativistic, spin-unpolarized, integer occupations, Z=2…30. Potential = −Z/r + Hartree + **Dirac exchange only**, v_x = −(3ρ/π)^(1/3), e_x = −(3/4)(3/π)^(1/3)ρ^(1/3) (Kohn–Sham/Dirac LDA exchange, i.e. Xα with α=2/3). **No correlation, no gradient corrections, no empirical parameter.** It is not Hartree–Fock. Total energy E = Σnε − E_H − ∫ρv_x + E_x. Validation of the code (literature values quoted from memory): He −2.72363 Ha, Ne −127.4906 Ha — the known LDA-exchange-only values.
Configurations compared by **total energy** (never by orbital eigenvalues). Experimental configurations used only to grade the output:

| Z | competing configs | lowest total energy (this functional) | gap | experiment |
|---|---|---|---|---|
| 19 K | 4s¹ / 3d¹ | 4s¹ | 2.31 eV | [Ar]4s¹ ✔ |
| 20 Ca | 4s² / 4s¹3d¹ / 3d² | 4s² | 2.29 eV | 4s² ✔ |
| 21 Sc | 4s²3d¹ / 4s¹3d² / 3d³ | 4s²3d¹ | 1.69 eV | 4s²3d¹ ✔ |
| 24 Cr | 4s²3d⁴ / 4s¹3d⁵ | 4s²3d⁴ | **0.093 eV** | 4s¹3d⁵ ✘ (near-tie) |
| 29 Cu | 4s²3d⁹ / 4s¹3d¹⁰ | 4s¹3d¹⁰ | 2.12 eV | 4s¹3d¹⁰ ✔ |
| 30 Zn | 4s²3d¹⁰ / 4s¹3d¹⁰4p¹ | 4s²3d¹⁰ | 4.74 eV | ✔ |

Reading [N]: 5 of 6 correct without any inserted ordering rule; Cr wrong by 0.093 eV, far below the functional's accuracy. Plausible missing physics for Cr [C, untested]: spin polarization (Hund exchange of the half-filled d⁵s¹ shell is absent in a spin-unpolarized functional). Coverage: only K–Zn were run; the closings 54, 86, 118 were **not** retrodicted; relativistic and Hartree–Fock extensions were **not** run.
Fixed-occupation energies per Z do not by themselves give the first-appearance threshold of d: I did not scan Z continuously.

## 3. Crossing vs. local-minimum change vs. bifurcation (definitions and what was tested)
- Configurations are a discrete set {occupation vectors n}; each has an energy branch E_n(Z) (Z may be continued to real values). A *level crossing* is E_a(Z*)=E_b(Z*) with transversal slope (d/dZ)(E_a−E_b)≠0: first-order; the preferred configuration jumps. This is the generic behavior for discrete configurations [A].
- A *change of local minima* or a genuine *bifurcation* needs a continuous order parameter (e.g. fractional occupation n_3d∈[0,10] with E[n_3d;Z] smooth). A bifurcation (second-order-type) is a critical point where ∂²E/∂n²=0 at the minimum; a first-order transition is two coexisting minima exchanging global status.
- **Tested: none of these.** I computed only integer-occupation energies at a few Z. The data above say nothing yet about whether any transition is a crossing or a bifurcation. The Cr near-tie (0.093 eV) indicates the two branches are within functional error of crossing there. [C]
Cheap next test (not run): E_a−E_b as a function of continuous Z for K…Cu (sign change, slope), then with fractional occupations.

## 4. Does the orthogenetic selection principle add predictive content?
Stated honestly: **not at present.** As defined in the instruction ("selection of energetically preferred configurations"), selection = argmin of an energy functional, which is conventional energy minimization; it reproduces conventional results by construction and gives no extra prediction. The original η_k hierarchy had no generator (negative result retained). For TOGT to be a distinct predictive theory it needs a selection rule S that (i) is fixed *before* looking at data, (ii) differs from argmin E on some configurations, (iii) is graded against established configurations. Concrete graded test set (validation, not targets): Cr, Cu, Nb, Mo, Ru, Rh, Pd, Ag, La, Ce, Gd, Pt, Au, Ac, Th, Cm. If S either equals argmin or is not specified, the model is a geometric *representation* of known physics, not a new predictive theory. [C]

## 5. Superheavy literature (checked against primary pages, fetched this session) [L]
- Pyykkö, PCCP 13, 161 (2011): extended-average-level Dirac–Fock on atoms and ions; rough filling order 8s < 5g ≤ 8p½ < 6f < 7d < 9s < 9p½ < 8p3/2; ranges quoted from earlier Dirac–Slater work: 8p½+5g ≈121–143, 6f 144–154, 7d 155–164, 9s/9p½/8p3/2 165–172; QED dropped above Z=137; discusses 1s critical charge ≈170–175; says lifetimes above Z=118 are too short for chemistry. It does not classify the order against Madelung (my own observation: it departs from n+l by putting 8p½ before 6f/7d).
- Savelyev et al., arXiv:2301.01740 (Z=120–170; Dirac–Coulomb–Breit CI + model QED): I could read only part; the page I got does not state where 5g begins to fill; a summary lists 5g among candidate valence shells from ≈124. **Not verified** — do not cite Z≈121 or 124 as the start of g-filling.
- My TF onset for g (135) is a bound-state existence threshold, not a prediction of g occupation; g-shell appearances are theoretical, never observed. Electronic-configuration predictions say nothing about nuclear existence or stability.

## 6. Regularized contact form — independent proposition
**Proposition (analytical [A], numerically spot-checked [N]).** Let D⊂ℂ be open, f holomorphic on D, s=σ+it. On D×ℝ define η = dz + (Re f) d(Im f). Then (i) η is smooth on all of D, including zeros of f; (ii) dη = d(Re f)∧d(Im f) = |f′|² dσ∧dt (Cauchy–Riemann); (iii) η∧dη = |f′|² dz∧dσ∧dt; (iv) η is contact at (z,s) iff f′(s)≠0; at a zero of order m the coefficient vanishes to order 2m−2 (m=1 contact; m≥2 not contact; also not contact at any critical point of f); (v) the Reeb field is ∂_z wherever η is contact (η(∂_z)=1, ι_{∂_z}dη=0 — this holds identically, even where η is not contact).
**Separate the three layers:** smooth extension (always), contact nondegeneracy (off zeros of f′ — for f=ζ: at simple zeros of ζ yes; at a *multiple* zero of ζ no; and at zeros of ζ′ that are not zeros of ζ, no), global bundle structure (η is a connection form on a trivial R- or S¹-bundle over a non-compact base; no Boothby–Wang integrality constraint arises; the zero set of f′ is where the curvature degenerates).
**Speiser (Levinson–Montgomery 1974, Acta Math. 133)** [L]: RH ⇔ ζ′≠0 on 0<σ<½; so "η is contact on {0<σ<½}×ℝ" restates it. It gives no leverage on zeros and does not prove or advance RH. Known zeros of ζ are numerically simple at all computed heights [L], but simplicity of all zeros is an open conjecture [C].
Checks [N]: `regularized_contact_checks.py` — 11/11 pass (Jacobian = |ζ′|² at five points; simple zero ρ₁ has |ζ′|²=0.629; a zero of ζ′ at 2.463+23.298i has zero curvature; toy f=s² has J=4|s|², zero at the double zero; orders 1,2,3 scale as m²|s|^(2m−2)).
**Correction to earlier draft [kk-zeta-lift-analysis.md]:** it said the variant is "contact through ζ-zeros"; correct is "contact at *simple* zeros".

### Minimal Lean formalization requirements (spec only, UNVERIFIED, not written)
1. Model the 1-form by coefficients to avoid Mathlib's immature differential-form calculus: define the contact test as the 3×3 determinant det[η, ∂dη] on ℝ³ with η=(1,0,u·v_σ... explicit components) — i.e. a real function `contactCoeff f σ t : ℝ`.
2. Lemma (core): for `f : ℂ → ℂ` with `HasDerivAt f f' s`, the real Jacobian determinant of `(re ∘ f, im ∘ f)` at s equals `‖f'‖^2` (needs: `HasDerivAt → HasFDerivAt` over ℝ, matrix of multiplication by f′ on ℝ², `Complex.normSq`). Cauchy–Riemann in the form u_σ=v_t, u_t=−v_σ.
3. Lemma: for analytic f with a zero of order m at s₀, f′ vanishes there iff m≥2 (`AnalyticAt.order`, `deriv` of analytic functions).
4. Reeb statement: η(∂_z)=1, ι_{∂_z}dη=0 (pure algebra on coefficient vectors).
5. No ζ-specific facts needed for 1–4; Speiser's theorem is not in Mathlib and must remain a hypothesis `(h : RH ↔ ∀ s, 0<s.re → s.re<1/2 → deriv riemannZeta s ≠ 0)`, never an axiom.
These are elementary identities suitable for AXLE; none proves anything about zero locations.

## 7. Nodal Taylor expansion at z=i — complete result
Setting [A]: f(x+iy)=E*(z,s)=ξ(2s)E(z,s), complex-valued for general s, v=y−1, μ=s(s−1). Only three inputs: (E) y²(f_xx+f_yy)=μ f, (P) evenness in x, (S) invariance under z→−1/z. Solved symbolically to total degree 5 (`nodal_taylor.py`). With f(i)=0 the solution space has exactly two free parameters (c40, c41); put A=10c40+c41 and a=4A/(μ−10) (μ≠10, i.e. s(s−1)≠10; if μ=10 the denominators vanish and this derivation says nothing — separate case, not analysed).
- Degree 2: (a/2)(x²−v²) → common nodal directions v=±x for Re f and Im f separately, orthogonal. [A]
- Degree 3: −(a/2) v(3x²−v²) (fixed by a).
- Degree 4 (general a): [3μ c40 x⁴ − 30 c40 x⁴ + 12 μ c40 x²v² + 180 c40 x²v² + 3 μ c41 x²v² − 7 μ c40 v⁴ − 30 c40 v⁴ − μ c41 v⁴] / (3(μ−10)); it depends on c40 independently of a (c40 is free).
**Exceptional case a=0** (⇔ 10c40+c41=0): degrees 2 and 3 vanish and the **complete homogeneous quartic is f₄ = c40·(x⁴−6x²v²+v⁴) = c40·Re (x+iv)⁴** [A, derived by substitution, symbolic]. Hence nodal rays of Re f₄ (and Im f₄ for complex c40, same lines): cos4θ=0 ⇒ θ=π/8+kπ/4, **8 rays = 4 lines through i, 45° apart (orientation 22.5°, 67.5°, 112.5°, 157.5°), adjacent lines at 45°, alternate lines orthogonal**. This is a degenerate crossing of order 4 (vs. orthogonal pair of order 2). The degree-5 part when a=0 is printed by `nodal_taylor.py` but I did not simplify or analyse it. **Further degeneracy:** if additionally c40=0 then all coefficients through degree 5 vanish and the expansion would start at degree ≥6; I did not compute beyond degree 5, so more degeneracy is not excluded and I make no claim.
Numerical check [N] (`nodal_taylor_numcheck.py`): on the actual Eisenstein function at s=½+i·14.1347 (first zeta zero; there a=2c20≈2.4e-7, not exceptional), with only c20 and c40 as inputs, **all remaining coefficients to total degree 4 are predicted to relative accuracy 1.7e-14** (c21=−3a/2, c03=a/2, c02=−a/2, c22, c04, c13=c31=0, odd-x coefficients 0).
For the zero set of a complex f itself: Re f and Im f vanish on common quadratic tangent lines, but {f=0} is the intersection of two curves and is generically an isolated point, not a pair of curves; the 'two orthogonal nodal curves' picture holds for real f (critical line, F(t) real).
**Limits (explicit):** (1) this is local; it uses only symmetry and the eigen-equation, so it holds for *every* joint eigenfunction and therefore **cannot constrain where zeros of Λ_{Q(i)} or ζ lie**; (2) s=0.7+3i checks verify structural identities at that parameter only — they do not exhibit an off-line zero; (3) a=0 is a codimension-2 coincidence in a real one-parameter family; not expected, not excluded.

## 8. Open / next
- TF: continuous-Z crossing analysis; spin-polarized LDA to test the Cr hypothesis; Hartree–Fock and relativistic extensions (not run).
- Specify the TOGT selection rule S before any further atomic test (§4).
- Lean: spec in §6 is unwritten and untested.
