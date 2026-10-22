#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Pablo Nogueira Grossi / G6 LLC
"""
book26/ch04-verify.py -- book26/ch04-response-gap-policy-brief.html: the author's credit-governance paper read as a policy analyst would,
each proposed control turned into something testable, with one control run. Run first (R24).
    python3 book26/ch04-verify.py
Needs python3 and node. Checks STRUCTURE, the labels, the control matrix, the response-time check (by running it), and exclusions.
  [1] sections S1..S5 in order
  [2] the control matrix names all four controls, each with a plain-words requirement, a test, and a status; the paper's DOI is cited
  [3] labels: not peer-reviewed; invented example numbers; not privacy or data-protection experience; not tested on a real system
  [4] budgetCheck() is RUN in node against hand-derived cases (below)
  [5] kept out: no employer name, no employer token from Chapter 1's hashed list; no network, storage or form action
  [6] controls: each check fails on a damaged copy
  [HONESTY] what this does not establish
Hand-derived cases for budgetCheck(detected, executed, budget), all in minutes:
  A: (0, 45, 60)  gap 45 < 60            -> fail, short by 15
  B: (0, 90, 60)  gap 90 >= 60           -> pass, gap 90
  C: (10, 70, 60) gap 60 >= 60 (equal)   -> pass, gap 60
  D: (30, 10, 60) executed before detected -> invalid
  E: all blank                           -> ask
  F: (0, 45, blank) budget missing       -> ask
"""
import re, sys, json, subprocess, tempfile, os, shutil, hashlib, ast
from pathlib import Path
HERE = Path(__file__).resolve().parent
FAIL = []
def check(label, ok, detail=""):
    print(("PASS " if ok else "FAIL ") + label + (f"  -- {detail}" if detail else ""))
    if not ok: FAIL.append(label)
def plain(t):
    t = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", t, flags=re.S)
    t = re.sub(r"<[^>]+>", " ", t)
    for a, b in (("&rsquo;", "'"), ("&lsquo;", "'"), ("&ldquo;", '"'), ("&rdquo;", '"'), ("&amp;", "&"), ("&mdash;", "-"), ("&middot;", "."), ("&ge;", ">=")):
        t = t.replace(a, b)
    return re.sub(r"\s+", " ", t)
FORBIDDEN = ["fetch(", "XMLHttpRequest", "sendBeacon", "localStorage", "sessionStorage", "indexedDB", "document.cookie", "WebSocket", "<form", "action="]
SECS = ["S1", "S2", "S3", "S4", "S5"]
CONTROLS = ["Published liquidation formulas", "Minimum response-time budget", "Epistemic-disclosure standard", "Rule-based circuit breaker"]
LABELS = ["not peer-reviewed", "invented", "not data-privacy", "not been tested on a real system"]
BANNED = ["ey", "ernst", "young", "secaucus", "baruch", "nga", "rutgers", "jpmorgan", "banco", "brasil", "tishman", "speyer"]
DOI = "10.5281/zenodo.21752834"

def secs_ok(t): return re.findall(r'<div class="sec" data-n="([^"]+)">', t) == SECS
def matrix_ok(t):
    rows = re.findall(r'<tr data-control="([^"]+)">(.*?)</tr>', t, re.S)
    got = {n: re.findall(r"<td[^>]*>(.*?)</td>", b, re.S) for n, b in rows}
    if list(got) != CONTROLS: return False
    return all(len(c) == 4 and all(plain(x).strip() for x in c) for c in got.values()) and DOI in t
def labels_ok(t):
    p = plain(t).lower(); return all(l.lower() in p for l in LABELS)
def script_of(t):
    m = re.search(r'<script id="budget">(.*?)</script>', t, re.S); return m.group(1) if m else ""
def run_cases(t):
    js = script_of(t).split("// glue")[0]
    if "function budgetCheck(" not in js: return None
    cases = [[0, 45, 60], [0, 90, 60], [10, 70, 60], [30, 10, 60], ["", "", ""], [0, 45, ""]]
    prog = js + "\nconsole.log(JSON.stringify(" + json.dumps(cases) + ".map(c=>budgetCheck(c[0],c[1],c[2]))));"
    if shutil.which("node") is None: return "NONODE"
    with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False) as f:
        f.write(prog); path = f.name
    try: r = subprocess.run(["node", path], capture_output=True, text=True, timeout=20)
    finally: os.unlink(path)
    if r.returncode != 0: return None
    try: return json.loads(r.stdout.strip().splitlines()[-1])
    except Exception: return None
def rule_ok(o):
    if not isinstance(o, list) or len(o) != 6: return False
    a, b, c, d, e, f = o
    return (a.get("status") == "fail" and a.get("gap") == 45 and a.get("shortBy") == 15
            and b.get("status") == "pass" and b.get("gap") == 90
            and c.get("status") == "pass" and c.get("gap") == 60
            and d.get("status") == "invalid" and e.get("status") == "ask" and f.get("status") == "ask")
def banned_ok(t):
    words = set(re.findall(r"[a-z\-]+", plain(t).lower()))
    return not any(b in words for b in BANNED)
def hashes():
    src = (HERE / "ch01-verify.py").read_text(encoding="utf-8")
    m = re.search(r"EMPLOYER_HASHES\s*=\s*set\((\{.*?\})\)", src, re.S)
    return ast.literal_eval(m.group(1)) if m else set()
def hash_ok(t):
    H = hashes()
    if not H: return False
    ws = set(re.findall(r"[a-z][a-z']+", plain(t).lower()))
    return not any(hashlib.sha256(w.encode()).hexdigest() in H for w in ws)
def privacy_ok(t):
    return not any(w in t for w in FORBIDDEN) and "Nothing you type leaves this page" in plain(t) and bool(script_of(t))

path = HERE / "ch04-response-gap-policy-brief.html"
if not path.exists():
    check("page exists: book26/ch04-response-gap-policy-brief.html", False, "not written yet")
    print("\nFAILED: " + ", ".join(FAIL)); sys.exit(1)
t = path.read_text(encoding="utf-8")
print("[1] sections"); check("five sections S1..S5 in order", secs_ok(t))
print("[2] control matrix"); check("four controls, each with requirement, test, status; paper DOI cited", matrix_ok(t))
print("[3] labels"); check("not peer-reviewed / invented numbers / not data-privacy / not tested on a real system", labels_ok(t))
print("[4] the check, run")
out = run_cases(t)
if out == "NONODE": print("CANNOT RUN: node is not installed."); sys.exit(2)
check("budgetCheck() returns the hand-derived results (6 cases)", rule_ok(out), "" if rule_ok(out) else str(out))
print("[5] kept out")
check("no employer, school or place name", banned_ok(t))
check("no employer token from Chapter 1's hashed list (loaded: %d)" % len(hashes()), hash_ok(t))
check("no network, storage or form action; page says nothing typed leaves it", privacy_ok(t))
print("[6] controls")
check("control: a missing section is caught", not secs_ok(t.replace('data-n="S3"', 'data-n="S3x"')))
check("control: a missing control row is caught", not matrix_ok(t.replace('data-control="Rule-based circuit breaker"', 'data-control="x"')))
check("control: a missing DOI is caught", not matrix_ok(t.replace(DOI, "")))
check("control: a missing label is caught", not labels_ok(re.sub("not peer-reviewed", "reviewed", t, flags=re.I)))
check("control: equal-to-budget treated as fail is caught", not rule_ok(run_cases(t.replace(">= b", "> b", 1))))
check("control: executed-before-detected treated as pass is caught", not rule_ok(run_cases(t.replace("g < 0", "false", 1))))
check("control: an employer word is caught", not banned_ok(t.replace("</body>", "<p>Ernst</p></body>")))
check("control: an injected fetch( is caught", not privacy_ok(t.replace("// glue", "fetch('/x'); // glue")))
print("[HONESTY] This runs the response-time check against hand-derived cases and checks structure, labels and exclusions.")
print("  It does not check the paper's claims about credit markets, does not test any real system, and the example minutes are invented.")
print("\nFAILED: " + ", ".join(FAIL) if FAIL else "\nALL PASS")
sys.exit(1 if FAIL else 0)
