#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Pablo Nogueira Grossi / G6 LLC
"""
book22/ch04-verify.py -- book22/ch04-placement.html: a satire sketch plus a placement form. Run first (R24).
    python3 book22/ch04-verify.py
Needs python3 and node. Checks STRUCTURE, the labels, the placement rule (by running it), and that nothing is sent or stored.
  [1] seven sketch beats S1..S7, each with English and Portuguese text
  [2] the fiction label, and the Doctor's name, are present
  [3] the form exists (name, learned, accent, staff, button, result area) and the page script defines place()
  [4] place() is RUN in node against recorded cases (the rule is the one in Chapter 1: no place named -> Thursday Alaska;
      a place named -> Tuesday Nantucket; staff exempt; empty name -> asked again; long names shortened to four letters)
  [5] privacy: no network call, no storage, no form action; the page says nothing typed leaves it
  [6] controls: each check fails on a damaged copy
  [HONESTY] what this does not establish
"""
import re, sys, json, subprocess, tempfile, os, shutil
from pathlib import Path
HERE = Path(__file__).resolve().parent
FAIL = []
def check(label, ok, detail=""):
    print(("PASS " if ok else "FAIL ") + label + (f"  -- {detail}" if detail else ""))
    if not ok: FAIL.append(label)
def plain(t): return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", t))
BEATS = ["S1", "S2", "S3", "S4", "S5", "S6", "S7"]
FORBIDDEN = ["fetch(", "XMLHttpRequest", "sendBeacon", "localStorage", "sessionStorage", "indexedDB", "document.cookie", "WebSocket", "<form", "action="]

def beats_ok(text):
    got = {}
    for m in re.finditer(r'<div class="sec" data-n="([^"]+)">(.*?</div>)\s*</div>\s*(?=<div class="sec"|<!--end-secs-->)', text, re.S):
        body = m.group(2)
        en = re.search(r'<div lang="en">(.*?)</div>', body, re.S)
        pt = re.search(r'<div lang="pt">(.*?)</div>', body, re.S)
        got[m.group(1)] = bool(en and plain(en.group(1)).strip()) and bool(pt and plain(pt.group(1)).strip())
    return list(got) == BEATS and all(got.values())
def uniform_ok(text):
    m = re.search(r'<div class="sec" data-n="S6">(.*?)<div lang="pt">', text, re.S)
    q = plain(m.group(1)) if m else ""
    return all(w in q for w in ["combat boots", "tuxedo", "tweed", "uniform", "no accent"])
def label_ok(text):
    p = plain(text)
    return "Fiction." in p and "invented" in p and "Fairweather" in p
def form_ok(text):
    ids = ["f-name", "f-learned", "f-accent", "f-staff", "f-go", "f-result"]
    return all(f'id="{i}"' in text for i in ids) and "function place(" in text
def script_of(text):
    m = re.search(r'<script id="placement">(.*?)</script>', text, re.S)
    return m.group(1) if m else ""
def run_cases(text):
    """Run the pure part of the page script (everything before '// glue') in node."""
    js = script_of(text).split("// glue")[0]
    if "function place(" not in js: return None
    cases = [
        ("Julia", "home", "", False),
        ("Nguyen", "school", "Vietnam", False),
        ("Anna", "school", "Brazil", False),
        ("", "school", "", False),
        ("   ", "school", "", False),
        ("Edmundo", "school", "", True),
        ("Ana", "school", "none", False),
    ]
    prog = js + "\nconsole.log(JSON.stringify(" + json.dumps(cases) + ".map(c=>place(c[0],c[1],c[2],c[3]))));"
    if shutil.which("node") is None: return "NONODE"
    with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False) as f:
        f.write(prog); path = f.name
    try:
        r = subprocess.run(["node", path], capture_output=True, text=True, timeout=20)
    finally:
        os.unlink(path)
    if r.returncode != 0: return None
    try: return json.loads(r.stdout.strip().splitlines()[-1])
    except Exception: return None
def rule_ok(out):
    if not isinstance(out, list) or len(out) != 7: return False
    julia, nguyen, anna, empty, blank, staff, ana = out
    return (julia.get("status") == "placed" and julia.get("elective") == "Alaska" and julia.get("day") == "Thursday"
            and nguyen.get("elective") == "Nantucket" and nguyen.get("day") == "Tuesday" and nguyen.get("shortName") == "Nguy"
            and anna.get("elective") == "Nantucket" and anna.get("shortName") == "Anna"
            and empty.get("status") == "ask" and blank.get("status") == "ask"
            and staff.get("status") == "exempt" and not staff.get("elective")
            and ana.get("elective") == "Alaska")
def privacy_ok(text):
    s = script_of(text)
    return not any(w in text for w in FORBIDDEN) and "Nothing you type leaves this page" in plain(text) and bool(s)

path = HERE / "ch04-placement.html"
if not path.exists():
    check("page exists: book22/ch04-placement.html", False, "not written yet")
    print("\nFAILED: " + ", ".join(FAIL)); sys.exit(1)
t = path.read_text(encoding="utf-8")
print("[1] sketch beats")
check("seven beats S1..S7 each have EN and PT text", beats_ok(t))
print("[1b] the dress-code beat")
check("S6 has the punk's boots, the tuxedo, the tweed, the word uniform and the Doctor's 'no accent'", uniform_ok(t))
check("control: beat without the tuxedo is caught", not uniform_ok(t.replace("tuxedo", "suit")))
print("[2] labels")
check("fiction label present, names the Doctor, says the people are invented", label_ok(t))
print("[3] the form")
check("form fields, button, result area and place() exist", form_ok(t))
print("[4] the rule, run")
out = run_cases(t)
if out == "NONODE":
    print("CANNOT RUN: node is not installed."); sys.exit(2)
check("place() returns the recorded placements (7 cases)", rule_ok(out), "" if rule_ok(out) else str(out))
print("[5] privacy")
check("no network, storage or form action; page says nothing typed leaves it", privacy_ok(t))
print("[6] controls")
check("control: renamed beat -> caught", not beats_ok(t.replace('data-n="S3"', 'data-n="S3x"')))
check("control: staff exemption removed -> caught",
      not rule_ok(run_cases(t.replace("if (staff)", "if (false)"))), "")
check("control: Julia sent to Tuesday -> caught",
      not rule_ok(run_cases(t.replace('"Alaska"', '"Nantucket"', 1))), "")
check("control: an injected fetch( is caught", not privacy_ok(t.replace("// glue", "fetch('/x'); // glue")))
check("control: a localStorage line is caught", not privacy_ok(t.replace("// glue", "localStorage.x=1; // glue")))
print("[HONESTY] This runs the placement rule and checks structure, labels and that the page makes no network or storage call.")
print("  The rule is arbitrary by design (satire). It does not measure anyone's accent. The Portuguese has not been read by a Portuguese speaker.")
print("\nFAILED: " + ", ".join(FAIL) if FAIL else "\nALL PASS")
sys.exit(1 if FAIL else 0)
