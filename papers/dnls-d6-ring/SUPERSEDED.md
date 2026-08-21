# DNLS_D6_ring_draft.pdf — §7 IS KNOWN FALSE. DO NOT CIRCULATE.

Built 2026-08-21, superseded the same day.

Section 7 of that PDF states that the `SaturnHexagon.lean` header "was false
when written and stayed false for a month." **That is wrong**, and it was
wrong in the direction that accuses someone.

Running the preserved 20 July copy under `leanprover/lean4:v4.14.0` — the
toolchain the header actually named — on 2026-08-21 returned:

    gate_commutes_onsite     [propext, Classical.choice, Quot.sound]
    angCoupling_not_commute  [propext, Classical.choice, Quot.sound]
    rot_commutes_coupling    [propext, Classical.choice, Quot.sound]
    hex_rotation_invariant   [propext, Classical.choice, Quot.sound]
    hex_coupling_uniform     [propext, sorryAx, Classical.choice, Quot.sound]

Four of the five were genuinely proved in July. Two of them later decayed when
Mathlib stopped supplying `Fintype (Fin 6)` transitively through
`Mathlib.Data.Real.Basic`; nobody edited the file. Only `hex_coupling_uniform`
was never proved in that copy, and its `ring` existed in a sibling copy written
one minute earlier under a header reading `<pending>`.

The verdict in the PDF was reached by searching one directory — chosen because
the header named it — and treating absence of evidence as evidence. It was
corrected because the author disputed it, not because any check caught it.

**Current account:** `book6/wp73-the-stamp-and-the-triple.html`.
**Specimens and timestamps:** `~/Desktop/DO NOT DELETE/MANIFEST.md`.
**Source generator:** `build_paper.py` in this directory — §7 must be rewritten
from the three-class account before the PDF is regenerated or cited.
