#!/usr/bin/env python3
"""
self_reference.py -- the vicious-circle principle, applied to this repository.

WHY THIS EXISTS. Principia Mathematica (Whitehead and Russell, Vol I,
Introduction ch. II and *12) is built around one rule: no object may be defined
in terms of a totality that includes itself. The theory of logical types exists
to enforce it, and it enforces it by stratifying the RANGE OF A VARIABLE -- a
function may not take itself as argument, because its range is a lower type than
it is.

This repository keeps committing the fallacy and has patched three by hand
without naming the class:

  ch-van-der-pol-verify.py [6] asserted "van der Pol" appears in no chapter.
  Publishing the chapter put the phrase into the Book 7 index and two generated
  index pages, so the count it asserted on included the act of asserting it.

  Two verify scripts shipped a LITERAL control token meant to match nothing.
  Each file then contained it, so each found the other.

  ch-van-der-pol's Lienard row read 0 for a word printed twice on the page doing
  the counting -- a different cause (HTML entities), the same shape: the
  instrument inside the set it measures.

THE TEST, AND WHY IT IS ABOUT RANGE. A script is not in danger because it
contains a word. It is in danger when the TOTALITY IT COUNTS OVER contains the
script or the page it belongs to. So this tool works out, per script, what that
totality is:

  CORPUS-WIDE  -- it greps tracked files by extension, or walks the repo and
                  filters by suffix. The totality is a set of repo files, and
                  the script's own page (and sometimes the script) is in it.
  NARROW       -- it opens named files, or ranges over a tree outside the corpus
                  such as .lake/packages/mathlib. The totality cannot contain
                  the counter, so the principle is not engaged.

Only a CORPUS-WIDE script can commit the fallacy, and only if it does not
stratify. Stratification is recognised in any of the forms this repository
actually uses: a classify() returning 'self', a startswith guard on the script's
own stem, or an explicit exclusion of its own basename.

    python3 tools/self_reference.py            # report
    python3 tools/self_reference.py --strict    # exit 1 if any VICIOUS

LIMITS, stated. The range is inferred from literals and call shapes, not by
running anything; a script that builds its pathspec at run time reads as NARROW
whether or not it is. A pattern assembled from pieces is invisible here, which
is exactly the trick that fixes the control-token bug, so a clean report is
consistent with a script that assembles a bad pattern. This tool reports what it
examined rather than a bare verdict, so that a clean line can be checked instead
of believed. Standard library only.
"""
import os
import re
import subprocess
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

EXT_LITERAL = re.compile(r"""['"]\*(\.[a-z]{2,5})['"]""")
SUFFIX_TUPLE = re.compile(r"""endswith\(\s*\(([^)]*)\)\s*\)""")
GREPPY = re.compile(r"""git['"]?\s*,\s*['"]--no-optional-locks|git['"]\s*,\s*['"]grep|"""
                    r"""\bls-files\b|\bgit\s+grep\b|corpus_count""")
WALKY = re.compile(r"""os\.walk\(""")
OUTSIDE = re.compile(r"""\.lake|packages/mathlib|args\.upstream|urlopen|Desktop/AXLE|Desktop/GTCT""")
GUARD = re.compile(
    r"""return\s+['"]self['"]"""                    # a classify() bucket
    r"""|startswith\(\s*['"](?:book\d+/)?(?:ch|wp)[-\w]*['"]\s*\)"""
    r"""|exclude_finding"""                          # wp109's named guard
    r"""|keep_ruler|\bRULER\b"""                    # wp82's named guard
    r"""|basename\([^)]*\)\.startswith"""
    r"""|classify\s*\(|kind_of\s*\("""            # a classifier of any name
)
CALLS = re.compile(r"""\b(?:files|chapters|count|nfiles|raw_files|gap)\s*\(\s*(?:r?['"])""")
LITERAL = re.compile(r"""(?:^|[\s(,\[])r?(['"])((?:\\.|(?!\1).){2,120})\1""")


def ls(pathspec):
    r = subprocess.run(['git', '--no-optional-locks', 'ls-files', '--', pathspec],
                       cwd=REPO, capture_output=True, text=True)
    return sorted(l for l in r.stdout.splitlines() if l.strip())


def totality(src):
    """(kind, extensions) -- what set does this script count over?"""
    if OUTSIDE.search(src) and not GREPPY.search(src):
        return 'NARROW', set()
    exts = set(EXT_LITERAL.findall(src))
    for m in SUFFIX_TUPLE.finditer(src):
        exts |= {e for e in re.findall(r"""['"](\.[a-z]{2,5})['"]""", m.group(1))}
    if (GREPPY.search(src) or WALKY.search(src)) and exts:
        return 'CORPUS-WIDE', exts
    return 'NARROW', exts


def patterns_in(src):
    out = []
    for m in CALLS.finditer(src):
        lit = LITERAL.search(' ' + src[m.end() - 2:m.end() + 140])
        if lit:
            p = lit.group(2)
            if p and not p.startswith('*.'):
                out.append(p)
    return sorted(set(out))


def main():
    strict = '--strict' in sys.argv
    scripts = ls('*-verify.py')
    print('%d verify scripts tracked' % len(scripts))
    print('the question is not whether a script contains a word.')
    print('it is whether the set it counts over contains the script.\n')
    vicious, guarded, narrow, nopat, nopage = [], [], [], [], []
    for s in scripts:
        with open(os.path.join(REPO, s), encoding='utf-8', errors='replace') as fh:
            src = fh.read()
        kind, exts = totality(src)
        page = None
        stem = s[:-len('-verify.py')]
        for ext in ('.html', '.md', '.tex'):
            if os.path.exists(os.path.join(REPO, stem + ext)):
                page = stem + ext; break
        if page is None:
            # a script's page may carry a longer title than the script does:
            # book6/wp82-verify.py belongs to book6/wp82-the-missing-floor.html.
            # Matching on the stem alone reported "no page" and mis-filed it.
            d, base = os.path.split(stem)
            lead = re.split(r'[-_]', base)[0]
            if lead:
                cands = [f for f in ls(os.path.join(d, lead + '*') if d else lead + '*')
                         if f.endswith(('.html', '.md', '.tex')) and '-verify' not in f]
                if cands:
                    page = sorted(cands, key=len)[0]
        # is the counter inside its own totality?
        inside = []
        if kind == 'CORPUS-WIDE':
            if '.py' in exts:
                inside.append(s)
            if page and os.path.splitext(page)[1] in exts:
                inside.append(page)
        pats = patterns_in(src)
        strat = bool(GUARD.search(src))
        row = (s, page, kind, sorted(exts), inside, len(pats), strat)
        if kind != 'CORPUS-WIDE':
            narrow.append(row)
        elif not pats:
            nopat.append(row)
        elif inside and not strat:
            vicious.append(row)
        elif inside:
            guarded.append(row)
        else:
            nopage.append(row)

    def dump(title, rows, detail):
        print('%s  (%d)' % (title, len(rows)))
        for s, page, kind, exts, inside, npats, strat in rows:
            if detail:
                print('   %-42s range %s %-22s patterns %2d  stratified %s'
                      % (s, kind, ','.join(exts) or '-', npats, 'yes' if strat else 'NO'))
                if inside:
                    print('       inside its own range: %s' % ', '.join(inside))
            else:
                print('   %-42s %s' % (s, ','.join(exts) or '-'))
        print()

    dump('VICIOUS -- corpus-wide range containing the counter, not stratified', vicious, True)
    dump('GUARDED -- corpus-wide and inside its own range, and stratifies', guarded, True)
    dump('NARROW -- counts named files or a tree outside the corpus', narrow, False)
    dump('CORPUS-WIDE but counts no pattern this tool can read', nopat, False)
    dump('CORPUS-WIDE, counts patterns, but the counter is NOT in its own range', nopage, True)
    print('vicious %d   guarded %d   narrow %d   unread %d   out-of-range %d'
          % (len(vicious), len(guarded), len(narrow), len(nopat), len(nopage)))
    print('\nPM Introduction ch. II. A GUARDED script is the theory of types,')
    print('kept by hand, once per script. A VICIOUS one is the fallacy, live.')
    if strict and vicious:
        sys.exit(1)


if __name__ == '__main__':
    main()
