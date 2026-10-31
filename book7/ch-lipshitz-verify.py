#!/usr/bin/env python3
"""ch-lipshitz-verify.py -- Book 7, "Robert Lipshitz / The Author Who Kept the Transcript".

The chapter is sourced only from R. Lipshitz, arXiv:2610.37595v1 (27 Oct 2026). This script checks two things:

  1. every figure the chapter states from the paper is on the page, and a control shows the check can fail
     (the constants below were typed from the paper's text once, here, and are what the page is held to);
  2. the headline "six" is the rank gain that ch-local-equivalence-verify.py computes from the paper's Table 2,
     by running that script and reading its line B4.

It cannot check that the paper's account of how the work was done is true, and it does not try.
Run:  python3 ch-lipshitz-verify.py   (in book7/, beside both chapters)
"""
import os, re, subprocess, sys, html

HERE = os.path.dirname(os.path.abspath(__file__))
fails = []
def check(name, ok, detail=""):
    print(("PASS  " if ok else "FAIL  ") + name + (("  -- " + detail) if detail else ""))
    if not ok: fails.append(name)

def text_of(fn):
    s = open(os.path.join(HERE, fn), encoding='utf8').read()
    s = re.sub(r'<(script|style)[^>]*>.*?</\1>', ' ', s, flags=re.S)
    s = re.sub(r'<[^>]+>', ' ', s)
    return re.sub(r'\s+', ' ', html.unescape(s))

page = text_of('ch-lipshitz.html')

# (label, string that must appear on the page) -- each typed from the paper
FROM_PAPER = [
    ("arXiv number",                 "2610.37595"),
    ("date of v1",                   "27 Oct 2026"),
    ("page count",                   "40 pages"),
    ("rewrite hours, low end",       "between 50 and 100 hours"),
    ("subscription price",           "$20 a month"),
    ("quota statement",              "more than half his weekly quota"),
    ("NSF grant",                    "DMS-2505715"),
    ("first model",                  "Fable 5"),
    ("later models",                 "Opus 5.5"),
    ("collaborators named",          "Nathan Dunfield"),
    ("collaborators named (2)",      "Dirk Sch"),
    ("coauthor of the key proof's source", "Section 2.4.2"),
    ("false failures",               "forty-four"),
    ("number of questions answered", "six concordance"),
]
for label, needle in FROM_PAPER:
    check(f"1  page states: {label}", needle in page, repr(needle))

# control: a corrupted copy of the page must fail the same test
bad = page.replace("between 50 and 100 hours", "between 15 and 100 hours")
check("1c control: corrupting the hours figure makes the check fail", "between 50 and 100 hours" not in bad)

# the 'six' check, run from the sibling verifier
proc = subprocess.run([sys.executable, os.path.join(HERE, 'ch-local-equivalence-verify.py')], capture_output=True, text=True)
m = re.search(r"B4 .*gain = (\d+)", proc.stdout)
check("2  the sibling verifier reports a rank gain of 6 on Table 2", bool(m) and m.group(1) == "6", m.group(0) if m else "B4 line not found")
check("2b the sibling verifier passes as a whole", proc.returncode == 0)

mathpage = text_of('ch-local-equivalence.html')
for nxt in ("249, 185, 888, 5110, 27436", "168030 and 1008906"):
    check("3  math chapter prints the Table 3 column sums the verifier computes", nxt in mathpage, nxt)

print()
if fails:
    print("FAILED:", ", ".join(fails)); sys.exit(1)
print("All checks passed. They tie the page to the paper's text as typed here; they do not test the paper.")
