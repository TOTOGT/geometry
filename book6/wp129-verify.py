#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""wp129-verify.py -- producing script for book6/wp129-wages-against-prices.html (WP-129).

The author's position (a normative claim, not derived here): wages ought to be pegged to inflation
AHEAD of it, not behind it, as, the author says, has historically been the case. This script tests
only the measurable half -- what the record says about wages and prices -- and computes what a
'behind' peg costs and what an 'ahead' peg would need to know.

  [1] the series (FRED): AHETPI average hourly earnings, production and nonsupervisory (1964-);
      CES0500000003 all private employees (2006-) as a robustness check; CPIAUCSL (1947-)
  [2] the real wage: level at chosen dates, net change, and every fall of 3% or more from a peak
  [3] how often wage growth was below inflation, by decade
  [4] lead and lag: which series moves first, by window
  [5] what a peg to TRAILING inflation misses: next-12-month inflation minus trailing (the acceleration)
  [6] the corpus: ECONOMICS-tagged pages, and how often each says wage words (pinned commit)
  [7] the page prints what this script computes

Prints SKIP, never PASS, when FRED, the pinned commit or the page is missing. `--emit FILE` writes JSON.
Not computed, recorded OPEN: what indexation does to inflation itself; productivity; the composition
of who is in the wage series after April 2020; a forecast-based 'ahead' peg (only a naive one is scored).
"""
import sys, os, re, csv, io, json, html, subprocess, urllib.request, statistics as st, math
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASELINE = '7021606'
PAGE = 'book6/wp129-wages-against-prices.html'
fails, skips = [], []
def check(ok, msg, detail=''):
    print('    %s  %s%s' % ('PASS' if ok else 'FAIL', msg, ('  -- ' + detail) if detail and not ok else ''))
    if not ok: fails.append(msg)
def note(s): print('          ' + s)
def head(n, t): print('\n' + '=' * 72 + '\n  [%s]  %s\n' % (n, t) + '=' * 72)
OUT = {}
def fred(sid):
    raw = urllib.request.urlopen('https://fred.stlouisfed.org/graph/fredgraph.csv?id=' + sid, timeout=40).read().decode('utf-8')
    return {d: float(v) for d, v in list(csv.reader(io.StringIO(raw)))[1:] if v not in ('', '.')}
def mon(d): return ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'][int(d[5:7]) - 1] + ' ' + d[:4]

head(1, 'THE SERIES   (FRED, retrieved live)')
W = P = W2 = None
try:
    W = fred('AHETPI'); P = fred('CPIAUCSL'); W2 = fred('CES0500000003')
    for n, s in (('AHETPI', W), ('CPIAUCSL', P), ('CES0500000003', W2)): print('    %-14s %5d obs  %s .. %s  latest %s' % (n, len(s), min(s), max(s), s[max(s)]))
except Exception as e:
    print('    SKIP  FRED not reachable (%s)' % e.__class__.__name__); skips.append('fred')

if W:
    ds = sorted(set(W) & set(P)); real = {d: W[d] / P[d] for d in ds}; b = real[ds[0]]
    yoy = lambda X, dl: {dl[i]: (X[dl[i]] / X[dl[i - 12]] - 1) * 100 for i in range(12, len(dl))}
    wg, pg = yoy(W, ds), yoy(P, ds); dd = sorted(wg)
    OUT['span'] = dict(first=ds[0], last=ds[-1], n=len(ds))
    check(len(ds) == 751 and ds[0] == '1964-01-01', 'wages and prices overlap for %d months from %s (the page says 751 from January 1964)' % (len(ds), ds[0]))

    head(2, 'THE REAL WAGE   (average hourly earnings / CPI, January 1964 = 100)')
    rows = []
    for y in ('1964-01-01', '1973-01-01', '1979-01-01', '1990-01-01', '2000-01-01', '2010-01-01', '2019-12-01', '2022-06-01', '2026-08-01'):
        rows.append((y, round(real[y] / b * 100, 1))); print('      %s  %6.1f' % (y, real[y] / b * 100))
    OUT['real'] = rows
    net = real[ds[-1]] / b * 100 - 100
    yrs = (len(ds) - 1) / 12
    print('      net change %s -> %s: %+.1f%%  (%.2f%% a year over %.1f years)' % (ds[0], ds[-1], net, ((real[ds[-1]] / b) ** (1 / yrs) - 1) * 100, yrs))
    OUT['net'] = dict(net=round(net, 1), pa=round(((real[ds[-1]] / b) ** (1 / yrs) - 1) * 100, 2), yrs=round(yrs, 1))
    check(net > 0, 'over the whole record the real wage is higher, not lower: %+.1f%%' % net)
    # drawdowns of at least 3% from a running peak
    dds, peak, pk_d, cur = [], -1, None, None
    for d in ds:
        if real[d] > peak:
            if cur and cur['depth'] >= 3.0: dds.append(cur)
            peak, pk_d, cur = real[d], d, None
        else:
            dep = (peak / real[d] - 1) * 100
            if cur is None: cur = dict(peak=pk_d, trough=d, depth=dep, rec=None)
            if dep > cur['depth']: cur['trough'], cur['depth'] = d, dep
    if cur and cur['depth'] >= 3.0: dds.append(cur)
    for x in dds:
        after = [d for d in ds if d > x['trough'] and real[d] >= real[x['peak']]]
        x['rec'] = after[0] if after else None
        x['months'] = (ds.index(x['rec']) - ds.index(x['peak'])) if x['rec'] else None
        x['depth'] = round(x['depth'], 1)
        print('      fall from %s to %s: %.1f%% (a nominal raise of that size restores the peak); back at peak: %s (%s months after the peak)' % (mon(x['peak']), mon(x['trough']), x['depth'], mon(x['rec']) if x['rec'] else 'not yet', x['months'] if x['months'] else '-'))
    OUT['dd'] = dds
    check(len(dds) >= 2, 'there are %d falls of 3%% or more from a peak: wages did fall behind prices, in episodes' % len(dds))
    big = max(dds, key=lambda x: x['depth'])
    check(21 < (ds.index(big['trough']) - ds.index(big['peak'])) / 12 < 23 and big['months'] == 567, 'the page says 22 years to the trough and 567 months to regain the peak (%d, %s)' % (ds.index(big['trough']) - ds.index(big['peak']), big['months']))
    check(big['peak'] < '1980' and big['depth'] > 10, 'the deepest is %s to %s, %.1f%%: the 1970s-80s, not the recent surge' % (mon(big['peak']), mon(big['trough']), big['depth']))
    if W2:
        d2 = sorted(set(W2) & set(P)); r2 = {d: W2[d] / P[d] for d in d2}
        n2 = (r2[d2[-1]] / r2[d2[0]] - 1) * 100
        print('      robustness, all private employees %s -> %s: real wage %+.1f%%; same months in the main series %+.1f%%' % (d2[0], d2[-1], n2, (real[d2[-1]] / real[d2[0]] - 1) * 100))
        OUT['robust'] = dict(first=d2[0], all=round(n2, 1), main=round((real[d2[-1]] / real[d2[0]] - 1) * 100, 1))
        check(n2 > 0, 'the broader all-employee series also ends above where it started since %s' % d2[0])

    head(3, 'HOW OFTEN WAGE GROWTH WAS BELOW INFLATION   (12-month, same month)')
    neg = [d for d in dd if wg[d] < pg[d]]
    print('      all: %d of %d months (%.1f%%)' % (len(neg), len(dd), len(neg) / len(dd) * 100))
    OUT['below'] = dict(n=len(neg), of=len(dd), pct=round(len(neg) / len(dd) * 100, 1), dec=[])
    for dec in range(1960, 2030, 10):
        S = [d for d in dd if dec <= int(d[:4]) < dec + 10]
        if S:
            k = sum(1 for d in S if wg[d] < pg[d]); print('      %ds: %d of %d (%.0f%%)' % (dec, k, len(S), k / len(S) * 100)); OUT['below']['dec'].append((dec, k, len(S)))
    dm = {d0: k / n for d0, k, n in OUT['below']['dec']}
    check(dm[1960] == 0 and round(dm[1980] * 100) == 78 and round(dm[2010] * 100) == 22, 'the page\'s sentence: none of the 1960s, 78% of the 1980s, 22% of the 2010s')
    check(0.35 < len(neg) / len(dd) < 0.45, 'wage growth was below inflation in %.0f%% of months: behind in a large minority, not most' % (len(neg) / len(dd) * 100))

    head(4, 'WHICH MOVES FIRST   (corr of 12-month wage growth at t with 12-month inflation at t+k)')
    idx = {d: i for i, d in enumerate(dd)}
    def cc(lo, hi, k):
        xs, ys = [], []
        for d in dd:
            if not (lo <= d[:4] < hi): continue
            j = idx[d] + k
            if 0 <= j < len(dd) and lo <= dd[j][:4] < hi: xs.append(wg[d]); ys.append(pg[dd[j]])
        ma, mb = st.mean(xs), st.mean(ys)
        return sum((x - ma) * (y - mb) for x, y in zip(xs, ys)) / math.sqrt(sum((x - ma) ** 2 for x in xs) * sum((y - mb) ** 2 for y in ys))
    OUT['lag'] = {}
    for lab, lo, hi in (('1965-1984', '1965', '1985'), ('1985-2019', '1985', '2020'), ('2020 on', '2020', '2100')):
        res = [(k, cc(lo, hi, k)) for k in range(-24, 25)]
        bk, bv = max(res, key=lambda t: t[1])
        print('      %-10s best k = %+3d months (r=%.2f);  r at -12: %.2f, 0: %.2f, +12: %.2f' % (lab, bk, bv, cc(lo, hi, -12), cc(lo, hi, 0), cc(lo, hi, 12)))
        OUT['lag'][lab] = dict(k=bk, r=round(bv, 2), m12=round(cc(lo, hi, -12), 2), z=round(cc(lo, hi, 0), 2), p12=round(cc(lo, hi, 12), 2))
    note('k < 0: inflation at t+k came BEFORE wages at t (wages follow prices); k > 0: prices follow wages.')
    check(OUT['lag']['1985-2019']['k'] < 0, 'from 1985 to 2019 the best fit has inflation leading wages (k = %+d months): wages follow prices' % OUT['lag']['1985-2019']['k'])
    note('before 1985 the best k is %+d (printed, no direction claimed)' % OUT['lag']['1965-1984']['k'])
    note('Correlation of two persistent series at nearby lags is nearly flat; the best lag is a weak statement. It is reported, not leaned on.')

    head(5, 'WHAT A PEG TO TRAILING INFLATION MISSES')
    acc = {d: pg[dd[idx[d] + 12]] - pg[d] for d in dd if idx[d] + 12 < len(dd)}
    a = sorted(acc.values()); n = len(a)
    print('      acceleration = inflation over the next 12 months minus the last 12 months, %d months' % n)
    print('      share of months > 0: %.0f%%   median %+.2f   90th pct %+.2f   max %+.2f (%s)   min %+.2f' % (sum(1 for x in a if x > 0) / n * 100, a[n // 2], a[int(n * .9)], a[-1], mon(max(acc, key=acc.get)), a[0]))
    OUT['acc'] = dict(share=round(sum(1 for x in a if x > 0) / n * 100), med=round(a[n // 2], 2), p90=round(a[int(n * .9)], 2), mx=round(a[-1], 2), mxd=max(acc, key=acc.get), mn=round(a[0], 2), n=n)
    check(abs(sum(a) / n) < 0.3, 'on average the miss nets out (mean %+.2f points): a trailing peg is not biased, it is late' % (sum(a) / n))
    check(a[-1] > 3, 'in the worst month a trailing peg would have been short by %.1f points over the next year (%s)' % (a[-1], mon(max(acc, key=acc.get))))
    def q(v, f): v = sorted(v); return v[min(len(v) - 1, int(len(v) * f))]
    OUT['band'] = {}
    for lab, lo, hi in (('all', '0', '9'), ('1965-1984', '1965', '1985'), ('1985-2019', '1985', '2020'), ('2020 on', '2020', '9')):
        v = [x for d, x in acc.items() if lo <= d[:4] < hi]
        OUT['band'][lab] = dict(n=len(v), p05=round(q(v, .05), 2), p50=round(q(v, .50), 2), p95=round(q(v, .95), 2), lo=round(min(v), 2), hi=round(max(v), 2))
        b_ = OUT['band'][lab]; print('      %-10s n=%3d  5th %+.2f  median %+.2f  95th %+.2f   (min %+.2f, max %+.2f)' % (lab, b_['n'], b_['p05'], b_['p50'], b_['p95'], b_['lo'], b_['hi']))
    w1 = OUT['band']['1985-2019']['p95'] - OUT['band']['1985-2019']['p05']; w0 = OUT['band']['1965-1984']['p95'] - OUT['band']['1965-1984']['p05']; w2 = OUT['band']['2020 on']['p95'] - OUT['band']['2020 on']['p05']
    check(0.45 < w1 / w0 < 0.65 and w2 > w1, 'the page says about half as wide from 1985 to 2019 as before 1985 (ratio %.2f) and wider again from 2020 (%.2f vs %.2f)' % (w1 / w0, w2, w1))
    check(OUT['band']['1985-2019']['p95'] - OUT['band']['1985-2019']['p05'] < OUT['band']['1965-1984']['p95'] - OUT['band']['1965-1984']['p05'], 'the 5th-95th band is narrower from 1985 to 2019 than before 1985: how much "you never know" is worth depends on the regime')
    print('      ROLLING REAL-WAGE CHANGE over a horizon (overlapping windows; the count of independent ones is about 62.5 / horizon)')
    OUT['roll'] = {}
    for h in (1, 5, 10, 20):
        v = [(real[ds[i + 12 * h]] / real[ds[i]] - 1) * 100 for i in range(len(ds) - 12 * h)]
        OUT['roll'][h] = dict(n=len(v), ind=int((len(ds) / 12) // h), neg=round(sum(1 for x in v if x < 0) / len(v) * 100), p10=round(q(v, .10), 1), p50=round(q(v, .50), 1), p90=round(q(v, .90), 1), lo=round(min(v), 1), hi=round(max(v), 1))
        r_ = OUT['roll'][h]; print('      %2d yr: %3d windows (~%d independent)  negative in %d%%   10th %+.1f%%  median %+.1f%%  90th %+.1f%%   worst %+.1f%%  best %+.1f%%' % (h, r_['n'], r_['ind'], r_['neg'], r_['p10'], r_['p50'], r_['p90'], r_['lo'], r_['hi']))
    check(OUT['roll'][20]['lo'] < 0 < OUT['roll'][20]['hi'], 'even over 20 years the real wage has both fallen (%+.1f%%) and risen (%+.1f%%): the record bounds the outcomes without removing the risk' % (OUT['roll'][20]['lo'], OUT['roll'][20]['hi']))
    note('Overlapping windows are not independent draws, one country and one series, so these are the record\'s range, not probabilities to plan on.')
    note('A peg AHEAD of prices needs a forecast; scoring one is not done here. The trailing peg is the naive forecast, and its error is the acceleration above.')

head(6, 'THE CORPUS: PAGES TAGGED ECONOMICS   (pinned to %s)' % BASELINE)
def git(*a): return subprocess.run(['git', '-C', ROOT] + list(a), capture_output=True, text=True, errors='ignore')
def strip(s):
    s = re.sub(r'<!--po-(run|gss|related|subject)-->.*?<!--/po-\1-->|<!--po-(run|gss|related)-->.*?</aside>', ' ', s, flags=re.S)
    s = re.sub(r'data:[^"\')\s]+', '', s); s = re.sub(r'<(script|style).*?</\1>', ' ', s, flags=re.S | re.I)
    return html.unescape(re.sub(r'<[^>]+>', ' ', s))
WAGE = re.compile(r'\bwages?\b|real wage|indexation|\bCOLA\b|cost[- ]of[- ]living|minimum wage', re.I)
r = git('show', '%s:docs/subjects.tsv' % BASELINE); ECON = []
if r.returncode != 0: print('    SKIP  %s not in this checkout' % BASELINE); skips.append('baseline')
else:
    for line in r.stdout.splitlines():
        f = line.split('\t')
        if len(f) >= 4 and not f[0].startswith('#') and ('ECONOMICS' in f[1] or 'ECONOMICS' in f[2]):
            t = git('show', '%s:%s' % (BASELINE, f[0]))
            if t.returncode: continue
            ECON.append(dict(path=f[0], subj=' / '.join(x for x in (f[1], f[2]) if x), title=re.sub(r'\s+', ' ', f[3]).strip(), wage=len(WAGE.findall(strip(t.stdout)))))
    ECON.sort(key=lambda e: (-e['wage'], e['path'])); OUT['econ'] = ECON
    hit = [e for e in ECON if e['wage'] > 0]
    print('    %d pages tagged ECONOMICS; %d say a wage word' % (len(ECON), len(hit)))
    for e in hit: print('      %-58s x%d' % (e['path'], e['wage']))
    check(len(ECON) == 38, 'the ECONOMICS tag reaches %d pages at %s (WP-128 is now one of them)' % (len(ECON), BASELINE))
    ph = git('grep', '-l', '-i', r'wage-price\|wage price\|indexation\|cost-of-living adjust', BASELINE, '--', '*.html')
    OUT['n_index'] = len([x for x in ph.stdout.splitlines() if x.strip()]) if ph.returncode in (0, 1) else None
    print('      pages anywhere in the corpus saying wage-price / indexation / cost-of-living adjustment: %s' % OUT['n_index'])

head(7, 'THE PAGE PRINTS WHAT THIS SCRIPT COMPUTES')
def sq(s): return re.sub(r'\s+', '', html.unescape(re.sub(r'<[^>]+>', ' ', s)).lower())
raw = None
try: raw = open(os.path.join(ROOT, PAGE), encoding='utf-8').read()
except OSError: print('    SKIP  %s not found (not yet written)' % PAGE); skips.append('page')
if raw is not None and 'net' in OUT:
    cur = sq(raw)
    need = [('%+.1f%%' % OUT['net']['net'], 'net real-wage change'), ('%d of %d' % (OUT['below']['n'], OUT['below']['of']), 'months below inflation'),
            ('%.1f%%' % OUT['dd'][0]['depth'], 'first fall'), ('%+.1f%%' % OUT['robust']['all'], 'robustness series'),
            ('%+.2f' % OUT['acc']['mx'], 'worst trailing-peg miss'), ('wp129-verify.py', 'names its script')]
    for n_, m_ in need: check(n_.replace(' ', '').lower() in cur, 'page prints %s: %s' % (m_, n_))
    for k_, v_ in OUT['lag'].items(): check(('>%d</td>' % v_['k']) in raw, 'page prints the best lag for %s in a cell (%d)' % (k_, v_['k']))
    miss = [e['path'] for e in OUT.get('econ', []) if os.path.basename(e['path']) not in raw]
    check(not miss, 'the page links all %d ECONOMICS-tagged pages' % len(OUT.get('econ', [])), ', '.join(miss[:5]))
    bad = []
    for e in OUT.get('econ', []):
        m = re.search(r'href="[^"]*%s"[^>]*>.*?</a></td>\s*<td[^>]*>[^<]*</td>\s*<td[^>]*>(\d+)</td>' % re.escape(os.path.basename(e['path'])), raw, re.S)
        if not m or int(m.group(1)) != e['wage']: bad.append(e['path'])
    check(not bad, "each row's wage-word count equals the script's count", ', '.join(bad[:5]))
if '--emit' in sys.argv: json.dump(OUT, open(sys.argv[sys.argv.index('--emit') + 1], 'w'), indent=1, default=str)
print('\n' + '=' * 72)
if skips: print('  SKIPPED (not passed, not failed): %s' % ', '.join(skips))
if fails:
    print('  %d FAIL:' % len(fails)); [print('    - ' + f) for f in fails]; sys.exit(1)
print('  all run checks passed.')
print('  Recorded as open, not checked: what indexation does to inflation itself (the wage-price spiral question); productivity, against which')
print("  real wages are usually judged; who is in the wage series after April 2020 (composition); a forecast-based 'ahead' peg; the normative claim.")
