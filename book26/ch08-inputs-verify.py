#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Pablo Nogueira Grossi / G6 LLC
"""
book26/ch08-inputs-verify.py -- checklist item C8: reconcile the stated inputs.

The abstract and p.12 say the electroweak VEV is the one empirical input. Table 16
(p.216) lists that same VEV, with c, hbar, e, alpha and G, under Predictions. This
reads both pages out of the source and checks that each says what C8 reports.
It does not judge the physics; it checks the paper against itself.

Source not in hand -> SKIP, never PASS (CLAUDE.md). Paper found by content in
~/Downloads and pinned by digest, not by filename.
"""
import hashlib, os, re, shutil, subprocess, sys
from pathlib import Path

PAPER_MD5 = "b7ae1a50d535d15027cdd5336d5e7f22"
PAPER_MARKS = ("Nielsen", "complex Hopf fibration")
FAIL = []

def check(label, ok, detail=""):
    print(("PASS " if ok else "FAIL ") + label + (f"  -- {detail}" if detail else ""))
    if not ok: FAIL.append(label)

def norm(s): return re.sub(r"\s+", " ", s)

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
        if all(m in head for m in PAPER_MARKS): return f, hashlib.md5(f.read_bytes()).hexdigest()
    return None, "preprint not found in " + str(d)

def page(path, n):
    return norm(subprocess.run(["pdftotext","-f",str(n),"-l",str(n),str(path),"-"],
                               capture_output=True, text=True, timeout=60).stdout)

# What each page must say for C8's report to be accurate.
P11 = ["Input (v)", "α = 1/137.036", "Derived"]
P12 = ["The only dimensionful input is the electroweak VEV, v = 246 220 MeV (Axiom 1)",
       "This input is a unit conversion, not a physical parameter",
       "no fitting routine, no optimization loop, and no adjustable coefficient",
       "No dimensionless number was adjusted after the fact"]
P216 = ["Table 16: Inputs, calibration targets, and predictions",
        "GR; c, ℏ, e, α, G, v;",
        "Fixed by Hopf geometry",
        "v/R fixed once across sectors",
        "Numerically fixed; no fits"]

def main():
    paper, info = find_paper()
    if paper is None:
        print("SKIP source paper: " + info); print("SKIP every check below. C8 is UNCHECKED here.")
        sys.exit(0)
    check("source paper found and is the audited copy", info == PAPER_MD5, paper.name)
    if info != PAPER_MD5:
        print("\nFAILED: wrong document"); sys.exit(1)

    p11, p12, p216 = page(paper,11), page(paper,12), page(paper,216)
    for lbl, pg, want in (("p.11 summary table", p11, P11),
                          ("p.12 zero-free-parameters proof", p12, P12),
                          ("p.216 Table 16", p216, P216)):
        miss = [q for q in want if q not in pg]
        check(lbl + " says what C8 reports", not miss, "missing: " + " | ".join(miss) if miss else "")

    # The contradiction, stated as two membership facts about one symbol.
    v_is_input      = "The only dimensionful input is the electroweak VEV" in p12
    v_in_predictions = bool(re.search(r"Predictions.{0,400}GR; c, ℏ, e, α, G, v;", p216))
    check("v is called the only input on p.12", v_is_input)
    check("v is listed among the predictions in Table 16", v_in_predictions)
    check("C8 holds: one symbol is both the sole input and a prediction",
          v_is_input and v_in_predictions)

    # A calibration step inside a paper that says it contains no fits.
    check("Table 16's own method fixes a ratio by matching",
          "v/R fixed once across sectors" in p216,
          "p.216 item 2, against p.12 'no fitting routine ... no adjustable coefficient'")

    print()
    ctl = []
    def control(name, ok_when_damaged):
        print(("PASS " if not ok_when_damaged else "FAIL ") + "control rejected: " + name)
        if ok_when_damaged: ctl.append(name)
    control("a quote dropped from p.12", not [q for q in P12 if q not in p12.replace("Axiom 1", "")])
    control("Table 16 predictions row altered",
            bool(re.search(r"Predictions.{0,400}GR; c, ℏ, e, α, G, v;",
                           p216.replace("GR; c, ℏ, e, α, G, v;", "GR only;"))))
    control("contradiction test satisfied with one side false", (False and v_in_predictions))

    print()
    print("[HONESTY] This shows the paper labels one quantity both ways on two pages. It does")
    print("          NOT establish that v cannot be derived, that the theory is wrong, or that")
    print("          Theorem 68 (G) and Theorem 66 (alpha) fail - neither was read.")

    if FAIL or ctl:
        print(f"\nFAILED: {len(FAIL)} check(s), {len(ctl)} control(s) not rejected"); sys.exit(1)
    print("\nALL PASS")

if __name__ == "__main__":
    main()
