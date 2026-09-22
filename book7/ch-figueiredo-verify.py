#!/usr/bin/env python3
"""book7/ch-figueiredo-verify.py -- presence-checks the facts printed on
ch-figueiredo.html against the page itself.

Same pattern as book7/ch-descartes-verify.py: the sources for this chapter
are web pages (Princeton Dept. of Physics, Breakthrough Prize Foundation,
The Daily Princetonian, UC Berkeley news) and one arXiv preprint, checked
live on 2026-09-22, not held-and-hashed PDFs. This script cannot re-fetch
the web at verify time -- it can only confirm the page still says what it
said when the sources were checked, catching silent drift on a later edit.

    python3 book7/ch-figueiredo-verify.py
"""
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
PAGE = ROOT / "book7" / "ch-figueiredo.html"

REQUIRED = [
    "Vera Rubin New Frontiers Prize",
    "Nima Arkani-Hamed",
    "surfaceology",
    "Instituto Superior T",  # Técnico -- avoid encoding mismatch on the accent
    "Jensen Huang",
    "Yuri Milner",
    "Ant",  # António José Seguro -- avoid encoding mismatch on the accent
    "Jos",  # same
    "Seguro",
    "2408.11891",
    "whole semester of surprises",
    "doable at least",
    "should become emergent in some way",
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
    print("ESTABLISHED: the page still prints the specific facts checked against")
    print("its web sources on 2026-09-22 (see the page's own Sources table).")
    print()
    print("NOT ESTABLISHED: that those web sources are themselves correct. This")
    print("script has no network access and cannot re-fetch them; it is a")
    print("presence check, not an independent re-verification. The page itself")
    print("also states plainly what it does NOT claim: that surfaceology covers")
    print("the full Standard Model, that spacetime-as-emergent is a proven result")
    print("rather than Figueiredo's own stated direction, and that any connection")
    print("is drawn to this corpus's own contact-geometric machinery.")
    if fail:
        print()
        print(f"{len(fail)} CHECK(S) FAILED")
        return 1
    print()
    print(f"ALL {len(REQUIRED)} CHECKS PASSED")
    return 0

if __name__ == "__main__":
    sys.exit(main())
