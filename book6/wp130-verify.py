#!/usr/bin/env python3
"""
WP-130 -- rung thirty-two, re-measured, and checked against its own stated method.

WHY THIS FILE EXISTS. WP-130's tables are a DATED measurement: tracked *.html
and *.md files containing at least one case-insensitive match, at commit
6b7918b on 2026-10-01. WP-82 established why that needs a checker -- a dated
measurement does not decay into an error, it decays into a measurement about a
day that has passed, and on 2026-09-15 a reading of one of its rows as a live
count produced a wrong conclusion about Volume XIII.

WP-130 adds a second thing to check, and it is the paper's actual finding: the
TOTAL for a rung is not the quantity of interest. Nine files carry the word
Langlands and seven of them are index pages, inventories, or WP-82 itself.
Block [2] pins the composition, not just the count, because the composition is
the argument.

WHAT IT CHECKS.
  [1] The §1 pattern table reproduces at 6b7918b, the commit the paper names.
  [2] The §2 composition table reproduces: every file behind the 9, and its
      kind. This is the block that fails if the finding stops being true.
  [3] The zero rows, twice: pinned at 6b7918b for reproducibility, and read
      again at HEAD, live. The first draft of this file asserted them only at
      the commit and said in the same breath that writing the slate would turn
      them red. It would not have -- a value pinned to a historical commit
      never moves, so that green would have meant nothing, which is the exact
      defect WP-82 recorded in a vacuity scan whose anchor could never match.
      The HEAD reading is the one that moves.
  [4] The two control rows, in opposite directions: k-theory 8 -> 25 and
      w-algebra 0 -> 7. WP-82 named rung 28 as the missing floor and chose the
      W-algebra route as rung 32's reachable bridge; both were built. If these
      do not hold, the instrument is not measuring construction and nothing
      else here means anything.
  [5] Anchor control. WP-82 recorded a vacuity scan whose grep anchor could
      never match, so its green meant nothing. A pattern that must match and a
      pattern that must not, so a silently-broken search is caught.
  [6] Stratification. The ruler is inside the set it measures. At 6b7918b this
      paper is not in the tree at all, so excluding it changes nothing there --
      which is how the exclusion is known to be the right one rather than a
      convenient one. At HEAD, once committed, it must be excluded or every
      row it prints carries a spurious +1.

Standard library only, but it shells out to git: the corpus is tracked files,
not the working tree.

    python3 book6/wp130-verify.py
"""
import subprocess, sys, os

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
COMMIT = '6b7918b'
RULER = 'book6/wp130-rung-thirtytwo.html'
fails = []

def check(ok, msg, detail=''):
    print('    %s  %s%s' % ('PASS' if ok else 'FAIL', msg,
                            ('  -- ' + detail) if detail and not ok else ''))
    if not ok:
        fails.append(msg)

def head(n, t):
    print('\n' + '=' * 70 + '\n  [%s]  %s\n' % (n, t) + '=' * 70)

def matches(pattern, ref, keep_ruler=False):
    """WP-82's method: tracked *.html and *.md, case-insensitive, by file.

    Returns the sorted list of paths. `git grep` against a ref prints
    'ref:path', so the prefix is stripped. The ruler is excluded unless asked
    for -- see block [6].
    """
    r = subprocess.run(
        ['git', '--no-optional-locks', 'grep', '-il', '--', pattern, ref,
         '--', '*.html', '*.md'],
        cwd=REPO, capture_output=True, text=True)
    out = []
    for line in r.stdout.strip().split('\n'):
        if not line:
            continue
        path = line.split(':', 1)[1] if ':' in line else line
        if path == RULER and not keep_ruler:
            continue
        out.append(path)
    return sorted(set(out))

def n(pattern, ref=COMMIT, keep_ruler=False):
    return len(matches(pattern, ref, keep_ruler))

# ---------------------------------------------------------------- [1]
head(1, 'The §1 pattern table reproduces at %s' % COMMIT)
TABLE = [
    ('langlands', 9), ('motivic', 11), ('automorphic', 5), ('reciprocity', 4),
    ('galois representation', 2), ('shimura', 2), ('gaitsgory', 1),
    ('drinfeld', 0), ('beilinson', 0), ('harish-chandra', 0),
    ('lafforgue', 0), ('raskin', 0), ('fundamental lemma', 0),
    ('w-algebra', 7), ('vertex algebra', 10), ('frenkel', 9),
    ('k-theory', 25), ('connes', 36),
]
for pat, want in TABLE:
    got = n(pat)
    check(got == want, '%-24s = %d' % (pat, want), 'got %d' % got)

# ---------------------------------------------------------------- [2]
head(2, 'The §2 composition table -- what KIND of file each of the 9 is')
COMPOSITION = {
    'book32/index.html': 'INDEX',
    'book7/index.html': 'INDEX',
    'series-hub.html': 'INDEX',
    'docs/audit-log.md': 'INVENTORY',
    'docs/corpus-inventory.md': 'INVENTORY',
    'docs/part-ii-source-wants.md': 'INVENTORY',
    'book6/wp82-the-missing-floor.html': 'RULER',
    'book4/ch14.html': 'CONTENT',
    'book7/ch-feigin.html': 'CONTENT',
}
found = matches('langlands', COMMIT)
check(found == sorted(COMPOSITION), 'the 9 files are exactly as §2 lists them',
      'got %s' % found)
content = [f for f, k in COMPOSITION.items() if k == 'CONTENT']
check(len(content) == 2, 'exactly 2 of the 9 are CONTENT')
check(len(COMPOSITION) - len(content) == 7,
      '7 of the 9 are index, inventory or the ruler -- the finding')
# the single gaitsgory mention is in a wants-list, not a chapter
g = matches('gaitsgory', COMMIT)
check(g == ['docs/part-ii-source-wants.md'],
      'the one gaitsgory mention is a wants-list', 'got %s' % g)

# ---------------------------------------------------------------- [3]
head(3, 'The zero rows -- pinned at the commit, and read live at HEAD')
ZEROS = ('drinfeld', 'beilinson', 'harish-chandra', 'lafforgue',
         'raskin', 'fundamental lemma')
print('  at %s (reproducibility -- these must not move):' % COMMIT)
for pat in ZEROS:
    got = n(pat)
    check(got == 0, '%-20s was 0 at the commit' % pat, 'now reads %d' % got)
print('\n  at HEAD (live -- this is the one that moves):')
closed = []
for pat in ZEROS:
    got = n(pat, 'HEAD')
    if got == 0:
        print('    OPEN  %-20s still absent' % pat)
    else:
        closed.append((pat, got))
        print('    BUILT %-20s now in %d file(s)' % (pat, got))
if closed:
    print('\n    %d of %d closed since %s. When all six are built, retire this'
          % (len(closed), len(ZEROS), COMMIT))
    print('    block and re-measure: the paper it checks will be describing a')
    print('    corpus that no longer exists.')
else:
    print('\n    None closed yet. This block is how the corpus notices when they are.')

# ---------------------------------------------------------------- [4]
head(4, 'Controls -- the two rungs WP-82 named, both since built')
check(n('k-theory') == 25, 'k-theory = 25 (WP-82 measured 8)')
check(n('w-algebra') == 7, 'w-algebra = 7 (WP-82 correction measured 0)')
wp82 = os.path.join(REPO, 'book6/wp82-the-missing-floor.html')
src = open(wp82, encoding='utf-8', errors='ignore').read() if os.path.exists(wp82) else ''
check('0 using &ldquo;W-algebra&rdquo;' in src or '0 using "W-algebra"' in src
      or 'W-algebra' in src,
      'WP-82 is present and names the W-algebra route')
print('\n    If these two fail, the instrument is not measuring construction,')
print('    and no other row in this file means anything.')

# ---------------------------------------------------------------- [5]
head(5, 'Anchor control -- a broken search must not read as a clean result')
check(n('connes') > 0, 'a pattern that must match, matches')
check(n('zzzz-no-such-pattern-zzzz') == 0, 'a pattern that must not match, does not')
check(n('langlands') != n('zzzz-no-such-pattern-zzzz'),
      'the two are distinguishable')

# ---------------------------------------------------------------- [6]
head(6, 'Stratification -- the ruler is inside the set it measures')
at_commit_with = n('langlands', COMMIT, keep_ruler=True)
at_commit_without = n('langlands', COMMIT, keep_ruler=False)
check(at_commit_with == at_commit_without,
      'at %s the ruler is not in the tree, so excluding it changes nothing'
      % COMMIT,
      '%d vs %d' % (at_commit_with, at_commit_without))
head_with = n('langlands', 'HEAD', keep_ruler=True)
head_without = n('langlands', 'HEAD', keep_ruler=False)
if head_with == head_without:
    print('    NOTE  the ruler is not yet committed, so HEAD and %s agree.' % COMMIT)
    print('          Once it is, this block asserts the +1 it would otherwise add.')
else:
    check(head_with - head_without == 1,
          'at HEAD the ruler adds exactly +1, and is excluded',
          '%d vs %d' % (head_with, head_without))

# ----------------------------------------------------------------
print('\n' + '=' * 70)
if fails:
    print('  %d FAILED' % len(fails))
    for f in fails:
        print('    - %s' % f)
    sys.exit(1)
print('  all checks pass')
print('=' * 70)
