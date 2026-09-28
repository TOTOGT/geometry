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
  [4] Humpty Dumpty and Alice, from L. Schrieber's letter (Notices AMS 71(6), 2024, p. 704): quotes; the
      Mock Turtle's four branches against the four operations by edit distance; WordNet senses of the letter's words
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

print("[4] Humpty Dumpty and Alice (Schrieber, Notices of the AMS 71(6), June/July 2024, p. 704)")
import os, subprocess, itertools
dl = next((Path(os.path.expanduser(c)) for c in ("~/mnt/Downloads", "~/Downloads") if Path(os.path.expanduser(c)).is_dir()), None)
letter = next((f for f in sorted(dl.iterdir()) if f.name.lower().startswith("202406fullissue") and f.suffix == ".pdf"), None)
check("the June/July 2024 Notices is held", letter is not None, letter.name if letter else "")
L = subprocess.run(["pdftotext", "-f", "6", "-l", "6", str(letter), "-"], capture_output=True, text=True).stdout
sq = lambda s: re.sub(r"\s+", "", s.replace("-\n", "")).lower()
for q in ["LETTERS TO THE EDITOR",
          "Charles Dodgson, who is hardly remembered as an Oxford mathematician",
          "I once heard a story, possibly apocryphal, that Queen Victoria",
          "we find this characterization of what a mathematical definition is",
          "“When I use a word,” Humpty Dumpty said in rather a scornful tone, “it means just what I choose it to mean—neither more nor less.”",
          "“The question is,” said Alice, “whether you can make words mean so many different things.”",
          "“The question is,” said Humpty Dumpty, “which is to be master—that’s all.”",
          "Who among us, trying to prove some theorem, has not experienced this exact phenomenon?",
          "the different branches of Arithmetic—Ambition, Distraction, Uglification and Derision",
          "Leonard Schrieber", "DOI: https://doi.org/10.1090/noti2952",
          "704 NOTICES OF THE AMERICAN MATHEMATICAL SOCIETY VOLUME 71, NUMBER 6"]:
    check(f'letter p.704: "{q[:62]}"', sq(q) in sq(L))
def lev(a, b):
    d = list(range(len(b) + 1))
    for i, x in enumerate(a, 1):
        p, d[0] = d[0], i
        for j, y in enumerate(b, 1):
            p, d[j] = d[j], min(d[j] + 1, d[j - 1] + 1, p + (x != y))
    return d[-1]
MT = ["ambition", "distraction", "uglification", "derision"]
OPS = ["addition", "subtraction", "multiplication", "division"]
costs = {perm: sum(lev(a, b) for a, b in zip(MT, perm)) for perm in itertools.permutations(OPS)}
best = min(costs, key=costs.get)
print("     edit distances:", {a: lev(a, b) for a, b in zip(MT, OPS)}, " total", costs[tuple(OPS)])
check("of the 24 ways to pair the Mock Turtle's branches with the four operations, the one with the least total edit distance is Ambition-Addition, Distraction-Subtraction, Uglification-Multiplication, Derision-Division",
      best == tuple(OPS) and sorted(costs.values())[0] < sorted(costs.values())[1], f"{costs[tuple(OPS)]} vs next {sorted(costs.values())[1]}")
ws = {w: len(wn.synsets(w, pos=wn.NOUN)) for w in ("word", "question", "master", "definition")}
print("     WordNet noun senses:", ws)
check("WordNet noun senses: word 10, master 10, question 6, definition 2 (Alice's point, counted)",
      ws == {"word": 10, "question": 6, "master": 10, "definition": 2}, str(ws))

print("[HONESTY]")
print("  SemCor is a sense-tagged part of the Brown Corpus (American prose, 1961); counts are small and dated. A count of 0 means")
print("  unattested in SemCor, not absent from English. Which WordNet synset is the template's head")
print("  is our judgement, stated per row. The co-predication table in Polysemy.lean is an input,")
print("  not a corpus result. Lean checks the counting logic, not the linguistics. [4] quotes Carroll")
print("  through Schrieber's letter, not from a held edition of the Alice books; the pairing of the")
print("  Mock Turtle's branches with the operations is the reader's pun, measured, not stated in the letter.")
print(f"\n{len(FAIL)} FAIL" + (": " + ", ".join(FAIL) if FAIL else ""))
sys.exit(1 if FAIL else 0)
