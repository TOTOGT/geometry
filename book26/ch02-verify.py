#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Pablo Nogueira Grossi / G6 LLC
"""
book26/ch02-verify.py -- book26/ch02-fpa-hvac.html, an FP&A work sample for HVAC and mechanical services. Run first (R24).
    python3 book26/ch02-verify.py
Needs python3 and node.
  [1] the sourced figures are on the page (BLS Occupational Outlook Handbook; ACCA/Farmington survey, via ACHR News)
  [2] the page's metrics() function is RUN in node against hand-derived cases
  [3] labels: no company data; illustrative example is marked invented; sources read through a fetch summary; framework is definitions
  [4] privacy: no network call, no storage, no form action; the page says nothing typed leaves it
  [5] controls: each check fails on a damaged copy
  [HONESTY] what this does not establish
Hand-derived cases (arithmetic done on paper, not by the page):
  A: 4 trucks, 6000 service revenue -> 1500 per truck-day. Labor 5000+1500+400+600 = 7500 over 100 billable hours -> 75.00 per hour.
     Install: price 15000; quoted material 8000 + 40 h x 50 = 10000 -> GM 5000 (33.33%); actual material 8800 + 52 h x 50 = 11400 -> GM 3600 (24%);
     material variance -800, labor variance -600, bridge -1400 = 3600 - 5000.
     Agreements: 500 at start, 40 lost -> 8% churn; 90 sold of 600 eligible -> 15% attach.
     Cash floor: fixed 30000 per shoulder month; fee 200, cost to serve 40% -> 200 x 0.6 / 12 = 10.00 per month -> 3000 agreements.
  B: all inputs blank -> every output blank (null). C: zero billable hours -> burden blank, not infinity.
"""
import re, sys, json, subprocess, tempfile, os, shutil
from pathlib import Path
HERE = Path(__file__).resolve().parent
FAIL = []
def check(label, ok, detail=""):
    print(("PASS " if ok else "FAIL ") + label + (f"  -- {detail}" if detail else ""))
    if not ok: FAIL.append(label)
def plain(t): return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", t))
FORBIDDEN = ["fetch(", "XMLHttpRequest", "sendBeacon", "localStorage", "sessionStorage", "indexedDB", "document.cookie", "WebSocket", "<form", "action="]
FIGURES = [
 ("BLS", "61,010", "median pay May 2025"), ("BLS", "29.33", "hourly"), ("BLS", "440,900", "jobs 2025"),
 ("BLS", "11%", "growth 2025-2035"), ("BLS", "2035", "projection end"), ("BLS", "August 27, 2026", "page last modified"),
 ("ACCA", "over 1,000", "contractors surveyed"), ("ACCA", "6%", "national average net profit"), ("ACCA", "10%", "ACCA target"),
 ("ACCA", "5%", "residential / small / mid / rural"), ("ACCA", "9%", "commercial / marketing >=12%"), ("ACCA", "8%", "large firms"),
 ("ACCA", "12%", "marketing threshold"), ("ACCA", "27%", "extended labor warranty margin"), ("ACCA", "19%", "adjust pricing by season"),
 ("ACCA", "January 28, 2026", "article posted"), ("ACCA", "Farmington Consulting Group", "ran the survey"),
 ("SEC", "21,747", "Carrier 2025 net sales, $ millions (8-K ex. 99, Feb 5, 2026)"),
 ("SEC", "22,486", "Carrier 2024 net sales"),
 ("SEC", "21,321.9", "Trane Technologies 2025 net revenues (8-K ex. 99.1, Jan 29, 2026)"),
 ("SEC", "19,838.2", "Trane 2024 net revenues"),
 ("SEC", "16,986.4", "EMCOR 2025 revenues (8-K ex. 99.1, Feb 26, 2026)"),
 ("SEC", "14,566.1", "EMCOR 2024 revenues"),
 ("SEC", "7,050.5", "EMCOR US mechanical construction and facilities services 2025"),
 ("SEC", "16.6%", "EMCOR increase as stated in the release"),
 ("SEC", "9,101.6", "Comfort Systems USA 2025 revenue (8-K ex. 99.1, Feb 19, 2026)"),
 ("SEC", "7,027.5", "Comfort Systems USA 2024 revenue"),
 ("SEC", "11.94 billion", "Comfort Systems USA backlog at Dec 31, 2025"),
 ("SEC", "20.4 billion", "figure in the supplied summary for Carrier, shown as not matching the filing"),
]
def figures_missing(t):
    p = plain(t)
    return [f"{s}:{x}" for s, x, _ in FIGURES if x not in p]
def script_of(t):
    m = re.search(r'<script id="fpa">(.*?)</script>', t, re.S)
    return m.group(1) if m else ""
INPUT_A = {"trucks":4,"svcrev":6000,"wages":5000,"tax":1500,"ins":400,"fuel":600,"hours":100,"price":15000,"qmat":8000,"qhrs":40,"rate":50,
           "amat":8800,"ahrs":52,"start":500,"lost":40,"sold":90,"elig":600,"fixed":30000,"fee":200,"cts":40}
def run_cases(t):
    js = script_of(t).split("// glue")[0]
    if "function metrics(" not in js: return None
    blank = {k: "" for k in INPUT_A}
    zero = dict(INPUT_A); zero["hours"] = 0
    prog = js + "\nconsole.log(JSON.stringify([" + ",".join("metrics(%s)" % json.dumps(c) for c in (INPUT_A, blank, zero)) + "]));"
    if shutil.which("node") is None: return "NONODE"
    with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False) as f:
        f.write(prog); path = f.name
    try: r = subprocess.run(["node", path], capture_output=True, text=True, timeout=20)
    finally: os.unlink(path)
    if r.returncode != 0: return None
    try: return json.loads(r.stdout.strip().splitlines()[-1])
    except Exception: return None
def close(a, b): return a is not None and abs(a - b) < 0.005
def cases_ok(out):
    if not isinstance(out, list) or len(out) != 3: return False
    A, B, C = out
    ok = (close(A.get("revPerTruckDay"), 1500) and close(A.get("burdenPerHour"), 75)
          and close(A.get("quotedGM"), 5000) and close(A.get("quotedGMpct"), 1/3) and close(A.get("actualGM"), 3600) and close(A.get("actualGMpct"), 0.24)
          and close(A.get("matVar"), -800) and close(A.get("labVar"), -600) and close(A.get("bridgeTotal"), -1400)
          and close(A.get("churn"), 0.08) and close(A.get("attach"), 0.15)
          and close(A.get("monthlyContribution"), 10) and A.get("floorAgreements") == 3000)
    return ok and all(v is None for v in B.values()) and C.get("burdenPerHour") is None and close(C.get("revPerTruckDay"), 1500)
def comfort_change_ok(t):
    # 9,101.641 / 7,027.476 - 1 = 29.5%: the page's own arithmetic, checked here
    return "29.5%" in plain(t) and abs((9101.641 / 7027.476 - 1) * 100 - 29.5) < 0.05
def players_ok(t):
    q = plain(t)
    return all(w in q for w in ["Who the players are", "not all of it is HVAC", "fiscal year", "Daikin", "Gree", "private-equity"]) and comfort_change_ok(t) and "expects the industry to consolidate" in q and "an expectation, not a finding" in q
def labels_ok(t):
    q = plain(t)
    return all(w in q for w in ["Work sample", "no company data", "invented", "not independently checked", "definitions", "Stakeholders VR"])
def privacy_ok(t):
    return not any(w in t for w in FORBIDDEN) and "Nothing you type leaves this page" in plain(t) and bool(script_of(t))

path = HERE / "ch02-fpa-hvac.html"
if not path.exists():
    check("page exists: book26/ch02-fpa-hvac.html", False, "not written yet")
    print("\nFAILED: " + ", ".join(FAIL)); sys.exit(1)
t = path.read_text(encoding="utf-8")
print("[1] sourced figures")
miss = figures_missing(t)
check(f"all {len(FIGURES)} recorded figures are on the page", not miss, ", ".join(miss))
print("[2] the metrics, run")
out = run_cases(t)
if out == "NONODE": print("CANNOT RUN: node is not installed."); sys.exit(2)
check("metrics() matches the hand-derived cases A, B, C", cases_ok(out), "" if cases_ok(out) else str(out)[:300])
print("[2b] players section")
check("players section: not all HVAC, fiscal year stated, Daikin/Gree/PE named as left out, Comfort change recomputed", players_ok(t))
print("[3] labels")
check("labels present (work sample, no company data, invented example, not independently checked, definitions, link to first piece)", labels_ok(t))
print("[4] privacy")
check("no network, storage or form action; page says nothing typed leaves it", privacy_ok(t))
print("[5] controls")
check("control: a changed figure (61,010 -> 61,100) is caught", bool(figures_missing(t.replace("61,010", "61,100"))))
check("control: insurance dropped from labor burden is caught", not cases_ok(run_cases(t.replace("v.wages, v.tax, v.ins, v.fuel", "v.wages, v.tax, v.fuel"))))
check("control: cash floor using the wrong divisor is caught", not cases_ok(run_cases(t.replace("div(v.fixed, contrib)", "div(v.fixed, v.fee)"))))
check("control: churn inverted is caught", not cases_ok(run_cases(t.replace("div(v.lost, v.start)", "div(v.start, v.lost)"))))
check("control: material variance sign flipped is caught", not cases_ok(run_cases(t.replace("-(v.amat - v.qmat)", "(v.amat - v.qmat)"))))
check("control: an injected fetch( is caught", not privacy_ok(t.replace("// glue", "fetch('/x'); // glue")))
check("control: players caveat removed is caught", not players_ok(t.replace("not all of it is HVAC", "")))
check("control: label removed is caught", not labels_ok(t.replace("no company data", "")))
print("[HONESTY] This checks that the page carries the recorded figures, that its arithmetic is right on three hand-derived cases, and that it sends and stores nothing.")
print("  It does not check the BLS or ACCA figures against the sources (read through a fetch tool's summary), the framework, or that any real HVAC firm looks like the example.")
print("\nFAILED: " + ", ".join(FAIL) if FAIL else "\nALL PASS")
sys.exit(1 if FAIL else 0)
