#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Pablo Nogueira Grossi / G6 LLC
"""
book14/ch07-verify.py -- every quotation and number on book14/ch07-maximum-meaning.html. Run first (R24).
    python3 book14/ch07-verify.py [--downloads DIR]
  [1] Briggs (1985), the sentences the page quotes, on the printed pages it cites (printed = PDF + 31)
  [2] compression: words in the Sanskrit sentence, the English, and the grammarian's paraphrase
  [3] word order: all orders of the seven-word rice sentence give the same karaka triples (toy analyser)
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

print("[HONESTY]")
print("  [3] is a toy keyed to the endings of one sentence, not a Sanskrit parser; it shows what case")
print("  marking buys, not that the grammarians' analysis is complete. Briggs' closing claims about zero and")
print("  binary numbers (p.39) are his and are not checked here. Briggs does not say Sanskrit is 'the best")
print("  language for computers'; nothing on these eight pages says so.")
print(f"\n{len(FAIL)} FAIL" + (": " + ", ".join(FAIL) if FAIL else ""))
sys.exit(1 if FAIL else 0)
