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

### 2. γ(f) — a frequency-resolved damping — **CLOSED 2026-09-17: NOT AVAILABLE**

**Answered by `book7/dm3-transverse-modes-verify.py`, six blocks, exit 0.** The open
technical question below — whether the right object is a monodromy cocycle over the
z-translation — is settled: it is, and it is explicit.

The Jacobian on Γ is `[[−2 + 2e^{−z}, 0], [2, 0]]`, checked against the true field at nine
heights. Both z-derivatives vanish **identically**, because every `e^{−z}` term in the field
carries a factor `(r − 1)`. So the system is lower-triangular, the transverse equation is
autonomous, and the one-turn monodromy is

    M(z₀) = [[m(z₀), 0], [2 I(z₀), 1]],   m(z₀) = exp(−4π + 2K e^{−z₀}),  K = 1 − e^{−2π}

agreeing with RK4 to better than 1e-9 at six base points. Its exponent **is** the `E(z)` of
item 1 above — the q-factor logarithmic decrement and the transverse Floquet multiplier are
one object, and `m(z_c) = 1` at the same `z_c = ln(K/2π)` that item 1 reports as a pole.

**Why γ(f) does not exist here.** `eig M(z₀) = {m(z₀), 1}` by triangularity, and the 1 is
translation along the helix — the flow direction, not a mode. The transverse spectrum is a
single number for every base point. A frequency-resolved damping needs a family of modes to
attach frequencies to; a rank-one transverse direction cannot supply one, under any Floquet
set-up. **Not a technical obstruction — a structural one.**

**Consequence for the vocabulary.** "Overshoot", "fold" and "resistance" are *not* modes of
the transverse linearisation with a frequency and a width each. Whatever separates them is in
the nonlinear terms or in the z-dependence of the single multiplier. Pages using them as modes
are speaking loosely and should say so.

**The cocycle, and what it costs to ignore it.** `m_n(z₀) = Π_{j<n} m(z₀ + 2πj)`, matched to
RK4 for n = 1..4 at three base points. `m(z₀)^n` — the closed-orbit answer — is wrong by a
factor of order 1 or more, e.g. at z₀ = −1, n = 4: cocycle 3.40e−20 against 3.95e−13.
**e^{−4π} is the z → +∞ limit of this cocycle and the multiplier of no orbit**; the ratio is
exactly `exp(2K e^{−z₀})`, which is 2.5e6 at z₀ = −2 and exp(2K) = 7.3615 at z₀ = 0. This is
`ch-conley`'s conclusion reached from the other side, now in closed form.

**Still open, and a different question:** a genuine spectrum could exist for a different
object — a PDE or lattice version of the flow with many degrees of freedom, or the
linearisation about a different invariant set. None of that is examined. What is closed is
γ(f) *for the transverse linearisation about Γ*.

<details><summary>Original statement of the gap, 12 September</summary>

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

</details>

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

### 4. The symmetry-image count in multi-orbit theory — **CLOSED 2026-09-17**

**Answered by `book8/multiorbit-symmetry-verify.py`, five blocks, exit 0.**

**The conjecture is much stronger than "expect three companions."** ℤ₂^d acting by d
orthogonal reflections sends a generic point to an orbit of 2^d points that are *not* in
general position: for d = 2 they are **the four corners of a rectangle** centred on the
mirrors' intersection. Verified on 400 random mirror pairs and random points, every corner a
right angle to 1e-9. So the count carries a geometric constraint that three observed systems
can be tested against **without locating the mirrors**:

> Three points are three corners of some rectangle **iff** one of their triangle's angles is
> exactly 90°. If one is, the fourth corner is *predicted*.

Test validated on three fixtures before use — exact rectangle reads 90.000000 and predicts
(3, 2); equilateral reads 60.000000; collinear reads 0.0. All three fire.

**Verdict on the Pacific trio: falsified as a symmetry-image set, for every d.** Positions
reconstructed from the prose bearings in `multiorbit-pacific-2026-09.md` (Lowell 600 mi S of
Kauaʻi, Karina 955 mi E of Hilo, Marie 550 mi WSW of Cabo San Lucas). Triangle angles
**10.0° / 161.1° / 8.9°** — the closest to a right angle is 71° away. Monte Carlo over the
reconstruction (landmark ±0.15°, distance ±8%, bearing ±11°): median 161.4°, 5–95% band
[137.3°, 178.0°], and **0 of 20,000 draws** within 5° of a right angle.

**Why it dies for every d, not just d = 2.** The trio is collinear to **1.4%** — the
separations are 2,143 km, 2,391 km and 4,473 km, so the triangle inequality is tight to 61 km.
d = 1 gives an orbit of 2 points, so three systems cannot be one orbit at all; d = 2 needs a
right angle; d ≥ 3 contains rectangles as 2-faces, and three collinear points share no 2-face
of a box. This quantifies what the register already said in words — the storms are *strung*,
not nested.

**What this does NOT falsify: the conjecture itself.** A claim about where companions appear
*when a mirror symmetry is present* is untouched by a configuration with no mirror symmetry —
and the register's own note records the Pacific environment as asymmetric (cooler water,
shear, higher latitude east). The conjecture's escape clause, "only asymmetry does" break the
count, is exactly what this configuration supplies. **The trio was never a test case, and the
test was cheap enough to establish that.** A symmetric environment with an identified source
would be one.

**Now settled on real tracks, not a reconstruction.** `book8/hurdat-symmetry-verify.py`,
five blocks, exit 0, against **NOAA HURDAT2 Atlantic 1851–2025** (7,071,568 bytes, 57,513
lines, retrieved 2026-09-17 from nhc.noaa.gov/data). Parses to 1,988 storms and 36,351 TS/HU
six-hourly positions over 30,544 synoptic epochs, zero unparseable coordinates.

| co-active storms | epochs | test | observed | climatological null |
|---|---|---|---|---|
| 3 | 588 | closest angle within 5° of 90° | **10.0%** | 11.1% |
| 4 | 72 | four-point rectangle within 5° | **0.0%** | 0.0% |

Observed/null ratio on the corner test is **0.91** — storms co-active at the same synoptic
hour are *very slightly further* from a right angle than positions drawn at random from the
same geography. On the direct d = 2 test, not one of the 72 four-storm epochs is a rectangle,
and the median worst-corner deviation is **80.7° observed against 72.0° for the null**, so real
quadruples are further from rectangles than random ones. Both tests fire correctly on exact
fixtures first.

**Verdict: the d = 2 symmetry-image prediction has no support in 175 years of Atlantic
tracks.** Same answer the prose trio gave, now with the reconstruction removed, a null
attached, and 660 configurations instead of one. The corpus should stop offering storm
groupings as evidence for a symmetry-image mechanism.

**Also added, and it is the cheaper guard:** `d ≤ k`, because ℤ₂^d needs d mutually orthogonal
mirrors and ℝ^k admits at most k. A cyclone field is a surface, k = 2, so the only counts
available to it are **1 and 3** — the seven-point case cannot apply to storms at all. Written
down because NOAA's 2002 report records September 2002 as the most active month on record with
**eight** named formations, and 8 = 2³ fits a source-plus-seven cardinality exactly. It is the
most attractive d = 3 candidate in the record and the geometry refutes it before any position
is looked up. A matching headcount is not evidence.

<details><summary>Original statement of the gap, 12 September</summary>

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

</details>

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

**Where to test it: geology and linguistics.** These are the two poles of the
boundary, which is why they are the right pair. Geology is maximally *rival* and
maximally dissipative — erosion, deposition, subduction, every process one-way and
every gram of rock in one place at a time. Linguistics is maximally *non-rival* —
a sound change spreads through a population without depleting anyone who already
has it, and a language can be given away entire without being lost.

If the operator sequence holds unchanged in both, the generality claim survives its
hardest test. If it needs different terms at each pole, the register has found the
line it was looking for.

The two fields also share a method, which is the reason the comparison can be made
at all: both reconstruct unobservable past states from present residue by regular
correspondence — stratigraphic correlation on one side, the comparative method and
regular sound laws on the other. Neither can rerun its experiment. Both are the
same epistemic situation as the archaeoacoustics chapters, and as this corpus.

*To check before writing, not to assert:* the nineteenth-century historical sciences
are widely said to have borrowed method from one another (Lyell's uniformitarianism,
Schleicher's family trees, the Neogrammarians' exceptionless sound laws). The
direction and strength of that borrowing is a real historiographical question and
this register does not currently know the answer.

**The better test is not the poles. It is tourism and music.** A pole only tells
you what happens far from the line. Two fields carry the boundary *inside*
themselves, and those are where its position can actually be measured.

*Tourism* is the congestible case. A view, a shoreline, a plaza is non-rival at low
density — one more person looking costs nobody anything — and becomes rival above a
threshold, where each additional visitor subtracts from every other. The field has
a standing name for that threshold, **carrying capacity**, and a standing economics
for goods of this shape (club and congestible goods, after Buchanan 1965). That is
a fold with the rival/non-rival transition as its own control parameter: one smooth
description up to a threshold, branches after it. No other field on this list has
the boundary as its central object.

*Music* splits instead of folding. The composition is non-rival — a tune given away
is not lost, and every performance since Josquin has confirmed it. The performance
is rival — one room, one night, finite seats, and the reverberation is a property of
that room and no other. Content non-rival, carrier rival, cleanly separable. Which
is the same split as the echea: the tuning is non-rival and anyone may build another
pot, while the pot itself is one object in one wall. It is also the split between a
score and a Q.

So the programme is: **geology and linguistics to bracket the claim, tourism and
music to locate the line.** Tourism because the threshold is the subject; music
because the two kinds of good come apart cleanly enough to be studied separately.

*Noted for the record:* the author holds a Bacharelado em Turismo from
UnB / UPIS (2003) — the qualification that has looked least relevant on every
application he has made, and the one whose literature owns this concept.

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
