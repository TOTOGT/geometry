"""Numerical tests of RH criteria, pre-registered in docs/prereg-rh-criteria.md (2026-10-25).

Usage: python3 docs/rh-criteria-check.py T1 | T2 | T3
Each test prints its control first. A control that does not behave as registered is
reported as VACUOUS and the test result is not to be used.
A pass means no counterexample in the stated range. It is not evidence that RH is true.
"""
import sys, math
import numpy as np
import mpmath as mp

EG = math.exp(0.5772156649015329)


def t1(N=10**7):
    sigma = np.zeros(N + 1, dtype=np.int64)
    r = int(math.isqrt(N))
    for d in range(1, r + 1):
        k = np.arange(d, N // d + 1, dtype=np.int64)
        m = d * k
        sigma[m] += d + k
        sigma[d * d] -= d
    n = np.arange(N + 1, dtype=np.float64)
    n[0] = 1
    H = np.cumsum(1.0 / n)          # H[n] for n>=1 (index 0 adds 1/1, fix below)
    H = H - 1.0                     # undo the dummy n=0 term
    H[0] = 0
    s = sigma.astype(np.float64)
    idx = np.arange(2, N + 1)
    lag_rhs = H[idx] + np.exp(H[idx]) * np.log(H[idx])
    lag_margin = lag_rhs - s[idx]
    print("T1 sanity: sigma(12)=%d (28), sigma(5040)=%d (19344), sigma(N) sieve ok" % (sigma[12], sigma[5040]))
    lag_viol = idx[lag_margin <= 0]
    lag_ctrl = idx[0.95 * lag_rhs - s[idx] <= 0]
    big = np.arange(5041, N + 1)
    lln = np.log(np.log(big.astype(np.float64)))
    rob = EG * big * lln
    rob_margin = rob - s[big]
    rob_viol = big[rob_margin <= 0]
    rob_ctrl = big[0.98 * rob - s[big] <= 0]
    print("CONTROL Lagarias x0.95: violations =", len(lag_ctrl), "first", lag_ctrl[:3], "->", "ok" if len(lag_ctrl) else "VACUOUS")
    print("CONTROL Robin   x0.98: violations =", len(rob_ctrl), "first", rob_ctrl[:3], "->", "ok" if len(rob_ctrl) else "VACUOUS")
    print("Lagarias violations n in [2,%d]: %d" % (N, len(lag_viol)))
    i = int(np.argmin(lag_margin / lag_rhs)); print("  tightest relative margin %.3e at n=%d" % (float((lag_margin / lag_rhs)[i]), int(idx[i])))
    print("Robin violations n in [5041,%d]: %d" % (N, len(rob_viol)))
    j = int(np.argmin(rob_margin / rob)); print("  tightest relative margin %.3e at n=%d" % (float((rob_margin / rob)[j]), int(big[j])))
    ok = (len(lag_ctrl) > 0 and len(rob_ctrl) > 0)
    print("T1 RESULT:", ("PASS (no counterexample to n<=%d; range far too small to bear on RH)" % N) if ok and not len(lag_viol) and not len(rob_viol) else ("FAIL/VACUOUS"))


def t2(T=300.0, h=0.02):
    mp.mp.dps = 20
    ts = [k * h for k in range(1, int(T / h) + 1)]
    Z = [mp.siegelz(t) for t in ts]
    sc = sum(1 for a, b in zip(Z, Z[1:]) if a * b < 0)
    nz = int(mp.nzeros(ts[-1]))
    print("T2: sign changes of Z on (0,%.2f] step %.3f = %d ; N(T) by argument principle = %d" % (ts[-1], h, sc, nz))
    # control: replace first adjacent pair beyond index 10 by a complex pair
    idxs = [i for i in range(len(Z) - 1) if Z[i] * Z[i + 1] < 0]
    a, b = idxs[10], idxs[11]
    t1_, t2_ = ts[a], ts[b]
    c, eps = (t1_ + t2_) / 2, 0.2
    Zc = [z * ((t - c) ** 2 + eps ** 2) / ((t - t1_ - h / 2) * (t - t2_ - h / 2)) for z, t in zip(Z, ts)]
    scc = sum(1 for x, y in zip(Zc, Zc[1:]) if x * y < 0)
    print("CONTROL: pair near t=%.3f,%.3f replaced by complex pair; sign changes = %d (expected %d) -> %s" % (t1_, t2_, scc, sc - 2, "ok" if scc == sc - 2 else "VACUOUS"))
    print("T2 RESULT:", "PASS" if (sc == nz and scc == sc - 2) else "DEFICIT/MISMATCH (re-run with h/4 before calling it)")


def xi(s):
    return 0.5 * s * (s - 1) * mp.pi ** (-s / 2) * mp.gamma(s / 2) * mp.zeta(s)


def dlogxi(s, rho_shift=None):
    # (xi'/xi) by the digamma/zeta' formula: 1/s + 1/(s-1) - log(pi)/2 + psi(s/2)/2 + zeta'/zeta
    v = 1 / s + 1 / (s - 1) - mp.log(mp.pi) / 2 + mp.digamma(s / 2) / 2 + mp.zeta(s, derivative=1) / mp.zeta(s)
    if rho_shift is not None:
        r0, r1 = rho_shift
        v += 1 / (s - r1) - 1 / (s - r0)
    return v


def t3():
    mp.mp.dps = 20
    zeros = [mp.zetazero(k) for k in range(1, 30)]
    sigmas_fine = [0.5005, 0.501, 0.505, 0.51]
    sigmas_all = [0.55, 0.6, 0.75, 1.0, 2.0]
    r0 = zeros[0]
    r1 = mp.mpc(0.52, r0.imag)
    def scan(shift):
        best = (1e9, None)
        for sg in sigmas_fine:
            for rz in zeros:
                t = float(rz.imag) - 0.5
                while t <= float(rz.imag) + 0.5:
                    v = mp.re(dlogxi(mp.mpc(sg, t), shift))
                    if v < best[0]: best = (float(v), (sg, round(t, 3)))
                    t += 0.01
        for sg in sigmas_all:
            t = 0.5
            while t <= 100:
                v = mp.re(dlogxi(mp.mpc(sg, t), shift))
                if v < best[0]: best = (float(v), (sg, round(t, 3)))
                t += 0.05
        return best
    ctrl = scan((r0, r1))
    print("CONTROL: first zero moved to Re s=0.52; min Re(xi'/xi) = %.4g at (sigma,t)=%s (zero1 t=%.4f) -> %s" % (ctrl[0], ctrl[1], float(r0.imag), "ok" if ctrl[0] < 0 and abs(ctrl[1][1] - float(r0.imag)) < 0.05 else "VACUOUS"))
    real = scan(None)
    print("T3: min Re(xi'/xi) over grid = %.6g at (sigma,t)=%s" % (real[0], real[1]))
    print("T3 RESULT:", "PASS (min > 0 on grid)" if real[0] > 0 and ctrl[0] < 0 else "FAIL/VACUOUS")


if __name__ == "__main__":
    {"T1": t1, "T2": t2, "T3": t3}[sys.argv[1]]()
