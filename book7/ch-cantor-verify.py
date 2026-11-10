#!/usr/bin/env python3
"""
Georg Cantor -- book7/ch-cantor.html.

WHY THIS FILE EXISTS. The page states a theorem with a proof, says where the corpus
uses it, and prints eight corpus counts. This script (1) re-derives the finite cases of
the theorem by brute force, (2) checks the Lean file the page cites (text only),
(3) re-measures the eight counts with tools/corpus_count.py and compares them with the
numbers printed on the page, (4) checks the page's links, and (5) shows every check can fail.

BLOCKS
  [1] Cantor's theorem for |X| <= 4: no map X -> P(X) is onto (brute force, 65536 maps at |X| = 4).
  [2] The Lean file states rung_is_strict, from Cardinal.cantor, with no `sorry` outside comments.
  [3] The corpus, counted, entity-aware and anchored; page == measurement.
  [4] Links resolve; the index card exists.
  [5] Control.

PRIMARY SOURCE for the biographical statements: not machine-checked here (see HONESTY).
Standard library only.  python3 book7/ch-cantor-verify.py
"""
import os, re, sys, itertools, html as H
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(REPO, 'tools'))
fails = []
def check(ok, msg, detail=''):
    print('    %s  %s%s' % ('PASS' if ok else 'FAIL', msg, ('  -- ' + detail) if (detail and not ok) else ''))
    if not ok: fails.append(msg)
def head(n, t): print('\n' + '=' * 70 + '\n  [%s]  %s\n' % (n, t) + '=' * 70)
page = open(os.path.join(HERE, 'ch-cantor.html'), encoding='utf-8').read()
txt = re.sub(r'\s+', ' ', H.unescape(re.sub(r'<[^>]+>', ' ', page)))

head(1, "CANTOR'S THEOREM, FINITE CASES")
def onto(n):
    P = range(2 ** n)
    return any(set(fn) == set(P) for fn in itertools.product(P, repeat=n))
def onto_to_self(n): return any(set(fn) == set(range(n)) for fn in itertools.product(range(n), repeat=n))
for n in range(5):
    check(not onto(n), 'no map from a %d-set onto its power set (%d maps tried)' % (n, (2 ** n) ** n))
check(all(2 ** n > n for n in range(300)), '2^n > n for n < 300')

head(2, "THE LEAN FILE (text only)")
lp = os.path.join(REPO, 'Orthogenesis', 'NestedInfinities', 'EightChecks.lean')
lt = open(lp, encoding='utf-8').read() if os.path.exists(lp) else ''
code = re.sub(r'--.*', '', lt)
check('theorem rung_is_strict' in lt and 'Cardinal.cantor' in lt, 'the file states rung_is_strict (a < 2 ^ a) from Cardinal.cantor')
check(not re.search(r'\bsorry\b', code), 'no `sorry` outside comments')
print('    (not compiled by this script: a text check is not a kernel check)')

head(3, "THE CORPUS, COUNTED")
try:
    from corpus_count import files as _files; HAVE = True
except Exception:
    HAVE = False
check(HAVE, 'tools/corpus_count.py imported -- counts are entity-aware')
OWN = {'book7/ch-cantor.html', 'book7/ch-cantor-verify.py', 'book7/index.html'}
BOX = re.compile(r'<aside class="po-(?:related|run|gss)".*?</aside>', re.S)
def _own_text(f):
    try: return BOX.sub('', H.unescape(open(os.path.join(REPO, f), encoding='utf-8', errors='replace').read()))
    except OSError: return ''
def files(pat):
    # candidates from the entity-aware counter, then re-tested with the generated link boxes removed:
    # those boxes name this page's title on other pages and would count Cantor chapters that never mention him.
    rx = re.compile(pat, re.I)
    return [f for f in _files(pat) if f not in OWN and classify(f) not in ('listing', 'audit') and rx.search(_own_text(f))]
def classify(f):
    if f.startswith('tools/'): return 'tooling'
    if f.startswith('docs/'): return 'audit'
    if f.startswith(('_archive/', '_to_delete/')): return 'archive'
    if f == 'CLAUDE.md': return 'scaffolding'
    if f.endswith('index.html') or f.startswith('index-') or f.startswith('master-index'): return 'listing'
    return 'CHAPTER'
ROWS = [('Cantor', r'\bcantor\b'), ('alephbeth', r'\b(aleph|beth)\b|ℵ|ℶ|&#8501;|&#8502;|&aleph;|&beth;'),
        ('diagonal', r'diagonal argument'), ('transfinite', r'transfinite'), ('ch', r'continuum hypothesis'),
        ('Kronecker', r'kronecker'), ('Dedekind', r'dedekind'), ('Hilbert', r'hilbert')]
M = {}
if HAVE:
    print('\n      %-12s %7s %10s' % ('pattern', 'files', 'chapters'))
    for k, pat in ROWS:
        fs = files(pat); M[k] = (len(fs), len([f for f in fs if classify(f) == 'CHAPTER']))
        print('      %-12s %7d %10d' % (k, M[k][0], M[k][1]))
    for k, pat in ROWS:
        fz, cz = M[k]
        tokens = (re.search(r'<tr><td>[^<]*(?:<strong>)?[^<]*(?:</strong>)?[^<]*</td><td class="n">%d</td><td class="n">%d</td></tr>' % (fz, cz), page))
        check(tokens is not None, 'page prints %s: %d files, %d chapters' % (k, fz, cz))
    check('in %d files and' % M['Cantor'][0] in txt or ('%d files' % M['Cantor'][0]) in txt, 'the hero and prose print the measured Cantor file count')
    check('Dedekind, appears in %d.' % M['Dedekind'][0] in txt, 'the hero prints the measured Dedekind count')
    check(M['Cantor'][0] > M['Dedekind'][0] * 5, 'Cantor files exceed 5x Dedekind files (the ratio the page remarks on)')
    check(M['Hilbert'][0] > M['Kronecker'][0] > M['Dedekind'][0], 'Hilbert > Kronecker > Dedekind in files (the order the page states)')
    for must in ('book7/ch-whitehead-russell.html', 'ch8-nested-infinities.html', 'ch-ocio.html'):
        check(must in files(r'\bcantor\b'), '%s names Cantor (the page cites it)' % must)
    ABSENT = 'qqx' + '-no-file-contains-this-' + 'qqx'
    check(files(ABSENT) == [], 'control: the counter returns nothing for a token no file writes down')
    check(len(files(r'moonshine')) > 0, 'control: the counter returns files rather than nothing')

head(4, "LINKS AND CARD")
ll = [l for l in re.findall(r'href="([^"#]+)"', page) if not re.match(r'https?:|mailto:|/', l)]
miss = [l for l in ll if not os.path.exists(os.path.normpath(os.path.join(HERE, l)))]
check(len(ll) >= 8 and not miss, '%d local links, none missing' % len(ll), ', '.join(miss))
idx = open(os.path.join(HERE, 'index.html'), encoding='utf-8').read()
check('href="ch-cantor.html"' in idx, 'book7/index.html has the Cantor card')

head(5, "CONTROL")
check(onto_to_self(3) and not onto(3), 'the search finds an onto map X->X for |X| = 3 but none X->P(X)')
check('{{' not in page, 'no unfilled placeholder left on the page')
check(re.search(r'\bsorry\b', re.sub(r'--.*', '', 'theorem t : True := by sorry')) is not None, 'control: a `sorry` in code is detected')
check(re.search(r'\bsorry\b', re.sub(r'--.*', '', '-- no sorry here\ntheorem t : True := trivial')) is None, 'control: a `sorry` only in a comment is not flagged')

print('\n' + '=' * 70 + '\n  [HONESTY]\n' + '=' * 70)
print("""
  WHAT THIS ESTABLISHES. That no function from a set of 0..4 members onto its power set
  exists (brute force); that the Lean file's text states the theorem and has no sorry
  outside comments; that the eight counts printed on the page equal what
  tools/corpus_count.py returns on the working tree; and that the page's links resolve.

  WHAT IT DOES NOT ESTABLISH. The theorem for infinite sets: the proof is the standard
  one, printed on the page, and not machine-checked here. That the Lean file compiles.
  Any biographical statement (dates, school, languages, translations): those come from
  sources read through a fetch tool and are not checked. Whether the chapters that name
  Cantor treat him correctly: only three were read, and they are cited, not audited.
  The counts move whenever a file mentioning these names is added, so this script is
  written to FAIL then; update the page, not the script.
""")
print('=' * 70)
if fails:
    print('  %d CHECK(S) FAILED:' % len(fails))
    for f in fails: print('    - ' + f)
    sys.exit(1)
print('  ALL CHECKS PASSED')
