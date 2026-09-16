#!/usr/bin/env python3
"""
corpus_count.py -- count tracked corpus files matching a pattern, correctly.

WHY THIS EXISTS. The corpus measures itself with `git grep -il`, and that
instrument has three failure modes. Two of them are recorded; the third was
found on 2026-09-16 and is the worst, because it produces false ZEROS on text
that is plainly visible on the page.

  1. WRONG SPELLING (WP-82 section 4, recorded). `k-theory` does not match
     `K theory` or `$K$-theory`. A 0 means "zero in that spelling".

  2. SUBSTRING INFLATION (found 2026-09-16, book7/ch-conley-verify.py [7]).
     An unanchored pattern matches inside longer words: /gns/ returns 68 files
     because of "designs" and "assignments"; /bott/ returns 810 because of
     "bottom". Both anchor to 0. A count without an anchor is not a measurement.

  3. HTML ENTITIES (found 2026-09-16). The corpus is HTML, and accented names
     are written as entities. `Li&eacute;nard` renders as Liénard and matches
     neither /lienard/ nor /liénard/. Measured at d97154e:

         pattern              plain   entity-aware
         Lienard                  2        5
         Poincare                58       68
         Godel                   23       27
         Poincare-Bendixson      12       14

     Sixty-eight tracked HTML files carry at least one accented entity, so this
     is not a corner case. Every published count for a name with a diacritic is
     low until it is taken through this module.

USE

    from tools.corpus_count import files, count      # or add tools/ to sys.path
    files('li[eé]nard')            -> ['book6/wp120-...', 'book7/ch-van-der-pol.html', ...]

    python3 tools/corpus_count.py 'poincar[eé]'
    python3 tools/corpus_count.py --raw 'poincar[eé]'     # the git grep answer, for comparison

METHOD. `git grep -l` is used only to shortlist candidate files cheaply; the
match itself is made against the file's text with entities unescaped and tags
left in place, so `Li&eacute;nard` and `Li<em>é</em>nard` both match. Tracked
files only, per R13. Standard library only.
"""
import html as _html
import os
import re
import subprocess
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_EXT = ('*.html', '*.md')


def _tracked(ref, ext):
    """Tracked paths matching ext. `git ls-tree` does not honour a *.html
    pathspec the way `ls-files` and `grep` do -- it returns nothing and exits 0,
    which is a silent empty answer and exactly the failure class this module is
    about. So: list everything, filter here."""
    r = subprocess.run(['git', '--no-optional-locks', 'ls-tree', '-r', '--name-only', ref],
                       cwd=REPO, capture_output=True, text=True)
    import fnmatch
    pats = ['*' + e[1:] if e.startswith('*') else e for e in ext]
    out = []
    for l in r.stdout.splitlines():
        l = l.strip()
        if l and any(fnmatch.fnmatch(l, p) for p in pats):
            out.append(l)
    return out


def _text(path, ref):
    if ref in (None, 'WORKTREE'):
        try:
            with open(os.path.join(REPO, path), encoding='utf-8', errors='replace') as fh:
                raw = fh.read()
        except OSError:
            return ''
    else:
        r = subprocess.run(['git', '--no-optional-locks', 'show', '%s:%s' % (ref, path)],
                           cwd=REPO, capture_output=True, text=True)
        raw = r.stdout
    # Unescape entities so Li&eacute;nard reads as Liénard. Tags are NOT stripped:
    # a caller who wants prose-only text can strip them, but stripping here would
    # silently change what "a file contains this word" means.
    return _html.unescape(raw)


def files(pattern, ref='HEAD', ext=DEFAULT_EXT, strip_tags=False):
    """Tracked files whose entity-unescaped text matches `pattern` (case-insensitive)."""
    rx = re.compile(pattern, re.I)
    out = []
    for path in _tracked(ref, ext):
        t = _text(path, ref)
        if strip_tags:
            t = re.sub(r'<[^>]+>', ' ', t)
        if rx.search(t):
            out.append(path)
    return sorted(out)


def count(pattern, ref='HEAD', ext=DEFAULT_EXT, strip_tags=False):
    return len(files(pattern, ref, ext, strip_tags))


def raw_files(pattern, ref='HEAD', ext=DEFAULT_EXT):
    """What plain `git grep -ilE` returns -- kept so the gap can be printed."""
    r = subprocess.run(['git', '--no-optional-locks', 'grep', '-ilE', pattern, ref, '--', *ext],
                       cwd=REPO, capture_output=True, text=True)
    return sorted(l.split(':', 1)[1] for l in r.stdout.splitlines() if ':' in l)


def gap(pattern, ref='HEAD', ext=DEFAULT_EXT):
    """Files this module finds that plain git grep misses."""
    a = set(raw_files(pattern, ref, ext))
    return [f for f in files(pattern, ref, ext) if f not in a]


if __name__ == '__main__':
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    if not args:
        print(__doc__)
        sys.exit(0)
    pat = args[0]
    ref = args[1] if len(args) > 1 else 'HEAD'
    if '--raw' in sys.argv:
        for f in raw_files(pat, ref):
            print(f)
        sys.exit(0)
    found = files(pat, ref)
    missed = gap(pat, ref)
    for f in found:
        print('%s%s' % (f, '   <-- plain git grep misses this' if f in missed else ''))
    print('\n%d files  (plain git grep: %d, missing %d)'
          % (len(found), len(raw_files(pat, ref)), len(missed)))
