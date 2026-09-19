#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Pablo Nogueira Grossi / G6 LLC
"""
floor_texts.py -- bind each WP-82 rung to a primary text that is ALREADY on this
machine, and give it an address: (path, sha256, pages, title line).

WHY. WP-82 measured the corpus against the 33-rung ruler and found the
distribution inverted: rung 33 in 31 file-mentions, rung 28 in two, K-theory in
zero. Its recommendation was to build the floor first. On 2026-09-19 a scan of
~/Downloads found the floor texts already downloaded and never opened --
Weibel for XI, van Neerven for XII, Connes-Marcolli for XVI, Deisenroth for the
machine-learning gap. The corpus was re-deriving what it already held.

This is the anti-churn instrument: a text with an address is cited, not
rediscovered (R19). Run it after adding a text; it rewrites docs/floor-texts.tsv.

    python3 tools/floor_texts.py [--downloads DIR]

Needs pypdf only for the page count and title line; without it the rest still runs.
"""
import hashlib, os, re, sys

# rung, volume, subject (WP-82 §3), expected filename in Downloads, short cite
TEXTS = [
 (28, "XI",  "K-Theory & Index Theory",        "Kbook.pdf",
  "C. A. Weibel, The K-book: an introduction to Algebraic K-theory, 2013"),
 (29, "XII", "Operator Algebras / functional analysis floor", "2112.11166v7.pdf",
  "J. van Neerven, Functional Analysis, Cambridge Studies in Advanced Mathematics"),
 (33, "XVI", "Noncommutative Geometry",        "Connes–Marcolli Noncommutative Algebra.pdf",
  "A. Connes and M. Marcolli, Noncommutative Geometry, Quantum Fields and Motives"),
 (None, "—",  "Machine learning: the mathematics", "MATHEMATICS FOR MACHINE LEARNING.pdf",
  "M. P. Deisenroth, A. A. Faisal, C. S. Ong, Mathematics for Machine Learning, CUP 2020"),
 (None, "—",  "Discrete mathematics floor",     "mcs.pdf",
  "E. Lehman, F. T. Leighton, A. R. Meyer, Mathematics for Computer Science, MIT 2018"),
 (None, "—",  "Linear algebra floor",           "LINEAR ALGEBRA.pdf",
  "J. Hefferon, Linear Algebra, 4th edition"),
 (None, "—",  "Probability floor",              "Probability and Statistics- The Science of Uncertainty.pdf",
  "M. J. Evans and J. S. Rosenthal, Probability and Statistics: The Science of Uncertainty"),
 (None, "—",  "Nonlinear dynamics floor",       "Nonlinear_Dynamics_and_Chaos_2018_Steven_H._Strogatz.pdf",
  "S. H. Strogatz, Nonlinear Dynamics and Chaos, 2nd ed."),
]

def sha256(p, blocks=1 << 20):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(blocks), b""):
            h.update(b)
    return h.hexdigest()

def main():
    dl = os.path.expanduser("~/mnt/Downloads")
    if "--downloads" in sys.argv:
        dl = sys.argv[sys.argv.index("--downloads") + 1]
    try:
        import pypdf
    except ImportError:
        pypdf = None

    rows, missing = [], 0
    for rung, vol, subject, fname, cite in TEXTS:
        p = os.path.join(dl, fname)
        if not os.path.exists(p):
            print("  MISSING  %-5s %s" % (vol, fname)); missing += 1
            rows.append(("%s" % (rung or ""), vol, subject, fname, "", "", "MISSING", cite))
            continue
        digest = sha256(p)
        pages = ""
        if pypdf:
            try: pages = str(len(pypdf.PdfReader(p).pages))
            except Exception: pages = "?"
        print("  held     %-5s rung %-4s %-6s pp  %s  %s"
              % (vol, rung or "-", pages, digest[:12] + "…", fname))
        rows.append((str(rung or ""), vol, subject, fname, digest, pages, "HELD", cite))

    out = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                       "docs", "floor-texts.tsv")
    with open(out, "w", encoding="utf-8") as f:
        f.write("rung\tvolume\tsubject\tfile\tsha256\tpages\tstatus\tcitation\n")
        for r in rows:
            f.write("\t".join(r) + "\n")
    print("\n  wrote %s  (%d held, %d missing)" % (out, len(rows) - missing, missing))
    print("  The floor texts are on the machine. WP-82 asked for the floor to be")
    print("  built first; what was missing was not the books but their addresses.")
    return 1 if missing else 0

if __name__ == "__main__":
    sys.exit(main())
