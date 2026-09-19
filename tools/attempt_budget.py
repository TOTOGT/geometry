#!/usr/bin/env python3
"""What $3-4k buys a one-person desk, and what it does not.

Usage:
    python3 tools/attempt_budget.py
    python3 tools/attempt_budget.py --budget 4000
    python3 tools/attempt_budget.py --rate-in 3 --rate-out 15 --attempts-per-day 400

WHAT THIS IS FOR, AND WHAT IT REFUSES

The request was a budget saying that solving the Riemann Hypothesis needs
$3,000-$4,000. No budget can say that. RH is not compute-bound; if it were
bounded by money it would have been bought. A number attached to a theorem does
not become true by being small and specific -- it becomes persuasive, which is
worse, because a reader cannot check it and will not try.

What the money is actually for is not tokens. It is CAPITAL: a machine, a
retrieval index over the corpus, storage. And the point of capital is not that
it is cheaper per unit. It is that it has NO unit. A metered API charges per
attempt, so the menial half of discovery -- enumerate, discard, re-enumerate --
is charged at the same rate as the useful half, and a desk with no funding
simply does not run it. Owning the machine moves that cost from the meter to a
one-off, after which the marginal cost of an attempt is electricity.

That is the fundable sentence, and it is checkable:

    $3-4k converts a per-attempt metered cost into a fixed cost, after which
    the menial half of discovery can be run at all.

CURRENT STATE: ZERO. There is no compute budget at this desk. Not a small one.
None. Every figure below describes a transition from nothing, which is why the
break-even is the number that matters rather than the total.

WHAT IS NOT PRICED HERE, AND IS NOT AN OVERSIGHT

Labour. The author's own time is not in this budget and is not intended to be.
A reader should know that the plan's largest input is unpaid rather than cheap.
Printing a total that silently excludes it would be the same move as printing a
count without its denominator, which this corpus spends most of its pages
objecting to.

THE PRICES ARE PLACEHOLDERS. Replace them from invoices and quotes before this
goes in front of anybody. A cost model quoting its own defaults is the same
object as a page quoting its own earlier page.
"""
import argparse
import sys

CAPITAL = [
    ("Workstation with enough memory to hold a usable local model", 2400.0,
     "The single line that decides whether the marginal cost of an attempt is "
     "a metered rate or electricity."),
    ("Storage for the corpus, the floor texts and the indexes", 250.0,
     "Thirteen repositories, ~800 pages of HTML in one of them, and 5,309 "
     "pages of third-party PDF already on the desk."),
    ("Embedding pass to build the retrieval index, one-off", 150.0,
     "Charged once per corpus revision, not per query. The index is then "
     "local and free to read."),
    ("Contingency, 15%", 420.0,
     "Named rather than hidden inside the other lines."),
]

NOT_PRICED = [
    ("The author's time", "Unpaid. The largest input in the plan."),
    ("Electricity", "Real, small, and not estimated here."),
    ("Peer review, publication fees, travel", "Out of scope for this budget."),
]

DEFAULTS = dict(
    rate_in=3.00,            # USD / 1M input tokens, metered API   [PLACEHOLDER]
    rate_out=15.00,          # USD / 1M output tokens, metered API  [PLACEHOLDER]
    tok_in=8_000,            # input tokens per attempt
    tok_out=2_000,           # output tokens per attempt
    attempts_per_day=400.0,  # what a search loop would actually run
    budget=3500.0,
)


def main():
    ap = argparse.ArgumentParser(add_help=True)
    for k, v in DEFAULTS.items():
        ap.add_argument("--" + k.replace("_", "-"), type=float, default=v)
    a = ap.parse_args()

    capital = sum(c for _, c, _ in CAPITAL)
    metered = (a.tok_in / 1e6) * a.rate_in + (a.tok_out / 1e6) * a.rate_out

    print("  PLACEHOLDER PRICES. Replace from invoices before quoting.")
    print("  CURRENT COMPUTE BUDGET AT THIS DESK: ZERO.\n")

    print("  %-58s %10s" % ("capital, one-off", "USD"))
    for name, cost, _ in CAPITAL:
        print("  %-58s %10s" % (name[:58], "%.0f" % cost))
    print("  %-58s %10s" % ("", "-" * 9))
    print("  %-58s %10s" % ("total capital", "%.0f" % capital))
    print("  %-58s %10s" % ("stated budget", "%.0f" % a.budget))
    print()

    print("  NOT PRICED")
    for name, why in NOT_PRICED:
        print("    %-26s %s" % (name, why))
    print()

    if metered <= 0:
        print("::error::metered cost per attempt is zero -- check the rates")
        return 1

    break_even = capital / metered
    days = break_even / a.attempts_per_day if a.attempts_per_day > 0 else float("inf")

    print("  SUBSTITUTION, NOT PAYBACK")
    print("  metered cost per attempt            $%.4f" % metered)
    print("  capital / metered cost              %.0f attempts" % break_even)
    print("  at %.0f attempts a day that is       %.0f days (%.1f months)"
          % (a.attempts_per_day, days, days / 30.4))
    print()
    print("  Read that as a substitution figure, not a return. It says what the")
    print("  capital replaces IF the metered spend were happening. It is not")
    print("  happening: the budget at this desk is zero, so the real comparison")
    print("  is not metered against owned. It is running the search against not")
    print("  running it.")
    print()

    print("  WHY NOBODY FUNDS THIS, INCLUDING PEOPLE WHO COULD")
    print("  A laboratory with millions would not buy this either, and not")
    print("  because the sum is awkward. The investment is open-ended and the")
    print("  return is zero: no product at the end, no licensable asset, no")
    print("  date. Capital goes to problems with returns. That is rational, and")
    print("  it is why work of this kind has always been done by people who were")
    print("  not paid for it -- and why the result, when one arrives, arrives")
    print("  looking authorless.")
    print()

    print("  THE SENTENCE THIS SUPPORTS")
    print("  $%.0f is not an investment and does not pay back. It is the price" % a.budget)
    print("  of the menial half of discovery becoming runnable at a desk where")
    print("  it is currently not run at all: a machine, an index, and no meter.")
    print("  The author's time is not in the figure and is not being paid for.")
    print()
    print("  THE SENTENCE THIS DOES NOT SUPPORT")
    print("  'To solve RH we need $3-4k.' Nobody can price a theorem, and a")
    print("  programme that says so loses the one reader it most needs: the one")
    print("  who already knows the problem is not compute-bound.")
    print()
    print("  Ask for the machine. Do not sell the theorem.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
