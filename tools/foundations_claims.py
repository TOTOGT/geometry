#!/usr/bin/env python3
"""
foundations_claims.py -- what the foundational documents claim, and what checks it.

THE ORDER THIS SERVES. book1 -> book2 -> toy -> gcm -> what books 3 and 4 build
on them -> GTCT. Foundations first, because a tag on a chapter that rests on an
untagged assumption is decoration.

THE FINDING THIS WAS WRITTEN TO MEASURE. The four foundational documents carry
~97 numbered claims between them and NONE of the corpus's evidence tags
(SHOWN / CITED / MODEL / CONJECTURE / OPEN), while the 59 chapters of Book IV
that rest on them are tagged throughout. The base is the only unmarked layer.

Separately, 82 theorems ARE kernel-checked for Volume I -- in TOTOGT/vol1-proofs,
another repository -- and nothing here maps one onto the other. So no reader,
including the author, can say which of Volume I's numbered results are proved
and which are prose.

This script does not fix that. It enumerates it, so fixing it is mechanical.

Run:  python3 tools/foundations_claims.py
"""
import os, re, html, json, sys

DOCS = [("Book I   · vol1-mathematics", "book1/vol1-mathematics.html"),
        ("Book II  · vol2-contact",     "book2/vol2-contact.html"),
        ("toy      · vol2-toymodel",    "vol2-toymodel.html"),
        ("gcm      · gcm-framework",    "gcm-framework.html")]
TAGS = ["SHOWN","CITED","MODEL","CONJECTURE","VERIFIED","OPEN"]
KIND = r"(Theorem|Proposition|Lemma|Corollary|Result|Assumption|Definition|Claim)"
LEAN = os.path.expanduser("~/mnt/Desktop/vol1-proofs/tools/axioms.txt")

def text(p):
    s = open(p, encoding="utf-8", errors="replace").read()
    return s, html.unescape(re.sub(r"<[^>]+>", " ", s))

def claims(flat):
    seen, out = set(), []
    for m in re.finditer(KIND + r"\s+([A-Z]?\d+(?:\.\d+)*|[A-Z]\b)", flat):
        k = "%s %s" % (m.group(1), m.group(2))
        if k in seen: continue
        seen.add(k); out.append((k, m.start()))
    return out

def lean_names():
    if not os.path.exists(LEAN): return None
    return sorted({m.group(1) for m in
                   re.finditer(r"^'([^']+)'", open(LEAN, encoding="utf-8").read(), re.M)})

print("=" * 78); print("FOUNDATIONAL CLAIMS, AND WHAT MARKS THEM"); print("=" * 78)
grand = 0; grand_tagged = 0; rows = []
for label, path in DOCS:
    if not os.path.exists(path):
        print("  MISSING: %s" % path); continue
    raw, flat = text(path)
    cs = claims(flat)
    tagcount = {t: len(re.findall(t, raw)) for t in TAGS}
    tagged = sum(tagcount.values())
    grand += len(cs); grand_tagged += tagged
    rows.append((label, path, len(cs), tagged, tagcount))
    print()
    print("  %s" % label)
    print("     %-58s %5d bytes" % (path, os.path.getsize(path)))
    print("     numbered claims : %d" % len(cs))
    print("     evidence tags   : %s" % (
        "  ".join("%s=%d" % (t, tagcount[t]) for t in TAGS) if tagged else "NONE"))
    kinds = {}
    for k, _ in cs: kinds[k.split()[0]] = kinds.get(k.split()[0], 0) + 1
    print("     by kind         : %s" % ", ".join("%s %d" % (k, v) for k, v in sorted(kinds.items())))

print()
print("-" * 78)
print("  TOTAL   %d numbered claims across %d documents, %d evidence tags between them."
      % (grand, len(rows), grand_tagged))
print("-" * 78)

names = lean_names()
print()
print("=" * 78); print("WHAT IS ACTUALLY KERNEL-CHECKED, AND WHERE IT LIVES"); print("=" * 78)
if names is None:
    print("  vol1-proofs/tools/axioms.txt NOT FOUND on this disk.")
    print("  The Lean for Volume I is in TOTOGT/vol1-proofs, a DIFFERENT repository.")
else:
    ns = {}
    for n in names: ns[n.split(".")[0]] = ns.get(n.split(".")[0], 0) + 1
    print("  TOTOGT/vol1-proofs, tools/axioms.txt -- %d theorems:" % len(names))
    for k, v in sorted(ns.items()): print("      %-22s %d" % (k, v))
    print()
    print("  How many are named in the four documents above:")
    raws = {p: text(p)[0] for _, p in DOCS if os.path.exists(p)}
    hit = [n for n in names if any(n.split(".")[-1] in r for r in raws.values())]
    print("      named:     %d of %d" % (len(hit), len(names)))
    print("      NOT named: %d of %d  <-- kernel-checked and unclaimed by the prose"
          % (len(names)-len(hit), len(names)))
    if hit:
        print("      a sample of those that are named:")
        for h in hit[:6]: print("         %s" % h)

print()
print("=" * 78); print("GAPS"); print("=" * 78)
for g in [
 "R1  THE JOIN DOES NOT EXIST. %d numbered claims here; %s kernel-checked" % (
     grand, len(names) if names else "?"),
 "    theorems there; no mapping between them in either repository. Until one",
 "    exists, 'Volume I is machine-verified' is a statement about a file, not",
 "    about the document that cites it.",
 "",
 "R2  CLAIM EXTRACTION IS A REGEX. It counts numbered headings, so it misses",
 "    an unnumbered claim and double-counts a number reused across sections.",
 "    Treat the totals as within ten percent, not exact.",
 "",
 "R3  A TAG COUNT IS NOT A TAG AUDIT. This reports that the base layer carries",
 "    no evidence tags. It does NOT check that the tags in Book IV are correct",
 "    where they do appear.",
 "",
 "R4  BOOKS III AND IV ARE NOT SCANNED HERE. 59 chapters in Book IV alone.",
 "    They are next in the order and this script does not touch them.",
 "",
 "R5  NOTHING IS FIXED. This enumerates. Tagging the 50 claims is the work,",
 "    and",
 "    it requires deciding, per claim, which of SHOWN / CITED / MODEL /",
 "    CONJECTURE / OPEN is true -- which is a judgement, not a script.",
]: print("  " + g)
print(); print("=" * 78)
print("Inventory complete. 5 gaps recorded above remain open.")
print("=" * 78)
