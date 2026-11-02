---
title: "Generative Contact Mechanics: A Geometric Framework for Dissipative Systems with Structured Limit Cycles"
subtitle: "Version 2 (draft, Part I)"
author: "Pablo Nogueira Grossi"
---

**[DRAFT. Author block, dedication, acknowledgments and the DOI line are carried over from V1 by the author; nothing in this draft is final until the author signs it off.]**

# 0. Status of this version

Version 1 stated four theorems (A to D). An audit of its proofs, recorded in the project note "Audit: GCM PDF paper, Theorems A to D" (2026-11-01) and re-done in `engineering/gcm-paper-audit.py`, found statements that fail as written. This version restates them as far as the proofs now go and says plainly where a claim is proved, where it is only sketched, and where it is open. Each result carries one of three labels:

* **[P]** proved here by a hand derivation that is also checked by a script in `gcm-v2/` or `engineering/`.
* **[S]** a proof sketch relying on standard theory cited but not re-derived here.
* **[O]** open. Stated so that it can be attacked; not claimed.

A Lean file is named under a result only when it compiles (checked by the author with Lean v4.32.0 and Mathlib) and only for what its docstring says it proves. A compiling Lean file is never offered as proof of a statement it does not state.

# 1. Setting

Throughout, $(S,g)$ is a smooth complete Riemannian manifold and $Y$ a smooth complete vector field with flow $\varphi^t$.

**Definition 1.1 (hyperbolic limit cycle).** A *limit cycle* is a compact connected invariant curve $\Gamma\cong S^1$ on which $Y\neq 0$, with minimal period $T^*>0$. Let $\mu_1,\dots,\mu_{n-1}$ be the Floquet multipliers of the linearised return map transverse to $\Gamma$ ($n=\dim S$). $\Gamma$ is *hyperbolic* if $|\mu_j|<1$ for all $j$. Put
$$\mu_{\max}:=\max_j \tfrac{1}{T^*}\log|\mu_j|<0 .$$

**Definition 1.2 (dm3 system).** A *dm3 system* is $D=(S,g,Y,\Gamma,\sigma)$ with $\Gamma$ a hyperbolic limit cycle of $Y$ and $\sigma:S\to\mathbb{R}^{n\times m}$ a smooth bounded noise coefficient. The Lyapunov function is *not* part of the data; it is derived (Definition 1.3). The four phase points $p_{\mathrm{I}},p_{\mathrm{VI}},p_{\mathrm{III}},p_{\mathrm{VII}}$ of V1 are the images of one point under $\varphi^{jT^*/4}$, $j=0,1,2,3$; they are distinct because $T^*$ is minimal, so they are a naming convention and not an axiom.

**Definition 1.3 (adapted Lyapunov function).** Fix $c>0$. A smooth $V:S\to\mathbb{R}_{\ge0}$ is *$c$-adapted* on a neighbourhood $N$ of $\Gamma$ if $V=0$ exactly on $\Gamma$, $V$ is comparable to $d_g(\cdot,\Gamma)^2$ on $N$, and $\dot V:=g(\nabla V,Y)\le -cV$ on $N$.

**Axiom N (noise).** For the chosen $c$-adapted $V$ there is $\kappa>0$ with
$$\mathcal{L}V\le -cV+\kappa\,\|\sigma\|_\infty^2\quad\text{on }S,\qquad \mathcal{L}f=g(\nabla f,Y)+\tfrac12\operatorname{tr}\!\big(\sigma^{\top}\operatorname{Hess}f\,\sigma\big).$$

**Remark 1.4 (the eight axioms of V1).** V1 listed eight axioms and called them logically independent. They are not. Axiom 4 ($\dot V\le -cV$) implies Axiom 3 ($\dot V<0$ off $\Gamma$), since $V>0$ off $\Gamma$. Axioms 2, 6, 7 and 8 restate Definitions 1.1 and 1.2 (compact invariant cycle, $Y\neq0$ and minimal period, $Y$ smooth, hyperbolicity). Axiom 1 is the naming convention above. What remains is hyperbolicity (in Definition 1.2) and Axiom N.

# 2. Theorem A, restated

**Theorem A.** Let $D$ be a dm3 system.

1. $\Gamma$ is a hyperbolic limit cycle with minimal period $T^*>0$. **[P]** (by Definition 1.2)
2. *(Exponential orbital stability.)* For every $c<2|\mu_{\max}|$ there is a $c$-adapted $V$ on some neighbourhood of $\Gamma$ provided $\dim S=2$. **[S]** For $\dim S>2$, for every $c<2|\mu_{\max}|$ there is a norm $N$ on the transverse bundle with $N(\varphi^t v)\le e^{-ct/2}N(v)$; a *smooth* $c$-adapted $V$ is **[O]**.
3. *(Noise.)* Under Axiom N, for every $t\ge0$ and every initial point,
$$\mathbb{E}\,V(X_t)\le e^{-ct}V(X_0)+\frac{\kappa}{c}\,\|\sigma\|_\infty^2 .$$ **[S]** This is an ultimate bound. It is **not** convergence to $0$.
4. *(Holonomy.)* Section 3. **[P]**

**Why V1's A(ii) proof failed.** V1 took $V=d_g(\cdot,\Gamma)^2$ in the given metric and claimed $\dot V\le 2\mu_{\max}V+O(V^{3/2})$. That needs the transverse linearisation to contract in the metric $g$, which Floquet multipliers do not guarantee. Counterexample: transverse $\dot x=Ax$ with $A=\begin{pmatrix}-1&10\\0&-1\end{pmatrix}$ has both eigenvalues $-1$ yet $\tfrac{d}{dt}|x|^2=16>0$ at $x=(1,1)$ (`engineering/gcm-paper-audit.py`, F2). The remedy is an adapted function. For this $A$ and $\kappa=\tfrac12$ one is $V=x^2+20xy+201y^2$, with $\dot V=-(x^2+y^2)-V\le -V$ (`gcm-v2/GCMv2Adapted.lean`, Route B, compiles; one matrix and one $\kappa$ only).

**Proof sketch of (ii), $\dim S=2$.** In Fermi coordinates $(\rho,\theta)$ about $\Gamma$ the transverse equation is $\dot\rho=a(\theta)\rho+O(\rho^2)$ with $a$ periodic along the cycle and time-average $\mu_{\max}$. The substitution $\rho'=\rho\,e^{-\int(a-\mu_{\max})}$ (the integral is periodic because the average of $a-\mu_{\max}$ is zero) gives $\dot\rho'=\mu_{\max}\rho'+O(\rho'^2)$, and $V=\rho'^2$ has $\dot V=2\mu_{\max}V+O(V^{3/2})\le -cV$ near $\Gamma$ for any $c<2|\mu_{\max}|$. The constant-coefficient step is `scalar_adapted_deriv` (Route A, compiles); the periodic-coefficient substitution is a hand argument not formalised.

**General $\dim S$, the norm.** For a linear semigroup $E$ with $\|E_s\|\le Ke^{-\mu s}$ and $\kappa\le\mu$, the norm $N(x)=\sup_{s\ge0}e^{\kappa s}\|E_sx\|$ satisfies $\|x\|\le N(x)$ and $N(E_tx)\le e^{-\kappa t}N(x)$ (`adaptedNorm_ge`, `adaptedNorm_decay`, compile). This is a decay statement for a non-smooth norm, not a $C^1$ Lyapunov function.

**Proof sketch of (iii).** By Itô's formula and Axiom N, $m(t)=\mathbb{E}V(X_t)$ satisfies $m'\le -cm+\kappa\|\sigma\|_\infty^2$ (after localisation by stopping times and Fatou's lemma, since $V\ge0$). The comparison function $e^{-ct}m_0+\frac{\kappa}{c}\|\sigma\|_\infty^2(1-e^{-ct})$ solves the equality case (`gronwall_equality_case`, compiles; it checks only that equality-case ODE solution, not the stochastic argument).

**Why the limit is not zero.** Take $dx=-x\,dt+\sigma\,dW$ and $V=x^2$. Then $\mathcal{L}V=-2V+\sigma^2$, so Axiom N holds with $c=2$, $\kappa=1$, and $\mathbb{E}V(X_t)\to\sigma^2/2>0$ for every $\sigma>0$ (script F1). V1's claim that $\mathbb{E}V\to0$ below a threshold $\tau$ is false.

**On the embodiment threshold.** V1 defined $\tau=\sqrt{c/\kappa}$ as a canonical invariant. It is not: replacing $V$ by $\lambda V$ replaces $\kappa$ by $\lambda\kappa$ and $c$ is unchanged, so $\tau\mapsto\tau/\sqrt{\lambda}$; and the claimed characterisation "$\mathcal{L}V<0$ whenever $\|\sigma\|<\tau$" fails near $\Gamma$, where $V=0$ and $\mathcal{L}V=\tfrac12\operatorname{tr}(\sigma^\top\operatorname{Hess}V\sigma)>0$. This version therefore defines no noise threshold as an invariant of $D$. If one is wanted, the honest object is $\tau(V,N):=\sup\{s:\{V\le\kappa s^2/c\}\subset N\}$, the noise level at which the ultimate ball of (iii) still lies in the region where $V$ is adapted. It depends on the choice of $V$ and $N$, and that dependence is part of its definition.

# 3. The winding integral is a holonomy, not an invariant

Let $\omega$ be a 2-form on $S$ with $\omega=d\lambda$ for a chosen primitive $\lambda$, and put $M=S\times\mathbb{R}$, $\alpha=dz-\lambda$. When $\dim S=2$ and $\omega$ is nowhere zero, $\alpha\wedge d\alpha=-dz\wedge\omega$ (up to sign) is nowhere zero, so $(M,\alpha)$ is a contact manifold with Reeb field $\partial_z$. For $\dim S>2$ this needs an even dimension and a non-degenerate $\omega$, neither of which follows from the axioms; it is an extra hypothesis, and on a compact $S$ an exact non-degenerate $\omega$ cannot exist. Both are stated here as hypotheses and not as consequences.

**Definition 3.1.** The *holonomy* of $\Gamma$ for the primitive $\lambda$ is $h_\lambda(\Gamma)=\oint_\Gamma\lambda$.

**Proposition 3.2 [P].**

(a) If $\lambda'$ is another primitive of $\omega$ then $\lambda'-\lambda$ is *closed*, and $h_{\lambda'}(\Gamma)-h_\lambda(\Gamma)=\oint_\Gamma(\lambda'-\lambda)$, which is not zero in general. On the plane $\mathbb{R}^2$ with the origin removed, with $\omega=2r\,dr\wedge d\theta$, $\lambda=r^2d\theta$ and $\lambda'=(r^2-1)d\theta$ give $h=2\pi$ and $h=0$ on $r=1$, with the same $\omega$. (Script F3; `winding_depends_on_primitive` in `gcm-v2/GCMv2Core.lean`, compiles, radial toy only.)

(b) If $\Gamma=\partial D$ for a chain $D\subset S$ then $h_\lambda(\Gamma)=\int_D\omega$ by Stokes. The converse direction in V1 ("nonzero when $\Gamma$ bounds no chain") is not a consequence of Stokes' theorem and is false by (a).

(c) For a smooth family of loops $\Gamma_s$, $\frac{d}{ds}h_\lambda(\Gamma_s)=\oint\omega(\partial_s\Gamma_s,\dot\Gamma_s)\,d\theta$. For $\dot r=r(a-r^2)$ the cycle is $r_0=\sqrt a$ and $h=2\pi a$, so an arbitrarily small $C^1$ perturbation of $a$ moves $h$ by $2\pi\,\delta a$ (scripts F4 and L3).

Consequently the winding integral is **not** invariant under perturbation of the cycle, and V1's Theorem D statement "the same winding number" is false for $h_\lambda$. What does survive: for a *fixed* primitive $\lambda$, $h_\lambda$ is a continuous function of the cycle, with the first variation in (c), and for cycles in one homology class it changes only by $\int\omega$ over the strip between them.

# 4. Theorem B, restated

Let $D_1,D_2$ be dm3 systems with periods $T_1^*,T_2^*$ and Floquet exponents $\mu_1,\mu_2$ (largest transverse exponents). They are in *$k{:}m$ period resonance* if $kT_1^*=mT_2^*$.

**Proposition 4.1 (the product is not a dm3 system) [P].** On $S_1\times S_2$ with $Y_1\oplus Y_2$ the set $\Gamma_1\times\Gamma_2$ is an invariant 2-torus. Its Floquet exponents are $(\mu_1,\mu_2,0,0)$: two neutral directions, so it is not a hyperbolic limit cycle in the sense of Definition 1.1. At $k{:}m$ resonance every orbit on the torus is periodic, so the torus is a continuum of cycles and no single cycle is selected. V1's claim that the unification of two dm3 systems is a dm3 system cannot hold without extra structure that selects a cycle. (Script B1.)

**Proposition 4.2 (the resonance locus) [P].** In $(\mathbb{R}/\mathbb{Z})^2$ the set $\{k\varphi_1-m\varphi_2\in\mathbb{Z}\}$ is a union of $\gcd(k,m)$ circles. It is not the set of $\operatorname{lcm}(k,m)$ points claimed in V1 Proposition 4.21, and so the "resonant orbit $\Gamma_\lambda$" of V1 Definition 4.24 is not a finite point set. The period of the resonant torus orbits is $T_{12}^*=kT_1^*/\gcd(k,m)$, as in V1. (Script L4 in `gcm-v2-verify.py`.)

**Proposition 4.3 (coupling selects cycles) [S].** For weak coupling $Y_\varepsilon=Y_1\oplus Y_2+\varepsilon F$ the torus persists as a normally hyperbolic invariant manifold (Hirsch, Pugh and Shub; Fenichel), and on it the phase difference $\psi$ obeys, to first order in $\varepsilon$, an averaged equation $\dot\psi=\varepsilon\,g(\psi)$. Each simple zero $\psi^*$ of $g$ gives a closed orbit; zeros of $g$ alternate in sign around the circle, so they come in stable/unstable pairs. A dm3 system $D_{12}$ is obtained by choosing a stable zero. This is the standard Arnold-tongue picture; it is cited, not re-derived here.

**Proposition 4.4 (the unified exponent) [P in the model, S in general].** The exponents of the locked cycle are $\mu_1,\mu_2$ and the slow phase exponent $\mu_\varphi=\varepsilon g'(\psi^*)<0$, so
$$\mu_{\max,12}=\max(\mu_1,\mu_2,\mu_\varphi),$$
not $\max(\mu_1,\mu_2)$ as in V1 Theorem 1.2(ii). Model: $x_i'=\mu x_i$, $\theta_1'=1+\varepsilon\sin(\theta_2-\theta_1)$, $\theta_2'=1+\varepsilon\sin(\theta_1-\theta_2)$. The locked cycle has exponents $(\mu,\mu,0,-2\varepsilon)$, so with $\mu=-2$ and $\varepsilon=0.1$ one gets $\mu_{\max,12}=-0.2$, not $-2$. (Script B2.)

**Proposition 4.5 (noise after unification) [P in the model].** Axiom N with an adapted $V$ forces $c\le 2|\mu_{\max,12}|$, so after unification $c_{12}=O(\varepsilon)$. For noise $d\psi=-2\varepsilon\psi\,dt+s\,dW$ on the phase difference, $\mathbb{E}\psi^2\to s^2/(4\varepsilon)$: the ultimate noise ball grows like $1/\varepsilon$ as coupling weakens (script B3). So unification does cost noise tolerance, but through the slow phase mode. V1's inequality $\tau_{12}\le\min(\tau_i)$ came from the bookkeeping choice $c_{12}=\min c_i$, $\kappa_{12}=\max\kappa_i$; that arithmetic is correct but it is a choice, not a consequence of the construction, and $\tau$ is not an invariant (Section 2). It is not claimed here.

**What is not claimed.** The category $\mathbf{dm3}$ with morphisms (M1) to (M4), its pushouts, and the operators $g_i,L_i,R_i,U_i$ of V1 Section 4 are not restated: V1 gives no proof of Propositions 4.3 and 4.19, and the pushout construction rests on the point-set $\Gamma_\lambda$ ruled out by Proposition 4.2. **[O]**

# 5. Theorem C, restated

V1 Theorem C claimed that every dm3 system is locally contact-diffeomorphic to a normal form $\dot\rho=\mu_{\max}(1-e^{-\beta z})\rho$, $\dot\theta=\omega$, $\dot z=\omega-|\mu_{\max}|\rho^2e^{-\beta z}$. The audit found that the derivation does not follow from the stated action (Section 8), that the normal form needs $\dim S=2$, and that the paper's own toy model is not a contact flow (Corollary 5.2). The question that does have an exact answer is: **when does a dissipative flow $Y$ on a surface lift to a contact flow on $S\times\mathbb{R}$ with $\alpha=dz-\lambda$?**

Let $S$ be a connected surface, $\omega=d\lambda$ an area form, $Y$ a vector field on $S$ independent of $z$, and $X=Y+(\lambda(Y)+h)\,\partial_z$ a lift, with $h=h(s,z)$.

**Proposition 5.1 (contact lifts) [P].**

(a) $\mathcal{L}_X\alpha=f\alpha$ for some $f$ if and only if $\iota_Y\omega=d_sh+h_z\lambda$, and then $f=h_z$.

(b) If $Y$ does not depend on $z$, then $h=cz+h_0(s)$ for a constant $c$, $f=c$, and $\mathcal{L}_Y\omega=c\,\omega$, i.e. $\operatorname{div}_\omega Y\equiv c$.

(c) If $Y$ has a hyperbolic limit cycle $\Gamma$ with exponent $\mu$, then $c=\mu$.

(d) On an annular neighbourhood of $\Gamma$, a lift exists if and only if $\mathcal{L}_Y\omega=\mu\,\omega$ and the holonomy $h_\lambda(\Gamma)=\oint_\Gamma\lambda$ is zero.

*Proof.* (a) $\alpha(X)=h$ and $\iota_X d\alpha=-\iota_Y\omega$, so $\mathcal{L}_X\alpha=dh-\iota_Y\omega=h_z\,dz+(d_sh-\iota_Y\omega)$. This equals $f(dz-\lambda)$ exactly when $f=h_z$ and $\iota_Y\omega=d_sh+h_z\lambda$. (b) Differentiate in $z$: with $u=h_z$, $d_su=-u_z\lambda$. Apply $d_s$: $0=-d_su_z\wedge\lambda-u_z\,\omega$, and $d_su_z=-u_{zz}\lambda$ makes the first term vanish, so $u_z\omega=0$, hence $u_z=0$, hence $d_su=0$ and $u=c$. Then $\iota_Y\omega=dh_0+c\lambda$, and applying $d$ gives $\mathcal{L}_Y\omega=c\,\omega$. (c) By Liouville, $\oint_\Gamma\operatorname{div}_\omega Y\,dt$ is the sum of the Floquet exponents times $T^*$, that is $\mu T^*$ (the exponent along the cycle is $0$), so $c=\mu$. (d) $\eta=\iota_Y\omega-\mu\lambda$ is closed, since $\mathcal{L}_Y\omega=\mu\omega$. On an annulus it is exact iff $\oint_\Gamma\eta=0$. Along $\Gamma$, $Y$ is tangent and $\omega(Y,Y)=0$, so $\oint_\Gamma\iota_Y\omega=0$ and $\oint_\Gamma\eta=-\mu\,h_\lambda(\Gamma)$; since $\mu\neq0$, exactness is equivalent to $h_\lambda(\Gamma)=0$. Conversely if $\eta=dh_0$ take $h=\mu z+h_0$. $\square$ (Checked on the radial family, script C3.)

**Corollary 5.2 (V1's toy model is not a contact flow) [P].** V1's toy $\dot r=r(1-r^2)+2(r-1)e^{-z}$, $\dot\theta=1$, $\dot z=r^2-2(r-1)^2e^{-z}$ with $\alpha=dz-r^2d\theta$ has $\mathcal{L}_X\alpha$ with a non-zero $dr$-component, while $\alpha$ has none, so $\mathcal{L}_X\alpha$ is not a multiple of $\alpha$ (script C1). Its holonomy $h_\lambda(\Gamma)=2\pi\neq0$ also violates Proposition 5.1(d), but its projected dynamics depends on $z$, so (d) is not the cause; the direct computation is.

**What replaces the normal form.** Proposition 5.1 says the dissipation of a contact lift with an autonomous attracting cycle is *linear in $z$*, $h=\mu z+h_0$, with a *constant* rate equal to the cycle's own exponent. There is no $\beta$ and no $e^{-\beta z}$. A normal form for general $Y$ satisfying $\mathcal{L}_Y\omega=\mu\omega$ is not claimed. **[O]** V1's invariant triple $(\mu_{\max},\omega,\beta)$ is withdrawn.

# 6. The toy model, corrected

Take $S=\{r>0\}\times S^1$, $\omega=2r\,dr\wedge d\theta$, the primitive $\lambda=(r^2-1)\,d\theta$ (holonomy $0$ on $r=1$), $\alpha=dz-\lambda$, and for $\mu<0$, $\omega_0>0$:
$$\dot r=\tfrac{\mu}{2}\Big(r-\frac1r\Big),\qquad \dot\theta=\omega_0,\qquad \dot z=\mu z-\omega_0 .$$

**Proposition 6.1 [P].**

1. $\mathcal{L}_X\alpha=\mu\,\alpha$ exactly (script C2). The flow is a contact flow, dissipative with constant rate $\mu$, and $\mathcal{L}_Y\omega=\mu\omega$.
2. The exact solutions are $r^2(t)=1+(r_0^2-1)e^{\mu t}$, $\theta(t)=\theta_0+\omega_0t$, $z(t)=\omega_0/\mu+(z_0-\omega_0/\mu)e^{\mu t}$. Hence every start with $r_0>0$ and any $z_0$ converges to the cycle $\{r=1,\ z=\omega_0/\mu\}$ with the exact rate $e^{\mu t}$. There is no dependence of the basin on $z_0$, unlike the toy of V1.
3. The Floquet exponents of that cycle are $(\mu,\mu,0)$.
4. The holonomy of $\lambda$ on $r=1$ is $0$; changing to $\lambda=r^2d\theta$ makes it $2\pi$ and, by Proposition 5.1(d), destroys the contact lift. The primitive is part of the model.

Lean: `gcm-v2/GCMv2Toy.lean` states the two exact solutions and the $d\theta$-coefficient identity. It has **not** been compiled; its docstring says what each theorem does and does not say.

# 7. Theorem D, restated

**Theorem D′.**

1. **[S]** For every dm3 system there is some $\varepsilon_0(Y)>0$ such that every $C^1$-perturbation $Y+F$ with $\|F\|_{C^1}<\varepsilon_0$ has a unique hyperbolic limit cycle $\Gamma'$ near $\Gamma$, with period and exponents varying continuously (implicit function theorem on the Poincare map; Hirsch, Pugh, Shub for the normally hyperbolic case). Cited, not re-derived.
2. **[P]** The explicit radius of V1, $\varepsilon_0=\tfrac12|\mu_{\max}|/\sup_\Gamma\|\operatorname{Hess}V\|$ (abstract and Remark 7.3) or $|\mu_{\max}|/(2(1+\sup_\Gamma\|\operatorname{Hess}V\|))$ (Theorem 1.4), is wrong.
   *(a) It depends on $V$ and the cycle's persistence does not.* Replacing $V$ by $cV$ multiplies the abstract formula by $1/c$ (script D1).
   *(b) Counterexample, with a global Lyapunov function.* On the cylinder $\mathbb{R}\times S^1$ with metric $dx^2+d\theta^2$ let $\dot x=f_e(x)=-e\tanh(2x/e)$, $\dot\theta=1$. The field is bounded and smooth, so the flow is complete. $x=0$ is a hyperbolic cycle with $\mu=f_e'(0)=-2$ for every $e>0$. $V=x^2$ has $\dot V=2xf_e(x)<0$ for $x\neq0$, so it is a global Lyapunov function, with $\operatorname{Hess}V=2$. The formulas give $1/2$ or $1/3$, whatever $e$ is. But $|f_e|<e$ everywhere, so the constant perturbation $F=\delta\,\partial_x$ with $|\delta|\ge e$ ($\|F\|_{C^1}=\delta$) leaves $f_e+\delta$ with no zero: **the cycle is destroyed.** With $e=0.1$ and $\delta=0.2$: $\|F\|_{C^1}=0.2$ is below both claimed radii. The true persistence radius is exactly $e$ (for $|\delta|<e$ a zero remains, at $x=-\tfrac e2\operatorname{artanh}(\delta/e)$) and can be made arbitrarily small with $\mu$ and $\operatorname{Hess}V$ fixed (script D2).
3. **[P]** The claim "the same winding number" is false for $h_\lambda$ (Section 3).
4. **[O]** A computable radius in terms of the Poincare map's second derivative or of the adapted-norm constants. The example in 2(b) shows that no formula in $\mu_{\max}$ and $\operatorname{Hess}V$ alone can work, because the radius there is controlled by the size of the nonlinearity ($e$), which neither quantity sees.
5. **[O]** The composition bound $\prod(1+\delta_i)-1$ for sequences of operators (V1 Step 2) has no derivation, and the operators are not restated (Section 4).

# 8. What is still open or withdrawn

* **The action principle (V1 Section 6.5, Theorem 6.7, Proposition 6.8).** For the action as written, $S[\gamma]=\int(\dot z-\lambda(\dot s)-H(s,z))\,dt$ with $H$ independent of a momentum, the Euler-Lagrange equations are $\partial_zH=0$ and (in the radial toy) $r\dot r=0$, which force $V=0$ (script F6 in `engineering/gcm-paper-audit.py`). Theorem 6.7 also uses a momentum $p$ that V1 never introduces, and on shell the integrand of $S$ vanishes, so $S[\gamma|_\Gamma]=0$, not $\oint\lambda$. A correct variational principle for contact dynamics is Herglotz's; restating the theory on it is **[O]** and is not claimed.
* **Definition 6.4 / Proposition 6.5.** The phase part $H_{\mathrm{ph}}=\tfrac12\omega(Y,Y)=0$ identically because $\omega$ is alternating, so $Y$ cannot be recovered from it. Section 5 replaces the construction by the exact lift criterion.
* **Theorem 6.9 (Noether) and Corollary 6.10.** Unverified. **[O]**
* **Proposition 6.11.** $B_1\times\mathbb{R}$ has even dimension and cannot carry a contact form, and $\hat B_3$ cannot be Legendrian for $n>1$ (dimension $2n-1\neq n$). Withdrawn.
* **Higher dimension.** Everything in Sections 5 and 6 is for $\dim S=2$. For $\dim S>2$ one needs an even dimension and an exact non-degenerate $\omega$ as extra hypotheses (Section 3). **[O]**
* **V1's appendices** were placeholders and are not carried over. V1's statement that the companion paper contains the complete verification is replaced by Section 6 here and by the scripts and Lean files named in the text.
