# Missing instruments

*A scan of the corpus for gaps the acoustics work has just made visible, and what
it would take to fill each one. Opened 12 September 2026.*

The framing is Pablo's: the score exists, the orchestra does not have every part.
This register lists the parts that are missing, what each would let us play, and
whether it can be built with what is already in the repository or needs something
from outside. Items are ranked by that last column, because an instrument we can
build this week is worth more than one we can only describe.

---

## I. Built this week

### 1. The quality factor — **FILLED**

**The gap.** A search of every `.html` and `.md` in the series found the phrase
*quality factor* exactly once, in `book7/ch-nachbin.html`, written two days ago.
The corpus computes decay rates everywhere — eigenvalues, Lyapunov exponents,
monodromy exponents, Grönwall bounds — and has never once divided one by its own
period. That division is the whole of acoustics' relationship with time.

**What fell out when we did it.** `book7/dm3-q-factor-verify.py`:

- z_c = −1.839746254986 is **a pole, not a sign change**. Λ(z_c) = 0, so Q is
  infinite there. It is the only height in the flow where dm³ can sustain a mode.
- The underdamped band (Q > ½) has width **exactly ln 3**, with the model's only
  constant K = 1 − e^{−2π} cancelling out. Verified to 2.2 × 10⁻¹⁶.
- z_c is the exact midpoint of that band in e^{−z}, the coordinate the flow moves in.
- Outside the band, Q → ¼ and one turn costs a factor of 286,751. There is no
  oscillator there at all.
- Λ = 0 **is** the critical-coupling condition from resonator theory — internal
  loss equal to radiation loss — written in the other vocabulary.

**Status.** Done, verified, in `book7/ch-grothendieck.html` as an addendum.

---

## II. Buildable now, with what is in the repository

### 2. γ(f) — a frequency-resolved damping

**The gap.** dm³ has one γ. The medieval echea says damping is properly a
*function of frequency* and is set at the boundary, one mode at a time. There is
no spectral decomposition of the dm³ flow anywhere in the corpus — no place where
the transverse direction is resolved into modes each with its own decay rate.

**Why it matters.** The whole `§ 22.5` g-series taxonomy, the overshoot band, and
the multi-orbit variants are all *mode* language being spoken without modes. If
the linearisation about Γ were decomposed properly, "overshoot," "fold," and
"resistance" would each get a frequency and a width instead of a name.

**What it needs.** Floquet analysis of the transverse linearisation along the
helix. The period is T* = 2π and the monodromy is already known in closed form,
so this is a page of work, not a programme. The obstruction is that Γ is a helix,
not a closed orbit — the standard Floquet theorem does not directly apply, and
the right object is probably a monodromy **cocycle** over the z-translation.
That is an honest open technical question, not a blocker.

**Cost.** Days. Highest value-per-hour item on this list.

### 3. An admissibility test for the holonomy programme

**The gap.** `book6/holonomy-test.py` is validated and has been blocked on CIRA
data for a week. Nobody has asked whether the test is *admissible* before it is
run.

**Why it matters.** The acoustics gave us the precondition for free. Passive
Green's-function retrieval — the thing that retired the "you cannot clap at a
hurricane" objection — needs a **diffuse field**, which means modal overlap
M ≫ 1. In the Hypogeum, M < 0.05 at 63 Hz across every plausible volume, so the
method fails there no matter how good the sensors are. The same number can be
estimated for a tropical-cyclone environment from scale heights and decorrelation
times that are already tabulated in the literature.

**What it needs.** One script computing M for the storm environment from published
figures, with an explicit pass/fail. If M ≪ 1, the passive-retrieval argument in
`ch-nachbin.html` does not transfer and we should say so ourselves before someone
else does.

**Cost.** A day, and it does not need the CIRA files. **Do this before the data
arrives, not after.**

### 4. The symmetry-image count in multi-orbit theory

**The gap.** Multi-orbit theory (`docs/multiorbit-pacific-2026-09.md`,
`book8/ch12-container.html`, `chPrev-prevention.html`) has no group-theoretic
prediction about where companion orbits appear.

**Why it matters.** Gallot, Catheline & Roux's 1 / 3 / 7 enhancement points are
**2^d − 1** — the mirror group ℤ₂^d less the identity. Chaotic dynamics does not
break the count; only asymmetry does. That is a hard, cheap prediction about
configurations, and the Pacific trio was tested for *nesting* when it could have
been tested for *symmetry images*.

**What it needs.** State the count as a conjecture with its d-dependence, and
re-read the Lowell/Karina/Marie geometry against it. The trio failed the
band-width test structurally; it has not been asked this question.

**Cost.** Hours. Low risk: the result is a clean falsification either way.

---

## III. Needs something from outside

### 5. Anything measured

Unchanged and still the binding constraint. The four CIRA files (SHIPS EP/AL
5-day, EBTRK EP/AL new format) are still not downloaded; page 5 of the SHIPS
format PDF is still unread, and a size predictor there would remove the EBTRK
join entirely. Every acoustic figure used this week is somebody else's
measurement, correctly attributed and not ours.

### 6. The Oracle Chamber's dimensions

A tape measure would settle two things at once: the Weyl mode count (we can only
sweep volume from 10 to 250 m³ at present), and whether the niche sits on a
mirror plane — which under 2^d − 1 would make it the place the sound *arrives*
rather than the place it is made. No source found in this session gives the
volume.

---

### 7. The rival / non-rival boundary on the framework's generality

**The gap.** The corpus claims the operator sequence governs structural transitions
"across seventeen orders of magnitude." Every system it has actually computed is
**dissipative**: one turn of the dm³ helix costs a factor of 286,751; the Hypogeum
gives back fourteen seconds and then silence; Q settles at ¼. Loops lose.

**What broke it.** A teaching relationship, traced this week, runs the other way —
both parties end with more than they started with. That is the exponent changing
sign, and it is not a poetic reading: it happens because knowledge is **non-rival**.
Telling someone does not deplete the teller. The conservation constraint that makes
every mechanical cycle lossy simply does not bind.

**This is not new, and that is the useful part.** Two established results already
own this ground, both in economics:

- **Arrow's information paradox** (Kenneth Arrow, *Economic Welfare and the
  Allocation of Resources for Invention*, 1962): information cannot be valued by a
  buyer without being disclosed, and once disclosed the buyer already has it. The
  market failure is the formal shadow of "a gift that is earned."
- **Romer's non-rivalry result** (Paul Romer 1990; Nobel Memorial Prize 2018; see
  Jones, *Paul Romer: Ideas, Nonrivalry, and Endogenous Growth*, Scand. J. Econ.
  2019): doubling rival inputs alone gives constant returns, F(A, λX) = λY, but
  doubling objects *and* ideas gives **increasing** returns, F(λA, λX) > λY. That
  inequality is the sign flip, stated rigorously, thirty-six years ago.

**What it costs this corpus.** A boundary the generality claim has never
acknowledged. Rival systems are lossy; non-rival ones can have growing modes. The
operator sequence cannot be assumed to cross that line unchanged, and no chapter
currently says where the line is. Either the framework has something to say about
non-rival dynamics that Romer does not, or its scope is narrower than advertised
and should be stated so.

**Cost.** Reading, not computing. The relevant literature is thirty-five years old
and was written for economists, which is the degree this author already holds.

---

## IV. Housekeeping that is now overdue

- Five untracked `.lean` files at the repository root: `ReactionDiffusionFold.lean`,
  `TurnaroundUniverse.lean`, `ZetaScratch.lean`, `probe_book8.lean`, `probe_dm3.lean`.
  Track them or move them to a scratch directory; they have sat untracked for days.
- `MultiOrbitTogt.lean`: the `Norm_num` → `NormNum` import fix, then
  `lake env lean` from the geometry repo.
- v4 pre-deposit checklist item 15: the `rfl`/`decide` vacuous theorems, and
  `g6_equals_schumann` still present in 18 files including two lakefile roots.
- `omega-point-v2-draft.html`: abandoned orphan flagged by `duplicates.py`,
  awaiting a decision on `_to_delete/`.

---

## What the register says as a whole

Items 1 through 4 are all the same instrument seen from four sides: **the corpus
has rates and no resonances.** It can say how fast something decays and has never
asked whether it rings. Adding Q turned an existing sign change into a pole and
produced an exact ln 3 with no new assumptions — which is the cheapest real
result this series has had in a while, and it was sitting inside arithmetic that
was already written down.

The uncomfortable reading is in item 3. The same acoustics that supplied the
quality factor also supplied a precondition our own holonomy programme has not
been checked against, and the check does not need the data we have been waiting
for. It should be run first, and it might well close the programme.
