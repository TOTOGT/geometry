# Control Ledger — verification-claim audit (geometry corpus)

**Draft, uncommitted. No chapter was edited to produce this. For sign-off before any repair.**

Purpose: the prose is strong but the *control* layer is weak — claims of "verified in
AXLE / 0 sorry / machine-verified" pointing at Lean files that may not exist, or that
carry `sorry`. This ledger separates confirmed false claims from things that only *look*
false because of an incomplete scan.

## Method + the honesty caveat

- Scanned **all mounted repos** for real `.lean` files (175 non-mathlib), excluding
  `.lake/` and `.git/`: AXLE, io-clone, geometry, **GTCT, grossi-ops, cajueiro**.
- **First pass overstated.** An initial scan of only AXLE+io+geometry flagged ~85
  "phantom" files. Adding `Desktop/GTCT/` and `Desktop/grossi-ops/` resolved most of
  them — the GTCT operator files (`Chain.lean`, `Compress.lean`, `Threshold.lean`, …)
  are real, just in a repo the first scan missed. **This is logged here deliberately:
  absence-from-scan is not proof of absence.** A `.lean` still on this list could live
  in an unmounted repo.
- Excluded from counts: escaping fragments (`_invariant.lean`, `_updated.lean` = pieces
  of `MOF\_topology\_invariant.lean`, `Chain\_updated.lean`) and generic/example names
  (`b.lean`, `box.lean`, `item.lean`, `axiom.lean`, …).
- A file *existing* is necessary but **not sufficient** for "0 sorry" — that still needs
  a `#print axioms` / sorry check per the repo's own rule. This ledger reaches the
  file-existence layer only.

---

## Tier A — CONFIRMED false verification (phantom file + explicit "verified" claim)

These assert Lean verification for a `.lean` that exists in **no** mounted repo.

| Claim location | Cited file | Claim text | Status |
|---|---|---|---|
| `book7/ch-kitagawa.html:194` | `MOF_topology_invariant.lean` | "Verified in AXLE: … 0 sorry in core" | **FALSE — file absent.** Novel claim, no plausible home. Topological designability is real reticular chemistry, not a Lean theorem — restate as [MODEL]. |
| `book8/ch1-darkmatter.html:641, :1207` | `DarkMatter_MachineVerified.lean` | "Formally verified in …" / "machine-verified in Lean 4" | **FALSE — file absent.** Needs opening; restate honestly or produce the file. |

## Tier B — File-backed verification claims (exist; still need a sorry/axioms check)

Not false at the file level. Do **not** relabel as verified until `#print axioms` is clean.

| Claim location | Cited file | Note |
|---|---|---|
| `book7/ch-curie.html:383`, `chcurie.html`, `ch-curie.html` | `Chain_updated.lean` | Exists (1 copy). Confirm 0 sorry before trusting "0 sorry in core". |
| `gomc-opus.html:305`, `book4/gomc-opus.html` | `AutophagyDm3.lean` | Exists. **But** the μ_max ≈ −0.41 s⁻¹ physiological anchor was already withdrawn (WP-30) — the "Lean 4 full / proved" wording overstates what's physical. |
| `hub.html`, `series-hub.html`, `book4/hub.html`, multilingual strings | `Chain.lean` | Exists in `Desktop/GTCT/…/Operators/`. Corpus already tracks the naming in `book6/policy/SITE_ERRATA.md` (`Chain.lean` → `Chain_updated.lean`). |

## Tier C — Cited `.lean` absent from every mounted repo (TRIAGE, not yet "false")

~50 files cited somewhere in the books but found in no mounted repo. **Each needs
opening before any verdict** — a match here can mean (i) unmounted repo, (ii) renamed
file, (iii) a *non-verification* mention (roadmap / "planned" / conceptual), or (iv) a
genuinely false verified-claim. Known sub-cases:

- `CatGT_PROOFS_COMPLETE.lean` — **known-removed** per io `CLAUDE.md`; citations from
  `research-status.html` are stale references, not live proofs.
- `Analemma.lean`, `BernoulliLemniscate.lean`, `GeronoLemniscate.lean`, `LunarAnalemma.lean`,
  `ArithmeticContact.lean`, `AdelicContact.lean`, `CriticalLineContactomorphism.lean`,
  `ContactHomology.lean`, `ContactNormalForm.lean`, `Convolution.lean`, `Coupling.lean`,
  `Gronwall_Closure.lean`, `HeatEquation_Step1.lean`, `HelixToyModel.lean`,
  `HexabonacciOmega.lean`, `PentanacciSigma.lean`, `TetranacciDelta.lean`,
  `TribonacciEta.lean`, `Lyapunov.lean`, `ChaosMu.lean`, `CatastropheF.lean`,
  `DisasterTheory.lean`, `Prevention.lean`, `MarketThreshold.lean`, `G6Threshold.lean`,
  `Monster.lean`, `MonsterLaw.lean`, `Jackknife.lean`, `Plimpton322.lean`,
  `Saturn_Chladni.lean`, `T5_Collatz.lean`, `CajueiroTheorems.lean`, `CatGT_D1.lean`,
  `CatGT_Tatiana.lean`, `CatGT_Thoreau.lean`, `AutophagyDm3_v3.lean`, `SpiralReturn.lean`,
  and the `book4/chpt11.md` `lean*.lean` set — **all pending per-file check.**
- `SeuArquivo.lean` ("YourFile"), `knacci_spine.lean` — likely templates/placeholders.

Priority within Tier C: any that appear in a **"verified / 0 sorry / machine-verified"**
context (like Tier A) are the real defects; the rest are stale-reference / roadmap
housekeeping.

---

## Part 2 — Cognate-glossary noise (separate, lighter sweep)

Bilingual pt/en glossaries "define" Latin/Greek cognates that are near-identical across
the two languages — pure noise: `limit`/`limite`, `topology`/`topologia`,
`operator`/`operador`, `function`/`função`, `energy`/`energia`, `molecule`/`molécula`,
`structure`/`estrutura`. Keep only entries that genuinely differ or need explaining
(`framework` → `estrutura básica`). Parallel-column *prose* is a legitimate format and
stays; only the vocabulary lists need trimming. **Not yet enumerated — flagged for the
same read-through pass.**

---

## What this ledger is NOT

- Not a count to quote. The Tier C number is mechanical; overstating it is the same error
  as overstating a proof.
- Not a set of edits. Nothing was changed. Tier A is the only high-confidence "false"
  set; everything else is "open the file first."
