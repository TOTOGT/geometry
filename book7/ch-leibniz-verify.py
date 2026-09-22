#!/usr/bin/env python3
"""book7/ch-leibniz-verify.py -- presence-checks the historical facts printed
on ch-leibniz.html against the page itself. Same limitation as
ch-descartes-verify.py: web-sourced facts, no network at verify time, so this
is a presence check against the page's own text, not a live re-verification.

    python3 book7/ch-leibniz-verify.py
"""
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
PAGE = ROOT / "book7" / "ch-leibniz.html"

REQUIRED = [
    "29 October 1675",
    "Analyseos tetragonisticae pars secunda",
    "11 November 1675",
    "Methodi tangentium inversae exempla",
    "Nova Methodus pro Maximis et Minimis",
    "1684",
    "dy ad dx",
    "June 1686",
]

def main():
    fail = []
    if not PAGE.exists():
        print("FAIL missing page:", PAGE)
        return 1
    text = PAGE.read_text(encoding="utf-8")
    norm = re.sub(r"\s+", " ", text)
    for s in REQUIRED:
        ok = s in norm
        print(("PASS " if ok else "FAIL ") + repr(s))
        if not ok:
            fail.append(s)
    print()
    print("=" * 60)
    print("[HONESTY]")
    print()
    print("ESTABLISHED: the page still prints the specific dates and quoted")
    print("manuscript/paper titles checked against its web sources on")
    print("2026-09-22 (see the page's own Sources table).")
    print()
    print("NOT ESTABLISHED: that those web sources are themselves correct, or")
    print("that Part III's claim about why continental mathematics moved")
    print("faster on multivariable calculus is independently verified -- the")
    print("page itself marks that OPEN. This script has no network access and")
    print("cannot re-fetch the sources; it is a presence check, not a")
    print("re-verification.")
    if fail:
        print()
        print(f"{len(fail)} CHECK(S) FAILED")
        return 1
    print()
    print(f"ALL {len(REQUIRED)} CHECKS PASSED")
    return 0

if __name__ == "__main__":
    sys.exit(main())
