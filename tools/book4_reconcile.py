#!/usr/bin/env python3
"""
book4_reconcile.py -- measure the geometry/GTCT Book IV split, per chapter.

CLAUDE.md, "CANONICAL: all HTML lives in geometry", records that Book IV exists
twice and that as measured 2026-08-30 every shared chapter differed, with drift
running in BOTH directions. It also says the fix is a reconciliation and never a
copy: diff, merge both ways, land in geometry, leave a pointer behind. And it
says that until a page is reconciled it must not be edited in either repo --
which is why the section 12.2 correction is still unwritten.

That instruction has been sitting there since 2026-08-30 without a work list.
This produces one. It MERGES NOTHING and WRITES NOTHING. For each shared
chapter it reports how far apart the two copies are and, where it can tell,
which side carries material the other does not.

"Which side is ahead" is measured as paragraphs of prose present in one copy
and absent from the other. It is a signal, not a verdict: a chapter can be
rewritten shorter and be later. Every row needs a human before it is merged.

Run:  python3 tools/book4_reconcile.py
"""
import os, re, io, html, difflib

GEO  = "book4"
GTCT = os.path.expanduser("~/mnt/Desktop/GTCT/book4")

# A copyright/licence/ISBN/doi/ORCID line is not content. Without this, eight
# chapters that are word-for-word identical read as "geometry ahead" because
# geometry's copy carries a footer GTCT's does not. Measuring the footer as
# authorship is exactly the kind of number that sends someone merging for an
# afternoon and finding nothing.
BOILER = re.compile(r'(\u00a9|Licen[cs]e CC|ISBN\s|doi\s*10\.|ORCID\s*\d)', re.I)

def prose(path):
    s = io.open(path, encoding="utf-8", errors="replace").read()
    s = re.sub(r"<(style|script).*?</\1>", "", s, flags=re.S|re.I)
    s = re.sub(r"<[^>]+>", "\n", s)
    out = [p for p in (re.sub(r"\s+"," ",html.unescape(x)).strip()
                       for x in s.split("\n")) if len(p) > 60]
    return [p for p in out if not (len(p) < 260 and BOILER.search(p))]

def ls(d):
    return sorted(f for f in os.listdir(d) if f.endswith(".html")) if os.path.isdir(d) else []

g, t = ls(GEO), ls(GTCT)
if not t:
    print("GTCT/book4 not found at %s -- nothing to reconcile from here." % GTCT)
    raise SystemExit(0)
shared  = [f for f in g if f in t]
only_g  = [f for f in g if f not in t]
only_t  = [f for f in t if f not in g]

print("="*78); print("BOOK IV -- THE geometry/GTCT SPLIT, CHAPTER BY CHAPTER"); print("="*78)
print("  geometry/book4 %d files   GTCT/book4 %d files   shared %d"
      % (len(g), len(t), len(shared)))
print("  this script merges nothing and writes nothing.")
print()
print("%-34s %9s %9s %6s %7s %7s  %s"
      % ("chapter","geometry","GTCT","sim","geo-only","gtct-only","reading"))
print("-"*78)

tally = {}
for f in shared:
    pg, pt = prose(os.path.join(GEO,f)), prose(os.path.join(GTCT,f))
    sg, st = set(pg), set(pt)
    sim = difflib.SequenceMatcher(None, " ".join(pg), " ".join(pt)).ratio()
    og, ot = len(sg - st), len(st - sg)
    if   sim > 0.995 and not og and not ot: verdict = "identical"
    elif og and not ot:                     verdict = "geometry ahead"
    elif ot and not og:                     verdict = "GTCT ahead"
    elif og and ot:                         verdict = "BOTH WAYS -- read it"
    else:                                   verdict = "formatting only"
    tally[verdict] = tally.get(verdict,0) + 1
    print("%-34s %9d %9d %6.3f %7d %7d  %s"
          % (f, os.path.getsize(os.path.join(GEO,f)),
             os.path.getsize(os.path.join(GTCT,f)), sim, og, ot, verdict))

print()
print("="*78); print("TALLY"); print("="*78)
for k,v in sorted(tally.items(), key=lambda x:-x[1]):
    print("  %-24s %3d of %d shared chapters" % (k, v, len(shared)))
print()
print("  only in geometry (%d): %s" % (len(only_g), ", ".join(only_g)))
print()
print("  only in GTCT (%d): %s" % (len(only_t), ", ".join(only_t)))
print()
print("="*78); print("HOW TO READ THIS"); print("="*78)
print("""  'geo-only' and 'gtct-only' count paragraphs of prose over 60 characters
  present in one copy and absent from the other. A high count on BOTH sides is
  the expensive case: neither copy is simply newer, and a cp in either
  direction destroys work. Those rows are the reconciliation, and CLAUDE.md
  says each one is merged by hand, landed in geometry, and replaced on the
  GTCT side by a pointer -- never left as a second copy.

  A high similarity with a nonzero count is usually a rewritten sentence, not
  a new section. A low similarity with counts on both sides is two documents
  that grew apart.

  This script cannot tell a later paragraph from a deleted one. Nothing here
  is a merge instruction.""")
print("="*78)
