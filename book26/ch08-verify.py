#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Pablo Nogueira Grossi / G6 LLC
"""
book26/ch08-verify.py -- book26/ch08-a-preprint-against-a-kernel.html.
  [1] sections S1..S6   [2] labels   [3] the checklist: eleven items, C1..C4 checked, C5..C11 open, in the page's own markup
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
CENSUS = HERE / "nielsen-census.tsv"
FAIL = []
def check(label, ok, detail=""):
    print(("PASS " if ok else "FAIL ") + label + (f"  -- {detail}" if detail else ""))
    if not ok: FAIL.append(label)
def plain(t):
    t = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", t, flags=re.S)
    t = re.sub(r"<[^>]+>", " ", t)
    for a, b in (("&rsquo;", "'"), ("&ldquo;", '"'), ("&rdquo;", '"'), ("&amp;", "&"), ("&mdash;", "-"), ("&ndash;", "-"), ("&middot;", ".")):
        t = t.replace(a, b)
    return re.sub(r"\s+", " ", t)
SECS = ["S1", "S2", "S3", "S4", "S5", "S6"]
LABELS = ["most of the checklist below is open", "a hand derivation", "this is an estimate", "not a verdict", "not established here", "keyword matching"]
BANNED = ["citadel", "north bridge", "uerj", "zilacleide"]
FORBIDDEN = ["fetch(", "XMLHttpRequest", "localStorage", "<form", "action=", "<script"]
IDS = ["C%d" % i for i in range(1, 12)]
DONE = {"C1", "C2", "C3", "C4"}
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
    check("checklist: C1..C11, C1-C4 checked, C5-C11 open, markup agrees with status", checklist_ok(t))
    check("audit report exists: 7 theorem lines, axioms within the permitted set", audit_ok())
    check("second audit report (abstract arithmetic) exists: 6 theorem lines, permitted axioms", audit2_ok())
    check("census has 140 rows", census_ok())
    ctl = []
    def control(name, damaged, fn):
        ok = fn(damaged); print(("PASS " if not ok else "FAIL ") + "control rejected: " + name)
        if ok: ctl.append(name)
    control("section removed", t.replace('data-n="S3"', 'data-n="X"'), secs_ok)
    control("label removed", t.replace("Most of the checklist below is open", "All done"), labels_ok)
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
