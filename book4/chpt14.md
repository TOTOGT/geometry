# Chapter 14 · The Positivity Rung
## What Remains — The Open Door and the Function-Field Key

*Principia Orthogona · Book 4 · Higher Dimensions Arc*

> "The last rung of the ladder is not missing.  
> It is visible. You can touch it.  
> You cannot yet stand on it."

**CEFR C2→D1 · Operator: U — the honest unification**  
**Parallel chapters: Ch 5 (OPERA SATOR) + Ch 6 (111 Square)**  
**Status: Open conjecture — clearly labelled, function-field proof examined, future directions stated**

---

## §14.1 · Activation

### The Last Move

A chess player sees the winning position three moves before it arrives. The pieces are arranged. The logic is clear. But the move that closes it has not been played. The position is not won until the move is made.

Chapters 11–13 have arranged the pieces. The arithmetic contact form exists. The functional equation gives it a symmetry whose fixed locus is the critical line. The adelic structure assembles the Euler product place-by-place. The non-integrability holds almost everywhere. Everything is in position.

The move that closes it — the Global Positivity Theorem — has not been played. Chapter 14 is the honest account of why not, what it would look like if it were, and where the opening might be found.

This chapter does not prove the Riemann Hypothesis. It describes the proof's last door precisely enough that a reader who finds the key will recognize the lock.

---

## §14.2 · The Obstruction — Stated Precisely

### Global Positivity Theorem (Open)

Everything built in Ch11–13 would imply the Riemann Hypothesis if the following statement were true:

**Global Positivity Theorem (Conjecture 14.1):** *The natural action of the idele class group $\mathbb{A}_{\mathbb{Q}}^\times / \mathbb{Q}^\times$ on the kernel $\ker\alpha_{\text{arith}}$ of the global arithmetic contact form is positive-definite. Equivalently: the "twisting energy" of the arithmetic contact structure is strictly minimized on the critical hyperplane $\sigma = \tfrac{1}{2}$, and any zero-trajectory at $\sigma \neq \tfrac{1}{2}$ would force $\alpha_{\text{arith}} \wedge d\alpha_{\text{arith}} = 0$ at some adelic point.*

**Why this implies RH:** If the contact structure is maximally non-integrable (i.e., $\alpha_{\text{arith}} \wedge d\alpha_{\text{arith}} \neq 0$ everywhere on the admissible domain), and if the action of the idele class group is positive-definite on $\ker\alpha_{\text{arith}}$, then any zero-trajectory must lie in the fixed locus of the positive-definite action — which by Theorem 12.2 is exactly the critical line $\sigma = \tfrac{1}{2}$.

**Why this is precisely RH:** The statement of Conjecture 14.1 encodes exactly the same arithmetic information as the classical RH. It is not a simplification. It is a reformulation in contact-geometric language. The proof of Conjecture 14.1 would be a proof of RH by another name.

**What the conjecture adds:** A precise geometric question. Instead of "do the zeros lie on the line?", we ask "is the idele-class-group action positive-definite on this specific kernel?" This second question has the form of a problem in functional analysis and representation theory — a domain with powerful tools (trace formulas, spectral theory, L-functions) that may be easier to connect than the original complex-analytic question.

---

## §14.3 · The dm³ Parallel — Why It Worked There

### How the Smooth Case Was Proved

In Ch3 and Ch10, the convergence to the helical attractor was proved by an explicit Lyapunov function: $V(r) = \tfrac{1}{2}(r-1)^2$. Along any outer-basin trajectory:

$$\frac{d}{dt} V(r(t)) = (r-1)\dot{r} = (r-1)\bigl[r(1-r^2) + \varepsilon(r-1)e^{-z}\bigr]$$

For $r > 1$ and $z \to \infty$, the coupling term vanishes and the leading term is $(r-1) \cdot r(1-r^2) < 0$ (since $r > 1$ makes $1-r^2 < 0$). The Lyapunov function decreases along trajectories — this is the positive-definiteness of the convergence mechanism.

The dm³ proof worked because:
1. There was an explicit positive-definite function $V$ measuring distance from the attractor.
2. Its derivative along trajectories was explicitly negative outside the attractor.
3. The structure of the ODE made this computable in closed form.

For the arithmetic case, step (1) requires a "distance from the critical line" function that is positive-definite with respect to the idele-class-group action. This function, if it existed, would be an explicit element of the Selberg trace formula or the Weil explicit formula — something already known to exist in the theory of L-functions, but not yet connected to the contact-geometric framework.

---

## §14.4 · The Function-Field Key

### Where Everything Already Works

There is one setting where the Riemann Hypothesis is proved: **function fields**.

Let $C$ be a smooth projective curve of genus $g$ over a finite field $\mathbb{F}_q$. The zeta function of $C$ is:

$$Z(C, q^{-s}) = \exp\!\left(\sum_{n=1}^\infty \frac{|C(\mathbb{F}_{q^n})|}{n} q^{-ns}\right)$$

The analogue of RH for $Z(C, q^{-s})$ — that all zeros have $\operatorname{Re}(s) = \tfrac{1}{2}$ — was proved by Weil (1948 for curves) and Deligne (1974 for general varieties).

**The mechanism of the proof:** Weil's proof for curves used:
1. The Riemann–Roch theorem on $C$, which gives an explicit formula for the number of points on the curve.
2. The Weil pairing on the Jacobian of $C$, which produces a positive-definite Hermitian form.
3. The Cauchy–Schwarz inequality applied to this form.

The positivity came from the **Riemann–Roch theorem** — an algebraic geometry result that gives an explicit, computable formula for divisors on a curve. The Hermitian form is positive-definite *because Riemann–Roch says so*, and the zeros are confined to $\sigma = \tfrac{1}{2}$ *because the positivity says so*.

**The analogue over $\mathbb{Q}$:** For the classical Riemann zeta function over $\mathbb{Q}$, there is no direct analogue of Riemann–Roch on a "curve over $\mathbb{F}_1$." The Connes–Consani program is, at its core, an attempt to construct such an analogue — the arithmetic site and scaling site are the geometries over $\mathbb{F}_1$ that would support a Riemann–Roch theorem.

**What the function-field proof looks like in GTCT language:**

In the function-field case, the contact form $\alpha_{\text{arith}}$ over $\mathbb{F}_q$ has a *finite-dimensional* kernel (because the Euler product is a finite product for each degree). The positivity of the Hermitian form (Weil pairing) is the contact-geometric statement that the idele-class-group action is positive-definite. Riemann–Roch provides the explicit formula that makes this positivity checkable.

| Function field ($\mathbb{F}_q$) | Number field ($\mathbb{Q}$) |
|--------------------------------|---------------------------|
| Riemann–Roch theorem (proved) | Analogous arithmetic Riemann–Roch (open) |
| Weil pairing — positive definite | Idele-class action — positive definite? |
| Finite-dimensional kernel | Infinite-dimensional kernel |
| RH: proved (Weil 1948) | RH: open |
| dm³ contact form: finite-dimensional ODE | dm³ arithmetic form: infinite Dirichlet series |

The function-field proof is the proof schema. The missing piece over $\mathbb{Q}$ is the positive-definite Hermitian form — the arithmetic Weil pairing.

---

## §14.5 · The 111 Arithmetic Square

### What the Magic Square Says About Positivity

Chapter 6 built the 6×6 magic square with rows summing to 111. Every row, column, diagonal, and path through the square preserved the invariant 111. The GTCT group (Galilean Contact Transformations) preserved this invariant. Zeros of the dm³ system — the fixed points — were confined to the cell structure where all paths sum correctly.

The arithmetic analogue:

The six coordinates of the 6D arithmetic jet space (from Ch5–6, now applied to the zeta setting) are:
- $x$ = adelic time parameter
- $y_1 = \operatorname{Re}\zeta$, $y_2 = \operatorname{Im}\zeta$ (the zeta values)  
- $p_1, p_2 = \operatorname{Re}(-\zeta'/\zeta), \operatorname{Im}(-\zeta'/\zeta)$ (the slopes — the von Mangoldt data)
- $t$ = imaginary part of $s$ (the frequency)

The functional equation acts on this 6D space by:

$$(x, y_1, y_2, p_1, p_2, t) \mapsto (x, y_1, -y_2, p_1, -p_2, -t)$$

The fixed locus of this action (the "central column" of the arithmetic magic square) is the set of points where $y_2 = 0$ and $p_2 = 0$ and $t = 0$ simultaneously — which for the zeta function describes the critical line (where $\zeta$ is real, i.e., on the real axis — but by analytic continuation, the critical line at $\sigma = \tfrac{1}{2}$ is where this symmetry is exact).

**Conjecture 14.2 (Arithmetic 111-Invariant):** *The functional equation symmetry on the 6D arithmetic jet space preserves a weighted sum of the six coordinate contributions. All zero-trajectories invariant under this symmetry sum to the same invariant — the arithmetic analogue of 111. The zero-trajectories at $\sigma \neq \tfrac{1}{2}$ would violate this invariant.*

This conjecture is at the same level as Conjecture 14.1 — they are the same obstruction stated in two different languages. The magic-square language makes the symmetry constraint visual. The positivity language makes it analytically precise.

---

## §14.6 · Three Approaches to the Missing Step

### What Might Work

There are three known frameworks that approach the Global Positivity obstruction from different directions. Each has made progress. None has closed the gap.

**Approach A — Weil's explicit formula and positivity of test functions:**

Weil (1952) showed that RH is equivalent to the positivity of a certain distribution: for every smooth compactly supported function $h$ on the idele class group,

$$\sum_{\rho} \hat{h}(\rho) \geq 0$$

where the sum is over non-trivial zeros. This is a spectral positivity condition. In GTCT language, it says: the contact structure has non-negative spectral content when tested against smooth observables. Known results (Odlyzko's numerical computations, conditional bounds on zero-free regions) give partial positivity for specific test functions, but not for all.

**Approach B — Connes' spectral realization:**

Connes (1999) proposed that the zeros of $\zeta$ are the "missing" eigenvalues of a Hamiltonian operator on $L^2(\mathbb{A}_{\mathbb{Q}}/\mathbb{Q}^\times)$. RH would follow if this operator were self-adjoint (Hermitian). Self-adjointness is the spectral-theoretic version of positive-definiteness. The operator has been partially constructed; its self-adjointness has not been proved.

**Approach C — Arithmetic Riemann–Roch (Connes–Consani):**

The most recent approach (Connes–Consani 2014–2024) builds a commutative geometric shadow of the adele class space over $\mathbb{F}_1$. The "square of the arithmetic site" is the object on which a Riemann–Roch theorem would need to hold. Frobenius correspondences play the role of the Weil pairing. The intersection theory required for the Riemann–Roch statement is partially developed but not complete.

**The GTCT contribution:** The contact-geometric reformulation provides a fourth language for the same obstruction — one that makes the geometric meaning of positivity (twisting energy is minimized on the critical line) visually and analytically transparent. Whether this language suggests a new proof strategy is an open question. It has not yet.

---

## §14.7 · The Honest Ledger

### What the Arc Has Built

Across Ch11–14, the Higher Dimensions Arc applied to the Riemann Hypothesis has built:

| Chapter | Contribution | Status |
|---------|-------------|--------|
| Ch11 | Arithmetic contact form $\alpha_{\text{arith}}$; non-integrability from $\mathbb{Q}$-linear independence of $\{\log p\}$ | ✓ Proved (within standard analysis) |
| Ch12 | Functional equation as candidate contactomorphism; critical line as unique contact-symmetric fixed locus (Theorem 12.2) | ✓ Proved (digamma calculation) |
| Ch13 | Adelic decomposition; local forms $\alpha_p$; corrected p-adic norm analysis; global assembly | ✓ Constructed (local pieces proved, global assembly correct) |
| Ch14 | Global Positivity Theorem (Conjecture 14.1); function-field key; three approaches surveyed | ✗ Open (= RH in geometric language) |

**The reformulation is complete.** The Riemann Hypothesis has a contact-geometric address. The proof requires one additional input — the Global Positivity Theorem — that is beyond the current reach of any approach, including this one.

**The Lean 4 ledger:**

```lean
-- AXLE: Honest sorry count for the RH arc
-- Issue #42: g_arith definition (connects to Mathlib VonMangoldt)
-- Issue #34: Non-integrability (Baker's theorem in Lean)
-- Issue #43: Critical line = contact symmetry locus (digamma)
-- Issue #44: Local p-adic coefficient definition
-- Issue #33: Global Positivity Theorem — THIS IS RH ITSELF

-- Issues #42–#44: Closeable with existing Mathlib (~200 lines total)
-- Issue #33: Open. Not closeable without proving RH.
-- This is the correct status. There is no sorry-free path to RH
-- that does not pass through the same mathematical wall.
```

---

## §14.8 · What This Arc Is

### The Reformulation as Research

The Higher Dimensions Arc applied to RH (Ch11–14) is a **reformulation paper** embedded in a textbook. Its value is:

**What it offers:**
- A new geometric language for RH that is precise, computable, and connected to existing frameworks (Connes, Weil).
- The explicit contact form $\alpha_{\text{arith}}$ with its von Mangoldt coefficient, computed to the level of a specific 1-form.
- The identification of the functional equation as a contact symmetry, with the critical line as its unique fixed locus (Theorem 12.2 — this is new and correct).
- The corrected p-adic analysis (§13.4 — the previous literature error fixed).
- A precise statement of the missing step as Conjecture 14.1.

**What it does not offer:**
- A proof of RH.
- A shortcut around the Global Positivity obstruction.
- A new theorem not derivable from standard complex analysis and p-adic geometry.

**Where to go next:**

A researcher who finds this arc interesting should look at:
1. Whether Theorem 12.2 (critical line = contact symmetry locus) has appeared in the literature. It appears to be original in this form.
2. Whether the contact-geometric language for the Global Positivity suggests a new test-function construction in the Weil explicit formula.
3. Whether the finite adelic approximation (§13.8 — 7 places up to the 13th prime) gives a computationally accessible approximation to the full adelic contact structure.

---

## §14.9 · The Dimension Ladder — Complete Arc

### Where the Book Now Stands

The Higher Dimensions Arc is now:

| Ch | Dimension | Object | Smooth/Arithmetic |
|----|-----------|--------|-------------------|
| 1 | 1D | Fermion seed $\psi^2 = 0$ | Smooth |
| 2 | 2D+t | Extended phase space, helix | Smooth |
| 3 | 3D | Contact 3-manifold, dm³ ODE | Smooth |
| 4 | 4D | Tesseract, symplectisation | Smooth |
| 5 | 5D | Jet space $J^1$, OPERA SATOR | Smooth |
| 6 | 5D+t | 6D magic square, GTCT | Smooth |
| 7 | Cross | Crystalline return, D₆, Monster | Mixed |
| 8 | Cross | Axiomatic turn, Gödel, Lean 4 | Formal |
| 9 | Cross | φ, Fibonacci, subcritical approach | Didactic |
| 10 | 3D | Helical attractors (formal paper) | Smooth (formal) |
| **11** | **2D+t** | **Arithmetic seed, $\alpha_{\text{arith}}$** | **Arithmetic** |
| **12** | **3D** | **Critical contact, functional equation** | **Arithmetic** |
| **13** | **∞D** | **Adelic tesseract, $\mathbb{A}_{\mathbb{Q}}$** | **Arithmetic** |
| **14** | **Open** | **Positivity rung, RH** | **Open** |

The book has climbed the smooth ladder (Ch1–10) and then — from Ch11 — repeated the same ascent in the arithmetic register. The two ladders are parallel: each smooth chapter has an arithmetic twin. The arithmetic arc ends at an open rung that the smooth arc never encountered, because the smooth system (dm³ ODE) is solvable and the arithmetic system (Riemann zeta) is not — yet.

---

## §14.10 · Bridge

### What Comes After

Chapter 14 is not the end of the book — it is the end of the arithmetic arc within the Higher Dimensions wing. The arc demonstrated that the GTCT contact-geometric ladder can be climbed in the arithmetic setting up to the point where the problem becomes RH itself.

What follows in the book's arc (toward Ch15 and beyond, currently in planning):

**Ch15 — The Spectral Return:** The connection between the arithmetic contact structure and Connes' spectral triple. Can the Reeb vector field of $\alpha_{\text{arith}}$ be related to the Dirac operator of the spectral triple? This would unify the two approaches at the level of operators — the GTCT C-K-F-U chain and the spectral A-H-D triple.

**Ch16 — The Function Field:** A complete chapter developing the function-field analogue of the arithmetic arc. This is the case where everything works — the Weil pairing provides the positivity, the Riemann–Roch theorem provides the formula, and the Riemann Hypothesis is provably true. Writing it out in full contact-geometric language would both validate the framework and show precisely where the number-field case breaks down.

**Ch17 — The Transmission:** The educational arc closes. What does it mean to teach the Riemann Hypothesis — not as a fact about zeros, but as a living problem whose structure is visible in contact geometry, reachable by anyone who has climbed the dimension ladder from Ch1?

The book is not complete. It was never designed to be complete. It is designed to end at the open door — and hand the reader the tools to go further.

---

## §14.11 · Final Tasks

**Task 1 — Summarize:** In four sentences, describe what the four chapters (11–14) have built, in the order C→K→F→U: Ch11 is C (the first contact with the arithmetic structure). Ch12 is K (the conjugate move — the functional equation symmetry). Ch13 is F (the fixed-point construction — assembling the global form). Ch14 is U (the unification attempt — and the honest statement of what remains). Write four sentences, one per operator, one per chapter.

**Task 2 — Identify the key:** Weil's proof of RH over function fields used the Weil pairing — a positive-definite Hermitian form on the Jacobian of the curve. In two sentences, describe what the arithmetic analogue of the Weil pairing would need to be — what object, on what space, satisfying what properties — for the proof strategy to transfer from function fields to the number field case.

**Task 3 — Open question:** Theorem 12.2 shows that the arithmetic contact form is exactly invariant under the functional equation reflection only on the critical line. Has this specific result — the critical line as the contact-symmetry fixed locus of $\alpha_{\text{arith}}$ — appeared in the contact geometry or number theory literature? (Genuine open question — if you find a prior reference, the author of this book wants to know.)

**Task 4 — The D1 question:** The arc ends at an open conjecture. The Fibonacci sequence never reaches $\phi$ — it approaches it forever. At what point is an approach to a theorem as valuable as the theorem itself? Write one sentence. There is no correct answer. There is a correct way of holding the tension.

---

*→ Chapter 15 · The Spectral Return (in preparation)*  
*← Chapter 13 · The Adelic Tesseract — Local-to-Global*

---

*Principia Orthogona · Vol IV · G6 LLC · Newark NJ · 2026*  
*Pablo Nogueira Grossi · ORCID: 0009-0000-6496-2186*  
*MSC 2020: 11M26 · 53D10 · 11R56 · CC BY-NC-ND 4.0 (text) · MIT (code)*
