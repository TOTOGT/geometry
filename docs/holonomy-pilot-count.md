# Orientation count — pilot, n = 1 storm, 2026-09-12

Run on real SHIPS bytes pulled through the browser pane: **EP011982**, init
1982-05-20 00Z, the first case in `lsdiage_1982_2022_sat_ts_5day.txt`. Controls
are the SST anomaly `DSTA − XDST` and vortex-removed shear `SHDC`, at 6-hourly
steps from t = 0 to 120 h. This is one storm. Everything below is a pilot and the
sample size is stated in every claim.

## The trajectory does not close over the full window

```
  t=0    anomaly +0.20 degC   shear  6.4 kt
  t=120  anomaly -0.20 degC   shear 28.7 kt
  closure gap: 0.40 degC, 22.3 kt
```

Shear ran from 6.4 to 28.7 kt and did not come back. My first read of that was
pessimistic — that storms evolve monotonically and closed loops would be rare.
**That read was wrong**, and the increments say why: 10 of the 19 six-hour shear
steps were upward and 9 were downward. The shear oscillates while drifting. The
drift prevents the *whole window* from closing; the oscillation lets *sub-windows*
close.

## Closed sub-loops exist, and both orientations appear

Searching all sub-tracks of at least 24 h that return to within tolerance in both
controls:

| tolerance | closed sub-loops | orientations |
|---|---:|---|
| ±0.15 °C, ±2.0 kt | **2** | both CW |
| ±0.25 °C, ±4.0 kt | **8** | 1 CCW, 7 CW |
| ±0.40 °C, ±6.0 kt | **17** | CCW and CW both present |

So the population is not empty — the risk named as item 9 of the run checklist
does not materialise, at least not here. One storm yields loops. Across 32
seasons of two basins the sample should be substantial.

## Three things this pilot changes about the design

**1. The loops overlap, badly, and must not be counted as independent.**

```
  t= 54 -> 114 h   area -3.600
  t= 60 -> 102 h   area -3.975
  t= 60 -> 114 h   area -3.650
  t= 72 ->  96 h   area -0.705
  t= 72 -> 108 h   area -1.370
```

These share most of their path. They are five views of one structure, not five
samples. Treating them as independent would inflate the significance of any
regression enormously — and with one storm producing eight "loops" at moderate
tolerance, a naive count across 32 seasons would report tens of thousands of
observations where there are perhaps hundreds of independent ones. **Selection
must enforce non-overlap within a storm**, and the statistics must cluster by
storm regardless. This is the single most important thing the pilot found.

**2. The orientation mix is tolerance-dependent.** At ±0.15/±2.0 both loops are
clockwise; loosening to ±0.40/±6.0 brings counter-clockwise ones in. So the
CW/CCW balance — the thing the sign-reversal test depends on — is not a property
of the data alone but of where the closure threshold is set. **The count must be
run across a tolerance sweep and reported as a curve, not a number**, and the
sign test must be shown to survive the sweep or be reported as not surviving it.

**3. Loop count scales steeply with tolerance**: 2 → 8 → 17 across a modest
widening. Combined with (1), that means the headline "N loops found" is almost
meaningless without both the tolerance and the non-overlap rule stated beside it.

## What this does not establish

That the CW and CCW populations are comparable in the full dataset — one storm
cannot say. That any of these loops has a measurable ΔRMW — no EBTRK data is
joined yet. That the areas are large enough for a residual to be detectable above
the unquantified RMW error. The pilot establishes that **the geometry code runs on
real values, closed loops exist, and the counting design as previously specified
would have over-counted by roughly an order of magnitude.**

*Method: values parsed with `book6/ships_parse.py`; signed area by shoelace on the
(anomaly, shear) polygon. One storm, three overlapping analysis cases of it, from
a 50 KB sample of a file that is far larger.*
