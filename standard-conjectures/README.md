# standard-conjectures/

Context: the closing paragraph of `omega/ch-in-the-air.html` says Grothendieck's
standard conjectures are an unwalked third route to the Weil conjectures. This
directory is the working area for taking that sentence seriously. It proves
nothing about the conjectures themselves.

## Status (2026-11-11)

| item | state |
|---|---|
| `StandardConjectures.lean` | Written, **never compiled**. No Lean on the machine that wrote it. Not a lakefile target, so it cannot break CI. By R22 it stays an out-of-tier draft until it elaborates clean at the v4.32.0 pin with an axiom report. |
| `P2xP2.lean` + `verify_lean_tables.py` | Written 2026-11-11; **compiled in CI run #3 (45cdb1f), no `sorry`, standard axioms only**. Formalizes (1) the Frobenius-only countermodel (FᵀJF = q⁴J, J indefinite), (2) the P²×P² primitive-space and pairing calculations for every s,t>0 in codimensions 0, 1, 2, (3) both compositions of the explicit L² inverse via a correspondence Γ. Non-default lib `P2xP2`; built only by the manual workflow `jacobian-lean.yml`. The sympy script checks the multiplication tables and the push-pull formula against polynomial reduction mod (a³,b³): 22/22 PASS. **Geometric inputs are assumed, not proved**: CH = ℚ[a,b]/(a³,b³), the monomials being a basis, and the pushforward formula for Γ. This proves arithmetic in a supplied ring; it does not touch the general conjectures. |
| `product_of_surfaces.md` + `verify_surfaces.py` | Family test, 2026-11-11: X = T×S, product polarization. Hodge-type positivity proved (by hand, from the Hodge index theorem on each surface) on the product-generated primitive codimension-2 classes, with an exact rational LDLᵀ certificate on test Gram matrices, 5/5 PASS. Names the **open lemma**: positivity on algebraic classes outside NS(T)⊗NS(S) (exotic H²⊗H² classes, H¹⊗H³ parts). Not new; no claim on the general conjecture. |
| `p3xp3.md` + `verify_p3xp3.py` | P³×P³, 2026-11-11: Hodge-type positivity for **all** primitive algebraic classes, every ample rational h = sa+tb, via dim P^r = 1 (exact), the s,t scaling automorphism, and V_r = 20, 4, 20/9, 4 > 0; Lefschetz-B from cellularity. 24/24 exact checks PASS. Classical case; not new; no general claim. Not in Lean (P2xP2.lean covers P²×P² only). |
| `ch-primitive.html` + `ch-primitive-verify.py` | Chapter "Primitive" (2026-11-11), standalone, no book number: what primitive means, the three worked cases, the failed Frobenius shortcut, the open lemma, a tag table. Verifier re-runs the three scripts and checks the page's numbers against them: 14/14 PASS. Linked from `book7/ch-grothendieck.html`, `book7/ch-weil.html`, `omega/ch-in-the-air.html`. Not enrolled in the generated "Across the series" roster (see audit log). |
| Mathlib names at risk | `Subspace.dual_finrank_eq`, `IsNilpotent.isUnit_one_add`, `LinearMap.injective_iff_surjective_of_finrank_eq_finrank`. The file imports all of `Mathlib` to avoid guessing module paths. |
| A copy is in `TOTOGT/jacobian` (commit 3a4ab43, local) | That repo's CI will be the first compile. If it goes green, copy the axiom report here and add a target (R22). |

## What the Lean file is

Three algebraic steps from Milne, *Grothendieck's standard conjecture of
Lefschetz type over finite fields*, arXiv:2011.06563, sections 4 and 6:

1. a nondegenerate pairing of finite-dimensional spaces forces equal dimension
   (Prop. 6.1: Conjecture D gives dim AH^i = dim AH^(d-i));
2. an injective map between such spaces is surjective (Prop. 6.1: D implies A);
3. if beta.alpha = 1 + n with n nilpotent, alpha has a left inverse (Prop. 6.6).

No Weil cohomology, no algebraic cycles, no motives. Mathlib has none of these.
R20 applies: read the hypotheses before citing any of the three as evidence for
anything geometric. They are the easy half of the argument.

## Where dm3 stands against the problem (from Book 4 s12.8, not new)

The standard conjectures ask for a **positivity statement on algebraic cycles**:
for a smooth projective X of dimension d with Lefschetz operator L, the form
`(x, y) -> <L^(d-2i) x . y>` is positive definite on primitive algebraic classes
(Hodge standard conjecture), and L^(d-2i) is algebraic-ly invertible
(Lefschetz standard conjecture, B). To use dm3 on this, the framework would
have to supply, at minimum:

1. a Q-valued Weil cohomology (or a fibre functor on numerical motives) built
   from contact data;
2. a notion of algebraic class and a Lefschetz operator on it;
3. an inequality, not an invariance.

Book 4 s12.8 already records the state of item 3: the contact form
alpha_arith gives invariance of the critical line under the functional-equation
involution, which is cheap, and does not give positivity, which is the whole
difficulty. Nothing written here changes that. Items 1 and 2 are not defined
anywhere in the corpus. So there is no dm3 route to the standard conjectures at
present, and a page saying otherwise would fail R10 and R18.

## What is reachable

Milne's finite-field target: Conjecture B over F-bar_p. It already follows from
the Tate conjecture there (his Prop. 4.1), and his Theorem 2 derives the Tate
conjecture and the Hodge standard conjecture for abelian varieties from it. Work
on that route is work on a stated, bounded problem. It is research, with no
promise of an outcome.

## Open

- compile and axiom-report `StandardConjectures.lean` (R22);
- decide whether the finite-field B route is worth a chapter, and if so
  pre-register what would count as progress (R30);
- the 2026 status sentence in `omega/ch-in-the-air.html` ("open in 2026") rests
  on one search that returned no accepted proof (R15: not a survey).

## Added 2026-11-11 (later): the other session's benchmark note

`Grothendieck_research_start.md` and `verify_p2xp2.py` were written by another AI session (not identified in the files) and are kept here unedited, as received.

- **Checked by Claude Sonnet 5.5:** the script reads cleanly and runs here (SymPy 1.14, exact arithmetic): 24 of 24 checks pass. An independent re-derivation matched it: h*p1 and h*p2 vanish; deg(p2^2) = 3 s^2 t^2; the L^2 matrix, its determinant 3 s^2 t^2 and its inverse; the correspondence action reproducing the inverse; the middle form of signature (2,1). The Frobenius control (F = q^2 I, J = diag(1,-1)) is trivially true and rules out only that shortcut.
- **What it is:** a known case. In P^2 x P^2 every class is algebraic, so the standard conjectures hold and the positivity is classical. It shows the machinery is right, and proves nothing new.
- **The Milne claim, now read at the source (2026-11-11, later):** the user supplied the PDF `2611.00244v1.pdf` (header `hexagon:2611.00244v1`, J. S. Milne, "On the Hodge, Tate, and standard conjectures for abelian varieties", dated 9 Nov 2026, expanded notes of a Michigan talk of 5 Nov). It exists and says what the note says, with the following scope. It is a *report*: Theorem 1.6 (rationality conjecture for all abelian varieties) and Theorem 2.1 (the Hodge conjecture for CM abelian varieties) are credited to two OpenAI preprints of 6 Oct 2026, with supporting papers by Madapusi (hexagon:2610.00226) and van Hoften-Sempliner (hexagon:2610.00259v2). Theorem 3.5, the Hodge-type standard conjecture for all abelian varieties, is credited to **Milne 2002**, which was conditional until the CM Hodge result; his table marks it with an asterisk (conditional until 2026). Also stated there: Lefschetz-type conjecture known for abelian varieties; Tate conjecture for all abelian varieties over finite fields (Milne 1999*); Hodge standard for abelian fourfolds by Ancona 2021; Hodge theory gives the Hodge-type conjecture in characteristic zero. Section 3.6 of the report omits the factor (-1)^r in the primitive pairing, as the note says. **Not audited:** the OpenAI, Madapusi and van Hoften-Sempliner proofs themselves. The PDF is not copied into this repo.
- **Correction to an earlier line of this README and to the Claude reply of the same day:** the host name hexagonmath.org was treated as a red flag, and "all abelian varieties" as overstated. Both were wrong: the document is real, and the claim is Milne's own report. What remains true: this is abelian varieties only; the general standard conjectures (arbitrary smooth projective varieties, and the Lefschetz-type conjecture over finite fields in general) are open. Agugliaro, arXiv:2510.21562 (powers of abelian threefolds etc.) is partial and now superseded in scope for the Hodge-type conjecture on abelian varieties, if Milne's report holds.
- **One finding of the note that is right:** section 7, the s -> 1-s versus s -> 1-conj(s) distinction. Book 4 s12.8 conflated them; a dated correction box was added to `book4/ch12.html` on 2026-11-11.
