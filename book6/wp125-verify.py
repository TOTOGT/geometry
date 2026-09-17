#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
wp125-verify.py -- the corpus knows its limits and cannot be asked about them.

CORRECTED 2026-09-17, after publication. The first version of this script
recognised exactly two syntactic shapes of gap record and concluded that 4.1%
of scripts recorded any limit at all. That was wrong by an order of magnitude:
51% do, almost entirely in PROSE the detector could not see. The paper's own
gap [1] predicted precisely this failure and the headline was published anyway,
which is the more useful lesson: writing a limitation down is not heeding it.

The finding that survives is different, and better.

Producing script for book6/wp125-what-was-not-checked.html.

Measures the ratio of named checks to recorded gaps across every producing
script in the repository, and reports the drift since a pinned baseline.

SELF-COUNT. This script measures a corpus that now contains it, and the
chapter it produces is itself a file this script counts. Per CLAUDE.md that
requires an explicit ref predating the work and a printed drift, not a
classification of the page out of its own measurement. BASELINE below is the
commit before WP-125 existed. Block [4] prints both numbers and never hides
the difference.

Reads source text only; executes nothing it measures.
"""

import ast, os, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASELINE = "35a9dd3"          # "Math placement map, and Chapter R enlarged"

FAIL = []
def check(name, ok, detail=""):
    print("  %-5s %-56s %s" % ("ok" if ok else "FAIL", name, detail))
    if not ok: FAIL.append(name)

def rule(t=""):
    print("\n" + "=" * 78)
    if t: print(t); print("=" * 78)

CHECK_RE = re.compile(r'check\(\s*["\']([^"\']{4,90})["\']')

# Prose limits records. These are the shapes the corpus actually uses, found
# by reading the 57 scripts the first version of this script scored as zero.
PROSE_RE = re.compile(
    r'HONESTY|NOT ESTABLISHED|not established|does not establish|'
    r'WHAT (THIS|IT) (SCRIPT )?DOES NOT|what this script does not|'
    r'WHAT IS NOT (SETTLED|KNOWN)|UNRESOLVED|LIMITS OF|known limits|'
    r'WOULD REFUTE|not claimed|NOT CLAIMED|SKIPPED|\[OPEN\]', re.I)
STRUCT_RE = re.compile(r'\ngaps\s*=\s*\[|\nGAPS\s*=\s*\[')


def gaps_of(src):
    """Count DISTINCT gap entries. Two syntactic shapes are in use and they
       overlap: an entry inside a `gaps = [...]` list usually ALSO matches the
       standalone-tuple pattern. The first version of this function added the
       two counts and reported 31 where tools/harvest.py, which dedupes by
       text, reported 21 on the same tree. Same corpus, two instruments,
       different answers -- caught only because both were run."""
    found = []
    m = re.search(r'\ngaps\s*=\s*\[(.*?)\n\]', src, re.S)
    if m:
        for g in re.findall(r'\(\s*["\'](.+?)["\']\s*,', m.group(1), re.S):
            t = " ".join(g.split())[:150]
            if t not in found: found.append(t)
    for m2 in re.finditer(r'^\s*\("([^"]{15,200})",\s*$', src, re.M):
        t = " ".join(m2.group(1).split())[:150]
        if t not in found: found.append(t)
    return len(found)

def survey(tree_at=None):
    """Walk the producing scripts. tree_at=None means the working tree;
       otherwise a git ref, read through `git show`."""
    if tree_at is None:
        # RECURSIVE. The first version of this walk used a single os.listdir
        # per book while the baseline side used `git ls-tree -r`, which
        # recurses. HEAD came out 4 scripts SHORT of a commit it postdates.
        # The self-count caught it; nothing else would have.
        files = []
        for d in sorted(os.listdir(ROOT)):
            p = os.path.join(ROOT, d)
            if os.path.isdir(p) and (d.startswith("book") or d in ("omega", "tools")):
                for dirpath, _dirs, fs in os.walk(p):
                    for f in sorted(fs):
                        if f.endswith(".py"):
                            files.append(os.path.relpath(
                                os.path.join(dirpath, f), ROOT))
        read = lambda rel: open(os.path.join(ROOT, rel), encoding="utf-8",
                                errors="ignore").read()
    else:
        out = subprocess.run(["git", "-C", ROOT, "ls-tree", "-r", "--name-only", tree_at],
                             capture_output=True, text=True)
        if out.returncode != 0:
            return None
        files = [f for f in out.stdout.splitlines() if f.endswith(".py")
                 and (f.split("/")[0].startswith("book")
                      or f.split("/")[0] in ("omega", "tools"))]
        def read(rel):
            r = subprocess.run(["git", "-C", ROOT, "show", "%s:%s" % (tree_at, rel)],
                               capture_output=True, text=True)
            return r.stdout

    n, checks, gaps, withgaps, nodoc = 0, 0, 0, 0, 0
    struct, prose, neither = 0, 0, 0
    for rel in files:
        try:
            src = read(rel)
        except Exception:
            continue
        if not src:
            continue
        n += 1
        checks += len(CHECK_RE.findall(src))
        g = gaps_of(src)
        gaps += g
        if g: withgaps += 1
        if STRUCT_RE.search(src):   struct += 1
        elif PROSE_RE.search(src):  prose += 1
        else:                       neither += 1
        try:
            if not ast.get_docstring(ast.parse(src)): nodoc += 1
        except SyntaxError:
            nodoc += 1
    return dict(scripts=n, checks=checks, gaps=gaps, withgaps=withgaps,
                nodoc=nodoc, struct=struct, prose=prose, neither=neither)

rule("1 . THE WORKING TREE")
now = survey()
print("      %-26s %d" % ("producing scripts", now["scripts"]))
print("      %-26s %d" % ("named checks", now["checks"]))
print("      %-26s %d" % ("no docstring", now["nodoc"]))
print()
print("      HOW A SCRIPT RECORDS ITS LIMITS:")
print("      %-26s %3d   machine-readable" % ("structured gaps = [...]", now["struct"]))
print("      %-26s %3d   prose only" % ("honesty / limits block", now["prose"]))
print("      %-26s %3d   nothing recognisable" % ("neither", now["neither"]))
recorded = now["struct"] + now["prose"]
print()
print("      records limits in SOME form : %d of %d  (%.0f%%)"
      % (recorded, now["scripts"], 100.0 * recorded / now["scripts"]))
print("      a TOOL can read them in     : %d of %d  (%.0f%%)"
      % (now["struct"], now["scripts"], 100.0 * now["struct"] / now["scripts"]))

check("most scripts DO record their limits",
      recorded > now["scripts"] / 2,
      "%d of %d -- the first version of this script said 5" % (recorded, now["scripts"]))
check("almost none of it is machine-readable",
      now["struct"] / now["scripts"] < 0.10,
      "%d structured against %d in prose" % (now["struct"], now["prose"]))
check("and a large minority record nothing at all",
      now["neither"] > now["scripts"] / 4,
      "%d scripts, %.0f%%" % (now["neither"], 100.0 * now["neither"] / now["scripts"]))

rule("2 . THE MOST-CHECKED SCRIPTS, AND HOW THEY RECORD LIMITS")
heavy = []
for d in sorted(os.listdir(ROOT)):
    p = os.path.join(ROOT, d)
    if not (os.path.isdir(p) and (d.startswith("book") or d in ("omega", "tools"))):
        continue
    for dirpath, _dirs, fs in os.walk(p):
        for f in sorted(fs):
            if not f.endswith(".py"): continue
            rel = os.path.relpath(os.path.join(dirpath, f), ROOT)
            src = open(os.path.join(dirpath, f), encoding="utf-8", errors="ignore").read()
            kind = ("structured" if STRUCT_RE.search(src)
                    else "prose" if PROSE_RE.search(src) else "NOTHING")
            heavy.append((rel, len(CHECK_RE.findall(src)), gaps_of(src), kind))
heavy.sort(key=lambda r: -r[1])
print("      %-42s %6s %6s  %s" % ("script", "checks", "gaps", "limits recorded as"))
for path, c, g, kind in heavy[:8]:
    print("      %-42s %6d %6d  %s" % (path, c, g, kind))
top8 = heavy[:8]
struct8 = sum(1 for _, _, _, k in top8 if k == "structured")
none8 = sum(1 for _, _, _, k in top8 if k == "NOTHING")
check("machine-readable gap records are rare even among the most-checked",
      struct8 <= 2,
      "%d of the top 8 carry a structured list (one of them backfilled today)"
      % struct8)
print("""
      ch-feynman-verify.py is the case that overturned this script's first
      conclusion. It has 25 named checks and scored ZERO gaps, because its
      record of limits is an HONESTY block in prose -- four things it does not
      establish, plus a statement of what would refute its chapter. That is a
      better gap record than most structured lists in the corpus, and the
      detector could not see it.""")

rule("3 . WHAT THIS MEANS, STATED NARROWLY")
print("""
      The corpus is not unaware of its limits. Fifty-one per cent of its
      scripts state them, some at length and with more care than the structured
      lists: ch-feynman-verify.py carries an HONESTY block with four things it
      does NOT establish and a statement of what would refute its chapter.

      The defect is that a tool cannot read any of it.

      A gap record has two jobs. It tells a READER what was not checked, and it
      tells a MACHINE what to go and get. The corpus does the first well and the
      second almost not at all -- 5 scripts of 122 in a form anything could
      parse. Whatever is built on top of these scripts later reads the second
      kind, and there are five.

      So the original claim was too strong and the structural point survives
      unchanged: a gap list is a request, and a request nobody can parse is not
      a request. What needs doing is not writing limits down. It is giving the
      ones already written a shape.""")

rule("4 . SELF-COUNT, AND DRIFT FROM THE BASELINE")
base = survey(BASELINE)
if base is None:
    print("      baseline %s not reachable in this clone -- drift not computed" % BASELINE)
    check("baseline resolves", False, "git ls-tree failed for %s" % BASELINE)
else:
    print("      %-12s %8s %8s" % ("", BASELINE, "HEAD"))
    for k in ("scripts", "checks", "gaps", "withgaps"):
        print("      %-12s %8d %8d   (%+d)" % (k, base[k], now[k], now[k] - base[k]))
    print("""
      This script and its chapter are inside the HEAD column. That is the point
      of printing both: WP-125 improves the very statistic it reports, and a
      reader who is shown only HEAD cannot see by how much.""")
    check("this script raises the gap count it is measuring",
          now["gaps"] > base["gaps"],
          "+%d gap entries, of which this file contributes its own"
          % (now["gaps"] - base["gaps"]))
    check("the ratio is still bad after this script improves it",
          now["checks"] / max(now["gaps"], 1) > 10,
          "one script does not fix a corpus-wide habit")

rule("5 . WHAT IS NOT KNOWN")
gaps = [
 ("THIS GAP WAS WRITTEN, PUBLISHED, AND NOT HEEDED",
  "the first version said the detector recognises two syntactic shapes and "
  "that the count was a floor -- then printed 4.1% as a headline anyway. The "
  "true figure is 51%. Recording a limitation is not the same as acting on "
  "one, and nothing in this corpus currently distinguishes the two"),
 ("the prose detector is a keyword list, so it over- and under-counts",
  "'SKIPPED' catches a script that merely skips a block; a limits paragraph "
  "using none of the keywords still reads as zero. The 57 is an estimate with "
  "error in both directions, and no entry count is attempted for prose"),
 ("'named check' means a call to check() -- a convention, not a law",
  "scripts using assert or bare prints are undercounted, and three scripts "
  "have no docstring at all and cannot be placed"),
 ("no claim is made that any particular script SHOULD have gaps",
  "some results are complete; this measures a habit across a corpus, and does "
  "not convict a file"),
 ("this script's gap counter double-counted before it was cross-checked",
  "it added two overlapping patterns and reported 31 where harvest.py "
  "reported 21 on the same tree; agreement between two instruments is the "
  "only thing that found it, and the headline ratio was wrong until it did"),
 ("the working-tree walk was not recursive in this script's first run",
  "it reported 4 FEWER scripts at HEAD than at a commit HEAD postdates; the "
  "baseline side used git ls-tree -r and recursed. Fixed. The self-count is "
  "the only thing that would have caught it, which is the argument for the rule"),
 ("the baseline is one commit, not a history",
  "whether the ratio has been worsening or improving over the corpus's life "
  "is unmeasured and would need a walk over many refs"),
]
for i, (g, why) in enumerate(gaps, 1):
    print("  %d. %s\n       -> %s" % (i, g, why))

rule()
if FAIL:
    print("FAILED: %d" % len(FAIL))
    for f in FAIL: print("   - " + f)
    sys.exit(1)
print("All checks passed.  %d gaps recorded above remain open." % len(gaps))
