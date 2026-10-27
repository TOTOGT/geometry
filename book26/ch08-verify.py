#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Pablo Nogueira Grossi / G6 LLC
"""
book26/ch08-verify.py -- book26/ch08-a-preprint-against-a-kernel.html.
  [1] sections S1..S6   [2] labels   [3] the checklist: twelve items, seven done (C1-C4, C8, C9, C12) and five open, in the page's own markup
  [4] the evidence behind each checked box exists: audit report with 7 theorem lines and only permitted axioms; census with 140 rows
  [5] no employer or personal names beyond the cited title; controls    [HONESTY] what this does not establish
"""
import re, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
PAGE = HERE / "ch08-a-preprint-against-a-kernel.html"
AUDIT = sorted((ROOT / "tools" / "verify-audit").glob("*/geometry__book26__NielsenKernels.axioms.txt"))
AUDIT2 = sorted((ROOT / "tools" / "verify-audit").glob("*/geometry__book26__NielsenAbstractArithmetic.axioms.txt"))
AUDIT3 = sorted((ROOT / "tools" / "verify-audit").glob("*/geometry__book26__NielsenLeptonDeviation.axioms.txt"))
CENSUS = HERE / "nielsen-census.tsv"

# --- the source paper -------------------------------------------------------
# CLAUDE.md: source in hand -> check the claim against it; source not in hand ->
# the script prints SKIP, never PASS, and the log says UNCHECKED. The paper is not
# in the repo (third-party, 9.4 MB); it is read from ~/Downloads where the author
# keeps sources. Identified by content and pinned by digest, not by filename --
# the file arrived named with a UUID and a rename must not silently change what
# was audited.
import hashlib, os, shutil, subprocess
PAPER_MD5 = "b7ae1a50d535d15027cdd5336d5e7f22"   # 247 pp, 9,389,556 bytes, 2026-08-14
PAPER_MARKS = ("Nielsen", "complex Hopf fibration")
def find_paper():
    """Return (path, md5) of the preprint, or (None, reason)."""
    d = Path(os.environ.get("NIELSEN_PDF_DIR", Path.home() / "Downloads"))
    if not d.is_dir(): return None, "no source directory"
    if not shutil.which("pdftotext"): return None, "pdftotext not installed"
    for f in sorted(d.glob("*.pdf")):
        try:
            if f.stat().st_size < 1_000_000: continue
            head = subprocess.run(["pdftotext", "-f", "1", "-l", "1", str(f), "-"],
                                  capture_output=True, text=True, timeout=60).stdout
        except Exception:
            continue
        if all(m in head for m in PAPER_MARKS):
            return f, hashlib.md5(f.read_bytes()).hexdigest()
    return None, "preprint not found in " + str(d)

# Strings this chapter attributes to the paper. If the page says the abstract
# claims the masses are within PDG uncertainties, the abstract must say so.
PAPER_CLAIMS = ["within PDG", "sin2 \u03b8W = 3/(4\u03c0) = 0.23873",
                "246 220 MeV", "mW = 80.3695 GeV", "mZ = 91.1878 GeV", "mH = 125.225 GeV"]
def paper_page1(path):
    return subprocess.run(["pdftotext", "-f", "1", "-l", "1", str(path), "-"],
                          capture_output=True, text=True, timeout=60).stdout

FAIL = []
def check(label, ok, detail=""):
    print(("PASS " if ok else "FAIL ") + label + (f"  -- {detail}" if detail else ""))
    if not ok: FAIL.append(label)
def plain(t):
    t = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", t, flags=re.S)
    t = re.sub(r"<[^>]+>", " ", t)
    for a, b in (("&rsquo;", "'"), ("&ldquo;", '"'), ("&rdquo;", '"'), ("&amp;", "&"), ("&mdash;", "-"), ("&ndash;", "-"), ("&middot;", "."), ("&nbsp;", " "), ("&thinsp;", " "), ("&hbar;", "h"), ("&prime;", "'"), ("&radic;", "sqrt"), ("&minus;", "-")):
        t = t.replace(a, b)
    return re.sub(r"\s+", " ", t)
SECS = ["S1", "S2", "S3", "S4", "S5", "S6"]
LABELS = ["four of the fifteen checklist items below are open", "a hand derivation", "this is an estimate", "not a verdict", "not established here", "keyword matching"]
BANNED = ["citadel", "north bridge", "uerj", "zilacleide"]
FORBIDDEN = ["fetch(", "XMLHttpRequest", "localStorage", "<form", "action=", "<script"]
IDS = ["C%d" % i for i in range(1, 16)]
DONE = {"C1", "C2", "C3", "C4", "C8", "C9", "C12", "C13", "C11", "C14", "C15"}
def method_ok(t): return re.findall(r'<li data-m="(M\d)">', t) == ["M%d" % i for i in range(1, 7)]
def secs_ok(t): return re.findall(r'<div class="sec" data-n="([^"]+)">', t) == SECS
def labels_ok(t):
    p = plain(t).lower(); return all(l in p for l in LABELS)
def names_ok(t): return not any(b in t.lower() for b in BANNED) and not any(f in t for f in FORBIDDEN)
def items(t): return re.findall(r'<li data-c="(C\d+)" data-s="(done|open)"[^>]*><input type="checkbox" disabled( checked)?', t)
def checklist_ok(t):
    it = items(t)
    if [i[0] for i in it] != IDS: return False
    for cid, st, ck in it:
        if (st == "done") != (cid in DONE): return False
        if bool(ck) != (st == "done"): return False   # markup agrees with status
    return True
def audit_ok():
    if not AUDIT: return False
    lines = [l for l in AUDIT[-1].read_text().splitlines() if l.strip()]
    if len(lines) != 7: return False
    allowed = {"propext", "Quot.sound", "Classical.choice"}
    for l in lines:
        if "does not depend on any axioms" in l: continue
        m = re.search(r"depends on axioms: \[(.*)\]", l)
        if not m or not {x.strip() for x in m.group(1).split(",")} <= allowed: return False
    return True
def audit2_ok():
    if not AUDIT2: return False
    lines = [l for l in AUDIT2[-1].read_text().splitlines() if l.strip()]
    allowed = {"propext", "Quot.sound", "Classical.choice"}
    if len(lines) != 6: return False
    for l in lines:
        if "does not depend on any axioms" in l: continue
        m = re.search(r"depends on axioms: \[(.*)\]", l)
        if not m or not {x.strip() for x in m.group(1).split(",")} <= allowed: return False
    return True
def audit3_ok():
    # NielsenLeptonDeviation.lean, run 2026-10-26 (363 s). Three declarations.
    # R20: a clean axiom report is not a reading of the statement. This checks the
    # receipt's shape, not that the theorems say what their names say.
    if not AUDIT3: return False
    lines = [l for l in AUDIT3[-1].read_text().splitlines() if l.strip()]
    allowed = {"propext", "Quot.sound", "Classical.choice"}
    if len(lines) != 3: return False
    for l in lines:
        if "does not depend on any axioms" in l: continue
        m = re.search(r"depends on axioms: \[(.*)\]", l)
        if not m or not {x.strip() for x in m.group(1).split(",")} <= allowed: return False
    return True
def census_ok():
    if not CENSUS.exists(): return False
    return len(CENSUS.read_text(encoding="utf-8").splitlines()) - 1 == 140
def main():
    t = PAGE.read_text(encoding="utf-8") if PAGE.exists() else ""
    check("page exists", bool(t))
    if not t:
        print("\nFAILED: page absent"); sys.exit(1)
    check("sections S1..S6 in order", secs_ok(t))
    check("required labels present", labels_ok(t))
    check("method points M1..M6 present in order", method_ok(t))
    check("no private names, scripts, forms or network", names_ok(t))
    check("checklist: C1..C15, eleven done (C1-C4, C8, C9, C11-C15), four open, markup agrees with status", checklist_ok(t))
    check("the table script behind C12 exists", (HERE / "nielsen-lepton-table.py").exists())
    check("audit report exists: 7 theorem lines, axioms within the permitted set", audit_ok())
    check("second audit report (abstract arithmetic) exists: 6 theorem lines, permitted axioms", audit2_ok())
    check("third audit report (lepton deviation) exists: 3 theorem lines, permitted axioms", audit3_ok())
    check("the page no longer says the lepton Lean file is unrun", "and not yet run" not in plain(t))
    check("C11 names the lambda_T expressions and the appendix contradiction",
          all(x in plain(t) for x in ("2/(3", "sign flip", "zeta'(-2) = -z3/(4*pi**2)")))
    check("C15 names the four multipliers and the anchor",
          all(x in plain(t) for x in ("1/12", "0.002012", "0.00% (anchor)")))
    check("C14 names the ratio factors and the p.12 argument",
          all(x in plain(t) for x in ("33.6", "350", "leaves invariant every mass ratio")))
    check("C13 names the coefficient, the n=1 closed form and the consequence",
          all(x in plain(t) for x in ("0.030448", "1.776980152292558942", "0.913", "4/3")))
    check("C8 names both labellings of v", all(x in plain(t) for x in ("Axiom 1", "Table 16", "v/R fixed once across sectors")))
    check("C9 names both derived values and the gap",
          all(x in plain(t) for x in ("0.238732", "0.223200", "6.96%", "97")))
    check("census has 140 rows", census_ok())

    # Source check. SKIP, never PASS, when the paper is not in hand.
    paper, info = find_paper()
    if paper is None:
        print("SKIP source paper: " + info + "  -- claims about the preprint are UNCHECKED here")
    else:
        same = (info == PAPER_MD5)
        check("source paper found and is the audited copy", same,
              paper.name if same else "digest %s != audited %s" % (info[:12], PAPER_MD5[:12]))
        if same:
            pg1 = paper_page1(paper)
            missing = [c for c in PAPER_CLAIMS if c not in pg1]
            check("the abstract says what this chapter says it says", not missing,
                  "missing: " + "; ".join(missing) if missing else "")

    ctl = []
    def control(name, damaged, fn):
        ok = fn(damaged); print(("PASS " if not ok else "FAIL ") + "control rejected: " + name)
        if ok: ctl.append(name)
    control("section removed", t.replace('data-n="S3"', 'data-n="X"'), secs_ok)
    control("label removed", t.replace("Four of the fifteen checklist items below are open", "All done"), labels_ok)
    control("an open item marked done in the markup only", t.replace('<input type="checkbox" disabled aria-label="C5">', '<input type="checkbox" disabled checked aria-label="C5">'), checklist_ok)
    control("a checked item whose status is open", t.replace('data-c="C1" data-s="done"', 'data-c="C1" data-s="open"'), checklist_ok)
    control("an item removed", t.replace('data-c="C9"', 'data-c="X9"'), checklist_ok)
    control("method point removed", t.replace('data-m="M4"', 'data-m="X"'), method_ok)
    control("private name pasted in", t + " UERJ ", names_ok)
    print("[HONESTY] Checks structure, labels, that the checklist markup matches its stated status, and that the audit report and census files exist with the stated shape. It does not show the audit was run on the file now on disk, that the census tiers are right, or that the theory is right or wrong.")
    if FAIL or ctl:
        print(f"\nFAILED: {len(FAIL)} check(s), {len(ctl)} control(s) not rejected"); sys.exit(1)
    print("\nALL PASS")
main()
