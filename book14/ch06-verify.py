#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Pablo Nogueira Grossi / G6 LLC
"""
book14/ch06-verify.py -- every number on book14/ch06-words-that-went-wrong.html. Run first (R24).
    python3 book14/ch06-verify.py
  [1] each entry's source still says what the lexicon says it says (WP-94, WP-61, CLAUDE.md rules)
  [2] usage now: how often each word appears across the published pages at a pinned commit,
      and whether the wrong use survives anywhere
  [HONESTY]
"""
import html, re, subprocess, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
PIN = "7a471e3"
FAIL = []
def check(label, ok, detail=""):
    print(("PASS " if ok else "FAIL ") + label + (f"  -- {detail}" if detail else ""))
    if not ok: FAIL.append(label)
def git(*a): return subprocess.run(["git", "--no-optional-locks", "-C", str(ROOT), *a],
                                   capture_output=True, text=True, errors="ignore").stdout
GEN = re.compile(r"<!--po-(run|gss|related|subject)-->.*?<!--/po-\1-->", re.S)
STY = re.compile(r"<(style|script)\b.*?</\1>", re.S | re.I)
def text(src): return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", STY.sub(" ", GEN.sub(" ", src)))))
RETIRED = ("docs/ml-evidence/", "_archive/", "_to_delete/")
pages = [f for f in git("ls-tree", "-r", "--name-only", PIN).split() if f.endswith(".html") and not f.startswith(RETIRED)]
T = {f: text(git("show", f"{PIN}:{f}")) for f in pages}
CL = git("show", f"{PIN}:CLAUDE.md")
print(f"[0] {len(pages)} published pages at {PIN}")

print("[1] the sources")
w94, w61 = T["book6/wp94-one-hole-five-words.html"], T["book6/wp61-root-language-sweep.html"]
check("WP-94: 'sorry' takes a bare numeral 905 times, 'gap' 26", "sorry 4,583 1,428.8 289 905" in w94 and "takes one 26 times" in w94)
check("WP-94: five communities, five words (sorry, sorry/oops, admit/Admitted, axiom, assumption)",
      all(w in w94 for w in ("sorry", "oops", "Admitted", "axiom", "assumption")))
check("WP-61: 'double root' ≠ 'degenerate' ≠ 'critical point'", "“double root” ≠ “degenerate” ≠ “critical point”" in w61)
check("WP-61: Theorem φ.1 was FALSE twice (not a root, and non-degenerate)", "Wrong twice over" in w61)
check("CLAUDE.md: 'Proved' belongs to the kernel-audited column only", '"Proved" belongs to the third column only' in CL)
check("CLAUDE.md: 'exactly' now carries the asymptotic qualifier", 'The word "exactly" now carries that qualifier' in CL)
check('CLAUDE.md: never write "there is no X" on one search', 'Never write "there is no X"' in CL)
check("CLAUDE.md: 666 is the printer's limit, not a resonance", "This is the printer's limit for this edition" in CL)
b19 = T["book19/index.html"]
check("Book XIX index: '110' was the count of files that exist", "which is the number of files that" in b19)
ch1 = T["book14/ch01-the-grammar-of-notation.html"]
check("Book XIV ch1: SS's own 'a rough indication' of a proof", "a rough indication of the lines along which a rigorous proof" in ch1)

print("[2] usage now")
QUOTING = {"book6/wp61-root-language-sweep.html", "book14/ch06-words-that-went-wrong.html",
           "book7/ch-huh.html"}   # ch-huh quotes the error in reporting WP-61 (use/mention, read 2026-09-27)
def pages_with(rx, skip=()):
    return sorted(f for f, t in T.items() if f not in skip and re.search(rx, t))
dd = pages_with(r"degenerate double root", QUOTING)
print(f"     'degenerate double root' outside WP-61: {dd}")
check("the WP-61 error phrase is used on no page (only quoted, in WP-61 and ch-huh)", len(dd) == 0, str(dd))
ndcp = pages_with(r"non-degenerate critical point")
print(f"     'non-degenerate critical point': {len(ndcp)} pages")
def count(rx): return sum(len(re.findall(rx, t)) for t in T.values())
C = {k: count(rx) for k, rx in [("Proved", r"\bProved\b"), ("proved", r"\bproved\b"), ("kernel-checked", r"kernel-checked"),
                                ("kernel-audited", r"kernel-audited"), ("sorry-free", r"sorry-free"),
                                ("there is no", r"\b[Tt]here is no\b"), ("did not find", r"\bdid not find\b"),
                                ("exactly", r"\bexactly\b")]}
for k, v in C.items(): print(f"     {k:16} {v:6,}")
EXPECT = dict(dd=0, ndcp=8, C={'Proved': 225, 'proved': 789, 'kernel-checked': 232, 'kernel-audited': 33,
              'sorry-free': 89, 'there is no': 322, 'did not find': 4, 'exactly': 1300})   # frozen at PIN
RES = dict(dd=len(dd), ndcp=len(ndcp), C=C)
print("     RESULT", RES)
for k, v in EXPECT.items():
    if v is not None: check(f"{k} = {v}", RES[k] == v, str(RES[k]))
check("'there is no' still outnumbers 'did not find'", C["there is no"] > C["did not find"])

print("[HONESTY]")
print("  Counts are string matches over visible text; they do not judge whether a given 'there is no'")
print("  is a one-search absence claim or a correct mathematical statement ('there is no rational")
print("  root'). The lexicon records rules and where they came from; it does not audit every use.")
print(f"\n{len(FAIL)} FAIL" + (": " + ", ".join(FAIL) if FAIL else ""))
sys.exit(1 if FAIL else 0)
