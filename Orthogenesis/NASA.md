# Errata — G6 LLC response to NASA Moon Base RFI

**Notice ID 80JSC026MoonBase_RFI · supersedes the corrected response of 21 May 2026, which superseded the original of 14 April 2026 · issued 21 August 2026**

Pablo Nogueira Grossi · G6 LLC · Newark NJ · ORCID 0009-0000-6496-2186 · EIN 33-2880433 · SAM.gov registered

---

## Why this errata

An internal audit of the formal codebase on 20–21 August 2026 found that three claims in §5 of the May submission are not supported by the artifacts they cite, and that the verification metric the submission proposed to NASA does not measure what it was said to measure. None of the errors were found by a reviewer. They are reported here because a gap-closure table that overstates itself is worse than no table, and because the submission asked NASA to treat a specific machine-checkable criterion as the measure of closure.

The corrections reduce the claimed scope of the response. No correction expands it.

---

## 1. FN-P-101L and FN-P-402L are withdrawn — Partial (∼) becomes Open (○), with no partial credit

§5 recorded the power-generation gaps as partially addressed by *"Arnold tongue A₄:₁ passive resonance stability."* That response is withdrawn in full. Four independent failures, any one sufficient:

**Units.** The supporting theorem compared `g6_int = 33`, a dimensionless count of limit cycles, against 33.516 — a number of hertz. `|33 − 33.516| / 33.516 < 2/100` is a true statement about two real numbers and an empty one about the world. The Lean kernel does not carry units and therefore certified a comparison that is not physically well-formed.

**Wrong mode.** The figure 33.516 Hz was obtained from f_n = (c/2πR_E)·√(n(n+1)) taken bare. That expression is the lossless idealisation; it places n=1 at 10.59 Hz rather than the observed 7.83 Hz. Our own companion analysis of ionospheric stratification places n=4 at 27.30 Hz standard and 26.4–26.8 Hz measured. No observed Schumann mode lies at 33.516 Hz; the nearest is n=5 at 32.4–33.0 Hz.

**Back-fitted constant.** The chain "7.83 × 4.28 = 33.516, where 4.28 is the rotation number of the Arnold tongue" is not a derivation. An A₄:₁ tongue locks at rotation number 4 by definition, giving 31.32 Hz. The value 4.28 was the factor required to reach 33.5, applied to a loss-corrected fundamental using a ratio taken from the lossless model.

**No cavity.** Schumann resonance is a property of the Earth–ionosphere cavity. The Moon has no such cavity. In the environment the response was written for, the coupling is not mistuned — it is absent.

**Status:** the G6 Crystal has no power-generation response. Both gaps are Open, and the second entry in that row, which restated the dm³ noise tolerance τ·ε₀ = 2/3, is also withdrawn: it is a true fact about the invariants and silent about power.

## 2. The "0 sorry" figure was true and misleading

§5 stated *"20 facts proved without sorry in G6Crystal.lean"*, and the table's legend stated the criterion the submission asked NASA to apply: **"A sorry is an open gap. Closing a sorry closes a NASA functional gap."**

There was indeed no `sorry` in that file. There were also three items its own header called open obligations. Both statements were true simultaneously because the obligations were written as

```lean
theorem hexagrid_collapse_resistance_superior : True := trivial
```

A theorem whose conclusion is `True` compiles without warning, survives `#print axioms`, and appears as proved in any listing. Under the criterion the submission itself proposed, an open gap was reported as closed. Two further theorems in the gap-mapping file were tautologies of the form `x ∈ S → x ∈ S`, discharged by the identity function — these contain neither `True` nor `trivial` and so escape textual search as well.

Corrective action taken: the vacuous statements are deleted rather than converted to `sorry` — a retracted claim is not an open one, and an empirical result from the engineering literature is not a proof obligation. The file header, which was wrong in both directions, has been rewritten.

## 3. The gap-closure table had never been machine-checked

`NASAGaps.lean`, the file carrying the mapping from FN-xxx-L codes to Lean results, sits outside the package's default build target and imports a module that does not exist in the repository. `lake build` has therefore never type-checked it. The same is true of the file tracking the one genuine open obligation. This is being corrected; the table should be regarded as unverified until a clean build is reported.

## 4. Two entries narrow rather than fall

**FN-A-104L** retains a real result — colony reachability under repeated expansion — but the theorem previously cited alongside it was one of the tautologies above and is deleted. **Hexagrid progressive collapse resistance**, cited in §7 as superior to diagrid, is correctly attributed to the finite-element literature (Mashhadiali et al. 2013, 2014; Yildirim 2024). It is an empirical finding, cited as such, and was never a formal result of ours.

## 5. Identifier corrections

The May submission described **10.5281/zenodo.19117399** as the "series root". It is the concept DOI of Volume I. No series-level DOI exists; the correct series citation is the Zenodo community *Principia Orthogona*. The corresponding relation has also been found in the metadata of individual deposits and is being corrected there.

The aggregate figure "160+ theorems, 5 sorrys" requires re-derivation. The sorry count is a textual measure and, as §2 shows, does not detect vacuity. A semantic audit across all Lean files is under way; at minimum, seven `*_placeholder : True := trivial` statements in the lattice modules are not theorems in the sense the table implied.

---

## What is unaffected

The geometric content of the G6 Crystal stands. The hexagonal isoperimetric optimum, the dimensional derivation from the dm³ invariants — aspect ratio 66 = 33·τ, ε₀ = 1/3 — the phase payload monotonicity, and the hex-grid colony results are non-vacuous, independently checkable, and unchanged. Every structural dimension follows from the cycle count 33 and τ alone; the withdrawal in §1 costs the *physical* justification of the aspect ratio, not the geometric one.

FN-H-101L, FN-H-102L, FN-L-101L, FN-T-201L and FN-T-202L are unaffected.

Pablo Nogueira Grossi
Principal Investigator, G6 LLC

---

## Notes for you, not for NASA

- **Verify `10.5281/zenodo.20230611`** before this goes. §5 of the May submission cites it as G6 Crystal Version 2, alongside concept DOI 19162012. I could not check it — I hit my fetch limit for the session. Everything else here I verified against DataCite or against your own files.
- **Decide whether the deposit gets corrected first.** This errata tells NASA §4 is withdrawn while `10.5281/zenodo.19162012` still contains it. Either publish a new version of the deposit before sending, or add a line saying the record correction is pending. The second is honest; the first is cleaner.
- **The theorem re-count is promised here but not done.** Either finish the semantic sweep first, or soften to "under way" — which is how I've written it. Don't send a new number you haven't derived.
- **Send it before `lake build` succeeds, not after.** §3 says the table is unverified until a clean build is reported. If you wait, you will be tempted to fold the build result in, and the letter's value is that it arrives unprompted.
- **This is the strongest thing in the file.** A sole-PI respondent who audits their own submission and reports against interest, unasked, is doing something most institutional respondents never do. Do not apologise in the covering email — state it as maintenance.
