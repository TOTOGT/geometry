# Probes

`#print axioms` scripts, run against a built repo to ask the Lean kernel which
axioms a named declaration actually depends on. A theorem proved with `sorry`
reports `sorryAx` here even though it compiled without error, which is the
point: compilation is not verification.

These are not sources and must never become build targets. They are kept
under version control for their headers, which record **what is deliberately
not named, and why** — a declaration absent from a probe is a decision, and a
decision that leaves no evidence is indistinguishable from an oversight.

    probe_book8.lean   Orthogonal Witness scalar core (Book 8)
    probe_dm3.lean     dm3 invariants and the stability radius

Run from the repository root against a built tree, e.g.

    lake env lean tools/probes/probe_dm3.lean
