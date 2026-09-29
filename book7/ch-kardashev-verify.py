#!/usr/bin/env python3
"""
Kardashev -- the paper, the books that describe it, and what changed between them.

WHY THIS FILE EXISTS. book7/ch-kaku.html found that no page of the corpus mentions
the Kardashev scale and that Kaku's books print its rungs inconsistently. The author
then supplied Kardashev's own paper: N. S. Kardashev, "Transmission of Information by
Extraterrestrial Civilizations", Soviet Astronomy 8 (1964) 217-221 (a scan with no text
layer). This script reads it (OCR), derives its rungs from the years the paper itself
prints, sets them beside the ladders three later texts print, recomputes the two
waste-heat sentences the books make, and counts what the corpus's Dyson chapter says.

READS ~/Downloads (PDF pages, not book pages; SKIP, never PASS, when a file or tool is missing):
  The  Kardashev.pdf                       (the 1964 paper; needs pdftoppm + tesseract)
  The Cognitive Kardashev Scale-...pdf     (arXiv 2605.22840v2, 21 Jul 2026, Sachin Sharma)
  Michio-Kaku-Parallel-Worlds.pdf, Future Physics michio kaku.pdf, physics-of-the-impossible-...pdf
Standard library only, plus pdftotext / pdftoppm / tesseract for the scans.
   python3 book7/ch-kardashev-verify.py
"""
import math, os, re, subprocess, sys, html, hashlib, tempfile, glob

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
def find_pdf(name):
    for d in ('~/Downloads', '~/mnt/Downloads'):
        p = os.path.join(os.path.expanduser(d), name)
        if os.path.exists(p): return p
    return None
def pdftext(p):
    return subprocess.run(['pdftotext', '-layout', p, '-'], capture_output=True, text=True, check=True).stdout

# ---------------------------------------------------------------------------
head(1, 'THE PAPER ITSELF   (Soviet Astronomy 8, 217-221, 1964; OCR of a scan)')
PAPER = None
p = find_pdf('The  Kardashev.pdf')
if not p:
    print('    SKIP  The  Kardashev.pdf not found in ~/Downloads'); skips.append('paper')
else:
    print('    held  md5 %s  %s pages' % (hashlib.md5(open(p, 'rb').read()).hexdigest()[:8],
          re.search(r'Pages:\s+(\d+)', subprocess.run(['pdfinfo', p], capture_output=True, text=True).stdout).group(1)))
    try:
        tmp = tempfile.mkdtemp()
        subprocess.run(['pdftoppm', '-r', '250', '-png', p, os.path.join(tmp, 'p')], check=True, capture_output=True)
        PAPER = []
        for png in sorted(glob.glob(os.path.join(tmp, 'p-*.png'))):
            PAPER.append(squeeze(subprocess.run(['tesseract', png, '-'], capture_output=True, text=True, check=True).stdout))
    except Exception as e:
        print('    SKIP  OCR unavailable (%s)' % e.__class__.__name__); skips.append('paper'); PAPER = None

def in_paper(needle, msg):
    if PAPER is None: print('    SKIP  %s' % msg); return
    n = squeeze(needle); pgs = [i + 1 for i, t in enumerate(PAPER) if n in t]
    check(bool(pgs), '[paper scan p.%s] %s' % (','.join(map(str, pgs)) or '-', msg))

in_paper('TRANSMISSION OF INFORMATION BY EXTRATERRESTRIAL CIVILIZATIONS', 'title')
in_paper('P. K. Shternberg Astronomical Institute', 'author\'s institute as printed')
in_paper('Astronomicheskii Zhurnal, Vol. 41, No. 2', 'translated from Astronomicheskii Zhurnal 41(2)')
in_paper('Original article submitted December 12, 1963', 'submitted 12 December 1963')
in_paper('notably CTA-21 and CTA-102', 'the abstract speculates that CTA-21 and CTA-102 may be artificial sources')
in_paper('technological level close to the level presently attained on the earth', 'Type I is "technological level close to the level presently attained on the earth"')
in_paper('harnessing the energy radiated by its own star', 'Type II harnesses the energy radiated by its own star')
in_paper('Dyson sphere', 'Type II is exemplified by the stage of building a "Dyson sphere"')
in_paper('in possession of energy on the scale of its own galaxy', 'Type III has the energy of its own galaxy')
in_paper('F. G. Dyson, Science, 131, 1667 (1959)', 'reference [6]: F. G. Dyson, Science 131, 1667 (1959)')
in_paper('the total quantity of energy expended by all of mankind per second at the present time', 'the present-day figure is all of mankind\'s energy use')
in_paper('3-4% over the next 60 years', 'growth statistics: 3-4% over the next 60 years')
in_paper('Assuming x = 1%', 'the projection assumes x = 1%')
in_paper('3200 years from now', 'at 1%: the Sun\'s output, 3200 years from now')
in_paper('in 5800 years', 'at 1%: 10^11 stars, in 5800 years')
if PAPER is not None:
    check(not any('infrared' in t for t in PAPER), 'the word "infrared" is on none of the five pages: the paper is about radio')

print('\n  The exponents are superscripts and OCR garbles them, so they are DERIVED from the years the paper prints:')
x = 0.01
g1 = 3200 * math.log(1 + x) / math.log(10)      # decades from Type I to Type II
g2 = 5800 * math.log(1 + x) / math.log(10)      # decades from Type I to Type III
note('3200 yr at 1%%/yr = %.2f decades; 5800 yr = %.2f decades' % (g1, g2))
check(abs(g1 - 14) < 0.2 and abs(g2 - 25) < 0.2, 'the printed years give 14 decades (I -> II) and 25 (I -> III), so II -> III is 11')
KEYED = {'I': 4e19, 'II': 4e33, 'III': 4e44}     # erg/s, KEYED BY EYE from scan p.219 (journal), PDF p.3; exponents corroborated above
check(abs(math.log10(KEYED['II'] / KEYED['I']) - round(g1)) < 1e-9 and abs(math.log10(KEYED['III'] / KEYED['I']) - round(g2)) < 1e-9,
      'the keyed table (4e19, 4e33, 4e44 erg/s) agrees with those derived gaps exactly')
K_W = {k: v * 1e-7 for k, v in KEYED.items()}    # 1 erg/s = 1e-7 W
note('Kardashev 1964 in watts: I = %.1e   II = %.1e   III = %.1e' % (K_W['I'], K_W['II'], K_W['III']))
check(abs(K_W['II'] / 3.828e26 - 1) < 0.10, 'his Type II, 4e26 W, is the solar luminosity to within 10% (3.828e26 W, CITED)')
check(abs(1e11 * K_W['II'] / K_W['III'] - 1) < 1e-9, 'his Type III is 10^11 Type IIs: "the output of 10^11 stars like the sun"')
for gph, want, label in ((0.01, 3200, 'II'), (0.01, 5800, 'III')):
    t = math.log(KEYED[label] / KEYED['I']) / math.log(1 + gph)
    check(abs(t - want) / want < 0.02, 'his 1%% growth from 4e19 erg/s reaches Type %s in %.0f years; the paper prints %d' % (label, t, want))

# ---------------------------------------------------------------------------
head(2, 'THE LATER LADDERS   (three texts that describe it)')
BOOKS = {'PW': 'Michio-Kaku-Parallel-Worlds.pdf', 'PF': 'Future Physics michio kaku.pdf',
         'POTI': 'physics-of-the-impossible-by-michael-kaku1.pdf', 'SH': 'The Cognitive Kardashev Scale- Quantifying the Material Envelope of Civilisational Computation.pdf'}
PAGES = {}
for k, name in BOOKS.items():
    pp = find_pdf(name)
    if not pp:
        print('    SKIP  %s not found in ~/Downloads' % name); skips.append(k); continue
    try: PAGES[k] = [squeeze(pg) for pg in pdftext(pp).split('\f')]
    except Exception as e: print('    SKIP  %s: pdftotext unavailable' % name); skips.append(k)
def said(key, needle, msg):
    if key not in PAGES: print('    SKIP  [%s] %s' % (key, msg)); return
    n = squeeze(needle); pgs = [i + 1 for i, pg in enumerate(PAGES[key]) if n in pg]
    check(bool(pgs), '[%s pdf p.%s] %s' % (key, ','.join(map(str, pgs[:3])) or '-', msg))
said('PW', 'by definition, they are able to utilize the entire amount of solar energy striking their planet, or 1016 watts', 'Kaku PW: Type I = all sunlight striking the planet, 10^16 W')
said('PW', 'approximately 1026 watts', 'Kaku PW: Type II ~ 10^26 W'); said('PW', 'approximately 1036 watts', 'Kaku PW: Type III ~ 10^36 W')
said('PF', 'consuming the sliver of sunlight that falls on their planet, or about 1017 watts', 'Kaku PF: Type I = the sliver of sunlight on the planet, 10^17 W')
said('PF', 'all the energy that their sun emits, or 1027 watts', 'Kaku PF: Type II = 10^27 W'); said('PF', 'or about 1037 watts', 'Kaku PF: Type III = 10^37 W')
said('SH', 'Type I commands the energy striking a planet from its parent star (∼ 1016 W); Type II commands the full luminosity of its star (∼ 1026 W); Type III commands a galaxy (∼ 1037 W)',
     'Sharma 2026 (arXiv): Type I ~ 10^16 W, II ~ 10^26 W, III ~ 10^37 W, attributed to Kardashev [1964]')
said('SH', 'Nikolai S. Kardashev. Transmission of information by extraterrestrial civilizations. Soviet Astronomy, 8:217–221, 1964', 'Sharma\'s reference [Kardashev 1964] IS the paper above')
said('SH', 'Carl Sagan later refined the scale to a continuous logarithmic index K = (log10 P − 6)/10', 'Sagan\'s index as Sharma gives it: K = (log10 P - 6)/10')
said('PF', 'Carl Sagan introduced another scale, based on information processing', 'PF: the information scale is Sagan\'s')
said('PF', 'So we have to introduce yet another scale to rank civilizations', 'PF: the entropy scale is Kaku\'s addition')
said('PF', 'Freeman Dyson, in fact, once tried to find Type II civilizations in outer space by searching for objects that emit primarily infrared radiation', 'PF: Dyson searched for Type II civilizations as infrared sources')

LAD = {'Kardashev 1964': [math.log10(K_W[k]) for k in ('I', 'II', 'III')], 'Kaku, Parallel Worlds': [16, 26, 36],
       'Kaku, Physics of the Future': [17, 27, 37], 'Sharma 2026 (arXiv)': [16, 26, 37]}
print('\n      %-28s %8s %8s %8s   steps' % ('ladder', 'I', 'II', 'III'))
for k, v in LAD.items():
    print('      %-28s %8s %8s %8s   %.0f, %.0f decades' % (k, '1e%.1f' % v[0], '1e%.1f' % v[1], '1e%.1f' % v[2], v[1] - v[0], v[2] - v[1]))
check(len({tuple(round(x) for x in v) for v in LAD.values()}) == 4, 'the four ladders are four different ladders')
check(round(LAD['Kardashev 1964'][1] - LAD['Kardashev 1964'][0]) == 14 and round(LAD['Kardashev 1964'][2] - LAD['Kardashev 1964'][1]) == 11, 'Kardashev\'s steps are 14 then 11 decades; the books\' are 10 and 10, and Sharma\'s are 10 and 11')
S, R_E, L_SUN = 1361.0, 6.371e6, 3.828e26
p_planet = math.pi * R_E ** 2 * S
note('sunlight intercepted by the Earth = %.3e W (S=1361, R=6.371e6; CITED)' % p_planet)
note('Kardashev\'s Type I is 1 / %.0f of that; Kaku PW\'s is x%.0f below it; PF\'s x%.2f; Sharma\'s x%.0f' % (p_planet / K_W['I'], p_planet / 1e16, p_planet / 1e17, p_planet / 1e16))
check(p_planet / K_W['I'] > 3e4, 'Kardashev\'s Type I is more than 30,000 times below the sunlight on the planet: it is a level of technology, not a planetary energy budget')
Kidx = lambda P: (math.log10(P) - 6) / 10
note('Sagan index K = (log10 P - 6)/10: Kardashev I -> %.2f ; humanity at 2.0e13 W -> %.2f' % (Kidx(K_W['I']), Kidx(2.0e13)))
check(abs(Kidx(2.0e13) - 0.73) < 0.005, 'that index gives 0.73 for 2.0e13 W, the value Sharma prints')
check(abs(Kidx(K_W['I']) - 0.66) < 0.005, 'and 0.66 for Kardashev\'s own Type I: on Sagan\'s index his Type I sits well below 1')
r_pw, r_pf = 1e16 / K_W['I'], 1e17 / K_W['I']
note('Kaku PW Type I is x%.0f Kardashev\'s; Kaku PF Type I is x%.0f' % (r_pw, r_pf))
check(round(r_pw) == 2500 and round(r_pf) == 25000, 'the books\' Type I is 2,500 (PW) and 25,000 (PF) times Kardashev\'s Type I')
note('Whether a later grading (Sagan\'s) is where the 10^16 W ladder came from is NOT checked: it is not held [WANTED].')

# ---------------------------------------------------------------------------
head(3, 'A RUNG IS A RATE  (his 1%, and the books\' rungs)')
for g in (0.01, 0.02, 0.03):
    note('10^10 at %d%%/yr = %.0f years' % (round(100 * g), 10 * math.log(10) / math.log(1 + g)))
t1, t3 = 10 * math.log(10) / math.log(1.01), 10 * math.log(10) / math.log(1.03)
check(2300 < t1 < 2330 and 770 < t3 < 790, 'a 10^10 rung is 2,314 years at 1% and 779 at 3% (the books\' rung; ch-kaku-verify.py has the rest)')
t14 = 14 * math.log(10) / math.log(1.01)
check(3200 < t14 < 3300, 'his own first rung, 10^14 at 1%%, is %.0f years: not a 10^10 rung at any rate that gives his 3200' % t14)

# ---------------------------------------------------------------------------
head(4, 'THE TWO WASTE-HEAT SENTENCES, RECOMPUTED  (Physics of the Future; not in the 1964 paper)')
SIGMA, AU, B_WIEN = 5.670374419e-8, 1.495978707e11, 2.897771955e-3
T_shell = (L_SUN / (4 * math.pi * AU ** 2 * SIGMA)) ** 0.25; lam = B_WIEN / T_shell
note('shell at 1 AU absorbing all of L: T = %.0f K, Wien peak %.1f micrometres' % (T_shell, lam * 1e6))
check(300 < T_shell < 450 and 2e-6 < lam < 3e-5, 'the shell sits near 400 K and peaks in the infrared')
T_planet = (0.5 * L_SUN / (4 * math.pi * R_E ** 2 * SIGMA)) ** 0.25
note('Earth-sized planet, half of L as heat from the surface, no atmosphere: T = %.0f K' % T_planet)
check(T_planet > 1.0e4, 'about %.0f K, far above any rock melting point' % T_planet)
note('Constants (sigma, L_sun, AU, R_E, Wien b) are CITED reference values, not held. "Half" is the lower of two readings.')

# ---------------------------------------------------------------------------
head(5, 'THE CORPUS: WHAT ITS OWN DYSON CHAPTER SAYS')
def strip(s):
    s = re.sub(r'<!--po-(\w+)-->.*?<!--/po-\1-->', ' ', s, flags=re.S)
    s = re.sub(r'data:[^"\')\s]+', '', s)
    s = re.sub(r'<(script|style).*?</\1>', ' ', s, flags=re.S | re.I)
    return ' '.join(html.unescape(re.sub(r'<[^>]+>', ' ', s)).split())
pd = os.path.join(ROOT, 'book7', 'ch-dyson.html')
if os.path.exists(pd):
    t = strip(open(pd, encoding='utf8', errors='ignore').read())
    hits = {k: len(re.findall(k, t, re.I)) for k in ('sphere', 'infrared', 'civili[sz]ation', 'Kardashev', 'SETI', 'waste heat')}
    print('      book7/ch-dyson.html (own text) mentions: ' + ', '.join('%s x%d' % kv for kv in hits.items()))
    check(sum(hits.values()) == 0, 'the corpus\'s Freeman Dyson chapter says nothing of spheres, infrared, civilizations, Kardashev or SETI, and the 1964 paper cites Dyson\'s own paper')
else:
    print('    SKIP  book7/ch-dyson.html not present'); skips.append('dyson')

print('\n' + '=' * 72)
if skips: print('  SKIPPED (not passed, not failed): %s' % ', '.join(skips))
if fails:
    print('  %d FAIL:' % len(fails)); [print('    - ' + f) for f in fails]; sys.exit(1)
print('  all run checks passed.')
print('  Recorded as open, not checked: Dyson (1959) itself; Sagan\'s own grading and whether the 10^16 W ladder is his;')
print('  what Dyson\'s infrared search did; the exponents in the paper are DERIVED, not machine-read (superscripts).')
