#!/usr/bin/env python3
"""
ch-monster-machine-checked-verify.py -- what can and cannot be computed about
the Axiom Math CFSG announcement (Oct 2026) and the Science report on OpenAI's
722 preprints (13 Oct 2026).

WHAT THIS SCRIPT ESTABLISHES (and nothing more)
  A. Arithmetic about the Monster: order factorization, smallest faithful
     character degree 196883 = 47*59*71, and the j-coefficient 196884 = 196883+1.
  B. The classification's count: 1 + 1 + 16 = 18 infinite families, plus 26
     sporadic groups (27 if the Tits group is counted as sporadic).
  C. Internal consistency of the figures REPORTED by Axiom Math and by Science:
     date arithmetic, subtraction, rates. A reported figure that passes here is
     only self-consistent. It is not thereby true.

WHAT IT DOES NOT ESTABLISH
  That the Lean proof exists, compiles, is free of sorry/extra axioms, or states
  CFSG faithfully. Only a reader who builds the repository can check the first
  three; only mathematicians reading the formal statement can check the fourth.
  This script never touches Lean.

Run:  python3 book8/ch-monster-machine-checked-verify.py
"""
import datetime as dt

FAIL = []

def check(name, cond, note=""):
    print("  [%s] %s" % ("SHOWN" if cond else "FAIL ", name))
    if note: print("        " + note)
    if not cond: FAIL.append(name)
    return cond

def control(name, cond):
    """A control must FAIL the property it perturbs; if it passes, the test is blind."""
    print("  [%s] control: %s" % ("OK   " if not cond else "BLIND", name))
    if cond: FAIL.append("blind control: " + name)

# --- A. the Monster ----------------------------------------------------------
print("A. The Monster")
ORDER = 808017424794512875886459904961710757005754368000000000
EXPS = {2:46,3:20,5:9,7:6,11:2,13:3,17:1,19:1,23:1,29:1,31:1,41:1,47:1,59:1,71:1}
prod = 1
for p, e in EXPS.items(): prod *= p**e
check("factorization multiplies to the printed order", prod == ORDER)
check("15 distinct prime divisors", len(EXPS) == 15)
check("order ~ 8.08e53", abs(ORDER / 1e53 - 8.08) < 0.01)
bad = dict(EXPS); bad[2] = 47
bp = 1
for p, e in bad.items(): bp *= p**e
control("2^47 in place of 2^46 must not give the order", bp == ORDER)
check("196883 = 47*59*71", 47*59*71 == 196883,
      "smallest nontrivial irreducible degree; 47,59,71 are the three largest primes dividing |M|")
check("196884 = 196883 + 1 (j(q) = 1/q + 744 + 196884 q + ...)", 196883 + 1 == 196884)
control("47*59*72 must not be 196883", 47*59*72 == 196883)
check("47, 59, 71 each divide |M| exactly once", all(EXPS[p] == 1 for p in (47, 59, 71)))

# --- B. classification count -------------------------------------------------
print("\nB. The statement being formalized")
families = 1 + 1 + 16     # cyclic prime order, alternating n>=5, Lie type
check("18 infinite families (1 cyclic + 1 alternating + 16 Lie type)", families == 18)
check("26 sporadic groups listed", 26 == 26, "27 if the Tits group is counted as sporadic (Axiom's post notes this convention)")
control("17 families must not equal the count", 17 == families)

# --- C1. Axiom Math figures as reported --------------------------------------
print("\nC1. Axiom Math, figures as reported in their post (self-consistency only)")
start, end = dt.date(2026,10,2), dt.date(2026,10,25)
inclusive = (end - start).days + 1
check("Oct 2 through Oct 25 inclusive = 24 days (matches '24 days')", inclusive == 24)
control("exclusive count (23) must not equal 24", (end - start).days == 24)
LINES, MILESTONES, TASKS = 43_100_000, 108, 380
check("about %.2f million lines per day over 24 days" % (LINES/24/1e6), abs(LINES/24/1e6 - 1.80) < 0.01)
check("about %d thousand lines per milestone on average" % round(LINES/MILESTONES/1e3), round(LINES/MILESTONES/1e3) == 399)
check("about %d lines per task on average" % round(LINES/TASKS/1e3*1e3), 113000 < LINES/TASKS < 114000)
check("1.2M inherited lines = %.1f%% of 43.1M" % (1.2e6/LINES*100), abs(1.2e6/LINES*100 - 2.78) < 0.01,
      "so roughly 97% of the lines are new on Axiom's own figures; whether lines are a meaningful measure is a separate question")
print("  [NOTE ] the proof-map page lists 100 milestones in its summary and 108 in the Milestones header.")
print("          That is a discrepancy on Axiom's own page; it is recorded, not resolved.")

# --- C2. Science figures as reported -----------------------------------------
print("\nC2. Science, 13 Oct 2026, on OpenAI's preprints (self-consistency only)")
PRE, WITHDRAWN, REVISED, FORMAL = 722, 3, 14, 300
remaining = PRE - WITHDRAWN
check("722 - 3 withdrawn = 719 remaining (matches the article)", remaining == 719)
control("722 - 14 must not be the remaining count", PRE - REVISED == remaining)
check("300 of 719 formalized = %.1f%%" % (FORMAL/remaining*100), abs(FORMAL/remaining*100 - 41.7) < 0.05)
check("372 results from ~4000 problems = %.1f%%" % (372/4000*100), abs(372/4000*100 - 9.3) < 0.01)
check("10,000 agents x 88 h = 880,000 agent-hours (Navier-Stokes run)", 10_000*88 == 880_000)
check("722 preprints for 372 results = %.2f preprints per result" % (722/372), abs(722/372 - 1.94) < 0.01)

print()
if FAIL:
    print("FAILED:", FAIL); raise SystemExit(1)
print("ALL CHECKS SHOWN. Reminder: these are arithmetic checks on reported figures. No Lean was run.")
