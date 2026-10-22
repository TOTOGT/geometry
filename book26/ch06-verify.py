#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Pablo Nogueira Grossi / G6 LLC
"""
book26/ch06-verify.py -- book26/ch06-what-a-collaborator-found.html: what a collaborator studied, what the author did with her data,
what she said, and what changed. Run first (R24).    python3 book26/ch06-verify.py
  [1] sections S1..S4 in order
  [2] labels: exploratory, not a test; no table values shown; permission to name her pending; not peer-reviewed; paper not read in full
  [3] kept out: her name, institution and the paper citation (permission pending); her table values, employer names, network/storage/form
  [4] links to ch05 exist; the seven review points D1..D7 each present as a numbered item
  [5] controls: each check fails on a damaged copy
  [HONESTY] what this does not establish
"""
import re, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
PAGE = HERE / "ch06-what-a-collaborator-found.html"
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
LABELS = ["not a test", "no table values", "permission to name her is pending", "not peer-reviewed", "not read in full", "has not reviewed or endorsed the mathematics"]
NAMES = ["sousa", "zilacleide", "zila", "uerj", "catalysis today"]
PRIVATE = ["73.70", "81.44", "86.22", "88.89", "26.36", "28.65", "15.71", "18.01", "17.25", "27.43", "98.22", "98.01"]
BANNED = ["ernst", "secaucus", "baruch", "rutgers", "jpmorgan", "banco do brasil", "tishman", "speyer"]
def secs_ok(t): return re.findall(r'<div class="sec" data-n="([^"]+)">', t) == SECS
def labels_ok(t):
    p = plain(t).lower(); return all(l in p for l in LABELS)
def clean_ok(t):
    return not any(b in t.lower() for b in BANNED) and not any(v in t for v in PRIVATE) and not any(f in t for f in FORBIDDEN)
def unnamed_ok(t): return not any(n in t.lower() for n in NAMES)
def points_ok(t): return re.findall(r'<li data-d="(D[1-7])">', t) == ["D%d" % i for i in range(1, 8)]
def links_ok(t):
    return 'href="ch05-proposal-with-a-test-that-can-fail.html"' in t and (HERE / "ch05-proposal-with-a-test-that-can-fail.html").exists()
def main():
    t = PAGE.read_text(encoding="utf-8") if PAGE.exists() else ""
    check("page exists", bool(t))
    if not t:
        print("\nFAILED: page absent"); sys.exit(1)
    check("sections S1..S4 in order", secs_ok(t))
    check("all required labels present", labels_ok(t))
    check("no table values, employer names, network/storage/form", clean_ok(t))
    check("collaborator, institution and paper are NOT named (permission pending)", unnamed_ok(t))
    check("review points D1..D7 present in order", points_ok(t))
    check("link to ch05 present and the file exists", links_ok(t))
    ctl = []
    def control(name, damaged, fn):
        ok = fn(damaged); print(("PASS " if not ok else "FAIL ") + "control rejected: " + name)
        if ok: ctl.append(name)
    control("section removed", t.replace('data-n="S2"', 'data-n="X"'), secs_ok)
    control("label removed", re.sub("(?i)not a test", "zzz", t), labels_ok)
    control("table value pasted in", t + " 81.44 ", clean_ok)
    control("her name pasted in", t + " Zilacleide Sousa ", unnamed_ok)
    control("review point removed", t.replace('data-d="D4"', 'data-d="X"'), points_ok)
    control("ch05 link broken", t.replace("ch05-proposal", "ch99-proposal"), links_ok)
    print("[HONESTY] Checks structure, labels and exclusions. It does not show the collaborator agreed to any of this, that the transcriptions are right, or that the law holds or fails.")
    if FAIL or ctl:
        print(f"\nFAILED: {len(FAIL)} check(s), {len(ctl)} control(s) not rejected"); sys.exit(1)
    print("\nALL PASS")
main()
