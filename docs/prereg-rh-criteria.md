# Pre-registration: three numerical tests of RH criteria (written before the run)

Date: 2026-10-25 (US Eastern). Written and committed BEFORE `docs/rh-criteria-check.py` was run.
Never edited after the run; a change is `prereg-rh-criteria-2.md`.

Purpose. Vol. Ω No. 14 withdrew the "non-integrability <=> RH" equivalence and left two known
criteria standing. This file fixes, in advance, what is tested for Vol. Ω No. 15, what counts as
a pass, and what the test is shown able to detect. No test here can prove RH. A pass means
"no counterexample in the stated range"; a fail would be a finding that needs a second,
independent check before anything is claimed.

## T1. Lagarias / Robin, arithmetic side (equivalent to RH, unconditional equivalences)
- Lagarias (2002): RH <=> sigma(n) <= H_n + exp(H_n) ln H_n for all n >= 1, strict for n > 1.
- Robin (1984): RH <=> sigma(n) < e^gamma n ln ln n for all n > 5040.
- Range: every n <= 10**7 (integer sieve, exact integer sigma; floats only for the bound,
  with the margin printed).
- Outcome rule: PASS if no n in range violates. FAIL otherwise.
- Control (detectability): the same loop with Robin's constant replaced by 0.99 e^gamma must
  report violations (n > 5040); with Lagarias's right side multiplied by 0.95 it must report
  violations. If a control reports none, the test is vacuous and is reported as such.
- Weight: 10**7 is far below any range where a violation would be expected if RH were false.
  Reported as such, not as evidence for RH.

## T2. Zeros on the line up to height T (Backlund counting)
- Count real sign changes of Hardy Z(t) on (0, T] with step h, and compare with N(T) from
  the argument principle (mpmath nzeros). If equal, every zero up to T is on the line and
  simple (numerical, not interval-certified).
- T = 300, h = 0.02 (precision 20 digits). PASS if counts are equal. A step too coarse to
  separate two close zeros shows as a deficit; any deficit is re-run with h/4 before it is called.
- Control: replace one adjacent pair of zeros of Z by a complex-conjugate pair c +/- i*eps
  (multiply by ((t-c)^2+eps^2)/((t-t1)(t-t2))); the sign-change count must drop by exactly 2.

## T3. Lagarias analytic side, fine grid near zeros
- Re(xi'/xi)(s) > 0 for Re s > 1/2 (Lagarias 1999), evaluated as sum over the first 30 zeros
  of Re 1/(s-rho) plus the smooth remainder is NOT used; instead evaluated directly from
  xi(s) = (1/2) s(s-1) pi^(-s/2) Gamma(s/2) zeta(s) with mpmath.
- Grid: sigma in {0.5005, 0.501, 0.505, 0.51, 0.55, 0.6, 0.75, 1, 2}, t from 0.5 to 100 at step 0.01
  for sigma <= 0.51 near each of the first 29 zeros (+/- 0.5), step 0.05 elsewhere.
- PASS if the minimum of Re(xi'/xi) over the grid is > 0.
- Control: xi multiplied by (s-(rho1+0.02))/(s-rho1), moving the first zero to Re s = 0.52;
  the minimum must go negative at a grid point within 0.02 of rho1.

## What is not tested, and why
- Li coefficients, Weil positivity, Jensen polynomials: not run; no instrument built or controlled.
- The contact condition itself: already refuted as an equivalence (RH paper 4.9, ch14A check 3).
