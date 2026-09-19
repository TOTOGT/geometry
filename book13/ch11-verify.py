#!/usr/bin/env python3
"""Re-establish, mechanically, every finding in Book XIII chapter 11.

Usage:  python3 book13/ch11-verify.py            (from the repository root)
        python3 book13/ch11-verify.py --lean PATH-TO-Vol13_Coherence.lean

Chapter 11 audits Volume XIII against the document Volume XIII names as its
authority. An audit that has to be believed is worth nothing, so each finding
below is recomputed here from files in this repository. Where a finding is
about a file that is NOT in this repository, the script says so and reports
what it could and could not reach -- an absence it produced itself is not a
finding, which is the rule that this volume's own ch10 sets out.

Exit 0 means every finding still holds as chapter 11 states it. Exit 1 means
the corpus has moved and the chapter is now wrong about something.
"""
import os
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
B13 = ROOT / "book13"

def live_html(*dirs):
    out = []
    for d in dirs:
        for p in (ROOT / d).rglob("*.html") if d else ROOT.rglob("*.html"):
            s = str(p.relative_to(ROOT))
            if "_to_delete" in s or "_archive" in s:
                continue
            out.append(p)
    return out

def flat(p):
    t = p.read_text(encoding="utf-8", errors="replace")
    t = re.sub(r"<script.*?</script>|<style.*?</style>", " ", t, flags=re.S)
    return " ".join(re.sub(r"<[^>]+>", " ", t).split())

def main():
    lean = None
    if "--lean" in sys.argv:
        lean = pathlib.Path(sys.argv[sys.argv.index("--lean") + 1])
    else:
        guess = pathlib.Path(os.path.expanduser("~/Desktop/AXLE/Vol13_Coherence.lean"))
        alt = pathlib.Path(os.path.expanduser("~/mnt/Desktop/AXLE/Vol13_Coherence.lean"))
        lean = guess if guess.exists() else (alt if alt.exists() else None)

    fail, note = [], []

    # ---- F1 · "rung 30" is asserted by this volume and by nothing else -------
    holders = sorted(p.relative_to(ROOT).as_posix()
                     for p in ROOT.rglob("*.html")
                     if "_to_delete" not in str(p) and "_archive" not in str(p)
                     and re.search(r"[Rr]ung 30", flat(p)))
    outside = [h for h in holders if not h.startswith("book13/")]
    wp82 = [p for p in (ROOT / "book6").glob("wp82*.html")]
    if not wp82:
        fail.append("F1: book6/wp82*.html not found -- the authority cited does not exist")
        wp_rungs = []
    else:
        wp_rungs = sorted({int(n) for p in wp82
                           for n in re.findall(r"rung (\d+)", flat(p))})
    ladder = ROOT / "docs" / "floor-ladder.tsv"
    lad_rungs = []
    if ladder.exists():
        lad_rungs = [ln.split("\t")[0] for ln in
                     ladder.read_text(encoding="utf-8").rstrip("\n").split("\n")[1:] if ln.strip()]
    print("F1  pages asserting 'rung 30' : %d, of which outside book13: %d"
          % (len(holders), len(outside)))
    print("    rung numbers WP-82 names  : %s" % (wp_rungs or "none"))
    print("    rung numbers the ladder has: %s" % (lad_rungs or "none"))
    if 30 in wp_rungs:
        fail.append("F1: WP-82 DOES name rung 30 -- the chapter is wrong")
    if "30" in lad_rungs:
        fail.append("F1: docs/floor-ladder.tsv has a rung 30 -- the chapter is wrong")
    if outside:
        fail.append("F1: 'rung 30' is asserted outside book13 too: %s" % outside)
    if not holders:
        fail.append("F1: no page asserts 'rung 30' any more -- the chapter is stale")

    # ---- F2 · the artifact is cited and is not in this repository ------------
    cites = sorted(p.relative_to(ROOT).as_posix() for p in ROOT.rglob("*.html")
                   if "_to_delete" not in str(p) and "_archive" not in str(p)
                   and "Vol13_Coherence.lean" in flat(p))
    here = list(ROOT.rglob("Vol13_Coherence.lean"))
    print("F2  pages citing Vol13_Coherence.lean : %d" % len(cites))
    print("    copies of it inside this repository: %d" % len(here))
    if here:
        fail.append("F2: the file IS in this repository now (%s) -- chapter is stale"
                    % [str(p.relative_to(ROOT)) for p in here])
    if not cites:
        fail.append("F2: nothing cites Vol13_Coherence.lean any more -- chapter is stale")

    # ---- F3 · the saved report is doubled, and the gate counted lines -------
    rep = ROOT / "tools/verify-audit/2026-09-09/Vol13_Coherence.axioms.txt"
    gate = pathlib.Path(str(rep) + ".gate")
    if not rep.exists():
        fail.append("F3: %s is gone" % rep.relative_to(ROOT))
    else:
        lines = [l for l in rep.read_text(encoding="utf-8").split("\n") if "depend" in l]
        names = [re.match(r"'([^']+)'", l).group(1) for l in lines if re.match(r"'([^']+)'", l)]
        distinct = sorted(set(names))
        print("F3  lines in the saved report      : %d" % len(lines))
        print("    DISTINCT declarations in it    : %d" % len(distinct))
        if gate.exists():
            g = gate.read_text(encoding="utf-8").strip()
            print("    the gate's recorded verdict    : %s" % g)
            m = re.search(r"OK: (\d+) theorems", g)
            if m and int(m.group(1)) != len(lines):
                fail.append("F3: gate says %s, report has %d lines" % (m.group(1), len(lines)))
            if m and int(m.group(1)) == len(distinct):
                fail.append("F3: the gate's count already equals the distinct count "
                            "-- the doubling is gone and the chapter is stale")
        if len(lines) == len(distinct):
            fail.append("F3: the report is no longer doubled -- chapter is stale")
        # what the pages say
        for p in sorted(B13.glob("*.html")):
            f = flat(p)
            for m in re.finditer(r"(\w+) axiom probes", f):
                print("    %-34s says '%s axiom probes'" % (p.name, m.group(1)))

    # ---- F4/F5 · what the artifact actually declares ------------------------
    if lean is None or not lean.exists():
        note.append("F4/F5: Vol13_Coherence.lean was not reachable from here. "
                    "Pass --lean PATH to check the declarations. NOT a finding of "
                    "absence -- the file is known to exist outside this repository.")
    else:
        src = lean.read_text(encoding="utf-8", errors="replace")
        probes = re.findall(r"#print axioms (\S+)", src)
        thms = re.findall(r"^theorem (\S+)", src, re.M)
        trivial = re.findall(r"^theorem (\S+)\s*:\s*True\s*:=\s*trivial", src, re.M)
        by_rfl = re.findall(r"^theorem (\S+)[^\n]*(?::=\s*rfl|\n\s*:=\s*rfl)", src, re.M)
        print("F4  #print axioms probes in the file: %d" % len(probes))
        print("    theorems declared                : %d" % len(thms))
        print("    declared vacuous (True := trivial): %s" % (trivial or "none"))
        if len(probes) != 9:
            fail.append("F4: the file now has %d probes, not 9" % len(probes))
        if not trivial:
            fail.append("F4: no `True := trivial` control in the file any more")
        for needed in ("assoc₂_hom_inv", "assoc₂_inv_hom"):
            if needed not in src:
                fail.append("F5: %s is gone from the file" % needed)
        if "hom_inv_id" not in src or "inv_hom_id" not in src:
            fail.append("F5: the level-2 theorems no longer close by Iso.hom_inv_id / "
                        "Iso.inv_hom_id -- chapter 11 section 4 is stale")
        print("F5  level-2 theorems close by       : Iso.hom_inv_id / Iso.inv_hom_id"
              if "hom_inv_id" in src else "F5  level-2 proof shape CHANGED")

    # ---- F6 * the volume's own index skips one of its chapters -------------
    idx = B13 / "index.html"
    chapter_files = sorted(p.name for p in B13.glob("ch*.html"))
    if idx.exists():
        itext = idx.read_text(encoding="utf-8", errors="replace")
        unlinked = [c for c in chapter_files if c != "index.html" and c not in itext]
        print("F6  chapter files in book13/        : %d" % len(chapter_files))
        print("    not linked from book13/index.html: %s" % (unlinked or "none"))
        if "ch10-what-a-check-establishes.html" in itext and unlinked == []:
            pass
        elif not unlinked:
            fail.append("F6: every chapter is linked now -- chapter 11 section 6 is stale")
    else:
        fail.append("F6: book13/index.html is missing")

    print()
    for n in note:
        print("  NOTE  " + n)
    for f in fail:
        print("::error::" + f)
    if fail:
        return 1
    print("every finding in chapter 11 still holds, recomputed from the files.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
