#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Pablo Nogueira Grossi / G6 LLC
"""
book22/ch01-verify.py -- what Book XXII's two pages must contain. Run first (R24).
    python3 book22/ch01-verify.py
Standard library only. No external source is used, so this checks STRUCTURE, not truth.
  [1] index.html carries every glossary term and every Portuguese counterpart
  [2] ch01 carries sections 1, 2, 2-A, 3, 3-A, 4, 5, 6, each in English AND Portuguese
  [3] the satire and unverified-claims labels are on the page
  [4] each check is run against a damaged copy and must FAIL (control)
  [HONESTY] what this does not establish
"""
import re, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
FAIL = []
def check(label, ok, detail=""):
    print(("PASS " if ok else "FAIL ") + label + (f"  -- {detail}" if detail else ""))
    if not ok: FAIL.append(label)

TERMS = ["ELA", "EFL", "ESL", "ELL", "EAL", "ENL", "ELD", "ESOL", "Heritage speaker", "World Languages",
         "Língua Portuguesa", "PLE", "PL2", "PLAc", "PLA", "PFOL", "PLH",
         "Português como Língua Adicional", "Português como Língua Estrangeira",
         "Português como Segunda Língua", "Português como Língua de Acolhimento",
         "Português como Língua de Herança", "Português para Falantes de Outras Línguas"]
SECTIONS = ["1", "2", "2-A", "3", "3-A", "4", "5", "6"]

def plain(t): return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", t))

def missing_terms(text):
    p = plain(text)
    return [t for t in TERMS if t not in p]

def section_map(text):
    out = {}
    for m in re.finditer(r'<div class="sec" data-n="([^"]+)">(.*?</div>)\s*</div>\s*(?=<div class="sec"|<!--end-secs-->)', text, re.S):
        n, body = m.group(1), m.group(2)
        en = re.search(r'<div lang="en">(.*?)</div>', body, re.S)
        pt = re.search(r'<div lang="pt">(.*?)</div>', body, re.S)
        out[n] = (bool(en and plain(en.group(1)).strip()), bool(pt and plain(pt.group(1)).strip()))
    return out

def sections_ok(text):
    sm = section_map(text)
    return list(sm) == SECTIONS and all(a and b for a, b in sm.values())

idx_p, ch_p = HERE / "index.html", HERE / "ch01-notice-to-participants.html"
print("[1] glossary on index.html")
if idx_p.exists():
    idx = idx_p.read_text(encoding="utf-8")
    miss = missing_terms(idx)
    check("every glossary term and Portuguese counterpart is on the page", not miss, ", ".join(miss))
else:
    idx = ""; check("index.html exists", False)
print("[2] sections on ch01")
if ch_p.exists():
    ch = ch_p.read_text(encoding="utf-8")
    check("sections are exactly 1, 2, 2-A, 3, 3-A, 4, 5, 6, each with EN and PT text", sections_ok(ch),
          str(list(section_map(ch))))
else:
    ch = ""; check("ch01 exists", False)
print("[3] labels")
check("ch01 says it is satire and invented", "satire" in ch.lower() and "invented" in ch.lower())
check("ch01 says the Specialist's claims are not fact-checked", "not been fact-checked" in plain(ch))
check("index.html says its definitions are not yet sourced", "not yet checked against" in plain(idx))
print("[4] controls: each check must fail on a damaged copy")
check("control: removing 'PLAc' from the glossary is caught", "PLAc" in missing_terms(idx.replace("PLAc", "")) if idx else False)
dam = re.sub(r'<div lang="pt">.*?</div>', '<div lang="pt"></div>', ch, count=1, flags=re.S) if ch else ""
check("control: emptying one Portuguese paragraph is caught", bool(ch) and not sections_ok(dam))
dam2 = ch.replace('data-n="3-A"', 'data-n="3-B"') if ch else ""
check("control: renaming a section is caught", bool(ch) and not sections_ok(dam2))
print("[HONESTY] This checks that the text is present and aligned. It does not check that any definition is correct,")
print("  that Julia's name etymology is right, or that the Michigan claims are false. Those are labelled on the pages as unverified.")
print("\nFAILED: " + ", ".join(FAIL) if FAIL else "\nALL PASS")
sys.exit(1 if FAIL else 0)
