#!/usr/bin/env python3
"""
WP-82 -- the ruler, re-measured, and checked against its own stated method.

WHY THIS FILE EXISTS. WP-82's rung table is a DATED measurement: it states its
own method and its own commit -- "tracked *.html and *.md files containing at
least one case-insensitive match, taken at commit 654fb06 on 2026-08-29". A
dated measurement does not decay into an error, it decays into a measurement
about a day that has passed. Nothing in the repository re-ran it, so nothing
could say how far it had moved, and on 2026-09-15 a reading of the rung-30 row
as a live count produced a wrong conclusion about Volume XIII.

WHAT IT CHECKS.
  [1] The method reproduces. Every number printed in the table is recomputed at
      654fb06, the commit the paper names. This is the strongest block here:
      a source checked against itself, on its own terms.
  [2] The same method at HEAD, and the drift.
  [3] What the drift is made of -- a file count counts index pages and the
      ruler itself, so the composition is printed, not just the total.
  [4] The two claims §3 makes about specific volumes.
  [5] Control.

Standard library only, but it shells out to git, which the repo requires for
any tracked-file count (R13: the corpus is tracked files, not the working tree).

    python3 book6/wp82-verify.py
"""
import subprocess, sys, os

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
fails = []
def check(ok, msg, detail=''):
    print('    %s  %s%s' % ('PASS' if ok else 'FAIL', msg, ('  -- ' + detail) if detail and not ok else ''))
    if not ok: fails.append(msg)
def head(n, t):
    print('\n' + '=' * 70 + '\n  [%s]  %s\n' % (n, t) + '=' * 70)

def files(pattern, ref):
    """WP-82's method: tracked *.html and *.md, case-insensitive, file count."""
    r = subprocess.run(['git', '--no-optional-locks', 'grep', '-lic', '-e', pattern,
                        ref, '--', '*.html', '*.md'],
                       cwd=REPO, capture_output=True, text=True)
    return set(l.split(':', 1)[1] for l in r.stdout.splitlines() if ':' in l)

def count(patterns, ref):
    s = set()
    for p in patterns: s |= files(p, ref)
    return len(s), s

BASE   = '654fb06'        # the commit WP-82's first column names
SECOND = 'd97154e'        # the commit its second column names, added 2026-09-16
                          # after six rows moved inside a single day. A date is
                          # not a commit; both columns now name one.
ROWS = [                  # (rung, field, patterns, col-1 @BASE, col-2 @SECOND)
    ('28', 'K-Theory & Index Theory',   ['k-theory'],                          0, 9),
    ('28', '  index theorem',           ['index theorem'],                     1, 6),
    ('28', '  Atiyah',                  ['atiyah'],                            1, 5),
    ('29', 'Operator Algebras',         ['operator algebra'],                 76, 100),
    ('29', '  von Neumann',             ['von neumann'],                       7, 12),
    ('30', 'Higher Category Theory',    ['∞-categor', 'infinity-categor'],     0, 3),
    ('31', 'Derived Algebraic Geometry',['sheaf', 'sheaves'],                   1, 7),
    ('32', 'Motivic / Langlands',       ['motivic', 'langlands'],               3, 7),
    ('33', 'Noncommutative Geometry',   ['noncommutative'],                     9, 17),
    ('33', '  Connes',                  ['connes'],                            15, 27),
    ('33', '  spectral triple',         ['spectral triple'],                    7, 15),
    ('--', 'Monstrous Moonshine',       ['moonshine'],                         25, 28),
]

# ---------------------------------------------------------------------------
head(1, "THE PAPER'S OWN TABLE, RECOMPUTED AT THE COMMIT IT NAMES")
r = subprocess.run(['git', '--no-optional-locks', 'cat-file', '-t', BASE],
                   cwd=REPO, capture_output=True, text=True)
check(r.stdout.strip() == 'commit', 'commit %s is in this repository' % BASE, r.stdout.strip())
print('  Method, quoted from the page: "the number of tracked *.html and *.md files')
print('  containing at least one case-insensitive match, taken at commit 654fb06')
print('  on 2026-08-29."\n')
print('     %5s %-28s %10s %10s' % ('rung', 'field', 'printed', 'recomputed'))
ok_repro = True
base_n = {}
for rung, field, pats, printed, printed2 in ROWS:
    n, _ = count(pats, BASE)
    base_n[field] = n
    flag = '' if n == printed else '   <-- MISMATCH'
    print('     %5s %-28s %10d %10d%s' % (rung, field, printed, n, flag))
    if n != printed: ok_repro = False
check(ok_repro, 'every one of the %d published numbers reproduces exactly' % len(ROWS))
print('\n     The table was right on the day it was taken, the rung-30 zero included.')
print('     book13 was stubbed the same day in 9d78ff8, but 654fb06 precedes it and')
print('     book13/ch06-past-two.html does not exist in that tree. The measurement')
print('     is sound and so is its date; what it is not is current.')

# ---------------------------------------------------------------------------
head(2, 'THE SECOND COLUMN, AT THE COMMIT IT NAMES -- AND TODAY')
print('  The second column was first published against HEAD rather than a named')
print('  commit, and six of its twelve rows moved inside a single day. A date is')
print('  not a commit. It now names %s, and reproduces there the way the first' % SECOND)
print('  column reproduces at %s. The live HEAD column is printed for information' % BASE)
print('  and asserted only for monotonicity.\n')
print('     %5s %-28s %10s %10s %8s %8s' % ('rung', 'field', '@' + BASE, '@' + SECOND, 'recomp', 'HEAD'))
head_n = {}
ok_repro2 = True
for rung, field, pats, printed, printed2 in ROWS:
    n2, _ = count(pats, SECOND)
    nh, _ = count(pats, 'HEAD')
    head_n[field] = nh
    flag = '' if n2 == printed2 else '   <-- MISMATCH'
    print('     %5s %-28s %10d %10d %8d %8d%s'
          % (rung, field, base_n[field], printed2, n2, nh, flag))
    if n2 != printed2: ok_repro2 = False
check(ok_repro2,
      'every one of the %d numbers in the second column reproduces at %s' % (len(ROWS), SECOND))
check(all(head_n[f] >= base_n[f] for _, f, _, _, _ in ROWS),
      'no row went down between %s and HEAD, so nothing was lost from the corpus' % BASE)
r28_b = sum(base_n[f] for r_, f, _, _, _ in ROWS if r_ == '28')
r28_h = sum(head_n[f] for r_, f, _, _, _ in ROWS if r_ == '28')
r33_b = sum(base_n[f] for r_, f, _, _, _ in ROWS if r_ == '33')
r33_h = sum(head_n[f] for r_, f, _, _, _ in ROWS if r_ == '33')
print('\n     rung 28 total : %3d  ->  %3d' % (r28_b, r28_h))
print('     rung 33 total : %3d  ->  %3d' % (r33_b, r33_h))
print('     ratio 33 : 28 : %.1f  ->  %.1f' % (r33_b / max(r28_b, 1), r33_h / max(r28_h, 1)))
check(r28_h > r28_b, 'rung 28, the missing floor, is no longer at zero mentions')
check(r33_h / max(r28_h, 1) < r33_b / max(r28_b, 1),
      'and the inversion the paper reported has narrowed')
check(r33_h > r28_h, 'it has NOT reversed: rung 33 still leads rung 28')

# ---------------------------------------------------------------------------
head(3, 'WHAT THE DRIFT IS MADE OF')
print('  A file count counts every file that says the word, including index pages,')
print('  the audit log, and the ruler itself. The composition matters more than the')
print('  total, so here it is.\n')
n_k, set_k = count(['k-theory'], SECOND)
def kind_of(f):
    if 'wp82' in f:                                    return 'the ruler itself'
    if f == 'CLAUDE.md':                               return 'project scaffolding'
    if (f.endswith('index.html') or f.startswith('index-')
            or f.startswith('master-index')):          return 'index / listing'
    if f.startswith('docs/'):                          return 'audit narrative'
    return 'CHAPTER'
for f in sorted(set_k):
    print('     %-46s %s' % (f, kind_of(f)))
chapters = [f for f in set_k if kind_of(f) == 'CHAPTER']
print()
check(n_k == 9, 'k-theory is in %d files at %s' % (n_k, SECOND), str(n_k))
check(len(chapters) == 2,
      'exactly %d of them are chapters -- the rest are listings, the log, CLAUDE.md '
      'and this paper' % len(chapters), str(sorted(chapters)))
print('     So the floor is STARTED, not built: %d chapters (%s)'
      % (len(chapters), ', '.join(sorted(chapters))))
print('     plus the echoes a new chapter produces in navigation. Reporting 0 -> 9')
print('     without this breakdown would overstate it by a factor of four and a half.')
print()
print('     CLAUDE.md is separated out here because it is not a chapter and not a')
print('     listing: it is scaffolding that names the vocabulary in a handoff note.')
print('     The earlier version of this block had no bucket for it and counted it')
print('     as a chapter, which is the same one-look failure the paper is about.')

# ---------------------------------------------------------------------------
head(4, "THE TWO VOLUME CLAIMS IN §3")
page = open(os.path.join(REPO, 'book6', 'wp82-the-missing-floor.html'),
            encoding='utf-8').read()
# strip tags before matching: a phrase in this page can be split by an <em>,
# and a needle that straddles one silently misses. That is the same one-look
# failure the rest of this script is about.
import re as _re
flat = ' '.join(_re.sub(r'<[^>]+>', ' ', page).split())
check('Zero files use the vocabulary' in flat,
      'the XIII entry still carries its 2026-08-29 reading verbatim')
n30, set30 = count(['∞-categor', 'infinity-categor'], 'HEAD')
print('     rung-30 vocabulary at HEAD: %d files' % n30)
for f in sorted(set30): print('       %s' % f)
check(n30 > 0, 'which is no longer zero, so the entry needs its date carried')
check(any(f.startswith('book13/') for f in set30),
      'and Volume XIII on disk is where the vocabulary now is')
print()
print('     §3 also flags its own limits, and both still stand as written:')
for phrase, what in (
        ('is an ordering chosen here', 'XIII-XV placement is declared ASSUME, not derived'),
        ('no title appears anywhere in the repository', 'Volume X is declared OPEN')):
    check(phrase in flat, what, phrase)

# ---------------------------------------------------------------------------
head(5, 'CONTROL: THIS SCRIPT COMPUTED SOMETHING')
check(len(files('moonshine', 'HEAD')) > 0, 'git grep returned files rather than nothing')
# assembled, not written down: a literal control token matches itself once the
# script is committed, and the one this file used is also in
# book7/ch-van-der-pol-verify.py, so a grep for it returns files.
ABSENT = 'qqx' + '-no-file-contains-this-' + 'qqx'
check(files(ABSENT, 'HEAD') == set(), 'and returns none for a token no file contains',
      str(files(ABSENT, 'HEAD')))
check(len(ROWS) == 12 and len(base_n) == 12, 'all twelve rows were measured at both refs')
print('    A vacuous pass is a pass. Block [5] exists so that block [1] cannot')
print('    report a perfect reproduction by having matched nothing against nothing.')

# ---------------------------------------------------------------------------
head('HONESTY', 'What this establishes, and what it does not.')
print("""
  ESTABLISHED. WP-82's rung table reproduces exactly -- twelve of twelve -- when
  its own stated method is re-run at the commit it names. The paper was right on
  the day, and its rung-30 zero was right too. Re-run at HEAD, every row has
  risen: rung 28 from 2 file-mentions to %d, rung 33 from %d to %d, and the
  inversion the paper reported has narrowed from %.1f:1 to %.1f:1 without
  reversing. Of the %d files that say "k-theory" at %s, %d are chapters.

  NOT ESTABLISHED. That the floor is built. A file count measures vocabulary,
  not content -- it was the right instrument for the paper's question, which was
  whether the words appear at all, and it is the wrong instrument for "is there
  a theorem here". Nothing in this script reads a proof. Nor does it revisit the
  paper's argument: the reading of the ruler, the choice to treat rung order as
  construction order, and the six proposed volumes are untouched.

  AND THE REASON THIS FILE EXISTS AT ALL. A dated measurement with no tool
  behind it can only be re-derived by hand, and on 2026-09-15 a hand reading of
  the rung-30 row as a live count produced a wrong conclusion about Volume XIII.
  The row was not wrong. The reading was, and re-running the measurement is what
  would have caught it in one command.
""" % (r28_h, r33_b, r33_h, r33_b / max(r28_b, 1), r33_h / max(r28_h, 1),
       n_k, SECOND, len(chapters)))

print('=' * 70)
if fails:
    print('  %d CHECK(S) FAILED' % len(fails))
    for f in fails: print('    - ' + f)
    print('=' * 70); sys.exit(1)
print('  ALL CHECKS PASSED')
print('=' * 70)
