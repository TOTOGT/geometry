# TODO — commutator-lemma repair + open items

Opened 2026-07-18. Ordered **cheapest first**. Check items off in place; a future
session should trust this file plus `CLAUDE.md`'s "KNOWN DEFECT" ledger.

Cost key: **XS** = minutes · **S** = under an hour · **M** = a working session ·
**L** = multi-session / needs decisions.

---

## TIER 0 — Do these first. Not about the lemma; they are at risk right now.

- [ ] **XS · Revoke the exposed PAT.** github.com/settings/tokens → delete the
      token that was embedded in `~/geometry/.git/config`. The remote URL is
      already scrubbed (done 2026-07-18), but the token itself is still live
      until revoked. **User action — cannot be delegated.**

- [ ] **XS · Audit the home-directory repo.** `~` is a git repo pushing to
      `TOTOGT/3M` and tracks anything under it. Run:
      ```bash
      git -C ~ ls-files | wc -l
      git -C ~ ls-files | grep -iE '\.ssh/|\.aws/|\.env|id_rsa|credential|token|_history$'
      ```
      Anything returned by the second line = treat as exposed, rotate it.

- [ ] **XS · Commit and push today's io-clone work.** Currently UNCOMMITTED and
      would be lost:
      `zeolite_operator_order/ZeoliteCommutation.lean` (new, kernel-checked) ·
      `zeolite_operator_selectivity_v3.tex` + `.pdf` (new) ·
      `OPERATOR_ORDER_DERIVATIONS_AND_STATUS.md` (edited) · `CLAUDE.md` (edited).
      Do **not** commit the stray `.aux` / `.log` / `.out` files pdflatex left.

---

## TIER 1 — Cheapest real repair. Highest leverage.

- [ ] **S · Fix `book4/chIV-orthogonality.html` Lemma 5.3.** This is the
      **injection point**; the other carriers cite it. Fixing it first collapses
      most of Cluster 1.
      *Minimal edit only.* Steps 1–3 of its own proof already derive
      `KFψ = FKψ`; delete step 4's invented δ and restate the lemma with `F`
      carrying its coupling term. Do not rewrite the file.

- [ ] **S · Settle Cluster 3 (triage, 3 files).** Read each once, decide carrier
      or clean, then move it out of triage in the ledger:
      `AMonster/dm3_operators.lean` · `book6/ch03-explicit-Ai-matrices.html` ·
      `omega/ch-resonance.html`

- [ ] **S · Verify Cluster 2 (inheritors, 3 files).** These cite the *true*
      chain-level 5.3 and may need zero changes — confirm each does not silently
      rely on the gate/pointwise version:
      `ch19-enzyme-noncommutativity.html` (D3) ·
      `ch20-saf-noncommutativity.html` (D4) · `research-status.html`
      Priority within this: **ch20 first** — it chains D3's K,F into D2's K,F,
      and D2 (ch18) is a confirmed carrier.

---

## TIER 2 — The remaining carriers. Real work, one file at a time.

- [ ] **M · `ch18-zeolite-noncommutativity.html` (D2).** §18.2 Theorem 18.1
      states the δ formula outright and calls it *"the Mini-Beast's central
      commutator, applied across every domain so far in this book."* Repair =
      let `F` carry the zeolite's `J` hopping term. Conclusion (ZSM-5/MCM-22
      divergence) is expected to survive; the corrected version already exists in
      `TOTOGT/io` → `OPERATOR_ORDER_DERIVATIONS_AND_STATUS.md` — reuse it.

- [ ] **M · `ALGEBRAIC_PROOFS_D1_RIBOSWITCH.md` (D1).** Note this file *notices*
      the commutator vanishes ("This appears to vanish — but…") and argues past
      it; the correction should say so plainly. Repair = non-local base-pairing
      along the chain as the coupling term.

- [ ] **M · `ALGEBRAIC_PROOFS_CH7_CRYSTALLINE_RETURN.md` Ch7-T1 Step 5 (Saturn).**
      Repair = the `r⁶cos(6θ)` angular term already in the Hamiltonian is the
      coupling. D₆ / wavenumber-6 stability conclusion expected to survive intact.

- [ ] **S · Write the domain-general correction note, once.** A single short
      document stating and proving `gate_commutes` / `coupling_not_commute` /
      `gate_fold_not_commute` abstractly, which every affected record cites
      instead of re-deriving. Seed already exists:
      `TOTOGT/io` → `zeolite_operator_order/ZeoliteCommutation.lean`.

- [ ] **M · Sweep Cluster 4 (~70 files) to confirm.** Expected all clean — they
      use the vocabulary without the derivation. Do this **last**, and only to
      close the audit. Only after this can a real count be stated.

---

## TIER 3 — Author decisions. Do not action unilaterally.

- [ ] **L · Zenodo amendments.** Affected records include 10.5281/zenodo.21296707
      (zeolite — v3 drafted, ready) and 10.5281/zenodo.19162012 (G6 Crystal /
      Saturn). Amending a DOI is the author's call: draft, show, do not deposit.

- [ ] **L · Decide Book 3's framing.** The Mini-Beast presents the false lemma as
      its spine across D1–D4. It is eBook-only and an explicitly living document,
      so it can be revised without a print run — but the revision is editorial,
      not just technical, and needs the author's voice.

---

## TIER 4 — Unblocked but parked.

- [ ] **M · BRASA smoke paper ("Where does it blow?").** Blocked on framing, not
      effort. Resolved so far: dm³ covers planetary atmospheric systems (Saturn =
      the stable wavenumber-6 case at g⁶=33; the July 2026 smoke episode = the
      same chain far from stability). Still open: whether the paper claims where
      a transient plume sits relative to `ε₀ = 1/3` and `μ_max = −2`, or leaves
      that open. **Do not reuse the first draft** — it treated dm³ as decoration,
      had no peer-reviewed sources, and cited Wikipedia.
      Verified sources already gathered: JAMA (NYC asthma ED visits, 261 vs 182
      daily, PM2.5 100.9 vs 9 µg/m³), Nature 2025 (82,100 premature deaths;
      US +1.49 µg/m³), CDC MMWR.

- [ ] **S · Send Zila's and Felipe's DRIFTS protocols.** Drafted, in PT, at
      `~/Desktop/cajulina/`. Numbers in them are suggested starting points and say
      so; both need the author's review before going to the collaborators.

- [ ] **L · OPTIONAL — Lean toolchain v4.14.0 → v4.33.** Both Lean files are
      already 4.33-clean. Deliberate task; never do it while debugging something
      else.

---

## Ground rules for whoever picks this up

1. Read `CLAUDE.md` ("KNOWN DEFECT" + cluster ledger) before touching a file.
2. **Never wholesale-replace a working file.** Minimal edit to the specific lemma.
3. Nothing is "proved"/"verified" without green CI or a watched kernel check.
4. Do not write a count of affected records until Cluster 4 is swept.
5. Update the ledger in `CLAUDE.md` in the same session you settle a file.
6. `Theorem53NonCommutativity.lean` and Vol I §5.3 are **clean** — do not "fix"
   them. Different claim, similar number.
