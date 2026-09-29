#!/usr/bin/env python3
"""
Kikkawa -- four passages in one book, and the row in chGravity-scales they touch.

WHY THIS FILE EXISTS. book7/ch-kaku.html found that no page of the corpus names
Keiji Kikkawa, while chGravity-scales.html leans on string field theory and on
T-duality. The only source held that says what Kikkawa did is Kaku's account of
his own collaborator, in Parallel Worlds. This script confirms what that book says
he did (sentence by sentence, with the PDF page), does the arithmetic the duality
needs, and sets the corpus's list of string-interaction vertices beside the count
the book gives. It does NOT confirm the physics history: the papers are not held.

READS ~/Downloads/Michio-Kaku-Parallel-Worlds.pdf (447 PDF pages; book page = PDF page - 19).
Without pdftotext or the book those checks print SKIP, never PASS.
Standard library only.   python3 book7/ch-kikkawa-verify.py
"""
import math, os, re, subprocess, sys, html
from fractions import Fraction

fails, skips = [], []
def check(ok, msg, detail=''):
    print('    %s  %s%s' % ('PASS' if ok else 'FAIL', msg, ('  -- ' + detail) if detail and not ok else ''))
    if not ok: fails.append(msg)
def note(s): print('          ' + s)
def head(n, t): print('\n' + '=' * 72 + '\n  [%s]  %s\n' % (n, t) + '=' * 72)
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def squeeze(s):
    s = s.replace('­', '').lower()
    s = re.sub(r'-\s*\n\s*', '', s)
    return re.sub(r'[\s\-]+', '', s)

# ---------------------------------------------------------------------------
head(1, 'WHAT PARALLEL WORLDS SAYS ABOUT HIM  (his collaborator\'s account, not an independent source)')
PW = None
for d in ('~/Downloads', '~/mnt/Downloads'):
    p = os.path.join(os.path.expanduser(d), 'Michio-Kaku-Parallel-Worlds.pdf')
    if os.path.exists(p):
        try:
            txt = subprocess.run(['pdftotext', '-layout', p, '-'], capture_output=True, text=True, check=True).stdout
            PW = [squeeze(pg) for pg in txt.split('\f')]
        except Exception as e:
            print('    SKIP  pdftotext unavailable (%s)' % e.__class__.__name__)
        break
else:
    print('    SKIP  Parallel Worlds not found in ~/Downloads')
if PW is None: skips.append('PW')

def said(needle, msg):
    if PW is None:
        print('    SKIP  %s' % msg); return
    n = squeeze(needle)
    pgs = [i + 1 for i, pg in enumerate(PW) if n in pg]
    check(bool(pgs), '[PW pdf p.%s] %s' % (','.join(map(str, pgs[:3])) or '-', msg))

said('Bunji Sakita, Miguel Virasoro, and Keiji Kikkawa, then at the University of Wisconsin, realized that the S-matrix could be viewed as an infinite series of terms',
     'at Wisconsin with Sakita and Virasoro: the S-matrix as an infinite series, Veneziano the first term (book p.190)')
said('the Veneziano model was just the first and most important term in the series', 'Veneziano model = the first term of that series')
said('With my colleague Keiji Kikkawa of Osaka University, I successfully extracted the field theory of strings', '1974, Osaka: the field theory of strings, with Kaku (book p.191)')
said('Type I strings undergo five possible interactions', 'type I strings: five possible interactions (book p.209)')
said('For closed strings, only the last interaction is necessary', 'closed strings: only the last is necessary')
said('we showed that type I strings require five interactions', 'with string field theory they catalogued the interactions: five (book p.210)')
said('only one interaction term is necessary', 'closed strings: one interaction term')
said('Kikkawa and I also showed that it is possible to construct fully self-consistent theories with only closed strings', 'closed-string-only theories are self-consistent')
said('Today, these are called type II string theories', 'those are today called type II string theories')
said('This duality was first found in 1984 by my old colleague Keiji Kikkawa and his student Masami Yamasaki', 'the R <-> 1/R duality, 1984, with his student Yamasaki (book p.237)')
said('Kikkawa, Keiji, 190, 191, 209–10, 237', 'the index lists him on book pp.190, 191, 209-10, 237: the four passages, no others')

# ---------------------------------------------------------------------------
head(2, 'THE CORPUS ROW: HOW MANY STRING INTERACTIONS?   (R9: recorded, not resolved)')
def strip(s):
    s = re.sub(r'data:[^"\')\s]+', '', s)
    s = re.sub(r'<(script|style).*?</\1>', ' ', s, flags=re.S | re.I)
    return ' '.join(html.unescape(re.sub(r'<[^>]+>', ' ', s)).split())
gpath = os.path.join(ROOT, 'chGravity-scales.html')
g = strip(open(gpath, encoding='utf8', errors='ignore').read()) if os.path.exists(gpath) else ''
row = 'String interaction vertex: A₁ = emission, A₂ = splitting, A₃ = four-string junction. ADE singularity hierarchy in scattering amplitudes.'
check(row in g, 'chGravity-scales.html, F row, nano column, says exactly: ' + row[:70] + '...')
corpus_vertices = len(set(re.findall(r'A[₁₂₃] = ', row)))
book_open, book_closed = 5, 1
print('      corpus (F row)       : %d named vertices  (A1 emission, A2 splitting, A3 four-string junction)' % corpus_vertices)
print('      Parallel Worlds p.209: %d interactions for type I strings (break, join, fission), %d for closed strings' % (book_open, book_closed))
check(corpus_vertices == 3 and (book_open, book_closed) == (5, 1), 'the two counts are 3, 5 and 1 and they are not the same list')
note('They need not conflict: the corpus names singularity types of a fold hierarchy, the book counts')
note('terms in a field-theory action. Whether the A1-A3 hierarchy IS meant as the interaction terms is the')
note('AUTHOR\'S CALL [OPEN]; this script does not guess a mapping.')

# ---------------------------------------------------------------------------
head(3, 'THE DUALITY HE IS CREDITED WITH: A REFLECTION, NOT A RUNG')
print('  Closed string on a circle of radius R (alpha\' = 1): zero-mode M^2 = (n/R)^2 + (wR)^2.')
print('  [CITED, standard mass formula; not in the held text, which says the R and 1/R theories are "exactly the same".]')
def spec(R, nmax=6): return sorted((Fraction(n) / R) ** 2 + (w * R) ** 2 for n in range(-nmax, nmax + 1) for w in range(-nmax, nmax + 1))
check(all(spec(Fraction(p, q)) == spec(Fraction(q, p)) for p in range(1, 8) for q in range(1, 8)), 'the spectrum at R equals the spectrum at 1/R, n and w swapped (49 ratios)')
check([r for r in (Fraction(k, 100) for k in range(1, 1000)) if r == 1 / r] == [Fraction(1)], 'R = 1/R has the one positive solution R = 1')
x = lambda R: math.log10(R)
refl = lambda v: -v            # log R -> -log R
trans = lambda v: v + 10       # one Kardashev rung is +10 in log10 of power
vals = [-7.5, -1.0, 0.0, 3.25, 12.0]
check(all(refl(refl(v)) == v for v in vals) and refl(0.0) == 0.0 and all(refl(v) != v for v in vals if v != 0), 'log R -> -log R is an involution with exactly one fixed point (log R = 0)')
check(all(trans(v) != v for v in vals) and trans(trans(0.0)) == 20.0, 'a Kardashev rung, +10 in log10 power, has no fixed point and only ever moves one way')
note('So a scale ladder that goes on forever (translation) and a duality that folds the scale line back at')
note('one point (reflection) are different maps. chGravity-scales has a scale ladder and a self-dual point on the')
note('same nano column; whether they are one structure is a MODEL question, not claimed here.')
note('UNIT [OPEN]: R = 1 here is the string length; Parallel Worlds states the circles against the Planck length.')

# ---------------------------------------------------------------------------
head(4, 'A NAMESAKE, RECORDED SO NOBODY MERGES THEM')
p = os.path.join(ROOT, 'book6', 'ch07-microtubule-fibonacci.html')
if os.path.exists(p):
    t = strip(open(p, encoding='utf8', errors='ignore').read())
    check('Kikkawa, M., Ishikawa, T., Nakayama, T., Hirokawa, N. (1994)' in t, 'book6/ch07-microtubule-fibonacci cites M. Kikkawa (J. Cell Biol. 1994, the microtubule seam): the author of a J. Cell Biol. paper, not the string theorist')
else:
    print('    SKIP  book6/ch07 not present'); skips.append('ch07')

print('\n' + '=' * 72)
if skips: print('  SKIPPED (not passed, not failed): %s' % ', '.join(skips))
if fails:
    print('  %d FAIL:' % len(fails)); [print('    - ' + f) for f in fails]; sys.exit(1)
print('  all run checks passed.')
print('  Recorded as open, not checked: the 1974 and 1984 papers (WANTED, not held); whether the A1-A3')
print('  hierarchy is the interaction terms (author\'s call); Planck vs string length (OPEN).')
