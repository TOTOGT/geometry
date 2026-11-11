# P³ × P³: Hodge-type positivity on ALL primitive algebraic classes

2026-11-11. A known classical case, done completely so the statement covers the whole primitive
space and not only a chosen generator. **Not a new theorem; says nothing about general varieties.**

## Setting and inputs

X = P³ × P³ over any field, d = 6, h = s·a + t·b, s,t > 0 rational (every ample rational class).

* (G1) CH*(X)_ℚ = ℚ[a,b]/(a⁴,b⁴), deg(a³b³) = 1 (projective bundle formula, Stacks 02TX).
* (G2) X is cellular: the cycle class map CH^r → H^{2r} is an isomorphism and odd cohomology
  vanishes. So **every** class in H*(X) is algebraic, and "algebraic classes modulo homological
  equivalence" is exactly ℚ[a,b]/(a⁴,b⁴). This is what makes "all primitive algebraic classes"
  honest here. Neither (G1) nor (G2) is proved by the scripts.

## Argument

1. **Primitive spaces.** P^r = ker(L^{7−2r}: A^r → A^{7−r}), r = 0,…,3. dim A^r = r+1.
   The exact computation gives dim P^r = 1 for r = 0,1,2,3 (matrix ranks 0,1,2,3 on 1,2,3,4 columns).
   So a generator spans the entire primitive space in each codimension.
2. **Reduction to s = t = 1.** The map a ↦ s·a, b ↦ t·b is a ring automorphism of ℚ[a,b]/(a⁴,b⁴)
   sending a+b to h and scaling deg(a³b³) by s³t³. It carries the primitive space for (1,1) onto
   that for (s,t), and gives (−1)^r deg(z_s² h^{6−2r}) = s³t³ · V_r, with V_r computed at s = t = 1.
   (Checked symbolically in s,t as a cross-check.)
3. **Values at s = t = 1**, generators p_r and V_r = (−1)^r deg(p_r² h^{6−2r}):

   | r | p_r | V_r |
   |---|-----|-----|
   | 0 | 1 | 20 |
   | 1 | a − b | 4 |
   | 2 | a² − (4/3)ab + b² | 20/9 |
   | 3 | (a − b)(a² + b²) | 4 |

   All positive. For z = c·p_r(s,t): (−1)^r deg(z² h^{6−2r}) = c² s³t³ V_r > 0 for c ≠ 0.

**Result.** For every ample rational h = s·a + t·b, every r ≤ 3, and every nonzero primitive
algebraic class z in A^r(P³×P³)_ℚ, (−1)^r deg(z² h^{6−2r}) > 0.

**Lefschetz type (B)** for this X: every ℚ-linear operator on H*(X) is induced by an algebraic
correspondence, because H*(X×X) is also entirely algebraic (X×X is cellular). The P²×P² note
exhibits the explicit cycle in one degree; here it is a consequence of (G2), not a new construction.

## Checked

`verify_p3xp3.py`: 24/24 exact checks PASS (dimensions, symbolic-ranks, V_r, scaling law, and primitivity of
z_s for symbolic s,t). Arithmetic only; (G1), (G2) and the reduction argument are on paper.

## Not claimed

Not a new result (Hodge–Riemann holds for P³×P³ in characteristic 0, and cellular varieties
satisfy both standard conjectures). Not an argument for any variety whose cycle space is not
fully known. The gap named in `product_of_surfaces.md` is untouched.
