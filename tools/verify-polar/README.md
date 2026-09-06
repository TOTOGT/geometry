# verify-polar — the polar-polygon gate

    bash tools/verify-polar/run.sh

Covers the three modules written for the hexagon/decagon question:

| module | declarations | what it is |
|---|---|---|
| `PolarTriadClosure.lean` | 9 | resonant-triad arithmetic on the pair (6, 10) |
| `PolarPolygonCommonRefinement.lean` | 7 | the negative result: sixfold **and** tenfold forces a constant |
| `ChladniPolygon.lean` | 4 | the nodal-set statements `AXLE/SBM/nodal-sets.html` displays |

**20 declarations.** The figure is `grep -c '^#print axioms' probe_polar.lean`,
and it is anchored on purpose: the unanchored form `verify-book8/run.sh` uses
also matches the probe's own docstring, so `N` there counts prose. Worth fixing
there; not fixed here, because changing another gate's `N` inside a commit about
this one is how a number moves without anyone noticing.

## Why the probe names every declaration by hand

So that the Tier-1 count in `AXLE/theorem-registry.html` cannot be typed. That
number is read out of the `axioms.txt` this run writes; a declaration that is not
named here does not appear in it, and therefore does not appear in Tier 1. Adding
a theorem to one of the three modules without adding its line here silently
leaves it out. That is the intended failure mode — under-report, never over-report.

## What GREEN does and does not mean

GREEN means: the three modules compile under the pinned toolchain, and every one
of the 20 declarations was kernel-checked with no `sorryAx`.

GREEN does not mean any of them says anything about Saturn. They are statements
about periodic functions on a finite ring, about reachability in ℕ, and about
zeros of `cos 6θ` and `cos 10θ`. The bridge from those to a planetary atmosphere
is not in this repository and is not claimed anywhere in it.
