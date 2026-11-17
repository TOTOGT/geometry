#!/usr/bin/env python3
"""
Euclid -- verifier for book7/ch-euclid.html.

CHECKS: IX.20 instance (2*3*5*7*11*13 + 1 = 30031 = 59 x 509, a composite whose prime
factors are new); the IX.36 divisor-sum identity M + M(2^(p-1) - 1) = N by exact
integer arithmetic for p = 2..31; every row of the page's table against
tools/odd_perfect_check.py; the control (p = 11); the links.

DOES NOT ESTABLISH: Euler's converse (cited), the Lean declaration names (read from
local Mathlib checkouts, not compiled, not at pin 81a5d257c8), or anything about
odd perfect numbers.

    python3 book7/ch-euclid-verify.py
"""
import importlib.util, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(HERE)
fails = []
def check(ok, msg):
    print('    %s  %s' % ('PASS' if ok else 'FAIL', msg))
    if not ok: fails.append(msg)
def head(n, t): print('\n' + '=' * 70 + '\n  [%s]  %s\n' % (n, t) + '=' * 70)
spec = importlib.util.spec_from_file_location('opc', os.path.join(REPO, 'tools', 'odd_perfect_check.py'))
opc = importlib.util.module_from_spec(spec); spec.loader.exec_module(opc)
html = open(os.path.join(HERE, 'ch-euclid.html'), encoding='utf-8').read()

head(1, 'IX.20 INSTANCE')
P = 2 * 3 * 5 * 7 * 11 * 13
check(P + 1 == 30031 and 59 * 509 == 30031, '2*3*5*7*11*13 + 1 = 30031 = 59 x 509')
check(opc.factorise(30031) == [59, 509] and not opc.is_prime(30031), '30031 is composite, with prime factors 59 and 509')
check(all(30031 % q == 1 for q in (2, 3, 5, 7, 11, 13)) or all((P + 1) % q == 1 for q in (2, 3, 5, 7, 11, 13)), 'remainder 1 on division by each listed prime')
check(59 not in (2, 3, 5, 7, 11, 13) and 509 not in (2, 3, 5, 7, 11, 13), 'both prime factors are new')

head(2, 'IX.36 IDENTITY, p = 2..31, EXACT INTEGERS')
ok = True
for p in range(2, 32):
    M = 2 ** p - 1; N = 2 ** (p - 1) * M
    if sum(2 ** k for k in range(p)) != M or M + M * (2 ** (p - 1) - 1) != N: ok = False
check(ok, 'sum(1..2^(p-1)) = 2^p - 1 and M + M(2^(p-1) - 1) = N for every p in 2..31')
check(1 + 2 + 3 == 6 and 1 + 2 + 4 + 7 + 14 == 28, '6 = 1+2+3 and 28 = 1+2+4+7+14')

head(3, 'TABLE vs tools/odd_perfect_check.py')
ref = {r['p']: r for r in opc.compute(1000)['mersenne']}
rows = re.findall(r'<tr data-p="(\d+)" data-M="(\d+)" data-N="(\d+)" data-prime="([01])" data-brute="([01])"', html)
check(len(rows) == 9, 'table has %d rows' % len(rows))
for p, M, N, pr, br in rows:
    p = int(p); r = ref[p]
    check(int(M) == r['M'] and int(N) == r['N'] and (pr == '1') == r['M_prime'], 'p = %d: M, N, primality match' % p)
    if br == '1' and r['M_prime']:
        check(opc.proper_sum(r['N']) == r['N'], 'p = %d: brute-force divisor sum of N equals N' % p)
    if br == '0':
        check(r['M_prime'] and r['N'] > 10 ** 10, 'p = %d: not brute-forced because N > 10^10; M prime, so the IX.36 argument applies' % p)
check(opc.proper_sum(2 ** 10 * 2047) != 2 ** 10 * 2047, 'control p = 11: N = 2096128 is not perfect')
check(2 ** 10 * 2047 == 2096128 and 2047 == 23 * 89, 'control arithmetic: N = 2096128, 2047 = 23 x 89')

head(4, 'STRUCTURE AND LINKS')
for lab in ('THEOREM', 'CHECKED INSTANCE', 'OPEN QUESTION'):
    check(('<b>%s</b>' % lab) in html, 'visible evidence label %s present' % lab)
check('href="ch-odd-perfect.html"' in html, 'links to the interactive chapter')
odd = open(os.path.join(HERE, 'ch-odd-perfect.html'), encoding='utf-8').read()
check('href="ch-euclid.html"' in odd, 'interactive chapter links back')
check('Theorems100.Nat.even_and_perfect_iff' in html and '81a5d257c8' in html, 'Lean name and pinned revision stated, with the not-compiled caveat')
check('were not compiled here' in html, 'caveat that the Lean names were not compiled is on the page')
print('\n' + '=' * 70)
if fails:
    print('  %d CHECK(S) FAILED:' % len(fails)); [print('    - ' + f) for f in fails]; sys.exit(1)
print('  ALL CHECKS PASSED')
