#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Pablo Nogueira Grossi / G6 LLC
"""
book14/ch07-verify.py -- every quotation and number on book14/ch07-maximum-meaning.html. Run first (R24).
    python3 book14/ch07-verify.py [--downloads DIR]
  [1] Briggs (1985), the sentences the page quotes, on the printed pages it cites (printed = PDF + 31)
  [2] compression: words in the Sanskrit sentence, the English, and the grammarian's paraphrase
  [3] word order: all orders of the seven-word rice sentence give the same karaka triples (toy analyser)
  [4] Malba Tahan, The Man Who Counted (English, 105-page PDF): the sentences quoted; the 35 camels in exact fractions
  [HONESTY]
"""
import itertools, os, re, subprocess, sys
from pathlib import Path
FAIL = []
def check(label, ok, detail=""):
    print(("PASS " if ok else "FAIL ") + label + (f"  -- {detail}" if detail else ""))
    if not ok: FAIL.append(label)
def dl():
    if "--downloads" in sys.argv: return Path(sys.argv[sys.argv.index("--downloads") + 1])
    for c in ("~/mnt/Downloads", "~/Downloads"):
        p = Path(os.path.expanduser(c))
        if p.is_dir(): return p
pdf = dl() / "466-Article Text-466-1-10-20080128.pdf"
pages = subprocess.run(["pdftotext", str(pdf), "-"], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True).stdout.split("\f")
norm = lambda s: re.sub(r"\s+", " ", s.replace("’", "'").replace("“", '"').replace("”", '"')).strip()

print("[1] Briggs, 'Knowledge Representation in Sanskrit and Artificial Intelligence', AI Magazine 6(1), 1985")
check("held: 8 printed pages, 32-39", len([p for p in pages if p.strip()]) == 8)
for pr in (32, 33, 37, 38, 39):
    t = norm(pages[pr - 32])
    check(f"printed p.{pr} is PDF p.{pr-31}", f"{pr} THE AI MAGAZINE" in t or f"Spring, 1985 {pr}" in t)
Q = [(32, "natural language can serve as an artificial language also"),
     (32, "much work in AI has been reinventing"),
     (34, "has a deviation of zero"),
     (34, "It is a terse, very condensed form of Sanskrit, which paradoxically at times becomes so abstruse that a commentary is necessary to clarify it"),
     (34, "brief, algebraic formulations"),
     (35, "cannot be applied to the solitary point reached by extreme subdivision"),
     (36, "in a remarkably concise way"),
     (36, "Agent, Object, Instrument, Recipient, Point of Departure, Locality"),
     (38, "often apparently redundant way"),
     (39, "computer scientists without the hardware")]
for pr, q in Q:
    check(f'p.{pr}: "{q[:60]}"', norm(q) in norm(pages[pr - 32]))

print("[2] compression")
sk = "graamam gacchati caitra"                     # (1), p.34, as transliterated in the article
en = "Caitra goes to the village"
para = ("There is an activity which leads to a connection-activity which has as Agent no one other than Caitra, "
        "specified by singularity, [which] is taking place in the present and which has as Object something not "
        "different from 'village'")
check("the paraphrase (2) is printed on p.34", norm("which has as Agent no one other than Caitra") in norm(pages[2]))
w = lambda s: len(s.split())
print(f"     Sanskrit {w(sk)} words; English {w(en)}; the grammarian's paraphrase {w(para)}")
check("3 Sanskrit words unfold to 38 in the grammarian's paraphrase (about 13x)", (w(sk), w(para)) == (3, 38))

print("[3] word order (toy analyser, this sentence's endings only)")
SENT = "Maitrah sauhardyat Devadattaya odanam ghate agnina pacati".split()   # p.38
check("the Sanskrit sentence is printed on p.38", norm("Devadattaya odanam") in norm(pages[6]))
ENDINGS = [("aya", "recipient"), ("at", "because-of"), ("ah", "agent"), ("am", "object"),
           ("na", "instrument"), ("e", "locality"), ("ti", "VERB")]
def analyse(words):
    verb = next(x for x in words if x.endswith("ti"))
    out = set()
    for x in words:
        if x is verb: continue
        role = next(r for e, r in ENDINGS if x.endswith(e))
        out.add((verb, role, x))
    return frozenset(out)
base = analyse(SENT)
for t in sorted(base): print("     ", t)
orders = list(itertools.permutations(SENT))
same = all(analyse(list(o)) == base for o in orders)
check(f"all {len(orders):,} orders give the same six triples", same and len(orders) == 5040 and len(base) == 6)

print("[4] Malba Tahan, The Man Who Counted")
from fractions import Fraction as Fr
MW = subprocess.run(["pdftotext", "-layout", str(dl() / "themanwhocounted.pdf"), "-"], stdout=subprocess.PIPE,
                    stderr=subprocess.DEVNULL, text=True).stdout.split("\f")
sq = lambda s: re.sub(r"\s+", "", s.replace("-\n", "").replace("’", "'").replace("“", '"').replace("”", '"')).lower()
MQ = [(1, "THE MAN WHO COUNTED A Collection of Mathematical Adventures MALBA TAHAN"),
      (2, "My name is Beremiz Samir. I was born in the little village of Khoi, in Persia"),
      (4, "Of the singular episode of the thirty-five camels that were to be divided between three Arab brothers"),
      (4, "half of them belong to me"),
      (4, "and one-ninth to Harim, the youngest"),
      (5, "18 + 12 + 4 = 34 camels"),
      (5, "The other rightly belongs to me for having resolved the complicated problem of the inheritance")]
for pg, q in MQ:
    check(f'Tahan PDF p.{pg}: "{q[:56]}"', sq(q) in sq(MW[pg - 1]))
alltxt = " ".join(MW)
check("the PDF (104 pages of text) has no front matter: no translator, publisher or author's real name",
      len([p for p in MW if p.strip()]) == 104 and not re.search(r"Mello|Souza|Sousa|Norton|translated by", alltxt, re.I))
w = [Fr(1, 2), Fr(1, 3), Fr(1, 9)]
check("the father's shares 1/2 + 1/3 + 1/9 add to 17/18, not 1", sum(w) == Fr(17, 18))
s35 = [x * 35 for x in w]; s36 = [x * 36 for x in w]
check("of 35: 17 1/2, 11 2/3, 3 8/9, together 33 1/18", s35 == [Fr(35, 2), Fr(35, 3), Fr(35, 9)] and sum(s35) == Fr(595, 18))
check("of 36: 18, 12, 4, together 34, leaving 2", s36 == [18, 12, 4] and 36 - sum(s36) == 2)
ok = [n for n in range(1, 200) if all((x * (n + 1)).denominator == 1 for x in w)]
check("the lent camel makes every share whole exactly when N + 1 is a multiple of 18: N = 17, 35, 53, ...",
      ok == list(range(17, 200, 18)), str(ok[:5]))
check("…and then 18k - 17k = k camels are left over: for 17 the lender just gets his back; for 35 Beremiz earns one",
      all((n + 1) - sum(x * (n + 1) for x in w) == (n + 1) // 18 for n in ok))
check("every brother gets more than the will gave him, at N = 35", all(b > a for a, b in zip(s35, s36)))

print("[HONESTY]")
print("  [3] is a toy keyed to the endings of one sentence, not a Sanskrit parser; it shows what case")
print("  marking buys, not that the grammarians' analysis is complete. Briggs' closing claims about zero and")
print("  binary numbers (p.39) are his and are not checked here. Briggs does not say Sanskrit is 'the best")
print("  language for computers'; nothing on these eight pages says so. [4]: the PDF of The Man Who Counted")
print("  has no front matter, so the hoax history on the page is cited from A. Bellos (Guardian, 9 May 2014),")
print("  which was pasted into the working session and is not held as a file.")
print(f"\n{len(FAIL)} FAIL" + (": " + ", ".join(FAIL) if FAIL else ""))
sys.exit(1 if FAIL else 0)
