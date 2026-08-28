#!/usr/bin/env python3
"""declaration_scan_fixtures.py — specimens that prove the resolver fires.

CONVENTIONS.md §2. Each case is (index, name, expected_how). `how` is EXACT when
the name is declared verbatim, SHORT when only its final component matched and
Lean namespaces were not parsed, MISSING when nothing resolves.

The third case is the one that matters and it is drawn from real output:
`UnfoldOp.stable_branch` was cited in a Zenodo deposit as "Theorem D". It is a
structure field, so no theorem, lemma, def or axiom carries the name, and the
resolver must report MISSING rather than reaching for a near match.
"""

# index: name -> [(kind, repo, relpath, has_sorry)]
IDX = {
    'gronwall_radius': [('theorem', 'AXLE', 'AutophagyDm3.lean', False)],
    'GenerativeOp': [('def', 'AXLE', 'main_v7.lean', False)],
    'stable_branch_other': [('theorem', 'AXLE', 'Elsewhere.lean', False)],
    'admitted_thm': [('theorem', 'AXLE', 'Roadmap.lean', True)],
}

CASES = [
    (IDX, 'gronwall_radius', 'EXACT', 'a theorem declared verbatim'),
    (IDX, 'GenerativeOp', 'EXACT', 'resolves, but as a def — prose calling it a theorem is wrong'),
    (IDX, 'UnfoldOp.stable_branch', 'MISSING', 'a structure field is not a declaration'),
    (IDX, 'Ns.stable_branch_other', 'SHORT', 'final component matched; namespace unverified'),
    (IDX, 'admitted_thm', 'EXACT', 'resolves and carries sorry — reported, never dropped'),
]
