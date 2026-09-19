#!/usr/bin/env python3
"""Locate Strogatz §5.2's page numbers in the actual file, do not recite them.

Usage:  python3 book21/spiral-pages-verify.py [path-to-strogatz.pdf]

book21/Spiral.lean cites Strogatz for the classification of planar linear
systems. A citation in this corpus has to resolve at the path it names, so
this script opens the PDF, finds the pages, and fails if they have moved.

It checks four things:

  1. the file's sha256 matches the one docs/floor-texts.tsv recorded;
  2. the table of contents puts 5.1 and 5.3 where the cited range implies;
  3. the discriminant really does appear on the printed pages the Lean header
     names;
  4. Figure 5.2.8 -- the classification diagram -- is on the page named.

Point 4 is the one most likely to rot. A different printing moves figure
numbers, and a header that says 5.2.8 while the reader's copy says 5.2.7 is a
broken address, not a rounding error. If this fails on your copy, the corpus
has cited an edition you do not hold, and that is a finding rather than an
inconvenience.

One thing this script deliberately does NOT do: claim the phrase "the
trace-determinant plane" is Strogatz's. It is not in this printing. He gives
the diagram without naming the plane.
"""
import hashlib
import os
import re
import subprocess
import sys

DEFAULT = os.path.expanduser(
    "~/mnt/Downloads/Nonlinear_Dynamics_and_Chaos_2018_Steven_H._Strogatz.pdf")

SHA = "e4c3681c828fd301dfd5449c5d777fc5c24eff9cbf9cfdc1a51d54cfd3800c08"
PAGES = 532
WANT_DISCRIMINANT = [132, 135]
WANT_FIGURE = 138
TOC = {"5.1 Definitions and Examples": 125, "5.3 Love Affairs": 139}


def text(path, first, last):
    r = subprocess.run(["pdftotext", "-f", str(first), "-l", str(last), path, "-"],
                       capture_output=True, text=True)
    if r.returncode != 0:
        raise SystemExit(f"::error::pdftotext failed: {r.stderr.strip()[:200]}")
    return r.stdout


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else DEFAULT
    fail = []

    if not os.path.exists(path):
        print(f"::error::{path} not found — pass the path to your copy")
        return 1

    got = hashlib.sha256(open(path, "rb").read()).hexdigest()
    if got != SHA:
        print(f"::error::sha256 {got[:16]}… is not the recorded {SHA[:16]}…")
        print("  This is a different file. Every page number below describes a "
              "copy you do not have; stop and re-locate them.")
        return 1

    flat_toc = " ".join(text(path, 1, 40).split())
    for entry, page in TOC.items():
        if f"{entry} {page}" not in flat_toc:
            fail.append(f"table of contents does not read {entry!r} at p. {page}")

    found_disc, found_fig = [], None
    for pg in text(path, 140, 160).split("\f"):
        nums = [int(n) for n in re.findall(r"^\s*(\d{2,4})\s*$", pg, re.M)]
        if not nums:
            continue
        p, flat = nums[0], " ".join(pg.split())
        if "τ 2 − 4Δ" in flat or "τ2 − 4Δ" in flat:
            found_disc.append(p)
        if "Figure 5.2.8" in flat and found_fig is None:
            found_fig = p

    for p in WANT_DISCRIMINANT:
        if p not in found_disc:
            fail.append(f"the discriminant is not on printed p. {p} "
                        f"(found on {found_disc})")
    if found_fig != WANT_FIGURE:
        fail.append(f"Figure 5.2.8 is on printed p. {found_fig}, not {WANT_FIGURE}")

    for f in fail:
        print(f"::error::{f}")
    if fail:
        return 1
    print("  ok  §5.2 Classification of Linear Systems, printed pp. 129–138")
    print(f"  ok  discriminant on printed pp. {found_disc}")
    print(f"  ok  Figure 5.2.8 (the classification diagram) on printed p. {found_fig}")
    print(f"  ok  sha256 {SHA[:12]}…, {PAGES} pages")
    print("every page this corpus cites was located in the file, not recalled.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
