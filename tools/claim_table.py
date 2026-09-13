#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Claim registry (v0) — pratijna as an object rather than prose.

Harvests every status/warrant label already in use across the corpus and emits
one row per labelled claim. Invents no vocabulary: the labels are the corpus's
own, normalised only for spelling and synonymy.

    python3 tools/claim_table.py [--out docs/claims.tsv]

Two fields, not one list. The corpus currently collapses them, which is why
three words do one job (machine-checked / kernel-checked / kernel-audited) and
one word does two (Established).

  status  — how far the claim has got:   conjecture | open | argued | proved
  warrant — how it is known:             kernel | recomputed | measured | cited | none
"""
import argparse, io, os, re, collections

# label -> (status, warrant).  None means the label does not speak to that axis.
LABELS = {
    "conjecture": ("conjecture", None), "conjectured": ("conjecture", None),
    "hypothesis": ("conjecture", None),
    "open": ("open", None), "open (sorry)": ("open", None),
    "scaffold": ("open", None), "placeholder": ("open", None),
    "not claimed": ("open", None),
    "argued, not formalised": ("argued", "none"),
    "argued, not formalized": ("argued", "none"),
    "speculative": ("conjecture", "none"),
    "contested": ("argued", None),
    "proved": ("proved", None),
    "proved, machine-checked": ("proved", "kernel"),
    "machine-checked": (None, "kernel"),
    "kernel-checked": (None, "kernel"),
    "kernel-audited": (None, "kernel"),
    "formalized": (None, "kernel"), "formalised": (None, "kernel"),
    "verified symbolically": (None, "recomputed"),
    "verified numerically": (None, "recomputed"),
    "empirical": (None, "measured"), "measured": (None, "measured"),
    "established": ("proved", "cited"),
}
LABEL_RE = re.compile("|".join(sorted((re.escape(k) for k in LABELS), key=len, reverse=True)), re.I)
REF_RE = re.compile(r"\b([A-Za-z0-9_./-]+\.(?:lean|py))\b")
HEAD_RE = re.compile(r"<h[1-3][^>]*>(.*?)</h[1-3]>", re.S | re.I)
SKIP_DIRS = {".git", "_to_delete", ".lake", "verify-audit", "node_modules"}

FIELDS = ["page", "claim_id", "heading", "label", "status", "warrant", "reference", "context"]


def text_of(html):
    html = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", html, flags=re.S | re.I)
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", html))


def headings(html):
    out = []
    for m in HEAD_RE.finditer(html):
        out.append((m.start(), re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", m.group(1))).strip()))
    return out


def nearest(heads, pos):
    best = ""
    for p, h in heads:
        if p <= pos:
            best = h
        else:
            break
    return best[:70]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="docs/claims.tsv")
    ap.add_argument("--root", default=".")
    ap.add_argument("--strict", action="store_true",
                    help="only claim-shaped occurrences: an assertive label, or any label "
                         "within 200 chars of a .lean/.py reference")
    a = ap.parse_args()

    rows, per_page = [], collections.Counter()
    for dp, dn, fn in os.walk(a.root):
        dn[:] = [d for d in dn if d not in SKIP_DIRS]
        for f in sorted(fn):
            if not f.endswith(".html"):
                continue
            path = os.path.relpath(os.path.join(dp, f), a.root)
            html = io.open(os.path.join(dp, f), encoding="utf-8", errors="replace").read()
            heads, flat = headings(html), text_of(html)
            for m in LABEL_RE.finditer(flat):
                lab = m.group(0).lower()
                if lab not in LABELS:
                    continue
                status, warrant = LABELS[lab]
                lo, hi = max(0, m.start() - 200), min(len(flat), m.end() + 200)
                ctx = flat[lo:hi].strip()
                ref = REF_RE.search(ctx)
                assertive = warrant is not None or lab in (
                    "proved", "proved, machine-checked", "argued, not formalised",
                    "argued, not formalized", "open (sorry)", "not claimed",
                    "conjecture", "conjectured", "hypothesis", "speculative", "contested")
                if a.strict and not (assertive or ref):
                    continue
                per_page[path] += 1
                rows.append({
                    "page": path,
                    "claim_id": "%s#%d" % (os.path.basename(path)[:-5], per_page[path]),
                    "heading": nearest(heads, m.start() * len(html) // max(1, len(flat))),
                    "label": lab, "status": status or "-", "warrant": warrant or "-",
                    "reference": ref.group(1) if ref else "-",
                    "context": ctx[:180].replace("\t", " "),
                })

    with io.open(a.out, "w", encoding="utf-8") as fh:
        fh.write("\t".join(FIELDS) + "\n")
        for r in rows:
            fh.write("\t".join(r[k] for k in FIELDS) + "\n")
    print("%s: %d claims across %d pages" % (a.out, len(rows), len(per_page)))
    for axis in ("status", "warrant"):
        c = collections.Counter(r[axis] for r in rows)
        print("  %-8s %s" % (axis, "  ".join("%s=%d" % kv for kv in c.most_common())))
    kern = [r for r in rows if r["warrant"] in ("kernel", "recomputed")]
    unref = [r for r in kern if r["reference"] == "-"]
    nowar = [r for r in rows if r["status"] in ("proved",) and r["warrant"] == "-"]
    nostat = [r for r in rows if r["warrant"] != "-" and r["status"] == "-"]
    print("\n  PENDING TO BE TAGGED")
    print("    machine warrant, no address in context : %4d  (%d pages)"
          % (len(unref), len({r["page"] for r in unref})))
    print("    'proved' with no warrant named         : %4d  (%d pages)"
          % (len(nowar), len({r["page"] for r in nowar})))
    print("    warrant named with no status           : %4d  (%d pages)"
          % (len(nostat), len({r["page"] for r in nostat})))
    print("    fully tagged (status AND warrant)      : %4d"
          % sum(1 for r in rows if r["status"] != "-" and r["warrant"] != "-"))


if __name__ == "__main__":
    main()
