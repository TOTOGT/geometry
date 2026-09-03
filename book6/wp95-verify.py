#!/usr/bin/env python3
"""
wp95-verify.py — reproduces every published figure in
book6/wp95-the-right-word-the-wrong-reader.html

Standing rule (CLAUDE.md, 2026-08-27): a published number must be produced by a
tool in the repository. Every figure on WP-95 is computed here.

The script runs a known-answer self-test BEFORE reporting anything and exits
non-zero if any fixture fails. The fixtures include an HONEST CONTROL — an
independently funded subscriber, where loss absorption must come out POSITIVE.
A metric that reported zero on every case would look authoritative and mean
nothing; the control is what makes the zero informative.

    python3 book6/wp95-verify.py            # self-test, then the table
    python3 book6/wp95-verify.py --quiet    # self-test only, exit code is the result

No transaction data is used. Every parameter is illustrative and is declared as
such on the page (WP-95 §8).
"""

import sys

# ---------------------------------------------------------------- parameters
# All STYLIZED. Chosen to make the arithmetic legible, not drawn from any
# identified transaction.
L_PLACEMENT = 100.0     # initial placement                              (T0)
ADVANCE_RATE = 0.77     # advance rate, both collateral legs         (T2, T4)
R_LOAN = 4.00           # administered rate on the collateralized advance, %
C_COUPON = 6.25         # coupon on the capital instrument subscribed at T3, %
I_POLICY_A = 10.00      # Country A policy rate, %
SPREAD_A = 2.00         # domestic corporate spread over policy, percentage pts
I_FUND_B = 0.25         # Country B dollar funding cost, %


# ----------------------------------------------------------------- mechanics
def loss_absorption(face_instrument, face_loan):
    """
    Net loss absorption in the trigger state.

    In the write-down state tau the instrument goes to zero, so the pledged
    asset is worthless while the loan obligation stands at its face. Absent
    independent recourse capacity the issuer realises a credit loss equal to
    the loan. Net absorption is therefore the capital raised less the credit
    loss the raising created.

        Lambda = F - L

    Lambda > 0  capital genuinely absorbs loss
    Lambda = 0  circular: the write-down is exactly offset by the default
    Lambda < 0  the issuance is loss-making in the state it exists to survive
    """
    return face_instrument - face_loan


def net_carry_bp(coupon_pct, loan_rate_pct):
    """Subscriber net carry, basis points. Positive => paid to hold the paper."""
    return (coupon_pct - loan_rate_pct) * 100.0


def collateral_chain(placement, advance_rate, legs=2):
    """Gross notional supported by one cash pool through a chain of pledges."""
    amounts = [placement]
    for _ in range(legs):
        amounts.append(amounts[-1] * advance_rate)
    return amounts, sum(amounts)


def wedge_split(domestic_pct, administered_pct, funding_pct):
    """Rate wedge and how the administered rate divides it, in basis points."""
    saving = (domestic_pct - administered_pct) * 100.0
    margin = (administered_pct - funding_pct) * 100.0
    total = (domestic_pct - funding_pct) * 100.0
    return saving, margin, total


# ----------------------------------------------------------------- self-test
FIXTURES = [
    # (name, F, L, expected Lambda, why this case exists)
    ("circular (L = F)",        77.0,  77.0,   0.0,
     "the WP-95 case: capital raised with the issuer's own money"),
    ("over-financed (L > F)",   77.0, 100.0, -23.0,
     "loan exceeds the subscription; the issuance loses money in tau"),
    ("HONEST CONTROL (L = 0)",  77.0,   0.0,  77.0,
     "independently funded subscriber; absorption must be POSITIVE"),
    ("partial financing",       77.0,  38.5,  38.5,
     "half-funded by the issuer; absorption is halved, not destroyed"),
]


def self_test(verbose=True):
    """Known-answer tests. Returns True only if every fixture passes."""
    ok = True
    if verbose:
        print("SELF-TEST — known-answer fixtures")
        print("-" * 72)
    for name, F, L, expected, why in FIXTURES:
        got = loss_absorption(F, L)
        passed = abs(got - expected) < 1e-9
        ok &= passed
        if verbose:
            print(f"  [{'PASS' if passed else 'FAIL'}]  {name:<24} "
                  f"F={F:>6.2f} L={L:>6.2f}  Lambda={got:>7.2f} "
                  f"(expect {expected:>7.2f})")
            print(f"          {why}")

    # The control must be strictly positive, or the metric cannot tell
    # genuine capital from circular capital and every result above is noise.
    control = loss_absorption(77.0, 0.0)
    discriminates = control > 0
    ok &= discriminates
    if verbose:
        print(f"  [{'PASS' if discriminates else 'FAIL'}]  "
              f"discrimination check: control is strictly positive")

    # Chain arithmetic against a hand-computed answer.
    _, gross = collateral_chain(100.0, 0.77, legs=2)
    chain_ok = abs(gross - (100.0 + 77.0 + 59.29)) < 1e-9
    ok &= chain_ok
    if verbose:
        print(f"  [{'PASS' if chain_ok else 'FAIL'}]  "
              f"collateral chain: 100 + 77 + 59.29 = {gross:.2f}")

    # Wedge must decompose exactly: saving + margin == total.
    s, m, t = wedge_split(12.00, 4.00, 0.25)
    wedge_ok = abs((s + m) - t) < 1e-9 and abs(t - 1175.0) < 1e-9
    ok &= wedge_ok
    if verbose:
        print(f"  [{'PASS' if wedge_ok else 'FAIL'}]  "
              f"wedge decomposition: {s:.0f} + {m:.0f} = {t:.0f} bp")
        print("-" * 72)
        print("SELF-TEST " + ("PASSED" if ok else "FAILED"))
        print()
    return ok


# -------------------------------------------------------------------- report
def report():
    domestic = I_POLICY_A + SPREAD_A
    saving, margin, wedge = wedge_split(domestic, R_LOAN, I_FUND_B)
    amounts, gross = collateral_chain(L_PLACEMENT, ADVANCE_RATE, legs=2)
    multiplier = gross / L_PLACEMENT
    carry = net_carry_bp(C_COUPON, R_LOAN)
    face_instrument = amounts[1]          # subscribed at T3
    face_loan = amounts[1]                # funded by the T2 advance: L = F
    lam = loss_absorption(face_instrument, face_loan)

    print("WP-95 — The Right Word, the Wrong Reader")
    print("Every figure below is STYLIZED. No transaction data is used.")
    print("=" * 72)

    print("\n§2.1  RATE WEDGE")
    print(f"  Country A policy rate                {I_POLICY_A:>8.2f} %")
    print(f"  Domestic corporate spread            {SPREAD_A:>8.2f} pp")
    print(f"  Borrower's domestic cost             {domestic:>8.2f} %")
    print(f"  Administered loan rate               {R_LOAN:>8.2f} %")
    print(f"  Country B funding cost               {I_FUND_B:>8.2f} %")
    print(f"    borrower saving                    {saving:>8.0f} bp")
    print(f"    bank margin                        {margin:>8.0f} bp")
    print(f"    wedge                              {wedge:>8.0f} bp")

    print("\n§2.2  COLLATERAL CHAIN")
    for i, a in enumerate(amounts):
        print(f"  leg {i}                                {a:>8.2f}")
    print(f"  gross notional G                     {gross:>8.2f}")
    print(f"  multiplier G/L                       {multiplier:>8.2f} x")

    print("\n§4    SUBSCRIBER NET CARRY")
    print(f"  instrument coupon c                  {C_COUPON:>8.2f} %")
    print(f"  loan rate r                          {R_LOAN:>8.2f} %")
    print(f"  net carry pi = c - r                 {carry:>+8.0f} bp")
    if carry > 0:
        print("  => subscriber is PAID to hold the issuer's capital.")
        print("     Negative net cost of funds to the subscriber of a capital")
        print("     instrument is the screen proposed in §4.")

    print("\n§3    LOSS ABSORPTION IN THE TRIGGER STATE")
    print(f"  instrument face F                    {face_instrument:>8.2f}")
    print(f"  loan face L                          {face_loan:>8.2f}")
    print(f"  Lambda = F - L                       {lam:>8.2f}")
    if abs(lam) < 1e-9:
        print("  => CIRCULAR. The write-down is exactly offset by the default")
        print("     it causes. The instrument absorbs nothing.")

    print("\n" + "=" * 72)
    print("Compare the honest control: an independently funded subscriber of")
    print(f"the same instrument gives Lambda = {loss_absorption(face_instrument, 0.0):.2f}, "
          "which is what")
    print("capital is supposed to do.")


def main():
    quiet = "--quiet" in sys.argv
    if not self_test(verbose=not quiet):
        print("SELF-TEST FAILED — refusing to report. "
              "An instrument with no working known-answer case is not "
              "known to work.", file=sys.stderr)
        return 1
    if not quiet:
        report()
    return 0


if __name__ == "__main__":
    sys.exit(main())
