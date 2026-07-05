# RH Arc (ch11–15) — Math & Link Audit

Style untouched per your direction — the dark theme correctly separates the arc.
Severity legend: ■ structural (must fix) · ▲ incorrect statement (fix wording/formula) · ● typo/link.

---

## ■ M1. The central kernel claim of Ch 11 is false as stated (propagates to 12–14)

**Where:** Ch 11 §11.5 (Definition 11.1), §11.2, hero equation; inherited by ch12–14.

**Claim as written:** with ζ(σ+it) = U + iV, the lifted curve γ(t) = (U,V,t) satisfies
∂ₜV = g(σ,t)·∂ₜU "from the Cauchy–Riemann equations," hence γ ∈ ker(α) for
α = dV − g dU, with g = Σ Λ(n) n^(−σ) sin(t log n). The Honest Inventory marks this "✓ Proved."

**Why it's false:** ∂ₜζ = iζ′(s), so (∂ₜU, ∂ₜV) = (−Im ζ′, Re ζ′). The claimed relation
forces Re ζ′ = −g·Im ζ′, i.e. the slope of the trajectory would be −Im(ζ′/ζ) — but the slope
is Re ζ′/(−Im ζ′), governed by arg ζ′, not by ζ′/ζ. Check numerically at any point: it fails.

**Repair A (recommended — keeps the von Mangoldt series, makes everything exact):**
work in log-zeta coordinates. Define U + iV = log ζ(σ+it) and the **pair** of prime series

- c(σ,t) = Σ Λ(n) n^(−σ) cos(t log n)
- g(σ,t) = Σ Λ(n) n^(−σ) sin(t log n)   (so −ζ′/ζ = c − ig)

Then (∂ₜU, ∂ₜV) = (−g, −c), and the form that **exactly** annihilates the velocity is

> **α_arith = c(σ,t) dU − g(σ,t) dV**

α(γ̇) = c(−g) − g(−c) = 0 — a one-line identity, honestly "✓ Proved."

Knock-on edits if you adopt Repair A:
1. §11.4 "piercing events": in log coordinates a zero is not a crossing of the axis but a plunge
   U → −∞ (log|ζ| → −∞). Rewrite as: *zeros are the points where the lift escapes to U = −∞;
   RH says all escapes happen over σ = ½.* (Or keep the (Re ζ, Im ζ) picture for Fig 11.1 — the
   figure is fine — and introduce log coordinates only when the form is defined.)
2. §11.6 non-integrability: dα = ∂ₜc dt∧dU − ∂ₜg dt∧dV, and
   α ∧ dα = −W(t) dU∧dt∧dV with the **Wronskian** W = c·∂ₜg − g·∂ₜc.
   Non-vanishing on a dense set still follows from the prime-frequency argument (see M2) —
   the statement survives, the formula changes.
3. Ch 12/13/14 references to "α = dV − g dU" → "α = c dU − g dV"; ch13's decomposition becomes
   the pair (c_p, g_p) per prime — additivity still exact since −ζ′/ζ = Σ_p (local factors).
4. Ch 11 Lean stub: `g_arith` comment "Im(−ζ′/ζ)" — note Im(−ζ′/ζ) = **−g** with your g
   (sign), and add `c_arith`. AXLE Issue #18 should build the pair.

## ■ M2. "Provable from Baker's theorem" — wrong tool, и the right tool is elementary

**Where:** Ch 11 Proposition 11.1 + Lean Issue #19 ("Baker–Wüstholz, ~80 lines").

ℚ-linear independence of {log p} is **unique factorization** (if Σ aᵢ log pᵢ = 0 with aᵢ ∈ ℚ,
clear denominators and exponentiate — contradiction). Baker's theorem is about *quantitative
lower bounds* for linear forms in logs of algebraic numbers; you don't need it. Density of sign
changes of the (absolutely convergent, σ>1) almost-periodic sum follows from Kronecker–Weyl
equidistribution + Bohr almost-periodicity.

Fix: cite "unique factorization + Kronecker–Weyl" instead of Baker(-Wüstholz). Good news for
AXLE Issue #19: it drops from transcendence machinery to an elementary argument.

## ▲ M3. Sign of g vs. −ζ′/ζ

**Where:** Ch 11 §11.5 ("g is the imaginary part of this"), Ch 13 §13.3.

With g = Σ Λ n^(−σ) sin(t log n): Im(−ζ′/ζ) = **−g**, and the local computation gives
Im(log p · p^(−s)/(1−p^(−s))) = **−** (log p · p^(−σ) sin(t log p))/D. Either flip the sign in the
two prose claims or define g with a minus. (Repair A's convention −ζ′/ζ = c − ig settles it.)

## ▲ M4. g_p formula inconsistency in Ch 13

The header box says g_p = p^(−σ) sin(t log p)/(1 − p^(−2σ)) — missing the **log p** factor and
the wrong denominator. §13.3 has the right denominator D = 1 − 2p^(−σ)cos(t log p) + p^(−2σ).
Make the box match §13.3 (with the M3 sign).

## ▲ M5. Series only converges for σ > 1 — say how g extends

**Where:** Ch 11 §11.7, Ch 12 §12.4 use g at σ = ½. The Dirichlet series for g (and c) diverges
for σ ≤ 1. One sentence fixes it: *for σ ≤ 1, define c, g via the meromorphic continuation of
ζ′/ζ; the series representation is valid for σ > 1.* The "g diverges at a zero" conclusion in
§11.7 survives (simple pole of ζ′/ζ) — both c and g blow up there.

## ▲ M6. Ch 14's Global Positivity statement is not well-formed

**Where:** Ch 14 header box: "∫_{ker α} Ω > 0 for all s …" — one cannot integrate a 3-form Ω
over a 2-plane field, and the quantifier "for all s" floats outside the integral.

Well-formed version (standard contact positivity):

> **dα_arith restricted to ker α_arith is positive-definite as a 2-form on the plane field for
> all 0 < σ < 1, σ ≠ ½, and degenerates exactly on σ = ½.**

This is the centerpiece equation of the arc — it must be flawless. Same fix in §14.5 table and
in the proof-ladder figure caption. (With Repair A: positivity of W = c∂ₜg − g∂ₜc off the
critical line, degeneracy on it — a concrete, checkable function.)

## ▲ M7. Attribution: pair correlation is Montgomery, not Bombieri–Hejhal

**Where:** Ch 14 §14.2. Pair correlation of zeros = **Montgomery (1973)**; GUE numerics =
Odlyzko (1987). Bombieri–Hejhal (1995) is on zeros of linear combinations of L-functions.
Replace the bullet: "Montgomery (1973), Odlyzko (1987): pair correlation / GUE."

## ▲ M8. Weil explicit formula display is garbled

**Where:** Ch 14 §14.3 Direction 2. As printed, "Σ_ρ f(ρ) = −f(1) + f̂(0) − …" mixes f and f̂
and drops the archimedean term. Either label it "schematically" or print the standard form:
Σ_ρ h(γ_ρ) = h(i/2) + h(−i/2) − (1/2π)∫ h(r)·Re[Γ′/Γ(¼+ir/2)] dr + h(r)-normalization
− 2 Σ_p Σ_k (log p) p^(−k/2) ĥ(k log p), for even Schwartz h. Flawless > evocative here.

## ▲ M9. Function-field slip: the Euler product is NOT finite

**Where:** Ch 13 §13.6 and Ch 14 Direction 1. A curve over F_q has **infinitely many closed
points** (infinitely many monic irreducibles already for 𝔸¹). What's true: ζ of the curve is a
**rational function of q^(−s)** — finitely many zeros/poles. Fix both passages: "the zeta
function is rational in q^(−s) with finitely many zeros (even though the product runs over
infinitely many places); the positivity data is finite-dimensional via Riemann–Roch."

## ▲ M10. "p-adic norm of p^(−s)" is a category slip

**Where:** Ch 13 §13.4. c = p^(−s) is a **complex** number; |c|_p has no meaning unless you move
to a formal variable in ℂ_p. The ultrametric identity you state (|1−c|_p = 1 for |c|_p < 1) is
correct *in that formal setting* — say so explicitly: "treat c as a p-adic variable in the open
unit disk of ℂ_p," or recast archimedean: poles of the local factor at p^(−s) = 1, i.e.
σ = 0, t = 2πk/log p. Also: those are zeros of (1−p^(−s)) — don't call them "trivial zeros"
(collision with ζ's trivial zeros at −2, −4, …).

## ▲ M11. Ch 11 §11.2 repeats the old (wrong) Ch 2 certificate

"α = dy + x dx … the key was non-integrability α∧dα ≠ 0" — (i) on a 2-plane α∧dα ≡ 0
(it's a 3-form), and (ii) d(dy + x dx) = 0 anyway. The revamped Ch 2 uses the certificate
α̃ = x dx + y dy = ½d(r²) and reserves non-integrability for the 3-space prototype dy − y′dx.
Update §11.2 to quote the corrected Ch 2.

## ▲ M12. Ch 12 small items

- Table: "Inner basin r\* ≈ 0.80" → **0.776** (canonical value you fixed).
- "Hopf symmetry r ↦ 2−r": the dm³ flow is not equivariant under r ↦ 2−r; label the row
  "(structural analogy, not an equivariance)".
- §12.3 "unique fixed set of the Hopf symmetry r ↦ r (trivially)" — delete or rewrite; r ↦ r
  fixes everything.

## ▲ M13. Ch 15 Cayley–Dickson ladder

"sêdenions (perde divisão) → **E₈/excepcionais**" — E₈ is not in the Cayley–Dickson sequence
(next CD rung = trigintaduonions, 32-dim). Either continue the true sequence or say "the
exceptional families (E₈) enter by a different construction." Theorems 15.1/15.2 honestly
sorry-marked — good. (J = Ψ/λ with Ψ² = −λ²·id ⇒ J² = −id checks out.)

---

## Links & typos

| # | File | Issue | Fix |
|---|---|---|---|
| ●L1 | ch13 | footer ORCID **text** says 0009-0000-6496-**2196** (link correct) | text → 2186 |
| ●L2 | ch14 | footer ORCID **href** points to …**2196** (text correct) | href → 2186 |
| ●L3 | ch11 | top nav lists Ch 1–7, 10–14 — skips 8, 9 | add ch08/ch09 (new Harrison/Belleville) |
| ●L4 | ch14 | "Arc complete → Index"; no link onward to ch15 | decision below |
| ●L5 | index/hub | ch11–15 not listed anywhere — orphaned arc | add an "Arithmetic Arc · RH" section (ch11→14, dark-theme tier) |
| ●L6 | ch15 | prev = `../ch14-axle.html` (Book 3's AXLE chapter at geometry root) while book4/ch14.html = Positivity Rung | decision below |
| ●L7 | ch15 (uploaded) | differs from live ch15 by ~16 bytes | diff before overwriting |
| ●L8 | ch12 | uses α = dV − g dU from ch11 | inherits Repair A |

## Two decisions only you can make

1. **Where does ch15 live?** Its content (Ψ=[F,T], Cayley–Dickson, Vol VI hand-off) belongs to
   the GTCT/chIV lineage ("Cap 14 · AXLE" predecessor), but its filename collides with the RH
   arc's numbering (ch14 = Positivity Rung). Options: (a) rename to `chIV-15.html` and leave the
   RH arc ending at ch14 → Index; (b) keep `ch15.html` and re-point its prev to `ch14.html`,
   accepting that the "complex turn" follows the positivity chapter; (c) ch14 gains a forward
   link "→ Cap 15 · A Virada Complexa" as a cross-arc bridge. My recommendation: **(a)** — the
   numbering stays honest in both lineages.
2. **Repair A adoption.** It changes the flagship formula of the arc (α = c dU − g dV in
   log-zeta coordinates). It is the minimal change that makes "γ ∈ ker α — Proved" true. The
   alternative is to keep ζ-coordinates with a position-dependent form (α = Re ζ′ dU + Im ζ′ dV),
   which is also exact but loses the clean prime-series coefficients. I recommend Repair A.

Once you decide both, I can generate the corrected ch11–ch14 HTML (text edits only — dark theme
and figures untouched) and patch ch15 locally.
