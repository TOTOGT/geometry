#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
placement_check.py  --  keeps docs/math-placement-map.md honest.

Three jobs, none of them clever:

  [1] every file the map names must exist
  [2] every producing script in the corpus must be placed, or reported unplaced
  [3] rows the map marks "to write" are reported as PLANNED, so an assertion of
      intent never reads as an assertion of fact

It does NOT check that a file does the job the map claims for it. Nothing
automates that, and section 5 of the map says so.

Run from the repo root:  python3 tools/placement_check.py
Exit 1 if a named file is missing.  Unplaced scripts are reported, not fatal --
they are the queue, and an empty queue would mean the corpus had stopped.
"""

import os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAP = os.path.join(ROOT, "docs", "math-placement-map.md")

def rule(t=""):
    print("\n" + "=" * 78)
    if t:
        print(t); print("=" * 78)

if not os.path.exists(MAP):
    print("FATAL: %s not found" % MAP); sys.exit(1)
text = open(MAP, encoding="utf-8").read()

# ---------------------------------------------------------------- [1] named files
rule("1 . FILES THE MAP NAMES")
# backticked paths that look like repo files
# Only backticked strings containing a directory separator are treated as repo
# paths. A bare filename in prose ("run placement_check.py") is a mention, not a
# path, and the first version of this script reported two of them as MISSING.
cited = sorted(set(re.findall(r"`([A-Za-z0-9_.-]+/[A-Za-z0-9_./-]+\.(?:py|html|lean|md))`", text)))
missing, present, external = [], [], []
for c in cited:
    if c.startswith("neuro/") or c.startswith("~"):
        external.append(c); continue
    p = os.path.join(ROOT, c)
    (present if os.path.exists(p) else missing).append(c)

for c in present:
    print("  ok       %s" % c)
for c in external:
    print("  external %s   (another repository; not checked here)" % c)
for c in missing:
    print("  MISSING  %s" % c)

# --------------------------------------------------------------- [2] placed or not
rule("2 . PRODUCING SCRIPTS -- PLACED OR UNPLACED")
scripts = []
for d in sorted(os.listdir(ROOT)):
    full = os.path.join(ROOT, d)
    if not os.path.isdir(full) or d.startswith("."):
        continue
    if not (d.startswith("book") or d == "omega"):
        continue
    for f in sorted(os.listdir(full)):
        if f.endswith(".py"):
            scripts.append("%s/%s" % (d, f))

placed = [s for s in scripts if s in text]
unplaced = [s for s in scripts if s not in text]
print("  %d producing scripts found, %d named in the map, %d unplaced"
      % (len(scripts), len(placed), len(unplaced)))
if unplaced:
    print("\n  UNPLACED -- this is the queue, not an error:")
    for s in unplaced:
        print("      %s" % s)

# -------------------------------------------------------------------- [3] planned
rule("3 . PLANNED PLACEMENTS -- ASSERTED, NOT BUILT")
planned = text.count("**to write**")
print("  %d table cells marked 'to write'." % planned)
print("  These are placements this map ASSERTS and the corpus has NOT built.")
print("  They are intent. Reading them as done is the failure this block exists")
print("  to prevent.")

# ------------------------------------------------------------------- [4] the split
rule("4 . THE WP-124 COLLISION")
wp124 = os.path.join(ROOT, "book6", "wp124-three-segments-away.html")
mapten = os.path.join(ROOT, "book7", "ch-the-map-on-page-ten.html")
claude = os.path.join(ROOT, "CLAUDE.md")
both = os.path.exists(wp124) and os.path.exists(mapten)
claims = "WP-124" in open(claude, encoding="utf-8").read() if os.path.exists(claude) else False
print("  book6/wp124-three-segments-away.html exists : %s" % os.path.exists(wp124))
print("  book7/ch-the-map-on-page-ten.html exists    : %s" % os.path.exists(mapten))
print("  CLAUDE.md mentions WP-124                   : %s" % claims)
if both and claims:
    print("""
  STILL OPEN. Two chapters are called WP-124. Only one occupies a wp-numbered
  filename. This script will not pick, because the numbering is the owner's and
  a script that renamed a published file would break its own index.""")

rule()
if missing:
    print("FAILED: %d file(s) named in the map do not exist." % len(missing))
    for m in missing: print("   - " + m)
    sys.exit(1)
print("Map is consistent with the tree. %d unplaced scripts remain queued."
      % len(unplaced))
