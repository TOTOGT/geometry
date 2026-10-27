#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Pablo Nogueira Grossi / G6 LLC
"""
book26/ch07-verify.py -- book26/ch07-two-postings-one-employer.html: two recruiting-coordinator postings compared.
  [1] sections S1..S4 in order   [2] labels present   [3] no employer names   [4] posted figures match the source texts
  [5] controls: each check fails on a damaged copy   [HONESTY] what this does not establish
"""
import re, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
PAGE = HERE / "ch07-two-postings-one-employer.html"
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
SECS = ["S1", "S2", "S3", "S4"]
LABELS = ["does not show that they are the same role", "an inference", "not offers", "no outside source was read", "two postings, treated as possibly one role"]
BANNED = ["citadel", "north bridge", "chicago", "stetson"]
FIGS = ["$85K", "$110", "120K", "$75", "95K", "2026-11-09", "12:59 AM", "Hudson Yards", "Midtown Manhattan", "two-year"]
FORBIDDEN = ["fetch(", "XMLHttpRequest", "localStorage", "<form", "action="]
def secs_ok(t): return re.findall(r'<div class="sec" data-n="([^"]+)">', t) == SECS
def labels_ok(t):
    p = plain(t).lower(); return all(l in p for l in LABELS)
def names_ok(t): return not any(b in t.lower() for b in BANNED) and not any(f in t for f in FORBIDDEN)
def figs_ok(t):
    p = plain(t).lower(); return all(f.lower() in p for f in FIGS)
def main():
    t = PAGE.read_text(encoding="utf-8") if PAGE.exists() else ""
    check("page exists", bool(t))
    if not t:
        print("\nFAILED: page absent"); sys.exit(1)
    check("sections S1..S4 in order", secs_ok(t))
    check("required labels present", labels_ok(t))
    check("no employer or agency names, no network/storage/form", names_ok(t))
    check("posted figures and places present as in the source texts", figs_ok(t))
    ctl = []
    def control(name, damaged, fn):
        ok = fn(damaged); print(("PASS " if not ok else "FAIL ") + "control rejected: " + name)
        if ok: ctl.append(name)
    control("section removed", t.replace('data-n="S3"', 'data-n="X"'), secs_ok)
    control("label removed", t.replace("an inference", "a fact"), labels_ok)
    control("employer name pasted in", t + " Citadel ", names_ok)
    control("agency name pasted in", t + " North Bridge ", names_ok)
    control("pay figure changed", t.replace("$85K", "$99K"), figs_ok)
    print("[HONESTY] Checks structure, labels, exclusions and that the quoted figures are present. It does not show the postings are one role, that the figures are current, or that anything was sent.")
    if FAIL or ctl:
        print(f"\nFAILED: {len(FAIL)} check(s), {len(ctl)} control(s) not rejected"); sys.exit(1)
    print("\nALL PASS")
main()
