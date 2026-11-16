# EulerLean (drafts, 2026-11-16)

Independent Lean attempt at parts of Howe-Huffman-Kohlmeyer-Kruer, hexagon:2611.00370v1
(Euler's 1747 conjecture). NOT their formalization.

- `Euler1747.lean`: finite range (their Prop 7.2) via `native_decide`, plus a CONDITIONAL theorem:
  the conjecture follows from `AnalyticRange` (their Prop 6.1, a hypothesis here, not proved).
  `native_decide` trusts the compiler (`Lean.ofReduceBool`), so `#print axioms` for `euler_finite`
  is expected to list it. That is not a pure kernel check.
- `FourSquaresMixed.lean`: |Rmix| = (2/3)|R| for n = 2 mod 4 (their eq. 2.2). Expected to use only
  standard axioms. Does not prove Jacobi's four-square formula.

Status: neither file had been confirmed to compile when this folder was made. The
"Euler (Lean kernel check)" workflow (manual run) is what produces the evidence; a green run counts
only for the file it printed axioms for.
