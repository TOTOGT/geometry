#!/usr/bin/env python3
"""book7/ch-descartes-verify.py -- presence-checks the historical facts printed
on ch-descartes.html against the page itself.

This is a WEAKER verification than the corpus's usual PDF-hash pattern: the
sources for this chapter are web pages (Wikipedia, a Rutgers course history
note), checked live on 2026-09-22, not held-and-hashed PDFs. Standard-library
scripts cannot re-fetch the web at verify time, so this script cannot
re-confirm the sources -- it can only confirm the page still says what it said
when the sources were checked, catching silent drift on a later edit.

    python3 book7/ch-descartes-verify.py
"""
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
PAGE = ROOT / "book7" / "ch-descartes.html"

REQUIRED = [
    "a single reference line",
    "Frans van Schooten",
    "1649",
    "Johan de Witt",
    "Johannes Hudde",
    "Hendrik van Heuraet",
    "Nicole Oresme",
    "Ad Locos Planos et Solidos Isagoge",
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
    print("presence check, not an independent re-verification.")
    if fail:
        print()
        print(f"{len(fail)} CHECK(S) FAILED")
        return 1
    print()
    print(f"ALL {len(REQUIRED)} CHECKS PASSED")
    return 0

if __name__ == "__main__":
    sys.exit(main())
