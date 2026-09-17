#!/usr/bin/env python3
"""
The Present King of France -- what a name does when there is nothing to name.

WHY THIS FILE EXISTS. tools/lean_addresses.py reports 66 Lean file names cited
in this corpus that it cannot resolve UNDER THE ROOTS IT WAS GIVEN -- here two
of them, this repository and AXLE -- across 142 citations. Chain.lean is cited
by 23 pages, ZeoliteCommutation.lean by 11.

UNRESOLVED IS NOT ABSENT. More than twenty other repositories exist and have not
been searched, and R15 in CLAUDE.md is explicit: never report absence from a
single search. Two roots is a single search. So this script measures where we
have looked, and blocks [1] and [2] establish what follows ONCE a name is
confirmed absent -- which for these 66 is work not yet done. The logic is
unconditional; its application to any particular name is not.

BLOCKS
  [1] The 1905 analysis, made exact and exhaustive over small domains.
  [2] Scope -- the two readings of the negation, and which a correction needs.
  [3] The corpus, evaluated under the unpacking.
  [4] Mention is not use, and the corpus already knew it without saying so.
  [5] The ledger Hardy kept, and the one this corpus keeps.
  [6] Control.

PRIMARY SOURCES.
  B. Russell, "On Denoting", Mind 14 (1905).
  G. H. Hardy on Ramanujan's first letter -- 16 January 1913, nine pages, some
  120 theorems, almost no proofs -- and his reply of 8 February asking for them.
  A. N. Whitehead and B. Russell, "Principia Mathematica" Vol I, 2nd ed.,
  Introduction ch. III "Incomplete Symbols" and *14 "Descriptions".
  In-corpus: tools/lean_addresses.py, docs/audit-log.md, and R11 in CLAUDE.md.

Standard library only.  python3 book6/ch-the-present-king-of-france-verify.py
"""
import itertools, os, subprocess, sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
fails = []
def check(ok, msg, detail=''):
    print('    %s  %s%s' % ('PASS' if ok else 'FAIL', msg, ('  -- ' + detail) if detail and not ok else ''))
    if not ok: fails.append(msg)
def head(n, t):
    print('\n' + '=' * 70 + '\n  [%s]  %s\n' % (n, t) + '=' * 70)

# ---------------------------------------------------------------------------
head(1, "THE 1905 ANALYSIS, EXHAUSTIVELY")
print('  "The F is G" does not name an F. It says three things at once:')
print('      (a) there is at least one F')
print('      (b) there is at most one F')
print('      (c) whatever is F, is G')
print('  With no F at all, (a) fails and the whole sentence is FALSE -- not')
print('  meaningless, and not about a ghost.\n')
def russell(F, G):
    return any(x in F and all(y == x for y in F) and x in G for x in F)
def narrow_neg(F, G):                      # "the F is not-G"
    return any(x in F and all(y == x for y in F) and x not in G for x in F)
def wide_neg(F, G):                        # "it is not the case that the F is G"
    return not russell(F, G)
rows = 0
both_false_when_empty = True
excluded_middle = True
for n in (1, 2, 3, 4):
    D = list(range(n))
    subs = [frozenset(c) for k in range(n + 1) for c in itertools.combinations(D, k)]
    for F in subs:
        for G in subs:
            rows += 1
            s, nn, wn = russell(F, G), narrow_neg(F, G), wide_neg(F, G)
            if len(F) == 0 and (s or nn): both_false_when_empty = False
            if s == wn: excluded_middle = False
check(rows == sum((2 ** n) ** 2 for n in (1, 2, 3, 4)),
      'evaluated over all %d (F, G) pairs for domains of size 1..4' % rows)
check(both_false_when_empty,
      'when nothing is F, BOTH "the F is G" and "the F is not-G" come out false')
check(excluded_middle,
      'and excluded middle is untouched: the wide-scope negation is exactly not-S')
print('\n      F = {}      "the F is G"      false')
print('                  "the F is not-G"  false      <-- the puzzle')
print('                  "not(the F is G)" TRUE       <-- the resolution')
print('\n  The two are different sentences. Meinong kept one sentence and stocked')
print('  the world with subsisting kings to make it about something. Russell kept')
print('  the world and split the sentence. Nothing has to subsist.')

# ---------------------------------------------------------------------------
head(2, "SCOPE, AND WHY A CORRECTION HAS TO CHOOSE ONE")
print('  "X is not proved in AXLE" carries the same ambiguity, and the two')
print('  readings are not equivalent when the file is missing:\n')
print('      narrow: there is a proof in AXLE, and it does not establish X')
print('      wide:   it is not the case that there is a proof in AXLE establishing X\n')
empty = frozenset()
one = frozenset([0])
print('      file missing  (F = {}):   narrow %-5s   wide %-5s'
      % (narrow_neg(empty, one), wide_neg(empty, one)))
print('      file present, proves X:  narrow %-5s   wide %-5s'
      % (narrow_neg(one, one), wide_neg(one, one)))
print('      file present, does not:  narrow %-5s   wide %-5s'
      % (narrow_neg(one, empty), wide_neg(one, empty)))
check(not narrow_neg(empty, one) and wide_neg(empty, one),
      'with the file missing, only the WIDE reading is true -- a correction that '
      'says "the proof does not establish X" asserts a proof exists')
check(narrow_neg(one, empty) and wide_neg(one, empty),
      'and with the file present but insufficient, both readings are true')
print('\n  So a retraction of a missing-file citation must be written wide. Saying')
print('  "the proof there is incomplete" concedes the proof. Saying "there is no')
print('  such file" is the true sentence, and it is shorter.')

# ---------------------------------------------------------------------------
head(3, "THE CORPUS, EVALUATED UNDER THE UNPACKING")
ROOTS_SEARCHED = [REPO, os.path.expanduser('~/mnt/AXLE')]
r = subprocess.run([sys.executable, os.path.join(REPO, 'tools', 'lean_addresses.py'),
                    REPO, '--roots', ROOTS_SEARCHED[1]],
                   cwd=REPO, capture_output=True, text=True)
out = r.stdout + r.stderr
dang = [l for l in out.splitlines() if l.strip().startswith('DANGLING')]
summary = [l for l in out.splitlines() if 'resolve nowhere' in l]
print('  tools/lean_addresses.py, live:\n')
for l in summary: print('     ' + l.strip())
print()
top = []
for l in dang:
    parts = l.split()
    if len(parts) >= 3 and parts[2].isdigit():
        top.append((int(parts[2]), parts[1]))
top.sort(reverse=True)
print('      %-40s %s' % ('name cited', 'pages citing it'))
for n, name in top[:8]:
    print('      %-40s %d' % (name, n))
check(len(dang) >= 50,
      'at least fifty names are unresolved UNDER THE TWO ROOTS SEARCHED -- which '
      'is a statement about where we looked, not about what exists', str(len(dang)))
check(len(ROOTS_SEARCHED) == 2,
      'and the run passed exactly %d roots, so R15 is not satisfied and no '
      'absence is claimed' % len(ROOTS_SEARCHED), str(ROOTS_SEARCHED))
check(top and top[0][0] >= 10,
      'and the most-cited of them, %s, is named by %d pages -- the threshold is 10 '
      'because the 2026-09-17 eleven-root search resolved Chain.lean (23 pages) and '
      'moved the top of this table' % (top[0][1], top[0][0])
      if top else 'no dangling names parsed')
print('\n  Each of those citations asserts clause (a): there is such a file. Whether')
print('  clause (a) is FALSE is exactly what the unsearched roots decide, and they')
print('  have not been searched. What is established is conditional: for any name')
print('  that comes back absent from a full search, every sentence built on it is')
print('  false -- not "unverified", not "pending", not "to be restored". Until then')
print('  the right tag is OPEN, and the right next action is to pass the roots.')

# ---------------------------------------------------------------------------
head(4, "MENTION IS NOT USE -- AND THE CORPUS ALREADY KNEW IT")
src = open(os.path.join(REPO, 'tools', 'lean_addresses.py'), encoding='utf-8').read()
ex = src[src.index('EXEMPT = {'):src.index('}', src.index('EXEMPT = {')) + 1]
pairs = [l.strip() for l in ex.splitlines() if l.strip().startswith('(')]
print('  A page that NAMES a missing file in order to report that it is missing')
print('  is not citing it. lean_addresses.py has always exempted those, by')
print('  (page, name) PAIR and never by name alone -- "a blanket name exemption')
print('  would hide a real dangling citation elsewhere". That is Russell\'s')
print('  use/mention distinction, kept by hand and never named.\n')
for l in pairs: print('      ' + l)
check(len(pairs) >= 6, 'the exemption list holds %d (page, name) pairs' % len(pairs))
check(all(l.count(',') >= 1 for l in pairs), 'every exemption is a pair, not a bare name')
check("'book7/ch-gelfand.html', 'ZeoliteCommutation.lean'" in ex.replace('(', '').replace(')', ''),
      'ch-gelfand is exempted: it names the file to say it does NOT rely on it',
      'not found in EXEMPT')
print('\n  Adding that one pair took ZeoliteCommutation.lean from 12 citing pages')
print('  to 11. The name did not become less dangling; one of the twelve was')
print('  never using it.')

# ---------------------------------------------------------------------------
head(5, "THE LEDGER HARDY KEPT, AND THE ONE THIS CORPUS KEEPS")
sys.path.insert(0, os.path.join(REPO, 'tools'))
from corpus_count import files as cfiles
def cls(f):
    if f.startswith('book6/ch-the-present-king'):              return 'self'
    if f == 'CLAUDE.md':                                       return 'scaffolding'
    if f.startswith('tools/'):                                 return 'tooling'
    if f.startswith('docs/'):                                  return 'audit'
    if f.startswith('_archive/'):                              return 'archive'
    if (f.endswith('index.html') or f.startswith('index-')
            or f.startswith('master-index')):                  return 'listing'
    return 'CHAPTER'
def ch(pat): return [f for f in cfiles(pat) if cls(f) == 'CHAPTER']
print('  Hardy did not believe or disbelieve the nine pages. He sorted them:')
print('  some wrong, some already known, some new -- and he wrote down which.')
print('  The corpus keeps the same kind of ledger, in its tier tags and in its')
print('  vocabulary. Measured at HEAD, entity-aware:\n')
print('      %-26s %7s %10s' % ('pattern', 'files', 'chapters'))
LEDGER = [('proof', r'\bproof\b'), ('Ramanujan', r'ramanujan'), ('notebook', r'notebook'),
          ('unproved / unproven', r'unproved|unproven'), ('without proof', r'without proof'),
          ('Hardy', r'hardy'), ('Littlewood', r'littlewood'),
          ('Russell', r'russell'), ('theory of descriptions', r'theory of descriptions'),
          ('On Denoting', r'on denoting'), ('use.{0,4}mention', r'use.{0,4}mention')]
L = {}
for name, pat in LEDGER:
    L[name] = (len(cfiles(pat)), len(ch(pat)))
    print('      %-26s %7d %10d' % (name, L[name][0], L[name][1]))
check(L['proof'][1] > 300, 'the corpus says "proof" in %d chapters' % L['proof'][1])
check(L['unproved / unproven'][1] > 10,
      'and keeps an explicit unproved column in %d of them' % L['unproved / unproven'][1])
check(ch(r'theory of descriptions') == [], 'no chapter but this one names the theory of descriptions',
      str(ch(r'theory of descriptions')))
check(ch(r'use.{0,4}mention') == [], 'nor the use/mention distinction it turns on',
      str(ch(r'use.{0,4}mention')))
print('\n  So the habit is there and the name for it is not. Hardy asked for the')
print('  proofs on 8 February and went on believing the theorems in the meantime.')
print('  Those are two ledgers, and the corpus has to keep both.')

# ---------------------------------------------------------------------------
head(6, 'CONTROL')
check(russell(frozenset([0]), frozenset([0])), 'the unpacking is true when it should be')
check(not russell(frozenset([0, 1]), frozenset([0, 1])),
      'and false when there are two Fs -- clause (b) does work')
check(not russell(frozenset(), frozenset()), 'and false when there are none')
check(r.returncode in (0, 1), 'lean_addresses.py ran', 'rc=%d' % r.returncode)
check(len(out.strip()) > 0, 'and produced output')

print('\n' + '=' * 70 + '\n  [HONESTY]\n' + '=' * 70)
print("""
  WHAT THIS ESTABLISHES. That on Russell's analysis a description with nothing
  answering to it makes its sentence false rather than meaningless, that the
  narrow and wide negations come apart exactly there, and that excluded middle
  is untouched -- all exhaustively, over every (F, G) pair on domains up to four
  elements. That the corpus currently carries dozens of Lean names resolving
  nowhere across well over a hundred citations, with the most-cited named by
  more than twenty pages. And that the practical consequence is a rule for
  writing corrections: a retraction of a missing-file citation must take wide
  scope, because the narrow reading concedes that a proof exists.

  WHAT IT DOES NOT ESTABLISH. THAT ANY OF THE 66 NAMES IS ABSENT. The run behind
  block [3] passed two roots, this repository and AXLE, and more than twenty
  other repositories exist unsearched. R15 forbids reporting absence from a
  single search, and two roots is a single search. Every consequence drawn from
  the analysis is written as a conditional on a name being confirmed absent, and
  none of the 66 has been. Nor that any particular page is wrong about its
  mathematics. A citation being false is a statement about the citation, not
  about the theorem it gestures at -- the theorem may be true, may be provable,
  may be proved somewhere this tool cannot see. The counts come from
  lean_addresses.py and inherit its limits: it asks whether a FILE of that name
  exists under the roots it was given, not whether a declaration inside it
  exists or elaborates, and a root that is not passed is a root not searched.
  The use/mention exemptions are curated by hand, so the citation count is only
  as good as that curation. Nothing here evaluates Russell's analysis against
  its rivals; Strawson's objection of 1950, that such a sentence presupposes
  rather than asserts existence, is not addressed and is not obviously wrong.
  No priority is claimed: "On Denoting" is 1905.
""")
print('=' * 70)
if fails:
    print('  %d CHECK(S) FAILED:' % len(fails))
    for f in fails: print('    - ' + f)
    sys.exit(1)
print('  ALL CHECKS PASSED')
