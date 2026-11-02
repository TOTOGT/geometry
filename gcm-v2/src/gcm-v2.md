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

# 4. What is not yet in this version

Theorems B, C and D, the action principle of V1 Section 6, and the toy model are not yet restated. The audit found that Theorem B's torus count is wrong (the resonance locus has $\gcd(k,m)$ components, not $\operatorname{lcm}(k,m)$ points), that the stated Euler-Lagrange equations do not follow from the stated action, that Theorem C holds only for $\dim S=2$, and that V1 gives two different values of $\varepsilon_0$. Those are the next parts. They are listed here so that this draft cannot be read as having settled them.
