# Novelty register

**What this is.** A priority ledger. The mathematics in this corpus is derived here, from
first principles, without reading the literature first. That is a working method, not a
citation practice, and it has one consequence: **priority runs on publication date, not on
route.** A result derived here in 2026 that someone published in 1928 is re-derived, however
it was arrived at. So the novelty claim rests entirely on a search — done before publishing,
looking *for* the prior art rather than for its absence.

**The rule this register exists to enforce.** *A failed search is a fact about the search.*
"Not found" is not "novel", and the word **novel** is not in the verdict vocabulary below.
`tools/novelty_check.py` fails if it appears in a verdict, if a row is missing its search
record, or if a verdict is outside the closed list.

**Two things that are not the same.** A citation here is a pointer for the reader — *"this is
classical, see X p. N"* — never an attribution of source. Where the derivation is printed on
the page, the row says so, and the derivation is what earns it: neither a referee nor a tool
can check a route, only printed work. `book6/wp58-galactic-fold.html` is the model — it
derives `r - r^3` from the flat-rotation-curve effective force rather than importing it as a
normal form, and keeps the derivation visible.

## Verdict vocabulary (closed)

| verdict | meaning |
|---|---|
| `KNOWN-EXACT` | the same mathematical result is already published |
| `KNOWN-GENERAL` | the general phenomenon or theorem is published; the exact formulation may differ |
| `PRIOR-ART-CANDIDATE` | a strongly related published result exists and needs equation-level comparison |
| `UNRESOLVED` | the search evidence is not sufficient to support or deny a priority claim |
| `UNMATCHED-LIMITED` | no match found, in a search that was narrow or named-corpus only |
| `UNMATCHED-BROAD` | no match found after a deliberately adversarial search |

`KNOWN-EXACT` → `KNOWN-GENERAL` → `PRIOR-ART-CANDIDATE` → `UNRESOLVED` →
`UNMATCHED-LIMITED` → `UNMATCHED-BROAD`. Never a binary found / not-found.

**A keyword-level similarity is not a prior-art match.** Two papers containing the phrase
"no-go theorem" in contact geometry are not prior art for each other. That failure mode is
the reason this file exists, and it has already been caught once here — see rows N06 and N08.

## Rows

| id | claim | stated in | verdict | searched (terms) | corpora | date | candidate hits | equation-level disposition |
|---|---|---|---|---|---|---|---|---|
| N01 | Γ = {r=1} attracting, T\* = 2π, transverse exponent −2 | WP-22 §2; ch-strogatz | `KNOWN-EXACT` | limit cycle, r(1−r²), θ̇=1 | Strogatz 2nd ed | 2026-09-15 | Example 7.1.1, p. 199 | identical system; standard well before 1994 |
| N02 | closed-form return map P(r) = [1+e^(−4π)(r⁻²−1)]^(−1/2) | WP-122 §1 | `KNOWN-EXACT` | Poincaré map, surface of section | Strogatz 2nd ed | 2026-09-15 | Example 8.7.1, p. 282 | identical formula, worked in the text |
| N03 | uniqueness of the closed orbit | WP-120 §3–4 | `KNOWN-EXACT` | uniqueness limit cycle, Dulac | Strogatz 2nd ed | 2026-09-16 | Liénard's Theorem p. 212; Example 7.4.1 p. 213 | same conclusion by a classical named theorem (Liénard 1928; Levinson–Smith 1942) |
| N04 | trapping annulus for the perturbed system | WP-120 §3; WP-122 §3 | `KNOWN-EXACT` | trapping region, Poincaré–Bendixson | Strogatz 2nd ed | 2026-09-15 | Example 7.3.1, p. 206 | same construction, same μ<1 threshold |
| N05 | μ = −2 survives the integrable e^(−z) modulation | WP-22 Thm 2.1 | `UNMATCHED-BROAD` | exponential modulation, invariant Lyapunov exponent, integrable modulation | Strogatz 2nd ed; web pass ×2 | 2026-09-16 | adjacent integrability literature only | no equation-level match located |
| N06 | base-point drift of the per-period exponent | ch-grothendieck; WP-122 §2 | `UNMATCHED-BROAD` | Floquet multiplier base point, monodromy base point | Strogatz; ChaosBook; web pass ×2 | 2026-09-16 | ChaosBook §5.3: multipliers **invariant** under base point (similarity); one 2022 source notes the monodromy *matrix* depends on base point | the adjacent literature runs the **other way**. A genuine periodic-orbit monodromy has base-point-invariant multipliers, so the drift is a diagnostic that the object is a time-2π flow map and not a monodromy — because ż = 1 and the flow has no periodic orbit. **The claim must be stated in multipliers/exponents, not in the matrix**, or it collides with a true and uninteresting statement |
| N07 | neutral line z = 0 and the exact time reversal across it | WP-22 Thm 3.1 | `UNMATCHED-BROAD` | neutral line, time-reversal symmetry, stability reversal locus | Strogatz 2nd ed; web pass ×2 | 2026-09-16 | both terms have large independent literatures | no combined construction located |
| N08 | contact-Hamiltonian obstruction: θ̇≡1 ⟹ ℋ = p + g(θ,z), locking identity, c→−2 ⟹ H→−∞ | WP-22 §7 | `PRIOR-ART-CANDIDATE` | contact Hamiltonian no-go, Lie–Hamilton obstruction, Jacobi–Nijenhuis | Strogatz; web pass ×2 | 2026-09-16 | de Lucas & Rivas, arXiv:2207.04038 (Jul 2022) / J. Phys. A 2023, **Prop. 3.8 published / 3.7 arXiv**: *"If (M,Λ,X) is a Lie–Hamilton system and D^X = TM, then M is even-dimensional"* · Colombo & López-Gordón, Anal. Math. Phys. 16:118 (2026), Remark 2.9, Jacobi–Nijenhuis integrability no-go | **neither states this theorem.** The first is a dimension obstruction on Poisson structures; the second is an integrability obstruction on dissipated quantities. Shared with WP-22: the phrase "no-go" and the setting. Both are the right neighbourhood and must be read line by line before any priority claim |
| N09 | closure-dependent finite-time escape | WP-22 §4 | `KNOWN-GENERAL` / `UNRESOLVED` | finite-time escape, blow-up, super-linear closure | web pass ×2 | 2026-09-16 | finite-time escape is standard background | escape itself is prior art and was never the claim. The unresolved part is the **dependence on closure** — that a cubic closure escapes below z₀\*(ε₀) and any bounded closure does not |
| N10 | second circular orbit r₂ = (−1+√(1+8e^(−z)))/2, transcritical collision with Γ at z = 0 | WP-120 §2 | `UNMATCHED-BROAD` | exact expression; second limit cycle; transcritical bifurcation of cycles | corpus (`git grep`); web pass ×2 | 2026-09-16 | expression occurs in unrelated contexts | formula occurrence is not prior art; no match for its role here |

## N08 — the span, computed 2026-09-16

Prop. 3.8's hypothesis is `D^X = TM`. It was never checked against this system. It is a
computation, not a search, and it comes out as follows.

Write the flow with the modulation as its own generator:

    X = X1 - X2 + X3 + X4,     X1 = f(r) d_r,   X2 = f(r) e^{-z} d_r,
                               X3 = d_theta,    X4 = d_z

The only non-vanishing bracket is `[X4, X2] = -X2` — `[X1,X2] = (f f' e^{-z} - f e^{-z} f') d_r
= 0` identically, `[X4,X1] = 0`, and nothing depends on θ — so **V = span{X1,X2,X3,X4} is a
4-dimensional solvable Lie algebra**, verified numerically for both canonical closures
(max |[X1,X2]| ≤ 2.7e-7, max |[X4,X2] + X2| ≤ 1.4e-8 over a grid).

X1 and X2 are both multiples of `d_r`, so `D^V = span{ f(r) d_r, d_theta, d_z }`:

| where | rank D^V | Prop. 3.8 |
|---|---|---|
| M \ {r = 1} | **3 = dim M** | hypothesis holds |
| the invariant cylinder r = 1 | 2 | hypothesis fails |

M is 3-dimensional, i.e. odd. **So off the cylinder r = 1, this Vessiot–Guldberg algebra
admits no Lie–Hamilton structure relative to any Poisson bivector.** Contact geometry is not
a stylistic choice for this system; for this decomposition it is forced. And the single locus
where the obstruction lapses is the invariant cylinder — the object the paper is about.

**Scope, stated because it is easy to overclaim here.** The system is autonomous, so the
minimal Vessiot–Guldberg algebra is ⟨X⟩ itself, of rank 1, and Prop. 3.8 is silent on that
one. What is obstructed is the decomposition above — the one that carries the `e^{-z}`
modulation as a separate generator, which is the decomposition with the content. Whether
*every* VG algebra of this system is obstructed is not settled here and is the open question
the computation leaves.

**What this does to the row.** It does not make Prop. 3.8 prior art for WP-22 §7 — the two
theorems remain different, one a parity-of-rank obstruction on Poisson bivectors, the other a
locking identity forcing H → −∞. It changes the *relation*: Prop. 3.8 sits **upstream of the
setting**, as part of the reason the setting is contact at all. The row stays
`PRIOR-ART-CANDIDATE`, and the equation-level comparison it calls for now has a first result.

**The proof of Prop. 3.8 does not rest on peer review, and need not.** Λ^♯ : T\*M → TM has
image the tangent space to a symplectic leaf; a symplectic leaf carries a nondegenerate skew
form and is therefore even-dimensional; if every field of the system is Λ-Hamiltonian it lies
in that image, and if those fields span TM then TM has even rank. Three sentences, checkable
without the journal. Published is not true — WP-90 reports three defects in a peer-reviewed
paper — so results are verified here, not cited on authority. This one verifies.

## Searches still owed on N08

Searching for the theorem has not worked and is not expected to. Search its **ingredients**,
separately and in combination:

1. the locking identity in its algebraic form, not its interpretation;
2. contact Hamiltonians carrying a cyclic coordinate whose velocity is fixed identically;
3. the obstruction between a transverse attractor and a positive constant expansion rate,
   phrased without the words "no-go".

## Not covered here

**Patents.** A literature pass is not a patent novelty search — different corpus, different
priority rules, different disclosure bar. HVEH and the SAF work are the IP-directed threads
and need their own search. No row in this file speaks to patentability.
