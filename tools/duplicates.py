#!/usr/bin/env python3
"""
duplicates.py — one chapter, two homes: declared or a finding.

WHY THIS EXISTS
---------------
Sessions run out of context and continue on another account. The next session
does not always see what the previous one left, or continues and saves into a
different folder. Nothing is wrong at the moment it happens: two copies of a
chapter behave identically until somebody edits one. Then the corpus quietly
has two answers and no record of which is current.

That is not hypothetical here. On 2026-08-25, `book7/ch-curie.html` and
`book7/chcurie.html` were both live, 516 lines apart, carrying the same title,
linked from different pages, neither mentioning the other. The newer one
decomposed a `sorry` the older left opaque. A reader arriving from the Book 7
hub got the older text; a reader arriving from master-index got the newer.

The sweep that found it found 33 duplicated titles, of which the whole
`HVEH/` <-> `book4/` chapter set is one directory copied once with both copies
edited since.

CLAUDE.md already knew. Its index section records that `ch-tatiana.html` and
`ch6-resonance.html` each exist twice and instructs the crawler to "resolve by
path, not basename" -- a workaround for the duplication rather than a fix --
and "What NOT to do" forbids deduplicating two named shadow pages because they
are intentional alternate editions. So the corpus could neither prevent a new
duplicate nor tell an intended pair from an accident. This file closes that.

DECLARED vs UNDECLARED
----------------------
Some duplication is correct. `ch7-topological-orthogenesis.html` and
`ch8-nested-infinities.html` are intentional alternate editions and must not be
merged. A redirect stub shares its target's subject on purpose. What must not
happen is an UNDECLARED pair -- two live copies nobody decided to have.

Declared pairs live in `tools/duplicate_ledger.txt`, one group per line, with
the reason. Append-only, like the placeholder ledger: a retired entry is
commented out with the date, never deleted, so the file cannot quietly lose its
own history.

THE METRIC, AND WHY IT IS THIS ONE
----------------------------------
Similarity is the Jaccard index over the set of paragraphs longer than 60
characters, after stripping tags, script and style.

The first version of this sweep used 8-gram shingles over the whole document.
It reported **2%** similarity for `book7/ch-curie.html` and `ch-curie.html`,
which are **100%** identical paragraph for paragraph. Reported as written, it
would have presented sixteen pure duplicates as unrelated files sharing a
title, and every one of them would have been left in place. It was caught only
because the Curie pair had already been compared by hand, so there was a known
answer to check against.

Hence `--self-test`, and hence the rule: an instrument with no known-answer
case is not known to work.

Usage
-----
    python3 tools/duplicates.py               # report; non-zero if undeclared
    python3 tools/duplicates.py --self-test   # check the metric first
    python3 tools/duplicates.py --json report.json
"""

import argparse
import collections
import glob
import html
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LEDGER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "duplicate_ledger.txt")
# docs/ml-evidence/ is skipped for the same reason as _to_delete/: every file in
# it is a superseded copy of a live page, so it is a duplicate BY CONSTRUCTION.
# Its README is the standing declaration; listing 17 groups in
# tools/duplicate_ledger.txt would restate that once per file.
SKIP = (".lake/", "_to_delete/", "_archive/", "node_modules/", ".git/",
        "docs/ml-evidence/")

# A redirect stub legitimately shares its target's title. It is not a second
# copy of anything -- it has no paragraphs of its own to speak of.
REDIRECT = re.compile(r'<meta\s+http-equiv=["\']refresh["\']', re.I)


def paragraphs(src):
    src = re.sub(r"<(script|style)\b.*?</\1>", "", src, flags=re.S | re.I)
    out = set()
    for m in re.findall(r"<p[^>]*>(.*?)</p>", src, re.S):
        t = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", m))).strip()
        if len(t) > 60:
            out.add(t)
    return out


def norm_title(src):
    m = re.search(r"<title>(.*?)</title>", src, re.S)
    if not m:
        return None
    t = html.unescape(re.sub(r"<[^>]+>", "", m.group(1)))
    t = re.sub(r"\s+", " ", t).strip().lower()
    return re.sub(r"\s+", " ", re.sub(r"[·|—–-]+", " ", t)).strip()


def load_ledger(path):
    declared, reasons = set(), {}
    if not os.path.exists(path):
        return declared, reasons
    for line in open(path, encoding="utf-8"):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        files, _, why = line.partition("#")
        key = frozenset(p.strip() for p in files.split("|") if p.strip())
        if key:
            declared.add(key)
            reasons[key] = why.strip()
    return declared, reasons


def scan(root):
    groups = collections.defaultdict(list)
    data = {}
    for f in glob.glob(os.path.join(root, "**", "*.html"), recursive=True):
        rel = os.path.relpath(f, root)
        if any(k in rel.replace(os.sep, "/") for k in SKIP):
            continue
        try:
            s = open(f, encoding="utf-8", errors="replace").read()
        except OSError:
            continue
        t = norm_title(s)
        if not t or t.startswith("redirecting"):
            continue
        data[rel] = (t, paragraphs(s), bool(REDIRECT.search(s)))
        groups[t].append(rel)
    return {t: sorted(fs) for t, fs in groups.items() if len(fs) > 1}, data


def similarity(sets):
    inter = set.intersection(*sets)
    union = set.union(*sets)
    return (len(inter) / len(union)) if union else 0.0, len(inter), len(union)


SELF_TEST = [
    # (name, doc A, doc B, expected similarity band)
    ("identical", ["x" * 80, "y" * 80], ["x" * 80, "y" * 80], (0.99, 1.0)),
    ("one added", ["x" * 80, "y" * 80], ["x" * 80, "y" * 80, "z" * 80], (0.60, 0.70)),
    ("disjoint", ["x" * 80], ["z" * 80], (0.0, 0.01)),
    ("half", ["x" * 80, "y" * 80], ["x" * 80, "z" * 80], (0.30, 0.36)),
]


def self_test():
    bad = 0
    for name, a, b, (lo, hi) in SELF_TEST:
        j, _, _ = similarity([set(a), set(b)])
        ok = lo <= j <= hi
        bad += not ok
        print("  %-12s %5.0f%%  expected %.0f-%.0f%%   %s"
              % (name, j * 100, lo * 100, hi * 100, "ok" if ok else "** WRONG **"))
    print("  %d/%d metric cases correct" % (len(SELF_TEST) - bad, len(SELF_TEST)))
    return bad


def main(argv):
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", default=ROOT)
    ap.add_argument("--ledger", default=LEDGER)
    ap.add_argument("--json", metavar="PATH")
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args(argv[1:])

    print("duplicates.py -- metric self-test")
    if self_test():
        print("::error::the similarity metric is wrong. Nothing below can be trusted.")
        return 2
    if args.self_test:
        return 0

    groups, data = scan(args.root)
    declared, reasons = load_ledger(args.ledger)

    # A scan that examined nothing is not a clean scan.
    if not data:
        print("::error::duplicates.py read 0 documents. Check --root.")
        return 2

    rows, undeclared = [], 0
    for title, files in groups.items():
        live = [f for f in files if not data[f][2]]      # redirect stubs are not copies
        if len(live) < 2:
            continue
        j, i, u = similarity([data[f][1] for f in live])
        key = frozenset(live)
        rows.append({"title": title, "files": live, "similarity": round(j, 4),
                     "shared": i, "union": u, "declared": key in declared,
                     "reason": reasons.get(key, "")})
        undeclared += key not in declared
    rows.sort(key=lambda r: -r["similarity"])

    print("\n%d documents scanned, %d titles on more than one live file\n"
          % (len(data), len(rows)))
    for r in rows:
        mark = "declared" if r["declared"] else "UNDECLARED"
        print("  %4.0f%%  %-10s %s" % (r["similarity"] * 100, mark, r["title"][:58]))
        for f in r["files"]:
            print("             %s" % f)
        if r["reason"]:
            print("             reason: %s" % r["reason"])

    if args.json:
        json.dump(rows, open(args.json, "w", encoding="utf-8"), indent=2)

    print("\n%d undeclared duplicate group(s)" % undeclared)
    if undeclared:
        print("::error::an undeclared duplicate is two live copies nobody decided to have.")
        print("         Merge them, or add the group to tools/duplicate_ledger.txt")
        print("         with the reason it is intended.")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
