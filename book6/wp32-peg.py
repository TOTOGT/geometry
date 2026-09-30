#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""wp32-peg.py -- producing script for the PEG addendum to book6/wp32-forced-urgency-gap.html.

Population Employment Gap:  PEG = (CNP16OV - CE16OV) / CNP16OV * 100  =  100 - EMRATIO.

Reads five public FRED series over HTTPS (fredgraph.csv, no key): CNP16OV, CE16OV, CLF16OV,
UNEMPLOY, EMRATIO, plus UNRATE and U6RATE. Prints SKIP, never PASS, when FRED cannot be reached.

The table on the page is PINNED to August 2026 (PIN below). If FRED later revises that month,
the pinned check FAILS and says so: the page's table is then stale, not the script wrong.
The script also prints the latest observation, so a newer release is visible without editing.

Not computed, recorded OPEN: the decomposition by BLS 'not employed, by reason' categories,
and any Okun's-law conversion to foregone output. Neither is run here.
"""
import sys, urllib.request, csv, io
fails, skips = [], []
def check(ok, msg, detail=''):
    print('    %s  %s%s' % ('PASS' if ok else 'FAIL', msg, ('  -- ' + detail) if detail and not ok else ''))
    if not ok: fails.append(msg)
def note(s): print('          ' + s)
def head(n, t): print('\n' + '=' * 72 + '\n  [%s]  %s\n' % (n, t) + '=' * 72)

PIN = dict(date='2026-08-01', CNP16OV=275415, CE16OV=162746, EMRATIO=59.1, UNRATE=4.1, U6RATE=7.7)

def fred(sid):
    url = 'https://fred.stlouisfed.org/graph/fredgraph.csv?id=' + sid
    raw = urllib.request.urlopen(url, timeout=40).read().decode('utf-8')
    rows = list(csv.reader(io.StringIO(raw)))[1:]
    return {d: float(v) for d, v in rows if v not in ('', '.')}

head(1, 'THE SERIES   (FRED, retrieved live)')
S = {}
try:
    for sid in ('CNP16OV', 'CE16OV', 'CLF16OV', 'UNEMPLOY', 'EMRATIO', 'UNRATE', 'U6RATE'):
        S[sid] = fred(sid)
        last = max(S[sid]); print('    %-9s %5d obs, latest %s = %s' % (sid, len(S[sid]), last, S[sid][last]))
except Exception as e:
    print('    SKIP  FRED not reachable (%s)' % e.__class__.__name__); skips.append('fred'); S = {}

if S:
    common = sorted(set.intersection(*[set(S[k]) for k in S]))
    peg = lambda d: (S['CNP16OV'][d] - S['CE16OV'][d]) / S['CNP16OV'][d] * 100
    latest = common[-1]

    head(2, 'THE IDENTITY   PEG = 100 - EMRATIO')
    worst = max(abs(peg(d) - (100 - S['EMRATIO'][d])) for d in common)
    check(worst < 0.051, 'PEG equals 100 - EMRATIO on all %d months with all series (largest gap %.4f points; EMRATIO is published to 0.1)' % (len(common), worst))
    u3 = lambda d: S['UNEMPLOY'][d] / S['CLF16OV'][d] * 100
    w3 = max(abs(u3(d) - S['UNRATE'][d]) for d in common)
    check(w3 < 0.051, 'U-3 recomputed as UNEMPLOY / CLF16OV equals UNRATE on every month (largest gap %.4f)' % w3)

    head(3, 'THE PAGE\'S TABLE   (pinned to %s)' % PIN['date'])
    d = PIN['date']
    if d not in common:
        print('    SKIP  %s not in the retrieved series' % d); skips.append('pin')
    else:
        check(S['CNP16OV'][d] == PIN['CNP16OV'] and S['CE16OV'][d] == PIN['CE16OV'], 'population %d and employment %d (thousands) as pinned' % (PIN['CNP16OV'], PIN['CE16OV']),
              'live: %s / %s' % (S['CNP16OV'][d], S['CE16OV'][d]))
        p = peg(d); print('      PEG = (%d - %d) / %d x 100 = %.4f' % (S['CNP16OV'][d], S['CE16OV'][d], S['CNP16OV'][d], p))
        check(abs(p - 40.91) < 0.005, 'PEG for August 2026 is 40.91%')
        check(S['EMRATIO'][d] == PIN['EMRATIO'] and abs(100 - S['EMRATIO'][d] - p) < 0.06, 'EMRATIO 59.1, and 100 - 59.1 = 40.9 agrees')
        check(S['UNRATE'][d] == PIN['UNRATE'], 'U-3 is 4.1%')
        check(S['U6RATE'][d] == PIN['U6RATE'], 'U-6 is 7.7%')
    print('      latest month with all series: %s  PEG = %.2f%%  U-3 = %.1f%%  U-6 = %.1f%%' % (latest, peg(latest), S['UNRATE'][latest], S['U6RATE'][latest]))

    head(4, 'WHAT THE GAP IS MADE OF   (exact, from the same series)')
    d = PIN['date'] if PIN['date'] in common else latest
    cnp, ce, clf, un = (S[k][d] for k in ('CNP16OV', 'CE16OV', 'CLF16OV', 'UNEMPLOY'))
    out_lf = (cnp - clf) / cnp * 100          # not in the labour force
    unemp = un / cnp * 100                     # unemployed, as a share of the same population
    print('      %s: not in labour force %.2f%% + unemployed %.2f%% = %.2f%%   (PEG %.2f%%)' % (d, out_lf, unemp, out_lf + unemp, peg(d)))
    check(abs(out_lf + unemp - peg(d)) < 1e-9, 'PEG = (population outside the labour force + unemployed) / population, exactly, because employment = labour force - unemployed')
    share = unemp / peg(d) * 100
    print('      unemployed are %.1f%% of the gap; people outside the labour force are %.1f%%' % (share, 100 - share))
    check(share < 10, 'the unemployed are under a tenth of the gap: PEG is not a joblessness measure')
    note('"Outside the labour force" is not "by choice": it includes retirees, students, people unable to work and people who want a job but are not counted.')
    note('The split of that block by reason (BLS table) is NOT computed here: OPEN.')

    head(5, 'THREE OTHER DATES   (computed, for scale)')
    for dd in ('2000-01-01', '2019-12-01', '2020-04-01'):
        if dd in common: print('      %s  PEG %.2f%%   U-3 %.1f%%   U-6 %.1f%%' % (dd, peg(dd), S['UNRATE'][dd], S['U6RATE'][dd]))
    note('U6RATE exists on FRED from 1994; the ShadowStats alternate measure has no public series to compare (see the page).')

print('\n' + '=' * 72)
if skips: print('  SKIPPED (not passed, not failed): %s' % ', '.join(skips))
if fails:
    print('  %d FAIL:' % len(fails)); [print('    - ' + f) for f in fails]; sys.exit(1)
print('  all run checks passed.')
print('  Recorded as open, not checked: the ShadowStats status (public updates ended in late 2023; subscriber-only since) is the author\'s')
print('  statement, not confirmed here; the ~23% (June 2016) figure has no held source; the by-reason decomposition and the Okun conversion are not run.')
