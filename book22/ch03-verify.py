#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Pablo Nogueira Grossi / G6 LLC
"""
book22/ch03-verify.py -- book22/ch03-ulqin.html, a short story. Run first (R24).
    python3 book22/ch03-verify.py
Standard library only. Checks STRUCTURE and the label; truth of the town facts is in ch02 (F7).
  [1] seven scenes S1..S7, each with English and Portuguese text
  [2] the fiction label is present, saying the town and word are real and the people invented
  [3] the story uses the word Ulqin in both languages and states the checked town facts
  [4] words that were REJECTED are absent: Ulgemisht (invented, collided with a real word),
      Ulqinisht (dialect name not found in any source read), Vashkorel (unused replacement)
  [5] controls: each check fails on a damaged copy
  [HONESTY] what this does not establish
"""
import re, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
FAIL = []
def check(label, ok, detail=""):
    print(("PASS " if ok else "FAIL ") + label + (f"  -- {detail}" if detail else ""))
    if not ok: FAIL.append(label)
def plain(t): return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", t))
SCENES = ["S1", "S2", "S3", "S4", "S5", "S6", "S7"]
BANNED = ["Ulgemisht", "Ulqinisht", "Vashkorel"]

def scenes_ok(text):
    got = {}
    for m in re.finditer(r'<div class="sec" data-n="([^"]+)">(.*?</div>)\s*</div>\s*(?=<div class="sec"|<!--end-secs-->)', text, re.S):
        body = m.group(2)
        en = re.search(r'<div lang="en">(.*?)</div>', body, re.S)
        pt = re.search(r'<div lang="pt">(.*?)</div>', body, re.S)
        got[m.group(1)] = bool(en and plain(en.group(1)).strip()) and bool(pt and plain(pt.group(1)).strip())
    return list(got) == SCENES and all(got.values())
def label_ok(text):
    p = plain(text)
    return "Fiction." in p and "real" in p and "invented" in p
def facts_ok(text):
    en = "".join(re.findall(r'<div lang="en">(.*?)</div>', text, re.S))
    pt = "".join(re.findall(r'<div lang="pt">(.*?)</div>', text, re.S))
    p = plain(text)
    return ("Ulqin" in plain(en) and "Ulqin" in plain(pt) and "Ulcinj" in p and "Montenegro" in p
            and "Albanian" in plain(en) and "albanês" in plain(pt))
def banned_present(text): return [w for w in BANNED if w in plain(text)]

p = HERE / "ch03-ulqin.html"
if p.exists():
    t = p.read_text(encoding="utf-8")
else:
    t = ""; check("ch03 exists", False)
print("[1] scenes"); check("scenes are exactly S1..S7, each with EN and PT text", bool(t) and scenes_ok(t))
print("[2] label"); check("fiction label is present", bool(t) and label_ok(t))
print("[3] word and facts"); check("Ulqin appears in both languages with the Ulcinj / Montenegro / Albanian facts", bool(t) and facts_ok(t))
print("[4] rejected words"); b = banned_present(t) if t else BANNED
check("no rejected word is on the page", bool(t) and not b, ", ".join(b))
print("[5] controls")
check("control: emptying a Portuguese scene is caught", bool(t) and not scenes_ok(re.sub(r'<div lang="pt">.*?</div>', '<div lang="pt"></div>', t, count=1, flags=re.S)))
check("control: removing the label is caught", bool(t) and not label_ok(t.replace("Fiction.", "Note.")))
check("control: dropping Montenegro is caught", bool(t) and not facts_ok(t.replace("Montenegro", "X")))
check("control: a banned word is caught", bool(t) and bool(banned_present(t + " Ulqinisht")))
print("[HONESTY] This checks that scenes are present and aligned, that the label is on, and that three rejected words are absent.")
print("  It does not check that the Portuguese reads naturally, that the story works, or that the town facts are right (ch02 F7 holds those).")
print("\nFAILED: " + ", ".join(FAIL) if FAIL else "\nALL PASS")
sys.exit(1 if FAIL else 0)
