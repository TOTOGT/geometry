#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Pablo Nogueira Grossi / G6 LLC
"""
book26/ch09-verify.py -- book26/ch09-a-licence-before-a-student.html: NJ private career school status and the ETPL route.
  [1] sections S1..S6 in order   [2] the citations are present and spelled as in the source message
  [3] the money figures are present and unaltered   [4] no individual is named; no network, storage or form
  [5] the disclaimers are present (not legal advice; no determination; the eight-agency list of the cheaper route)
  [6] controls: each check fails on a damaged copy   [HONESTY] what this does not establish
"""
import re, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
PAGE = HERE / "ch09-a-licence-before-a-student.html"
FAIL = []

def check(label, ok, detail=""):
    print(("PASS " if ok else "FAIL ") + label + (f"  -- {detail}" if detail else ""))
    if not ok: FAIL.append(label)

def plain(t):
    t = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", t, flags=re.S)
    t = re.sub(r"<[^>]+>", " ", t)
    for a, b in (("&rsquo;", "'"), ("&ldquo;", '"'), ("&rdquo;", '"'), ("&amp;", "&"),
                 ("&mdash;", "-"), ("&ndash;", "-"), ("&middot;", "."), ("&nbsp;", " ")):
        t = t.replace(a, b)
    return re.sub(r"\s+", " ", t)

SECS = ["S1", "S2", "S3", "S4", "S5", "S6"]
# Citations exactly as the source message gave them. A wrong citation sends a reader to the wrong law.
CITES = ["N.J.S.A. 34:15C-10.1", "N.J.A.C. 12:41", "N.J.A.C. 6A:19", "N.J.A.C. 12:41-2.2"]
# Money. These are the two numbers a reader would act on.
FIGS = ["$1,150", "$20,000"]
# The four-part test and the three exclusions must both survive editing.
SUBSTANCE = ["future education or the workplace", "avocational, cultural or recreational",
             "non-refundable", "several months", "page 7"]
DISCLAIM = ["not legal advice", "no determination was requested",
            "difficult to say with certainty"]
# The officer is a named individual in a public role; this book does not name people.
NAMED = ["tatsiana", "dagrosa", "grosa,"]
# The eight bodies the reply lists for the cheaper (ETPL-only) route, read from the image in the message.
AGENCIES = ["Department of Education", "Office of the Secretary of Higher Education", "State Police",
            "Motor Vehicle Commission", "Federal Aviation Administration", "Office of Apprenticeship",
            "Board of Cosmetology and Hairstyling", "Real Estate Commission"]
FORBIDDEN = ["fetch(", "XMLHttpRequest", "localStorage", "sessionStorage", "<form", "action="]

def secs_ok(t):  return re.findall(r'<div class="sec" data-n="([^"]+)">', t) == SECS
def cites_ok(t): p = plain(t); return all(c in p for c in CITES)
def figs_ok(t):  p = plain(t); return all(f in p for f in FIGS)
def subst_ok(t): p = plain(t).lower(); return all(s in p for s in SUBSTANCE)
def disc_ok(t):  p = plain(t).lower(); return all(d in p for d in DISCLAIM)
def agencies_ok(t): p = plain(t); return all(a in p for a in AGENCIES) and 'did not come through' not in p
def clean_ok(t):
    low = t.lower()
    return not any(n in low for n in NAMED) and not any(f in t for f in FORBIDDEN)

def main():
    t = PAGE.read_text(encoding="utf-8") if PAGE.exists() else ""
    check("page exists", bool(t))
    if not t:
        print("\nFAILED: page absent"); sys.exit(1)

    check("sections S1..S6 in order", secs_ok(t))
    check("citations present and spelled as received", cites_ok(t))
    check("fee and bond figures present and unaltered", figs_ok(t))
    check("test, exclusions and timing survive editing", subst_ok(t))
    check("disclaimers present", disc_ok(t))
    check("all eight agencies listed; no 'did not come through' wording", agencies_ok(t))
    check("no individual named; no network, storage or form", clean_ok(t))

    # R24. A check that cannot fail is not a check. Damage a copy and require refusal.
    print()
    ctl = []
    def control(name, damaged, fn):
        ok = fn(damaged)
        print(("PASS " if not ok else "FAIL ") + "control rejected: " + name)
        if ok: ctl.append(name)
    control("a section removed",        t.replace('<div class="sec" data-n="S4">', '<div class="sec">'), secs_ok)
    control("citation altered",         t.replace("34:15C-10.1", "34:15C-10.2"), cites_ok)
    control("fee altered",              t.replace("$1,150", "$1,500"), figs_ok)
    control("bond altered",             t.replace("$20,000", "$2,000"), figs_ok)
    control("'non-refundable' dropped", t.replace("Non-refundable.", "").replace("non-refundable", ""), subst_ok)
    # NOTE: the page writes "not</b> legal advice" and "Not legal advice." -- a naive
    # replace("not legal advice", ...) matches neither and damages nothing. The first
    # version of this control was itself vacuous and passed; R24 caught it, not a reader.
    control("disclaimer dropped",       t.replace("not</b> legal advice", "</b> guidance")
                                         .replace("Not legal advice.", ""), disc_ok)
    d = t.replace("Real Estate Commission: real estate schools", "x")
    assert d != t, "agency control would be vacuous"
    control("one agency dropped",       d, agencies_ok)
    control("'missing' wording returns", t.replace("pasted into the e-mail as an image", "did not come through"), agencies_ok)
    control("officer named",            t.replace("<body>", "<body>Tatsiana DaGrosa"), clean_ok)

    print()
    print("[HONESTY] This verifies the page against the message it was written from. It does NOT")
    print("          establish that the figures are current, that the citations say what the page")
    print("          says they say, or that this company is or is not a private career school.")
    print("          No determination was requested or received. Not legal advice.")

    if FAIL or ctl:
        print(f"\nFAILED: {len(FAIL)} check(s), {len(ctl)} control(s) that should have been rejected")
        sys.exit(1)
    print("\nALL PASS")

if __name__ == "__main__":
    main()
