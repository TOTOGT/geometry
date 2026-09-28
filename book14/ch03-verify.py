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
  [5] Carroll himself: Alice's Adventures in Wonderland (Zelchenko's replica of the 1865 edition), ch. IX, pp. 142-146:
      the Mock Turtle's thirteen school subjects against their real names; the lessons that lessen
  [6] Gardner, The Annotated Alice (Definitive Edition, Norton 2000): Looking-Glass ch. 6 in Carroll's own
      text; Gardner's note on Humpty Dumpty (nominalism) and on the twelfth day (negative numbers)
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

import hashlib
img = ROOT / "book14/img/tenniel-queen-of-hearts.png"
check("the Tenniel engraving shown on the page is the one supplied (sha256 a0832fb3e60fbf05...)",
      img.exists() and hashlib.sha256(img.read_bytes()).hexdigest().startswith("a0832fb3e60fbf05"))

print("[5] Carroll: Alice's Adventures in Wonderland, ch. IX (replica of the 1865 edition, held)")
AW = next((f for f in sorted(dl.iterdir()) if f.name.lower().startswith("alice_in_wonderland") and f.suffix == ".pdf"), None)
check("Alice's Adventures in Wonderland is held", AW is not None, AW.name if AW else "")
def aw(a, b): return subprocess.run(["pdftotext", "-f", str(a), "-l", str(b), str(AW), "-"], capture_output=True, text=True).stdout
front, ch9 = aw(1, 3), aw(79, 81)
check("it is Zelchenko's replica of the first edition: 'exact digital replica of Lewis Carroll’s first edition'",
      sq("exact digital replica of Lewis Carroll’s first edition") in sq(front))
for q in ["“Reeling and Writhing, of course, to begin with,” the Mock Turtle replied",
          "the different branches of Arithmetic—Ambition, Distraction, Uglification, and Derision.",
          "“Mystery, ancient and modern, with Seaography: then Drawling",
          "he taught us Drawling, Stretching, and Fainting in Coils.",
          "he taught Laughing and Grief, they used to say.",
          "“Ten hours the first day,” said the Mock Turtle : “nine the next, and so on.”",
          "“That ’s the reason they ’re called lessons,” the Gryphon remarked : “because they lessen from day to day.”",
          "“Then the eleventh day must have been a holiday ?”",
          "“And how did you manage on the twelfth ?” Alice went on eagerly.",
          "“That ’s enough about lessons,” the Gryphon interrupted in a very decided tone"]:
    check(f'Wonderland ch. IX: "{q[:60]}"', sq(q) in sq(ch9))
PUN = ["reeling", "writhing", "ambition", "distraction", "uglification", "derision", "mystery",
       "seaography", "drawling", "stretching", "fainting in coils", "laughing", "grief"]
REAL = ["reading", "writing", "addition", "subtraction", "multiplication", "division", "history",
        "geography", "drawing", "sketching", "painting in oils", "latin", "greek"]
nearest = {p: min(REAL, key=lambda r: (lev(p, r), r)) for p in PUN}
hits = sum(nearest[p] == r for p, r in zip(PUN, REAL))
print("     nearest real subject by edit distance:", {p: nearest[p] for p in PUN})
check(f"each of the 13 subjects is closest, by edit distance, to the real one it puns on: {hits}/13", hits == 13)
hours = [10 - d for d in range(12)]
check("lessons that lessen: 10, 9, ..., 1 hours is 55 hours; day 11 is 0 (the holiday); day 12 would be -1",
      sum(hours[:10]) == 55 and hours[10] == 0 and hours[11] == -1)

print("[6] Gardner, The Annotated Alice, the Definitive Edition (Norton, 2000)")
GA = dl / "annotated-alice.pdf"
check("The Annotated Alice is held", GA.exists())
def ga(a, b=None): return subprocess.run(["pdftotext", "-f", str(a), "-l", str(b or a), str(GA), "-"], capture_output=True, text=True).stdout
check("Definitive Edition, Norton, New York: 'Copyright© 2000, 1990, 1988, 1960 by Martin Gardner'",
      sq("Copyright© 2000, 1990, 1988, 1960 by Martin Gardner") in sq(ga(1, 3)))
g136 = ga(136)
for q in ['"When I use a word," Humpty Dumpty said, in rather a scornful tone, "it means just what I choose it to mean—neither more nor less."',
          '"The question is," said Alice, "whether you can make words mean so many different things."',
          '"But \'glory\' doesn\'t mean \'a nice knock-down argument,\' " Alice objected.',
          'particularly verbs: they\'re the proudest—adjectives you can do anything with, but not verbs']:
    check(f'Looking-Glass ch. 6 (Gardner PDF p.136): "{q[:58]}"', sq(q) in sq(g136))
g320 = ga(320)
for q in ["Lewis Carroll was fully aware of the profundity in Humpty Dumpty's whimsical discourse on semantics",
          "Humpty takes the point of view known in the Middle Ages as nominalism",
          'Even in logic and mathematics, where terms are usually more precise than in other subject matters, enormous confusion often results from a failure to realize that words mean "neither more nor less" than what they are intended to mean',
          "Carroll answers these questions at some length on page 165 of his Symbolic Logic",
          "it is straight from the broad mouth of Humpty Dumpty"]:
    check(f'Gardner, Looking-Glass ch. 6 note 11 (PDF p.320): "{q[:52]}"', sq(q) in sq(g320))
g252 = ga(252)
check('Gardner, Wonderland ch. IX note 19 (PDF p.252): "Alice\'s excellent question rightly puzzles the Gryphon because it introduces the possibility of mysterious negative numbers"',
      sq("Alice's excellent question rightly puzzles the Gryphon because it introduces the possibility of mysterious negative numbers") in sq(g252))
check('…"On the twelfth day and succeeding days did the pupils start teaching their teacher?"',
      sq("On the twelfth day and succeeding days did the pupils start teaching their teacher?") in sq(g252))

print("[HONESTY]")
print("  SemCor is a sense-tagged part of the Brown Corpus (American prose, 1961); counts are small and dated. A count of 0 means")
print("  unattested in SemCor, not absent from English. Which WordNet synset is the template's head")
print("  is our judgement, stated per row. The co-predication table in Polysemy.lean is an input,")
print("  not a corpus result. Lean checks the counting logic, not the linguistics. [4] quotes the letter; [5] and")
print("  [6] check Carroll's own text (Wonderland replica; Looking-Glass in Gardner). The pairing of the")
print("  Mock Turtle's branches with the operations is the reader's pun, measured, not stated in the letter.")
print("  The Tenniel image came with an AI-generated summary (illustration counts, the recalled 1865")
print("  printing, the 1890 Nursery Alice); none of that is used, because no held source states it.")
print(f"\n{len(FAIL)} FAIL" + (": " + ", ".join(FAIL) if FAIL else ""))
sys.exit(1 if FAIL else 0)
