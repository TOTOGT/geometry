#!/usr/bin/env python3
"""Fold early-warning pipeline from docs/prereg-bitcoin.md (committed fb29d1a).

  python3 docs/bitcoin-fold-check.py --selftest            synthetic worlds only, no market data
  python3 docs/bitcoin-fold-check.py --csv F --source NAME real run (needs a named source)

Every analysis choice below is the one pinned in the pre-registration:
  state      x_t = log(close_t) - trailing 90-day mean of log(close) (causal, includes day t)
  event      close <= 70% of the trailing 60-day maximum (a decline of at least 30% within 60 days);
             event start = date of that maximum; triggers closer than 120 days to the previous kept one are merged
  window     the 120 days before the event start; rolling 60-day windows inside it (61 windows)
  statistic  Kendall tau against time of the rolling variance and of the rolling lag-1 autocorrelation,
             each averaged over events
  null       GARCH(1,1) with Student-t innovations fitted to the same returns, N surrogates through the same steps
  primary    real mean tau at or above the 95th percentile of the surrogates for BOTH statistics
  limits     fewer than 6 events -> underpowered, never a pass

Things the pre-registration did NOT pin, decided here and reported by the script, not hidden:
  (a) a surrogate with no events has no tau and is excluded from the percentile (the count is printed);
  (b) events with fewer than 89+120 days of history before the start are skipped (the count is printed);
  (c) rolling lag-1 autocorrelation is the Pearson correlation of x[t-59..t-1] with x[t-58..t];
  (d) if fewer than half of the surrogates produce any event, the null is degenerate and the test is not a pass.
"""
import argparse, math, sys
import numpy as np
from numpy.lib.stride_tricks import sliding_window_view as swv
from scipy.optimize import minimize
from scipy.special import gammaln
from scipy.stats import kendalltau

DETREND, DD, DD_WIN, SPACING, PRE, ROLL = 90, 0.30, 60, 120, 120, 60
MIN_EVENTS = 6

FAIL = []
def check(ok, msg):
    print('    %s  %s' % ('PASS' if ok else 'FAIL', msg))
    if not ok: FAIL.append(msg)
def head(n, t):
    print('\n' + '=' * 70 + '\n  [%s]  %s\n' % (n, t) + '=' * 70)


# ------------------------------------------------------------------ pipeline
def state(logp):
    c = np.cumsum(np.insert(logp, 0, 0.0))
    m = np.full_like(logp, np.nan)
    m[DETREND - 1:] = (c[DETREND:] - c[:-DETREND]) / DETREND
    return logp - m

def find_events(price):
    """Return list of (trigger_index, start_index)."""
    T = len(price)
    if T < DD_WIN: return []
    w = swv(price, DD_WIN)                    # w[i] covers days i .. i+59, ending at t = i+59
    M = w.max(axis=1)
    d = price[DD_WIN - 1:] / M - 1.0
    cand = np.where(d <= -DD)[0]
    out, last = [], -10**9
    for i in cand:
        t = i + DD_WIN - 1
        if t - last >= SPACING:
            start = t - (DD_WIN - 1) + int(np.argmax(w[i]))
            out.append((t, start)); last = t
    return out

def roll_stats(x, s):
    """61 rolling (variance, lag-1 autocorr) values in the PRE days before s; None if history is short."""
    lo = s - PRE
    if lo < DETREND - 1 or s > len(x): return None
    seg = x[lo:s]
    if np.isnan(seg).any(): return None
    var, ac = [], []
    for e in range(ROLL, PRE + 1):            # windows seg[e-60:e], e = 60..120
        win = seg[e - ROLL:e]
        var.append(win.var())
        a, b = win[:-1], win[1:]
        sa, sb = a.std(), b.std()
        ac.append(0.0 if sa == 0 or sb == 0 else float(np.mean((a - a.mean()) * (b - b.mean())) / (sa * sb)))
    return np.array(var), np.array(ac)

def pipeline(price):
    """Return dict: n_events, n_skipped, tau_var, tau_ac (means over events; nan if none)."""
    logp = np.log(price)
    x = state(logp)
    evs = find_events(price)
    tv, ta, skipped = [], [], 0
    for _, s in evs:
        r = roll_stats(x, s)
        if r is None: skipped += 1; continue
        k = np.arange(len(r[0]))
        tv.append(kendalltau(k, r[0])[0]); ta.append(kendalltau(k, r[1])[0])
    return dict(n=len(tv), skipped=skipped,
                tau_var=float(np.mean(tv)) if tv else float('nan'),
                tau_ac=float(np.mean(ta)) if ta else float('nan'))


# ------------------------------------------------------------------ GARCH(1,1)-t
def _nll(p, r):
    mu, om, al, be, nu = p
    e = r - mu
    s2 = np.empty_like(r); s2[0] = r.var()
    for t in range(1, len(r)):
        s2[t] = om + al * e[t - 1] ** 2 + be * s2[t - 1]
    z2 = e ** 2 / s2
    c = gammaln((nu + 1) / 2) - gammaln(nu / 2) - 0.5 * math.log(math.pi * (nu - 2))
    return -np.sum(c - 0.5 * np.log(s2) - (nu + 1) / 2 * np.log1p(z2 / (nu - 2)))

def fit_garch(logp):
    r = 100 * np.diff(logp)
    v = r.var()
    best = None
    for al0, be0 in ((0.08, 0.9), (0.15, 0.8)):
        x0 = [r.mean(), v * (1 - al0 - be0), al0, be0, 6.0]
        res = minimize(_nll, x0, args=(r,), method='L-BFGS-B',
                       bounds=[(-5, 5), (1e-6, None), (1e-4, 0.6), (0.0, 0.999), (2.5, 60)])
        if best is None or res.fun < best.fun: best = res
    mu, om, al, be, nu = best.x
    if al + be >= 0.9999:                     # keep it stationary
        be = 0.9999 - al
    return dict(mu=mu, om=om, al=al, be=be, nu=nu)

def simulate(par, T, n, p0, rng):
    """n surrogate price paths of T days (T-1 returns), GARCH(1,1)-t."""
    mu, om, al, be, nu = (par[k] for k in ('mu', 'om', 'al', 'be', 'nu'))
    s2 = np.full(n, om / max(1e-9, 1 - al - be))
    out = np.zeros((n, T)); out[:, 0] = math.log(p0)
    sc = math.sqrt((nu - 2) / nu)
    for t in range(1, T):
        z = rng.standard_t(nu, size=n) * sc
        e = np.sqrt(s2) * z
        out[:, t] = out[:, t - 1] + (mu + e) / 100
        s2 = om + al * e ** 2 + be * s2
    return np.exp(out)


def surrogate_test(price, nsur, rng):
    par = fit_garch(np.log(price))
    sur = simulate(par, len(price), nsur, price[0], rng)
    tv, ta, noev = [], [], 0
    for row in sur:
        r = pipeline(row)
        if r['n'] == 0: noev += 1; continue
        tv.append(r['tau_var']); ta.append(r['tau_ac'])
    real = pipeline(price)
    out = dict(real=real, par=par, noev=noev, used=len(tv))
    if tv and real['n'] > 0:
        out['q_var'], out['q_ac'] = float(np.quantile(tv, 0.95)), float(np.quantile(ta, 0.95))
        out['pass_var'] = bool(real['tau_var'] >= out['q_var'])
        out['pass_ac'] = bool(real['tau_ac'] >= out['q_ac'])
        out['rank_var'] = float(np.mean(np.array(tv) >= real['tau_var']))
        out['rank_ac'] = float(np.mean(np.array(ta) >= real['tau_ac']))
    out['underpowered'] = real['n'] < MIN_EVENTS
    out['degenerate'] = len(tv) < 0.5 * nsur
    out['primary'] = bool(out.get('pass_var') and out.get('pass_ac') and not out['underpowered'] and not out['degenerate'])
    return out

def report(res, name):
    r = res['real']
    print('    %s: events used %d (skipped for short history: %d); mean tau variance %.3f, autocorrelation %.3f'
          % (name, r['n'], r['skipped'], r['tau_var'], r['tau_ac']))
    if 'q_var' in res:
        print('      surrogates used %d (no events: %d); 95th pct variance %.3f / autocorr %.3f; fraction of surrogates >= real: variance %.3f, autocorr %.3f'
              % (res['used'], res['noev'], res['q_var'], res['q_ac'], res['rank_var'], res['rank_ac']))
    print('      underpowered: %s; null degenerate: %s; PRIMARY TEST %s' % (res['underpowered'], res['degenerate'], 'PASSES' if res['primary'] else 'does not pass'))


# ------------------------------------------------------------------ synthetic worlds (self-test only)
def world_fold(rng, episodes=10, lam_end=0.04, lam_start=0.6, sigma=0.01, crash=-0.45, vol_ramp=1.0, const_lam=None):
    """Level = AR(1) deviation whose restoring rate lambda falls toward 0 (critical slowing), then a crash.
    const_lam keeps lambda fixed (no slowing); vol_ramp>1 ramps the noise scale instead."""
    parts = []
    for _ in range(episodes):
        n = 380
        lam = np.linspace(lam_start, lam_end, n) if const_lam is None else np.full(n, const_lam)
        sg = sigma * np.linspace(1.0, vol_ramp, n)
        x = np.zeros(n); xx = 0.0
        for t in range(n):
            xx = (1 - lam[t]) * xx + sg[t] * rng.standard_normal()
            x[t] = xx
        rec = []
        for t in range(120):
            lamr = 0.3
            xx = (1 - lamr) * xx + sigma * rng.standard_normal()
            shift = crash * (1.0 if t < 60 else (1 - (t - 60) / 60.0))
            rec.append(xx + shift)
        x[-1] += crash                        # the crash arrives within a day
        parts.append(np.concatenate([x, rec]))
    return np.exp(np.concatenate(parts))

def world_null(rng, T=3500, mu=0.0, om=0.25, al=0.12, be=0.86, nu=4.0):
    return simulate(dict(mu=mu, om=om, al=al, be=be, nu=nu), T, 1, 100.0, rng)[0]


def _job(a):
    kind, seed, nsur = a
    rng = np.random.default_rng(seed)
    if kind == 'null': p = world_null(rng)
    elif kind == 'fold_mod': p = world_fold(rng, vol_ramp=3.0)
    elif kind == 'fold_strong': p = world_fold(rng, lam_end=0.02, vol_ramp=6.0)
    if kind in ('null', 'fold_mod', 'fold_strong'):
        r = surrogate_test(p, nsur, rng)
        return kind, r['primary'], r['underpowered'], r['degenerate'], r['real']['tau_var'], r['real']['tau_ac']

def _stat_job(a):
    kind, seed = a
    rng = np.random.default_rng(seed)
    if kind == 'fold': p = world_fold(rng, vol_ramp=3.0)
    elif kind == 'noslow': p = world_fold(rng, const_lam=0.3, lam_start=0.3, lam_end=0.3)
    elif kind == 'varonly': p = world_fold(rng, const_lam=0.3, vol_ramp=12.0)
    r = pipeline(p)
    return kind, r['tau_var'], r['tau_ac'], r['n']

def selftest(nsur):
    from multiprocessing import Pool
    REP = 12
    with Pool(3) as P:
        stat = P.map(_stat_job, [(k, 500 + i) for k in ('fold', 'noslow', 'varonly') for i in range(REP)])
        jobs = P.map(_job, [(k, 900 + i, nsur) for k in ('fold_mod', 'fold_strong', 'null') for i in range(REP)])
    mean = lambda k, j: float(np.mean([x[j] for x in stat if x[0] == k]))

    head('S1', 'statistic-level controls (no surrogates): does each world move the right statistic?')
    print('    mean tau over %d replicates   variance   autocorrelation' % REP)
    for k, lab in (('fold', 'slowing + noise ramp'), ('noslow', 'no slowing'), ('varonly', 'variance ramp only')):
        print('      %-22s %8.2f %12.2f' % (lab, mean(k, 1), mean(k, 2)))
    check(mean('fold', 2) > mean('noslow', 2) + 0.1, 'autocorrelation tau is higher with slowing than without (%.2f vs %.2f)' % (mean('fold', 2), mean('noslow', 2)))
    check(mean('varonly', 2) < mean('fold', 2) - 0.1, 'a variance-only world does not raise autocorrelation tau (%.2f vs %.2f with slowing)' % (mean('varonly', 2), mean('fold', 2)))
    check(mean('fold', 1) > mean('noslow', 1) + 0.05, 'variance tau is higher with a noise ramp than without (%.2f vs %.2f)' % (mean('fold', 1), mean('noslow', 1)))

    head('S2', 'false-positive rate on pure GARCH-t worlds with bitcoin-like volatility (no fold exists)')
    nul = [x for x in jobs if x[0] == 'null']
    npos = sum(x[1] for x in nul); nunder = sum(x[2] for x in nul); ndeg = sum(x[3] for x in nul)
    print('    %d of %d passed the primary test; %d underpowered, %d with a degenerate null' % (npos, len(nul), nunder, ndeg))
    check(nunder + ndeg <= len(nul) // 4, 'the null worlds are mostly usable (%d underpowered, %d degenerate of %d), so this check is not vacuous' % (nunder, ndeg, len(nul)))
    check(npos / len(nul) <= 0.15, 'false-positive rate %.2f is not above 0.15' % (npos / len(nul)))

    head('S3', 'POWER: how often the pre-registered primary test passes when a fold signature is built in')
    for k in ('fold_mod', 'fold_strong'):
        f = [x for x in jobs if x[0] == k]
        pw = sum(x[1] for x in f) / len(f)
        print('    %-12s passes %d of %d  (power %.2f)' % (k, sum(x[1] for x in f), len(f), pw))
        check(pw >= 0.6, '%s: power %.2f is at least 0.6 (below that, a FAIL on real data cannot demote a row)' % (k, pw))

    head('S4', 'the shuffle control: destroying the order inside each window removes the trend')
    rng = np.random.default_rng(7)
    p = world_fold(rng, vol_ramp=3.0)
    x = state(np.log(p)); tv, ta = [], []
    for _, st in find_events(p):
        r = roll_stats(x, st)
        if r is None: continue
        v, a_ = r; perm = rng.permutation(len(v)); k = np.arange(len(v))
        tv.append(kendalltau(k, v[perm])[0]); ta.append(kendalltau(k, a_[perm])[0])
    check(abs(np.mean(tv)) < 0.3 and abs(np.mean(ta)) < 0.3, 'mean taus after shuffling %.2f, %.2f' % (np.mean(tv), np.mean(ta)))

    print()
    if FAIL:
        print('FAILED: %d check(s)' % len(FAIL)); sys.exit(1)
    print('all checks passed'); sys.exit(0)


def real(csv, source, nsur):
    if not source.strip():
        sys.exit('refusing to run: --source must name the data source (pre-registration requires it)')
    import csv as _csv
    rows = list(_csv.DictReader(open(csv)))
    key = next(k for k in rows[0] if k.strip().lower() in ('close', 'adj close', 'price'))
    price = np.array([float(r[key]) for r in rows if r[key] not in ('', 'null')])
    print('source: %s; %d daily closes' % (source, len(price)))
    rng = np.random.default_rng(1)
    res = surrogate_test(price, nsur, rng)
    report(res, 'real series')
    print('    fitted GARCH-t: ' + ', '.join('%s=%.4g' % kv for kv in res['par'].items()))


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--selftest', action='store_true')
    ap.add_argument('--csv'); ap.add_argument('--source', default='')
    ap.add_argument('--nsur', type=int, default=1000)
    a = ap.parse_args()
    if a.selftest: selftest(min(a.nsur, 80))
    elif a.csv: real(a.csv, a.source, a.nsur)
    else: ap.print_help()
