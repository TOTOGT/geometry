#!/usr/bin/env python3
"""
ch-claims-awaiting-verification-verify.py -- arithmetic on the figures Science
reported (13 Oct 2026) about OpenAI's release of 722 preprints.

ESTABLISHES: only that the reported figures are consistent with each other.
DOES NOT ESTABLISH: that any of OpenAI's results is correct, that any Lean file
states what its paper claims, or that the figures themselves are right. The
source is one news article; OpenAI's own page was not retrieved.

Run:  python3 book8/ch-claims-awaiting-verification-verify.py
"""
import datetime as dt
FAIL = []
def check(n, c, note=""):
    print("  [%s] %s" % ("SHOWN" if c else "FAIL ", n))
    if note: print("        " + note)
    if not c: FAIL.append(n)
def control(n, c):
    print("  [%s] control: %s" % ("OK   " if not c else "BLIND", n))
    if c: FAIL.append("blind control: " + n)

PRE, WD, REV, FORMAL, RES, PROB = 722, 3, 14, 300, 372, 4000
rem = PRE - WD
print("Counts")
check("722 preprints - 3 withdrawn = 719 remaining", rem == 719)
control("722 - 14 revised is not the remaining count", PRE - REV == rem)
check("719 - 300 formalized = 419 not formalized", rem - FORMAL == 419)
check("formalized share = %.1f%% of remaining" % (FORMAL/rem*100), abs(FORMAL/rem*100-41.7) < .05)
control("300/722 is not 41.7%", abs(FORMAL/PRE*100-41.7) < .05)
check("372 results of ~4000 problems = %.1f%% (so ~%d not solved)" % (RES/PROB*100, PROB-RES), PROB-RES == 3628)
check("%.2f preprints per distinct result" % (PRE/RES), abs(PRE/RES-1.94) < .01,
      "more preprints than results: some results appear in several papers (Science mentions a cluster on one 1975 conjecture)")

print("\nDates")
rel, press = dt.date(2026,10,6), dt.date(2026,10,13)
check("6 Oct release to 13 Oct article = 7 days", (press-rel).days == 7)
control("8 days would be wrong", (press-rel).days == 8)
check("a result 'cracked 10 days earlier' and posted 4 h after OpenAI's: release on 6 Oct means ~26 Sep for the human proof",
      (rel - dt.timedelta(days=10)) == dt.date(2026,9,26),
      "Science says the researchers had cracked it 10 days before they saw the preprint; the 10 days is theirs, reported by Science")

print("\nCost framing")
ah = 10_000 * 88
check("Navier-Stokes run: 10,000 agents x 88 h = %d agent-hours" % ah, ah == 880_000)
print("  [NOTE ] Science contrasts this with ~3 h of ChatGPT Pro 'thinking' per typical result.")
print("          Those are different units (parallel agent-hours vs one session's thinking time);")
print("          no ratio between them is computed here, because it would not mean anything.")

print()
if FAIL: print("FAILED:", FAIL); raise SystemExit(1)
print("ALL CHECKS SHOWN. Arithmetic on reported figures only; no result was checked.")
