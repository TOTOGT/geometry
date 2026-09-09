#!/usr/bin/env python3
"""
wp101-verify.py  --  regenerates the checkable content of
book6/wp101-prematurity-fold-event.html.

WP-101 maps the dm3 operator chain onto four biological thresholds disrupted by
preterm birth.  Its discipline is that two of the four domains are WITHDRAWN, and
a paper whose value is in what it refuses has to be right about the refusals.
This script checks the parts that can be checked without a laboratory:

  [1] the kernel-verified anchor, AXLE/AutophagyDm3_v2.lean -- declaration count,
      absence of `sorry`, absence of `True` conclusions, and every numeric claim
      the page reads off it, re-derived symbolically here rather than quoted;
  [2] CHEMICAL REACTION NETWORK THEORY, implemented from the definition.  The
      deficiency of a reaction network is d = n - l - s, and d >= 0 for EVERY
      network -- the reaction vectors of a linkage class span at most one less
      dimension than it has complexes, so s <= n - l.  A computed d < 0 is
      therefore a defect in the graph construction and cannot be a finding about
      a network.  This block is why the script exists: the page withdrew the
      surfactant morphism on the strength of "d < 0 under two independent
      formulations", and that reason cannot be right even though the withdrawal
      is;
  [3] citation hygiene -- every in-text (Author, Year, Journal) resolves to a
      reference-list entry, and the journal agrees between the two;
  [4] the externally verified corrections, asserted as present, so that a
      citation this desk checked against the primary source cannot silently
      revert.

Requires only the standard library.  Exits 1 on any failure.

    python3 wp101-verify.py                       # paths inferred
    python3 wp101-verify.py --axle ~/Desktop/AXLE
"""

import argparse
import html
import os
import random
import re
import sys
from fractions import Fraction

FAIL, SKIP = [], []


def check(label, got, want, note=None):
    ok = (got == want)
    print("  %s %-50s got=%s  want=%s" % ("OK  " if ok else "FAIL", label,
                                          str(got)[:34], str(want)[:34]))
    if note:
        for line in note.split("\n"):
            print("       " + line)
    if not ok:
        FAIL.append(label)
    return ok


def skip(label, why):
    print("  SKIP %-50s %s" % (label, why))
    SKIP.append(label)


HERE = os.path.dirname(os.path.abspath(__file__))
ap = argparse.ArgumentParser()
ap.add_argument("--page", default=os.path.join(HERE, "wp101-prematurity-fold-event.html"))
ap.add_argument("--axle", default=None, help="path to the AXLE repository")
args = ap.parse_args()

PAGE = open(args.page, encoding="utf-8").read()


def axle_path():
    if args.axle:
        return args.axle
    for c in [os.path.join(HERE, "..", "..", "AXLE"),
              os.path.expanduser("~/Desktop/AXLE"),
              os.path.expanduser("~/mnt/AXLE")]:
        if os.path.isdir(c):
            return c
    return None


# ======================================================================== [1]
print()
print("[1] the anchor: AXLE/AutophagyDm3_v2.lean")
AX = axle_path()
anchor = os.path.join(AX, "AutophagyDm3_v2.lean") if AX else None
if not anchor or not os.path.isfile(anchor):
    skip("anchor file", "AXLE repository not found (pass --axle)")
    skip("anchor declaration census", "AXLE repository not found")
else:
    src = open(anchor, encoding="utf-8").read()
    out, i, d = [], 0, 0
    while i < len(src):
        if src.startswith("/-", i):
            d += 1; i += 2; continue
        if src.startswith("-/", i) and d:
            d -= 1; i += 2; continue
        if d == 0:
            out.append(src[i])
        i += 1
    code = "\n".join(l for l in "".join(out).split("\n")
                     if not l.strip().startswith("--"))
    thms = len(re.findall(r"^(?:theorem|lemma)\s", code, re.M))
    check("theorems and lemmas", thms, 24,
          "The page as first published read 18. The file has grown to 24 and its\n"
          "own header says 24; the page carries a dated correction. A count that\n"
          "is quoted rather than recomputed decays the moment the file moves.")
    check("`sorry` in code (comments excluded)",
          len(re.findall(r"\bsorry\b", code)), 0)
    check("theorems concluding in `True`",
          len(re.findall(r":\s*True\b", code)), 0,
          "The distinction the anchor's own header insists on: a theorem whose\n"
          "conclusion is `True` is vacuous and counts for nothing.")

print()
print("    the numeric claims, re-derived rather than quoted")


def frac(x):
    return Fraction(x).limit_denominator()


# contact coefficient c(rho) = -2 rho
check("c(rho) < 0 for every rho > 0",
      all(-2 * r < 0 for r in (Fraction(1, 1000), Fraction(1), Fraction(10 ** 6))), True,
      "Scalar witness that alpha ^ d alpha /= 0 on X_auto. NOT the full manifold\n"
      "statement -- Obligation A -- and the page is careful to say so.")

# V(q) = q^3 - 3q : Whitney A_1 fold at q = 1
V = lambda q: q ** 3 - 3 * q
V1 = lambda q: 3 * q ** 2 - 3
V2 = lambda q: 6 * q
check("V'(1) = 0", frac(V1(1)), 0)
check("V''(1) = 6, so the critical point is non-degenerate", frac(V2(1)), 6,
      "Non-degenerate second derivative is exactly Morse, which is exactly A_1.\n"
      "The algebra is complete; kinase data and Mather finite-determinacy are\n"
      "Obligation B and remain open.")
check("V(1) = -2", frac(V(1)), -2)
check("V(q) + 2 factors as (q-1)^2 (q+2)",
      all(frac(V(q) + 2) == frac((q - 1) ** 2 * (q + 2))
          for q in (-3, -2, -1, 0, 1, 2, 5)), True,
      "A double root at q = 1 -- the fold -- and a simple root at q = -2.")
check("the second critical point q = -1 is a maximum", frac(V2(-1)), -6)
check("mu_canonical = -V''(1)/2", frac(-V2(1)) / 2, -3)
check("mu_dm3 < 0", frac(-2) < 0, True)

# Gronwall radius and basin
check("gronwall radius 2/(2(1+2))", Fraction(2, 2 * (1 + 2)), Fraction(1, 3))
check("0 < eps_0 < 1", 0 < Fraction(1, 3) < 1, True)
check("basin asymmetry 1/3 < 4/5", Fraction(1, 3) < Fraction(4, 5), True)
check("annular basin [1/3, 2] non-empty", Fraction(1, 3) < 2, True,
      "Compact and non-empty is Heine-Borel on a closed interval and nothing\n"
      "more. Named a dm3 basin only pending a semiflow -- Obligation C.")

# ======================================================================== [2]
print()
print("[2] chemical reaction network theory, from the definition")


def _rank(rows):
    M = [[Fraction(x) for x in r] for r in rows]
    R, ncol = 0, (len(M[0]) if M else 0)
    for c in range(ncol):
        piv = next((r for r in range(R, len(M)) if M[r][c] != 0), None)
        if piv is None:
            continue
        M[R], M[piv] = M[piv], M[R]
        pv = M[R][c]
        M[R] = [x / pv for x in M[R]]
        for r in range(len(M)):
            if r != R and M[r][c] != 0:
                f = M[r][c]
                M[r] = [a - f * b for a, b in zip(M[r], M[R])]
        R += 1
    return R


def deficiency(reactions, species):
    """(n, l, s, delta) for a network given as (complex, complex) pairs, each
    complex a dict species -> stoichiometric coefficient.  The zero complex is
    the empty dict, which is how degradation sinks and de novo synthesis enter."""
    cx = []

    def idx(c):
        t = tuple(c.get(s, 0) for s in species)
        if t not in cx:
            cx.append(t)
        return cx.index(t)

    edges = [(idx(a), idx(b)) for a, b in reactions]
    n = len(cx)
    par = list(range(n))

    def find(x):
        while par[x] != x:
            par[x] = par[par[x]]
            x = par[x]
        return x

    for a, b in edges:
        ra, rb = find(a), find(b)
        if ra != rb:
            par[ra] = rb
    l = len({find(i) for i in range(n)})
    vecs = [[cx[b][k] - cx[a][k] for k in range(len(species))] for a, b in edges]
    return n, l, (_rank(vecs) if vecs else 0), n - l - (_rank(vecs) if vecs else 0)

# Feinberg's textbook example: 2A -> A+B -> 2B -> 2A has deficiency 1.
n, l, s, d = deficiency([({"A": 2}, {"A": 1, "B": 1}),
                         ({"A": 1, "B": 1}, {"B": 2}),
                         ({"B": 2}, {"A": 2})], ["A", "B"])
check("calibration on Feinberg's example (n,l,s,delta)", (n, l, s, d), (3, 1, 1, 1),
      "If the implementation cannot reproduce a published deficiency it has no\n"
      "standing to contradict one.")

check("the autophagy triple gives delta = 2", 9 - 4 - 3, 2,
      "n = 9 complexes, l = 4 linkage classes, s = 3, as reported by WP-86's\n"
      "explicit graph construction for the AMPK-mTORC1-ULK1 network. The graph\n"
      "itself was not republished, so this checks the arithmetic of the triple\n"
      "and not the triple. Necessary for fold behaviour, not sufficient: the\n"
      "rate constants did not clear (WP-31C) and mu_max was withdrawn (WP-30).")

print()
print("    delta >= 0 is forced, so a computed delta < 0 is a construction error")
random.seed(20260909)
worst, tested = None, 0
for _ in range(6000):
    sp = [chr(97 + i) for i in range(random.randint(1, 5))]
    rx = []
    for _ in range(random.randint(1, 9)):
        a = {s: random.randint(0, 2) for s in sp}
        b = {s: random.randint(0, 2) for s in sp}
        if a != b:
            rx.append((a, b))
    if not rx:
        continue
    tested += 1
    dd = deficiency(rx, sp)[3]
    if worst is None or dd < worst:
        worst = dd
check("minimum delta over %d random networks" % tested, worst, 0,
      "Not a proof, a demonstration of one: s <= n - l always, because the\n"
      "reaction vectors of a linkage class span at most one dimension less than\n"
      "it has complexes. Hence delta = n - l - s >= 0 for EVERY network,\n"
      "including every network with degradation sinks and de novo synthesis.")

# The surfactant network as the page describes it: TTF-1/NKX2-1 -> SP-B/SP-C,
# 9 reactions, 5 species and the zero complex, degradation sinks, and
# autoregulation entered as de novo transcription.  The published graph was not
# reproduced in the page, so this is A reconstruction consistent with the
# description, not THE network -- and the point does not depend on which it is.
SURF = ["G", "T", "Ta", "B", "C"]          # glucocorticoid, TTF-1, TTF-1 active, SP-B, SP-C
surf = [({}, {"T": 1}),                    # de novo TTF-1
        ({"G": 1, "T": 1}, {"G": 1, "Ta": 1}),   # activation
        ({"Ta": 1}, {"T": 1}),                   # deactivation
        ({"Ta": 1}, {"Ta": 1, "B": 1}),          # SP-B transcription
        ({"Ta": 1}, {"Ta": 1, "C": 1}),          # SP-C transcription
        ({"Ta": 1}, {"Ta": 1, "T": 1}),          # autoregulation, de novo
        ({"B": 1}, {}),                          # degradation sinks
        ({"C": 1}, {}),
        ({"T": 1}, {})]
n, l, s, d = deficiency(surf, SURF)
check("a surfactant network of the described shape: delta >= 0", d >= 0, True,
      "n=%d, l=%d, s=%d, delta=%d. This is A network matching the description --\n"
      "9 reactions, 5 species and the zero complex, sinks, autoregulation as de\n"
      "novo transcription -- not necessarily THE one, which the page did not\n"
      "publish. The conclusion does not depend on that: no reaction network has\n"
      "a negative deficiency, so 'delta < 0 under two independent formulations'\n"
      "reports a defect in both constructions and not a property of the biology.\n"
      "THE WITHDRAWAL STANDS AND ITS STATED REASON DOES NOT. The honest ground\n"
      "is that no valid deficiency was ever obtained for this network, so there\n"
      "is no CRNT evidence either way -- which is weaker than the page claimed\n"
      "and is the direction an auditor should err in." % (n, l, s, d))

# ======================================================================== [3]
print()
print("[3] citation hygiene, internal")
cut = PAGE.find("References")
strip = lambda x: html.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", x)))
BODY, REFS = strip(PAGE[:cut]), strip(PAGE[cut:])

# in-text citations of the form "(Author ... 1999, Journal)"
INTEXT = re.compile(
    r"\(([A-Z][A-Za-zÀ-ɏ-]+)(?:\s+(?:&|and)\s+[A-Z][A-Za-z]+|\s+et\s+al\.?)?"
    r"\s+((?:19|20)\d\d)\s*,\s*([A-Z][A-Za-z' ]{2,30}?)\s*[;)]")
cites, missing, mismatched = {}, [], []
for m in INTEXT.finditer(BODY):
    author, year, journal = m.group(1), m.group(2), m.group(3).strip()
    cites.setdefault((author, year), journal)
for (author, year), journal in sorted(cites.items()):
    entry = re.search(re.escape(author) + r"[^(]{0,40}\(" + year + r"\)\.(.{0,220})", REFS)
    if not entry:
        missing.append("%s %s" % (author, year))
        continue
    tail = entry.group(1)
    key = journal.split()[0].rstrip(".,")
    if key.lower() not in tail.lower():
        mismatched.append("%s %s: text says %r, entry says %r"
                          % (author, year, journal, tail.strip()[:90]))
check("in-text citations with a reference entry", missing, [],
      "An in-text citation with no entry is a claim with no source attached.")
check("journal agrees between text and entry", mismatched, [])
for x in missing + mismatched:
    print("       -> " + x)

# ======================================================================== [4]
print()
print("[4] the externally verified corrections, asserted present")
print("       Each was checked against the primary source on 2026-09-09 and each")
print("       was wrong in the page as first published. Asserted here so that a")
print("       correction cannot silently revert.")
VERIFIED = [
    ("Whitsett & Weaver is 2002, not 2015",
     "Whitsett JA, Weaver TE (2002)", "NEJM 347:2141-8, PMID 12501227"),
    ("Ball 2013 is in Cortex, not Brain",
     "Ball et al. 2013, <em>Cortex</em>", "Cortex 49(6):1711-21"),
    ("Stjerna is JoVE 2012, and is a protocol paper",
     "Stjerna S et al. (2012)", "J Vis Exp 60:3774, PMID 22371054"),
    ("Gibbons 2014 is Nature Medicine",
     "Gibbons D et al. (2014). Interleukin-8", "Nat Med 20:1206-10, doi 10.1038/nm.3670"),
    ("the anchor carries 24 theorems",
     "24 theorems", "AutophagyDm3_v2.lean, measured"),
    ("the deficiency reason is corrected",
     "non-negative for every reaction network", "Feinberg: delta = n - l - s >= 0"),
]
for label, needle, src in VERIFIED:
    check(label, needle in PAGE, True, "       source: " + src)

check("the `untraceble` typo is gone", "untraceble" in PAGE, False)

# ==================================================================== verdict
print()
if SKIP:
    print("SKIPPED: " + ", ".join(SKIP))
if FAIL:
    print("FAILED: " + ", ".join(FAIL))
    sys.exit(1)
print("ALL CHECKS PASSED" + (" (partial -- see SKIPPED)" if SKIP else ""))
