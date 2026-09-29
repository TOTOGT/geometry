#!/usr/bin/env python3
"""
Kaku -- what the corpus's nano-scale row rests on, and what a civilization ladder
costs once every rung has a number.

WHY THIS FILE EXISTS. book7 is "who put a brick in dm3's wall, and which brick".
chGravity-scales.html has a nano-scale column whose C row is "Level truncation in
Witten's cubic string field theory" and whose header says "T-duality self-dual
point at R = 1". Neither the page nor any other page of the corpus names the
physicist who wrote the field theory of strings before Witten's, or the
physicist who found the R -> 1/R duality the row leans on. This script measures
that, does the arithmetic the row needs, and then holds one popular scale --
the Type I / II / III civilization ladder, as three of his books print it --
against its own numbers. R24: the script runs before the sentence.

READS (not bundled; the books are the author's own copies):
  ~/Downloads/Michio-Kaku-Parallel-Worlds.pdf
  ~/Downloads/physics-of-the-impossible-by-michael-kaku1.pdf
  ~/Downloads/Future Physics michio kaku.pdf     (Physics of the Future)
Without pdftotext or a book, that section prints SKIP -- it never prints PASS.
The scans are OCR and carry superscripts flattened ("10 16" reads "1016"); the
needles below are matched with whitespace, hyphens and case removed, and each
hit prints the PDF page it was found on. PDF page numbers are the file's, not
the book's (Parallel Worlds: book page = PDF page - 19).

Standard library only (plus pdftotext for section 1).   python3 book7/ch-kaku-verify.py
"""

import math, os, re, subprocess, sys, hashlib, html
from fractions import Fraction

fails, skips = [], []
def check(ok, msg, detail=''):
    print('    %s  %s%s' % ('PASS' if ok else 'FAIL', msg,
                            ('  -- ' + detail) if detail and not ok else ''))
    if not ok: fails.append(msg)
def note(s): print('          ' + s)
def head(n, t):
    print('\n' + '=' * 72 + '\n  [%s]  %s\n' % (n, t) + '=' * 72)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASELINE = 'aaba379'   # HEAD when this chapter was written; the "before" of section 6

# ---------------------------------------------------------------------------
head(1, 'THE THREE BOOKS: HELD, AND THE SENTENCES THIS CHAPTER RELIES ON')
BOOKS = {
    'PW': 'Michio-Kaku-Parallel-Worlds.pdf',
    'POTI': 'physics-of-the-impossible-by-michael-kaku1.pdf',
    'PF': 'Future Physics michio kaku.pdf',
}
def find_pdf(name):
    for d in ('~/Downloads', '~/mnt/Downloads'):
        p = os.path.join(os.path.expanduser(d), name)
        if os.path.exists(p): return p
    return None

def squeeze(s):
    s = s.replace('­', '').lower()
    s = re.sub(r'-\s*\n\s*', '', s)          # end-of-line hyphenation
    return re.sub(r'[\s\-]+', '', s)

PAGES = {}
for key, name in BOOKS.items():
    p = find_pdf(name)
    if not p:
        print('    SKIP  %s not found in ~/Downloads' % name); skips.append(key); continue
    try:
        txt = subprocess.run(['pdftotext', '-layout', p, '-'], capture_output=True,
                             text=True, check=True).stdout
    except Exception as e:
        print('    SKIP  %s: pdftotext unavailable (%s)' % (name, e.__class__.__name__)); skips.append(key); continue
    PAGES[key] = [squeeze(pg) for pg in txt.split('\f')]
    md5 = hashlib.md5(open(p, 'rb').read()).hexdigest()
    print('    held  %-5s %d PDF pages  md5 %s  %s' % (key, len(PAGES[key]) - 1, md5[:8], name))

def where(key, needle, near=None):
    """PDF pages (1-based) where the squeezed needle occurs; if near is given the
       page must also contain it."""
    n = squeeze(needle); m = squeeze(near) if near else None
    return [i + 1 for i, pg in enumerate(PAGES[key]) if n in pg and (m is None or m in pg)]

def said(key, needle, msg, near=None):
    if key not in PAGES:
        print('    SKIP  [%s] %s' % (key, msg)); return
    pgs = where(key, needle, near)
    check(bool(pgs), '[%s p.%s] %s' % (key, ','.join(map(str, pgs[:4])) or '-', msg))

# Physics of the Impossible (OCR is letter-spaced; squeezing repairs it)
said('POTI', 'thereby founding string field theory', 'he says he wrote strings in terms of Faraday fields and so founded string field theory')
said('POTI', 'cofounder of string field theory', 'the jacket calls him cofounder of string field theory')
said('POTI', 'Type II civilizations: those that can utilize the entire power of their sun, making them 10 billion times more powerful than a Type I', 'Type II = 10 billion times Type I (no watts given here)')
said('POTI', 'a matter of a few thousand years to tens of thousands of years', 'time between types at "a few percent per year": a few thousand to tens of thousands of years')
said('POTI', 'Henry Semat Professor of Theoretical Physics at the Graduate Center of the City University of New York', 'the jacket gives his chair: Henry Semat Professor, Graduate Center, CUNY')
# Parallel Worlds
said('PW', 'With my colleague Keiji Kikkawa of Osaka University, I successfully extracted the field theory of strings', 'string field theory with Kikkawa, 1974 (his own account)')
said('PW', 'In 1974, I decided to tackle this problem', 'the year is 1974')
said('PW', 'This duality was first found in 1984 by my old colleague Keiji Kikkawa and his student Masami Yamasaki', 'T-duality credited to Kikkawa and Yamasaki, 1984')
said('PW', 'take a string theory and wrap up one dimension into a circle of radius R', 'the R / 1/R statement of the duality')
said('PW', 'we find that they are exactly the same', 'the R theory and the 1/R theory are "exactly the same"')
said('PW', 'by definition, they are able to utilize the entire amount of solar energy striking their planet, or 1016 watts', 'Type I = 10^16 W (superscript flattened in the scan)')
said('PW', 'approximately 1026 watts', 'Type II = ~10^26 W')
said('PW', 'approximately 1036 watts', 'Type III = ~10^36 W')
said('PW', 'differs from the next lower type by a factor of 10 billion', 'each type is 10 billion times the last')
said('PW', 'grows at a modest rate of 2 to 3 percent', 'growth assumed: 2 to 3 percent a year')
said('PW', 'approximately 100 to 200 years from attaining type I status', 'Type I in 100 to 200 years')
said('PW', 'roughly 1,000 to 5,000 years to achieve type II status', 'Type II in 1,000 to 5,000 years')
said('PW', 'perhaps 100,000 to 1,000,000 years to achieve type III status', 'Type III in 100,000 to 1,000,000 years')
said('PW', 'type I.1 civilization, for example, which generates 1017 watts', 'Sagan: 10^17 W is Type I.1')
said('PW', 'more like a type 0.7 civilization', 'today is about Type 0.7')
said('PW', 'a thousand times smaller than a type I', 'Type 0.7 is a thousand times smaller than Type I')
# Physics of the Future
said('PF', 'consuming the sliver of sunlight that falls on their planet, or about 1017 watts', 'Type I = 10^17 W')
said('PF', 'all the energy that their sun emits, or 1027 watts', 'Type II = 10^27 W')
said('PF', 'or about 1037 watts', 'Type III = 10^37 W')
said('PF', 'Each type is separated by a factor of 10 billion', 'each type is 10 billion times the last')
said('PF', 'grows at the rate of 1 percent each year', 'growth assumed: 1 percent a year')
said('PF', 'it takes roughly 2,500 years to go from one civilization to the next', '1 percent: ~2,500 years per type')
said('PF', 'A 2 percent growth rate would give a transition period of 1,200 years', '2 percent: 1,200 years per type')
said('PF', 'we will attain Type I status in about 100 years', 'Type I in about 100 years')
said('PF', 'a Type .7 civilization', 'today is Type .7')
said('PF', 'the great recession of 2008', 'it refers to the great recession of 2008, so it postdates 2004')
said('PW', 'qxd 10/27/04', 'the page footers carry the date 10/27/04')

# ---------------------------------------------------------------------------
head(2, 'THE LADDERS THEMSELVES: INTERNAL ARITHMETIC')
PW_L  = [16, 26, 36]     # log10 watts, Parallel Worlds
PF_L  = [17, 27, 37]     # log10 watts, Physics of the Future
check(all(b - a == 10 for a, b in zip(PW_L, PW_L[1:])), 'Parallel Worlds: 10^16, 10^26, 10^36 step by 10^10')
check(all(b - a == 10 for a, b in zip(PF_L, PF_L[1:])), 'Physics of the Future: 10^17, 10^27, 10^37 step by 10^10')
check(10**10 * 10**26 == 10**36, 'PW: 10 billion stars x 10^26 W = 10^36 W (its own Type III definition)')

# Sagan's decimal grading as Parallel Worlds describes it: ten subtypes per type,
# I.1 = 10^17 W.  Extended to K(P) = (log10 P - 6)/10, which is 1.0 at 10^16.
K = lambda logP: (logP - 6) / 10
check(abs(K(16) - 1.0) < 1e-12 and abs(K(17) - 1.1) < 1e-12, 'Sagan grading: 10^16 W = Type 1.0, 10^17 W = Type 1.1 (PW p.308)')
check(abs(K(13) - 0.7) < 1e-12, 'Type 0.7 is 10^13 W on that grading, 10^3 below Type I (PW: "a thousand times smaller")')
note('So 10^17 W is "Type I.1" in Parallel Worlds and "Type I" in Physics of the Future.')

# ---------------------------------------------------------------------------
head(3, 'THE LADDERS AGAINST THE SUN')
S, R_E, L_SUN = 1361.0, 6.371e6, 3.828e26     # W/m^2, m, W  (nominal reference values, CITED, not held)
p_planet = math.pi * R_E**2 * S
note('sunlight intercepted by the Earth  pi R^2 S = %.4e W   (S=1361 W/m^2, R=6.371e6 m)' % p_planet)
note('solar luminosity                   L       = %.4e W' % L_SUN)
note('ratio star / planet intercept      = %.3e   (both books say 10^10)' % (L_SUN / p_planet))
d16 = math.log10(p_planet / 1e16); d17 = math.log10(p_planet / 1e17)
note('PW  Type I 10^16 W is %.2f decades below the intercepted sunlight (x%.1f)' % (d16, p_planet / 1e16))
note('PF  Type I 10^17 W is %.2f decades below it            (x%.2f)' % (d17, p_planet / 1e17))
check(d16 > 1.0,  'PW Type I (10^16 W) is more than a decade below the sunlight it says it equals')
check(0 < d17 < 1.0, 'PF Type I (10^17 W) is within a decade of that sunlight')
check(2.0e9 < L_SUN / p_planet < 2.4e9, 'star / planet-intercept is 2.2 x 10^9, not 10^10 (the 10^10 is a definition, PW p.307 "by definition")')

# ---------------------------------------------------------------------------
head(4, 'THE LADDERS AGAINST THEIR OWN GROWTH RATES   (t = ln(ratio) / ln(1+g))')
def years(ratio_log10, g): return ratio_log10 * math.log(10) / math.log(1 + g)
# Physics of the Future: one type to the next, 10^10
t1, t2 = years(10, 0.01), years(10, 0.02)
note('PF: 10^10 at 1%%/yr = %.0f yr (book: roughly 2,500);  at 2%%/yr = %.0f yr (book: 1,200)' % (t1, t2))
check(abs(t1 - 2500) / 2500 < 0.10, 'PF 1%%: %.0f years is within 10%% of the book\'s "roughly 2,500"' % t1)
check(abs(t2 - 1200) / 1200 < 0.05, 'PF 2%%: %.0f years is within 5%% of the book\'s 1,200' % t2)
# Parallel Worlds: today = Type 0.7 = 10^13 W; growth 2-3 %
a3, a2 = years(3, 0.03), years(3, 0.02)
note('PW: 10^3 (Type 0.7 -> I) at 3%%/yr = %.0f yr, at 2%%/yr = %.0f yr   (book: 100 to 200)' % (a3, a2))
check(a3 > 200, 'PW: 2-3%% growth needs %.0f to %.0f years to close the 10^3 gap, not 100 to 200' % (a3, a2))
need_hi, need_lo = math.exp(3 * math.log(10) / 100) - 1, math.exp(3 * math.log(10) / 200) - 1
note('    growth that WOULD close 10^3 in 100 yr = %.2f%%/yr; in 200 yr = %.2f%%/yr' % (100 * need_hi, 100 * need_lo))
b3, b2 = years(13, 0.03), years(13, 0.02)
note('PW: Type II (10^13 above today) at 3%%/yr = %.0f yr, at 2%%/yr = %.0f yr (book: 1,000 to 5,000)' % (b3, b2))
check(900 < b3 < 1100, 'PW Type II: the low end (1,000 yr) is what 3%%/yr gives (%.0f)' % b3)
c3, c2 = years(23, 0.03), years(23, 0.02)
note('PW: Type III (10^23 above today) at 3%%/yr = %.0f yr, at 2%%/yr = %.0f yr (book: 100,000 to 1,000,000)' % (c3, c2))
check(c2 < 5000, 'PW Type III: 2-3%%/yr gives %.0f to %.0f years, about 40 to 500 times fewer than the book\'s 100,000 to 1,000,000' % (c3, c2))
g_needed = math.exp(23 * math.log(10) / 1e5) - 1
note('    growth that WOULD take 10^5 years to reach Type III from today = %.3f%%/yr' % (100 * g_needed))

# ---------------------------------------------------------------------------
head(5, 'THE ROW THE CORPUS LEANS ON: T-DUALITY AND THE LEVEL-N SUBSPACE')
print('  5a. Closed string on a circle of radius R, alpha\' = 1: the zero-mode part of')
print('      M^2 is (n/R)^2 + (wR)^2.  [CITED, standard; not in the held text, which')
print('      says only that the R and 1/R theories are "exactly the same". WANTED.]')
def spectrum(R, nmax=6):
    return sorted((Fraction(n)/R)**2 + (w*R)**2 for n in range(-nmax, nmax+1) for w in range(-nmax, nmax+1))
ok = all(spectrum(Fraction(p, q)) == spectrum(Fraction(q, p))
         for p in range(1, 8) for q in range(1, 8))
check(ok, 'the (n,w) spectrum at R equals the spectrum at 1/R (n and w swapped), 49 ratios')
check(all(Fraction(n)/Fraction(1) == Fraction(n) for n in range(-6, 7)) and
      spectrum(Fraction(1)) == sorted((Fraction(n))**2 + Fraction(w)**2 for n in range(-6, 7) for w in range(-6, 7)),
      'at R = 1 the map R -> 1/R fixes the theory and only swaps n and w')
check([r for r in (Fraction(k, 100) for k in range(1, 1000)) if r == 1 / r] == [Fraction(1)], 'R = 1/R has the one positive solution R = 1')
note('UNIT: this is R = 1 in units of the string length sqrt(alpha\'). Parallel Worlds states')
note('the circle sizes against the Planck length. What that difference does is NOT checked here [OPEN].')

print('\n  5b. Light-cone gauge, open bosonic string, D = 26: 24 transverse oscillators.')
print('      States at level N = coefficient of q^N in 1 / prod (1 - q^n)^24.')
NMAX = 1000
def sigma(k): return sum(d for d in range(1, k + 1) if k % d == 0)
sig = [0] + [sigma(k) for k in range(1, 61)]
p24 = [1]
# n p(n) = 24 sum_{k=1..n} sigma(k) p(n-k): exact integers; sigma via sieve beyond 60
sig = [0] * (NMAX + 1)
for d in range(1, NMAX + 1):
    for m in range(d, NMAX + 1, d): sig[m] += d
for n in range(1, NMAX + 1):
    s = 24 * sum(sig[k] * p24[n - k] for k in range(1, n + 1))
    assert s % n == 0
    p24.append(s // n)
note('level N : states   ' + ' , '.join('%d:%d' % (n, p24[n]) for n in range(0, 9)))

def poly_mul(a, b, n):
    out = [0] * (n + 1)
    for i, x in enumerate(a):
        if x == 0: continue
        for j, y in enumerate(b):
            if i + j > n: break
            out[i + j] += x * y
    return out
N0 = 12
prod = [1] + [0] * N0
for k in range(1, N0 + 1):
    f = [0] * (N0 + 1); f[0] = 1; f[k] = -1
    for _ in range(24): prod = poly_mul(prod, f, N0)       # prod (1-q^n)^24
check(poly_mul(prod, p24[:N0 + 1], N0) == [1] + [0] * N0, 'the level counts times prod(1-q^n)^24 give exactly 1 through q^12 (independent expansion)')
tau = prod                                                 # q * prod (1-q^n)^24 = Delta = sum tau(n) q^n
check(tau[:6] == [1, -24, 252, -1472, 4830, -6048], 'prod(1-q^n)^24 = 1 - 24q + 252q^2 - 1472q^3 + 4830q^4 - 6048q^5, i.e. Ramanujan\'s tau(1..6), so the level counts are the coefficients of q/Delta')
check(p24[1] == 24, 'level 1 has 24 states (the 24 polarizations of the massless vector in D = 26)')
check(p24[2] == 24 + 24 * 25 // 2 == 25 * 26 // 2 - 1 == 324, 'level 2 has 324 = 24 + 300 states, the same number as a symmetric traceless tensor of SO(25) (arithmetic only)')
def logI(nu, x):
    """log of the modified Bessel function I_nu(x), summed in logs so x ~ 400 does not overflow"""
    terms = [(2*m + nu) * math.log(x / 2) - math.lgamma(m + 1) - math.lgamma(m + nu + 1)
             for m in range(0, int(2 * x) + 200)]
    mx = max(terms)
    return mx + math.log(sum(math.exp(t - mx) for t in terms))
def log_rademacher(N):
    """log of 2 pi (N-1)^(-13/2) I_13(4 pi sqrt(N-1)): the first term of the Rademacher series
       for the coefficient of q^(N-1) in 1/Delta.  The later terms are smaller by about exp(-2 pi sqrt(N))."""
    n = N - 1
    return math.log(2 * math.pi) - 6.5 * math.log(n) + logI(13, 4 * math.pi * math.sqrt(n))
errs = {N: abs(math.log(p24[N]) - log_rademacher(N)) for N in (10, 25, 100, 500, 1000)}
note('|log p24(N) - log(2 pi (N-1)^(-13/2) I_13(4 pi sqrt(N-1)))| :  ' + '  '.join('N=%d: %.1e' % (N, v) for N, v in errs.items()))
check(all(v < 1e-9 for v in errs.values()),
      'the level counts are 2 pi (N-1)^(-13/2) I_13(4 pi sqrt(N-1)) to better than 1 part in 10^9 for N = 10..1000, so they grow as exp(4 pi sqrt N) N^(-27/4)')
note('NOT computed [OPEN]: the same count for the covariant (Siegel-gauge, ghost-carrying) level truncation')
note('that Witten\'s cubic theory uses, which is NOT this number. And that light-cone gauge is the gauge of')
note('the 1974 Kaku-Kikkawa papers is [WANTED]: the held text says "field theory of strings", not which gauge.')

# ---------------------------------------------------------------------------
head(6, 'THE CORPUS, BEFORE THIS CHAPTER (pinned to %s)' % BASELINE)
def strip(s):
    s = re.sub(r'data:[^"\')\s]+', '', s)
    s = re.sub(r'<(script|style).*?</\1>', ' ', s, flags=re.S | re.I)
    return html.unescape(re.sub(r'<[^>]+>', ' ', s))
def blobs():
    out = subprocess.run(['git', '-C', ROOT, 'ls-tree', '-r', '--name-only', BASELINE], capture_output=True, text=True)
    if out.returncode != 0: return None
    for f in out.stdout.splitlines():
        if not f.endswith('.html'): continue
        if f.startswith(('_to_delete/', 'docs/ml-evidence/', 'node_modules/')): continue
        r = subprocess.run(['git', '-C', ROOT, 'show', '%s:%s' % (BASELINE, f)], capture_output=True, text=True, errors='ignore')
        yield f, strip(r.stdout)
bl = blobs()
if bl is None:
    print('    SKIP  baseline %s not in this checkout' % BASELINE); skips.append('git')
else:
    files = list(bl)
    n_kaku = [f for f, t in files if re.search(r'\bKaku\b', t)]
    n_kik  = [f for f, t in files if re.search(r'Keiji Kikkawa|Kikkawa and Yamasaki', t)]
    n_kik_any = [f for f, t in files if re.search(r'Kikkawa', t)]
    n_sft  = [f for f, t in files if re.search(r'string field theory', t, re.I)]
    n_td   = [f for f, t in files if re.search(r'T-duality', t)]
    n_lt   = [f for f, t in files if re.search(r'level truncation', t, re.I)]
    n_kar  = [f for f, t in files if re.search(r'Kardashev|Type I civili[sz]ation', t)]
    print('    %d chapters read.' % len(files))
    for label, L in (('Kaku', n_kaku), ('Keiji Kikkawa', n_kik), ('any Kikkawa (a namesake: M. Kikkawa, microtubule seam)', n_kik_any), ('"string field theory"', n_sft),
                     ('"T-duality"', n_td), ('"level truncation"', n_lt), ('Kardashev / Type I civilization', n_kar)):
        print('      %-34s %3d files  %s' % (label, len(L), ', '.join(L[:6])))
    check(len(n_kaku) == 0, 'no page of the corpus named Kaku before this chapter')
    check(len(n_kik) == 0, 'no page of the corpus named Keiji Kikkawa')
    check(len(n_kar) == 0, 'no page of the corpus mentioned the Kardashev scale')
    g = [t for f, t in files if f == 'chGravity-scales.html']
    check(bool(g) and 'Level truncation in Witten\'s cubic string field theory' in ' '.join(g[0].split()),
          'chGravity-scales.html, C row, nano column: "Level truncation in Witten\'s cubic string field theory"')
    check(bool(g) and 'T-duality self-dual point at R = 1' in ' '.join(g[0].split()),
          'chGravity-scales.html, nano-scale text: "T-duality self-dual point at R = 1"')

# ---------------------------------------------------------------------------
print('\n' + '=' * 72)
if skips: print('  SKIPPED (not passed, not failed): %s' % ', '.join(skips))
if fails:
    print('  %d FAIL:' % len(fails))
    for f in fails: print('    - ' + f)
    sys.exit(1)
print('  all run checks passed.')
print('  Recorded as open, not checked: original 1974 and 1984 papers (WANTED); Kardashev 1964 and')
print('  Sagan sources (WANTED); Planck vs string length in the R/1/R statement (OPEN); covariant')
print('  level-truncation counts (OPEN); which gauge Kaku-Kikkawa used (WANTED).')
