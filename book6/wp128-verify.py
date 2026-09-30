#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""wp128-verify.py -- producing script for book6/wp128-the-population-employment-gap.html (WP-128).

  [1] the FRED series and the identity PEG = 100 - EMRATIO
  [2] the table on the page: August 2026, pinned; a later FRED revision makes this FAIL
  [3] what the gap is made of, exactly, and what moved it between two dates
  [4] the corpus: every page tagged ECONOMICS in docs/subjects.tsv at a pinned commit, and how
      many times each says unemployment / employment / labour-force words. The page's
      cross-reference table is checked against this count.
  [5] the page prints what this script computes

Prints SKIP, never PASS, when FRED, the pinned commit or the page is missing.
`--emit FILE` writes the computed numbers and table rows as JSON (used to build the page).
Not computed, recorded OPEN: the split by BLS 'not employed, by reason'; an Okun's-law conversion.
"""
import sys, os, re, csv, io, json, html, subprocess, urllib.request
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASELINE = '13655f5'
PAGE = 'book6/wp128-the-population-employment-gap.html'
fails, skips = [], []
def check(ok, msg, detail=''):
    print('    %s  %s%s' % ('PASS' if ok else 'FAIL', msg, ('  -- ' + detail) if detail and not ok else ''))
    if not ok: fails.append(msg)
def note(s): print('          ' + s)
def head(n, t): print('\n' + '=' * 72 + '\n  [%s]  %s\n' % (n, t) + '=' * 72)
OUT = {}

PIN = dict(date='2026-08-01', CNP16OV=275415, CE16OV=162746, CLF16OV=169777, UNEMPLOY=7031, EMRATIO=59.1, UNRATE=4.1, U6RATE=7.7)
def fred(sid):
    raw = urllib.request.urlopen('https://fred.stlouisfed.org/graph/fredgraph.csv?id=' + sid, timeout=40).read().decode('utf-8')
    return {d: float(v) for d, v in list(csv.reader(io.StringIO(raw)))[1:] if v not in ('', '.')}

head(1, 'THE SERIES   (FRED, retrieved live)')
S = {}
try:
    for sid in ('CNP16OV', 'CE16OV', 'CLF16OV', 'UNEMPLOY', 'EMRATIO', 'UNRATE', 'U6RATE'):
        S[sid] = fred(sid); last = max(S[sid])
        print('    %-9s %5d obs   %s .. %s   latest = %s' % (sid, len(S[sid]), min(S[sid]), last, S[sid][last]))
except Exception as e:
    print('    SKIP  FRED not reachable (%s)' % e.__class__.__name__); skips.append('fred'); S = {}

if S:
    common = sorted(set.intersection(*[set(S[k]) for k in S if k != 'U6RATE']))      # U-6 starts in 1994; PEG does not need it
    peg = lambda d: (S['CNP16OV'][d] - S['CE16OV'][d]) / S['CNP16OV'][d] * 100
    parts = lambda d: ((S['CNP16OV'][d] - S['CLF16OV'][d]) / S['CNP16OV'][d] * 100, S['UNEMPLOY'][d] / S['CNP16OV'][d] * 100)
    head(2, 'THE IDENTITY AND THE PAGE\'S TABLE')
    worst = max(abs(peg(d) - (100 - S['EMRATIO'][d])) for d in common)
    check(len(common) == 943, 'the page says "all 943 months since January 1948": %d months from %s' % (len(common), common[0]))
    check(worst < 0.051, 'PEG equals 100 - EMRATIO on all %d months with the series it needs (largest gap %.4f; EMRATIO is published to 0.1)' % (len(common), worst))
    w3 = max(abs(S['UNEMPLOY'][d] / S['CLF16OV'][d] * 100 - S['UNRATE'][d]) for d in common)
    check(w3 < 0.051, 'U-3 recomputed as UNEMPLOY / CLF16OV equals UNRATE on every month (largest gap %.4f)' % w3)
    d = PIN['date']
    if d not in common:
        print('    SKIP  %s not in the retrieved series' % d); skips.append('pin')
    else:
        same = all(S[k][d] == PIN[k] for k in ('CNP16OV', 'CE16OV', 'CLF16OV', 'UNEMPLOY', 'EMRATIO', 'UNRATE'))
        same = same and S['U6RATE'][d] == PIN['U6RATE']
        check(same, 'August 2026 observations are the pinned ones (population, employment, labour force, unemployed, EMRATIO, U-3, U-6)',
              'live differs: ' + ', '.join('%s %s' % (k, S[k][d]) for k in PIN if k != 'date' and S[k][d] != PIN[k]))
        check(abs(peg(d) - 40.91) < 0.005, 'PEG for August 2026 = %.4f -> 40.91%%' % peg(d))
        OUT['aug'] = dict(peg=round(peg(d), 2), u3=S['UNRATE'][d], u6=S['U6RATE'][d], em=S['EMRATIO'][d])
    last = common[-1]
    print('      latest month: %s  PEG %.2f%%  U-3 %.1f%%  U-6 %s' % (last, peg(last), S['UNRATE'][last], S['U6RATE'].get(last, 'n/a')))
    OUT['latest'] = dict(date=last, peg=round(peg(last), 2))

    head(3, 'WHAT THE GAP IS MADE OF, AND WHAT MOVED IT')
    olf, un = parts(PIN['date'])
    check(abs(olf + un - peg(PIN['date'])) < 1e-9, 'PEG = (outside the labour force + unemployed) / population, exactly: employment = labour force - unemployed')
    print('      Aug 2026: outside labour force %.2f%% + unemployed %.2f%% = %.2f%%; unemployed = %.1f%% of the gap' % (olf, un, olf + un, un / peg(PIN['date']) * 100))
    OUT['comp'] = dict(olf=round(olf, 2), un=round(un, 2), share=round(un / peg(PIN['date']) * 100, 1))
    check(un / peg(PIN['date']) < 0.10, 'the unemployed are under a tenth of the gap')
    rows = []
    for dd in ('1948-01-01', '1960-01-01', '1970-01-01', '1980-01-01', '1990-01-01', '2000-01-01', '2010-01-01', '2019-12-01', '2020-04-01', '2026-08-01'):
        if dd in common:
            o, u = parts(dd); rows.append(dict(date=dd, peg=round(peg(dd), 2), olf=round(o, 2), un=round(u, 2), u3=S['UNRATE'][dd], u6=S['U6RATE'].get(dd)))
            print('      %s  PEG %5.2f  = outside LF %5.2f + unemployed %4.2f   U-3 %4.1f   U-6 %s' % (dd, peg(dd), o, u, S['UNRATE'][dd], ('%4.1f' % S['U6RATE'][dd]) if dd in S['U6RATE'] else '  n/a'))
    OUT['hist'] = rows
    lo = min(common, key=peg); hi = max(common, key=peg)
    print('      lowest  %s %.2f   highest %s %.2f   (over %s .. %s)' % (lo, peg(lo), hi, peg(hi), common[0], common[-1]))
    OUT['range'] = dict(lo=lo, lov=round(peg(lo), 2), hi=hi, hiv=round(peg(hi), 2), first=common[0], last=common[-1])
    a, b = '2000-01-01', '2026-08-01'
    oa, ua = parts(a); ob, ub = parts(b)
    dpeg, dolf, dun = peg(b) - peg(a), ob - oa, ub - ua
    print('      %s -> %s: PEG %+.2f points = outside LF %+.2f + unemployed %+.2f' % (a, b, dpeg, dolf, dun))
    check(abs(dolf + dun - dpeg) < 1e-9, 'the change in PEG splits exactly into the two parts')
    check(abs(dolf) > abs(dun), 'between January 2000 and August 2026 the outside-the-labour-force part moved more than the unemployed part')
    OUT['delta'] = dict(dpeg=round(dpeg, 2), dolf=round(dolf, 2), dun=round(dun, 2))
    note('That block contains retirees, students, people unable to work and people who want a job but are not counted; the split by reason is NOT computed (OPEN).')

head(4, 'THE CORPUS: PAGES TAGGED ECONOMICS   (pinned to %s)' % BASELINE)
def git(*a):
    return subprocess.run(['git', '-C', ROOT] + list(a), capture_output=True, text=True, errors='ignore')
def strip(s):
    s = re.sub(r'<!--po-(run|gss|related|subject)-->.*?<!--/po-\1-->|<!--po-(run|gss|related)-->.*?</aside>', ' ', s, flags=re.S)
    s = re.sub(r'data:[^"\')\s]+', '', s); s = re.sub(r'<(script|style).*?</\1>', ' ', s, flags=re.S | re.I)
    return html.unescape(re.sub(r'<[^>]+>', ' ', s))
UN = re.compile(r'unemploy', re.I)
EMP = re.compile(r'\bU-?[36]\b|employment|labou?r[ -]force|jobless|labou?r market|payroll|\bjobs\b', re.I)
r = git('show', '%s:docs/subjects.tsv' % BASELINE)
ECON = []
if r.returncode != 0:
    print('    SKIP  %s not in this checkout' % BASELINE); skips.append('baseline')
else:
    for line in r.stdout.splitlines():
        f = line.split('\t')
        if len(f) >= 4 and not f[0].startswith('#') and ('ECONOMICS' in f[1] or 'ECONOMICS' in f[2]):
            t = git('show', '%s:%s' % (BASELINE, f[0]))
            if t.returncode != 0: continue
            txt = strip(t.stdout)
            ECON.append(dict(path=f[0], subj=' / '.join(x for x in (f[1], f[2]) if x), title=re.sub(r'\s+', ' ', f[3]).strip(), un=len(UN.findall(txt)), emp=len(EMP.findall(txt))))
    ECON.sort(key=lambda e: (-e['un'], -e['emp'], e['path']))
    print('    %d pages tagged ECONOMICS at %s' % (len(ECON), BASELINE))
    for e in ECON: print('      %-58s unemployment x%-3d  employment-words x%-3d' % (e['path'], e['un'], e['emp']))
    check(len(ECON) >= 30, 'the ECONOMICS tag reaches %d pages' % len(ECON))
    check(any(e['path'] == 'book6/wp32-forced-urgency-gap.html' and e['un'] > 0 for e in ECON), 'WP-32, whose section 5 uses unemployment as an urgency proxy, says "unemployment" in its text')
    zero = [e['path'] for e in ECON if e['un'] == 0]
    said = sorted(e['path'] for e in ECON if e['un'] > 0)
    check(said == ['book6/wp32-forced-urgency-gap.html', 'book6/wp64-the-recorder.html'], 'the only pages that say "unemployment" are WP-32 and WP-64 (the page says so)', str(said))
    check(len(zero) == 35, '35 of the pages never say "unemployment" (the page says 35)', str(len(zero)))
    print('      %d of %d never say "unemployment"' % (len(zero), len(ECON)))
    OUT['econ'] = ECON

head(5, 'THE PAGE PRINTS WHAT THIS SCRIPT COMPUTES')
def sq(s): return re.sub(r'\s+', '', html.unescape(re.sub(r'<[^>]+>', ' ', s)).lower())
cur = None
try: raw = open(os.path.join(ROOT, PAGE), encoding='utf-8').read(); cur = sq(raw)
except OSError: print('    SKIP  %s not found (not yet written)' % PAGE); skips.append('page')
if cur is not None and 'aug' in OUT:
    a_ = OUT['aug']; c_ = OUT['comp']; d_ = OUT['delta']
    for needle, msg in (('%.2f%%' % a_['peg'], 'PEG for Aug 2026'), ('%.2f%%' % c_['olf'], 'outside the labour force'), ('%.2f%%' % c_['un'], 'unemployed'),
                        ('%.1f%%ofthegap' % c_['share'], 'the unemployed share of the gap'), ('%+.2f' % d_['dpeg'], 'change since Jan 2000'), ('wp128-verify.py', 'names its producing script')):
        check(needle.lower().replace(' ', '') in cur, 'page prints %s: %s' % (msg, needle))
    miss = [e['path'] for e in OUT.get('econ', []) if os.path.basename(e['path']) not in raw]
    check(not miss, 'the page links every one of the %d ECONOMICS-tagged pages' % len(OUT.get('econ', [])), 'missing: ' + ', '.join(miss[:6]))
    bad = []
    for e in OUT.get('econ', []):
        m = re.search(r'href="[^"]*%s"[^>]*>.*?</a></td>\s*<td[^>]*>[^<]*</td>\s*<td[^>]*>(\d+)</td>\s*<td[^>]*>(\d+)</td>' % re.escape(os.path.basename(e['path'])), raw, re.S)
        if not m or (int(m.group(1)), int(m.group(2))) != (e['un'], e['emp']): bad.append(e['path'])
    check(not bad, "each row's two counts equal the script's count", ', '.join(bad[:5]))

if '--emit' in sys.argv:
    json.dump(OUT, open(sys.argv[sys.argv.index('--emit') + 1], 'w'), indent=1)
print('\n' + '=' * 72)
if skips: print('  SKIPPED (not passed, not failed): %s' % ', '.join(skips))
if fails:
    print('  %d FAIL:' % len(fails)); [print('    - ' + f) for f in fails]; sys.exit(1)
print('  all run checks passed.')
print("  Recorded as open, not checked: the split of the outside-the-labour-force block by BLS reason; an Okun's-law foregone-output figure;")
print('  the ShadowStats status (author\'s statement, not confirmed here) and its ~23% June 2016 figure (no held source).')
