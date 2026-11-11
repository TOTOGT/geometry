#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Pablo Nogueira Grossi / G6 LLC
"""
ch-imrad-guide-verify.py -- ch-imrad-guide.html (English for Researchers support chapter, weeks 9 to 11): a retelling of
Ecarnot et al., "Writing a scientific article: A step-by-step guide for beginners", Eur Geriatr Med 2015.
  [1] structure: sections present, local links resolve, no script/form/network/storage code
  [2] the tense table on the page equals the one typed here from the guide (8 rows)
  [3] the exercise answers agree with that table (exercise 1, five items)
  [4] the guide's numbers and lists appear as stated: 1 to 1.5 pages, 20 of 25 / 80 per cent, four abstract parts
  [5] SOURCE: no run of 8 words on the page is copied from the guide, IF a copy is held (pdftotext); else SKIP
  [6] controls: each check family fails on a corrupted input   [HONESTY]
  [7] honesty: the page says the guide is clinical and untested, claims no effect on acceptance, quotes no more than
      two titles, and lists its limits
Held copy: $GUIDE_PDF, else ~/Downloads/Writing_a_scientific_article__A_step-by-step_guide_for_beginners_.pdf.
Standard library only; the source check needs pdftotext.
"""
import os, re, subprocess, sys, html as _h
from pathlib import Path
HERE = Path(__file__).resolve().parent
PAGE = HERE / "ch-imrad-guide.html"
PDF = Path(os.environ.get("GUIDE_PDF", Path.home() / "Downloads" / "Writing_a_scientific_article__A_step-by-step_guide_for_beginners_.pdf"))
FAIL, SKIP = [], []
def check(label, ok, detail=""):
    print(("PASS " if ok else "FAIL ") + label + (f"  -- {detail}" if detail else ""))
    if not ok: FAIL.append(label)
def skip(label, why): print(f"SKIP {label}  -- {why}"); SKIP.append(label)
def visible(r):
    t = re.sub(r"<(script|style)[^>]*>.*?</\1>", "", r, flags=re.S)
    t = re.sub(r"<[^>]+>", " ", t)
    return re.sub(r"\s+", " ", _h.unescape(t))

raw = PAGE.read_text(encoding="utf-8"); txt = visible(raw)

# typed from the guide's Table 2 (tense for the introduction) and section 3.2/3.3 (methods, results)
TENSE = [("the current state of knowledge", "present"),
         ("what other authors observed", "past"),
         ("a process begun earlier and not yet finished", "present perfect"),
         ("something that has not been settled yet", "present perfect"),
         ("your hypothesis", "past for the first verb, present for the second"),
         ("your objective", "past"),
         ("your methods", "past; past perfect for events before your study"),
         ("your results", "past")]
EX1 = [("are", "present", "the current state of knowledge"), ("measured", "past", "what other authors observed"),
       ("has not been", "present perfect", "something that has not been settled yet"),
       ("hypothesized", "past", "your hypothesis"), ("aimed", "past", "your objective")]
SECTIONS = ["Part 1", "Part 2", "Part 3", "Part 4", "Part 5", "Part 6", "Limits"]

def c_structure(r):
    t = visible(r)
    ok = [(f"section label: {s}", f'class="section-label">{s}<' in r) for s in SECTIONS]
    ok.append(("no script/form/network/storage", not re.search(r"<script|<form|fetch\(|XMLHttpRequest|localStorage|sessionStorage", r)))
    ok.append(("four exercises", len(re.findall(r"<h3>Exercise \d", r)) == 4))
    return ok
def c_tense(t):
    return [(f"tense row: {a} -> {b}", re.search(re.escape(a) + r"\s+" + re.escape(b), t) is not None) for a, b in TENSE]
def c_ex1(t):
    ans = re.search(r"Check:\s*(.*?)\s*Exercise|Check:\s*(.*?)</p>", t)
    line = (ans.group(1) or ans.group(2)) if ans else t
    tmap = dict(TENSE)
    out = []
    for verb, tense, topic in EX1:
        first = tense.split(";")[0]
        rule_ok = tmap[topic].split(" for ")[0].split(";")[0] == first
        out.append((f"exercise 1 rule: {topic} is {first}", rule_ok))
        out.append((f"exercise 1 answer shows '{verb}' ({tense})", re.search(re.escape(verb) + r"[^.]*?\(" + re.escape(tense) + r"\)", line) is not None))
    return out
def c_numbers(t):
    return [("one to one and a half pages", "one to one and a half pages" in t),
            ("20 of 25 and 80 per cent", "20 of 25" in t and "80 per cent" in t),
            ("abstract has four parts", "four short parts" in t),
            ("introduction funnel has five steps", "five steps" in t),
            ("exercise 3 has two answers", "Two answers" in t)]
def c_honest(t):
    ok = [("says the guide is by physicians for clinical research", "physicians" in t and "clinical" in t),
          ("says the advice is untested here", "has not tested them" in t or "does not report a test" in t),
          ("claims no effect on acceptance", not re.search(r"guarantee|will get (your|a) paper accepted|improves? (your )?acceptance|proven to", t, flags=re.I)),
          ("says it reproduces nothing", "does not reproduce it" in t),
          ("limits listed", all(k in t for k in ["That the advice works", "That it fits every field", "The journals", "The guide itself in full"]))]
    ne = visible(re.sub(r'<div class="exercise">.*?</div>', "", raw, flags=re.S))   # exercise sentences are invented, not quotations
    quotes = re.findall(r"\u201c([^\u201d]{1,200})\u201d", ne)
    long_q = [q for q in quotes if len(q.split()) > 10 and "Writing a scientific article" not in q]
    ok.append(("no long quotation outside the exercises", len(long_q) == 0))
    return ok

def run(label, rs):
    for l, o in rs: check(f"{label} {l}", o)
print("== [1] structure"); run("[1]", c_structure(raw))
for l in sorted(set(re.findall(r'href="([^"#:]+\.html)"', raw))):
    check(f"[1] link resolves: {l}", (HERE / l).resolve().exists())
print("== [2] tense table"); run("[2]", c_tense(txt))
print("== [3] exercise answers"); run("[3]", c_ex1(txt))
print("== [4] numbers and lists"); run("[4]", c_numbers(txt))
print("== [7] honesty"); run("[7]", c_honest(txt))

print("== [5] source")
if PDF.exists():
    try:
        g = subprocess.run(["pdftotext", str(PDF), "-"], capture_output=True, text=True, timeout=60).stdout
        norm = lambda s: re.sub(r"[^a-z0-9 ]", "", re.sub(r"\s+", " ", s.lower().replace("ﬁ", "fi").replace("ﬂ", "fl")))
        own = re.sub(r"Writing a scientific article: A step-by-step guide for beginners", "", txt.split("Source F.")[0], flags=re.I)   # the cited title is a citation, not copied prose
        gw, pw = norm(g).split(), norm(own).split()
        sh = {" ".join(gw[i:i+8]) for i in range(len(gw) - 7)}
        hits = [" ".join(pw[i:i+8]) for i in range(len(pw) - 7) if " ".join(pw[i:i+8]) in sh]
        check("[5] no 8-word run copied from the guide", len(hits) == 0, f"{len(hits)} shared runs, first: {hits[:2]}")
    except Exception as e: skip("[5] source overlap", f"pdftotext failed: {e}")
else:
    skip("[5] source overlap", f"no held copy at {PDF}; set GUIDE_PDF")

print("== [6] controls")
def must_fail(label, rs):
    bad = [l for l, o in rs if not o]
    check(f"[6] control fails: {label}", len(bad) > 0, f"{len(bad)} check(s) fail as they should")
must_fail("tense table", c_tense(txt.replace("present perfect", "future")))
must_fail("exercise answers", c_ex1(txt.replace("has not been (present perfect)", "has not been (past)")))
must_fail("numbers", c_numbers(txt.replace("20 of 25", "21 of 25")))
must_fail("honesty (claim added)", c_honest(txt + " This advice is proven to get your paper accepted."))
must_fail("structure (script added)", c_structure(raw + "<script>fetch('x')</script>"))
print(); print(f"{len(FAIL)} FAIL, {len(SKIP)} SKIP"); sys.exit(1 if FAIL else 0)
