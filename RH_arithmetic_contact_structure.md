# The Riemann Hypothesis as Non-Integrability of an Arithmetic Contact Structure on the Adele Class Space

**Pablo Nogueira Grossi (framework) · Collaborative Draft**

*Preprint — not peer reviewed*

**DOI reserved for v1: [10.5281/zenodo.22179684](https://doi.org/10.5281/zenodo.22179684)** — Zenodo community *Principia Orthogona*. Deposit pending; the DOI will not resolve until the record is published.

*Version 2, revised 30 August 2026.* Version 1 (10 June 2026) constructed the form and
stated the missing rung. This version adds §4.4–§4.6: the one-sided pole at zeros, the two
reflection laws, the Riemann–Siegel identification (classical, credited), the refutation of
the contactomorphism conjecture, and a status-of-claims table separating what is proved,
machine-checked, classical, and numerical.

---

## Abstract

We reformulate the Riemann Hypothesis (RH) as a non-vanishing condition on a globally defined arithmetic contact 3-form on the adele class space $\mathbb{A}_{\mathbb{Q}}/\mathbb{Q}^\times$. Starting from the classical $2D+t$ contact geometry prototype of *Principia Orthogona* (Book 4, Chapter 2), we lift the Riemann zeta function to an extended arithmetic phase space, construct an explicit contact 1-form $\alpha_{\text{arith}}$ whose twisting coefficient is the von Mangoldt–Dirichlet series (or its meromorphic continuation), and decompose it into local contact forms $\alpha_v$ at each place of $\mathbb{Q}$. The non-integrability condition $\alpha_{\text{arith}} \wedge d\alpha_{\text{arith}} \neq 0$ — which in the smooth ODE setting is automatic — becomes, in the arithmetic setting, equivalent to a global positivity statement on the action of the idele class group on $\ker\alpha_{\text{arith}}$. We compare this positivity condition to Weil's explicit formula criterion, Connes' spectral-triple approach, and the function-field case (where everything is already proved), identifying precisely where the final rung of the proof would need to sit. This revision adds two reflection laws for the form's coefficients under the functional equation, verified numerically to 30 digits; the observation that the pole at each zero falls entirely into one component while the other remains analytic and coincides with the Riemann–Siegel $\vartheta'$; and a refutation of the earlier conjecture that the functional equation acts as a contactomorphism. **RH itself is untouched, and §4.6 states exactly which claims are proved, which are machine-checked, which are classical, and which are numerical only.** The contribution remains a translation dictionary between contact geometry and arithmetic, intended for researchers at the arithmetic–geometry–physics interface.

**MSC classes:** 11M26 (Riemann and Hurwitz zeta functions) · 53D10 (Contact manifolds, general) · 11R56 (Adèle rings and groups) · 81Q10 (Selfadjoint operator theory in quantum mechanics)

**Keywords:** Riemann Hypothesis · contact geometry · adele class space · von Mangoldt function · Weil explicit formula · Connes spectral triple · p-adic differential forms

---

## 1. Introduction

The Riemann Hypothesis asserts that every non-trivial zero of $\zeta(s)$ satisfies $\operatorname{Re}(s) = \tfrac{1}{2}$. Despite 160 years of effort, the statement resists proof, in part because it inhabits a peculiar intersection: it is simultaneously a statement about complex analysis (zeros of a meromorphic function), analytic number theory (distribution of primes via the Euler product), and, as Montgomery–Dyson noticed, random matrix theory / quantum chaos.

This paper asks a different question: **can the failure of zeros to escape the critical line be understood as a geometric rigidity property — specifically, the maximal non-integrability of a contact structure?**

In smooth mechanics, a contact 1-form $\alpha$ on a $(2n+1)$-dimensional manifold satisfies $\alpha \wedge (d\alpha)^n \neq 0$ everywhere; this condition geometrically forces trajectories into the contact distribution and prevents them from "drifting" transversally. The *Principia Orthogona* framework (Section 2 below) makes this explicit for 2D autonomous ODEs lifted to a $3D$ extended phase space $\mathbb{R}^2 \times \mathbb{R}_t$.

Our central observation is:

> The Riemann Hypothesis is equivalent to saying that the arithmetic version of this non-integrability condition holds globally on the adele class space.

This is not a proof. It is a **reformulation** — a new geometric language for an old arithmetic problem. The value of such a reformulation lies in the connections it makes visible, particularly to Connes' noncommutative geometric approach and to the known proof of RH over function fields (Weil, Deligne).

### Notation

| Symbol | Meaning |
|--------|---------|
| $s = \sigma + it$ | complex variable, $\sigma = \operatorname{Re}(s)$, $t = \operatorname{Im}(s)$ |
| $\zeta(s)$ | Riemann zeta function |
| $\Lambda(n)$ | von Mangoldt function ($\log p$ if $n = p^k$, else $0$) |
| $\mathbb{A}_{\mathbb{Q}}$ | adele ring of $\mathbb{Q}$ |
| $\mathbb{Q}_p$ | $p$-adic completion of $\mathbb{Q}$ |
| $\alpha$ | contact 1-form |
| $\ker\alpha$ | contact distribution (hyperplane field) |

---

## 2. The Classical Prototype: Principia Orthogona Chapter 2

### 2.1 Phase plane and extended phase space

Let $\dot{x} = f(x,y)$, $\dot{y} = g(x,y)$ be a smooth autonomous 2D ODE. The *extended phase space* is $\mathbb{R}^3$ with coordinates $(x, y, t)$; every solution $\gamma(t) = (x(t), y(t), t)$ is a curve in this space.

### 2.2 The contact form and non-integrability

Following Grossi (Book 4, Ch. 2, §2.3), the **contact 1-form** associated to the system is

$$\alpha = dy - g(x,y)\,dx.$$

Along any solution curve, $\alpha(\dot{\gamma}) = \dot{y} - g\,\dot{x} = g - g \cdot 1 = 0$, so $\gamma$ lies in $\ker\alpha$. The **maximal non-integrability** condition

$$\alpha \wedge d\alpha \neq 0$$

holds everywhere because $d\alpha = -\partial_x g\,dx\wedge dy - \partial_y g\,dy\wedge dy = -(\partial_x g)\,dx\wedge dy$ (plus cross terms), and the resulting 3-form is generically non-vanishing. This condition prevents $\ker\alpha$ from being integrable (i.e., from admitting a foliation by 2D surfaces), geometrically forcing the unique "threading" of trajectories through the contact distribution.

### 2.3 Example 1 — Harmonic oscillator

$$\dot{x} = y,\quad \dot{y} = -x \implies \alpha = dy + x\,dx,\quad d\alpha = dx\wedge dy.$$

Trajectories lift to helices in $\mathbb{R}^3$. Non-integrability: $\alpha\wedge d\alpha = dx\wedge dy\wedge dt \neq 0$.

### 2.4 Example 2 — Damped nonlinear oscillator (DNLS reduction)

The discrete nonlinear Schrödinger equation, reduced to an effective 2D envelope mode, yields

$$\dot{x} = y,\quad \dot{y} = -x - \gamma y - \beta(x^2+y^2)y.$$

The contact form is

$$\alpha = dy + \bigl(x + \gamma y + \beta(x^2+y^2)y\bigr)\,dx,$$

and $d\alpha = dx\wedge dy$ still (the cubic term contributes only $\partial_x(\cdots)\,dx\wedge dx = 0$). Trajectories become *tapered, nonlinearly modulated helices* — the radius shrinks as $t\to\infty$ while the nonlinearity introduces amplitude-dependent frequency shifts. Non-integrability continues to hold everywhere.

**Key lesson:** the Grossi prototype handles arbitrarily complex smooth ODEs uniformly. The contact structure is always local and finite-dimensional. The challenge for the Riemann zeta function is that it is *not* governed by any such local ODE.

---

## 3. Lifting the Zeta Function to the Extended Phase Space

### 3.1 The zeta phase plane

Write $\zeta(\sigma + it) = U(\sigma,t) + iV(\sigma,t)$ with $U, V$ real. Fix $\sigma$ and treat $(U, V)$ as a 2D state depending on the parameter $t$. The **lifted curve** is

$$\gamma(t) = \bigl(U(\sigma,t),\, V(\sigma,t),\, t\bigr) \in \mathbb{R}^3.$$

The non-trivial zeros of $\zeta$ are the $t$-values where $\gamma(t)$ pierces the plane $U = V = 0$.

![**Figure 1 — the lift.** Left: the phase plane at three abscissae, with $t$ present only as a parameter; the curves overlap and nothing distinguishes $\sigma=\tfrac12$. Right: the same three curves with $t$ promoted to a coordinate. They separate into helices, the mirror pair $\sigma$ and $1-\sigma$ sit either side of the self-mirror line, and each non-trivial zero becomes a puncture of the $U=V=0$ axis (marked). Regenerate with `figures.py`.](fig1_rh_lift.pdf){width=100%}

> **The figure is flat and the object is not.** A printed projection fixes one viewpoint and
> loses the rotation that makes the separation legible. An interactive version, in which the
> abscissa is a slider and the mirror pair can be watched converging onto the critical line, is
> published as Figure 12.1 of Book 4, Chapter 12:
> **<https://totogt.github.io/geometry/book4/ch12.html>**. Readers who want the geometry rather
> than a picture of it should start there; the construction of §4 will be easier to follow
> afterwards.


### 3.2 The Riemann Hypothesis as a geometric trapping condition

**Reformulation 3.1 (informal).** *The Riemann Hypothesis is equivalent to the statement that every zero-curve $\gamma$ satisfying $U(\sigma_0, t) = V(\sigma_0, t) = 0$ must lie on the single hyperplane $\sigma_0 = \tfrac{1}{2}$ inside the extended space $\mathbb{R}^3_{(U,V,t)}$.*

To make this a contact-geometric statement, we need a 1-form $\alpha$ such that:
1. $\alpha(\dot{\gamma}) = 0$ for every zero-curve $\gamma$.
2. $\alpha \wedge d\alpha \neq 0$ everywhere (non-integrability).
3. The *only* place where the contact distribution is compatible with hitting $U = V = 0$ is $\sigma = \tfrac{1}{2}$.

Conditions (1)–(3) together would constitute a proof of RH within the contact-geometric framework. We can satisfy (1) and (2) explicitly; condition (3) is the open part.

---

## 4. The Arithmetic Contact Form

### 4.1 Construction

The velocity of the zeta curve along $t$ is governed by the logarithmic derivative

$$-\frac{\zeta'}{\zeta}(s) = \sum_{n=1}^{\infty} \Lambda(n)\,n^{-s} = \sum_{n=1}^{\infty} \Lambda(n)\,n^{-\sigma} e^{-it\log n}.$$

Separating real and imaginary parts, the imaginary part of $-\zeta'/\zeta$ controls the "angular velocity" of the zeta curve. Define

$$g(\sigma,t) = -\operatorname{Im}\!\left(-\frac{\zeta'}{\zeta}(\sigma+it)\right) = \sum_{n=1}^{\infty} \frac{\Lambda(n)}{n^\sigma}\sin(t\log n).$$

(This series converges absolutely for $\sigma > 1$; elsewhere it is defined by meromorphic continuation of $\zeta'/\zeta$.)

**Definition 4.1.** The *arithmetic contact form* on $\mathbb{R}^3_{(U,V,t)}$ is

$$\boxed{\alpha_{\text{arith}} = dV - g(\sigma,t)\,dU.}$$

### 4.2 The exterior derivative

Applying $d$ term-by-term (justified by uniform convergence on compact sets for $\sigma > 1$, and by analytic continuation inside the critical strip):

$$d\alpha_{\text{arith}} = -dg \wedge dU = -(\partial_t g)\,dt\wedge dU,$$

where

$$\partial_t g = \sum_{n=1}^{\infty} \frac{\Lambda(n)\log n}{n^\sigma}\cos(t\log n).$$

### 4.3 Non-integrability

**Proposition 4.2.** *The non-integrability 3-form is*

$$\alpha_{\text{arith}} \wedge d\alpha_{\text{arith}} = -(\partial_t g)\,dV\wedge dt\wedge dU.$$

*This is nonzero almost everywhere because the frequencies $\{\log p : p \text{ prime}\}$ are $\mathbb{Q}$-linearly independent, making $\partial_t g$ a quasi-periodic function that is dense and non-vanishing.*

**Proof sketch.** The independence of $\{\log p\}$ over $\mathbb{Q}$ follows from the uniqueness of prime factorization. Hence the quasi-periodic sum $\partial_t g$ is not identically zero on any open interval of $t$. $\square$

### 4.4 Behaviour at zeros, and why one coefficient is not enough

At a zero $s_0 = \tfrac{1}{2}+it_0$ the logarithmic derivative has a simple pole, and $g(\sigma,t)\to\infty$: the contact planes twist infinitely rapidly at the moment the curve touches $U=V=0$. That much was in the first version of this paper. It is imprecise in a way worth repairing, because the repair is what motivates the two-coefficient form used in *Principia Orthogona* Book 4, Chapters 11–12.

Write the companion coefficient

$$c(\sigma,t) \;=\; \operatorname{Re}\!\left(-\frac{\zeta'}{\zeta}(\sigma+it)\right) \;=\; \sum_{n=1}^{\infty}\frac{\Lambda(n)}{n^\sigma}\cos(t\log n),$$

so that $-\zeta'/\zeta = c - ig$ and the Book 4 form reads $\alpha_{\text{arith}} = c\,d\tilde U - g\,d\tilde V$. The single-coefficient form of §4.1 is the special case in which $c$ is suppressed.

**Proposition 4.3 (the pole is one-sided).** *Along the critical line, the simple pole of $\zeta'/\zeta$ at a zero $\rho = \tfrac12+i\gamma$ falls entirely into $g$ and not at all into $c$.*

*Proof.* Near $\rho$, $\zeta'/\zeta(s) \sim (s-\rho)^{-1}$. Restricting to $\sigma=\tfrac12$ gives $s-\rho = i(t-\gamma)$, so $(s-\rho)^{-1} = -i(t-\gamma)^{-1}$, which is purely imaginary. The real part is therefore bounded and the imaginary part carries the entire singularity. $\square$

Numerically, with $\gamma_1 = 14.134725142$: $g(\tfrac12,\gamma_1+\delta) = -10.076,\,-100.08,\,-1000.08,\,-10000.08,\,-100000.08$ for $\delta = 10^{-1}\ldots10^{-5}$ — a simple pole of residue $-1$ — while $c$ converges to $0.4052744$.

This is the content the one-coefficient form cannot express. "$g\to\infty$" is true but says nothing about what stays finite. In the two-coefficient form the statement is sharp: **the $d\tilde V$ component carries every zero as a simple pole; the $d\tilde U$ component is analytic across each of them.**

### 4.5 The reflection laws, and the failure of contactomorphism

Book 4 §12.2 conjectured that the involution induced by the functional equation is a contactomorphism of $\alpha_{\text{arith}}$ — that $\Phi^*\alpha = f\alpha$ for a scalar $f$, with fixed locus the plane $\sigma=\tfrac12$. Two corrections are required, and the second refutes the conjecture as stated.

**First, the involution.** $s\mapsto 1-s$ carries $\sigma+it$ to $(1-\sigma)-it$; it does not preserve $t$, and its only fixed point is $s=\tfrac12$, not the critical line. The map with fixed locus $\sigma=\tfrac12$ is $\Phi: s\mapsto 1-\bar s$, i.e. $(\sigma,t)\mapsto(1-\sigma,t)$ — the functional equation composed with complex conjugation, available because $\zeta$ has real coefficients.

**Second, the transformation laws.** Taking the logarithmic derivative of $\zeta(s)=\chi(s)\zeta(1-s)$, and using that $c$ is even and $g$ odd in $t$:

$$g(\sigma,t) - g(1-\sigma,t) \;=\; \operatorname{Im}\big[(\chi'/\chi)(\sigma+it)\big], \qquad c(\sigma,t) + c(1-\sigma,t) \;=\; -\operatorname{Re}\big[(\chi'/\chi)(\sigma+it)\big],$$

with $(\chi'/\chi)(s) = \log\pi - \tfrac12\psi(s/2) - \tfrac12\psi((1-s)/2)$. Note the asymmetry: $g$ obeys a **difference** law, $c$ a **sum** law. Both verified numerically to 30 significant digits at $\sigma\in\{0.3,0.5,0.8,1.1,1.5,2.3\}$, $t\in[0.7,25]$.

**Corollary 4.4.** *On $\sigma=\tfrac12$ the two digamma arguments $\tfrac14\pm\tfrac{it}{2}$ are conjugate, so $\chi'/\chi$ is real there and the difference law gives $g(\tfrac12,t)=g(\tfrac12,t)$ identically — the reflection constraint holds on the critical line and on no other vertical line.*

**Corollary 4.5.** *On $\sigma=\tfrac12$ the sum law collapses to*
$$c\!\left(\tfrac12,t\right) = \tfrac12\left[\operatorname{Re}\psi\!\left(\tfrac14+\tfrac{it}{2}\right)-\log\pi\right] = \vartheta'(t),$$
*where $\vartheta$ is the Riemann–Siegel theta function.*

This last is **classical, and we claim no novelty for it**: it is equivalent to the standard fact that $Z(t)=e^{i\vartheta(t)}\zeta(\tfrac12+it)$ is real-valued, since $Z'/Z = i\vartheta' + i\zeta'/\zeta$ is real precisely when $\operatorname{Re}(\zeta'/\zeta)=-\vartheta'$. What is new here is only its role: it identifies the $d\tilde U$ coefficient of $\alpha_{\text{arith}}$ on the critical wall with the density of the Riemann–von Mangoldt counting formula $N(T)=\vartheta(T)/\pi+1+S(T)$. The form's two components separate the counting function from the zeros.

**Proposition 4.6 (the conjecture fails off the line).** *$\Phi^*\alpha_{\text{arith}} = f\cdot\alpha_{\text{arith}}$ with $f$ scalar does not hold away from $\sigma=\tfrac12$.*

*Reason.* Under $\Phi$, $g$ is carried not to $\pm g$ but to itself plus $-\operatorname{Im}[\chi'/\chi]$, a term built from gamma factors and containing no von Mangoldt data whatever. No scalar multiple of $\alpha_{\text{arith}}$, whose coefficients are $\Lambda$-series, can absorb it. $\square$

What survives is a graded statement: $\Phi^*\alpha_{\text{arith}} - \alpha_{\text{arith}}$ is an explicit gamma-factor $1$-form vanishing on $\sigma=\tfrac12$. Establishing its precise shape requires the transformation of $\tilde U$ and $\tilde V$ themselves, which is not settled here.

**A methodological remark.** The distinguished locus is not selected by the contact structure. It is selected by the gamma factor — an analytic input from outside the geometry — and the geometry then carries the consequence. Any claim elsewhere in this framework that a distinguished set is "determined by the contact geometry alone" should be checked against this example.

### 4.6 Status of claims

| Claim | Status |
|---|---|
| $c,g$ are the real and imaginary parts of $-\zeta'/\zeta$; $\sum\Lambda(n)n^{-s} = -\zeta'/\zeta$ for $\Re s>1$ | **Proved, machine-checked.** Lean 4 / Mathlib v4.32.0, `lseries_vonMangoldt_eq_neg_Zlog`, resting on `[propext, Classical.choice, Quot.sound]` |
| Proposition 4.3, the pole is one-sided | Proved above; residue confirmed numerically |
| Corollary 4.5, $c(\tfrac12,t)=\vartheta'(t)$ | **Classical** (equivalent to $Z$ real); verified to 25 digits |
| Reflection laws of §4.5 | **Numerical only**, 30 digits at 7 points. Stated in Lean as `reflection_law`, *admitted* (`sorryAx`) |
| $\chi'/\chi$ real on $\sigma=\tfrac12$ | Argued above; stated in Lean as `chiLog_real_on_critical_line`, *admitted* |
| Proposition 4.6, failure of contactomorphism | Argued, not formalised |
| Global positivity (§6), and RH itself | **Open.** Nothing here bears on it |

Lean source: `TOTOGT/GTCT`, `book4/ZetaReflection.lean`.

---

## 5. Adelic Decomposition

### 5.1 Why adeles?

The von Mangoldt coefficient $g(\sigma,t)$ is a global sum over all primes simultaneously. To make the contact structure genuinely "local-to-global" — and to connect with the Euler product factorization of $\zeta$ — we decompose $\alpha_{\text{arith}}$ over the adele ring $\mathbb{A}_\mathbb{Q} = \mathbb{R} \times \prod_p' \mathbb{Q}_p$.

### 5.2 Local contact forms

**Archimedean place $v = \infty$:**

$$g_\infty(\sigma,t) = -\operatorname{Im}\!\left(-\frac{\zeta'}{\zeta}(\sigma+it)\right), \quad \alpha_\infty = dV_\infty - g_\infty\,dU_\infty.$$

This is the form of Section 4.

**Non-Archimedean place $v = p$:** The local Euler factor contributes

$$g_p(t_p) = \frac{\log p}{1 - p^{-\sigma}e^{-it_p\log p}},$$

where $t_p \in \mathbb{Q}_p$ is the local idelic parameter. The local contact form is

$$\alpha_p = dV_p - g_p(t_p)\,dU_p.$$

### 5.3 Local exterior derivative at place $p$

Let $c = p^{-\sigma}p^{-it_p}$. Then

$$\partial_{t_p} g_p = -i(\log p)^2 \frac{c}{(1-c)^2}.$$

Hence

$$d\alpha_p = i(\log p)^2 \frac{c}{(1-c)^2}\,dt_p \wedge dU_p.$$

**p-adic norm analysis.** In the rigid-analytic domain $|c|_p < 1$ where the local Euler factor is holomorphic, $|1-c|_p = 1$ (since $c$ is in the open unit disk). Therefore

$$|\partial_{t_p} g_p|_p = |c|_p = p^{-\sigma}\cdot|p^{-it_p}|_p.$$

As a trajectory approaches the boundary $|c|_p \to 1^-$, the denominator $(1-c)^2$ acquires positive $p$-adic valuation, forcing $|d\alpha_p|_p \to 0$. The contact condition $\alpha_p(\dot\gamma_p) = 0$ thus imposes a **valuation inequality** that confines the local flow inside the rigid-analytic unit disk. Any attempt to cross into the ramified region $|c|_p \geq 1$ — corresponding to non-unit idelic components that would break the restricted-product structure of $\mathbb{A}_\mathbb{Q}$ — is geometrically forbidden.

### 5.4 Global assembly

A global 1-form on the adele class space $\mathbb{A}_\mathbb{Q}/\mathbb{Q}^\times$ is assembled as a restricted direct product of local forms. Because the Euler product factorizes globally, only finitely many places contribute non-trivially at any adelic point, and the global exterior derivative commutes with localization:

$$d\alpha_{\text{arith}} = \sum_v d\alpha_v \qquad \text{(restricted sum)}.$$

The global non-integrability condition

$$\alpha_{\text{arith}}\wedge d\alpha_{\text{arith}} \neq 0 \quad \text{on } \mathbb{A}_\mathbb{Q}/\mathbb{Q}^\times$$

is the statement that the restricted product of local 3-forms is nowhere-vanishing on the adele class space. The local "locking" mechanisms at each place — linear independence of $\{\log p\}$ at $v=\infty$, valuation rigidity of $(1-c)^2$ at $v=p$ — act jointly to enforce this.

---

## 6. The Missing Rung: Global Positivity

### 6.1 Formulation

All the local machinery works. The remaining step is:

**Conjecture 6.1 (Global Positivity / RH restated).** *The natural action of the idele class group $\mathbb{A}_\mathbb{Q}^\times/\mathbb{Q}^\times$ on $\ker\alpha_{\text{arith}}$ is **positive-definite**. Equivalently, the total "twisting energy" of the arithmetic contact structure is strictly minimized precisely on the hyperplane $\sigma = \tfrac{1}{2}$, and any zero-curve at $\sigma \neq \tfrac{1}{2}$ would force $\alpha_{\text{arith}} \wedge d\alpha_{\text{arith}} = 0$ at some adelic point — a contradiction with maximal non-integrability.*

This conjecture is exactly the Riemann Hypothesis, restated in contact-arithmetic language. It is not easier to prove in this language; the arithmetic difficulty is fully preserved.

### 6.2 Why the reformulation is still useful

A clean reformulation can:
- Suggest new proof strategies by connecting to known positivity results.
- Reveal structural analogies with cases where RH is already proved (see Section 7).
- Provide a unified geometric language for comparing disparate approaches (Connes, Weil, random matrix theory).

---

## 7. Comparison with Known Approaches

### 7.1 Weil's explicit formula and positivity criterion

Weil (1952) showed that RH for $\zeta$ is equivalent to the **positivity of a certain distribution** on the adele class space: for a suitable class of test functions $h$,

$$\sum_\rho \hat{h}(\rho) \geq 0,$$

where the sum is over non-trivial zeros. This is a spectral positivity statement. In our language: Weil's positivity is the statement that the idele class group action has non-negative spectrum, which is the $L^2$ analogue of our contact-geometric positive-definiteness condition. The two conditions are morally identical but technically formulated in different categories (measure theory vs. differential geometry).

**Partial results.** Zero-density estimates (e.g., $N(\sigma, T) \ll T^{A(1-\sigma)}\log^B T$ for $\sigma > \tfrac{1}{2}$) give unconditional bounds showing that "most" zeros satisfy the contact condition. These correspond to partial positivity of the arithmetic contact form on large subsets of the adele class space.

### 7.2 Connes' spectral triple

Connes (1999) proposes to realize the zeros of $\zeta$ as the **missing part of the spectrum** of an operator on $L^2(\mathbb{A}_\mathbb{Q}/\mathbb{Q}^\times)$. The absorption spectrum of a suitable Hamiltonian $H$ would contain the zeros, and RH would follow if $H$ were shown to be self-adjoint (Hermitian), forcing real eigenvalues — hence $\operatorname{Im}(\rho) \in \mathbb{R}$, i.e., $\operatorname{Re}(\rho) = \tfrac{1}{2}$.

**Translation to contact language.** The self-adjointness of $H$ corresponds to the positive-definiteness of the idele-class action in our framework. Connes' "Reeb vector field" is our contact-geometric Reeb flow. The spectral gap condition in Connes corresponds to the strict non-vanishing of $\alpha\wedge d\alpha$ away from $\sigma = \tfrac{1}{2}$.

The difference: Connes works in $L^2$ (spectral theory), we work on contact manifolds (differential geometry). The obstacle is the same: proving positivity.

### 7.3 Function-field analogue (where RH is proved)

Over a finite field $\mathbb{F}_q$, the analogue of $\zeta(s)$ is the **zeta function of a curve** $C/\mathbb{F}_q$, and the analogue of RH was proved by Weil (curves, 1948) and Deligne (varieties, 1974).

**Contact form in the function-field case.** The Euler product is finite in each degree, and the "frequencies" $\log p$ become discrete valuations $v(p)$ in the function field. The key simplifications:

1. The adele ring $\mathbb{A}_{k}$ (for function field $k$) is *locally compact* and the relevant spaces are *finite-dimensional* in the relevant cohomological sense.
2. The positivity (Weil's positivity for curves) follows from the **Riemann–Roch theorem**, which provides an explicit algebraic control over the zero distribution.
3. In contact terms: the "arithmetic contact form" over $\mathbb{F}_q$ has a **finite-dimensional Reeb flow**, and positive-definiteness can be verified by an explicit computation over the Jacobian of $C$.

**Lesson for the number-field case.** The function-field proof works because algebraic geometry (Riemann–Roch, Lefschetz trace formula) provides the positivity "for free." Over $\mathbb{Q}$, there is no analogue of Riemann–Roch that directly controls the infinite-dimensional adele class space. The contact form in Section 4 encodes all the same arithmetic, but the positivity argument must come from elsewhere — perhaps from a new analytic tool, a motivic cohomology result, or a non-commutative geometry calculation.

---

## 8. Structure of a Putative Proof

For completeness, we state what a proof of RH within this framework would require:

**Step 1** (done): Construct $\alpha_{\text{arith}}$ and verify $\alpha_{\text{arith}}\wedge d\alpha_{\text{arith}} \neq 0$ on the complement of the zeros (Section 4–5).

**Step 2** (done): Decompose into local forms $\alpha_v$ and verify the valuation lock at each $p$-adic place (Section 5.3).

**Step 3** (open): Prove that the functional equation $\zeta(s) = \chi(s)\zeta(1-s)$ implies a **geometric symmetry** $\Phi: \sigma \mapsto 1-\sigma$ of the contact structure, pairing $\alpha_{\text{arith}}$ at $\sigma$ with its dual at $1-\sigma$.

**Step 4** (open, core difficulty): Prove that $\Phi$-symmetry together with maximal non-integrability forces every zero-curve to lie on the fixed locus $\sigma = \tfrac{1}{2}$ of $\Phi$ — i.e., prove that any zero at $\sigma_0 \neq \tfrac{1}{2}$ would force $\alpha_{\text{arith}}\wedge d\alpha_{\text{arith}} = 0$ at some adelic point.

Step 4 is precisely Global Positivity (Conjecture 6.1) and is equivalent to RH.

---

## 9. Discussion and Open Questions

1. **Is there a Morse-theoretic approach to Step 4?** The "twisting energy" minimization language suggests a Morse-theory or symplectic-filling argument might work, analogous to how filling obstructions appear in 3-manifold contact topology (Giroux, Etnyre).

2. **Can the DNLS nonlinearity be tuned to approximate the prime distribution?** The reduced DNLS contact form (Section 2.4) produces chaotic helices whose statistics can be adjusted via $\beta$ and $\gamma$. Is there a parameter regime where the local zero-spacing statistics match GUE (the random matrix prediction for zeta zeros)?

3. **Adelic contact geometry as a field.** The construction of $\alpha_{\text{arith}}$ on $\mathbb{A}_\mathbb{Q}/\mathbb{Q}^\times$ is, to our knowledge, new. Does this space admit a well-defined contact topology (tight vs. overtwisted contact structures)? If $\alpha_{\text{arith}}$ defines a *tight* contact structure, that would be a strong rigidity result consistent with RH.

4. **$p$-adic Reeb dynamics.** The local Reeb vector field at each place $p$ is the dual vector field to $\alpha_p$ (defined by $\alpha_p(R_p) = 1$, $d\alpha_p(R_p, \cdot) = 0$). Studying the dynamics of $R_p$ in the rigid-analytic setting might reveal additional arithmetic structure.

---

## Appendix A: Meromorphic Continuation of $g(\sigma,t)$ Inside the Critical Strip

For $\sigma > 1$, the series $g(\sigma,t) = \sum_n \Lambda(n)n^{-\sigma}\sin(t\log n)$ converges absolutely. For $0 < \sigma \leq 1$, the Dirichlet series for $-\zeta'/\zeta$ diverges, but $\zeta'/\zeta$ extends meromorphically to $\mathbb{C}$ (with simple poles at zeros of $\zeta$ and a double pole at $s=1$). We define $g(\sigma,t)$ inside the strip as

$$g_{\text{cont}}(\sigma,t) = -\operatorname{Im}\!\left(-\frac{\zeta'}{\zeta}(\sigma+it)\right),$$

using this meromorphic continuation. The exterior derivative formula $d\alpha_{\text{arith}} = -(\partial_t g_{\text{cont}})\,dt\wedge dU$ remains valid wherever $\zeta \neq 0$ and $\zeta'$ exists. At a zero $s_0$, the logarithmic derivative has a simple pole, and $g_{\text{cont}} \to \pm\infty$: the contact planes twist infinitely rapidly, consistently with the zero-curve piercing $U = V = 0$.

---

## Appendix B: Summary Table — Parallel Structures

| Concept | Smooth ODE (Grossi Ch. 2) | Arithmetic (this paper) | Connes' approach |
|---------|--------------------------|------------------------|-----------------|
| Phase space | $\mathbb{R}^2 \times \mathbb{R}_t$ | $\mathbb{A}_\mathbb{Q}/\mathbb{Q}^\times$ | $L^2(\mathbb{A}_\mathbb{Q}/\mathbb{Q}^\times)$ |
| Contact form | $\alpha = dy - g(x,y)\,dx$ | $\alpha_{\text{arith}} = dV - g_{\text{cont}}\,dU$ | Spectral triple $(A, H, D)$ |
| Non-integrability | $\alpha\wedge d\alpha \neq 0$ (local, automatic) | $\alpha_{\text{arith}}\wedge d\alpha_{\text{arith}} \neq 0$ (global, non-trivial) | $D$ self-adjoint |
| RH condition | N/A (smooth zeros are fine) | Global positivity of idele-class action | Self-adjointness of $H$ |
| Forcing mechanism | Smooth ODE rigidity | $\mathbb{Q}$-independence of $\{\log p\}$ + $p$-adic valuation locks | Trace formula positivity |
| Status | Proved (trivially) | Open (= RH) | Open (= RH) |
| Function-field analogue | Same framework, finite-dim | Weil positivity via Riemann–Roch | Proven (Deligne) |

---

## References

1. B. Riemann, *Über die Anzahl der Primzahlen unter einer gegebenen Grösse*, Monatsberichte der Berliner Akademie (1859).
2. A. Weil, *Sur les "formules explicites" de la théorie des nombres premiers*, Comm. Sém. Math. Univ. Lund (1952).
3. A. Connes, *Trace formula in noncommutative geometry and the zeros of the Riemann zeta function*, Selecta Math. **5** (1999), 29–106.
4. A. Connes and C. Consani, *On the notion of geometry over $\mathbb{F}_1$*, J. Algebraic Geom. **20** (2011), 525–557.
5. H. Montgomery, *The pair correlation of zeros of the zeta function*, Analytic Number Theory, Proc. Sympos. Pure Math. **24** (1973), 181–193.
6. P. N. Grossi, *Principia Orthogona*, Book 4, Chapter 2: Contact geometry and the extended phase space. Available at: https://totogt.github.io/geometry/book4/ch02.html
7. H. Iwaniec and E. Kowalski, *Analytic Number Theory*, AMS Colloquium Publications **53** (2004).
8. V. I. Arnold, *Mathematical Methods of Classical Mechanics*, Springer (1989). [Contact geometry background]
9. J. Etnyre, *Introductory lectures on contact geometry*, Topology and Geometry of Manifolds, Proc. Sympos. Pure Math. **71** (2003).
10. P. Deligne, *La conjecture de Weil I*, Publ. Math. IHÉS **43** (1974), 273–307.

---

*End of draft. Version 0.1 — for internal review and critique.*
