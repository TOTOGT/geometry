#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Pablo Nogueira Grossi / G6 LLC
"""
floor_texts.py -- derive the primary-text ledger from the filesystem.

WHY, AND WHY IT WAS REWRITTEN ON 2026-09-19. The first version of this script
carried a hand-kept list of eight filenames. That is the defect `build_indexes.py`
records about its own FOLDERS list -- the list is not the corpus -- committed in
the tool written to cure it. A scan of every PDF in Downloads then found three
Lean textbooks the hand list had never heard of, in a corpus whose core practice
is Lean. So this version SCANS and classifies; the rung map is an overlay on what
is found, never the source of truth.

    python3 tools/floor_texts.py [--downloads DIR] [--min-pages N]

Writes docs/floor-texts.tsv. Exit 0 always -- absence here is data, not failure.
"""
import hashlib, os, re, sys

MIN_PAGES = 60

# Markers that identify the author's OWN work, so it is counted separately
# rather than mixed in with primary sources.
OWN = re.compile(r"principia orthogona|g6 ?llc|generative orthogonal matrix|"
                 r"topographical orthogenetic|topographical orthogonal|mini.?beast|"
                 r"grossi", re.I)

# filename -> (rung, volume) from WP-82 §3. An overlay, applied after the scan.
RUNGS = {
 "Kbook.pdf":                                   (28, "XI"),
 "2112.11166v7.pdf":                            (29, "XII"),
 "Connes–Marcolli Noncommutative Algebra.pdf":  (33, "XVI"),
}

def sha256(p, block=1 << 20):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(block), b""):
            h.update(b)
    return h.hexdigest()

def main():
    dl = os.path.expanduser("~/mnt/Downloads")
    if "--downloads" in sys.argv:
        dl = sys.argv[sys.argv.index("--downloads") + 1]
    minp = MIN_PAGES
    if "--min-pages" in sys.argv:
        minp = int(sys.argv[sys.argv.index("--min-pages") + 1])
    try:
        import pypdf
    except ImportError:
        print("needs pypdf"); return 2

    third, own, small = [], [], 0
    for fn in sorted(os.listdir(dl)):
        if not fn.lower().endswith(".pdf"):
            continue
        p = os.path.join(dl, fn)
        try:
            r = pypdf.PdfReader(p)
            n = len(r.pages)
            head = re.sub(r"\s+", " ", (r.pages[0].extract_text() or ""))[:200]
        except Exception:
            continue
        if n < minp:
            small += 1
            continue
        (own if OWN.search(head) or OWN.search(fn) else third).append((n, fn, head))

    print("  %d third-party texts >= %dpp, %d of the author's own, %d shorter files skipped\n"
          % (len(third), minp, len(own), small))

    out = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                       "docs", "floor-texts.tsv")
    with open(out, "w", encoding="utf-8") as f:
        f.write("rung\tvolume\tpages\tsha256\tfile\tfirst_line\n")
        for n, fn, head in sorted(third, key=lambda x: -x[0]):
            rung, vol = RUNGS.get(fn, ("", ""))
            d = sha256(os.path.join(dl, fn))
            f.write("%s\t%s\t%d\t%s\t%s\t%s\n" % (rung, vol, n, d, fn, head[:120].replace("\t", " ")))
            print("  %-4s %-5s %5dpp  %s…  %s" % (rung or "-", vol or "-", n, d[:10], fn[:52]))

    # The author's own PDFs are not primary sources; what matters about them is
    # how many near-copies of one work are sitting in one folder.
    print("\n  Own work in the same folder, grouped by opening line:")
    groups = {}
    for n, fn, head in own:
        groups.setdefault(head[:60], []).append(fn)
    for k, v in sorted(groups.items(), key=lambda kv: -len(kv[1])):
        if len(v) > 1:
            print("    %2d copies  %s" % (len(v), k[:70]))
    dup = sum(len(v) - 1 for v in groups.values() if len(v) > 1)
    print("    -> %d files are second-or-later copies of a work already present." % dup)
    print("\n  wrote %s" % out)
    return 0

if __name__ == "__main__":
    sys.exit(main())
