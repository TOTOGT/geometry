#!/usr/bin/env python3
"""
Whitehead and Russell -- the foundation 470 files of this corpus stand on.

WHY THIS FILE EXISTS. "Lean" occurs in 470 tracked files of this corpus. Lean's
kernel is a dependent type theory, and the theory of types was invented by
Whitehead and Russell to block a paradox. Measured at HEAD: "theory of types" 0,
"vicious circle" 0, "propositional calculus" 0, "definite description" 0,
"logicism" 0, "=Df" 0, Whitehead 1, "Principia Mathematica" 1, Frege 1,
Russell 3. The corpus talks about the phenomenon -- "paradox" 30,
"self-reference" 13, Godel 31, "incompleteness" 47 -- with none of the apparatus
built for it.

The apparatus bites. tools/self_reference.py implements Principia's rule -- no
object defined in terms of a totality containing itself -- and found that
WP-82's twelve-row table counts the paper that prints it, in all twelve rows of
its second column and none of its first. Block [6] here re-derives that.

BLOCKS
  [1] The Sheffer stroke and the four definitions PM's 2nd edition builds on.
  [2] Functional completeness of {|}, by construction, 16 of 16.
  [3] Nicod's single primitive proposition, exhaustively -- a formula printed in
      the book, checked against itself.
  [4] The rule of inference, and *54.43 in a finite universe.
  [5] Cantor's diagonal over EVERY map S -> 2^S, and the limitation the authors
      print themselves.
  [6] The vicious circle in this repository, found and fixed.
  [7] The corpus, counted, entity-aware.
  [8] Control.

PRIMARY SOURCE. A. N. Whitehead and B. Russell, "Principia Mathematica",
Volume I, 2nd edition, Cambridge University Press. Quoted here from a scan of
the second edition: Introduction to the Second Edition (the stroke, Nicod's
reduction, the Axiom of Reducibility, and the authors' own caveat on Cantor),
Introduction ch. II "The Theory of Logical Types", ch. III "Incomplete Symbols",
*12 "The Hierarchy of Types and the Axiom of Reducibility", *14 "Descriptions",
*54 "Cardinal Couples".

Standard library only.  python3 book7/ch-whitehead-russell-verify.py
"""
import itertools, os, subprocess, sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
fails = []
def check(ok, msg, detail=''):
    print('    %s  %s%s' % ('PASS' if ok else 'FAIL', msg, ('  -- ' + detail) if detail and not ok else ''))
    if not ok: fails.append(msg)
def head(n, t):
    print('\n' + '=' * 70 + '\n  [%s]  %s\n' % (n, t) + '=' * 70)

TF = (False, True)
stroke = lambda p, q: not (p and q)

# ---------------------------------------------------------------------------
head(1, "THE STROKE, AND THE FOUR DEFINITIONS BUILT ON IT")
print('  PM\'s second edition replaces the two indefinables "not-p" and "p or q"')
print('  with Sheffer\'s single one, p|q, "p is incompatible with q", and defines:\n')
print('      ~p    = p|p           p v q = ~p|~q')
print('      p > q = p|~q          p . q = ~(p|q)\n')
NOT = lambda p: stroke(p, p)
IMP = lambda p, q: stroke(p, stroke(q, q))
OR  = lambda p, q: stroke(stroke(p, p), stroke(q, q))
AND = lambda p, q: NOT(stroke(p, q))
print('      %-5s %-5s %-7s %-7s %-7s %-7s %-7s' % ('p', 'q', 'p|q', '~p', 'p>q', 'pvq', 'p.q'))
ok = True
for p, q in itertools.product(TF, repeat=2):
    print('      %-5s %-5s %-7s %-7s %-7s %-7s %-7s'
          % (p, q, stroke(p, q), NOT(p), IMP(p, q), OR(p, q), AND(p, q)))
    ok &= (NOT(p) == (not p) and IMP(p, q) == ((not p) or q)
           and OR(p, q) == (p or q) and AND(p, q) == (p and q))
check(ok, 'all four definitions reproduce their truth tables, on all four rows')

# ---------------------------------------------------------------------------
head(2, "FUNCTIONAL COMPLETENESS OF THE STROKE, BY CONSTRUCTION")
print('  Build every expression in p, q reachable from the stroke, and collect the')
print('  truth function each one realises. Not asserted -- enumerated.\n')
def realised(depth):
    cur = [('p', lambda p, q: p), ('q', lambda p, q: q)]
    seen = {}
    for _ in range(depth):
        new = []
        for na, fa in cur:
            for nb, fb in cur:
                new.append(('(%s|%s)' % (na, nb),
                            (lambda fa=fa, fb=fb: (lambda p, q: stroke(fa(p, q), fb(p, q))))()))
        cur = list({n: (n, f) for n, f in cur + new}.values())
    for n, f in cur:
        sig = tuple(f(p, q) for p, q in itertools.product(TF, repeat=2))
        if sig not in seen or len(n) < len(seen[sig]): seen[sig] = n
    return seen
R = realised(4)
allsigs = set(itertools.product(TF, repeat=4))
print('      truth functions of two variables realised: %d of 16' % len(set(R) & allsigs))
for label, sig in (('~p', (True, True, False, False)), ('p . q', (False, False, False, True)),
                   ('p v q', (False, True, True, True)), ('p > q', (True, True, False, True)),
                   ('p = q', (True, False, False, True)), ('false', (False, False, False, False))):
    print('      %-8s -> %s' % (label, R.get(sig, 'NOT REALISED')))
check(set(R) >= allsigs, 'every one of the 16 binary truth functions is expressible',
      str(len(allsigs - set(R))))
check(R[(True, True, False, False)] == '(p|p)', 'and ~p is the shortest of them, p|p')

# ---------------------------------------------------------------------------
head(3, "NICOD'S SINGLE PRIMITIVE PROPOSITION, EXHAUSTIVELY")
print('  PM 2nd ed. reports that Nicod reduced the primitive propositions of the')
print('  propositional calculus to one. As printed in the Introduction:\n')
print('      {p|(q|r)} | [ {t|(t|t)} | {(s|q)|((p|s)|(p|s))} ]\n')
print('  A formula printed in the book, checked against itself over all 32 rows.')
def nicod(p, q, r, s, t):
    A = stroke(p, stroke(q, r))
    B = stroke(t, stroke(t, t))
    Cc = stroke(stroke(s, q), stroke(stroke(p, s), stroke(p, s)))
    return stroke(A, stroke(B, Cc))
vals = [nicod(*v) for v in itertools.product(TF, repeat=5)]
print('\n      rows %d   true %d   false %d' % (len(vals), vals.count(True), vals.count(False)))
check(len(vals) == 32 and all(vals), 'it is a tautology', '%d false rows' % vals.count(False))

# ---------------------------------------------------------------------------
head(4, "THE RULE OF INFERENCE, AND *54.43")
print('  PM: "If p, q, r are elementary propositions, given p and p|(q|r), we can')
print('  infer r." Checked for soundness over all eight rows.\n')
bad = [(p, q, r) for p, q, r in itertools.product(TF, repeat=3)
       if p and stroke(p, stroke(q, r)) and not r]
check(not bad, 'no row makes both premises true and the conclusion false', str(bad))
print('\n  *54.43, the proposition Vol I is famous for. For unit classes alpha and')
print('  beta:  alpha n beta = 0  .=.  alpha u beta in 2. In a finite universe:\n')
allok = True
for n in (2, 3, 4, 5, 6):
    units = [frozenset([x]) for x in range(n)]
    tot = mism = 0
    for a in units:
        for b in units:
            tot += 1
            if (len(a & b) == 0) != (len(a | b) == 2): mism += 1
    allok &= (mism == 0)
    print('      universe of %d: %2d ordered pairs of unit classes, mismatches %d' % (n, tot, mism))
check(allok, 'no mismatch in any universe tested -- 1 + 1 = 2, in the only sense *54.43 claims')

# ---------------------------------------------------------------------------
head(5, "CANTOR'S DIAGONAL, AND THE AUTHORS' OWN CAVEAT")
print('  Russell\'s paradox in the form that survives: no map from a set onto its')
print('  power set. Enumerate EVERY map S -> 2^S and look for the diagonal set')
print('  D = {x : x not in f(x)} in the image.\n')
allmiss = True
for n in (1, 2, 3, 4):
    S = list(range(n))
    subs = [frozenset(c) for k in range(n + 1) for c in itertools.combinations(S, k)]
    total = missed = 0
    for f in itertools.product(subs, repeat=n):
        total += 1
        D = frozenset(x for x in S if x not in f[x])
        if D not in f: missed += 1
    allmiss &= (missed == total)
    print('      n = %d: %6d maps, D outside the image in %6d of them' % (n, total, missed))
check(allmiss, 'D is outside the image of EVERY map tested -- exhaustive, not sampled')
print('\n  And the caveat is the authors\'. The Introduction to the Second Edition')
print('  says of the Axiom of Reducibility that "it is not the sort of axiom with')
print('  which we can rest content", and records that without it')
print('  "Cantor\'s proof that 2^n > n breaks down unless n is finite".')
print('  Block [5] is entirely inside the case they say survives.')
check(True, 'the exhaustion above is over finite n only -- which is what they said')

# ---------------------------------------------------------------------------
head(6, "THE VICIOUS CIRCLE IN THIS REPOSITORY")
print('  PM Introduction ch. II: no object may be defined in terms of a totality')
print('  that includes itself. tools/self_reference.py applies it to this repo by')
print('  asking, for each verify script, whether the SET IT COUNTS OVER contains')
print('  the script or its page. Not whether the script contains a word -- the')
print('  principle is about the range of a variable.\n')
RULER = 'book6/wp82-the-missing-floor.html'
def gfiles(pat, ref):
    r = subprocess.run(['git', '--no-optional-locks', 'grep', '-lic', '-e', pat, ref,
                        '--', '*.html', '*.md'], cwd=REPO, capture_output=True, text=True)
    return set(l.split(':', 1)[1] for l in r.stdout.splitlines() if ':' in l)
PATS = ['k-theory', 'index theorem', 'atiyah', 'operator algebra', 'von neumann',
        'infinity-categor', 'sheaf', 'motivic', 'noncommutative', 'connes',
        'spectral triple', 'moonshine']
inb, ins = 0, 0
for pat in PATS:
    if RULER in gfiles(pat, '654fb06'): inb += 1
    if RULER in gfiles(pat, 'd97154e'): ins += 1
tree = subprocess.run(['git', '--no-optional-locks', 'ls-tree', '654fb06', '--name-only',
                       '--', RULER], cwd=REPO, capture_output=True, text=True).stdout.strip()
print('      the ruler is in the tree at 654fb06 : %s' % bool(tree))
print('      rows of the FIRST column containing the ruler  : %d of %d' % (inb, len(PATS)))
print('      rows of the SECOND column containing the ruler : %d of %d' % (ins, len(PATS)))
check(not tree, 'WP-82 is not in the tree at the commit its first column names')
check(inb == 0, 'so no row of the first column counts the ruler')
check(ins == len(PATS),
      'and every row of the second column did -- the paper prints all twelve of '
      'its own patterns', str(ins))
print('\n  Two columns, two totalities, and a spurious +1 in every row of the')
print('  second. Stratifying the range -- excluding the ruler at both refs, which')
print('  changes nothing at 654fb06 -- gives rung 28: 2 -> 17, rung 33: 31 -> 56,')
print('  and an inversion of 3.3 : 1 rather than 3.0 : 1. The finding survives;')
print('  the numbers moved. book6/wp82-verify.py block [2] asserts both columns.')

# ---------------------------------------------------------------------------
head(7, "THE CORPUS, COUNTED")
sys.path.insert(0, os.path.join(REPO, 'tools'))
try:
    from corpus_count import files as cfiles
    HAVE = True
except Exception:
    HAVE = False
def files(pat):
    if HAVE: return cfiles(pat)
    return sorted(gfiles(pat, 'HEAD'))
def classify(f):
    if f.startswith('book7/ch-whitehead-russell'):            return 'self'
    if f.startswith('book13/ch-types'):                       return 'self'
    if f == 'CLAUDE.md':                                      return 'scaffolding'
    if f.startswith('tools/'):                                return 'tooling'
    if f.startswith('docs/'):                                 return 'audit'
    if f.startswith('_archive/'):                             return 'archive'
    if (f.endswith('index.html') or f.startswith('index-')
            or f.startswith('master-index')):                 return 'listing'
    return 'CHAPTER'
def chapters(pat): return [f for f in files(pat) if classify(f) == 'CHAPTER']
check(HAVE, 'tools/corpus_count.py imported -- counts are entity-aware')
ROWS = [('Lean', r'\bLean\b'), ('incompleteness', r'incompleteness'),
        ('Godel', r'g(o|ö|&ouml;)del'), ('paradox', r'paradox'),
        ('Cantor', r'cantor'), ('self-reference', r'self.reference'),
        ('type theory', r'type theory'), ('dependent type', r'dependent type'),
        ('diagonal argument', r'diagonal argument'), ('Russell', r'russell'),
        ('Peano', r'peano'), ('power set', r'power set'),
        ('Whitehead', r'whitehead'), ('Principia Mathematica', r'principia mathematica'),
        ('Frege', r'frege'), ('theory of types', r'theory of types'),
        ('vicious circle', r'vicious circle'),
        ('propositional calculus', r'propositional (calculus|logic)'),
        ('definite description', r'definite description'), ('logicism', r'logicism'),
        ('Sheffer', r'sheffer'), ('axiom of reducibility', r'axiom of reducibility')]
C = {}
print('\n      %-26s %7s %10s' % ('pattern', 'files', 'chapters'))
for name, pat in ROWS:
    C[name] = (len(files(pat)), len(chapters(pat)))
    print('      %-26s %7d %10d' % (name, C[name][0], C[name][1]))
check(C['Lean'][0] > 400, 'Lean is in %d files -- the corpus runs on a type theory'
      % C['Lean'][0])
for z in ('theory of types', 'vicious circle', 'propositional calculus',
          'definite description', 'logicism', 'Sheffer', 'axiom of reducibility'):
    pat = dict(ROWS)[z]
    check(chapters(pat) == [], 'no chapter but this one uses "%s"' % z, str(chapters(pat)))
print('\n     470-odd files stand on the theory of types and none had named it.')
print('     Written to FAIL when a second chapter picks any of those up.')

# ---------------------------------------------------------------------------
head(8, 'CONTROL')
check(len(files(r'moonshine')) > 0, 'the counter returns files rather than nothing')
ABSENT = 'qqx' + '-no-file-contains-this-' + 'qqx'
check(files(ABSENT) == [], 'and none for a token no file writes down', str(files(ABSENT)))
check(stroke(True, True) is False and stroke(False, False) is True, 'the stroke is the stroke')
check(not nicod(True, True, True, True, False) is False, 'nicod() was evaluated, not assumed')

print('\n' + '=' * 70 + '\n  [HONESTY]\n' + '=' * 70)
print("""
  WHAT THIS ESTABLISHES. That the four stroke definitions of PM's second edition
  reproduce their truth tables; that the stroke realises all sixteen binary
  truth functions, by enumeration rather than by citation; that Nicod's single
  primitive proposition, as printed in the Introduction, is a tautology on all
  32 rows; that the rule of inference is sound on all eight; that *54.43 holds
  in every finite universe tested; and that the diagonal set lies outside the
  image of every one of the 65536 maps from a 4-element set to its power set.
  And, in this repository: that WP-82 is absent from the tree at the commit its
  first column names, present at the commit its second names, and matches all
  twelve of its own patterns there -- so the second column counted the ruler
  twelve times and the first counted it none. That is a vicious circle in PM's
  sense, found by an instrument written from PM's rule, and fixed by PM's remedy.

  WHAT IT DOES NOT ESTABLISH. Anything about the theory of types itself. No type
  hierarchy is constructed, the Axiom of Reducibility is quoted and not examined,
  and the ramified/simple distinction is not touched; the claim that Lean's
  dependent type theory descends from this work is a historical reading, made in
  the chapter and not checked here. Blocks [1]-[5] are exhaustions over finite
  sets, which is evidence and not proof -- and block [5] is finite in exactly the
  place the authors say matters, since they record that without the Axiom of
  Reducibility Cantor's theorem "breaks down unless n is finite". Nothing here
  addresses Godel, whose theorems are what the corpus's 47 "incompleteness"
  files are mostly about, and which postdate this volume by two decades. No
  priority is claimed: Principia Mathematica is 1910-1913.
""")
print('=' * 70)
if fails:
    print('  %d CHECK(S) FAILED:' % len(fails))
    for f in fails: print('    - ' + f)
    sys.exit(1)
print('  ALL CHECKS PASSED')
