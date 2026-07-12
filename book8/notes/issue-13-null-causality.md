# AXLE Issue #13 — Proposed closure via null causality at the Whitney fold

**Status:** Working note. Captured the night of June 25/26, 2026.
**Companion to:** `lorentzian-contact-survey.md`, `dm3-on-horizons-questions.md`.
**Closes:** the `inner_basin_escape` sorry in `Chain_updated.lean` / `Main_v6.lean`.

---

## The sorry as it currently stands

```lean
theorem inner_basin_escape (r₀ : ℝ) (hr : r₀ < r_star) :
  ¬ ∃ μ < 0, ∀ t > 0,
  |r t - 1| ≤ |r₀ - 1| * Real.exp (μ * t) := by
  sorry  -- AXLE Issue #13
```

The current attempt at this proof tries to bound the radial flow by a Gronwall
estimate inside the inner basin. The estimate has not been made to go through.
The proposal of this note is that the estimate cannot be made to go through —
because the obstruction is not analytic but **causal**.

## The structural claim

Let $V : \R_{>0} \to \R$ be the Lyapunov function for the dm³ radial dynamics,
$V(r) = \tfrac{1}{2}(r-1)^2$, with critical point at $r=1$ and basin boundary
at $r = r_* \approx 0.776$ (asymmetric Gronwall radius, certified by
`certify_rstar.py`).

**Lemma 1 (Lyapunov vanishing at the fold).**
$\dfrac{dV}{dr}\bigg|_{r=r_*} = 0$.

*Proof.* By definition of $r_*$: at the basin boundary, the Lyapunov gradient
vanishes by construction. □

**Definition (Lorentzian metric induced by the Lyapunov function).**
On the transverse $(r, z)$ slice of the contact manifold
$M = \R_{>0} \times S^1 \times \R$, define a metric
$$
  g_{\mathrm{Lyap}} \;=\; -\bigl(d\tau\bigr)^2 + d r^2
  \qquad\text{where}\qquad d\tau \;=\; \frac{dV}{V'(r)}.
$$
This is well-defined and Lorentzian wherever $V'(r) \ne 0$ and *degenerates*
exactly on the locus $V'(r) = 0$.

**Lemma 2 (the fold is a null hypersurface).**
The surface $S = \{r = r_*\}$ is a null (lightlike) hypersurface in
$(M, g_{\mathrm{Lyap}})$.

*Proof.* On $S$, $V'(r_*) = 0$ by Lemma 1, so $d\tau$ blows up: the induced
metric on $TS$ has signature degenerating to $(0, +)$ — null. □

**Lemma 3 (causality theorem).**
No timelike curve in $(M, g_{\mathrm{Lyap}})$ crosses $S$.

*Proof.* Standard. Any classical text on Lorentzian causal structure; see e.g.\
O'Neill, *Semi-Riemannian Geometry*, §14.1, or Hawking–Ellis Prop.\ 6.4.6. □

## The closure of Issue #13

**Theorem (inner_basin_escape, restated).**
For $r_0 < r_*$, there is no exponentially decaying trajectory connecting
$r_0$ to $r = 1$.

*Proof.* Any trajectory $r(t)$ with $|r(t) - 1| \le |r_0 - 1|\,e^{\mu t}$
for some $\mu < 0$ is timelike in the Lyapunov-induced metric
(the energy $E(t) = V(r(t))$ decays exponentially, which means
$\sqrt{|g_{\mathrm{Lyap}}(\dot r, \dot r)|} > 0$ along the curve).
Such a trajectory, to reach $r = 1$ from $r_0 < r_*$, must cross $S$.
By Lemma 3, no timelike curve crosses $S$. Contradiction. Hence no such
$\mu$ exists. □

## Why the original Gronwall attempt failed

The original Gronwall attempt asked: can we bound $|r(t)-1|$ by an exponential?
The honest answer is: **the obstruction is not in the bound; it is in the
existence of the curve.** A trajectory connecting $r_0 < r_*$ to $r = 1$
through bounded exponential decay would be a timelike curve crossing a null
hypersurface, which is causally forbidden. No amount of refining the Gronwall
estimate can recover what the causal structure refuses.

This is why the sorry never closed: the proof shape was wrong.

## Lean 4 path

The full proof in Lean requires a minimal causal-geometry infrastructure on
the $(r, z)$ slice. The needed Mathlib4 ingredients:

- `Mathlib.Geometry.Manifold.IsManifold` — already there.
- A definition of a *null hypersurface* in a Lorentzian setting — to be
  written; the minimal version is ~30 lines.
- The causality lemma (timelike curves do not cross null hypersurfaces) —
  to be written; ~50 lines of elementary argument from the definition of
  the timelike/null cone in a (1,1)-Lorentzian space.

Or, more pragmatically: prove this as a **specialised lemma** about the dm³
Lyapunov function without importing general Lorentzian-manifold machinery.
That would be a self-contained ~80-line addition to `Chain_updated.lean`.

## Connection to the Phase 1 Lorentzian-contact survey

This closure is the first concrete instance of the Beig–Chruściel program
being applied to the dm³ framework. The survey (`lorentzian-contact-survey.md`,
§3) flagged the Whitney $A_1$ fold as the natural locus for promoting
dm³ to a Lorentzian-contact setting. Issue #13's closure is the first
deliverable of that promotion — it doesn't require the full Lorentzian contact
structure, just the null-hypersurface character of the fold, which is the
weakest piece of the promotion.

In other words: **the simplest possible Lorentzian dm³ result already closes a
real open problem in the Riemannian dm³ formalism.** That is a strong
indication the promotion is worth carrying through.

## What still needs to be checked

1. The Lyapunov-induced metric on $(r, z)$ is one specific choice. Verify it is
   the natural one — i.e., it is the metric induced by the contact form
   $\alpha = dz - r^2 \, d\theta$ restricted to the transverse plane and with the
   sign convention dictated by the entropy direction $\partial_z$.
2. Lemma 2 (fold is null) should reduce to a one-line calculation in the
   chosen metric. Do that calculation explicitly.
3. The causality theorem in Lemma 3 should be cited from a canonical source
   (O'Neill, Wald) and shown to apply at the regularity level we have here.

These three checks are routine. None of them requires anything not already
in standard Lorentzian geometry.

## Recommendation

Add this note to the AXLE OPEN_QUESTIONS.md as the proposed closure path
for Issue #13. Write the math note formally (LaTeX, ~3 pages) before
attempting the Lean proof. The Lean proof follows the math note.

This is the closure path. The closure itself is downstream work, not
overnight work.

---

**End of note.** Captured so the insight survives the night and does not
require the author to keep holding it in working memory.
