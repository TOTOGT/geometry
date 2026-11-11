#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Pablo Nogueira Grossi / G6 LLC
"""
book24/ch12-verify.py -- every check behind book24/ch12-mle-consistency.html. Run first.

    python3 book24/ch12-verify.py

Standard library only. Simulations use a fixed seed, so the run is deterministic. Nothing here proves a theorem; the
proof is on the page. The Hill-curve numbers are idealised (known noise, one shared inflection time, no between-subject
variation) and are an illustration of design, not a prediction for any cohort.

  [1] Gibbs inequality: KL(p0 || p) > 0 for every p != p0 on a rational grid (Bernoulli), and = 0 at p = p0
  [2] consistency by simulation, seeded: the Bernoulli MLE (sample mean) and the Gaussian-location MLE come closer to
      the truth as n grows 10^2 .. 10^6 (a deterministic run of a probabilistic statement, not a proof)
  [3] the Hill curve mu = t^n/(t^n+tau^n) at n = 2*pi/sqrt(3), tau = 1: analytic derivatives against finite differences;
      efficient information for n (tau profiled out) for four observation designs; the number of subjects for a 95%
      half-width of 0.5, sigma = 0.05
  [4] noiseless identifiability: the squared-error surface over a grid has its unique minimum at (n0, 1) for the design
      that spans the inflection, and a long flat valley for the plateau-only design
  [5] the page prints the numbers above, tags SBIR Aim 1 and Aim 2, says no Lean file exists yet, and states the
      idealisations
"""
import math, os, random, sys
from fractions import Fraction
here = os.path.dirname(os.path.abspath(__file__))
ok = []
def chk(name, cond):
    ok.append(bool(cond)); print(('PASS ' if cond else 'FAIL ') + name)
# [1]
def kl(p0, p): return p0*math.log(p0/p) + (1-p0)*math.log((1-p0)/(1-p))
grid = [Fraction(i, 50) for i in range(1, 50)]
bad = [(a, b) for a in grid for b in grid if a != b and kl(float(a), float(b)) <= 0]
chk('Gibbs: KL(p0||p) > 0 for all %d pairs p != p0 on the grid 1/50..49/50' % (len(grid)*(len(grid)-1)), not bad)
chk('Gibbs: KL(p0||p0) = 0', all(abs(kl(float(a), float(a))) < 1e-15 for a in grid))
# [2]
random.seed(2026)
errs = []
for n in (10**2, 10**3, 10**4, 10**5, 10**6):
    xs = sum(random.random() < 0.3 for _ in range(n))/n
    errs.append(abs(xs - 0.3))
print('   Bernoulli |p_hat - 0.3|:', ['%.4f' % e for e in errs])
chk('Bernoulli MLE: error at n=10^6 is below 0.002 and below the error at n=10^2 (seed 2026)', errs[-1] < 0.002 and errs[-1] < errs[0])
random.seed(7)
g = []
for n in (10**2, 10**4, 10**6):
    m = sum(random.gauss(1.5, 2.0) for _ in range(n))/n
    g.append(abs(m - 1.5))
print('   Gaussian |mu_hat - 1.5|:', ['%.4f' % e for e in g])
chk('Gaussian-location MLE: error at n=10^6 is below 0.005 (seed 7)', g[-1] < 0.005)
# [3]
n0 = 2*math.pi/math.sqrt(3); tau0 = 1.0; sigma = 0.05
def mu(t, n, tau): return t**n/(t**n + tau**n)
def derivs(t, n, tau):
    w = mu(t, n, tau)*(1 - mu(t, n, tau)); return w*math.log(t/tau), -w*n/tau
h = 1e-6; fd_ok = True
for t in (0.3, 0.7, 1.3, 2.9):
    dn, dt = derivs(t, n0, tau0)
    fd_ok &= abs(dn - (mu(t, n0+h, tau0) - mu(t, n0-h, tau0))/(2*h)) < 1e-8
    fd_ok &= abs(dt - (mu(t, n0, tau0+h) - mu(t, n0, tau0-h))/(2*h)) < 1e-8
chk('Hill derivatives: analytic = finite differences at four times', fd_ok)
def eff(ts):
    Inn = Int = Itt = 0.0
    for t in ts:
        dn, dt = derivs(t, n0, tau0); Inn += dn*dn; Int += dn*dt; Itt += dt*dt
    return (Inn - Int*Int/Itt)/sigma**2
designs = {'sparse3': [0.5, 1.0, 2.0], 'dense12': [0.3*10**(i/11) for i in range(12)], 'plateau3': [2.0, 2.5, 3.0], 'early3': [0.3, 0.4, 0.5]}
res = {}
for k, ts in designs.items():
    e = eff(ts); res[k] = (e, math.ceil((1.96/0.5)**2/e))
    print('   %-9s efficient information %.2f -> subjects for half-width 0.5: %d' % (k, e, res[k][1]))
chk('efficient information: dense12 > sparse3 > plateau3 and early3', res['dense12'][0] > res['sparse3'][0] > max(res['plateau3'][0], res['early3'][0]))
chk('a design spanning the inflection needs at least 40x fewer subjects than a plateau-only design', res['plateau3'][1] >= 40*res['sparse3'][1])
# [4]
def sse(ts, n, tau): return sum((mu(t, n0, tau0) - mu(t, n, tau))**2 for t in ts)
ng = [1 + 0.05*i for i in range(0, 221)]; tg = [0.3 + 0.01*i for i in range(0, 271)]
def profile(ts):
    return [min(sse(ts, n, tau) for tau in tg) for n in ng]
pf = {k: profile(designs[k]) for k in ('sparse3', 'plateau3')}
best = ng[pf['sparse3'].index(min(pf['sparse3']))]
chk('noiseless sparse3: the profile minimum sits at n0 within the grid step (%.2f vs %.4f)' % (best, n0), abs(best - n0) <= 0.05)
def valley(p): return sum(1 for v in p if v/sigma**2 <= 3.84)*0.05
print('   noiseless one-subject 95%% deviance region widths: sparse3 %.2f, plateau3 %.2f' % (valley(pf['sparse3']), valley(pf['plateau3'])))
chk('noiseless: the plateau3 region for n is wider than the sparse3 region', valley(pf['plateau3']) > valley(pf['sparse3']))
# [5]
page = open(os.path.join(here, 'ch12-mle-consistency.html'), encoding='utf-8').read()
for k in ('sparse3', 'dense12', 'plateau3', 'early3'):
    chk('page prints information %.2f and %d subjects for %s' % (res[k][0], res[k][1], k), ('%.2f' % res[k][0]) in page and (' %d ' % res[k][1] in page or '>%d<' % res[k][1] in page))
chk('page carries the tag G6-SBIR PA-27-100 Aim 1 and Aim 2', 'G6-SBIR' in page and 'PA-27-100' in page and 'Aim 1' in page and 'Aim 2' in page)
chk('page says no Lean file exists yet', 'no lean file' in page.lower())
chk('page states the idealisations', 'between-subject' in page.lower() and 'known noise' in page.lower())
chk('page says consistency does not give a rate or an interval by itself', 'does not give' in page.lower())
print('%d/%d checks passed' % (sum(ok), len(ok)))
sys.exit(0 if all(ok) else 1)
