#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Pablo Nogueira Grossi / G6 LLC
"""
book14/ch03-verify.py -- every number on book14/ch03-how-many-senses.html and in IJL v4 §5.5. Run first (R24).
    pip3 install nltk && python3 -c "import nltk; nltk.download('wordnet')"
    python3 book14/ch03-verify.py
  [1] WordNet 3.0 noun senses and their SemCor tag counts for the nouns the manuscript analyses
  [2] prediction (ii) of v3 ("the head sense is the most frequent") against those counts
  [3] the Lean file: the two counting rules, and that the gate runs it
  [HONESTY]
"""
import re, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
FAIL = []
def check(label, ok, detail=""):
    print(("PASS " if ok else "FAIL ") + label + (f"  -- {detail}" if detail else ""))
    if not ok: FAIL.append(label)
try:
    from nltk.corpus import wordnet as wn
    wn.synsets("book")
except Exception as e:
    print("needs nltk + WordNet data:\n  pip3 install nltk && python3 -c \"import nltk; nltk.download('wordnet')\"")
    sys.exit(2)

print("[1] WordNet", wn.get_version(), "- noun senses, SemCor counts per sense (lemma matched)")
def senses(w):
    return [(s.name(), s.lexname(), sum(l.count() for l in s.lemmas() if l.name().lower() == w))
            for s in wn.synsets(w, pos="n")]
NOUNS = ["book", "examination", "charge", "school", "newspaper", "chicken", "lamb", "bottle"]
T = {w: senses(w) for w in NOUNS}
for w in NOUNS:
    s = T[w]
    print(f"     {w:12} {len(s):2} senses; attested {sum(1 for x in s if x[2]):2}; counts {[x[2] for x in s if x[2]]}")
check("WordNet is 3.0 (SemCor counts are tied to it)", wn.get_version() == "3.0")
check("'charge': 15 noun senses, 7 attested in SemCor", len(T["charge"]) == 15 and sum(1 for x in T["charge"] if x[2]) == 7)
check("'charge': most frequent is the rush/attack sense (16), not financial (4)",
      T["charge"][0][:1] == ("charge.n.01",) and T["charge"][0][2] == 16 and T["charge"][2][2] == 4)
check("'book': the content sense (46) outnumbers the physical object (10)",
      T["book"][0][1] == "noun.communication" and T["book"][0][2] == 46 and T["book"][1][2] == 10)

print("[2] prediction (ii): the derivational head is the most frequent sense")
# (noun, synset the template takes as head C, reason) -- the head assignment is a judgement (MODEL)
HEAD = [("examination", "examination.n.01", "process before result (Grimshaw 1990)"),
        ("book", "book.n.02", "v3 §5.1 lists the physical object as Sense 1"),
        ("chicken", "chicken.n.02", "animal before meat (grinding)"),
        ("lamb", "lamb.n.01", "animal before meat (grinding)"),
        ("bottle", "bottle.n.01", "container before contents")]
held = 0
for w, head, why in HEAD:
    s = T[w]; top = max(s, key=lambda x: x[2])
    ok = top[0] == head; held += ok
    hc = next(x[2] for x in s if x[0] == head)
    print(f"     {w:12} head {head:18} {hc:3} | most frequent {top[0]:18} {top[2]:3} | {'holds' if ok else 'FAILS'}  ({why})")
check("prediction (ii) holds in 3 of 5 and fails in 2 (book, chicken)", held == 3)
ch = {x[0]: x[2] for x in T["chicken"]}
check("'chicken': meat 16 > animal 10, a derived sense outnumbering its source",
      ch["chicken.n.01"] == 16 and ch["chicken.n.02"] == 10)

print("[3] the Lean")
lean = (ROOT / "book14/Polysemy.lean").read_text(encoding="utf-8")
for t in ["classes_force_transitive", "three_readings_no_division", "leaves_le_pow", "depth_one_two"]:
    check(f"Polysemy.lean proves {t}", f"theorem {t}" in lean and f"#print axioms Polysemy.{t}" in lean)
check("no sorry in code", "sorry" not in re.sub(r"/-.*?-/|--[^\n]*", "", lean, flags=re.S))
check("Book14 is a lean_lib", "lean_lib Book14" in (ROOT / "lakefile.lean").read_text())

print("[HONESTY]")
print("  SemCor is a sense-tagged part of the Brown Corpus (American prose, 1961); counts are small and dated. A count of 0 means")
print("  unattested in SemCor, not absent from English. Which WordNet synset is the template's head")
print("  is our judgement, stated per row. The co-predication table in Polysemy.lean is an input,")
print("  not a corpus result. Lean checks the counting logic, not the linguistics.")
print(f"\n{len(FAIL)} FAIL" + (": " + ", ".join(FAIL) if FAIL else ""))
sys.exit(1 if FAIL else 0)
