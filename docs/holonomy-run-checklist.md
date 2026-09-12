# What the holonomy run still needs — 2026-09-12

Everything below was read off the two datasets' own documentation through the
browser pane, and where possible checked against real bytes. `book6/ships_parse.py`
and `book6/holonomy-test.py` are green; this is the list of what is not yet closed.

---

## 1. The two downloads — the only thing that needs a human

| file | URL | note |
|---|---|---|
| SHIPS EP 5-day | `rammb-data.cira.colostate.edu/ships/data/EP/lsdiage_1982_2022_sat_ts_5day.txt` | the data host is `rammb-data`, not `rammb2` — which is why the earlier fetch 403'd |
| SHIPS AL 5-day | `.../ships/data/AL/lsdiaga_1982_2022_sat_ts_5day.txt` | second basin, more sample |
| EBTRK EP | `rammb2.cira.colostate.edu/wp-content/uploads/2020/11/EBTRK_EP_final_1949-2021_new_format_02-Sep-2022.txt` | **new** format |
| EBTRK AL | `.../EBTRK_AL_final_1851-2021_new_format_02-Sep-2022-1.txt` | **new** format |

Take the **new format** files. The old ones are maintained for continuity and
have different column widths.

## 2. `RMW` is field 9, not column 19

The EBTRK README gives the field order outright, and its own sample line resolves it:

```
  9  30     RMW        <-- radius of maximum wind
 10  -99    eye_diam
 ...
 19  0      r50_SW     <-- what "column 19" actually lands on
```

Field 19 is the **south-west quadrant radius of 50-knot winds**. A run using it
would have produced a confident ΔRMW that was a change in a wind-radius quadrant,
and nothing would have complained. This is the class of error that is cheap to
check and expensive to be wrong about.

## 3. The sentinels differ between the two files

**SHIPS uses `9999`. EBTRK uses `-99`.** One screening rule does not cover both.
A parser carrying 9999 into EBTRK treats every missing RMW as a valid 99-nm
radius; one carrying −99 into SHIPS catches nothing.

## 4. The usable window is 1990–2021, not 1982–2022

RMW and the outer-isobar variables "were not routinely estimated as part of the
NHC operational forecast procedure prior to 1990". 1988–89 RMW exists only where
aircraft reconnaissance was available, and was smoothed over three observations.
SHIPS begins 1982; EBTRK ends 2021. **The intersection is 32 seasons**, and the
pre-1990 SHIPS years contribute no usable residual.

## 5. Use the SST **anomaly**, not any raw SST

Better than the DSTA recommendation of yesterday. SHIPS carries both:

* `DSTA` — daily Reynolds SST, averaged over 5 points (centre, ±50 km N/E/S/W)
* `XDST` — **climatological value of the daily Reynolds SST**

`DSTA − XDST` is the daily SST **anomaly**, which by construction is not a
function of position and calendar date. That removes the confound at source
rather than partialling it out afterwards — and the partial correlation against
net latitude change stays in as the check that it worked.

`CSST` is the plain climatological SST and is the variable the confound simulation
in `holonomy-test.py` block [5] was built around. Do not use it as a control.

## 6. Use `SHDC`, not `SHRD`

`SHDC` is the 850–200 hPa shear **with the storm's own vortex removed**, averaged
0–500 km relative to the 850 hPa vortex centre. `SHRD` includes the storm's own
contribution — so a test asking whether the *environment* determines the state
would be feeding part of the state back in as a control. `SDDC` gives the shear
heading if a vector loop is wanted rather than a magnitude one.

## 7. Consider eye diameter as a second residual

Sitkowski's finding is that after an eyewall replacement the intensity returns and
**the eye rarely contracts back to its prior radius**. Eye diameter is EBTRK field
10, beside RMW. Two residual variables measuring the same asymmetry, in the same
file, at no extra cost — and agreement between them is worth more than either.

## 8. Filter on the data-source digit (new format only)

The new format adds a 4-digit column after DTL giving the provenance of RMW, eye
diameter, POCI and ROCI: `0` b-deck, `1` a-deck CARQ, `2` OFCL t=0, `3` OFCL t=3,
`4` previous EBTRK version, `9` missing. Restricting to `0` buys consistency at
the cost of sample; at minimum the result must be shown to survive the restriction.

## 9. Two things that bound what can be claimed, whatever the result

**No error estimates exist.** The README: "At present, there are no error
estimates for these variables." So the regression cannot be properly weighted and
no formal confidence interval on the slope is available from the data itself. A
bootstrap over storms is the honest substitute and must be labelled as such.

**Orientation balance is not guaranteed.** The sign-reversal test needs loops of
*both* handedness in comparable numbers. If storms overwhelmingly traverse
(SST-anomaly, shear) space in one direction — which is plausible, since both
tend to evolve monotonically along a track — the clean half of the test may have
no sample. **Count the two populations before running anything else.** If one is
empty, the sign test is unavailable and the result rests on area scaling alone,
which is weaker and should be reported as weaker.

## 10. Still open, and not blocking

Whether SHIPS carries any size variable that would remove the EBTRK join
entirely. Pages 3, 4, 6 and 7 of the format document carry no radius-of-maximum-wind
predictor; page 5 was not read. If one exists there, the join and items 2, 3, 4 and
8 all disappear, which would be worth the five minutes to check.
