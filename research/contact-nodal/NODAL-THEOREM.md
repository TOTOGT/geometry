# Standalone theorem: local nodal structure at the elliptic point i (exceptional cases included)
Status tags: [A] analytical (proof below) · [N] numerical · nothing here is [F] (no Lean). Published 2026-11-26 for review. No implication for RH or for the location of zeros.

## Setting and hypotheses
Let U ⊂ ℍ be a connected open neighbourhood of i, μ∈ℂ, and f : U → ℂ with
- (H0) regularity: f real-analytic (true for E*(z,s)=ξ(2s)E(z,s): an eigenfunction of an elliptic operator with analytic coefficients, equivalently the Fourier–Bessel expansion converges locally uniformly with all derivatives);
- (H1) eigen-equation: y²(f_xx+f_yy) = μ f, z=x+iy, μ=s(s−1) (any s∈ℂ);
- (H2) parity: f(−x+iy)=f(x+iy) (reflection; the Fourier expansion has x only through cos 2πnx);
- (H3) modular invariance at i: f(−1/z)=f(z) for z near i;
- (H4) f ≢ 0 and f(i)=0.
Write w=x+i(y−1)=x+iv.

## Theorem
**(A) Classification of leading terms.** Under (H0)–(H4), let k≥1 be the vanishing order of f at i (finite, since f≢0 is analytic on connected U). Then k is **even**, and the lowest-degree Taylor part is f_k = α·Re(w^k) with α∈ℂ\{0}. In particular ∇f(i)=0, k=2 gives f₂=(a/2)(x²−v²) (a=2α), and k=4 gives f₄=α(x⁴−6x²v²+v⁴).
**(B) Exceptional quartic case, explicit.** If μ≠10 and a=0, then k≥4, and (H1)–(H3) force c41=−10c40 (the only free parameters through degree 5 are c40, c41), the degree-4 part is c40·Re(w⁴), the degree-5 part is **−2c40·Im(w⁵)**, hence k=4 iff c40≠0.
**(C) Nodal structure.** If in addition f is real-valued (e.g. s=½+it, where f is real) with leading term αRe(w^k), α∈ℝ\{0}, k even, then there is ε>0 such that {f=0}∩B_ε(i) is the union of exactly **k real-analytic curves through i**, pairwise transverse at i, with tangent lines at angles π/(2k)+jπ/k (j=0,…,k−1) from the x-axis. For k=2: two orthogonal lines at ±45°. For k=4: four lines at 22.5°+45°j. **c40≠0 is therefore sufficient for the full local nodal structure in this sense, not just for the tangent lines of the leading polynomial.**
**(D) Complex f (off-line s).** If f is genuinely complex, Re f and Im f each have leading term (Re α)Re w^k, (Im α)Re w^k and the same tangent lines whenever the coefficient is nonzero; the zero set {f=0} is the intersection of the two nodal sets and is not claimed to be anything other than a closed set containing i (generically an isolated point). No statement about existence of such zeros.

## Proof
(A) Order the Taylor series f=Σ_{j≥k} f_j in homogeneous polynomials in (x,v), f_k≢0. In (H1), y²=(1+v)². The lowest-degree homogeneous part of y²Δf−μf is Δf_k (degree k−2); μf contributes only from degree k. Hence Δf_k=0 (the case k=1 included: nothing to cancel). Real harmonic homogeneous polynomials of degree k in two variables are spanned by Re w^k, Im w^k (restriction of a harmonic function to the circle: Fourier modes cos kθ, sin kθ with ρ^k), so f_k=α Re w^k+β Im w^k, α,β∈ℂ. (H2): x↦−x sends w↦−w̄; Re(−w̄)^k=(−1)^k Re w^k and Im(−w̄)^k=(−1)^{k+1}Im w^k. Evenness of f forces evenness of its lowest part, so β=0 for k even and α=0 for k odd. (H3): −1/(i+w)=i−w−iw²+O(w³), i.e. the differential at i is −Id. Then f(σ(i+w))=f_k(−w)+O(|w|^{k+1}); equating lowest terms, f_k(−w)=f_k(w), so (−1)^k f_k=f_k. For k odd the surviving f_k=βIm w^k is odd and must vanish: contradiction. Hence k even, f_k=αRe w^k, α≠0.
(B) [A, symbolic: `nodal_taylor.py`, `nodal_theorem_checks.py`] Solving the linear system (E),(P),(S) to degree 5 with c00=0 leaves exactly c40,c41 free; a=4(10c40+c41)/(μ−10). With a=0 substitute c41=−10c40; the degree-4 part reduces exactly to c40(x⁴−6x²v²+v⁴) (check (1) PASS) and the degree-5 part to −2c40 v(v⁴−10v²x²+5x⁴) = −2c40 Im w⁵. Beyond degree 5 not computed.
(C) f(ρe^{iθ})=ρ^k g(ρ,θ), g=α cos kθ+ρ h(ρ,θ), h real-analytic on |ρ|<r×S¹ (f analytic, so Σ_{j>k}f_j(e^{iθ})ρ^{j−k−1} converges). The 2k zeros of cos kθ on [0,2π) are simple: ∂_θ g(0,θ_j)=−αk sin kθ_j=±αk≠0. Implicit function theorem: analytic θ_j(ρ), |ρ|<ε, with g(ρ,θ_j(ρ))=0. Away from the θ_j, |cos kθ|≥δ>0 so |g|≥|α|δ−Cε>0 for small ε; inside each neighbourhood ∂_θ g≠0, so zeros are unique. For k even, θ_j and θ_j+π are both roots, and ρ↦ρe^{iθ_j(ρ)} for ρ∈(−ε,ε) traces one analytic curve through i (immersed: velocity e^{iθ_j}≠0). The 2k roots give k curves; tangent angles are the roots of cos kθ mod π: π/(2k)+jπ/k. ∎
Numerical sanity [N]: 5 random (c40, remainder) trials, circles ρ=0.05, 0.01: exactly 8 sign changes (=2k) and root angles within 0.026 rad (ρ=0.05) / 0.005 rad (ρ=0.01) of π/8+jπ/4 (deviation shrinks ∝ρ, as the proof says).

## What is and is not established
- [A] Every nonzero local solution of (H0)–(H3) vanishing at i vanishes to even order with leading term αRe w^k. This classifies the possible leading terms; **which (k, α) actually occur at zeros of Λ_{ℚ(i)}** is not determined: formal solutions exist to the degrees computed (k=2 generic; k=4 needs a=0, a codimension-2 coincidence), but I did not compute degrees ≥6 (the attempted N=8 symbolic run was stopped, not completed), so existence of order ≥6 formal solutions is neither claimed nor excluded.
- [N] At the first zeta zero t₁ the measured a=2c20≈2.4e-7≠0, so k=2 there (not exceptional); all coefficients to degree 4 matched the family to 1.7e-14.
- μ=10 (s(s−1)=10, real s≈3.70 or −2.70) is excluded from (B); not analysed.
- Nothing here constrains where zeros of ζ, L(χ₋₄) or Λ_{ℚ(i)} lie: (A)–(D) hold for every joint eigenfunction with these symmetries. Local symmetry ≠ global zero location.
