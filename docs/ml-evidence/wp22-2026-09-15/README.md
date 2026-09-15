# wp22-2026-09-15 — the helix toy model before its four clarifications

`helix_toy_model.tex.pre-revision` is `book6/differential-equations/helix-toy-model/helix_toy_model.tex`
as it stood before the revision of 2026-09-15. It is kept because the corrections
that revision made are cited in three published pages, and a correction needs the
artefact it corrected.

What the pre-revision source said, and what changed:

1. It called Γ "a periodic orbit of period T\* = 2π (a helix in (r, θ, z), since
   θ̇ = ż = 1)" — the parenthesis contradicting the phrase. Since ż = 1 the flow has
   no periodic orbit at all; T\* is the period of the (r, θ) projection.
2. It used "degenerate Hopf" without naming which sense. It is Guckenheimer &
   Holmes' (a vanishing first Lyapunov coefficient), not Strogatz p. 256's
   (a nonlinear centre, no limit cycle on either side). Both books are in its own
   bibliography.
3. Theorem 5.1's 2×2 Jacobian is that of the frozen planar subsystem; the three-
   dimensional field has ż ≡ 1 and hence no zero. The caveat existed only in the
   exercises ("freeze z"; solution 4).
4. `\bibitem{Strogatz}` appeared once and `\cite{Strogatz}` zero times; the string
   `7.1.1` appeared zero times, in a paper whose radial data are Example 7.1.1.

No result was withdrawn in the revision. Four of the five figures the document
`\includegraphics` were absent from the source directory, so it could not be rebuilt
from its own sources; they were regenerated from `helix_toy_model.py` in the same
pass and are now versioned beside it.

Cited by: `book7/ch-strogatz.html` (and `ch-strogatz-verify.py` block [7], which read
this file's counts and now reads the repaired ones), `book6/wp120-how-many-closed-orbits.html`,
`book6/wp122-the-return-map-was-in-the-exercise.html`, and `docs/audit-log.md`.
