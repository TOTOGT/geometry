#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Pablo Nogueira Grossi / G6 LLC
"""
strogatz-citations-verify.py -- check every Strogatz citation this corpus makes
against the book itself.

WHY. Several pages cite Strogatz by page and example number: book6/wp122,
book7/ch-strogatz, and -- added 2026-09-17 -- ch-van-der-pol, ch-smale,
ch-euler and ch-conley, written after this script existed. A page number is an address, and this corpus's standing rule is that
an address is checked, not remembered. Until 2026-09-17 none of these had been
opened against the source.

The book is not in this repository and will not be. Supply your own copy:

    python3 book7/strogatz-citations-verify.py /path/to/strogatz.pdf

EDITION. S. H. Strogatz, "Nonlinear Dynamics and Chaos", 2nd ed., Westview 2015
/ CRC 2018, ISBN 978-0-8133-4910-7. Checked against the 2018 printing, 532 PDF
pages, 481 printed pages located.

METHOD. Printed page numbers are read off the top of each page rather than
assumed from an offset -- the offset is NOT constant in this printing. The run
reports it directly: three distinct values, 4 to 18. So any check that hard-codes
one is checking the wrong page and will still pass on a lucky hit. Each claim then asserts that
specific strings appear on that specific printed page.

Page numbers are also not simply the leading integer: on recto pages the running
head is set tight against the number, so "2818.7 POINCARE MAPS" is page 281 of
section 8.7. Two pypdf versions disagree about the whitespace there, and a
reader that did not handle it found only 278 of 513 pages under pypdf 6.18 and
all of them under an older build -- a verifier whose verdict depends on its
extractor is not a verifier. read_page_number() below is the fix.

The located-page count depends on the extractor, so the run prints its pypdf
version beside it. A count quoted without that version is not reproducible.

Requires pypdf.  Exit 0 iff every claim holds.
"""
import re, sys

FRONT_MATTER_MAX = 40   # bound on (pdf index - printed page); it is 14-18 here

EDITION = "Strogatz, Nonlinear Dynamics and Chaos, 2nd ed. (2018 printing)"

# (citing file, printed page, [strings that must appear on it], note)
CLAIMS = [
 ("book7/ch-strogatz",        198, ["7.0", "limit cycle"],
  "section 7.0 opens Chapter 7"),
 ("book6/wp122 + ch-strogatz",199, ["Example 7.1.1", "limit cycle"],
  "Example 7.1.1, the r(1-r^2) limit cycle"),
 ("book6/wp122",              201, ["7.2"],
  "section 7.2, ruling out closed orbits"),
 ("book6/wp122",              203, ["7.2"],
  "still inside 7.2"),
 ("book6/wp122",              205, ["7.3"],
  "section 7.3, Poincare-Bendixson"),
 ("book6/wp122",              206, ["Example 7.3.1", "trapping region", "Bendixson"],
  "Example 7.3.1, the trapping annulus"),
 ("book7/ch-strogatz",        251, ["8.1", "8.2"],
  "Chapter 8 bifurcations revisited begins"),
 ("book7/ch-strogatz",        254, ["Rules of Thumb",
                                    "grows continuously from zero",
                                    "The frequency of the limit cycle"],
  "HEADING IS PLURAL: 'Rules of Thumb'. Rule 1 = amplitude, rule 2 = frequency"),
 ("book7/ch-strogatz",        256, ["degenerate Hopf bifurcation",
                                    "no limit cycles on either side",
                                    "continuous band of closed orbits",
                                    "nonlinear center"],
  "the degenerate case, damped pendulum"),
 ("book6/wp122",              281, ["8.7"],
  "section 8.7, Poincare maps"),
 ("book6/wp122",              282, ["EXAMPLE 8.7.1", "Exercise 8.7.1"],
  "Example 8.7.1 -- and the integral is deferred to EXERCISE 8.7.1"),
 ("book6/wp122",              373, ["10.5", "Liapunov"],
  "section 10.5, Liapunov exponent"),
 ("book6/wp122",              374, ["EXAMPLE 10.5.1", "stable p-cycle"],
  "Example 10.5.1, exponent of a p-cycle"),

 # ---- added 2026-09-17: the chapters written after this script existed. Their
 # ---- Strogatz page numbers were remembered, not checked, until this run.
 ("book7/ch-van-der-pol + ch-smale", 10, ["Figure 1.3.1", "RC circuit",
                                          "Radioactive decay", "Pendulum",
                                          "Strange attractors"],
  "Figure 1.3.1, the map of the subject -- and the cells both chapters quote"),
 ("book7/ch-van-der-pol",     200, ["EXAMPLE 7.1.2", "limit cycle"],
  "Example 7.1.2, the van der Pol oscillator, one page after 7.1.1"),
 ("book7/ch-van-der-pol",     212, ["7.4", "Liénard",
                                    "No Chaos in the Phase Plane"],
  "section 7.4 OPENS here with Lienard's equation -- but not the theorem"),
 ("book7/ch-van-der-pol",     213, ["EXAMPLE 7.4.1", "Liénard",
                                    "unique, stable limit cycle",
                                    "RELAXATION OSCILLATIONS"],
  "Lienard's THEOREM and its five conditions are on 213, not 212; 7.5 opens here too"),
 ("book7/ch-van-der-pol",     212, ["early days of nonlinear dynamics",
                                    "radio and vacuum tube",
                                    "mathematical life"],
  "the pull-quote the chapter prints -- a direct quotation is the strongest claim"),
 ("book7/ch-euler + ch-conley", 179, ["6.8", "INDEX THEORY", "6.8.1"],
  "section 6.8, index theory for closed curves"),
 ("book7/ch-euler",           180, ["Theorem 6.8.2",
                                    "enclose fixed points whose indices sum to"],
  "Theorem 6.8.2 is on 180 -- the statement ch-euler checks numerically"),
]

def read_page_number(t):
    """Read the printed page number off the top of a page.

    Not as simple as a leading integer. On recto pages the running head is set
    tight against the number -- "2818.7 POINCARE MAPS" is page 281, section 8.7
    -- so a naive \\d{1,3}\\b finds nothing there and a naive \\d+ finds 2818.
    Split the digit run so that what follows begins a section number.
    """
    m = re.match(r"\s*(\d+)", t)
    if not m:
        return None
    digits, rest = m.group(1), t[m.end():]
    for k in (3, 2, 1):
        if len(digits) < k:
            continue
        n = int(digits[:k])
        if not 1 <= n <= 600:
            continue
        if len(digits) == k:          # number stands alone
            return n
        if re.match(r"^\d*\.\d", digits[k:] + rest):   # remainder is "8.7", "10.5"
            return n
    return None


def main():
    if len(sys.argv) != 2:
        print(__doc__); return 2
    try:
        import pypdf
    except ImportError:
        print("needs pypdf:  pip install pypdf"); return 2
    reader = pypdf.PdfReader(sys.argv[1])
    printed, text = {}, {}
    for i, page in enumerate(reader.pages):
        try: t = page.extract_text() or ""
        except Exception: t = ""
        text[i] = re.sub(r"\s+", " ", t)
        n = read_page_number(text[i])
        # A page of front matter, or a figure caption that happens to open with
        # digits, can yield a number that is not a page number. The printed page
        # can only lag its pdf index by the front matter, never lead it, and the
        # front matter here is tens of pages -- so bound the gap and the stray
        # reads drop out without a hand-kept exception list.
        if n is not None and 0 <= i - n <= FRONT_MATTER_MAX and n not in printed:
            printed[n] = i

    print(f"  {EDITION}")
    print(f"  {len(reader.pages)} pdf pages, {len(printed)} printed pages located "
          f"(pypdf {pypdf.__version__} -- the count depends on the extractor)")
    offs = sorted({i - n for n, i in printed.items()})
    print(f"  pdf-index minus printed-page takes {len(offs)} distinct values "
          f"({min(offs)}..{max(offs)}) -- which is why no offset is assumed\n")

    bad = 0
    for who, page, needles, note in CLAIMS:
        idx = printed.get(page)
        if idx is None:
            print(f"  FAIL  p.{page:<4} printed page not found"); bad += 1; continue
        body = text[idx].lower()
        missing = [s for s in needles if s.lower() not in body]
        if missing:
            print(f"  FAIL  p.{page:<4} {who}")
            for s in missing: print(f"          not on the page: {s!r}")
            bad += 1
        else:
            print(f"  ok    p.{page:<4} {who:26s} {note}")

    print()
    if bad:
        print(f"  {bad} of {len(CLAIMS)} citations do not check out."); return 1
    print(f"  all {len(CLAIMS)} citations check out against {EDITION}.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
