# Probes

`#print axioms` scripts, run against a built repo to ask the Lean kernel which
axioms a named declaration actually depends on. A theorem proved with `sorry`
reports `sorryAx` here even though it compiled without error, which is the
point: compilation is not verification.

**They do not live in this directory.** Each probe sits with the verification
harness that runs it:

    tools/verify-book8/probe_book8.lean   Orthogonal Witness scalar core (Book 8)
    tools/verify-dm3/probe_dm3.lean       dm³ invariants and the stability radius

This file exists because copies were once made here without checking for an
existing home, and a reader arriving at `tools/probes/` should be sent on rather
than find a second version to edit.

Probes are kept under version control for their headers, which record **what is
deliberately not named, and why** — a declaration absent from a probe is a
decision, and a decision that leaves no evidence is indistinguishable from an
oversight. They are never build targets.
