#!/usr/bin/env python3
"""
proved_labels.py -- where a page names a kernel-checked declaration, say so,
and link to the Lean.

R22 moved the green Lean into geometry. R1 says only kernel-audited counts as
evidence. R11 says a declaration named in prose must resolve at the path cited.
Those three together mean a page that names a green declaration and carries no
PROVED label is understating what it has -- and a reader cannot find the proof.

This closes that. For each page it:
  1. collects every declaration the page names,
  2. keeps only those appearing in an axiom report with NO sorryAx,
  3. requires the declaration to RESOLVE -- to be declared in a .lean file in
     this repo, at a line this script records,
  4. appends one PROVED block listing them, each linked to its file and line.

It does not touch prose. It appends a single block before the footer, and it is
idempotent: a page already carrying the block is skipped.

    python3 tools/proved_labels.py            report only, writes nothing
    python3 tools/proved_labels.py --write    insert the blocks
"""
import collections, glob, io, os, re, sys

MARK = "po-proved-block"
SKIP_DIRS = ("_archive/", "_to_delete/", "docs/", ".lake/")

def axiom_reports():
    green, dirty = {}, {}
    for r in glob.glob("**/*.txt", recursive=True):
        if "axiom" not in r.lower() or r.startswith(SKIP_DIRS): continue
        for line in io.open(r, encoding="utf-8", errors="replace"):
            m = re.match(r"^'([^']+)' depends on axioms: \[([^\]]*)\]", line.strip())
            if m:
                (dirty if "sorryAx" in m.group(2) else green)[m.group(1)] = r
    return green, dirty

def lean_index():
    """short name -> (file, line). A declaration must be HERE to be linkable."""
    idx = {}
    pat = re.compile(r"^\s*(?:@\[[^\]]*\]\s*)?(?:private\s+|protected\s+|noncomputable\s+)*"
                     r"(theorem|lemma|def|abbrev|instance)\s+([A-Za-z_][A-Za-z0-9_'!?]*)")
    for f in glob.glob("**/*.lean", recursive=True):
        if f.startswith(SKIP_DIRS): continue
        for n, line in enumerate(io.open(f, encoding="utf-8", errors="replace"), 1):
            m = pat.match(line)
            if m: idx.setdefault(m.group(2), (f, n))
    return idx

GREEN, DIRTY = axiom_reports()
LEAN = lean_index()
SHORT = collections.defaultdict(set)
for full in GREEN:
    SHORT[full.split(".")[-1]].add(full)
DIRTY_SHORT = {d.split(".")[-1] for d in DIRTY}

CSS = """<style>
.po-proved-block{max-width:820px;margin:2.5rem auto 1rem;padding:1.1rem 1.3rem;
 border:1px solid rgba(122,148,113,.45);border-left:4px solid #7a9471;border-radius:0 6px 6px 0;
 background:rgba(122,148,113,.07);font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:.8rem;line-height:1.75;}
.po-proved-block .po-h{letter-spacing:.14em;text-transform:uppercase;font-size:.68rem;color:#5f7a57;margin-bottom:.6rem;}
.po-proved-block a{color:inherit;text-decoration:underline;text-underline-offset:2px;}
.po-proved-block .po-n{font-size:.68rem;opacity:.75;display:block;margin-top:.7rem;line-height:1.6;}
</style>"""

def block(rel, names):
    depth = rel.count("/")
    up = "../" * depth
    items = []
    for short in sorted(names):
        f, ln = LEAN[short]
        items.append('<a href="%s%s">%s</a> <span style="opacity:.6">%s:%d</span>'
                     % (up, f, short, f, ln))
    return (CSS + '\n<div class="%s">\n  <div class="po-h">Proved &middot; kernel-checked</div>\n'
            '  %s\n  <span class="po-n">Each name above is declared in this repository at the '
            'line shown and appears in an axiom report with no <code>sorryAx</code>. '
            'A clean axiom report is not a reading of the statement: per R20, a theorem can '
            'assume its conclusion and still report clean. Follow the link before citing one '
            'as evidence.</span>\n</div>\n' % (MARK, "<br>\n  ".join(items)))

def main(write=False):
    pages = [p for p in glob.glob("**/*.html", recursive=True) if not p.startswith(SKIP_DIRS)]
    hits, skipped, tainted = {}, 0, collections.defaultdict(set)
    for p in pages:
        s = io.open(p, encoding="utf-8", errors="replace").read()
        if MARK in s: skipped += 1; continue
        found = set()
        for short in SHORT:
            if len(short) < 7: continue
            if short not in LEAN: continue          # must resolve, R11
            if re.search(r"\b" + re.escape(short) + r"\b", s): found.add(short)
        for short in DIRTY_SHORT:
            if len(short) >= 7 and re.search(r"\b" + re.escape(short) + r"\b", s):
                tainted[p].add(short)
        if found: hits[p] = found
    print("=" * 74)
    print("PROVED LABELS -- pages naming a kernel-checked, resolvable declaration")
    print("=" * 74)
    print("  green declarations in axiom reports : %d" % len(GREEN))
    print("  of those, declared in a .lean here  : %d" % sum(1 for s in SHORT if s in LEAN))
    print("  sorryAx-tainted declarations        : %d" % len(DIRTY))
    print("  pages already carrying the block    : %d" % skipped)
    print("  pages to label                      : %d" % len(hits))
    print()
    for p, v in sorted(hits.items(), key=lambda kv: -len(kv[1]))[:18]:
        print("   %-50s %2d  %s" % (p, len(v), ", ".join(sorted(v)[:3])))
    if tainted:
        print()
        print("  PAGES NAMING A sorryAx DECLARATION -- not labelled, and they must disclose:")
        for p, v in sorted(tainted.items()): print("     %-48s %s" % (p, ", ".join(sorted(v))))
    if not write:
        print("\n  report only. pass --write to insert.")
        return
    n = 0
    for p, v in hits.items():
        s = io.open(p, encoding="utf-8", errors="replace").read()
        b = block(p, v)
        low = s.lower()
        i = low.rfind("<footer")
        if i == -1: i = low.rfind("</body>")
        if i == -1: continue
        io.open(p, "w", encoding="utf-8").write(s[:i] + b + s[i:])
        n += 1
    print("\n  inserted into %d pages." % n)

if __name__ == "__main__":
    main("--write" in sys.argv)
