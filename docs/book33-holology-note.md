# Book 33 planning note: can holology be a mathematical logic?

Status: planning note, 2026-10-01. Nothing here is a claim for publication. Author's decisions are marked OPEN.

## What the corpus already says

Book 8, Chapter 13 defines holology as the logic by which a whole is coherent as a whole, reaches it through topos theory (the subobject classifier as the "holological signature"), and calls the word a translation slot that "translates; it does not prove". Section 2 of that chapter names the missing piece: "a principle that selects among the universes topos theory is content to leave plural". Chapter 8.9 asks whether the whole of the dm³ structure is itself a well-defined object. Book 33 is rung 33 on the floor ladder, noncommutative geometry; `book33/Noncommutative.lean` is not written.

## Definition for a reader who does not use topology

If pieces are true locally and agree where they overlap, then they are true of the whole. A logic of this kind is a closure operation on the lattice of parts. Its standard name, for a closure operation that keeps finite intersections, is a nucleus; the logic of nuclei is known (lax logic, and the internal logic of sheaves). That part is not new, and the chapter does not claim it is.

## What the test shows (script: docs/book33-holology-test.py, passes)

Take a deterministic map on a set of states and four operators built from it: "always in S", "eventually always in S", "ever in S", and backward saturation (same as "ever"). Checked on random finite maps:

- None of them is a nucleus. "Ever" is extensive but does not keep intersections; "always" and "eventually always" keep intersections but are not extensive.
- "Always" is an interior operator (the box modality of the modal logic S4 over the dynamics). "Eventually always" keeps intersections and is idempotent but is neither inflationary nor deflationary.

On the radial toy (Volume I's drift in ρ = r − 1, return map of time 2π): any interval around Γ is forward invariant, every test point enters and stays in it, so "eventually always" sends every neighbourhood of Γ to the whole half-line r > 0, the basin. A set away from Γ goes to the empty set. So the operator that "sends a neighbourhood of the cycle to its basin" exists and is well behaved on the toy, but it is not a nucleus.

## What this means for the claim

- If holology is the internal logic of a topos, it is topos theory under a new name (as the chapter says).
- The dynamics gives a different structure: a modal logic on a space with a map. The literature I recall for this is dynamic topological logic (Artemov, Davoren and Nerode 1997; Kremer and Mints 2005). UNCHECKED: recalled from general knowledge, not read.
- The selection principle the chapter asks for would have to be a rule that picks one operator or topos from the dm³ chain. The test suggests "eventually always" as a candidate. OPEN: whether it extends beyond the radial toy, to the toy with the z coupling, where the basin has a fold.

## Checked against the books in Downloads (2026-10-01)

- Connes and Marcolli (705 pp., text layer searched): Tomita's theory of the modular automorphism group is there (section 4.1, p. 557; Theorem 4.206 and the "main result on the Tomita time evolution", with the appendix at section 9.3): a state on the algebra determines a time evolution. So "the state of the whole algebra fixes its own dynamics" is supported by the held text. The words quantum logic, orthomodular, projection lattice and topos do not occur in it, so the quantum-logic link is NOT supported by this book and stays unchecked.
- Da Costa's paraconsistent logic Cω, with Başkent's topological semantics (hal-01094786, 2014): models are Alexandroff topologies, equivalently preorders; negation is evaluated through the closure operator, so the boundary of a region matters; gluts (a statement and its negation both holding at a point) come from the negation-assignment function N, not from the topology alone. A deterministic map gives such a space: x precedes y when y is on the forward orbit of x. Under that preorder the interior operator is "always" and a closure-type operator is "ever", the same operators the test script tabulates. UNCHECKED: the direction conventions, and whether the dm³ toy gives a model in which the glut function has a natural choice. OPEN.
- Restall, "Paraconsistent Logics!" (1995): separates dialethic paraconsistency (some contradictions are true) from non-dialethic (contradictions are tolerated without being true). Which one holology would mean is a design choice for the author. OPEN.
- Da Costa and de Ronde, "The Paraconsistent Logic of Quantum Superpositions" (arXiv 1306.3121): argues for contradiction as part of the formal structure of superposition from the start; offered as a first step, not a closed scheme. Read the abstract and introduction only.
- Not read: the Kaku books, the Kardashev papers, Dyson 1960, Sagan, the K3 and T-duality papers. Their bearing on a logic of wholes is not established here.

## OPEN, author's call

Whether holology is presented as a new logic, a plain-language name for known ones, or a slot that translates between fields. The test favors the last two.
