#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Pablo Nogueira Grossi / G6 LLC
"""
book26/ch18-verify.py -- book26/ch18-a-burn-worth-measuring.html (Template B): a study proposal for planned forest
burns (drone lidar, thermal imaging, machine learning, satellite-lidar comparison), written for a state fire service and
a machine-learning lab, built from four public sources read on 11 November 2026.
  [1] structure: hero, section nav, sections in order, Sources footer; no script, form, network or storage code;
      internal links resolve
  [2] typed facts from the sources appear on the page (dates, counts, figures)
  [3] the three failure conditions of section 3 are stated, with their thresholds
  [4] honesty: no result, agreement, interest, review, experience or permission is claimed; no individual is named
      outside the cited source list; the limits are all present
  [5] SOURCE: the preprint's text has no occurrence of 'lidar' or 'GEDI' if a held copy is present (pdftotext); prints
      SKIP, never PASS, otherwise
  [6] controls: each check family is run on a page with the matching statement removed and must fail   [HONESTY]
Held copy is looked for in $PREPRINT_PDF, else ~/Downloads/2025.09.06.674602v3.full.pdf.
Standard library only; the preprint check needs pdftotext.
"""
import os, re, subprocess, sys, html as _h
from pathlib import Path
HERE = Path(__file__).resolve().parent
PAGE = HERE / "ch18-a-burn-worth-measuring.html"
PDF = Path(os.environ.get("PREPRINT_PDF", Path.home() / "Downloads" / "2025.09.06.674602v3.full.pdf"))
FAIL, SKIP = [], []
def check(label, ok, detail=""):
    print(("PASS " if ok else "FAIL ") + label + (f"  -- {detail}" if detail else ""))
    if not ok: FAIL.append(label)
def skip(label, why): print(f"SKIP {label}  -- {why}"); SKIP.append(label)

raw = PAGE.read_text(encoding="utf-8")
def visible(r):
    t = re.sub(r"<(script|style)[^>]*>.*?</\1>", "", r, flags=re.S)
    t = re.sub(r"<[^>]+>", " ", t)
    return re.sub(r"\s+", " ", _h.unescape(t))
txt = visible(raw)
body_txt = visible(raw.split('<footer id="sources"', 1)[0])   # everything before the Sources footer

# ---- typed from the sources as read ----
FACTS = ["1928", "11 November 2026", "Somerset County", "22 April 2024", "11 June 2024", "March 2023",
         "83 camera-trap datasets", "10 km", "0.10", "0.17", "17 February 2026", "February and early April",
         "2025 season", "Snapshot USA", "all three lasers"]
FAIL_CONDITIONS = ["twice the standard deviation", "At least 30 GEDI footprints", "Fewer than 30", "held-out"]
LIMITS = ["Any experience in fire science", "Any agreement, interest or review", "Any result", "drone flight near a burn is permitted",
          "GEDI is operating now", "Wildfire", "The whole preprint", "Anything after the date read"]
CLAIM_PHRASES = [r"\bwe found\b", r"\bresults show\b", r"\bdemonstrates?\b", r"\bproved\b", r"(?<!neither )\bhas agreed\b",
                 r"\bis interested\b", r"\bwere interested\b", r"\bhas approved\b", r"\bpermission was granted\b",
                 r"\bour experience\b", r"\bI have worked\b"]

def c_structure(r):
    t = visible(r)
    ok = []
    ok.append(("hero present", 'class="hero"' in r))
    ok.append(("section nav present", 'class="pillars"' in r))
    ids = re.findall(r'<section id="([a-z]+)"', r)
    ok.append(("sections in order", ids == ["intro","record","proposal","test","readers","limits","updates","checked"]))
    ok.append(("Sources footer", 'id="sources"' in r))
    ok.append(("no script/form/network/storage", not re.search(r"<script|<form|fetch\(|XMLHttpRequest|localStorage|sessionStorage", r)))
    return ok
def c_facts(t):  return [(f"fact: {f}", f in t) for f in FACTS]
def c_fail(t):   return [(f"failure condition: {f}", f in t) for f in FAIL_CONDITIONS]
def c_honest(t_full, t_body):
    ok = []
    ok.append(("states neither organization has seen or agreed", "Neither has seen this page, and neither has agreed" in t_body))
    for p in CLAIM_PHRASES:
        ok.append((f"no claim phrase {p}", not re.search(p, t_body, flags=re.I)))
    ok.append(("no first-name or surname of a person outside Sources", not re.search(r"\bSara\b|Beery(?!Lab)|\bHaucke,", t_body.replace("Haucke and colleagues", ""))))
    for l in LIMITS:
        ok.append((f"limit present: {l}", l in t_body))
    ok.append(("no result reported as measured", "No measurement has been made" in t_body))
    return ok

def run(label, results):
    for l, o in results: check(f"{label} {l}", o)

print("== [1] structure"); run("[1]", c_structure(raw))
# internal links
links = re.findall(r'href="([^"#:]+\.html)"', raw)
for l in sorted(set(links)):
    target = (HERE.parent / l[len('/geometry/'):]) if l.startswith('/geometry/') else (HERE / l)
    check(f"[1] link resolves: {l}", target.resolve().exists())
print("== [2] typed facts"); run("[2]", c_facts(txt))
print("== [3] failure conditions"); run("[3]", c_fail(txt))
print("== [4] honesty"); run("[4]", c_honest(txt, body_txt))

print("== [5] source")
if PDF.exists():
    try:
        out = subprocess.run(["pdftotext", str(PDF), "-"], capture_output=True, text=True, timeout=60).stdout
        n = len(re.findall(r"lidar|GEDI", out, flags=re.I))
        check("[5] preprint text has no 'lidar' or 'GEDI'", n == 0, f"{n} occurrences in {len(out)} characters")
    except Exception as e:
        skip("[5] preprint search", f"pdftotext failed: {e}")
else:
    skip("[5] preprint search", f"no held copy at {PDF}; set PREPRINT_PDF")

print("== [6] controls: each family must FAIL on a page with the statement removed")
def must_fail(label, results):
    bad = [l for l, o in results if not o]
    check(f"[6] control fails: {label}", len(bad) > 0, f"{len(bad)} check(s) fail as they should")
must_fail("facts", c_facts(txt.replace("1928", "").replace("0.17", "")))
must_fail("failure conditions", c_fail(txt.replace("twice the standard deviation", "").replace("Fewer than 30", "")))
must_fail("honesty (agreement claim removed)", c_honest(txt, body_txt.replace("Neither has seen this page, and neither has agreed", "")))
must_fail("honesty (claim phrase added)", c_honest(txt, body_txt + " The results show it works."))
must_fail("structure (script added)", c_structure(raw + "<script>fetch('x')</script>"))

print()
print(f"{len(FAIL)} FAIL, {len(SKIP)} SKIP")
sys.exit(1 if FAIL else 0)
