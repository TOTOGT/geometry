#!/usr/bin/env python3
"""
Kardashev -- a scale measured by a flux, and what the books that carry it say he did.

WHY THIS FILE EXISTS. book7/ch-kaku.html found that no page of the corpus mentions
the Kardashev scale, and that Kaku's three books print its rungs differently. The
Kardashev paper itself is not held. What is held is three books that describe it
and one page of Physics of the Future that says Freeman Dyson looked for Type II
civilizations in the infrared. This script confirms what the books say about him
and the scale, recomputes the two waste-heat sentences those books make, and counts
what the corpus's own Dyson chapter says about any of it.

READS ~/Downloads: Michio-Kaku-Parallel-Worlds.pdf, Future Physics michio kaku.pdf
(Physics of the Future), physics-of-the-impossible-by-michael-kaku1.pdf. PDF pages,
not book pages. Without pdftotext or a book, that check prints SKIP, never PASS.
Standard library only.   python3 book7/ch-kardashev-verify.py
"""
import math, os, re, subprocess, sys, html

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
head(1, 'WHAT THE HELD BOOKS SAY ABOUT HIM AND THE SCALE')
BOOKS = {'PW': 'Michio-Kaku-Parallel-Worlds.pdf', 'PF': 'Future Physics michio kaku.pdf',
         'POTI': 'physics-of-the-impossible-by-michael-kaku1.pdf'}
PAGES = {}
for k, name in BOOKS.items():
    for d in ('~/Downloads', '~/mnt/Downloads'):
        p = os.path.join(os.path.expanduser(d), name)
        if os.path.exists(p):
            try:
                txt = subprocess.run(['pdftotext', '-layout', p, '-'], capture_output=True, text=True, check=True).stdout
                PAGES[k] = [squeeze(pg) for pg in txt.split('\f')]
            except Exception as e:
                print('    SKIP  %s: pdftotext unavailable (%s)' % (name, e.__class__.__name__))
            break
    else:
        print('    SKIP  %s not found in ~/Downloads' % name)
    if k not in PAGES: skips.append(k)

def said(key, needle, msg):
    if key not in PAGES:
        print('    SKIP  [%s] %s' % (key, msg)); return
    n = squeeze(needle)
    pgs = [i + 1 for i, pg in enumerate(PAGES[key]) if n in pg]
    check(bool(pgs), '[%s pdf p.%s] %s' % (key, ','.join(map(str, pgs[:3])) or '-', msg))

said('PW', 'The ranking was introduced by Russian physicist Nikolai Kardashev in the 1960s for classifying the radio signals from possible civilizations in outer space', 'introduced in the 1960s to classify radio signals from possible civilizations (PW)')
said('PW', 'Each civilization type emits a characteristic form of radiation that can be measured and cataloged', 'each type emits a characteristic radiation that can be measured')
said('PW', 'any advanced civilization will create entropy in the form of waste heat that will inevitably drift into outer space', 'waste heat cannot be hidden (second law)')
said('PW', 'Kardashev wrote down the original classification in the 1960s, before the explosion in computer miniaturization', 'PW dates the classification before miniaturization, and adds information and entropy scales itself')
said('PF', 'first introduced in 1964 by Russian astrophysicist Nikolai Kardashev', 'introduced in 1964 (PF)')
said('PF', 'he introduced a quantitative scale to guide the work of astronomers', 'a quantitative scale to guide astronomers')
said('PF', 'there was one thing they all had to obey: the laws of physics', 'his reason: the one thing every civilization must obey is physics')
said('PF', 'The Kardashev classification was introduced in the 1960s, when physicists were concerned about energy production', 'PF: introduced when physicists were concerned about energy production')
said('PF', 'Freeman Dyson, in fact, once tried to find Type II civilizations in outer space by searching for objects that emit primarily infrared radiation', 'PF: Dyson searched for Type II civilizations as infrared sources')
said('PF', '(None, however, were found.)', 'PF: none were found')
said('POTI', 'has conjectured that the stages in the development of extraterrestrial civilizations in the universe could also be ranked by energy consumption', 'POTI: conjectured that stages could be ranked by energy consumption')
said('PF', 'Carl Sagan introduced another scale, based on information processing', 'the information scale is Sagan\'s, per PF, not Kardashev\'s')
said('PF', 'So we have to introduce yet another scale to rank civilizations', 'the entropy scale is Kaku\'s addition, per PF')

# ---------------------------------------------------------------------------
head(2, 'A SCALE MEASURED BY ONE FLUX: HOW FAST A RUNG COMES')
for g in (0.01, 0.02, 0.03):
    note('10^10 at %d%%/yr = %.0f years per rung' % (round(100 * g), 10 * math.log(10) / math.log(1 + g)))
t1, t3 = 10 * math.log(10) / math.log(1.01), 10 * math.log(10) / math.log(1.03)
check(2300 < t1 < 2330 and 770 < t3 < 790, 'a rung of 10^10 is 2,314 years at 1% and 779 at 3%: the rate, not the scale, sets the time (numbers recorded in ch-kaku-verify.py)')
check(all(abs((b - a) - 10) < 1e-12 for a, b in zip((16, 26), (26, 36))) and all(abs((b - a) - 10) < 1e-12 for a, b in zip((17, 27), (27, 37))), 'both printed ladders step by exactly 10 in log10(W)')

# ---------------------------------------------------------------------------
head(3, 'THE TWO WASTE-HEAT SENTENCES, RECOMPUTED')
SIGMA, L_SUN, AU, R_E, B_WIEN = 5.670374419e-8, 3.828e26, 1.495978707e11, 6.371e6, 2.897771955e-3   # CITED reference values, not held
print('  3a. A shell that absorbs all of the Sun\'s output at 1 AU and radiates it from its outer surface:')
T_shell = (L_SUN / (4 * math.pi * AU ** 2 * SIGMA)) ** 0.25
lam = B_WIEN / T_shell
note('T = (L / 4 pi r^2 sigma)^(1/4) = %.0f K ; Wien peak = %.1f micrometres' % (T_shell, lam * 1e6))
check(300 < T_shell < 450, 'the shell sits near 400 K, not at visible-light temperatures (PF: Type II "would glow with infrared radiation")')
check(2e-6 < lam < 3e-5, 'its blackbody peak is in the infrared, %.1f micrometres' % (lam * 1e6))
print('  3b. An Earth-sized planet running a Type II civilization (all of L), half of it as waste heat,')
print('      radiated from the planet\'s surface:')
T_planet = (0.5 * L_SUN / (4 * math.pi * R_E ** 2 * SIGMA)) ** 0.25
note('T = %.0f K' % T_planet)
check(T_planet > 1.0e4, 'about %.0f K, which is far above any rock melting point (PF: "the temperature of the planet will rise until it melts")' % T_planet)
note('Assumptions stated: L = 3.828e26 W, Earth radius 6.371e6 m, half of L as heat, radiated from the surface, no atmosphere.')
note('PF says "half the waste it produces is in the form of heat"; the reading "half of L" is mine and is the lower of the two readings.')

# ---------------------------------------------------------------------------
head(4, 'THE CORPUS: WHAT ITS OWN DYSON CHAPTER SAYS OF ANY OF THIS')
def strip(s):
    s = re.sub(r'<!--po-(\w+)-->.*?<!--/po-\1-->', ' ', s, flags=re.S)   # generated boxes (cross-links, stamps) are not the chapter's own text
    s = re.sub(r'data:[^"\')\s]+', '', s)
    s = re.sub(r'<(script|style).*?</\1>', ' ', s, flags=re.S | re.I)
    return ' '.join(html.unescape(re.sub(r'<[^>]+>', ' ', s)).split())
p = os.path.join(ROOT, 'book7', 'ch-dyson.html')
if os.path.exists(p):
    t = strip(open(p, encoding='utf8', errors='ignore').read())
    hits = {k: len(re.findall(k, t, re.I)) for k in ('sphere', 'infrared', 'civili[sz]ation', 'Kardashev', 'SETI', 'waste heat')}
    print('      book7/ch-dyson.html mentions: ' + ', '.join('%s x%d' % kv for kv in hits.items()))
    check(sum(hits.values()) == 0, 'the corpus\'s Freeman Dyson chapter says nothing of Dyson spheres, infrared searches, civilizations or Kardashev')
else:
    print('    SKIP  book7/ch-dyson.html not present'); skips.append('dyson')

print('\n' + '=' * 72)
if skips: print('  SKIPPED (not passed, not failed): %s' % ', '.join(skips))
if fails:
    print('  %d FAIL:' % len(fails)); [print('    - ' + f) for f in fails]; sys.exit(1)
print('  all run checks passed.')
print('  Recorded as open, not checked: Kardashev\'s own 1964 paper (WANTED, not held); Sagan\'s grading (WANTED);')
print('  what Dyson\'s infrared search actually did (WANTED); dates and editions of the books.')
