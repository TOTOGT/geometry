# Kaluza–Klein (Boothby–Wang) lifts of the zeta phase plane and the arithmetic contact form

Principia Orthogona, verification note, 2026-11-26. Script: `kk_zeta_lift_checks.py` in this folder. It ran 26 checks, 26 passed, exit code 0, in about 60 s.

**Scope.** RH is not proved, approached, or reformulated in a new way by anything here. The one RH-equivalent statement below (§5) is Speiser's 1934 criterion restated, and it is labelled that way.

Labels: **HAND-DERIVED**, **NUMERICALLY CHECKED** (check ID from the script), **KNOWN-LITERATURE**, **CONJECTURE**, **OPEN**.

---

## 0. What the series actually defines

These were read from `TOTOGT/geometry` main, through WebFetch summaries of the raw HTML.

- **Book 4 Ch 11, Def 11.1:** α_arith = c(σ,t) dŨ − g(σ,t) dṼ, with Ũ + iṼ = log ζ(σ+it).
  - c = Σ Λ(n) n^{−σ} cos(t log n) and g = Σ Λ(n) n^{−σ} sin(t log n). Equivalently, **−ζ′/ζ = c − i g**.
  - Both series converge absolutely for σ > 1. For σ ≤ 1, c and g come from meromorphic continuation, and σ = 1 is not treated.
  - σ is a frozen parameter. The ambient space is 3D. Ch 11 §11.4 writes it as ℝ³_(U,V,t), but the form is written in (Ũ, Ṽ); this inconsistency is in the source. I work on ℝ³_(Ũ,Ṽ,t).
  - Ch 11 states (∂_tŨ, ∂_tṼ) = (−g, −c) and α∧dα = −W dŨ∧dt∧dṼ, with W = c g_t − g c_t. It also says W changes sign for σ > 1, with a minimum of about −0.004 at σ = 2.
- **rh-paper.html, Def 4.1** is a different form: α = dV − g dU on ℝ³_(U,V,t), where U + iV = ζ itself and there is no c. §4.4 calls it the one-coefficient special case of c dŨ − g dṼ. I treat both forms.
- **Ch 14, correction of 2026-10-19.**
  - Withdrawn: "Global Positivity ⇔ RH" and the claim that one direction was established. Global Positivity is now a CONJECTURE.
  - Withdrawn as false: "RH ⇔ α_arith∧dα_arith ≠ 0 everywhere", because ∂_t g changes sign for σ > 1, where ζ has no zeros.
  - A later correction (2026-11-15) adds that the sign-of-W version of Global Positivity is false as written.
- **Book 5 ch V:** η = dy + κA on a circle bundle over a 4D base, with η∧dη∧dη = κ² dy∧F∧F. η is contact exactly where F∧F ≠ 0, and the Reeb field is ∂_y. The chapter itself calls this standard Boothby–Wang and makes no zeta claim.

---

## 1. α_arith: contact 3-form and Reeb field

Coordinates are (Ũ, Ṽ, t) with σ fixed, so c and g are functions of t only.

**1.1 Derivatives (HAND-DERIVED; S1).**
- dα = c_t dt∧dŨ − g_t dt∧dṼ.
- α∧dα = −(c g_t − g c_t) dŨ∧dt∧dṼ = −W dŨ∧dt∧dṼ.
- This confirms Ch 11 Prop 11.1.

**1.2 Closed form of W (HAND-DERIVED; N2A, N2B, residual < 1e−29).** Write L = ζ′/ζ and ψ = c + i g = −conj(L). Then

  W = Im(conj(ψ) ψ_t) = −Re(conj(L) · L′) = −|L|² · Re(L′/L).

W is |L|² times the t-rate of the phase of −ζ′/ζ along the vertical line. Its t-mean for σ > 1 is Σ Λ(n)² log n / n^{2σ} > 0, which agrees with Ch 11.

**1.3 Reeb field (HAND-DERIVED; S2, S3 symbolic, N3A, N3B numeric).** Wherever W ≠ 0:

  **R = (g_t ∂_Ũ + c_t ∂_Ṽ) / W.**

- Under the generic assumption (c_t, g_t) ≠ (0, 0), R is unique and has **zero ∂_t component**. The Reeb field is therefore **not ∂/∂t**.
- Because the coefficients depend only on t, each Reeb orbit is a straight line inside a fixed-t plane, with direction (g_t, c_t).

**1.4 Where it fails to be contact.**
- **On the planes {t : W(σ,t) = 0}.** These planes are non-empty for σ > 1. At σ = 2, W takes both signs, so it has zeros (N8, NUMERICALLY CHECKED).
  - The minimum of W is −0.00313 on t ∈ [0, 60] and −0.00591 near t ≈ 118.92 on [0, 200].
  - Ch 11's figure of "about −0.004" therefore depends on the t-range used. The range is unstated in the source, so I flag this as unverified rather than wrong.
- **At zeros of ζ′.** There c = g = 0, so α = 0 and α is not even a non-vanishing 1-form.
- **At zeros of ζ.** There c and g blow up like −1/(s−ρ), so α is singular.

**1.5 rh-paper Def 4.1 (HAND-DERIVED; S5, N7).** For α = dV − g dU:
- α∧dα = −g_t dV∧dt∧dU, and the Reeb field is ∂_V.
- At σ = 2, ∂_t g takes both signs, with a minimum of −0.392 (N7). This reproduces the stated reason for the 2026-10-19 withdrawal.

---

## 2. Is α_arith of Kaluza–Klein / Boothby–Wang form dz + κA over a 2D base?

### 2.1 Locally: yes, trivially, on each slab where W ≠ 0 (HAND-DERIVED; S4)

Define

  z = c Ũ − g Ṽ,  w = c_t Ũ − g_t Ṽ  (with t kept as a coordinate).

Then **α_arith = dz − w dt** exactly, and det ∂(z,w)/∂(Ũ,Ṽ) = −W.

- On each t-slab where W ≠ 0, (z, w, t) is a global chart on ℝ²×(slab).
- In that chart α is the standard Darboux form: the fibre is z, the base is (t, w), A = −w dt, and F = dA = dt∧dw.
- F is nowhere zero in this chart, so "contact iff F ≠ 0" holds **tautologically**.
- This is just Darboux's theorem made explicit. Every contact form is locally dz + A(x,y) in Reeb flow-box coordinates, because L_R α = 0 automatically (KNOWN-LITERATURE). So the local statement carries no information.

### 2.2 Globally across the W = 0 planes: no, in any coordinates (HAND-DERIVED)

**Claim.** No vector field X satisfies α(X) = 1 and ι_X dα = 0 at a point where W = 0 and (c_t, g_t) ≠ 0.

**Proof.**
1. dα = dt∧(c_t dŨ − g_t dṼ) has rank 2.
2. Its kernel is spanned by (g_t, c_t, 0).
3. α evaluates on that kernel vector to c g_t − g c_t = W = 0.

**Consequence.** A KK form dz + A(x,y) always has such an X, namely ∂_z, everywhere, including where F = 0. So α_arith is **not** of the form dz + A on any neighbourhood that meets a W = 0 plane at such a point.

The obstruction is that, on W = 0, the characteristic line of dα lies inside ker α. That is a different degeneration from KK's "F = 0". KK degenerates with the fibre still transverse to ker η; here the would-be fibre becomes Legendrian.

### 2.3 Not a Boothby–Wang circle bundle (HAND-DERIVED)

Boothby–Wang needs a Reeb flow that generates a free S¹-action (a regular contact form).
- On ℝ³ the Reeb orbits are straight lines, so they are never closed.
- Even with Ṽ = arg ζ taken mod 2π, an orbit closes only when its direction is parallel to ∂_Ṽ, i.e. g_t = 0. That happens on isolated t-planes, where the period is 2π|g|.
- So there is no circle action and no Boothby–Wang structure.

### 2.4 The one-coefficient form is literally KK, with a degenerate F (HAND-DERIVED; S5)

rh-paper Def 4.1 has the form dV + A with:
- fibre V (Re/Im of ζ, not a circle),
- base (U, t),
- A = −g(t) dU, F = g_t dU∧dt.

It is contact iff ∂_t g ≠ 0. The KK degeneracy locus {∂_t g = 0} is exactly the locus behind the withdrawn "RH ⇔ contact everywhere", and it is non-empty for σ > 1 (N7). In KK language the withdrawal reads: "F has zeros where ζ has none."

### 2.5 A natural KK lift of the zeta plane (HAND-DERIVED; S7, N4, N5)

On (σ, t, z) take

  **η = dz + Ũ dṼ = dz + log|ζ| · d arg ζ**  (gauge-equivalent to dz − Ṽ dŨ via z ↦ z + ŨṼ).

- **Well defined.** A = Ũ dṼ is single-valued on ℂ ∖ ({zeros of ζ} ∪ {1}), because d arg ζ is a single-valued closed form. The fibre z can be ℝ or S¹. The base is non-compact, so prequantization integrality does not constrain anything.
- **Curvature.** log ζ is holomorphic, so its Jacobian is |(log ζ)′|²:

  F = dŨ∧dṼ = |ζ′/ζ|² dσ∧dt ≥ 0,  η∧dη = |ζ′/ζ|² dσ∧dt∧dz.

  Residuals on both grids are below 1e−30 (N4A, N4B).
- **Reeb field:** ∂_z.
- **Degeneracies.**
  - F = 0 exactly at zeros of ζ′. N9 found ρ′ = 2.463161869 + 23.29832049 i, in σ > 1 where ζ has no zeros, with F = 1e−73 there.
  - F is singular, with infinite flux (∫|ζ′/ζ|² ~ ∫ r^{−2} r dr), at zeros of ζ and at s = 1.
- **Zeta-image variant.** η′ = dz + U dV with U + iV = ζ gives F = |ζ′|² dσ∧dt (N5).
  - It is smooth and contact **through** the zeros of ζ: at ρ₁ = ½ + 14.1347 i, F = |ζ′(ρ₁)|² = 0.6291 > 0 (N10).
  - Zeros of ζ are invisible to η′.

**What η carries that α_arith does not:**
- It uses the full s-plane, both σ and t, and its curvature is the area density of the map s ↦ log ζ(s).
- α_arith freezes σ and sees only the boundary data c, g on one vertical line.
- Conversely, α_arith's contact density W involves L′, which η never sees.

**Exact link between the two (HAND-DERIVED; N6A, N6B).** Let α̂ = c(σ,t) dŨ − g(σ,t) dṼ with σ now unfrozen, and pull it back along Φ(σ,t) = (log ζ(σ+it), σ, t). Then

  Φ*α̂ = Re(−conj(L) · L ds) = −|ζ′/ζ|² dσ,  hence F_η = −(Φ*α̂)∧dt.

The t-component vanishes, which is the Legendrian property of the curve. The σ-component is minus the KK curvature density. The only object the two constructions share is L = ζ′/ζ.

**Information content (HAND-DERIVED).** F = |f′|² dσ∧dt for any holomorphic f. It is non-negative because holomorphic maps preserve orientation, and it vanishes only at critical points of f. Contactness of the lift is the pointwise statement "f′ ≠ 0". The construction encodes holomorphy and the zero set of ζ′, and nothing about where the zeros of ζ are beyond what ζ′ ≠ 0 already says.

---

## 3. Numerical verification (NUMERICALLY CHECKED)

**Setup.** mpmath at 30 digits; mp.diff for derivatives; local branches of log ζ to avoid arg cuts.
- Region A: σ ∈ {1.05, …, 3} (6 values) × t ∈ [0.5, 40] (9 values).
- Region B: σ ∈ {0.3, …, 0.7} (5 values) × t ∈ [13.6, 14.6] (6 values). The closest grid point to ρ₁ is at distance ≈ 0.065.

| ID | Identity | Max residual A / B |
|---|---|---|
| S1–S7 | symbolic (sympy, explicit exterior algebra) | exact |
| N0 | c, g series = (Re, −Im)(−ζ′/ζ), σ ∈ {2, 2.5, 3}, N = 2·10⁵ | 4.3e−6 (within tail bound) |
| N1 | (Ũ_t, Ṽ_t) = (−g, −c) | 1e−31 / 2e−31 |
| N2 | W = −Re(conj(L) L′) | 3e−31 / 8e−31 |
| N3 | Reeb (g_t, c_t, 0)/W | 2e−31 / 3e−30 |
| N4 | dŨ∧dṼ = \|ζ′/ζ\|² dσ∧dt | 3e−31 / 3e−31 |
| N5 | dU∧dV = \|ζ′\|² dσ∧dt | 2e−31 / 2e−31 |
| N6 | Φ*α̂ = −\|ζ′/ζ\|² dσ | 1e−31 / 2e−31 |
| N7, N8 | ∂_t g and W change sign at σ = 2 | min −0.392, −0.00313 |
| N9 | zero of ζ′ at 2.4632 + 23.2983 i, F ≈ 1e−73 | — |
| N10 | \|ζ′(ρ₁)\|² = 0.6291 | — |
| N11 | winding count of ζ′: 0 zeros in [0.05, 0.45]×[10, 60], 7 zeros in [0.55, 3]×[10, 60] | integer to 1e−20 |
| N12 | 4D Pfaffian = \|ζ′/ζ(s₁)\|² \|L′/L(s₂, χ₋₄)\|² at 5 points (both regions) | 2e−33 |

**Limitations.**
- The grids are finite and avoid the exact zeros.
- N0 is not run for σ < 2, because the series tail converges too slowly near σ = 1.05 to give a useful bound.
- N11 covers a finite box. It is consistent with Speiser's theorem but proves nothing about RH.
- N12 assumes the product structure of the 4D form. Its real numerical content is the two 2D Jacobians.

---

## 4. Verdict

**(a) Is a KK lift of the zeta plane well defined?** Yes (HAND-DERIVED, NUMERICALLY CHECKED).
- η = dz + log|ζ| d arg ζ is a globally defined Boothby–Wang-type form over ℂ ∖ ({zeros of ζ} ∪ {1}), with Reeb field ∂_z and curvature F = |ζ′/ζ|² dσ∧dt. It is contact exactly off the zeros of ζ′.
- The variant dz + Re ζ d Im ζ is smooth everywhere except s = 1, and is contact exactly off the zeros of ζ′.
- Both are standard prequantum/KK constructions for a pulled-back area form (KNOWN-LITERATURE: Boothby–Wang 1958, Ann. Math. 68). Nothing in them is specific to ζ beyond holomorphy.

**α_arith itself:**
- Its Reeb field is (g_t, c_t, 0)/W, not ∂_t.
- It is of KK form only as a trivial Darboux chart (dz − w dt) on each slab where W ≠ 0.
- It is not of KK form in any coordinates across the planes W = 0, where the characteristic line of dα falls into ker α.
- It is never a Boothby–Wang circle bundle, because its Reeb orbits are non-closed lines.
- The one-coefficient form dV − g dU (rh-paper Def 4.1) is literally KK with F = g_t dU∧dt. Its F-degeneracy is exactly the sign-change locus behind the 2026-10-19 withdrawal.

**(b) Relation to the Book 5 condition F∧F ≠ 0.** Book 5 needs a 4D symplectic base. A natural candidate is (s₁, s₂) ↦ (log ζ(s₁), log L(s₂, χ₋₄)), using the two factors of ζ_{ℚ(i)} = ζ · L(·, χ₋₄) (KNOWN-LITERATURE).
- With ω = dŨ₁∧dṼ₁ + dŨ₂∧dṼ₂ pulled back: ω∧ω = 2 |ζ′/ζ(s₁)|² |L′/L(s₂)|² d⁴x (HAND-DERIVED; N12).
- So η₅ = dy + A₁ + A₂ is contact iff ζ′(s₁) ≠ 0 and L′(s₂, χ₋₄) ≠ 0, with singularities at the zeros of each factor.
- This is a product of two independent 3D lifts with no arithmetic coupling.
- The arithmetically meaningful diagonal s₁ = s₂ (where the Dedekind zeta actually lives) is a 2-surface, and any 4-form, including F∧F, restricts to zero there. The Book 5 condition is therefore either a pointwise product condition or vacuous.
- For a general holomorphic Ψ: ℂ² → ℂ², Ψ*(ω∧ω) = |det_ℂ DΨ|² ω∧ω (KNOWN-LITERATURE). The condition is again "non-critical point", which is holomorphy-level information.

**(c) What any RH-relevant content would require, and why none is present.**
- The only RH-equivalent statement available is KNOWN-LITERATURE: **Speiser (1934, Math. Ann. 110)**, with an analytic proof and quantitative form by **Levinson–Montgomery (1974, Acta Math. 133)**. RH holds iff ζ′(s) ≠ 0 for 0 < Re s < ½.
- Through §2.5 this restates as: "dz + Re ζ d Im ζ is contact on {0 < σ < ½} × fibre ⇔ RH." That is Speiser's criterion in new notation. It is not new, and it gives no leverage, because contactness here is literally the pointwise non-vanishing of |ζ′|².
- To be RH-relevant, a construction would need a mechanism that controls the zeros of ζ′ (or of ζ) in the strip using information beyond holomorphy and the Dirichlet-series data. Examples would be a global positivity, rigidity, or compactness argument (for instance one forcing a Reeb flow to be regular, or a curvature integral to be quantized) that is proved rather than conjectured.
- No such mechanism exists here:
  - The KK curvature is |f′|² for whatever holomorphic f is chosen.
  - The Boothby–Wang structure exists only on non-compact bases with non-compact or freely chosen fibres.
  - α_arith's contact locus fails in σ > 1, where ζ has no zeros (N7, N8).
- **RH is not proved, and nothing in this note is evidence for it.**

**OPEN.** Whether any compactification of the s-plane, for example a quotient by the functional-equation involution s ↦ 1 − s, could carry a regular Boothby–Wang structure with arithmetic content. Nothing above suggests one does.


## Erratum (Revision 2)
Where this note says the variant dz + Re ζ d Im ζ is 'contact through ζ-zeros', the correct statement is: it is smooth through every zero of ζ and **contact only at simple zeros** (ζ′≠0). At a multiple zero ζ′=0 and η∧dη=|ζ′|² dz∧dσ∧dt vanishes. See ../atomic/REVISION2-report.md §6.
