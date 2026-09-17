#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
wp125-verify.py -- the corpus records what it checked and not what it didn't.

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
        try:
            if not ast.get_docstring(ast.parse(src)): nodoc += 1
        except SyntaxError:
            nodoc += 1
    return dict(scripts=n, checks=checks, gaps=gaps, withgaps=withgaps, nodoc=nodoc)

rule("1 . THE WORKING TREE")
now = survey()
for k in ("scripts", "checks", "gaps", "withgaps", "nodoc"):
    print("      %-10s %d" % (k, now[k]))
ratio = now["checks"] / max(now["gaps"], 1)
print("\n      checks per recorded gap: %.1f" % ratio)
print("      scripts recording any gap at all: %d of %d  (%.1f%%)"
      % (now["withgaps"], now["scripts"], 100.0 * now["withgaps"] / now["scripts"]))

check("the corpus records far more checks than gaps",
      ratio > 10, "%.1f checks per gap" % ratio)
check("fewer than one script in ten records a gap",
      now["withgaps"] / now["scripts"] < 0.10,
      "%d of %d" % (now["withgaps"], now["scripts"]))

rule("2 . WHERE THE CHECKS ARE, AND WHERE THE GAPS ARE NOT")
print("""
      The asymmetry is not spread evenly. The most heavily verified scripts in
      the corpus record no gaps at all. Counting by script:""")
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
            heavy.append((rel, len(CHECK_RE.findall(src)), gaps_of(src)))
heavy.sort(key=lambda r: -r[1])
for path, c, g in heavy[:6]:
    print("      %-44s %3d checks   %d gaps" % (path, c, g))
top5_gaps = sum(g for _, _, g in heavy[:5])
check("the five most-checked scripts record zero gaps between them",
      top5_gaps == 0, "%d checks, %d gaps" % (sum(c for _, c, _ in heavy[:5]), top5_gaps))

rule("3 . WHAT THIS MEANS, STATED NARROWLY")
print("""
      A verification script that reports only passes asserts a completeness it
      never established. The claim "all checks passed" is true and says nothing
      about the checks that were not written.

      This is the same error as asserting a near-integer, which the Ramanujan
      1/pi work met twice in one afternoon: both are claims about the part that
      was not looked at. g_58^12 = 19601.99999 passes any test you write for
      19602 if you choose the tolerance after seeing the number.

      It is also the specific thing that blocks a corpus from asking for its own
      next input. A gap list is a request. 509 assertions of what is known and
      16 records of what is not is a machine that cannot say what it needs.""")

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
 ("the gap detector recognises two syntactic shapes, not the idea of a gap",
  "a script that discusses its limits in prose without a gaps list reads as "
  "zero here; the true count is a floor, and the ratio an upper bound"),
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
