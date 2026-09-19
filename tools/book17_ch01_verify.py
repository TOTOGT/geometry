#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Pablo Nogueira Grossi / G6 LLC
"""
book17_ch01_verify.py -- locate every term Book XVII ch01 cites, in the two texts
it cites them from, and print the printed page it sits on.

The chapter is a translation table: a dm3 term, the standard machine-learning
term, and where the standard term is defined. A table like that is worth nothing
asserted, so it is produced here instead. Addresses are LOCATED, not copied: the
printed page number is read off the page and the term is matched on it.

    python3 tools/book17_ch01_verify.py [--downloads DIR]

Exit 0 iff every row lands. Needs pypdf.
"""
import os, re, sys

FRONT_MATTER_MAX = 40

def read_page_number(t):
    m = re.search(r'(?:^|\s)(\d{1,4})(?:\s|$)', t[:40]) or re.search(r'(\d{1,4})\s*$', t[-40:])
    return int(m.group(1)) if m else None

def load(path):
    import pypdf
    r = pypdf.PdfReader(path)
    printed, text = {}, {}
    for i, p in enumerate(r.pages):
        try: raw = p.extract_text() or ""
        except Exception: raw = ""
        text[i] = re.sub(r"\s+", " ", raw)
        n = read_page_number(text[i])
        if n is not None and 0 <= i - n <= FRONT_MATTER_MAX and n not in printed:
            printed[n] = i
    return printed, text, len(r.pages)

# (dm3 term as the corpus says it, standard term, source key, term to locate)
ROWS = [
 ("the fold F / Jacobian rank-1 loss", "Jacobian of a vector-valued map", "D", "Jacobian"),
 ("transverse eigenvalue mu_max",      "eigenvalue of the linearisation",  "D", "eigenvalue"),
 ("the linearisation at Gamma",        "first-order Taylor / linearization","D", "Taylor series"),
 ("curvature at the threshold kappa*", "Hessian",                          "D", "Hessian"),
 ("operator chain G = U.F.K.C",        "chain rule for composite maps",    "D", "chain rule"),
 ("descent on the potential Phi",      "gradient descent",                 "D", "Gradient Descent"),
 ("stochastic forcing in the orbit",   "stochastic gradient descent",      "D", "Stochastic Gradient Descent"),
 ("constrained basin conditions",      "Lagrange multipliers",             "D", "Lagrange multipliers"),
 ("kernel-checked derivative chains",  "automatic differentiation",        "D", "automatic differentiation"),
 ("similar systems, same normal form", "similarity of matrices",           "H", "similarity"),
 ("diagonal normal form",              "diagonalizability",                "H", "diagonalizab"),
]

SOURCES = {
 "D": ("MATHEMATICS FOR MACHINE LEARNING.pdf",
       "Deisenroth, Faisal & Ong, Mathematics for Machine Learning, CUP 2020"),
 "H": ("LINEAR ALGEBRA.pdf", "Hefferon, Linear Algebra, 4th edition"),
}

def main():
    dl = os.path.expanduser("~/mnt/Downloads")
    if "--downloads" in sys.argv:
        dl = sys.argv[sys.argv.index("--downloads") + 1]
    cache, bad = {}, 0
    for key, (fname, cite) in SOURCES.items():
        p = os.path.join(dl, fname)
        if not os.path.exists(p):
            print("  MISSING SOURCE: %s" % fname); return 2
        cache[key] = load(p)
        print("  %s  %s  (%d pdf pages, %d printed located)" % (key, cite, cache[key][2], len(cache[key][0])))
    print()
    for dm3, std, key, term in ROWS:
        printed, text, _ = cache[key]
        pages = sorted(n for n, i in printed.items() if term.lower() in text[i].lower())
        if not pages:
            print("  FAIL  %-34s -> %-34s NOT FOUND" % (dm3, std)); bad += 1
        else:
            print("  ok    %-34s -> %-34s [%s] p. %s%s"
                  % (dm3, std, key, pages[0], (" (+%d more)" % (len(pages) - 1)) if len(pages) > 1 else ""))
    print()
    print("  Addresses are located on the printed page, not copied. Re-run against your")
    print("  own copy; a different printing moves the numbers and this script says so.")
    print("  all rows land." if not bad else "  %d rows did not land." % bad)
    return 0 if not bad else 1

if __name__ == "__main__":
    sys.exit(main())
