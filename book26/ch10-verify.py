#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Pablo Nogueira Grossi / G6 LLC
"""
book26/ch10-verify.py -- book26/ch10-four-pillars-one-mission.html: a vision for the New Jersey Institute for Social Justice.
  [1] sections in order   [2] the book is named as Book XXVI, 2026, and the template-B note is present
  [3] each stat-panel figure is on the page as it was found at its source (table below)
  [4] claims that failed checking on 2026-10-27 cannot return   [5] no network, storage or form
  [6] controls: each check fails on a damaged copy   [HONESTY] what this does not establish

Where each figure was read (2026-10-27, by fetching the page; this script does not fetch):
  $662,500 / $20,000 / 38.4% vs 75.9% / $132,000 vs $0 ..... njisj.org/economic-justice
  40.2 : 1 (241 and 6 per 100,000, 2023) ................... Sentencing Project fact sheet (federal juvenile census)
  29 : 1 (institute page; superseded in the panel) ......... njisj.org/criminal-justice
  59% (institute) vs 12.9% / 15.8% ......................... njisj.org/democracy-justice; nj.gov Labor RP-30; Census QuickFacts
  18 states + DC, NJ 21 days before ......................... NCSL; (institute says 22: not resolved)
  42.6% vs 76.7% (189,814/445,118; 1,511,434/1,970,408) .... ch10-acs-2024-tenure.tsv, Census ACS 2024 B25003B/H
  Newark decree terminated Nov 2025 ....................... justice.gov release of 21 Nov 2025; njisj.org/reports/newark-consent-decree
  S-731/A-796 (7 Jul 2026); S3379 (27 Aug 2026) ............ njbia.org; roi-nj.com (secondary reporting)
  Voter Empowerment Act A-1715/S-282, 2 July 2026 .......... nj.gov/governor/news/2026/20260702a
  Data center plan, four parts, 27 May 2026 ................ nj.gov/governor/news/2026/20260527a
  2 July 2026, tenth state, first after Louisiana v Callais . njisj.org press release of 2 July 2026
  $640,000 gap, 'less than $20,000' ......................... njisj.org press release of 3 April 2025
  60+ groups, 13 May 2026, 20 MW; four-part plan ............ New Jersey Monitor; PYMNTS (secondary)
  $6.1 million, 90%, $10 million, 80,000, 350,000, 3 prisons  position profile (Isaacson, Miller)
Removed after checking: a 'Feb 2026' date for the Newark report (inferred from a file path); a boys' facility at
Bordentown (the page says the only youth prison for girls); '150 Years is Enough' (not on the page); the county
line brief as a 2026 filing (undated); 'Vote 16 expansion' as unfinished (not on any source); the false Uceda title.
"""
import re, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
PAGE = HERE / "ch10-four-pillars-one-mission.html"
FAIL = []

def check(label, ok, detail=""):
    print(("PASS " if ok else "FAIL ") + label + (f"  [{detail}]" if detail and not ok else ""))
    if not ok: FAIL.append(label)

def plain(t):
    t = re.sub(r"<script.*?</script>|<style.*?</style>", " ", t, flags=re.S)
    t = re.sub(r"<[^>]+>", " ", t)
    for a, b in (("&rsquo;", "'"), ("&ldquo;", '"'), ("&rdquo;", '"'), ("&amp;", "&"), ("&middot;", "."),
                 ("&ndash;", "-"), ("&mdash;", "-"), ("&asymp;", "~"), ("&nbsp;", " ")):
        t = t.replace(a, b)
    return re.sub(r"\s+", " ", t)

SECS = ["mission", "economic", "criminal", "democracy", "environmental", "architecture", "updates", "checked"]
FIGS = ["$662,500", "$20,000", "42.6% vs 76.7%", "$132,000 vs $0", "40 : 1", "59% vs 13-16%", "80,000+", "350,000+",
        "18 + DC", "60+", "$6.1 million", "90%", "$640,000", "2 July 2026", "13 May 2026", "20 megawatts", "7 July 2026", "27 August 2026", "S-731/A-796", "S3379", "November 2025"]
# Claims that failed checking and were removed or corrected; none may reappear.
BANNED = ["Use Newark as the proof case", "compliance indicators in consent-decree", "Academic Coordinator", "150 Years is Enough", "Fund for New Jersey", "Feb 2026", "a boys' facility",
          "Vote 16 expansion", "June 2026 I was"]
URLS = ["nj.gov/governor/news/2026/20260702a", "nj.gov/governor/news/2026/20260527a", "ncsl.org/elections-and-campaigns/voter-registration-deadlines",
        "sentencingproject.org/fact-sheet/black-disparities", "data.census.gov/table/ACSDT1Y2024.B25003B", "njisj.org/economic-justice/", "njisj.org/criminal-justice/", "njisj.org/democracy-justice",
        "newjerseymonitor.com/2026/05/27/", "pymnts.com/cpi-posts/coalition-of-60-groups",
        "justice.gov/opa/pr/federal-court-terminates-newark", "roi-nj.com/2026/08/28/", "njbia.org/sherrill-signs-legislation"]
FORBIDDEN = ["fetch(", "XMLHttpRequest", "localStorage", "sessionStorage", "<form", "action=", "<script"]

def secs_ok(t):  return re.findall(r'<section id="([^"]+)">', t) == SECS
def label_ok(t): p = plain(t); return "Book XXVI . 2026" in p and "The 2026 Applications" not in p and "Template B" in t
def figs_ok(t):  p = plain(t); return all(f in p for f in FIGS)
def banned_ok(t): p = plain(t); return not any(b.lower() in p.lower() for b in [x.replace("'", "'") for x in BANNED])
def urls_ok(t):  return all(u in t for u in URLS)
def clean_ok(t): return not any(f in t for f in FORBIDDEN)
def tenure_ok(t):
    """Recompute the homeownership panel from the counts read off the Census tables."""
    import csv
    f = HERE / "ch10-acs-2024-tenure.tsv"
    if not f.exists(): return False
    rows = {r[0]: r for r in csv.reader(f.open(), delimiter="\t") if r and not r[0].startswith("#")}
    pct = lambda k: round(100 * int(rows[k][4]) / int(rows[k][2]), 1)
    return pct("B25003B") == 42.6 and pct("B25003H") == 76.7 and pct("B25003") == 63.9
def upd_ok(t):
    return '<section id="updates">' in t and "Not yet checked, and likely to have moved" in t and "What changed after the sources were written" in t
def exc_ok(t):   return "An exception to this book" in t and "What was checked, and what was not" in t

def main():
    t = PAGE.read_text(encoding="utf-8") if PAGE.exists() else ""
    check("page exists", bool(t))
    if not t:
        print("\nFAILED: page absent"); sys.exit(1)
    check("sections in order", secs_ok(t))
    check("book named Book XXVI . 2026; template-B note present; old title absent", label_ok(t))
    check("stat figures present as found at their sources", figs_ok(t))
    check("homeownership panel recomputes from the Census counts (42.6, 76.7, 63.9)", tenure_ok(t))
    check("claims that failed checking are absent", banned_ok(t))
    check("source links present", urls_ok(t))
    check("exception note and checked/not-checked box present", exc_ok(t))
    check("updates section present, with the not-yet-checked list", upd_ok(t))
    check("no network call, storage, form or script", clean_ok(t))

    print()
    ctl = []
    def control(name, damaged, fn):
        assert damaged != t, "control would be vacuous: " + name
        ok = fn(damaged)
        print(("PASS " if not ok else "FAIL ") + "control rejected: " + name)
        if ok: ctl.append(name)
    control("a section removed",      t.replace('<section id="democracy">', '<section>'), secs_ok)
    control("old book title returns", t.replace("Book XXVI &middot; 2026", "Book XXVI &middot; The 2026 Applications", 1), label_ok)
    control("wealth figure altered",  t.replace("$662,500", "$622,500"), figs_ok)
    control("homeownership figure altered", t.replace("42.6% vs 76.7%", "38.4% vs 75.9%"), figs_ok)
    control("40 to 1 altered",        t.replace("40 : 1", "24 : 1", 1), figs_ok)
    control("false title returns",    t.replace("Coordinator at Uceda until it closed", "Academic Coordinator at Uceda until it closed", 1), banned_ok)
    control("source link dropped",    t.replace("newjerseymonitor.com/2026/05/27/", "example.invalid/", 1), urls_ok)
    control("updates section emptied", t.replace("Not yet checked, and likely to have moved", "Notes"), upd_ok)
    control("stale Newark framing returns", t.replace("Use Newark as the test of whether reform outlasts oversight.", "Use Newark as the proof case."), banned_ok)
    control("checked box removed",    t.replace("What was checked, and what was not", "Notes"), exc_ok)
    control("script added",           t.replace("</body>", "<script>fetch('x')</script></body>"), clean_ok)

    print()
    print("[HONESTY] This verifies the page against what was read at its sources on 2026-10-27. It does NOT")
    print("          fetch them again, and the Institute's pages may have changed. The agenda items are the")
    print("          author's proposals, not the Institute's plans. It is a work sample, not a prediction")
    print("          that the author would be chosen, and not a statement by the Institute.")
    print()
    if FAIL or ctl:
        print(f"FAILED: {len(FAIL)} check(s), {len(ctl)} control(s) that should have been rejected"); sys.exit(1)
    print("ALL PASS")

if __name__ == "__main__":
    main()
