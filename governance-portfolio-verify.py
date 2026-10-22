#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Pablo Nogueira Grossi / G6 LLC
"""
governance-portfolio-verify.py -- governance-portfolio.html, one page listing the work that bears on policy and governance,
with what each piece shows and does not show. Run first (R24).
    python3 governance-portfolio-verify.py
Standard library only. Checks STRUCTURE, that every link points at something that exists in this repo (or the one DOI), the labels,
and what is kept out. It cannot check that the linked work is good, only that the page does not point at nothing.
  [1] five numbered items P1..P5 in order, plus a "does not show" section
  [2] links: required local pages exist; every GitHub link names a path that exists in this repo; the DOI is the paper's
  [3] labels: not peer-reviewed; not data-privacy; each item carries a "shows" and a "does not show"
  [4] kept out: no employer, school or place name; no employer token from the hashed list
  [5] no script, no network call, no form
  [6] controls: each check fails on a damaged copy
  [HONESTY] what this does not establish
"""
import re, sys, hashlib, ast
from pathlib import Path
ROOT = Path(__file__).resolve().parent
FAIL = []
def check(label, ok, detail=""):
    print(("PASS " if ok else "FAIL ") + label + (f"  -- {detail}" if detail else ""))
    if not ok: FAIL.append(label)
def plain(t):
    t = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", t, flags=re.S)
    t = re.sub(r"<[^>]+>", " ", t)
    for a, b in (("&rsquo;", "'"), ("&lsquo;", "'"), ("&ldquo;", '"'), ("&rdquo;", '"'), ("&amp;", "&"), ("&mdash;", "-"), ("&middot;", ".")):
        t = t.replace(a, b)
    return re.sub(r"\s+", " ", t)
ITEMS = ["P1", "P2", "P3", "P4", "P5"]
REQ_LOCAL = ["book26/ch04-response-gap-policy-brief.html", "book6/wp32-forced-urgency-gap.html", "book6/wp56-algorithmic-urgency.html"]
DOI = "10.5281/zenodo.21752834"
BANNED = ["ey", "ernst", "secaucus", "baruch", "nga", "rutgers", "jpmorgan", "banco", "brasil", "tishman", "speyer", "zoni", "uceda"]
GH = "https://github.com/TOTOGT/geometry/blob/main/"

def items_ok(t):
    got = re.findall(r'<div class="item" data-n="([^"]+)">', t)
    return got == ITEMS and 'data-n="S5"' in t
def each_item_ok(t):
    ok = True
    for n, body in re.findall(r'<div class="item" data-n="([^"]+)">(.*?)</div>\s*(?=<div class="item"|<div class="sec")', t, re.S):
        p = plain(body).lower()
        ok = ok and "shows:" in p and "does not show:" in p
    return ok and len(re.findall(r'<div class="item"', t)) == 5
def links(t): return re.findall(r'href="([^"]+)"', t)
def links_ok(t):
    ls = links(t)
    for r in REQ_LOCAL:
        if r not in ls or not (ROOT / r).exists(): return False
    for l in ls:
        if l.startswith(GH):
            if not (ROOT / l[len(GH):]).exists(): return False
        elif not l.startswith(("http://", "https://", "mailto:", "#")):
            if not (ROOT / l.split("#")[0]).exists(): return False
    return any(DOI in l for l in ls)
def labels_ok(t):
    p = plain(t).lower(); return "not peer-reviewed" in p and "not data-privacy" in p
def banned_ok(t):
    words = set(re.findall(r"[a-z\-]+", plain(t).lower())); return not any(b in words for b in BANNED)
def hashes():
    src = (ROOT / "book26" / "ch01-verify.py").read_text(encoding="utf-8")
    m = re.search(r"EMPLOYER_HASHES\s*=\s*set\((\{.*?\})\)", src, re.S)
    return ast.literal_eval(m.group(1)) if m else set()
def hash_ok(t):
    H = hashes()
    if not H: return False
    ws = set(re.findall(r"[a-z][a-z']+", plain(t).lower()))
    return not any(hashlib.sha256(w.encode()).hexdigest() in H for w in ws)
def clean_ok(t):
    return not any(w in t for w in ["<script", "fetch(", "XMLHttpRequest", "<form", "action=", "localStorage"])

path = ROOT / "governance-portfolio.html"
if not path.exists():
    check("page exists: governance-portfolio.html", False, "not written yet")
    print("\nFAILED: " + ", ".join(FAIL)); sys.exit(1)
t = path.read_text(encoding="utf-8")
print("[1] structure"); check("five items P1..P5 in order and a does-not-show section", items_ok(t)); check("each item says what it shows and what it does not", each_item_ok(t))
print("[2] links"); check("required pages exist; every GitHub link names an existing path; the paper's DOI is linked", links_ok(t))
print("[3] labels"); check("not peer-reviewed; not data-privacy", labels_ok(t))
print("[4] kept out"); check("no employer, school or place name", banned_ok(t)); check("no employer token from the hashed list (loaded: %d)" % len(hashes()), hash_ok(t))
print("[5] clean"); check("no script, network call or form", clean_ok(t))
print("[6] controls")
check("control: a missing item is caught", not items_ok(t.replace('data-n="P3"', 'data-n="P3x"')))
check("control: an item without a does-not-show is caught", not each_item_ok(re.sub("does not show:", "x:", t, count=1, flags=re.I)))
check("control: a dead local link is caught", not links_ok(t.replace("book6/wp56-algorithmic-urgency.html", "book6/nope.html")))
check("control: a dead GitHub path is caught", not links_ok(t.replace(GH + "docs/audit-log.md", GH + "docs/nope.md")))
check("control: a missing DOI is caught", not links_ok(t.replace(DOI, "")))
check("control: a missing label is caught", not labels_ok(re.sub("not peer-reviewed", "reviewed", t, flags=re.I)))
check("control: an employer word is caught", not banned_ok(t.replace("</body>", "<p>Ernst</p></body>")))
check("control: an injected script is caught", not clean_ok(t.replace("</body>", "<script>1</script></body>")))
print("[HONESTY] This checks that the page points at things that exist and says what each does not show. It does not judge the linked work,")
print("  and the GitHub links only resolve once the files are pushed to the main branch.")
print("\nFAILED: " + ", ".join(FAIL) if FAIL else "\nALL PASS")
sys.exit(1 if FAIL else 0)
