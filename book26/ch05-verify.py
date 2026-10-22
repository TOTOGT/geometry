#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Pablo Nogueira Grossi / G6 LLC
"""
book26/ch05-verify.py -- book26/ch05-proposal-with-a-test-that-can-fail.html: a research proposal's decision rule, runnable. Run first (R24).
    python3 book26/ch05-verify.py        (needs python3 and node)
  [1] sections S1..S4 in order
  [2] labels: exploratory not a test; invented example numbers; no real data shown; not peer-reviewed; plain statement of no PhD
  [3] rCheck() is RUN in node against hand-derived cases (below)
  [4] kept out: the collaborator's table values (private until permission), employer names, network/storage/form
  [5] controls: each check fails on a damaged copy
  [HONESTY] what this does not establish
rCheck(sZ, rZ, sM, rM, tol): R = (1-sZ) rZ^2 / ((1-sM) rM^2); pass if |R-1| <= tol; invalid if a sigma is outside [0,1) or a radius <= 0; ask if tol blank.
Hand-derived cases (radii in angstrom, ALL INVENTED for illustration):
  A: (0,    5, 0.75, 10, 0.1)  25 vs 0.25*100=25     R=1    -> pass
  B: (0,    5, 0.5,  10, 0.2)  25 vs 50              R=0.5  -> fail
  C: (0.4,  6, 0.5,  6,  0.2)  0.6/0.5               R=1.2  -> pass (edge, equal to tol)
  D: (0.4,  6, 0.5,  6,  0.1)  R=1.2, tol 0.1        -> fail
  E: (0,    5, 1,    10, 0.1)  sigma_M = 1           -> invalid
  F: (0,    5, 0.75, 10, '')   tolerance blank       -> ask
"""
import re, sys, subprocess, tempfile, os
from pathlib import Path
HERE = Path(__file__).resolve().parent
PAGE = HERE / "ch05-proposal-with-a-test-that-can-fail.html"
FAIL = []
def check(label, ok, detail=""):
    print(("PASS " if ok else "FAIL ") + label + (f"  -- {detail}" if detail else ""))
    if not ok: FAIL.append(label)
def plain(t):
    t = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", t, flags=re.S)
    t = re.sub(r"<[^>]+>", " ", t)
    for a, b in (("&rsquo;", "'"), ("&ldquo;", '"'), ("&rdquo;", '"'), ("&amp;", "&"), ("&mdash;", "-"), ("&middot;", ".")):
        t = t.replace(a, b)
    return re.sub(r"\s+", " ", t)
FORBIDDEN = ["fetch(", "XMLHttpRequest", "sendBeacon", "localStorage", "sessionStorage", "indexedDB", "document.cookie", "WebSocket", "<form", "action="]
SECS = ["S1", "S2", "S3", "S4"]
LABELS = ["not a test", "invented", "no real data", "not peer-reviewed", "do not hold a phd"]
PRIVATE_VALUES = ["73.70", "81.44", "86.22", "88.89", "26.36", "28.65", "15.71", "18.01", "17.25", "27.43"]
BANNED = ["ernst", "secaucus", "baruch", "rutgers", "jpmorgan", "banco do brasil", "tishman", "speyer"]
CASES = [((0, 5, 0.75, 10, 0.1), "pass"), ((0, 5, 0.5, 10, 0.2), "fail"), ((0.4, 6, 0.5, 6, 0.2), "pass"),
         ((0.4, 6, 0.5, 6, 0.1), "fail"), ((0, 5, 1, 10, 0.1), "invalid"), ((0, 5, 0.75, 10, ""), "ask")]

def secs_ok(t): return re.findall(r'<div class="sec" data-n="([^"]+)">', t) == SECS
def labels_ok(t):
    p = plain(t).lower()
    return all(l in p for l in LABELS)
def script_of(t):
    m = re.search(r'<script id="rcheck">(.*?)</script>', t, re.S)
    return m.group(1).split("// glue")[0] if m else ""
def run_cases(t):
    js = script_of(t)
    if not js.strip(): return None
    harness = js + "\nconst cases=" + repr([[list(c), e] for c, e in CASES]).replace("'", '"') + ";\n" + \
      "const out=cases.map(([a,e])=>[rCheck(...a).verdict,e]);console.log(JSON.stringify(out));"
    with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False) as f:
        f.write(harness); name = f.name
    try:
        r = subprocess.run(["node", name], capture_output=True, text=True, timeout=20)
    finally:
        os.unlink(name)
    if r.returncode != 0: return None
    import json
    return json.loads(r.stdout.strip().splitlines()[-1])
def cases_ok(t):
    res = run_cases(t)
    return bool(res) and all(g == e for g, e in res)
def clean_ok(t):
    low = t.lower()
    return not any(b in low for b in BANNED) and not any(v in t for v in PRIVATE_VALUES) and not any(f in t for f in FORBIDDEN)

def main():
    t = PAGE.read_text(encoding="utf-8") if PAGE.exists() else ""
    check("page exists", bool(t))
    if not t:
        print("\nFAILED: page absent"); sys.exit(1)
    print("[1] sections")
    check("sections S1..S4 in order", secs_ok(t))
    print("[2] labels")
    check("all required labels present", labels_ok(t))
    print("[3] rCheck run in node")
    res = run_cases(t)
    check("rCheck runs and matches all hand-derived cases", cases_ok(t), str(res))
    print("[4] kept out")
    check("no private table values, no employer names, no network/storage/form", clean_ok(t))
    print("[5] controls (each must reject a damaged copy)")
    ctl = []
    def control(name, damaged, fn):
        ok = fn(damaged)
        print(("PASS " if not ok else "FAIL ") + "control rejected: " + name)
        if ok: ctl.append(name)
    control("section removed", t.replace('data-n="S3"', 'data-n="X"'), secs_ok)
    control("label removed", re.sub("(?i)no real data", "zzz", t), labels_ok)
    control("rule broken (pass if |R-1| >= tol)", t.replace("<=", ">=", 1) if "<=" in script_of(t) else t + "BREAK", cases_ok)
    control("private value pasted in", t + " 73.70 ", clean_ok)
    control("fetch added", t + " fetch('x') ", clean_ok)
    print("[HONESTY] This checks structure, the labels and the arithmetic of the rule. It does not show the self-trapping law is true, that any real data pass or fail it, or that the proposal will be funded.")
    if FAIL or ctl:
        print(f"\nFAILED: {len(FAIL)} check(s), {len(ctl)} control(s) not rejected"); sys.exit(1)
    print("\nALL PASS")
main()
