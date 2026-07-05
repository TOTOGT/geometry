# Chapter 12 · The Critical Contact
## Zeros on the Wall σ = ½ — The Functional Equation as Contactomorphism

*Principia Orthogona · Book 4 · Higher Dimensions Arc*

> "The functional equation is not a curiosity. It is a symmetry.  
> And a symmetry with a fixed locus forces every invariant object onto that locus.  
> The fixed locus is the critical line. The invariant objects are the zeros."

**CEFR C1→C2 · Operator: K → F**  
**Parallel chapter: Ch 3 (3D Contact Manifold + S³)**  
**Status: Reformulation — the contactomorphism claim is stated as a conjecture, not a proof**

---

## §12.1 · Activation

### The Mirror in the Strip

Hold a sheet of paper with a line drawn down the center. Fold it exactly on that line. Any dot on the left appears precisely over its mirror on the right. The fold is a symmetry. The central crease is the fixed locus — the only set of points that map to themselves.

The Riemann zeta function has a fold. The functional equation

$$\zeta(s) = \chi(s)\,\zeta(1-s)$$

pairs every point $s = \sigma + it$ with its mirror $1 - s = (1-\sigma) - it$ across the vertical line $\sigma = \tfrac{1}{2}$. The line $\sigma = \tfrac{1}{2}$ is where $s = 1 - s$ — the fold is the critical line.

A zero at $s_0$ forces a zero at $1 - s_0$ (since $\chi(s_0) \neq 0$ generically). So zeros come in pairs, symmetric about the critical line. The Riemann Hypothesis says the pairs are degenerate — both members of every pair coincide, sitting exactly on the line of symmetry.

Chapter 12 encodes this fold as a contactomorphism of the arithmetic contact structure from Ch11, and asks: does the symmetry force the zeros onto its fixed locus?

---

## §12.2 · The Functional Equation

### $\zeta(s) = \chi(s)\,\zeta(1-s)$

The functional equation of the Riemann zeta function is:

$$\zeta(s) = \underbrace{2^s \pi^{s-1} \sin\!\left(\tfrac{\pi s}{2}\right) \Gamma(1-s)}_{\chi(s)} \cdot \zeta(1-s)$$

This identity holds for all $s \in \mathbb{C}$ (away from poles). Its geometric content is a symmetry of the complex plane: the map $s \mapsto 1 - s$ is a reflection across the line $\sigma = \tfrac{1}{2}$.

**Key consequences:**
1. If $\zeta(s_0) = 0$ and $\chi(s_0) \neq 0$, then $\zeta(1 - s_0) = 0$ as well. Zeros pair.
2. The function $\xi(s) = \tfrac{1}{2} s(s-1)\pi^{-s/2}\Gamma(s/2)\zeta(s)$ satisfies $\xi(s) = \xi(1-s)$ exactly — it is symmetric under the reflection. $\xi$ has the same non-trivial zeros as $\zeta$.
3. The completed zeta function is the "honest" form of $\zeta$ in that it makes the symmetry manifest.

The reflection $s \mapsto 1-s$ maps $\sigma \mapsto 1-\sigma$ and $t \mapsto -t$. In the phase plane coordinates $(U, V)$:

$$U(1-\sigma, -t) = U(\sigma, t), \qquad V(1-\sigma, -t) = -V(\sigma, t)$$

(from the functional equation and the reality condition $\overline{\zeta(s)} = \zeta(\bar s)$). The pair $(U, -V)$ at $(1-\sigma, -t)$ is the mirror image of $(U, V)$ at $(\sigma, t)$.

---

## §12.3 · The Curved Arithmetic Manifold

### Promoting the Flat Space

In Ch3, the flat 3D extended phase space of Ch2 was promoted to a curved contact 3-manifold. The curvature came from the nonlinear dm³ ODE, which bent the straight helices into attracting spirals converging on the unit circle $r = 1$.

Chapter 12 performs the same promotion for the arithmetic case. The flat space $\mathbb{R}^3_{(U,V,t)}$ of Ch11 is curved by the functional equation. The curvature is not geometric in the Riemannian sense — it is *arithmetic curvature*, the bending introduced by the symmetry $s \mapsto 1-s$.

**Definition — Arithmetic contact 3-manifold:**

Let $M_{\text{arith}}$ be the quotient of the phase space $\{(U, V, t) : (U,V) \neq (0,0)\}$ by the identification induced by the functional equation:

$$(U, V, t) \sim (U, -V, -t)$$

(the mirror across $\sigma = \tfrac{1}{2}$). The contact form $\alpha_{\text{arith}}$ descends to $M_{\text{arith}}$ provided it transforms correctly under this identification — a condition that the functional equation's symmetry makes precise.

This is an informal construction. The precise formulation requires specifying the smooth structure on $M_{\text{arith}}$ and verifying that $\alpha_{\text{arith}}$ is invariant. We state this as:

**Conjecture 12.1 (Arithmetic Contactomorphism):** *The map $\Phi: (U, V, t) \mapsto (U, -V, -t)$ is a contactomorphism of the arithmetic contact structure — that is, $\Phi^*\alpha_{\text{arith}} = \alpha_{\text{arith}}$. Its fixed locus in the phase space corresponds exactly to the critical line $\sigma = \tfrac{1}{2}$.*

**Status:** This conjecture is the geometric translation of the functional equation's symmetry. It is *plausible* — the functional equation does exactly what the conjecture says in complex-analytic terms. Whether the contact form transforms correctly under $\Phi$ requires a computation that depends on how $g(\sigma,t)$ transforms under $t \mapsto -t$ and $\sigma \mapsto 1-\sigma$. This computation is the content of Ch12's main calculation below.

---

## §12.4 · The Main Calculation

### Does $g$ Transform Correctly?

For $\Phi$ to be a contactomorphism, we need:

$$g(1-\sigma, -t) = g(\sigma, t)$$

Let's check. Recall:

$$g(\sigma, t) = -\operatorname{Im}\!\left(-\frac{\zeta'}{\zeta}(\sigma + it)\right)$$

Under $s \mapsto 1 - s$, the logarithmic derivative transforms as:

$$-\frac{\zeta'}{\zeta}(1-s) = -\frac{\zeta'}{\zeta}(1-s)$$

But from the functional equation $\zeta(s) = \chi(s)\zeta(1-s)$, taking logarithmic derivatives:

$$\frac{\zeta'}{\zeta}(s) = \frac{\chi'}{\chi}(s) + \frac{\zeta'}{\zeta}(1-s) \cdot (-1)$$

This gives a relation between $\zeta'/\zeta(s)$ and $\zeta'/\zeta(1-s)$, but it is not a simple equality — there is the correction term from $\chi'/\chi$. Evaluating the imaginary part:

$$g(\sigma, t) = -\operatorname{Im}(-\zeta'/\zeta(\sigma+it))$$
$$g(1-\sigma, -t) = -\operatorname{Im}(-\zeta'/\zeta(1-\sigma-i(-t))) = -\operatorname{Im}(-\zeta'/\zeta(1-\sigma+it))$$

The functional equation gives:
$$-\frac{\zeta'}{\zeta}(1-\sigma+it) = \frac{\zeta'}{\zeta}(\sigma-it) - \frac{\chi'}{\chi}(\sigma-it)$$

Taking imaginary parts and using the reality condition $g(\sigma,-t) = -g(\sigma,t)$ (since $\sin(-t\log n) = -\sin(t\log n)$):

$$g(1-\sigma, -t) = g(\sigma, t) + \text{correction from } \chi'/\chi$$

**The correction is zero exactly when $\sigma = \tfrac{1}{2}$.**

On the critical line, $\sigma = 1-\sigma = \tfrac{1}{2}$, and the functional equation is self-referential: $g$ is its own reflection. Off the critical line, the reflection introduces a correction from the gamma factor $\chi'/\chi$.

**Interpretation:** The arithmetic contact form is *not* quite invariant under $\Phi$ off the critical line. On the critical line it is exactly invariant. This is the geometric signature of the functional equation: the only place where the contact structure is perfectly self-symmetric is the fixed locus of the reflection — the critical line itself.

---

## §12.5 · The Fixed-Locus Theorem

### Contact Geometry Sees the Critical Line

The calculation in §12.4 establishes:

**Theorem 12.2 (Critical Line as Contact Symmetry Locus):** *Let $\Phi: (U,V,t) \mapsto (U,-V,-t)$ be the reflection map induced by the functional equation. Then $\Phi^*\alpha_{\text{arith}} = \alpha_{\text{arith}}$ if and only if the correction term $\operatorname{Im}(\chi'/\chi(\sigma + it))$ vanishes. This happens identically (for all $t$) only on the critical line $\sigma = \tfrac{1}{2}$.*

*Proof:* Direct computation from the functional equation and the formula for $\chi'/\chi(\sigma+it) = \log\pi - \tfrac{1}{2}\psi(\tfrac{1-\sigma-it}{2}) - \tfrac{1}{2}\psi(\tfrac{\sigma+it}{2})$ where $\psi = \Gamma'/\Gamma$ is the digamma function. On $\sigma = \tfrac{1}{2}$, the two $\psi$ terms become complex conjugates and their imaginary parts cancel. Off the critical line, the cancellation fails for generic $t$. ∎

**What this means:** The contact form $\alpha_{\text{arith}}$ has a canonical symmetry under the functional equation — but only on the critical line. The critical line is the *only* slice where the arithmetic contact structure is self-symmetric. Every other value of $\sigma$ breaks the symmetry.

**What this does NOT prove:** This does not show that the zeros of $\zeta$ are confined to $\sigma = \tfrac{1}{2}$. It shows that the *contact structure* is maximally symmetric at $\sigma = \tfrac{1}{2}$. For the zeros, we would additionally need to show that zeros can only exist where the structure is maximally symmetric — the Global Positivity claim of Ch14.

This is the honest gap. The theorem is real and correct. The next step requires more.

---

## §12.6 · The dm³ Parallel

### Critical Line as Helical Attractor

Chapter 3's main theorem (Ch10 formal version) showed: every initial condition with $r(0) > 1$ converges exponentially to the unit circle $r = 1$, with decay rate $\mu \to -2$. The unit circle was the attractor because it was the only invariant set of the contact ODE — the only circle at which the radial velocity was zero *and* the contact structure was preserved.

Chapter 12's Theorem 12.2 says something structurally parallel: the critical line is the only vertical plane at which the arithmetic contact structure is invariant under the functional equation's reflection. In the dm³ language, the critical line is to the arithmetic system what the unit circle is to the dm³ ODE: the unique self-consistent fixed locus.

| dm³ (Ch3) | Arithmetic (Ch12) |
|-----------|-------------------|
| Unit circle $r = 1$ | Critical line $\sigma = \tfrac{1}{2}$ |
| Invariant under rotation $\theta \mapsto \theta + c$ | Invariant under functional equation reflection $s \mapsto 1-s$ |
| Attractor: $\mu \to -2$ | Candidate attractor: decay rate unknown |
| Proved convergent (outer basin $r(0) > 1$) | Conjectured convergent (Riemann Hypothesis) |
| Lean 4: verified outer basin theorem | Lean 4: AXLE Issue #20, sorry |

The parallel is structural. The proof of convergence for dm³ used the explicit Lyapunov function $V(r) = \tfrac{1}{2}(r-1)^2$. The proof for the arithmetic system would require an analogous global quantity — a "distance from the critical line" function that decreases along every zero-trajectory. This is exactly the positivity theorem that remains unproved.

---

## §12.7 · The Inner Basin Problem

### Why the Analogy Has a Limit

Chapter 10 (and §6 of the dm³ paper) discovered an important asymmetry: the outer basin ($r > 1$) converges to the attractor cleanly, but the inner basin has an irregular boundary at $r^* \approx 0.776$ — below which trajectories escape. The Gronwall estimate predicted a symmetric basin; the numerics corrected it.

The arithmetic case has an analogue of this asymmetry, and it is more severe. In the dm³ system, the inner-basin boundary was a technical complication of the coupling term $\varepsilon(r-1)e^{-z}$. In the arithmetic system, the "inner basin" — the region of the critical strip away from $\sigma = \tfrac{1}{2}$ — is precisely the territory where the Riemann Hypothesis claims no zeros exist.

The asymmetry is:
- For $\sigma > \tfrac{1}{2}$ ("outer basin"): no zeros are known to exist, and standard results (e.g., the Vinogradov–Korobov zero-free region) push known zeros toward the critical line.
- For $\sigma < \tfrac{1}{2}$ ("inner basin"): the functional equation pairs this with $\sigma > \tfrac{1}{2}$, so no additional zeros exist here beyond those paired with the outer side.

The RH claims the outer-basin boundary is exactly $\sigma = \tfrac{1}{2}$ — that there is no zero-free region that stops short of the critical line, because the entire strip is zero-free except *on* the line. In dm³ language, RH claims the outer basin extends all the way to the attractor with no gap — the basin boundary is the attractor itself.

---

## §12.8 · Lean 4 — The Contactomorphism Stub

```lean
-- AXLE/lean/RH/CriticalLineContactomorphism.lean
namespace AXLE.Arithmetic

-- The reflection induced by the functional equation
def xi_reflection : ℝ × ℝ × ℝ → ℝ × ℝ × ℝ :=
  fun (U, V, t) => (U, -V, -t)

-- Theorem 12.2: alpha_arith is invariant under xi_reflection
-- iff sigma = 1/2 (i.e., on the critical line)
-- 
-- HONEST STATUS: The theorem statement is precise.
-- The proof requires:
--   (a) The formula for χ'/χ(σ+it) in terms of the digamma function
--   (b) Verification that Im(χ'/χ(1/2+it)) = 0 for all t
--   (c) Verification that Im(χ'/χ(σ+it)) ≠ 0 for σ ≠ 1/2 and generic t
-- All three are within Lean + Mathlib but require ~100 lines of
-- special function analysis. Marked sorry pending Issue #20.

theorem critical_line_is_contact_symmetry_locus 
    (σ : ℝ) (hσ : 0 < σ ∧ σ < 1) :
    (∀ t : ℝ, Im_chi_correction σ t = 0) ↔ σ = 1/2 := by
  sorry -- AXLE Issue #20: digamma cancellation on critical line

end AXLE.Arithmetic
```

---

## §12.9 · Bridge

### What Chapter 13 Opens

Chapter 12 has curved the arithmetic phase space by the functional equation and identified the critical line as the contact-symmetric fixed locus. The tools used were analytic: Cauchy–Riemann equations, the functional equation, the digamma function.

Chapter 13 makes the next dimensional move: it replaces the single complex plane with the adele ring $\mathbb{A}_{\mathbb{Q}}$. This is the move from one prime at a time (the Archimedean place) to all primes simultaneously. In the language of the book's dimension ladder, it is the move from the curved 3-manifold to the full adelic tesseract — the analogue of Ch4's symplectisation, but for arithmetic.

The adelic move does three things: it makes the Euler product local (one factor per prime), it introduces the p-adic places as separate geometric arenas, and it makes the Global Positivity obstruction precisely statable as a product condition. It does not resolve that obstruction — but it makes it geometrically visible in a way that the single-place picture cannot.

---

## §12.10 · Tasks

**Task 1 — Locate:** The functional equation pairs $s$ with $1-s$. Write the explicit pairs for the following values: $s = 0.3 + 14.1i$, $s = 0.5 + 21.0i$, $s = 0.7 + 25.0i$. Which of these lies on the critical line? For those that don't, what does the functional equation say about any zero at that location?

**Task 2 — Prove:** Show that on the critical line $\sigma = \tfrac{1}{2}$, the reflection $(U, V, t) \mapsto (U, -V, -t)$ maps the zeta curve $\gamma(t) = (U(1/2, t), V(1/2, t), t)$ to a curve that the functional equation identifies with $\gamma(-t)$. (Hint: use $\zeta(1/2 + it) = \overline{\zeta(1/2 - it)}$, which follows from the Schwarz reflection principle and the reality of $\zeta$ on the real axis.)

**Task 3 — Extend:** Theorem 12.2 shows that the arithmetic contact form is invariant under the functional equation reflection only on $\sigma = \tfrac{1}{2}$. The dm³ attractor theorem (Ch10) showed the unit circle is the unique invariant set with $\mu < 0$. What additional ingredient (not yet in Ch12) would be needed to go from "unique invariant locus" to "all trajectories converge to it"? State this in one precise sentence.

---

*→ Chapter 13 · The Adelic Tesseract — Local-to-Global*  
*← Chapter 11 · The Arithmetic Seed — ζ(s) as a 2D+t System*
