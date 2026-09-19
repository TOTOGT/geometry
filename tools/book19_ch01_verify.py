#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Pablo Nogueira Grossi / G6 LLC
"""
book19_ch01_verify.py -- locate, in the Lean reference, the things this corpus's
axiom gate is built on.

The gate reads `#print axioms` and accepts [propext, Classical.choice, Quot.sound].
It was written by inference from error messages. This script asks the reference
manual where each of those is defined, and reports honestly when a term is not
found -- including the command the gate is named after.

    python3 tools/book19_ch01_verify.py [--downloads DIR]

Theorem Proving in Lean carries no page numbers this reader can locate (3 of 206),
so it is addressed by CHAPTER AND SECTION, which is how that book is cited anyway.
Mathematics in Lean pages locate normally and are given as printed pages.

Exit 0 iff every expected term is found and every expected absence is absent.
"""
import os, re, sys

TPIL = ("file.pdf", "Avigad, de Moura & Kong, Theorem Proving in Lean")
MIL  = ("mathematics_in_lean.pdf", "Avigad & Massot, Mathematics in Lean v4.19.0")

EXPECT_PRESENT = ["sorry", "propext", "Quot.sound", "Axioms and Computation", "noncomputable"]
EXPECT_ABSENT  = ["#print axioms"]          # the command the gate is named after
UNRESOLVED     = ["Classical.choice"]       # searched, not found under this spelling

def pages(path):
    import pypdf
    r = pypdf.PdfReader(path)
    return {i: re.sub(r"\s+", " ", (p.extract_text() or "")) for i, p in enumerate(r.pages)}

def headings(T):
    h = {}
    for i, t in T.items():
        m = re.search(r"\b(\d{1,2}(?:\.\d{1,2})?)\s+([A-Z][A-Za-z ,\-]{4,45})", t[:300])
        if m: h[i] = m.group(0).strip()
    return h

def main():
    dl = os.path.expanduser("~/mnt/Downloads")
    if "--downloads" in sys.argv:
        dl = sys.argv[sys.argv.index("--downloads") + 1]
    bad = 0
    p = os.path.join(dl, TPIL[0])
    if not os.path.exists(p):
        print("  MISSING: %s" % TPIL[0]); return 2
    T = pages(p); H = headings(T)
    def section(i):
        for j in range(i, -1, -1):
            if j in H: return H[j]
        return "(no heading located)"
    print("  %s\n  %d pdf pages; addressed by section, not page\n" % (TPIL[1], len(T)))
    for term in EXPECT_PRESENT:
        hits = [i for i, t in T.items() if term.lower() in t.lower()]
        if hits:
            print("  ok     %-24s %2d pages; first in  %s" % (term, len(hits), section(hits[0])[:58]))
        else:
            print("  FAIL   %-24s expected present, not found" % term); bad += 1
    print()
    for term in EXPECT_ABSENT:
        hits = [i for i, t in T.items() if term.lower() in t.lower()]
        if hits:
            print("  FAIL   %-24s expected ABSENT, found on %d pages" % (term, len(hits))); bad += 1
        else:
            print("  ok     %-24s ABSENT from the reference -- the gate's own command" % term)
    for term in UNRESOLVED:
        hits = [i for i, t in T.items() if term.lower() in t.lower()]
        print("  %-6s %-24s %s" % ("note", term,
              "found on %d pages" % len(hits) if hits else
              "not found under this spelling; the axiom is discussed in ch.12, the identifier is not"))

    p2 = os.path.join(dl, MIL[0])
    if os.path.exists(p2):
        T2 = pages(p2); printed = {}
        for i, t in T2.items():
            m = re.search(r"(?:^|\s)(\d{1,4})(?:\s|$)", t[:40]) or re.search(r"(\d{1,4})\s*$", t[-40:])
            if m:
                n = int(m.group(1))
                if 0 <= i - n <= 40 and n not in printed: printed[n] = i
        s = sorted(n for n, i in printed.items() if "sorry" in T2[i].lower())
        print("\n  %s\n  ok     %-24s %d printed pages; first p. %s" % (MIL[1], "sorry", len(s), s[0] if s else "-"))

    print()
    print("  all expectations hold." if not bad else "  %d failed." % bad)
    return 0 if not bad else 1

if __name__ == "__main__":
    sys.exit(main())
