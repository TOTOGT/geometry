# X = T × S: the Hodge-type inequality on the product-generated part, and the lemma it leaves open

Written 2026-11-11. Family test requested after the P²×P² benchmark. **Not a new theorem of the
general conjecture, and probably not new at all** (it is a short consequence of the Hodge index
theorem on each factor). Its value is that it separates what the geometry proves from the one
lemma that remains.

## Setting (all explicit)

T, S smooth projective surfaces over an algebraically closed field of any characteristic;
X = T × S, dim 4; h = H_T + H_S with H_T, H_S ample, H_T² > 0, H_S² > 0. Work in Chow or
numerical classes ⊗ ℚ.

**Product-generated codimension-2 classes** (the subspace A_prod): z = a·[pt_T] + ω + b·[pt_S],
with ω ∈ NS(T)_ℚ ⊗ NS(S)_ℚ. Degree: deg([pt_T]·[pt_S]) = 1, ⟨D⊗E, D'⊗E'⟩ = (D·D')(E·E'),
so deg(z²) = 2ab + ⟨ω, ω⟩.

**Input (a theorem, every characteristic): Hodge index on each surface.** NS(T) = ℚH_T ⊕ P_T and
NS(S) = ℚH_S ⊕ P_S, orthogonal, with the intersection form negative definite on P_T and P_S.

## Computation

Primitive means h·z = 0 in A³. Its components are, in NS(S) and NS(T) respectively:

    a·H_S + (H_T · ω) = 0        and        (ω · H_S) + b·H_T = 0.

Write ω = c H_T⊗H_S + H_T⊗e + d⊗H_S + ω′ with e ∈ P_S, d ∈ P_T, ω′ ∈ P_T⊗P_S. The first equation
forces e = 0 and a = −c H_T²; the second forces d = 0 and b = −c H_S². So

    primitive product-generated classes  =  ℚ·c  ⊕  (P_T ⊗ P_S),   dimension 1 + (ρ_T−1)(ρ_S−1),

    deg(z²) = 2ab + ⟨ω,ω⟩ = 3 c² H_T² H_S²  +  ⟨ω′, ω′⟩.

On P_T ⊗ P_S the form is a product of two negative definite forms, hence **positive definite**
(constructively: diagonalise each by rational Gram–Schmidt, then ⟨ω′,ω′⟩ = Σ λ_i μ_j ω′_ij² with
every λ_i, μ_j > 0). Hence deg(z²) > 0 for every nonzero primitive z in A_prod: the Hodge-type
inequality, codimension 2, holds on A_prod for every such polarization. For ρ_T = ρ_S = 1 this
is the value 3 s² t² of the P²×P² note.

**Proposition.** On the primitive part of A_prod ⊂ A²(T×S)_ℚ, with product polarization,
(−1)² deg(z²h⁰) = deg(z²) is positive definite. Proof: the computation above, given the Hodge
index theorem on T and S.

## What was checked, and how (constructively)

`verify_surfaces.py`, exact rational arithmetic, generic non-orthogonal rational bases:
dimension of the primitive space 1 + (ρ_T−1)(ρ_S−1) for (ρ_T,ρ_S) = (1,1), (3,3), (2,4); and for each,
an explicit certificate Gram = L·D·Lᵀ with L unit lower triangular over ℚ and every entry of D
positive. That certificate is the positivity proof: a sum of squares with positive rational
weights, no eigenvalues and no choice. Two negative controls pass: if P_S is positive definite
(Hodge index violated) positivity fails; and without primitivity the form takes both signs.
5/5 checks PASS. The script checks arithmetic on chosen Gram matrices; the general case is the
hand proof above.

## The precise unresolved lemma

A²(T×S)_ℚ is not known to equal A_prod. What lies outside it:

1. **Exotic classes in the H²(T)⊗H²(S) Künneth summand** that are algebraic but not in
   NS(T)⊗NS(S): graphs and correspondences between the surfaces' transcendental parts
   (when T and S share motivic pieces).
2. **Classes in H¹(T)⊗H³(S) and H³(T)⊗H¹(S)**: homomorphisms between Albanese-type abelian
   varieties of T and S.

> **Open lemma (positive characteristic).** The intersection form (−1)²deg(z²) is positive on the
> primitive algebraic classes in these summands, equivalently: positive on the orthogonal
> complement of A_prod inside the primitive part of A²(T×S).

Status of that lemma, as far as read: in characteristic 0 it follows from Hodge theory
(Hodge–Riemann). For part 2, the abelian-variety pieces fall under the Milne report
2611.00244 (Theorem 3.5, read at source, proofs not audited), but whether that covers the
Albanese-type pieces of arbitrary surfaces was **not checked**. Part 1 has no reduction known to me.
Nothing here proves it.

## Not claimed

No new case of the Hodge standard conjecture is claimed: the Proposition covers a subspace
that the Hodge index theorem already controls, and the exotic classes are exactly the hard ones.
It does not touch algebraicity of the inverse Lefschetz operators (conjecture B), a separate
obligation. The Lean file P2xP2.lean covers only the ρ = 1 case.

## Constructive note

The Lean files in this directory use Mathlib; their axiom reports show propext, Classical.choice,
Quot.sound, which come from the library's tactics, not from the mathematics. The certificate above
is the constructive content: rational data and a verification that is a finite computation.
A Lean version without classical axioms was not attempted.
