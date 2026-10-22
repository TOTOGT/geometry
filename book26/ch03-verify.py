#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Pablo Nogueira Grossi / G6 LLC
"""
book26/ch03-verify.py -- book26/ch03-computer-room.html, a first-person account (told as "the author") of a cooling failure
in a bank branch computer room, and what it does and does not show. Run first (R24).
    python3 book26/ch03-verify.py
Standard library only. Checks STRUCTURE, the stated facts, the labels, and what is kept out. It cannot check that the account is true:
every fact on the page is the author's own statement, and the page says so.
  [1] sections S1..S6 exist, in order
  [2] the author's stated facts are present (room could not be warm; ATMs and mainframes; alarm; portable unit bought on a personal card;
      cooling "kind of" before 5am; many firms to fix it; promotion to corporate banking relationship manager; branch closed after the author left;
      head office wanted it closed; every firm said start from scratch)
  [3] labels: "the author's account"; not engineering; not sales experience; does not say the cooling caused the closure; reimbursement not recorded
  [4] kept out: no employer or landlord or retailer or school name; nothing about the outside candidate beyond "an outside candidate";
      no employer token from Chapter 1's hashed list
  [5] privacy: no network call, no storage, no form action
  [6] controls: each check fails on a damaged copy
  [HONESTY] what this does not establish
"""
import re, sys, hashlib, ast
from pathlib import Path
HERE = Path(__file__).resolve().parent
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
FORBIDDEN = ["fetch(", "XMLHttpRequest", "sendBeacon", "localStorage", "sessionStorage", "indexedDB", "document.cookie", "WebSocket", "<form", "action="]
SECS = ["S1", "S2", "S3", "S4", "S5", "S6"]
FACTS = ["could not be warm", "ATMs", "mainframe", "alarm", "2am", "3am", "portable air-conditioning unit", "personal card",
         "kind of", "before 5am", "many firms", "relationship manager", "after the author left", "head office wanted", "start from scratch"]
LABELS = ["the author's account", "not engineering", "not sales experience", "does not say", "not recorded"]
BANNED = ["tishman", "speyer", "boeing", "walmart", "wal-mart", "staubli", "stäubli", "jpmorgan", "chase", "banco", "brasil", "brazil",
          "mit", "mba", "director", "baruch", "nga", "rutgers"]

def secs_ok(text):
    got = re.findall(r'<div class="sec" data-n="([^"]+)">', text)
    return got == SECS
def facts_ok(text):
    p = plain(text).lower()
    return all(f.lower() in p for f in FACTS)
def labels_ok(text):
    p = plain(text).lower()
    return all(l.lower() in p for l in LABELS)
def banned_ok(text):
    words = set(re.findall(r"[a-zäö\-]+", plain(text).lower()))
    return not any(b in words for b in BANNED)
def hashes():
    src = (HERE / "ch01-verify.py").read_text(encoding="utf-8")
    m = re.search(r"EMPLOYER_HASHES\s*=\s*set\((\{.*?\})\)", src, re.S)
    return ast.literal_eval(m.group(1)) if m else set()
def hash_ok(text):
    H = hashes()
    if not H: return False
    ws = set(re.findall(r"[a-z][a-z']+", plain(text).lower()))
    return not any(hashlib.sha256(w.encode()).hexdigest() in H for w in ws)
def privacy_ok(text):
    return not any(w in text for w in FORBIDDEN) and "<script" not in text

path = HERE / "ch03-computer-room.html"
if not path.exists():
    check("page exists: book26/ch03-computer-room.html", False, "not written yet")
    print("\nFAILED: " + ", ".join(FAIL)); sys.exit(1)
t = path.read_text(encoding="utf-8")
print("[1] sections"); check("six sections S1..S6 in order", secs_ok(t))
print("[2] stated facts"); check("every stated fact is present", facts_ok(t))
print("[3] labels"); check("account / not engineering / not sales / not causal / reimbursement-not-recorded labels present", labels_ok(t))
print("[4] kept out")
check("no employer, landlord, retailer, school or outside-candidate detail", banned_ok(t))
check("no employer token from Chapter 1's hashed list (list loaded: %d)" % len(hashes()), hash_ok(t))
print("[5] privacy"); check("no network, storage, form action or script", privacy_ok(t))
print("[6] controls")
check("control: a missing section is caught", not secs_ok(t.replace('data-n="S3"', 'data-n="S3x"')))
check("control: a missing fact is caught", not facts_ok(t.replace("personal card", "card")))
check("control: a missing label is caught", not labels_ok(t.replace("not sales experience", "something")))
check("control: a landlord name is caught", not banned_ok(t.replace("</body>", "<p>Tishman</p></body>")))
check("control: an MBA detail about the outside candidate is caught", not banned_ok(t.replace("</body>", "<p>an MBA</p></body>")))
check("control: an injected fetch( is caught", not privacy_ok(t.replace("</body>", "<script>fetch('/x')</script></body>")))
print("[HONESTY] This checks structure, labels and what is left out. It does not check that the account is true; it is the author's statement,")
print("  with no documents attached. It does not check why the branch closed, whether the author was reimbursed, or what the firms quoted.")
print("\nFAILED: " + ", ".join(FAIL) if FAIL else "\nALL PASS")
sys.exit(1 if FAIL else 0)
