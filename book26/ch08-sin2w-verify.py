#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Pablo Nogueira Grossi / G6 LLC
"""
book26/ch08-sin2w-verify.py -- checklist item C5: is sin^2(theta_W) = 3/(4pi) derived or fitted?

The paper's eq. (100), p.123, sets sin^2(theta_W)^top = dim SU(2) / int_{CP^1} K dA = 3/(4pi).
This script reads that page out of the source preprint and recomputes every number the
argument rests on, from the paper's own inputs. It does not judge the physics; it checks
whether the paper is consistent with itself.

Source not in hand -> SKIP, never PASS (CLAUDE.md). The preprint is third-party and is not
in the repo; it is found in ~/Downloads by content and pinned by digest, not by filename.
"""
import hashlib, math, os, re, shutil, subprocess, sys
from pathlib import Path

PAPER_MD5 = "b7ae1a50d535d15027cdd5336d5e7f22"      # 247 pp, 9,389,556 bytes, 2026-08-14
PAPER_MARKS = ("Nielsen", "complex Hopf fibration")
PAGE = 123
FAIL = []

def check(label, ok, detail=""):
    print(("PASS " if ok else "FAIL ") + label + (f"  -- {detail}" if detail else ""))
    if not ok: FAIL.append(label)

def find_paper():
    d = Path(os.environ.get("NIELSEN_PDF_DIR", Path.home() / "Downloads"))
    if not d.is_dir(): return None, "no source directory"
    if not shutil.which("pdftotext"): return None, "pdftotext not installed"
    for f in sorted(d.glob("*.pdf")):
        if f.stat().st_size < 1_000_000: continue
        try:
            head = subprocess.run(["pdftotext","-f","1","-l","1",str(f),"-"],
                                  capture_output=True, text=True, timeout=60).stdout
        except Exception: continue
        if all(m in head for m in PAPER_MARKS):
            return f, hashlib.md5(f.read_bytes()).hexdigest()
    return None, "preprint not found in " + str(d)

def page_text(path, n):
    return subprocess.run(["pdftotext","-f",str(n),"-l",str(n),str(path),"-"],
                          capture_output=True, text=True, timeout=60).stdout

# --- what p.123 must contain for the rest of this script to be about that argument ---
QUOTES = [
    "sin2 θW = g ′ 2 /(g 2 + g ′ 2 )",          # the paper's own definition
    "carried by the SU (2) sector",                           # the prose identification
    "dim SU (2)",                                             # the numerator
    "K dA = 4π",                                         # Gauss-Bonnet denominator
    "0.23873",
    "sin2 θW (0) = 0.23867 ± 0.00016",              # the value it is compared to
    "0.23122 ± 0.00006",                                 # the value at M_Z
    "= 0.22320",                                              # its own on-shell number
]

def arithmetic():
    """Recompute from the paper's own inputs. Returns dict of (computed, printed)."""
    pi = math.pi
    mW, mZ = 80369.5, 91187.8                 # p.123 Table 6, MeV
    onshell = 1 - (mW/mZ)**2
    topo    = 3/(4*pi)
    return {
        "3/(4pi) equals the printed 0.23873":        (round(topo,5), 0.23873),
        "on-shell from its own masses is 0.22320":   (round(onshell,5), 0.22320),
        "pull vs Thomson value rounds to 0.4 sigma": (round(abs(topo-0.23867)/0.00016,1), 0.4),
    }

def main():
    paper, info = find_paper()
    if paper is None:
        print("SKIP source paper: " + info)
        print("SKIP every check below. C5 is UNCHECKED on this machine.")
        sys.exit(0)

    check("source paper found and is the audited copy", info == PAPER_MD5,
          paper.name if info == PAPER_MD5 else "digest %s != %s" % (info[:12], PAPER_MD5[:12]))
    if info != PAPER_MD5:
        print("\nFAILED: wrong document"); sys.exit(1)

    t = page_text(paper, PAGE)
    missing = [q for q in QUOTES if q not in t]
    check("p.123 carries the eq.(100) argument as quoted", not missing,
          "missing: " + " | ".join(missing) if missing else "")

    for label, (got, printed) in arithmetic().items():
        check(label, got == printed, f"computed {got}, paper prints {printed}")

    # The finding. Two derived values of one symbol, in one paper, both called successes.
    topo, onshell = 3/(4*math.pi), 1 - (80369.5/91187.8)**2
    gap = topo - onshell
    check("the two derived values of sin^2(theta_W) differ by more than 5%",
          abs(gap)/onshell > 0.05, f"{100*abs(gap)/onshell:.2f}% ({abs(gap)/0.00016:.0f} Thomson sigma)")

    # R24 controls: each check must be able to fail.
    print()
    ctl = []
    def control(name, ok_when_damaged):
        print(("PASS " if not ok_when_damaged else "FAIL ") + "control rejected: " + name)
        if ok_when_damaged: ctl.append(name)
    control("a quote removed from the page text",
            not [q for q in QUOTES if q not in t.replace("0.23873", "")])
    control("3/(4pi) compared against a wrong printed value", round(3/(4*math.pi),5) == 0.23900)
    control("on-shell recomputed from wrong masses", round(1-(80369.5/91187.8)**2,5) == 0.23873)
    control("gap test satisfied by two equal values", abs(topo-topo)/topo > 0.05)

    print()
    print("[HONESTY] This checks the paper against itself: that p.123 says what is quoted and")
    print("          that its printed numbers follow from its printed inputs. It does NOT")
    print("          establish that 3/(4pi) is wrong physics, that the Standard Model value is")
    print("          right, or that no derivation of this ratio could exist. What it shows is")
    print("          internal: one symbol is given two derived values 6.96% apart and each is")
    print("          compared to whichever PDG scheme value it matches.")

    if FAIL or ctl:
        print(f"\nFAILED: {len(FAIL)} check(s), {len(ctl)} control(s) not rejected"); sys.exit(1)
    print("\nALL PASS")

if __name__ == "__main__":
    main()
