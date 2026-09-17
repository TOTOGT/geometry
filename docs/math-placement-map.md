# Math Placement Map

Where a piece of mathematics goes when it touches more than one volume.

Written 2026-09-17, triggered by the Ramanujan 1/pi work, which landed in four
volumes at once and had no rule telling it where to sit.

Checked by `tools/placement_check.py`, which verifies that every file named here
exists and reports every producing script in the corpus that this map has not
placed. Run it before trusting any row.

---

## 1 · The rule, read off existing practice

The corpus already places material consistently. The rule was never written
down, so here it is, inferred from what the volumes actually contain rather
than invented for this document:

> **A piece of mathematics goes where its ROLE is, not where its SUBJECT is.**

One object therefore appears in several volumes, once per role, and the volumes
cross-reference rather than duplicate. That is why the same 9801 belongs in
Vol VII (whose chapter it is), Vol IV (how to use it), Vol XI (why it is exact)
and Vol X (how it reached us) without any of those being a copy.

| Volume | Role it owns | Test for "does this belong here?" |
|---|---|---|
| **IV** — GTCT Dimensional Theory | **The object, worked.** Definitions, computations, the thing made usable. | Could a reader *do* something with this after reading it? |
| **VI** — Roots | **The finding.** A claim checked, bounded, or overturned. WP-numbered. | Does it change what the corpus believes? |
| **VII** — Scientist Gallery | **The person.** How a named mathematician met the object. | Is there a human whose encounter with it is the point? |
| **VIII** — The Monster | **The large sporadic structure.** | Does it live in or near the Monster / moonshine? |
| **IX** — Omega Point | **The stance.** Tagged `[FAITH]` / `[CONJECTURE]`. | Is it a bet rather than a result? |
| **X** — Custody, Transmission | **The custody.** How it travelled, who held it, what was lost in transit. | Is the *transmission* the subject? |
| **XI** — *(no core yet)* | **The algebraic floor.** Number fields, units, class groups, K-theory. | Does the claim rest on an arithmetic invariant? |
| **XIII** — Coherence | **The check.** What a verification establishes and what it does not. | Is the subject the instrument rather than the result? |
| **XV** — *(not opened)* | **Representation theory.** Witt, E8, W-algebras, critical level. | Is it a statement about a Lie-algebraic structure? |

**Corollary, and the reason this document exists:** a piece of math with only
one role is not yet understood. If a result fits in exactly one volume, either
it is narrow or nobody has asked the other four questions about it.

---

## 2 · The Ramanujan 1/pi material, placed

The trigger. Producing scripts: `book7/ch-ramanujan-verify.py` (80-digit) and
`book7/ch-ramanujan-1pi-verify.py` (120-digit).

| Object | IV · worked | VI · finding | VII · person | X · custody | XI · algebra | XIII · check |
|---|---|---|---|---|---|---|
| Singular moduli `alpha_n` | `book4/ch-modular-equations-and-pi.html` §1 | — | `ch-ramanujan` VI(a,b) | notebooks, unlabelled | CM theory | — |
| Watson's algorithm | — | — | `ch-ramanujan` VI(c) | notebook p. 320 | — | — |
| The 1/pi series | `book4/ch-modular-equations-and-pi.html` §2 | — | `ch-ramanujan` VI(d) | — | — | — |
| `9801 = 99^2` bridge | — | — | `ch-ramanujan` VI(d) | — | — | — |
| Pell, `eps^6 = 9801 + 1820 sqrt29` | `book4/ch-modular-equations-and-pi.html` §3 | — | `ch-ramanujan` VI(e) | — | **core candidate** | — |
| **The Euclidean algorithm** | `book4/ch-euclidean-algorithm.html` — worked 2026-09-17 | — | Euclid, *Elements* VII.1–2 | — | the route to `eps`: expansion → convergent at norm −1 → unit | Lamé exhibited, not proved |
| Reading a damaged source | — | — | `ch-ramanujan` VI(f) | `book10/ch05-the-notebooks-and-what-reached-us.html` §5 | — | `book13/ch10-what-a-check-establishes.html` Rule 2 |
| Heegner 163 | — | `book6/wp82-the-missing-floor.html` | `ch-ramanujan` VI(g) | — | class-number floor | — |
| `k_210` discrepancy | — | — | `ch-ramanujan` sorry-box | `book10/ch05-the-notebooks-and-what-reached-us.html` §4 — **open** | — | limits of arithmetic |
| Four instrument failures | — | — | `ch-ramanujan` sorry-box | — | — | `book13/ch10-what-a-check-establishes.html` Rule 3 |

Rows marked **to write** are placements this map asserts and the corpus has not
yet built. They are the map's own open items, and `placement_check.py` prints
them as `PLANNED` rather than letting them read as done.

---

## 3 · Shape for the volumes that do not exist yet

Vols XI, XII, XIV, XVI-XX have no directory. Two of them already have an
identity implied by statements elsewhere in the corpus; the rest do not, and
saying so is the point of this section.

### XI — the algebraic floor · **first compile 2026-09-17**
`book6/lean/VolXI_K0_Floor.lean` was compiled for the first time against the
vendored Mathlib at 81a5d257c8. It did not elaborate: seven errors, all
`unknownIdentifier`, all one cause — `GrothendieckGroup` is
`Algebra.GrothendieckGroup`. The API was read correctly and namespaced wrongly.
Fixed with one `open`; one declared `sorry` remains, so `#print axioms` still
reports `sorryAx` and XI does not yet clear WP-82's bar.

### XI — the algebraic floor · **identity already implied**
CLAUDE.md: *"Volume XI still has no machine-checked core."* Material already
sitting unplaced that belongs here:
- `book6/wp82-k0-floor-verify.py` — class numbers by reduced-form counting,
  Heegner list recovered, `K_0(O_K) = Z + Cl(K)`
- `book6/lean/VolXI_K0_Floor.lean` — **written, UNCOMPILED**, never run through
  `lake env lean`. This is the nearest thing XI has to a core and it has not
  cleared its own bar.
- The unit group and Pell work from `ch-ramanujan-1pi-verify.py`, which is the
  first place in the corpus where a Pell solution does load-bearing work.
- Mathlib has `GrothendieckGroup`, `ClassGroup`, `NumberField.ClassNumber` and
  no `K_0` — measured, not assumed.

**What would open it:** compile the Lean file. That is one command and it has
been open since it was written.

### XV — representation theory · **identity already implied**
CLAUDE.md: *"Volume XV is not opened. `ch-feigin` supplies the data, not the
theorem."* Material: `H^2(Witt) = 1`; the `-m` in `m^3 - m` forced and the 12
conventional; E8 with `h^vee = 30`, self-dual, critical level `k = -30`.
`ch-feigin` says plainly that no W-algebra is built.

**What would open it:** the theorem `ch-feigin` declines to assert.

### XII, XIV, XVI–XX — **no identity, and none should be invented**
Nothing in the corpus implies what these hold. Assigning them themes now would
be the same error as the near-integer in section 2: asserting structure that
has not been measured. They stay empty until material arrives that fits nowhere
else, and then the volume is named after the material rather than the reverse.

---

## 4 · Unplaced material — the queue this map generates

Producing scripts and results the corpus holds that this map has not yet
assigned a role-set. `placement_check.py` regenerates this list; the copy below
is prose for the ones that matter.

- **`book4/certify_rstar.py`** — exists in 7 locations, none citing the right
  DOI. Placement: IV (worked) + XIII (what seven divergent copies of one script
  say about verification). The DOI fix to `10.5281/zenodo.20360288` is still open.
- **`neuro/Spine/asd-load-transfer-verify.py`** — lives outside this repo.
  Placement: VI (finding: the per-interface denominator) + XIII (check: an
  endpoint that is a decision, not a measurement). Cross-referenced from
  `book6/wp124-three-segments-away.html`.
- **The Galperin billiard** (`book4/galperin-billiards*`) — placed in IV. Also
  has a VII role (Grant Sanderson's talk) and an X role (a result that reached
  the public through a video rather than a paper) that are unwritten.
- **`book7/ch-the-map-on-page-ten`** — CLAUDE.md records it as closing WP-124,
  but `book6/wp124-three-segments-away.html` also exists and is indexed.
  **Two things are called WP-124.** Unresolved; needs an owner's decision, not
  a script's.

---

## 5 · Known limits of this map

1. The rule in section 1 is **inferred from practice, not legislated**. If a
   volume's actual contents contradict its row, the row is wrong.
2. Volumes I, II, III, V are not characterised here. They predate the pattern
   and were not surveyed.
3. `placement_check.py` checks that named files *exist*. It cannot check that a
   file does the job the map claims. Nothing automates that.
4. The map has no opinion on ordering within a volume.
5. Sections 2 and 4 are current as of 2026-09-17 and go stale the moment a
   chapter is written. The script reports drift; it does not fix it.
