#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Triage the pratijna-without-hetu worklist.

Pages asserting a machine warrant (machine-checked / kernel-checked /
kernel-audited / formalized) with no .lean or .py named anywhere on them.

v0 could not tell a claim from a mention. This splits the list by the only
signals available without reading: what kind of page it is, and what the
sentence is about. `own-claim` is the bucket that needs a human.

    python3 tools/claims_pending.py [--out docs/claims-pending.tsv]
"""
import argparse, io, os, re, collections

# `formalised` is ordinary English ("Cantor formalised this in 1874") and is only a
# warrant word next to Lean. v0 counted the verb and produced 52 false positives.
WARRANT = re.compile(r"machine-checked|machine-verified|kernel-checked|kernel-audited|"
                     r"formali[sz]ed in (?:Lean|Mathlib)|Lean[- ]?4? formali[sz]ed", re.I)
# A negation is the opposite of a claim, and a conditional is not yet one.
NEGATED = re.compile(r"\b(no|not|nothing|none|never|cannot|is not|are not)\b[^.;]{0,60}$", re.I)
CONDITIONAL = re.compile(r"^[^.;]{0,40}\b(if|once|when|until|should|would|could|suppose)\b", re.I)
REF = re.compile(r"\b[A-Za-z0-9_./-]+\.(?:lean|py)\b")
SKIP = {".git", "_to_delete", ".lake", "verify-audit", "node_modules"}
LISTING = re.compile(r"(^|/)(index|master-index|series-hub|classroom-index|.*-portal|archive)", re.I)
OTHERS = re.compile(r"Axiom|Palomar|Lean FRO|Tao|the field|movement|elsewhere|others|"
                    r"AlphaProof|DeepMind|OpenAI|Mathlib community|arXiv", re.I)
SELF = re.compile(r"\bthis (file|chapter|paper|page|result|theorem|proof|work)\b|"
                  r"\bwe (prove|proved|formali|verif|check)|\bis proved\b|\bare proved\b", re.I)


def sentences(flat):
    return re.split(r"(?<=[.;])\s+", flat)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="docs/claims-pending.tsv")
    ap.add_argument("--root", default=".")
    a = ap.parse_args()

    rows = []
    for dp, dn, fn in os.walk(a.root):
        dn[:] = [d for d in dn if d not in SKIP]
        for f in sorted(fn):
            if not f.endswith(".html"):
                continue
            path = os.path.relpath(os.path.join(dp, f), a.root)
            html = io.open(os.path.join(dp, f), encoding="utf-8", errors="replace").read()
            flat = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", re.sub(
                r"<(script|style)[^>]*>.*?</\1>", " ", html, flags=re.S | re.I)))
            if not WARRANT.search(flat) or REF.search(flat):
                continue
            for sent in sentences(flat):
                m = WARRANT.search(sent)
                if not m:
                    continue
                pre = sent[:m.start()]
                if NEGATED.search(pre):
                    bucket = "disclaimed"
                elif CONDITIONAL.search(sent):
                    bucket = "conditional"
                elif LISTING.search(path):
                    bucket = "listing"
                elif OTHERS.search(sent):
                    bucket = "about-others"
                elif SELF.search(sent):
                    bucket = "own-claim"
                else:
                    bucket = "unclassified"
                rows.append((path, bucket, m.group(0).lower(),
                             sent.strip()[:220].replace("\t", " ")))

    with io.open(a.out, "w", encoding="utf-8") as fh:
        fh.write("page\tbucket\tlabel\tsentence\n")
        for r in rows:
            fh.write("\t".join(r) + "\n")

    pages = collections.defaultdict(set)
    for p, b, _, _ in rows:
        pages[b].add(p)
    c = collections.Counter(b for _, b, _, _ in rows)
    print("%s: %d sentences on %d pages" % (a.out, len(rows), len({r[0] for r in rows})))
    for b in ("own-claim", "unclassified", "about-others", "listing",
              "disclaimed", "conditional"):
        print("  %-14s %4d sentences  %3d pages" % (b, c[b], len(pages[b])))
    print("\n  NEEDS A HUMAN — own-claim pages:")
    for p in sorted(pages["own-claim"]):
        print("    " + p)


if __name__ == "__main__":
    main()
