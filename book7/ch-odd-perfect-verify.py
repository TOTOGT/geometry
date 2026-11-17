#!/usr/bin/env python3
"""
Can a Perfect Number Be Odd? -- verifier for book7/ch-odd-perfect.html.

WHAT IT CHECKS
  [1] The numbers embedded in the page (static search result, Mersenne table) equal
      what tools/odd_perfect_check.py computes.
  [2] The page's own live functions (the <script id="odd-perfect-core"> block) are
      extracted and run under Node, and their outputs are compared with the Python
      values: proper-divisor sums, the odd search at several limits, Lucas-Lehmer,
      and the p = 2 special case. If Node is absent this block prints SKIPPED and the
      script exits non-zero, because an unrun check is not a pass.
  [3] Structure: the three evidence labels, the exact-interval wording, the
      cross-links to and from ch-euclid.html, the Book 7 index card.

WHAT IT DOES NOT ESTABLISH
  Nothing about odd perfect numbers beyond the searched interval. The cited
  statements (Ochem-Rao bound, Euler's form, Euler's converse) are not checked here;
  the Lean declaration names are not compiled here.

    python3 book7/ch-odd-perfect-verify.py
"""
import importlib.util, json, os, re, shutil, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
fails, skipped = [], []
def check(ok, msg):
    print('    %s  %s' % ('PASS' if ok else 'FAIL', msg))
    if not ok: fails.append(msg)
def head(n, t):
    print('\n' + '=' * 70 + '\n  [%s]  %s\n' % (n, t) + '=' * 70)

spec = importlib.util.spec_from_file_location('opc', os.path.join(REPO, 'tools', 'odd_perfect_check.py'))
opc = importlib.util.module_from_spec(spec); spec.loader.exec_module(opc)
html = open(os.path.join(HERE, 'ch-odd-perfect.html'), encoding='utf-8').read()

head(1, 'EMBEDDED NUMBERS vs tools/odd_perfect_check.py')
ref = opc.compute()
pre = re.search(r'<div[^>]*id="precomputed"([^>]*)>', html)
attrs = dict(re.findall(r'data-([a-z-]+)="([^"]*)"', pre.group(1))) if pre else {}
check(bool(pre), 'static result block id="precomputed" present')
check(int(attrs.get('limit', -1)) == ref['limit'] == 999999, 'limit 999999 matches the tool (%s)' % attrs.get('limit'))
check(int(attrs.get('candidates', -1)) == ref['odd_candidates'] == 500000, '500,000 odd candidates matches the tool')
check(int(attrs.get('odd-hits', -1)) == len(ref['odd_perfect_found']) == 0, '0 odd hits matches the tool')
check([int(x) for x in attrs.get('perfect', '').split(',') if x] == ref['perfect_found'], 'perfect numbers in the interval equal %s' % ref['perfect_found'])
check('1 through 999,999 inclusive' in html and '500,000' in html, 'prose states the exact inclusive interval and the candidate count')
rows = re.findall(r'<tr data-p="(\d+)"\s+data-M="(\d+)"\s+data-prime="([01])"', html)
byp = {r['p']: r for r in ref['mersenne']}
check(len(rows) >= 8, 'Mersenne table has %d rows' % len(rows))
check(all(int(M) == byp[int(p)]['M'] and (pr == '1') == byp[int(p)]['M_prime'] for p, M, pr in rows), 'every table row: M and primality match the tool')
check(('23 &times; 89' in html) and ('47 &times; 178481' in html) and ('233 &times; 1103 &times; 2089' in html), 'factorisations quoted for p = 11, 23, 29')
check(byp[11]['factors'] == [23, 89] and byp[23]['factors'] == [47, 178481] and byp[29]['factors'] == [233, 1103, 2089], 'quoted factorisations equal the tool')

head(2, 'THE PAGE\'S LIVE FUNCTIONS, RUN UNDER NODE')
m = re.search(r'<script id="odd-perfect-core">(.*?)</script>', html, re.S)
check(bool(m), 'core script block present')
node = shutil.which('node')
if not node:
    print('    SKIPPED  node not found; the live functions were NOT run'); skipped.append('node')
else:
    harness = m.group(1) + r'''
const out = {};
out.sums = {}; [1,2,6,9,25,28,36,496,12].forEach(n => out.sums[n] = OP.properSum(n));
out.search = {}; [1, 2, 27, 28, 999, 99999].forEach(l => { const r = OP.searchOdd(l); out.search[l] = {c: r.candidates, h: r.oddHits.length, p: r.perfect}; });
out.mers = {}; for (let p = 2; p <= 31; p++) { const r = OP.mersenne(p); out.mers[p] = {M: r.M.toString(), prime: r.prime, method: r.method}; }
out.naive2 = OP.lucasLehmer(2).prime;
out.euclid = {}; [2,3,5,7,11,13,17,19,31].forEach(p => { const e = OP.euclid(p); out.euclid[p] = {N: e.N.toString(), mode: e.mode, perfect: e.perfect}; });
console.log(JSON.stringify(out));
'''
    with tempfile.TemporaryDirectory() as td:
        fn = os.path.join(td, 'h.js'); open(fn, 'w').write(harness)
        r = subprocess.run([node, fn], capture_output=True, text=True, timeout=120)
    check(r.returncode == 0, 'node ran the page functions (exit %d)%s' % (r.returncode, '' if r.returncode == 0 else ': ' + r.stderr[:200]))
    if r.returncode == 0:
        js = json.loads(r.stdout)
        check(all(js['sums'][str(n)] == opc.proper_sum(n) for n in (1,2,6,9,25,28,36,496,12)), 'page properSum equals Python proper_sum on 1,2,6,9,12,25,28,36,496')
        check(js['sums']['9'] == 4 and js['sums']['25'] == 6 and js['sums']['36'] == 55 and js['sums']['1'] == 0 and js['sums']['12'] == 16, 's(9)=4, s(25)=6, s(36)=55, s(1)=0, s(12)=16 (square root counted once)')
        for l in (1, 2, 27, 28, 999, 99999):
            py = opc.compute(l); s = js['search'][str(l)]
            check(s['c'] == py['odd_candidates'] and s['h'] == len(py['odd_perfect_found']) and s['p'] == py['perfect_found'],
                  'odd search limit %d: candidates %d, hits %d, perfect %s agree with Python' % (l, s['c'], s['h'], s['p']))
        check(js['search']['1']['c'] == 1 and js['search']['2']['c'] == 1 and js['search']['27']['c'] == 14, 'candidate count is ceil(limit/2): limits 1, 2, 27 give 1, 1, 14')
        ok = all(js['mers'][str(p)]['prime'] == byp[p]['M_prime'] and js['mers'][str(p)]['M'] == str(byp[p]['M']) for p in range(2, 32))
        check(ok, 'page Mersenne primality equals Python for every p = 2..31')
        check(js['mers']['2']['method'] == 'p = 2 handled directly' and js['mers']['2']['prime'] is True, 'p = 2 is handled explicitly and returns prime')
        check(js['naive2'] is False, 'the page mechanical lucasLehmer(2) says composite (zero steps, s_0 = 4 is not 0), which is why p = 2 is special-cased')
        for p in (2, 3, 5, 7, 13, 17):
            e = js['euclid'][str(p)]
            check(e['mode'] == 'brute' and e['perfect'] is True and int(e['N']) == byp[p]['N'], 'p = %d: N = %s brute-forced perfect' % (p, e['N']))
        e = js['euclid']['11']; check(e['mode'] == 'brute' and e['perfect'] is False, 'p = 11 control: N = %s is not perfect' % e['N'])
        check(opc.proper_sum(byp[19]['N']) == byp[19]['N'] and js['euclid']['19']['perfect'] is True, 'p = 19: page says perfect; Python brute-force divisor sum of %d agrees' % byp[19]['N'])
        check(js['euclid']['31']['mode'] == 'formula' and js['euclid']['31']['perfect'] is True, 'p = 31: page uses the sigma identity (N > 10^12) and it holds')

head(3, 'STRUCTURE AND LINKS')
for lab in ('THEOREM', 'CHECKED INSTANCE', 'OPEN QUESTION'):
    check(('<b>%s</b>' % lab) in html, 'visible evidence label %s present' % lab)
tags = set(re.findall(r'>(SHOWN|CITED|MODEL|CONJECTURE|OPEN|PARTIAL|PROVED|COMPUTED|ASSUMPTION|DEFINITION)<', html))
check({'PROVED', 'COMPUTED', 'OPEN', 'CITED'} <= tags, 'corpus epistemic tags present: %s' % sorted(tags))
check('href="ch-euclid.html"' in html, 'links to ch-euclid.html')
euclid = open(os.path.join(HERE, 'ch-euclid.html'), encoding='utf-8').read()
check('href="ch-odd-perfect.html"' in euclid, 'ch-euclid.html links back to ch-odd-perfect.html')
idx = open(os.path.join(HERE, 'index.html'), encoding='utf-8').read()
check('href="ch-odd-perfect.html"' in idx and 'href="ch-euclid.html"' in idx, 'Book 7 index has both cards')
check(all(k in html for k in ('id="n-in"', 'id="p-in"', 'id="lim-in"')), 'all three controls present (divisor sum, exponent, search limit)')
check('width=device-width' in html and '@media (max-width:600px)' in html, 'viewport meta and a phone-width rule present')
check('81a5d257c8' in html, 'pinned Mathlib revision stated')

print('\n' + '=' * 70)
if skipped: print('  NOT RUN: %s' % ', '.join(skipped))
if fails:
    print('  %d CHECK(S) FAILED:' % len(fails)); [print('    - ' + f) for f in fails]
    sys.exit(1)
if skipped: sys.exit(2)
print('  ALL CHECKS PASSED')
