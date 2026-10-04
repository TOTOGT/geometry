#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ch-rohatgi-mukherjee-verify.py -- companion to book7/ch-rohatgi-mukherjee.html.

Blocks:
 [1] each claim the page makes about the memoir, found on the memoir page the page cites (pdftotext, page by page)
 [2] the page says what the script found
 [3] dates and arithmetic
 [4] three derivations the page works (ours, not hers): Stern-Volmer quenching, dimer twist angle, van't Hoff
     classification -- each with controls that must fail
 [HONESTY] at the end

The memoir is an 18-page scan with a text layer full of recognition errors; the needles below are the ones that
survived it. Two facts were read from page images, not text: the thesis title and the 1990 medal year (see HONESTY).
Standard library only; pdftotext is needed for block [1], which prints SKIP, never PASS, if the PDF is missing.
"""
import datetime, html, math, os, re, subprocess, sys

FAIL = 0
def check(ok, msg):
    global FAIL
    print('    %s  %s' % ('PASS' if ok else 'FAIL', msg))
    if not ok: FAIL += 1
def head(n, t): print('\n' + '=' * 72 + '\n  [%s]  %s\n' % (n, t) + '=' * 72)
def norm(t): return re.sub(r'\s+', ' ', t.replace('’', "'").replace('‘', "'")).lower()

here = os.path.dirname(os.path.abspath(__file__))
page = open(os.path.join(here, 'ch-rohatgi-mukherjee.html'), encoding='utf-8').read()
ptxt = norm(html.unescape(re.sub(r'<[^>]+>', ' ', page)))

# ---------------------------------------------------------------- [1]
head(1, 'memoir pages: each needle must be on the page the chapter cites (memoir page = PDF page + 110)')
CLAIMS = [  # (needle in the memoir page text, memoir page, what the chapter says)
    ('born in a joint family', 113, 'born in a joint family'),
    ('patna', 113, 'born in Patna'),
    ('six brothers and five sisters', 113, 'six brothers and five sisters'),
    ('matriculation in the year 1939', 113, 'Matriculation 1939'),
    ('sitar', 113, 'sitar'),
    ('scottish church', 114, 'BSc at Scottish Church College'),
    ('passed msc', 114, 'MSc 1945'),
    ('1948 under professor sachindra nath mukherjee', 114, 'Jadavpur 1948, S. N. Mukherjee'),
    ('quenching by chlorinated', 114, 'quenching by chlorinated hydrocarbons (research start)'),
    ('bowen, frs at oxford in 1950', 114, 'Oxford 1950, Bowen'),
    ('dphil (oxon)', 114, 'DPhil'),
    ('sir pc roy', 114, 'Sir P. C. Roy fellowship'),
    ('smith mundt', 114, 'Fulbright / Smith-Mundt'),
    ('phase shifting', 114, 'phase shifting technique'),
    ('lumetron', 114, 'Lumetron (not glossed on the page)'),
    ('professor of chemistry in 1974', 114, 'Professor 1974'),
    ('iit, kanpur', 114, 'IIT Kanpur'),
    ('jawaharlal nehru', 114, 'JNU'),
    ('(1979-1982)', 114, 'Head 1979-82'),
    ('1990 to 1993', 114, 'INSA Senior Scientist 1990-93'),
    ('cv raman gold medal', 114, 'C. V. Raman Gold Medal'),
    ('initiated such studies', 115, 'started systematic photochemistry after Oxford'),
    ('deoxygenated', 115, 'deoxygenated solutions'),
    ('excited state electron transfer', 115, 'excited-state electron transfer'),
    ('naqvi, ware, carrol, whitten', 115, 'Naqvi, Ware, Carrol, Whitten'),
    ('singlet oxygen', 115, 'singlet oxygen'),
    ('enthalpy directed', 115, 'enthalpy-directed'),
    ('entropy directed', 115, 'entropy-directed'),
    ('dimerisation constants', 115, 'dimerisation constants'),
    ('angle of twist', 116, 'angle of twist'),
    ('anthracene sulphonates', 116, 'anthracene sulphonates'),
    ('photo electrochemical conversion', 117, 'photoelectrochemical conversion'),
    ('porphyrins in organized media', 118, 'water-soluble porphyrins in organised media'),
    ('sir george porter', 119, 'flash photolysis with Sir George Porter'),
    ('tenth international photobiology congress', 119, 'Tenth Congress, Jerusalem'),
    ('conversion and storage of chemical energy', 119, 'UGC project c. 1980'),
    ('1966-68', 120, 'summer institutes 1966-68'),
    ('indian photobiology group', 120, 'Indian Photobiology Group'),
    ('ugc national lecturer in 1980', 120, 'UGC National Lecturer 1980'),
    ('president of chemistry section of indian science', 120, 'President, Chemistry Section 1985'),
    ('first from asia', 120, 'first from Asia'),
    ('sushil kumar mukherjee', 121, 'husband'),
    ('new scientist', 122, 'reviews of the textbook'),
    ('wiley eastern', 123, 'Wiley Eastern'),
    ('31st december', 123, 'died 31 December 2009'),
    ('nagpur', 123, 'Nagpur'),
    ('offspring', 123, 'no offspring'),
    ('memory loss', 123, 'memory loss'),
    ('bowen ej', 123, 'bibliography: with Bowen'),
    ('14 146', 123, 'bibliography: Faraday Discussions 14, 146'),
]
D = next((q for q in (os.path.expanduser('~/Downloads/'), os.path.expanduser('~/mnt/Downloads/'), '/mnt/user-data/uploads/Downloads/') if os.path.isdir(q)), None)
pdf = None
if D:
    for fn in os.listdir(D):
        if fn.lower().startswith('rohatgi') and fn.lower().endswith('.pdf'):
            pdf = os.path.join(D, fn)
if pdf is None:
    print('    SKIP  memoir PDF not found in Downloads (file name starts "ROHATGI")')
else:
    pages = {}
    for p in range(1, 19):
        t = subprocess.run(['pdftotext', '-f', str(p), '-l', str(p), pdf, '-'], capture_output=True, text=True).stdout
        pages[p + 110] = norm(t)
    check('biographical memoirs' in ' '.join(pages.values()) and 'fell. insa' in ' '.join(pages.values()), 'the file is the INSA memoir (it says so), not a thesis')
    for needle, pg, what in CLAIMS:
        check(needle in pages.get(pg, ''), 'p.%d has: %s' % (pg, what))
    check('photochemistry of antluacene' in pages[123], 'p.123 lists "Photochemistry of anthracene" (OCR spelling "antluacene") with Bowen')
    check('harvard' not in ' '.join(pages.values()), 'control: a name not in the memoir (Harvard) is absent')
    check('dphil 1953' not in ' '.join(pages.values()), 'control: a wrong year ("dphil 1953") is absent')
    check('beyond' not in pages[114] and 'cambridge' not in pages[114], 'control: p.114 does not mention Cambridge')
    check('first from asia' not in pages[119], 'control: "first from Asia" is NOT on p.119 (it is on p.120)')
    check('ugc national lecturer in 1980' not in pages[114], 'control: a p.120 claim is not on p.114')

# ---------------------------------------------------------------- [2]
head(2, 'what the page says')
for n in ['2 august 1924', '31 december 2009', 'photochemistry of anthracene derivatives', 'e. j. bowen', 'p.114', 'p.115', 'p.123',
          'was not read', 'naqvi, ware, carrol', 'no priority claim', 'cot²(θ/2)', "van't hoff", '1990', 'does not assess any result',
          'faraday society discussions', 'summer institutes', 'indian photobiology']:
    check(n in ptxt or n in html.unescape(page).lower(), 'page contains: %s' % n)
check('villani' not in ptxt and 'caffarelli' not in ptxt, 'control: the page names neither Villani nor Caffarelli')
check('1991' not in re.sub(r'one search summary gave 1991[^.]*\.', '', ptxt), 'the 1991 medal year appears only where the page refutes it')
cites = sorted(set(int(x) for x in re.findall(r'p\.(\d{3})', page)))
check(cites and min(cites) >= 113 and max(cites) <= 128, 'every cited page is inside the memoir (111-128): %s' % cites)
check(not any(c < 113 for c in cites), 'control: nothing cited from the cover or photograph pages')

# ---------------------------------------------------------------- [3]
head(3, 'dates and arithmetic')
b, d = datetime.date(1924, 8, 2), datetime.date(2009, 12, 31)
yrs = d.year - b.year - ((d.month, d.day) < (b.month, b.day))
check(yrs == 85, 'born 2 Aug 1924, died 31 Dec 2009: aged %d' % yrs)
check(6 + 5 + 1 == 12, 'six brothers and five sisters plus her: twelve children')
check(1952 - 1950 == 2, 'Oxford 1950-52: two years')
check(1982 - 1979 == 3, 'Head 1979-82: three years (the memoir says three)')
check(1956 - 1954 == 2, 'Sir P. C. Roy fellowship 1954-56: two years (the memoir says two)')
check(1968 - 1966 + 1 == 3, 'summer institutes 1966-68: three consecutive years (the memoir says three)')
check(1982 - 1979 != 4, 'control: it is not four')
check(1939 < 1941 < 1943 < 1945 < 1948 < 1950 < 1952 < 1954 < 1958 < 1974 < 1984 < 1989 < 2009, 'the dates in the table are in order')
rows = re.findall(r'<tr><td>(\d{4})(?:&ndash;(\d{2,4}))?</td>', page.split('Part I &middot;')[1].split('Part II &middot;')[0])
ys = [int(r[0]) for r in rows]
check(len(ys) == 13 and ys == sorted(ys), 'path table: 13 rows in date order %s' % ys)
check(ys != sorted(ys, reverse=True), 'control: not in reverse order')

# ---------------------------------------------------------------- [4]
head(4, 'three derivations (ours, not hers); every control must fail')

# 4a Stern-Volmer: integrate A*' = -(k0 + kq Q) A*, emission ~ integral of A*
def emission(k0, kq, Q, steps=200000):
    k = k0 + kq * Q
    T = 40.0 / k
    h = T / steps
    a, tot = 1.0, 0.0
    for _ in range(steps):             # RK4 on a' = -k a
        k1 = -k * a; k2 = -k * (a + h * k1 / 2); k3 = -k * (a + h * k2 / 2); k4 = -k * (a + h * k3)
        a_new = a + h * (k1 + 2 * k2 + 2 * k3 + k4) / 6
        tot += h * (a + a_new) / 2
        a = a_new
    return tot
k0, kq = 0.5, 3.0                      # tau0 = 2: chosen so that kq*tau0 differs from kq
tau0 = 1 / k0
I0 = emission(k0, kq, 0.0)
for Q in (0.1, 0.4, 1.0):
    r = I0 / emission(k0, kq, Q)
    check(abs(r - (1 + kq * tau0 * Q)) < 1e-6, 'Q=%.1f: I0/I = %.6f = 1 + kq*tau0*Q = %.6f' % (Q, r, 1 + kq * tau0 * Q))
    check(abs(r - (1 + kq * Q)) > 1e-3, 'control: 1 + kq*Q = %.3f is NOT the law (tau0 = 2, so the slope is kq*tau0)' % (1 + kq * Q))

# 4b dimer twist angle
def bands(mu, th):
    m1 = (mu, 0.0); m2 = (mu * math.cos(th), mu * math.sin(th))
    s = ((m1[0] + m2[0]) / math.sqrt(2), (m1[1] + m2[1]) / math.sqrt(2))
    a = ((m1[0] - m2[0]) / math.sqrt(2), (m1[1] - m2[1]) / math.sqrt(2))
    return s[0] ** 2 + s[1] ** 2, a[0] ** 2 + a[1] ** 2
for deg in (20, 60, 90, 120, 160):
    th = math.radians(deg)
    fs, fa = bands(1.7, th)
    check(abs(fs + fa - 2 * 1.7 ** 2) < 1e-12, '%3d deg: intensities sum to 2*mu^2 (sum rule)' % deg)
    check(abs(fs / fa - 1 / math.tan(th / 2) ** 2) < 1e-9, '%3d deg: ratio = cot^2(theta/2)' % deg)
    check(abs(2 * math.atan(math.sqrt(fa / fs)) - th) < 1e-9, '%3d deg: theta = 2*arctan(sqrt(r)) recovers the angle' % deg)
fs0, fa0 = bands(1.0, 0.0)
check(fa0 < 1e-12 and abs(fs0 - 2.0) < 1e-12, '0 deg: all intensity in one band, none splits')
fs9, fa9 = bands(1.0, math.pi / 2)
check(abs(fs9 - fa9) < 1e-12, '90 deg: bands equal')
fs6, fa6 = bands(1.0, math.radians(60))
check(abs(fs6 / fa6 - math.tan(math.radians(60) / 2) ** 2) > 0.5, 'control: tan^2(theta/2) is the reciprocal, not the same ratio, at 60 deg')

# 4c van't Hoff and the classification
R = 8.314462618
def lnK(T, dH, dS): return -dH / (R * T) + dS / R
def fit(Ts, dH, dS, noise=0.0, seed=7):
    import random
    rnd = random.Random(seed)
    xs = [1 / T for T in Ts]; ys = [lnK(T, dH, dS) + rnd.gauss(0, noise) for T in Ts]
    n = len(xs); mx = sum(xs) / n; my = sum(ys) / n
    sl = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sum((x - mx) ** 2 for x in xs)
    ic = my - sl * mx
    return -sl * R, ic * R                      # dH, dS
def klass(dH, dS, T=298.15):
    return 'enthalpy-directed' if (-dH > T * dS and dH < 0) else ('entropy-directed' if T * dS > -dH and dS > 0 else 'neither')
Ts = [283.15, 293.15, 303.15, 313.15, 323.15]
for dH, dS, want in ((-30e3, -20.0, 'enthalpy-directed'), (2e3, 90.0, 'entropy-directed')):
    h, s = fit(Ts, dH, dS)
    check(abs(h - dH) < 1e-6 and abs(s - dS) < 1e-9, 'recovers dH=%.0f J/mol, dS=%.0f J/mol/K from K(T)' % (dH, dS))
    check(klass(h, s) == want, 'classified %s' % want)
    check(abs((h - (-R * 298.15 * lnK(298.15, h, s))) / 298.15 - s) < 1e-9, 'dS = (dH - dG)/T with dG = -RT ln K')
    check(klass(h, s) != ('entropy-directed' if want == 'enthalpy-directed' else 'enthalpy-directed'), 'control: the other label does not fit')
h, s = fit(Ts, -30e3, -20.0, noise=1.5)
check(abs(h - (-30e3)) > 2e3, 'control: with heavy noise (sd 1.5 in ln K) the fit is off by %.0f J/mol, so the check can detect a bad fit' % abs(h + 30e3))

print()
print('[HONESTY] Block [1] establishes that each claim the chapter attributes to the memoir is on the memoir page the chapter cites, in the scan text layer.')
print('[HONESTY] It does not establish that the memoir is right: it is one colleague\'s account, with no citations for the claim that the thesis held the "initial idea" of excited-state electron transfer.')
print('[HONESTY] Two facts were read from page images, not text, because the text layer garbles them: the thesis title (p.114) and the medal year 1990 (p.114).')
print('[HONESTY] Block [4] is our own physics for three quantities the memoir names. It does not reproduce her methods, numbers or conclusions; the thesis was not read.')
print('[HONESTY] The Bowen paper and the encyclopaedia entry were not read in full (access error and summary only).')
print('\n' + ('ALL CHECKS PASS' if not FAIL else '%d FAILED' % FAIL))
sys.exit(1 if FAIL else 0)
