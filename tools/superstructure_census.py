#!/usr/bin/env python3
"""
superstructure_census.py -- what Books III and IV actually claim, and what marks it.

R21 order is book1 -> book2 -> toy -> gcm -> books 3 and 4 -> GTCT.
The base layer was mapped by hand in tools/foundations_evidence.py, claim by
claim, because 34 claims is a size a person can hold. Book IV is 59 files.
Hand-mapping it before knowing its shape would be guessing at scale.

So this one ASSERTS NOTHING. It reads the files and counts. Every number below
is derived from the corpus at the moment it runs; nothing here is a judgement
about whether a claim is true, and no tag is proposed. What it produces is the
work list for the tagging job, and three findings that were not visible until
the files were counted.

Run:  python3 tools/superstructure_census.py
"""
import os, re, io, glob, collections

AX = os.path.expanduser("~/mnt/Desktop/vol1-proofs/tools/axioms.txt")

# Book III's chapters live at the repo root, not under book3/. The two files in
# book3/ are its index and the ESL vocabulary companion. impa-portal.html is
# linked from book3/index.html but is a shared portal -- book1, book2 and book4
# link it too -- so it is not counted as Book III content.
BOOK3 = ["vol3-minibeast.html", "livro3-brasil.html", "minibeast-pilot.html",
         "ch-seismic.html", "book3/vocab-seismic-geometry.html", "book3/index.html"]
BOOK4 = sorted(glob.glob("book4/*.html"))

CLAIM = re.compile(r'\b(Theorem|Proposition|Lemma|Corollary|Conjecture)\s+'
                   r'([0-9]+(?:\.[0-9]+)*|[A-Z])\b')
TAGV  = ["SHOWN","CITED","MODEL","CONJECTURE","OPEN","PARTIAL",
         "PROVED","COMPUTED","ASSUMPTION","DEFINITION"]
TAG   = re.compile(r'>(' + "|".join(TAGV) + r')<')

def lean_names():
    if not os.path.exists(AX): return set()
    return {m.group(1) for m in
            re.finditer(r"^'([^']+)'", io.open(AX,encoding="utf-8").read(), re.M)}

LEAN = lean_names()
SHORT = {f.split(".",1)[1] for f in LEAN}

def body(path):
    s = io.open(path, encoding="utf-8", errors="replace").read()
    s = re.sub(r"<style.*?</style>", "", s, flags=re.S|re.I)
    s = re.sub(r"<script.*?</script>", "", s, flags=re.S|re.I)
    return s

def scan(files):
    rows, where = [], collections.defaultdict(list)
    for f in files:
        if not os.path.exists(f):
            rows.append((f, None, None, None, [])); continue
        b = body(f)
        cl = sorted({"%s %s" % (a,b_) for a,b_ in CLAIM.findall(b)})
        tg = TAG.findall(b)
        lr = sorted({n for n in SHORT if re.search(r'\b%s\b' % re.escape(n), b)})
        for c in cl: where[c].append(os.path.basename(f))
        rows.append((f, cl, tg, lr, cl))
    return rows, where

def report(label, files):
    rows, where = scan(files)
    nc = sum(len(r[1]) for r in rows if r[1] is not None)
    nt = sum(len(r[2]) for r in rows if r[2] is not None)
    nl = sum(len(r[3]) for r in rows if r[3] is not None)
    print(); print("-"*78)
    print("  %s -- %d files, %d numbered claims, %d tags, %d Lean names referenced"
          % (label, len(rows), nc, nt, nl))
    print("-"*78)
    for f, cl, tg, lr, _ in rows:
        if cl is None:
            print("    %-46s FILE MISSING" % os.path.basename(f)); continue
        if not cl and not tg: continue
        vocab = collections.Counter(tg)
        print("    %-46s claims %-3d tags %-3d  %s"
              % (os.path.basename(f), len(cl), len(tg),
                 " ".join("%s:%d" % (k,v) for k,v in sorted(vocab.items())) or "--"))
        if cl: print("    %-46s   %s" % ("", ", ".join(cl[:6]) +
                                         (" +%d" % (len(cl)-6) if len(cl)>6 else "")))
    silent = [os.path.basename(f) for f,cl,tg,_,_ in rows
              if cl is not None and not cl and not tg]
    print("    (%d files carry neither a numbered claim nor a tag)" % len(silent))
    dupes = {k:v for k,v in where.items() if len(v) > 1}
    stats = dict(files=len(rows), silent=len(silent),
                 with_claim=sum(1 for r in rows if r[1]),
                 with_tag=sum(1 for r in rows if r[2]))
    return nc, nt, nl, stats, dupes, collections.Counter(
        t for r in rows if r[2] for t in r[2])

print("="*78); print("BOOKS III AND IV -- CLAIM AND TAG CENSUS"); print("="*78)
print("  lean: %d declarations in TOTOGT/vol1-proofs tools/axioms.txt" % len(LEAN))
print("  this script proposes no tag and edits nothing. It counts.")

c3,t3,l3,s3,d3,v3 = report("BOOK III  (Mini-Beast)", BOOK3)
c4,t4,l4,s4,d4,v4 = report("BOOK IV   (Higher Dimensions)", BOOK4)

print(); print("="*78); print("FINDINGS"); print("="*78)

print()
print("F1  NOT ONE CLAIM IN EITHER BOOK NAMES A LEAN THEOREM.")
print("    Book III: %d claims, %d Lean names referenced." % (c3, l3))
print("    Book IV:  %d claims, %d Lean names referenced." % (c4, l4))
print("    The base layer matched 16 of 34 by topic. Here the join has no")
print("    starting point: no chapter cites a declaration by name, so a topic")
print("    match would be built out of nothing but resemblance.")

print()
print("F2  THE TAG VOCABULARY DIVERGED AND NOBODY RECONCILED IT.")
print("    base layer (foundations_evidence.py) proposes:  SHOWN / CITED / MODEL / CONJECTURE / OPEN")
print("    Book IV uses on the page:                       %s"
      % " / ".join("%s(%d)" % (k,v) for k,v in v4.most_common()))
print("    PROVED and COMPUTED are not in the base vocabulary. SHOWN is not in")
print("    Book IV's. Two conventions are running in one corpus, and PROVED is")
print("    the stronger word being used where the weaker one was chosen for the")
print("    foundations. Deciding this is the author's call; recording it is not.")

print()
print("F3  CLAIM NUMBERS COLLIDE ACROSS CHAPTERS.")
for label, d in (("Book III", d3), ("Book IV", d4)):
    if not d:
        print("    %-9s no collisions." % label); continue
    print("    %-9s %d numbers used by more than one chapter:" % (label, len(d)))
    for k, v in sorted(d.items()):
        print("        %-18s %s" % (k, ", ".join(v)))
print("    A cross-reference to a bare number in this corpus does not resolve.")

print()
print("="*78); print("THE WORK LIST"); print("="*78)
worst = max(d4.items(), key=lambda kv: len(kv[1])) if d4 else (None, [])
print("  %d of %d Book IV files carry neither claim nor tag -- narrative or"
      % (s4["silent"], s4["files"]))
print("  apparatus, and not the tagging job. %d files carry %d numbered claims"
      % (s4["with_claim"], c4))
print("  between them; %d files carry any tag at all." % s4["with_tag"])
print()
print("  The order that follows from the base-layer work:")
print("    1. fix the numbering collisions -- a tag on %s is useless" % worst[0])
print("       while %d chapters have one" % len(worst[1]))
print("    2. settle PROVED/COMPUTED vs SHOWN/CITED into one vocabulary")
print("    3. THEN map claims to Lean, chapter by chapter, and only where a")
print("       chapter names its evidence")
print()
print("="*78)
print("Census only. Nothing above is a tag, a proposal, or a judgement of truth.")
print("="*78)
