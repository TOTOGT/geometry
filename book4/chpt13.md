# Chapter 13 · The Adelic Tesseract
## Local-to-Global — One Contact Form per Prime

*Principia Orthogona · Book 4 · Higher Dimensions Arc*

> "The adele ring is not a clever trick. It is the natural home of the Euler product.  
> Once you see it, the alternative — treating each prime separately — looks like  
> trying to hear a chord by listening to one instrument at a time."

**CEFR C2 · Operator: F — the global fixed point**  
**Parallel chapter: Ch 4 (4D Tesseract — Symplectisation)**  
**Status: Reformulation — calculations correct, global conclusions explicitly labelled as open**

---

## §13.1 · Activation

### The Chord Problem

A chord is not the sum of its notes played one at a time. A C major chord — C, E, G — heard as three successive notes produces information about three pitches. Heard simultaneously, it produces information about their *relationship*: the consonance, the harmonic series they share, the way the frequencies reinforce and interfere. The chord is a global object. The individual notes are its local components.

The Euler product for the Riemann zeta function is a chord:

$$\zeta(s) = \prod_{p \text{ prime}} \frac{1}{1 - p^{-s}} = \frac{1}{1-2^{-s}} \cdot \frac{1}{1-3^{-s}} \cdot \frac{1}{1-5^{-s}} \cdots$$

Each factor $(1 - p^{-s})^{-1}$ is one note — the local contribution of the prime $p$. The product is the chord — the global object, the actual value of $\zeta(s)$.

The contact form $\alpha_{\text{arith}}$ from Ch11 heard this chord through one instrument: the Archimedean place, the real number line. Its coefficient $g(\sigma,t)$ was the Dirichlet series — an infinite sum encoding all primes simultaneously, but through a single real-number lens.

Chapter 13 adds a new instrument for each prime. The result is not louder — it is more precise. The local-to-global assembly makes the constraint on the zeros statable as a product condition, one factor per prime, each factor enforcing a local bound. Together they produce the global arithmetic contact structure on the adele ring.

---

## §13.2 · The Adele Ring

### $\mathbb{A}_{\mathbb{Q}} = \mathbb{R} \times \prod_p' \mathbb{Q}_p$

The adele ring of $\mathbb{Q}$ is:

$$\mathbb{A}_{\mathbb{Q}} = \mathbb{R} \times \prod_{p \text{ prime}}' \mathbb{Q}_p$$

The restricted product $\prod'$ means: an adele is a sequence $(x_\infty, x_2, x_3, x_5, \ldots)$ where $x_\infty \in \mathbb{R}$, $x_p \in \mathbb{Q}_p$ for each prime $p$, and *all but finitely many* of the $x_p$ lie in $\mathbb{Z}_p$ (the p-adic integers, the "unit ball" at each prime).

**Why the adeles?** Because they are the natural domain where the Euler product factorizes completely. The global zeta function is a product over all places (one factor per prime, plus the real place). The adele ring packages all these places into a single object.

A point in $\mathbb{A}_{\mathbb{Q}}$ knows about every prime simultaneously. An ordinary complex number $s = \sigma + it$ knows about $\sigma$ and $t$ — the Archimedean place. An adelic extension of $s$ additionally assigns a $p$-adic parameter $t_p \in \mathbb{Q}_p$ for each prime $p$, with the constraint that almost all $t_p \in \mathbb{Z}_p$.

---

## §13.3 · Local Contact Forms

### One $\alpha_v$ Per Place

The global contact form $\alpha_{\text{arith}}$ decomposes into local contact forms at each place.

**Archimedean place ($v = \infty$):**

This is exactly the form from Ch11:

$$\alpha_\infty = dV_\infty - g_\infty(\sigma, t_\infty)\,dU_\infty$$

where $g_\infty = -\operatorname{Im}(-\zeta'/\zeta(\sigma + it_\infty))$.

**Non-Archimedean place ($v = p$):**

The local Euler factor at prime $p$ is $(1 - p^{-s})^{-1}$. Its logarithmic derivative gives the local coefficient:

$$g_p(t_p) = \frac{\log p}{1 - p^{-\sigma}p^{-it_p}}$$

where $t_p \in \mathbb{Q}_p$ is the local $p$-adic parameter, and we set $c = p^{-\sigma}p^{-it_p}$.

The local contact form at place $p$ is:

$$\alpha_p = dV_p - g_p(t_p)\,dU_p$$

This is well-defined as a rigid-analytic 1-form on the $p$-adic unit disk $|c|_p < 1$ (i.e., for $\sigma > 0$, which is the critical strip).

**Local exterior derivative:**

By the chain rule on the rigid-analytic power series:

$$\partial_{t_p} g_p = -i(\log p)^2 \frac{c}{(1-c)^2}$$

and therefore:

$$d\alpha_p = -(\partial_{t_p} g_p)\,dt_p \wedge dU_p = i(\log p)^2 \frac{c}{(1-c)^2}\,dt_p \wedge dU_p$$

**The local non-integrability 3-form:**

$$\alpha_p \wedge d\alpha_p = -(\partial_{t_p} g_p)\,dV_p \wedge dt_p \wedge dU_p$$

This is non-zero whenever $c \neq 0$ and $(1-c)^2 \neq 0$ — i.e., everywhere in the interior of the unit disk except at $c = 0$ (which would require $\sigma \to \infty$).

---

## §13.4 · The p-Adic Valuation — Corrected Account

### What the Ultrametric Actually Says

A careful account of the p-adic norm, because the previous discussion in this thread (and the Gemini conversation) contained an error that must be corrected.

**The ultrametric inequality:** For $x, y \in \mathbb{Q}_p$:

$$|x + y|_p \leq \max(|x|_p, |y|_p)$$

with equality when $|x|_p \neq |y|_p$.

**For $|c|_p < 1$:** Since $|1|_p = 1$ and $|c|_p < 1$, we have $|1|_p \neq |c|_p$, so:

$$|1 - c|_p = \max(|1|_p, |c|_p) = 1$$

Therefore $|(1-c)^2|_p = 1$ throughout the *entire interior* of the unit disk. The denominator is a p-adic unit everywhere inside.

**Consequence for the local twisting strength:**

$$|\partial_{t_p} g_p|_p = |{-i}|_p \cdot |(\log p)^2|_p \cdot |c|_p / |(1-c)^2|_p = |c|_p = p^{-\sigma} \cdot |p^{-it_p}|_p$$

As $|c|_p \to 1^-$ (approaching the boundary of the disk), this approaches $1$ — not $0$.

**The corrected picture of the p-adic boundary:**

The local contact form $\alpha_p$ is holomorphic inside the unit disk $|c|_p < 1$. At the boundary $|c|_p = 1$, the denominator $(1-c)$ can be zero (when $c = 1$, i.e., when $p^{-s} = 1$), and the local Euler factor has a pole. The "wall" at the boundary is a *pole*, not a smooth boundary. The flow cannot cross this wall because the local form ceases to be holomorphic there — not because the norm of the coefficient collapses.

What was incorrectly described as "the norm goes to zero, locking the trajectory inside" is more precisely: "the pole of the Euler factor at $c = 1$ marks the boundary of the holomorphic domain; no trajectory governed by a holomorphic contact form can pass through a pole."

**The correct statement of the p-adic constraint:** The local contact form $\alpha_p$ is defined and non-degenerate on the rigid-analytic disk $|c|_p < 1$. The boundary of this disk is the locus where the local Euler factor $(1-p^{-s})^{-1}$ has a pole — not a zero of $\zeta$, but a singularity of the local Euler factor itself. The global adelic form is assembled over the product of these disks, and the restricted product structure ensures that the global form is well-defined precisely on the set where all local Euler factors are holomorphic.

---

## §13.5 · Global Assembly

### The Restricted Product and the Global Form

The global arithmetic contact form is assembled from the local forms via the restricted direct product:

$$\alpha_{\text{arith}} = \sum_v \alpha_v \qquad \text{(restricted sum)}$$

The global exterior derivative commutes with localization (because exterior calculus is local and the places are independent):

$$d\alpha_{\text{arith}} = \sum_v d\alpha_v$$

**The global non-integrability condition:**

$$\alpha_{\text{arith}} \wedge d\alpha_{\text{arith}} \neq 0 \quad \text{on } \mathbb{A}_{\mathbb{Q}}/\mathbb{Q}^\times$$

is *not* simply the product $\prod_v (\alpha_v \wedge d\alpha_v) \neq 0$ — because the adele class space is not a Cartesian product. It is the statement that the restricted product of the local 3-forms is nowhere-vanishing on the adele class space.

**How the local forms lock together:** The Archimedean place contributes twisting from the quasi-periodic series $\partial_{t_\infty} g_\infty$ — dense and non-vanishing by the $\mathbb{Q}$-linear independence of $\{\log p\}$. The non-Archimedean places contribute holomorphicity constraints — the local form at each prime $p$ is non-degenerate precisely on the domain where $p^{-s}$ lies inside the unit disk.

Together, they produce a global contact structure on the adele class space whose non-vanishing is enforced from two independent directions: the Archimedean analytic density and the non-Archimedean rigid-analytic holomorphicity.

---

## §13.6 · The Adelic Zeta Curve

### Every Place Contributes

In the Archimedean picture (Ch11), the zeta curve was $\gamma(t) = (U(\sigma,t), V(\sigma,t), t)$ in $\mathbb{R}^3$. In the adelic picture, the curve has one component per place:

$$\gamma_{\mathbb{A}}(\mathbf{t}) = \bigl((U_\infty, V_\infty, t_\infty),\; (U_2, V_2, t_2),\; (U_3, V_3, t_3),\; \ldots\bigr)$$

Each component $\gamma_p$ lives in the local phase space $\mathbb{Q}_p^3$. The global curve lives in the adelic phase space $\mathbb{A}_{\mathbb{Q}}^3$ (with appropriate topology).

A zero of $\zeta$ is now a piercing event in the *global* adelic phase space: a point where the Archimedean component pierces the axis $U_\infty = V_\infty = 0$ while the $p$-adic components remain inside their respective holomorphic disks.

The Riemann Hypothesis says: all such global piercing events occur only on the critical hyperplane $\sigma = \tfrac{1}{2}$.

---

## §13.7 · Comparison — Connes and Consani

### The Same Space, Different Instruments

Alain Connes and Caterina Consani have developed the arithmetic site and scaling site — geometric objects over the adele class space $\mathbb{A}_{\mathbb{Q}}/\mathbb{Q}^\times$ that encode the Riemann zeros in the language of algebraic geometry over the "field with one element" $\mathbb{F}_1$.

The comparison is illuminating:

| Connes–Consani | This chapter (GTCT) |
|----------------|---------------------|
| Topos $\widehat{\mathbb{N}^\times}$ with structure sheaf over $\mathbb{B} = \{0,1\}$ | Adelic contact manifold $M_{\text{arith}}$ over $\mathbb{A}_{\mathbb{Q}}$ |
| Frobenius correspondences | GTCT operator $G = U\circ F\circ K\circ C$ |
| Scaling site points = adele class space | Global adelic phase space $\mathbb{A}_{\mathbb{Q}}^3/\mathbb{Q}^\times$ |
| Missing Riemann–Roch on site square | Missing Global Positivity Theorem (Ch14) |
| Hasse–Weil zeta = spectrum of scaling action | $\alpha_{\text{arith}}$ non-integrability = prime-driven twisting |
| Status: open (Riemann–Roch not proved) | Status: open (Positivity not proved) |

The frameworks are different instruments playing the same chord. Connes–Consani works in the language of algebraic geometry and toposes. GTCT works in the language of contact geometry and differential forms. Both identify the same obstruction and express it as a missing positivity/non-degeneracy statement.

The value of the comparison is not that one proves the other — neither proves RH — but that agreement of two independent geometric frameworks at the same obstruction is evidence that the obstruction is structural, not an artifact of the approach.

---

## §13.8 · The Adelic Magic Square

### 13 = The Thirteenth Place

There is a numerological curiosity worth noting in the spirit of Ch6 (The 111 Square). The prime 13 is the 6th prime (2, 3, 5, 7, 11, **13**). In the adele ring, the first six non-Archimedean places are $p = 2, 3, 5, 7, 11, 13$. The restricted product up to the 13th prime would give a finite approximation to the adelic contact structure with exactly 6 prime factors — a natural finite adelic truncation at the G⁶ threshold.

The finite adelic approximation:

$$\mathbb{A}_{\mathbb{Q}}^{(13)} = \mathbb{R} \times \mathbb{Q}_2 \times \mathbb{Q}_3 \times \mathbb{Q}_5 \times \mathbb{Q}_7 \times \mathbb{Q}_{11} \times \mathbb{Q}_{13}$$

has dimension $2 \times 7 = 14$ over $\mathbb{R}$ (each factor contributing a 2D phase plane). This 14-dimensional space is the arithmetic tesseract up to the G⁶ threshold.

The 6×6 magic square of Ch6 had rows summing to 111. The finite adelic approximation has 7 places (one Archimedean, six prime) — not 6. But if we think of the adelic picture as a 7-voice chord, the sixth prime place is the last one that closes the G⁶ cycle. Adding the 7th prime (17) opens the next octave.

This observation is speculative. It is stated as an open pattern, not a theorem.

---

## §13.9 · Lean 4 — Adelic Structure

```lean
-- AXLE/lean/RH/AdelicContact.lean
namespace AXLE.Arithmetic.Adelic

-- The local Euler factor coefficient at prime p
noncomputable def g_p (p : ℕ) (hp : Nat.Prime p) (σ t_p : ℝ) : ℝ :=
  -- log p / (1 - p^{-σ} · p^{-it_p})
  -- Defined only for p^{-σ} < 1, i.e., σ > 0
  sorry -- AXLE Issue #21: p-adic local coefficient

-- The local non-integrability coefficient
noncomputable def dg_p (p : ℕ) (hp : Nat.Prime p) (σ t_p : ℝ) : ℂ :=
  -- -i (log p)² · c / (1-c)²   where c = p^{-σ-it_p}
  let c := Complex.exp (-(↑σ + Complex.I * t_p) * Real.log p)
  -(Complex.I * (Real.log p)^2 * c / (1 - c)^2)

-- Correctness of the p-adic norm computation
-- (This is the corrected version — NOT the erroneous "norm collapses to 0")
lemma dg_p_norm_correct (p : ℕ) (hp : Nat.Prime p) (σ t_p : ℝ) 
    (hσ : 0 < σ) :
    -- The p-adic norm of dg_p equals |c|_p = p^{-σ} · |p^{-it_p}|_p
    -- which approaches 1, NOT 0, as σ → 0+
    -- The boundary |c|_p = 1 is a pole, not a smooth wall.
    True := trivial -- placeholder for norm calculation

-- Global assembly: the adelic contact form
-- (formal declaration; proof of non-degeneracy is Ch14's content)
axiom adelic_contact_form_nondegenerate : 
    -- ∀ (s : AdelicPoint) in the admissible domain,
    -- alpha_arith ∧ d(alpha_arith) ≠ 0
    True -- AXLE Issue #22: requires Global Positivity (Ch14)

end AXLE.Arithmetic.Adelic
```

The axiom at Issue #22 is precisely the statement that Ch14 will address — and honestly label as open.

---

## §13.10 · Bridge

### What Chapter 14 Opens

Chapter 13 has assembled the global adelic contact structure: local forms at each place, restricted product gluing, corrected p-adic analysis. Everything is in place except one thing: the proof that the non-integrability forces zeros to $\sigma = \tfrac{1}{2}$.

Chapter 14 is the final rung. It states the missing piece as precisely as possible — the Global Positivity Theorem — and examines what would be needed to prove it. It looks at the function-field analogue, where the analogous statement is already proved (Weil 1948, Deligne 1974), and extracts the mechanism that makes the proof work there. It asks: what is the arithmetic analogue of Riemann–Roch, and can the GTCT framework suggest where to find it?

Chapter 14 does not prove the Riemann Hypothesis. It is the honest description of the last door — the one that remains locked.

---

## §13.11 · Tasks

**Task 1 — Local calculation:** Using the formula $g_p(t_p) = \log p / (1 - p^{-\sigma}p^{-it_p})$ for $p = 2$ and $\sigma = 1$, compute $|g_2(t_2)|$ as a function of $t_2 \in \mathbb{R}$. What is the maximum value? At what values of $t_2$ is this maximum achieved?

**Task 2 — Norm verification:** Let $c = p^{-\sigma}p^{-it_p}$ with $\sigma > 0$ and $p = 3$. Using the ultrametric inequality, verify that $|1 - c|_3 = 1$ when $|c|_3 < 1$. Conclude that $|(1-c)^2|_3 = 1$. Then compute $|\partial_{t_p} g_p|_3 = |c|_3 = 3^{-\sigma} \cdot |p^{-it_p}|_3$. What happens as $\sigma \to 0^+$?

**Task 3 — Comparison:** The Connes–Consani arithmetic site uses the structure sheaf valued in the Boolean semifield $\mathbb{B} = \{0, 1\}$ (tropical/characteristic-1 arithmetic). The GTCT adelic structure uses differential forms over $\mathbb{Q}_p$. In two sentences: what is the conceptual difference between these two ways of encoding the Euler product geometrically? What does each approach see that the other might miss?

---

*→ Chapter 14 · The Positivity Rung — What Remains*  
*← Chapter 12 · The Critical Contact — Zeros on the Wall σ = ½*
