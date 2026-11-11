# standard-conjectures/

Context: the closing paragraph of `omega/ch-in-the-air.html` says Grothendieck's
standard conjectures are an unwalked third route to the Weil conjectures. This
directory is the working area for taking that sentence seriously. It proves
nothing about the conjectures themselves.

## Status (2026-11-11)

| item | state |
|---|---|
| `StandardConjectures.lean` | Written, **never compiled**. No Lean on the machine that wrote it. Not a lakefile target, so it cannot break CI. By R22 it stays an out-of-tier draft until it elaborates clean at the v4.32.0 pin with an axiom report. |
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
- **Not verified, and not to be cited as fact:** note section 2 says Milne's Nov 2026 report (reached through hexagonmath.org/2611.00244v1, not arXiv or jmilne.org) states the Hodge standard conjecture for all abelian varieties as Theorem 3.5, and that Milne's author page and a Michigan seminar page record Oct-Nov 2026 updates. None of those pages could be opened from here, and a search found nothing under that arXiv number. What was found: Agugliaro, arXiv:2510.21562, proves the Hodge-type conjecture for powers of abelian threefolds and some families over finite fields, not for all abelian varieties. Status: reported, unverified.
- **One finding of the note that is right:** section 7, the s -> 1-s versus s -> 1-conj(s) distinction. Book 4 s12.8 conflated them; a dated correction box was added to `book4/ch12.html` on 2026-11-11.
