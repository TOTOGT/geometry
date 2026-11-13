#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Pablo Nogueira Grossi / G6 LLC
"""
multistability_toy.py -- the smallest toy for asking whether coupled cycles (macro, geopolitics, a large
city and its smaller neighbour) should be treated as multistable, and whether the test for it can be trusted.

THIS IS A TEST OF THE TEST, ON SYNTHETIC DATA WITH KNOWN TRUTH. It says nothing about any real economy or city.
Written 2026-11-13. Every claim is hand-derived first (below), then checked by this script. Status: run in the
cloud only; not yet run on the author's Mac.

MODEL (two nodes, A = the larger, B = the smaller and weaker; x = a state, e.g. a regime variable)
    dxA = ( xA - xA^3 + kBA (xB - xA) ) dt + s dWA
    dxB = ( mB xB - xB^3 + kAB (xA - xB) ) dt + s dWB            mB < 1: B's two wells are shallower
Each node alone is a double well (x -> -x symmetric), so each has two stable states.

HAND DERIVATION (symmetric case mB = 1, kAB = kBA = k, no noise)
  Mixed states (x, -x): from dxA = 0, x - x^3 - 2k x = 0, so x^2 = 1 - 2k. They exist iff k < 1/2.
  Jacobian [[1-3xA^2-k, k],[k, 1-3xB^2-k]] at (x,-x), with x^2 = 1-2k, has diagonal d = -2 + 5k and
  eigenvalues d +- k = -2 + 6k and -2 + 4k. So the mixed states are STABLE iff k < 1/3, exist but are saddles
  for 1/3 < k < 1/2, and vanish for k >= 1/2. The aligned states (+-1, +-1) have eigenvalues -2 and -2-2k: always stable.
  So the number of stable states is 4 for k < 1/3 and 2 for k > 1/3: coupling removes multistability.

THE TEST UNDER TEST ("is this series multistable?"), for observational data, no experiment:
  bimodal  iff  a 2-component Gaussian mixture beats a 1-component one by BIC by more than 10
           AND the two component means are more than 2 pooled standard deviations apart (Ashman's D > 2).
  The second condition is there because variance-regime switching (a volatility cycle) also makes a 2-component
  mixture fit better, with the SAME mean. That is the false positive this test must not give.

PRE-STATED FAILURE CRITERION (fixed before running):
  The test is unusable if it calls either control bimodal, or if the bistable model is not called bimodal, or if the
  correlation between nodes is NOT matched between the bistable model and the monostable control (then the
  comparison says nothing about correlation).

Standard library + numpy.
"""
import math, sys
import numpy as np

# ---------------------------------------------------------------- hand-derived facts, checked
def jac_eigs(xa, xb, k, mb=1.0, kab=None, kba=None):
    kab = k if kab is None else kab
    kba = k if kba is None else kba
    a = 1 - 3 * xa * xa - kba
    d = mb - 3 * xb * xb - kab
    b, c = kba, kab
    tr, det = a + d, a * d - b * c
    disc = tr * tr / 4 - det
    if disc >= 0:
        r = math.sqrt(disc); return (tr / 2 - r, tr / 2 + r)
    return (tr / 2, tr / 2)          # complex pair: real part


def analytic_checks():
    ok = True
    for k in (0.0, 0.2, 0.3):                    # mixed states exist and are stable
        x = math.sqrt(1 - 2 * k)
        e = jac_eigs(x, -x, k)
        ok &= max(e) < 0
        ok &= abs(e[0] - (-2 + 6 * k)) < 1e-9 or abs(e[1] - (-2 + 6 * k)) < 1e-9
    for k in (0.36, 0.45):                       # exist but unstable (saddle)
        x = math.sqrt(1 - 2 * k)
        ok &= max(jac_eigs(x, -x, k)) > 0
    ok &= (1 - 2 * 0.5) == 0                     # at k = 1/2 the mixed branch has x = 0
    for k in (0.0, 0.5, 2.0):                    # aligned states always stable
        e = jac_eigs(1, 1, k)
        ok &= max(e) < 0 and abs(min(e) - (-2 - 2 * k)) < 1e-9
    return bool(ok)


# ---------------------------------------------------------------- simulation (many paths in parallel)
def sim_bistable(kab, kba, mb=0.6, s=0.45, P=64, T=40000, dt=0.01, burn=4000, thin=20, seed=1):
    rng = np.random.default_rng(seed)
    xa = rng.choice([-1.0, 1.0], P); xb = rng.choice([-1.0, 1.0], P)
    A = np.empty((T // thin, P)); B = np.empty_like(A)
    sq = s * math.sqrt(dt)
    for t in range(T):
        na = rng.standard_normal(P); nb = rng.standard_normal(P)
        da = xa - xa ** 3 + kba * (xb - xa)
        db = mb * xb - xb ** 3 + kab * (xa - xb)
        xa, xb = xa + da * dt + sq * na, xb + db * dt + sq * nb
        if t % thin == 0:
            A[t // thin] = xa; B[t // thin] = xb
    b = burn // thin
    return A[b:], B[b:]


def sim_ou_common(rho_c, sd_target, theta=1.0, k=0.3, P=64, T=40000, dt=0.01, burn=4000, thin=20, seed=2):
    """Monostable control: linear pair with a common shock of weight rho_c. Scaled to sd_target on node A."""
    rng = np.random.default_rng(seed)
    ya = np.zeros(P); yb = np.zeros(P)
    A = np.empty((T // thin, P)); B = np.empty_like(A)
    sq = math.sqrt(dt)
    for t in range(T):
        c = rng.standard_normal(P)
        na = math.sqrt(1 - rho_c) * rng.standard_normal(P) + math.sqrt(rho_c) * c
        nb = math.sqrt(1 - rho_c) * rng.standard_normal(P) + math.sqrt(rho_c) * c
        ya, yb = ya + (-theta * ya + k * (yb - ya)) * dt + sq * na, yb + (-theta * yb + k * (ya - yb)) * dt + sq * nb
        if t % thin == 0:
            A[t // thin] = ya; B[t // thin] = yb
    b = burn // thin
    A, B = A[b:], B[b:]
    f = sd_target / A.std()
    return A * f, B * f


def sim_sv(sd_target, P=64, T=40000, dt=0.01, burn=4000, thin=20, seed=3):
    """Second control: monostable mean, but the VOLATILITY switches between two levels (a volatility cycle)."""
    rng = np.random.default_rng(seed)
    y = np.zeros(P); st = rng.integers(0, 2, P)
    out = np.empty((T // thin, P)); sq = math.sqrt(dt)
    for t in range(T):
        flip = rng.random(P) < 0.002
        st = np.where(flip, 1 - st, st)
        sig = np.where(st == 1, 1.6, 0.3)
        y = y + (-y) * dt + sig * sq * rng.standard_normal(P)
        if t % thin == 0:
            out[t // thin] = y
    out = out[burn // thin:]
    return out * (sd_target / out.std())


# ---------------------------------------------------------------- the test under test
def gmm(x, K, iters=200, seed=0):
    rng = np.random.default_rng(seed)
    n = x.size
    mu = np.quantile(x, np.linspace(0.25, 0.75, K)) if K > 1 else np.array([x.mean()])
    sd = np.full(K, x.std()); w = np.full(K, 1.0 / K)
    for _ in range(iters):
        pdf = np.stack([w[j] * np.exp(-0.5 * ((x - mu[j]) / sd[j]) ** 2) / (sd[j] * math.sqrt(2 * math.pi)) for j in range(K)])
        tot = pdf.sum(0) + 1e-300
        r = pdf / tot
        nk = r.sum(1) + 1e-12
        w = nk / n; mu = (r * x).sum(1) / nk
        sd = np.sqrt(np.maximum((r * (x[None, :] - mu[:, None]) ** 2).sum(1) / nk, 1e-8))
    ll = np.log(tot).sum()
    npar = 3 * K - 1
    return ll, npar * math.log(n), mu, sd, w


def bimodal_test(series, sub=7):
    x = series[::sub].ravel()
    ll1, p1, *_ = gmm(x, 1)
    ll2, p2, mu, sd, w = gmm(x, 2)
    dbic = (-2 * ll1 + p1) - (-2 * ll2 + p2)       # positive favours two components
    D = abs(mu[0] - mu[1]) / math.sqrt((sd[0] ** 2 + sd[1] ** 2) / 2)
    return dbic, D, (dbic > 10 and D > 2)


def corr(A, B):
    return float(np.corrcoef(A.ravel(), B.ravel())[0, 1])


def flips(S):
    """number of sign changes per path (with a dead zone, to ignore noise around 0)."""
    z = np.where(S > 0.3, 1, np.where(S < -0.3, -1, 0))
    cnt = 0
    for j in range(z.shape[1]):
        col = z[:, j]; col = col[col != 0]
        cnt += int((col[1:] != col[:-1]).sum())
    return cnt


def main():
    print("[1] hand-derived coupling thresholds, checked numerically")
    ok = analytic_checks()
    print("    mixed states stable for k < 1/3, saddle for 1/3 < k < 1/2, gone at k >= 1/2; aligned states always stable:", "PASS" if ok else "FAIL")
    fails = [] if ok else ["analytic checks"]

    print("[2] can correlation tell bistability from a common shock?  (matched correlation, matched spread)")
    A, B = sim_bistable(kab=0.3, kba=0.3)
    c_bi = corr(A, B); sd = float(A.std())
    lo, hi = 0.0, 0.99
    for _ in range(14):                       # bisect the common-shock weight to match the correlation
        mid = (lo + hi) / 2
        Ya, Yb = sim_ou_common(mid, sd)
        if corr(Ya, Yb) < c_bi: lo = mid
        else: hi = mid
    Ya, Yb = sim_ou_common((lo + hi) / 2, sd)
    c_ou = corr(Ya, Yb)
    print(f"    bistable pair: corr {c_bi:.3f}, sd {sd:.3f}   |   linear pair + common shock: corr {c_ou:.3f}, sd {Ya.std():.3f}")
    if abs(c_bi - c_ou) > 0.02:
        fails.append("correlation not matched")

    print("[3] the bimodality test on three kinds of series (node A)")
    sv = sim_sv(sd)
    rows = [("bistable pair (truth: multistable)", A, True), ("linear + common shock (truth: not)", Ya, False),
            ("volatility cycle, one mean (truth: not)", sv, False)]
    for name, S, truth in rows:
        dbic, D, flag = bimodal_test(S)
        verdict = "bimodal" if flag else "not bimodal"
        good = (flag == truth)
        print(f"    {name:44s} dBIC {dbic:10.1f}  D {D:5.2f}  -> {verdict:12s} {'ok' if good else 'WRONG'}")
        if not good: fails.append("bimodality verdict on: " + name)
    # what the extra condition buys: BIC alone on the volatility control
    dbic_sv, D_sv, _ = bimodal_test(sv)
    print(f"    (BIC alone would call the volatility cycle bimodal: dBIC {dbic_sv:.1f} > 10 is {dbic_sv > 10}; Ashman D {D_sv:.2f} is what rules it out)")

    print("[4] the satellite question, in the bistable pair: does coupling to the larger node change the smaller one's fate?")
    print("    flips = sign changes summed over 64 paths of 360 time units each after burn-in (a rate, not a probability)")
    print("    k_AB = pull of A on B; k_BA = pull of B on A; B has shallower wells (mB = 0.6)")
    print("    k_AB  k_BA | flips A  flips B | share of time B opposite to A | A flips per 1000 samples: B aligned / B opposite")
    for kab, kba in ((0.0, 0.0), (0.3, 0.0), (0.3, 0.3), (0.0, 0.3), (0.6, 0.0)):
        a, b = sim_bistable(kab, kba, seed=11)
        opp = float(((a > 0.3) & (b < -0.3) | (a < -0.3) & (b > 0.3)).mean())
        al = ((a > 0.3) & (b > 0.3)) | ((a < -0.3) & (b < -0.3))
        # A's flips in the next step, split by whether B was aligned or opposite at the earlier step
        za = np.where(a > 0.3, 1, np.where(a < -0.3, -1, 0)); fa = {True: 0, False: 0}; tm = {True: 0, False: 0}
        for j in range(a.shape[1]):
            col = za[:, j]; bal = al[:, j]; last = 0; lastidx = -1
            for t in range(len(col)):
                if col[t] == 0: continue
                if last != 0 and col[t] != last:
                    fa[bool(bal[lastidx])] += 1
                last = col[t]; lastidx = t
            tm[True] += int(bal.sum()); tm[False] += int((~bal).sum())
        ra = fa[True] / max(tm[True], 1) * 1000; ro = fa[False] / max(tm[False], 1) * 1000
        print(f"    {kab:4.1f}  {kba:4.1f} | {flips(a):7d} {flips(b):7d} | {opp:30.3f} | {ra:7.2f} / {ro:7.2f}")
    print("    Read this table as what the MODEL does under stated couplings. Whether Newark and New York, or any two real")
    print("    economies, sit at any of these rows is a separate question that needs data and is not answered here.")

    print("[5] power at a macro-like length: one path = one series of about 250 points (like quarterly data over 60 years)")
    print("    share of single series each test calls bimodal (64 series per row)")
    def share(S):
        n = 0
        for j in range(S.shape[1]):
            _, _, flag = bimodal_test(S[::7, j:j + 1], sub=1)
            n += flag
        return n / S.shape[1]
    for name, S, truth in rows:
        p = share(S)
        print(f"    {name:44s} called bimodal in {p:5.2f} of series   (truth: {'multistable' if truth else 'not'})")
    print("    the same, with the pair switching less often (smaller noise), as real regimes do; flips per series shown")
    for s in (0.35, 0.30, 0.25):
        a2, _ = sim_bistable(0.3, 0.3, s=s, seed=21)
        print(f"    bistable pair, noise {s:.2f}: {flips(a2[::7]) / a2.shape[1]:5.1f} flips of A per series, called bimodal in {share(a2):5.2f} of series")
    print("    A low share for the bistable pair means: at this length the test misses real multistability, so a")
    print("    'not bimodal' verdict on real macro data would not rule it out.")

    print(f"\n{len(fails)} FAIL" + (": " + "; ".join(fails) if fails else ""))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
