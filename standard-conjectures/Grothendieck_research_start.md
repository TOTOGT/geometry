# Grothendieck standard conjectures: a concrete starting point

Research setup, 11 November 2026. Prepared for Pablo Nogueira Grossi.

**Outcome:** an explicit proof of the Hodge-type positivity and inverse-Lefschetz statements for the classical example P² × P², with every ample rational polarization; an exact symbolic verifier; and an identified failure of a proposed extension using Frobenius alone. This is a reconstruction of a known case, not a new case of the general conjectures. No connection to dm³ has been proved.

## 1. Fix the target

Grothendieck proposed several standard conjectures. The two relevant here are:

* **Lefschetz type B:** inverse hard-Lefschetz maps on cohomology are induced by algebraic correspondences.
* **Hodge type:** the signed intersection form on primitive algebraic classes is positive definite.

Fix a smooth projective geometrically connected variety X of dimension d over a finite field, pass to its algebraic closure, choose an ample divisor class h, and fix ℓ different from the characteristic. Work with rational algebraic cycles modulo ℓ-adic homological equivalence, denoted A^r_ℓ(X). This choice is deliberate: numerical and homological equivalence are not silently identified.

Let L denote multiplication by h and, for 0 ≤ r ≤ d/2, put

\[
P^r_\ell(X)=\ker\bigl(L^{d-2r+1}:A^r_\ell(X)\to A^{d-r+1}_\ell(X)\bigr).
\]

The positivity target is

\[
Q_{r,h}(z,w)=(-1)^r\deg(z\,w\,h^{d-2r}),\qquad
Q_{r,h}(z,z)>0\quad\text{for }0\ne z\in P^r_\ell(X).
\]

The output of the degree pairing is rational, so the inequality uses the usual order on Q, not an imagined order on Q_ℓ. This formulation follows Milne's 2001/2002 account [2].

For a fourfold and codimension two, the target simplifies to

\[
\operatorname{cl}_\ell(hz)=0,\quad \operatorname{cl}_\ell(z)\ne0
\quad\Longrightarrow\quad \deg(z^2)>0.
\]

This is the precise first general statement to investigate. It is not established below for arbitrary fourfolds.

## 2. Update the literature before choosing a supposedly open case

Milne's author page records October 7 and October 14, 2026 updates concerning the Hodge conjecture for CM abelian varieties and its consequences [3]. His November 10 report states the Hodge standard conjecture for all abelian varieties as Theorem 3.5; its table explains that his earlier conditional implications have become unconditional through the 2026 work [4]. A University of Michigan seminar announcement independently documents discussion of these consequences [5].

These are primary-source reports. This session checked their statements, not the complete new proofs. They concern abelian varieties; they are not a proof for every smooth projective variety. A research target described simply as “prove Hodge positivity for abelian varieties” would therefore be outdated on the sources checked here.

There is also a sign issue in the displayed formula in §3.6 of the November report: it omits the factor (-1)^r shown in Milne's earlier precise formulation [2]. We use the signed formula above. The negative primitive divisor self-pairing in §3 below demonstrates why the sign is necessary under the ordinary intersection convention.

## 3. A complete known benchmark, with a nonzero primitive space

Take

\[
X=\mathbf P^2\times\mathbf P^2,
\qquad CH^*(X)_\mathbf Q=\mathbf Q[a,b]/(a^3,b^3),
\qquad\deg(a^2b^2)=1.
\]

Here a and b are the pulled-back hyperplane classes. The Chow-ring presentation follows from the projective bundle formula [6]. The same monomials give the usual Weil-cohomology basis of this product, so here all cohomology is algebraic and the cycle class map is injective. That special property is not assumed for a general X.

Every ample rational class is h = s a + t b with s,t > 0 rational. We retain s,t as symbols throughout; checking a few polarizations would not prove the statement for every polarization.

### Primitive codimension one

For z = x a + y b,

\[
h^3z=3st(tx+sy)a^2b^2.
\]

Thus P¹ is spanned by p₁ = s a − t b. Direct multiplication gives

\[
-\deg(h^2p_1^2)=2s^2t^2>0.
\]

### Primitive codimension two

For z = x a² + y ab + u b²,

\[
hz=(tx+sy)a^2b+(ty+su)ab^2.
\]

The two independent equations tx+sy=0 and ty+su=0 imply

\[
P^2=\mathbf Q p_2,\qquad p_2=s^2a^2-stab+t^2b^2.
\]

Because a³=b³=0,

\[
p_2^2=3s^2t^2a^2b^2.
\]

Consequently, for every nonzero rational c,

\[
\deg((cp_2)^2)=3c^2s^2t^2>0.
\]

This proves the entire primitive codimension-two statement for this X, not just positivity on one tested vector: the kernel calculation proves that p₂ spans the primitive space.

Codimension zero contributes deg(h⁴)=6s²t²>0. These three calculations establish all Hodge-type primitive positivity statements for this fourfold and this arbitrary ample rational polarization.

Notice that the full middle intersection form is not positive definite. In the basis (a²,ab,b²) its matrix is

\[
\begin{pmatrix}0&0&1\\0&1&0\\1&0&0\end{pmatrix},
\]

of signature (2,1). The primitive condition and the codimension-dependent sign are essential.

## 4. Construct the algebraic inverse, rather than only its matrix

In bases (a,b) of H² and (a²b,ab²) of H⁶, suppressing Tate twists in this display,

\[
L^2=\begin{pmatrix}2st&s^2\\t^2&2st\end{pmatrix},\qquad
(L^2)^{-1}=\begin{pmatrix}
2/(3st)&-1/(3t^2)\\-1/(3s^2)&2/(3st)
\end{pmatrix}.
\]

Its determinant is 3s²t², which is nonzero. A linear inverse alone would not settle B(X). We exhibit the cycle that induces it.

On X × X let a₁,b₁ denote source hyperplane classes and a₂,b₂ target hyperplane classes. Define the rational codimension-two cycle

\[
\Gamma=
b_1\left(\frac{2a_2}{3st}-\frac{b_2}{3s^2}\right)
+a_1\left(-\frac{a_2}{3t^2}+\frac{2b_2}{3st}\right).
\]

With the convention Γ_*(z) = (pr₂)_*(pr₁^*z · Γ), integration on the source gives

\[
\Gamma_*(a^2b)=\frac{2a}{3st}-\frac{b}{3s^2},\qquad
\Gamma_*(ab^2)=-\frac{a}{3t^2}+\frac{2b}{3st}.
\]

These are exactly the columns of the inverse matrix. Hence Γ_* L² and L² Γ_* are identities on the indicated cohomology groups.

The inverse to L⁴:H⁰→H⁸ is induced by the codimension-zero cycle (6s²t²)⁻¹[X × X]. The middle-degree map is the identity induced by the diagonal. Odd cohomology vanishes. Thus all inverse hard-Lefschetz maps required for B(X) are algebraic in this example.

## 5. An attempted extension that fails, and why

Proposed shortcut: use the known absolute values of Frobenius eigenvalues and the compatibility of Frobenius with intersection to deduce positivity.

This is insufficient even at the linear-algebra level. Put

\[
F=q^2I_2,\qquad J=\operatorname{diag}(1,-1).
\]

Every eigenvalue of F has the weight-four absolute value q², and

\[
F^TJF=q^4J.
\]

Yet (0,1) has square −1 for J. This example is not asserted to arise from a variety and is not a counterexample to the standard conjectures. It disproves only the proposed deduction from those spectral and pairing-similitude properties alone.

There is a geometric reason this shortcut is weak: after a finite extension of the finite field, any given finite collection of algebraic codimension-two cycles is defined over that extension. On their untwisted cohomology classes, geometric Galois Frobenius has the same scalar q² eigenvalue (with q replaced by the extension's cardinality). The eigenvalue does not distinguish a positive intersection direction from a negative one.

## 6. The next proof obligation

The benchmark works because the projective bundle formula supplies the complete cycle space, all relations, the degree map, and the relevant correspondences. None of those completeness statements is available automatically for an arbitrary fourfold.

The next attempt should work with an explicitly specified family of fourfolds and an explicitly specified space of codimension-two cycles. For that family:

1. Check whether its motive or a published theorem already places it in a known case, including the newly reported abelian results.
2. Establish the cycle-class relations and the full relevant primitive space. A convenient list of cycles is not automatically a basis of all algebraic classes.
3. Compute the rational intersection pairing and seek an exact positive decomposition on that space. Prove injectivity or nondegeneracy rather than replacing positivity with an assumed positive metric.
4. If claiming the full standard-conjecture route, construct the inverse-Lefschetz correspondence as an algebraic cycle. A cohomological operator is not automatically algebraic.

No new family is certified as open or solved in this note. The general codimension-two fourfold problem is the research target; selecting a tractable family is the next substantive step.

For a proposed dm³/contact connection, the missing object is a specified map from algebraic-cycle classes to the proposed analytic space together with a proved identity equating the signed intersection pairing to a positive expression. Positivity of an unrelated energy does not prove the required intersection inequality. No such map or identity is established here.

## 7. One correction to the motivating comparison

The literal map s ↦ 1−s fixes only s=1/2, and T ↦ 1/(qT) fixes only T=±q⁻¹ᐟ². The critical line and circle are fixed pointwise by the anti-holomorphic maps s ↦ 1−conjugate(s) and T ↦ 1/(q conjugate(T)), respectively. The source chapter explains the first distinction in §12.1 but its §12.8 table still conflates these maps. This matters if a proof attempt relies on fixed-point geometry. Either symmetry is compatible with paired off-locus zeros; symmetry alone gives no positivity theorem.

## 8. Verification and limits

Run `python3 verify_p2xp2.py` with Python 3 and SymPy. The script checks symbolic identities with arbitrary positive symbols s,t, primitive-space dimensions, the actual push-pull correspondence action, both inverse compositions, and the indefinite Frobenius countermodel. It performs no floating-point sampling.

Execution in this session: **24 exact checks passed; no skipped checks.**

The written proof covers the geometric meaning and universal quantifiers. The script checks its algebra; it does not independently construct Chow groups or ℓ-adic cohomology, prove the general standard conjectures, or verify the 2026 CM-abelian proofs. No Lean proof is included or claimed. No repository or published webpage was edited.

## Primary sources and supplied context

1. A. Grothendieck, *Standard Conjectures on Algebraic Cycles*, in *Algebraic Geometry, Bombay 1968*, published 1969. [Scan](https://download.uni-mainz.de/mathematik/Algebraische%20Geometrie/Lehre/WS23.Padische.1968.Grothendieck.StandardConjs.pdf). Original statement; retrieved, but the scan was not used for machine-extracted formula verification.
2. J. S. Milne, *Polarizations and Grothendieck's Standard Conjectures*, submitted 2001, published Annals of Mathematics 155 (2002), 599–610. [Author's submitted text](https://www.jmilne.org/math/articles/2002aS.pdf); [journal abstract](https://annals.math.princeton.edu/2002/155-2/p07). Introduction supplies the signed primitive pairing and distinguishes the two conjectures.
3. J. S. Milne, [author's article abstracts](https://www.jmilne.org/math/articles/abstracts.html), October 7 and 14, 2026 additions to the 1999 and 2002 entries. Accessed November 11, 2026.
4. J. S. Milne, *On the Hodge, Tate, and standard conjectures for abelian varieties*, [v1 landing page](https://hexagonmath.org/2611.00244v1), dated November 10, 2026; [PDF, §§3.5–3.10](https://hexagonmath.org/pdf/2611.00244v1). Its history separately labels initial submission November 9. Claims checked; full proofs not audited here.
5. University of Michigan, [Milne seminar announcement, November 5, 2026](https://lsa.umich.edu/math/news-events/all-events.detail.html/153453-21915872.html).
6. The Stacks Project, [Lemma 42.36.2, tag 02TX: projective space bundle formula](https://stacks.math.columbia.edu/tag/02TX), accessed November 11, 2026.
7. User-supplied context: [Book 7, André Weil](https://totogt.github.io/geometry/book7/ch-weil.html), and [Book 4, §12.8](https://totogt.github.io/geometry/book4/ch12.html#s12-8). Context and motivation, not evidence of a new proof.
