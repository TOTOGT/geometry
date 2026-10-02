# Pre-registration: Bitcoin as a fold row in the g-series translation table

Written 2026-10-02, before any price data was downloaded, plotted or looked at.
Status: DRAFT. The thresholds below were proposed by Claude; the author edits any of them
BEFORE committing. Once committed, this file is not edited. A change means a new dated file
(`prereg-bitcoin-2.md`) that says what changed and why, and the first file stays.

## Question
Does bitcoin's daily price behave, before large drawdowns, as the fold model predicts
(critical slowing: variance AND lag-1 autocorrelation rise together), beyond what a
volatility-clustering null produces? This is a test of structure only. It makes no claim about
prices, returns or trading.

## What the fold predicts (and what it does not)
Operator F (fold and jump) predicts rising variance and rising lag-1 autocorrelation of the
detrended state as the driver nears K*. C (one slow variable), K (repeatable critical driver
value) and U (hysteresis) need a driver series. This first pass is price-only, so K and U are
NOT TESTED and the row cannot be marked "established" from it.

## Data (fixed before looking)
- Daily BTC-USD close, one named public source (author chooses and records it in the first
  commit message or at the end of this file before running).
- Full history available from that source up to the commit date of this file. No later data.
- No data from any other asset or index.

## Fixed analysis choices (the researcher degrees of freedom, pinned)
1. State x_t = log(close_t) minus the trailing (causal) 90-day mean of log(close). No centred
   windows, so no future data enters.
2. Event = a decline of at least 30% from the trailing 60-day maximum, reached within 60 days.
   Event start = the date of that trailing maximum. Events closer than 120 days to an earlier
   event are merged into it (declustering).
3. Window = the 120 days before each event start. Statistics computed in rolling 60-day
   windows inside it: variance of x and lag-1 autocorrelation of x.
4. Statistic = Kendall tau of each rolling statistic against time, averaged over events.
5. Null = 1000 surrogate series from a GARCH(1,1) with Student-t innovations fitted to the same
   data, run through steps 1-4 identically (same event rule, same windows).
6. Primary test = the real mean Kendall tau for BOTH lag-1 autocorrelation and variance is
   at or above the 95th percentile of the surrogates. One primary test, no others promoted
   afterwards. Secondary results are reported as secondary.

## Rivals
- Stochastic volatility / jumps: raises variance without raising autocorrelation. Expected
  surrogate behaviour: tau(variance) high, tau(autocorrelation) near zero.
- Smooth (supercritical) change: slowing with no jump; excluded by the event rule only in part,
  so reported but not separately tested here.

## Outcomes, decided now
- Primary test fails: the row is "analogy" and F is not supported by this data.
- Primary test passes: the row is "model", with the explicit note "F-signature only; C, K, U
  not tested". Never "established" from this pass.
- Fewer than 6 declustered events: the test is reported as underpowered and the row stays at
  "analogy" whatever the numbers say.
- Every result is logged in docs/audit-log.md including failures, with the number of events,
  the surrogate count and the exact taus.

## Known limits, stated before the run
Few large episodes; non-stationary market structure over the sample; the 30%/60-day/90-day
choices are conventions, not derived; GARCH(1,1)-t is one null among many; this does not
address any driver.
