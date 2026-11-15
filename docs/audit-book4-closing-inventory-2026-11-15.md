# Book 4 audit — closing inventory (2026-11-15)

Audit records and proposed repairs only. No manuscript page, generator, Lean file or sealed readcheck artifact was edited by this audit. Remote `main` was reported at f249696f after the last push (publication only; CI and Lean kernel results for these commits are not confirmed here).

## 1. Coverage
Coverage sweep complete; listed verification gaps remain (see "Not audited" below and sections 4–5b).
Audited with a record in docs/audit-book4-ch11-14-ch18-ch19-2026-11-14.md: ch00 (staleness) and ch00-student-edition, 01, 02, 05, 06, 06b, 07, 08, 09b, 10-lambda-bone-handoff, 12, 15, 16, 21–28; earlier in this audit ch11, 13, 14, 17, 18, 19, 20. From the earlier external pass (docs/audit-ranking-2026-11-14.tsv, not re-audited here): ch03, ch04, ch09, ch10.
Not audited: ch09b's sites script and DEM/NOAA source checks (files not available here), ch10 sidebar and §6 beyond the recorded items; book5–book10 pages beyond the dependency grep (D1–D6).

## 2. Findings that change a mathematical statement (highest consequence first)
- ch22: Con(X) equals the graph of the Gauss map only for hypersurfaces. ch23: cusp/flex swap; π₂ not birational for defective X.
- ch24: Theorem 24.2 false as stated (disc_r f = 0 does not imply multiplier 1); r* "certificate" is not an enclosure.
- ch15: T is not the Reeb flow; Ψ as printed is first-order so Ψ² = −λ² id fails on constants; J² = −id impossible on the 3-manifold M; Re h = 4 vs stated gap 2; Theorem 15.4 contradicts 15.1.
- ch16 / ch10 / ch00: ε₀ = 1/3 is a chosen constant; "2/(2·2) = 1/3" is arithmetic error (= 1/2); H = 2 not established (audit-log entry on O7 records H = 6 as a candidate, unresolved).
- ch25: Carmichael count 3 of 8; Z(s) identity needs E ~ log T. ch26: Lean covers inequalities only; no axiom report in repo. ch27: ⟨log W⟩ formula is the log of the mean. ch28: Γ is a cylinder foliated by Legendrian helices; Reeb sign.
- ch02: α = dy − f(x,y)dx on (x,y,t) has α∧dα = 0 (not contact); oscillator form is a first integral. ch06: neither 6×6 array is magic (one-cell fix 34 → 31); Theorem 6.1 on a 6-manifold; three statements still say T1 proves a generative circuit.
- ch12: contactomorphism stated as fact in the central-claim box, open in the status table. ch14: Global Positivity is a conjecture; dependants: ch12 deferral, ch15 Thm 15.5, rh-paper Conj 6.1.
- wp56 §10: merger does not turn spacelike into timelike; draft replacement (Propositions 10.1, 10.3, Definition 10.2) in docs/proposed-patches/wp56-section10-replacement.md.

## 3. Findings about numbers, wording or provenance
r* "certified" wording (book7/wp58, book8/ch2, stjohns-meco/index, book6/wp69; ch10 already corrected); r* 0.7732 vs 0.7759 (ch28); Hill coefficient 3.64 vs 2π/√3 = 3.6276 (ch06b, ch07); ε₀ < r* compares a radius with a location (ch06b); corridor 2.6 MW does not recompute (2.90 MW from the site data, 3.06 MW from the prose mix; $2.8M consistent) (ch07); Schumann: fourth measured mode 26.3 Hz confirmed in Cole 1965 Table 1 (p. 1348), ideal n=4 33.4926 Hz, ch16 compares 33 with the ideal value (gap to measured 25.5%); ch05 torus claim, symmetry group, dm³ ≅ J¹ only onto {p>0}, z as independent variable; Sheffer prior art on light-cone readings; closed Reeb orbits contradiction across books (D4).

## 4. Proposed repairs (all unapplied; need Pablo's decision)
Manuscript wording: items in each chapter's "Proposed corrections" line in the audit record. Tools: docs/proposed-patches/proved_labels-identifier-match.patch, run_yourself-detect-imports.patch (apply with `patch -p1 < file`). Generated pages: `python3 tools/chapter_zero.py --write` then `--check` (ch00 stale in six books). Lean: LadderRung.lean (DRAFT, NOT COMPILED).

## 5. Unresolved checks
- Lean: LadderBound.lean and LadderRung.lean axiom reports (`lake env lean … | tee …; python3 tools/axiom_gate.py … N`); DualDerivations.lean, lean-toolchain, lake-manifest.json needed for the Jacobian CI fix; ZetaReflection counts checked by grep only; AXLE_v6.lean not rebuilt.
- Sources not read: Balser & Wagner 1960; Dyrda et al. 2015 (blocked); Sheffer full text (blocked); Sawala et al. 2025 (press only); Mathlib PR #43252; Zenodo 21708678; Larsen IMRN year; ch20 literature attributions; ch19 absolute-pitch factor 2.
- Open scripts: re-run ch11_14_wronskian_check.py on the Mac; ch16 Mars troposphere figure; ch07 source of 2.6 MW; which ch15 file is live (book4/ch15.html, book4/ch15-complex-turn.html, root copy differ).
- Uncommitted files of unknown origin left untouched: Orthogenesis/Architecture/G6Crystal.lean, TERMS.md, book4/certify_rstar*.py, readcheck tracked-file edits (eight files), other modified book4 pages.
- Readcheck publication status: sourcemap.tsv and chunk1-controls-expected.tsv are in remote history; sealed labels and blind returns are not; Pablo to decide whether any of this needs action.

## 5b. Added after the first version (2026-11-15)
- ch00-student-edition F0s-1..5 (the "every orbit with r(0)>1 converges" statement, flagged on the separate ch03/ch10 numerical evidence (largest converging r(0) ≈ 6.859 at z(0)=0), used as the model theorem; the r(0)=7.5 run is recorded as an observation only (four solvers stop with a step-size failure at t ≈ 0.178, endpoint solver-dependent), not as blow-up; Collatz asserted; stale chapter pointers; J¹(ℝ,ℝ²) as "5D contact"). ch09b: its own verifier passes (106 checks, 6 controls); the NOAA inputs remain unchecked. ch10-lambda-bone-handoff: the script runs successfully in this environment (75 PASS lines); that does not establish that it ran on Pablo's Mac or independently validate every proof.
- ch05 F5-5 reworded: ż ≠ 0 locally, not ż > 0; the Cartan distribution is rank 3 = codimension 2 on a 5-manifold (a contact distribution there has rank 4).
- ch00 regeneration trial: chapter_zero.py --write --book 4 fixes the hash but drops four downstream generated boxes; page left at its committed state. CI for 6aaee037 not readable here; LadderBound.lean and LadderRung.lean are not lean_lib targets, so no CI compile or axiom report covers them. Ladder files: kernel status unverified; adding explicit compilation and axiom reporting is a separate repair.

## 6. Method notes
Check scripts are read-only and live beside their chapters (ch06…ch28, wp56). Lines labelled NOTE in a script are hand arguments, not computed. A passing script does not establish a prose claim; where a script checks arithmetic only, the record says so.
