#!/usr/bin/env python3
"""
numbering.py  --  does a page's DISPLAYED number agree with its FILENAME?

The corpus addresses a working paper two ways: by the number a reader sees
("WP-31C") and by the slug in the URL (`wp86-...`).  Nothing has ever checked
that the two agree, and where they diverge a citation stops being well defined:
"WP-30" resolves to one paper by label and a different one by filename, and a
reader who constructs a URL from the label lands on nothing.  That is not
hypothetical -- it is where WP-101's three dead links came from, each one a
filename built out of a label.

This tool reports three things and judges none of them.  Divergence is a
decision the author is entitled to make; what is not acceptable is divergence
nobody can see.

    MISMATCH   the row's label and its filename carry different numbers
    COLLISION  one label on more than one file
    ORPHAN     a wpNN file that no index row lists
    DUPLICATE  the same wpNN number carried by files in two different books

Exit status is 0 unless --strict is passed, so this can run in a report loop
without failing a build over a deliberate choice.

    python3 tools/numbering.py
    python3 tools/numbering.py --strict     # non-zero if anything is reported
"""

import argparse
import html
import os
import re
import sys
from collections import defaultdict

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SKIP = {".git", ".lake", "_to_delete", "_archive", "node_modules", "ml-evidence"}

ROW = re.compile(r'<a\s+href="([^"]+\.html)"[^>]*class="ch-row"[^>]*>(.*?)</a>', re.S)
LABEL = re.compile(r'ch-n">([^<]+)<')
TITLE = re.compile(r"<strong>(.*?)</strong>", re.S)
NUM = re.compile(r"^(?:WP|Ch)[\s·-]*(\d+)", re.I)
SLUG = re.compile(r"(?:^|/)wp(\d+)", re.I)


def clean(x):
    return html.unescape(re.sub(r"<[^>]+>", "", x)).strip()


def indexes():
    out = []
    for dp, dns, fns in os.walk(ROOT):
        dns[:] = [d for d in dns if d not in SKIP]
        for f in fns:
            if f == "index.html" or f.startswith("index-") or f == "master-index.html":
                out.append(os.path.join(dp, f))
    return sorted(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--strict", action="store_true")
    args = ap.parse_args()

    rows, mism, coll, orph = 0, [], [], []
    bylabel = defaultdict(set)
    listed = set()

    for idx in indexes():
        rel = os.path.relpath(idx, ROOT)
        try:
            s = open(idx, encoding="utf-8", errors="replace").read()
        except OSError:
            continue
        for m in ROW.finditer(s):
            href, blk = m.group(1), m.group(2)
            lab = LABEL.search(blk)
            if not lab:
                continue
            label = clean(lab.group(1))
            title = clean(TITLE.search(blk).group(1))[:54] if TITLE.search(blk) else ""
            rows += 1
            target = os.path.normpath(os.path.join(os.path.dirname(rel), href))
            listed.add(os.path.basename(target).lower())
            bylabel[label].add((target, title))
            ln, sn = NUM.match(label), SLUG.search(href)
            if ln and sn and ln.group(1) != sn.group(1):
                mism.append((rel, label, target, title))

    for label, v in sorted(bylabel.items()):
        if len(v) > 1:
            coll.append((label, sorted(v)))

    for dp, dns, fns in os.walk(ROOT):
        dns[:] = [d for d in dns if d not in SKIP]
        for f in fns:
            if re.match(r"wp\d+[-.]", f, re.I) and f.endswith(".html"):
                if f.lower() not in listed:
                    orph.append(os.path.relpath(os.path.join(dp, f), ROOT))

    print("%d index rows read from %d index pages" % (rows, len(indexes())))

    print("\nMISMATCH -- label number != filename number (%d)" % len(mism))
    for rel, label, target, title in mism:
        print("   %-10s -> %-52s  %s" % (label, target, title))
        print("               listed in %s" % rel)

    print("\nCOLLISION -- one label, several files (%d)" % len(coll))
    for label, v in coll:
        print("   %s" % label)
        for t, ti in v:
            print("       %-52s %s" % (t, ti))

    print("\nORPHAN -- wpNN file no index row lists (%d)" % len(orph))
    for o in sorted(orph):
        print("   %s" % o)

    dup = defaultdict(list)
    for dp, dns, fns in os.walk(ROOT):
        dns[:] = [d for d in dns if d not in SKIP]
        for f in fns:
            m = re.match(r"wp(\d+)[-.]", f, re.I)
            if m and f.endswith(".html"):
                dup[int(m.group(1))].append(
                    os.path.relpath(os.path.join(dp, f), ROOT))
    dups = [(k, sorted(v)) for k, v in sorted(dup.items()) if len(v) > 1]
    print("\nDUPLICATE -- one wpNN number, files in two places (%d)" % len(dups))
    for k, v in dups:
        print("   WP-%d" % k)
        for f in v:
            print("       %s" % f)

    total = len(mism) + len(coll) + len(orph) + len(dups)
    print("\n%d reported. Divergence may be deliberate; invisible divergence is not."
          % total)
    if args.strict and total:
        sys.exit(1)


if __name__ == "__main__":
    main()
