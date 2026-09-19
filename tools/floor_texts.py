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

External SOFTWARE does not belong in the output of this script. It scans PDFs on
disk and rewrites docs/floor-texts.tsv wholesale, so a hand-added row would be
silently wiped. Libraries live in docs/external-tools.tsv, addressed by DOI and
version rather than by a hash of a paper about them.

Writes docs/floor-texts.tsv. Exit 0 always -- absence here is data, not failure.
"""
import hashlib, os, re, sys

MIN_PAGES = 12   # was 60 until 2026-09-19, which hid three primary sources at 13, 37 and 47pp

# Markers that identify the author's OWN work, so it is counted separately
# rather than mixed in with primary sources.
OWN = re.compile(r"principia orthogona|g6 ?llc|generative orthogonal matrix|"
                 r"topographical orthogenetic|topographical orthogonal|mini.?beast|"
                 r"grossi", re.I)

# filename -> (rung, volume) from WP-82 §3. An overlay, applied after the scan.
#
# 2026-09-19: the volumes here were XI, XII and XVI, which read WP-82's rung
# ladder through a second numbering that nothing wrote down. The rule now is
# that the rung number IS the volume number, so rung 28 is Volume XXVIII and
# not XI. Volume XI is the bottom of the teaching ladder (what a numeral
# names); index theory is 28; noncommutative geometry is 33. See the entry
# of that date in docs/audit-log.md for how the collision was found.
RUNGS = {
 "Kbook.pdf":                                   (28, "XXVIII"),
 "2112.11166v7.pdf":                            (29, "XXIX"),
 "Connes–Marcolli Noncommutative Algebra.pdf":  (33, "XXXIII"),
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

    third, own, unreadable, small = [], [], [], 0
    for fn in sorted(os.listdir(dl)):
        if not fn.lower().endswith(".pdf"):
            continue
        p = os.path.join(dl, fn)
        try:
            r = pypdf.PdfReader(p)
            n = len(r.pages)
            head = re.sub(r"\s+", " ", (r.pages[0].extract_text() or ""))[:200]
        except Exception as e:
            # NEVER swallow this. A file the reader cannot open is not an absent
            # text; it is an unread one, and a scanner that drops it silently
            # manufactures exactly the false absence this ledger exists to stop.
            unreadable.append((fn, type(e).__name__))
            continue
        if n < minp:
            small += 1
            continue
        (own if OWN.search(head) or OWN.search(fn) else third).append((n, fn, head))

    print("  %d third-party texts >= %dpp, %d of the author's own, %d shorter files skipped"
          % (len(third), minp, len(own), small))
    if unreadable:
        print("  %d UNREADABLE -- not absent, unread:" % len(unreadable))
        for fn, err in unreadable:
            print("      %-52s %s" % (fn[:52], err))
    print()

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
    if unreadable:
        print("  NOTE: %d file(s) could not be read. Absence below is not established"
              " for them." % len(unreadable))
    return 0

if __name__ == "__main__":
    sys.exit(main())
