# Multi-orbit theory against the Pacific trio, 1–5 September 2026

An attempt, with the negative result first. Written 2026-09-12 against reported
NHC intensities; no atmospheric modelling was done here and none is claimed.

---

## What was actually there

Three systems in the eastern and central Pacific at once, at the season's peak.

| | position, 4 Sep | intensity, 4 Sep | what it did |
|---|---|---|---|
| **Lowell** | 600 mi S of Kauaʻi | Cat 3, 125 mph | formed 27 Aug · Cat 5 on 2 Sep · **down to Cat 3 by 4 Sep** · **back to Cat 5, 160 mph / 922 mbar, on 5 Sep** |
| **Karina** | 955 mi E of Hilo | Cat 1, 90 mph | gradual weakening forecast; post-tropical early the following week |
| **Marie** | 550 mi WSW of Baja | Cat 2, 100 mph | slow weakening from the Saturday |

Lowell's decline was attributed to increasing wind shear, dry air, and
**eyewall replacement cycles**; the re-intensification followed the completion of
one.

## 1. The negative result: the trio is not a nested system

The Minimum Orbit Theorem (`chPrev-prevention.html`, Theorem 1) is stated for
**O₁ ⊂ O₂ ⊂ ⋯ ⊂ Oₙ** — nested, by containment. Lowell, Karina and Marie are strung
side by side across one basin, thousands of kilometres apart. They are **peers,
not nested orbits.**

So the theorem does not apply to the trio, and `minᵢ(Hᵢ/κᵢ*)` has no referent
here: there is no sense in which Karina's weakness gates Lowell's convergence.
Any reading that says otherwise is reading the shape of the theorem onto a
situation that does not have it. **This is the first thing the exercise
establishes and it should not be buried.**

## 2. A real nesting does exist, and the storms occupy one level of it

What *is* nested is the column the storms live in:

```
eyewall  ⊂  storm  ⊂  basin / season  ⊂  ENSO
```

and the clocks separate cleanly:

| orbit | characteristic time | ratio to the one below |
|---|---:|---:|
| eyewall replacement cycle | ~1 day | — |
| storm lifecycle (Lowell) | ~9 days | ×9 |
| basin season | ~180 days | ×20 |
| ENSO | ~4 years | ×8 |

**Eyewall to ENSO is a factor of about 1,460.** This is exactly the situation
item 19 flagged as untested: the theorem assigns one rate, `e^{−2} per step`, to
every orbit, which is one clock for all orbits. Here there are four clocks and
they differ by three orders of magnitude. The trio does not test the theorem — it
**instantiates the objection to one of its hypotheses.**

## 3. Lowell is a clean instance of the two-threshold structure — and the
## meteorology already has a name for it

Item 18 distinguished a **pointwise** threshold (the rate stops expanding) from a
**lap-wise** one (a full circuit stops opening), and found a band where a system
is losing at every instant and still closing its circuit.

Lowell, 2–5 September:

```
  2 Sep   Cat 5                    peak
  4 Sep   Cat 3, 125 mph           trough   — pointwise, this is failure
  5 Sep   Cat 5, 160 mph, 922 mb   peak     — lap-wise, the circuit closed
```

trough/peak = 0.78; the lap returned to **1.00** of its starting intensity and
past it in absolute terms. A gate testing instantaneous health on 4 September
scores Lowell as failing. It was mid-cycle.

The physical name for that cycle is the **eyewall replacement cycle**: an outer
rainband organises into a secondary eyewall, chokes the inner one, intensity
falls, the new eyewall contracts, and the storm re-intensifies. It is a textbook
phenomenon with a fluid-dynamical account. **Nothing in dm³ derives it, predicts
its timing, or predicts its amplitude.** What the two-threshold reading supplies
is a vocabulary in which the decline is not a failure: the correspondence is
analogical, and no derivation from atmospheric physics is offered.

## 4. The part that is an actual test, and what it costs

On 4 September **all three were declining pointwise.** Karina was weakening,
Marie was weakening, Lowell was at its trough. Instantaneous intensity did not
distinguish them — and only Lowell closed a lap.

So the two-threshold reading is not free. To use it you must already know whether
a decline is **cyclic or terminal**, and on 4 September that judgement came from
meteorology, not geometry: Lowell was in a recognised internal cycle; Karina and
Marie were weakening into a hostile environment — cooler water, shear, higher
latitude — with no cycle to close.

**That is the honest boundary of the exercise.** The framework organises the
observation after the classification is made. It does not make the
classification, and the classification is where all the information is.

## 5. What would be a real test

Stated so it cannot be quietly dropped. The framework would earn something here
if, given a nested column and per-orbit periods, it predicted **the width of the
band** — how far an orbit may decline and still close its circuit — from the
periods alone, in advance, and that width matched observed eyewall-replacement
survival rates. That is a number, it is checkable against existing
best-track archives, and **it has not been computed.** Until it is, this document
is a vocabulary match and should be cited as nothing more.

---

*Sources: NASA Earth Observatory, "A Trio of Tropical Cyclones in the Pacific";
Wikipedia, "Hurricane Lowell (2026)"; Maui Now, 4 September 2026 advisory summary.
Intensities as reported by the NHC. No independent verification of the track data
was performed.*

---

# The test, computed — 2026-09-12

§5 above said the framework would earn something if it predicted the width of the
band from the periods alone and matched it against eyewall-replacement data. Done.
The result is negative.

## The band width, in closed form, from the period alone

The band edge solves ∫₀ᵀ λ(z_c + t) dt = 0 with λ(z) = −2(1 − e^{−z}):

```
    −2T + 2e^{−z_c}(1 − e^{−T}) = 0
    W(T) = |z_c| = ln( T / (1 − e^{−T}) )
```

`W(2π) = 1.839746254986`, matching the constant found independently. So there is a
genuine period-only formula. But **W/T is not constant** — it falls like ln(T)/T:

| T | W(T) | W/T |
|---:|---:|---:|
| 1 | 0.4587 | 0.4587 |
| 2π | 1.8397 | 0.2928 |
| 24 | 3.1781 | 0.1324 |

So "the band width from the periods alone" is only a number once you say *which*
period — eyewall, storm, or season. That ambiguity is the first result and it is
a defect in the proposal, not in the data.

## A prediction that survives the ambiguity

At the band edge the lap exactly closes and splits at λ = 0 into an expanding half
of length W and a contracting half of length T − W. Their ratio is dimensionless:

```
    contract / expand  =  T/W − 1
```

For T = 2π this is **2.4152**: a system that exactly closes its lap should spend
about 2.4× as long recovering as it spent declining.

**And the model has a hard floor.** W(T) → T/2 as T → 0, and W/T falls
monotonically from there, so `W/T < 1/2` for every T > 0 and therefore

```
    contract / expand  >  1      for every period, without exception.
```

The model's entire reachable range is (1, ∞). **It cannot produce a recovery
shorter than the decline, at any period.** That is a falsifiable statement with no
free parameters.

## The data

Sitkowski's ERC climatology — **24 ERCs across 14 hurricanes, aircraft
reconnaissance, 1977–2007**:

| phase | duration |
|---|---|
| weakening | 18–20 h |
| reintensification | 12–15 h |
| total ERC | 42–48 h |
| net intensity change | **near zero** |

Net change near zero is precisely the band-edge condition the prediction is about,
so the comparison is the right one.

```
    observed contract/expand  =  12/20 … 15/18  =  0.60 … 0.83
    model's reachable range   =  (1, ∞)
```

**Falsified, and structurally.** The observation lies outside everything the model
can produce for any period whatsoever — not a parameter mismatch, a sign. Lowell's
own 1 day / 2 days = 0.50 sits *with* the population, so the n = 1 case was not an
outlier; it agreed with 24 others and all 25 disagree with the model.

## The one way out, and why it is not taken

Invert the sign convention — make the quiescent state the attractor and intensity
the excursion — and the phases swap: expanding = intensification (~12 h),
contracting = weakening (18–20 h), ratio 1.50–1.67, inside the model's range and
matched at T ≈ 2.90.

Two reasons that is not a rescue. It requires **fitting** the period, which is not
"from the periods alone" and was the whole point. And it requires Γ to be
**repelling**, which contradicts Theorem A of the toy model, where Γ is the global
attractor everything converges to. A model rescued by reversing its own stability
is not the same model.

## What this does and does not settle

**Settled:** the band-width prediction, stated in §5 and computed here, is false
against the best available ERC sample, for a structural reason, with no parameter
left to adjust.

**Not settled:** anything about whether the *taxonomy* is useful. Items 18 and 19
are about a distinction — pointwise versus lap-wise thresholds — which remains
real in the toy model and remains a live question for the Minimum Orbit Theorem.
What is dead is the specific quantitative bridge from that distinction to hurricane
timing. The vocabulary match of §§1–4 stands exactly where it stood, and is now
known not to extend to this number.

That is the result. It cost one afternoon, and it is the reason to write the test
down before running it.
