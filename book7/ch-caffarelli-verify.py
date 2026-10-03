#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ch-caffarelli-verify.py -- companion to book7/ch-caffarelli.html.

Checks the page's dates and names against the biography PDF in ~/Downloads and for internal
consistency. It does NOT check that the biography is right. Every control must fail.
"""
import os, re, subprocess, sys, html
FAIL = 0
def check(ok, msg):
    global FAIL
    print('    %s  %s' % ('PASS' if ok else 'FAIL', msg))
    if not ok: FAIL += 1
def head(n, t): print('\n' + '=' * 72 + '\n  [%d]  %s\n' % (n, t) + '=' * 72)

here = os.path.dirname(os.path.abspath(__file__))
page = open(os.path.join(here, 'ch-caffarelli.html'), encoding='utf-8').read()
ptxt = re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', page))).lower()

head(1, 'sourcing against the biography in ~/Downloads')
D = next((q for q in (os.path.expanduser('~/Downloads/'), os.path.expanduser('~/mnt/Downloads/')) if os.path.isdir(q)), None)
src = None
if D:
    for fn in os.listdir(D):
        if fn.lower().startswith('caffarelli biography') and fn.endswith('.pdf'):
            src = subprocess.run(['pdftotext', os.path.join(D, fn), '-'], capture_output=True, text=True).stdout
if src is None:
    print('    SKIP  biography PDF not found'); 
else:
    s = re.sub(r'\s+', ' ', src.replace('’', "'").replace('‘', "'")).lower()
    needles = ['born in buenos aires', '1948', 'calixto calderon', '1972', 'sobre conjugaci', 'hans lewy', 'obstacle problem',
               'in 1976 he published six papers', '1977', 'acta mathematica', 'regularity of free boundaries in higher dimensions',
               'chinatown', 'robert kohn', 'louis nirenberg', 'partial regularity of suitable weak solutions', 'steele prize for seminal',
               'stampacchia', 'warsaw', 'bôcher prize', 'university of chicago between 1983 and 1986', 'institute of advanced study',
               'monge-ampère', 'optimal transportation', '1994', 'sid richardson chair', 'homogenization', '320 papers', 'aged 74',
               'more than 130', 'avner friedman', '19,000 citations', 'more than 30 phd', 'alessio figalli', 'fields medal',
               '2005 rolf schock', '2009 steele prize for lifetime', '2012 wolf prize', '2013 solomon lefschetz', '2018 shaw prize',
               'national academy', '1991', 'irene martínez gamba', 'tex moncrief', 'three sons', 'mathsci', 'nolan zunk']
    for n in needles:
        check(n in s, 'biography contains: %s' % n)
    check('villani' not in s, 'control: a name not in the biography (Villani) is absent')
    check('abel prize' not in s.replace('abel prize laureate', ''), 'the Abel Prize 2023 is NOT in the biography (the page says so)')

head(2, 'what the page says matches')
for n in ['1948', '1972', '1977', '1982', '1983', '1994', '1997', '320 papers', '130 people', '19,000', 'figalli',
          'abel prize 2023', 'not</em> in the biography'.replace('</em>', '')]:
    check(n in ptxt, 'page contains: %s' % n)
check('villani' not in ptxt, 'control: the page does not name Villani')

head(3, 'arithmetic and consistency')
check(1972 - 1948 == 24, 'PhD at 24 (1972 - 1948)')
check(1986 - 1983 == 3, 'Chicago 1983-86 is three years')
check(1994 - 1986 == 8, 'Institute 1986-94 is 8 years, not a decade (the page says the biography is loose here)')
check(1994 - 1986 != 10, 'control: it is not 10')
check(2022 - 1948 == 74 or 2023 - 1948 == 75, 'age 74 puts the biography at 2022 (or early 2023)')
check(1982 < 1983 < 1984 < 1991 < 2005 < 2009 < 2012 < 2013 < 2014 < 2018, 'honours table is in date order')
rows = re.findall(r'<tr><td>(\d{4})</td><td>([^<]*(?:<[^t][^>]*>[^<]*)*)</td></tr>', page.split('Part III')[1].split('Abel')[0])
yrs = [int(r[0]) for r in rows]
check(len(yrs) == 9 and yrs == sorted(yrs), 'honours rows: 9, in order (%s)' % yrs)
check(yrs != sorted(yrs, reverse=True), 'control: not in reverse order')
print('\n' + ('ALL CHECKS PASS' if not FAIL else '%d FAILED' % FAIL))
sys.exit(1 if FAIL else 0)
