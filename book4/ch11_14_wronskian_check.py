#!/usr/bin/env python3
"""Audit evidence for book4/ch11.html, ch13.html, ch14.html (2026-11-14). Read-only: edits nothing.

Conventions are the pages' own: -zeta'/zeta(sigma+it) = c - i g, with
c = sum Lambda(n) n^-sigma cos(t log n), g = sum Lambda(n) n^-sigma sin(t log n) (series: sigma > 1),
W = c dg/dt - g dc/dt, and alpha^dalpha = -W dU^dt^dV.
For sigma <= 1 the script uses the meromorphic continuation (mpmath zeta and its derivatives).
A PASS means the line printed is what was computed; several PASS lines record that a page
statement does NOT hold. Read the text of each line.
"""
import math, sys, time
import numpy as np
from mpmath import mp, zeta, mpc, mpf, log as mlog
mp.dps = 25
fails = 0
def check(name, ok):
    global fails
    print(("PASS " if ok else "FAIL ") + name); fails += (not ok); sys.stdout.flush()

def H_and_dt(sig, t):
    s = mpc(sig, t); z = zeta(s); z1 = zeta(s, derivative=1); z2 = zeta(s, derivative=2)
    H = -z1 / z; Hp = -(z2 * z - z1 * z1) / (z * z); d = 1j * Hp      # dH/dt = i H'(s)
    return H, d
def cgW(sig, t):
    H, d = H_and_dt(sig, t)
    c, g, ct, gt = H.real, -H.imag, d.real, -d.imag
    return c, g, c * gt - g * ct

def mangoldt(N):
    lam = np.zeros(N + 1); sieve = np.ones(N + 1, bool); sieve[:2] = False
    for p in range(2, N + 1):
        if sieve[p]:
            sieve[2 * p::p] = False
            q = p
            while q <= N:
                lam[q] = math.log(p); q *= p
    return lam, np.nonzero(sieve)[0]
LAM, PRIMES = mangoldt(200000)
NZ = np.nonzero(LAM)[0]

# ---- [1] ch11 sec 11.5: velocity of log zeta and the kernel identity ----
sig, t, h = 0.8, mpf("17.3"), mpf("1e-8")
dlog = (mlog(zeta(mpc(sig, t + h))) - mlog(zeta(mpc(sig, t - h)))) / (2 * h)
c, g, _ = cgW(sig, t)
check("[1] d/dt log zeta = (-g, -c) at sigma=0.8, t=17.3 (err %.1e)" % max(abs(dlog.real + g), abs(dlog.imag + c)),
      max(abs(dlog.real + g), abs(dlog.imag + c)) < 1e-10)
check("[1] alpha(velocity) = c(-g) - g(-c) = 0 identically", c * (-g) - g * (-c) == 0)

# ---- [2] the series for c converges only for sigma > 1; Prop 11.1 is stated for sigma > 1/2 ----
def c_partial(sig, t, N):
    n = NZ[NZ <= N]; return float(np.sum(LAM[n] * n ** (-sig) * np.cos(t * np.log(n))))
t0 = 20.0
ref2 = float(cgW(2.0, t0)[0]); ps2 = [c_partial(2.0, t0, N) for N in (1000, 10000, 100000, 200000)]
check("[2] sigma=2: partial sums of c settle on the continuation value (%.6f; last two differ by %.1e)" % (ref2, abs(ps2[-1] - ps2[-2])),
      abs(ps2[-1] - ref2) < 1e-4)
ref = float(cgW(0.75, t0)[0]); ps = [c_partial(0.75, t0, N) for N in (1000, 10000, 100000, 200000)]
print("    sigma=0.75, t=20: continuation c = %.4f; partial sums N=1e3,1e4,1e5,2e5: %s" % (ref, ", ".join("%.3f" % v for v in ps)))
check("[2] sigma=0.75, t=20: partial sums of c do not settle (spread %.2f over N = 1e3..2e5): consistent with divergence; NOT a proof. Justification used on the page: a convergent complex Dirichlet series would be analytic on Re s > Re s0, which contains the pole of -zeta'/zeta at s=1 when Re s0 < 1, so the complex series diverges for every sigma<1; at least one of c, g diverges; at t=0 g's terms are all zero while c diverges" % (max(ps) - min(ps)),
      max(ps) - min(ps) > 0.5)
check("[2] t=0: every term of the g-series is zero (so g alone converges there for every sigma)", all(math.sin(0 * math.log(n)) == 0 for n in range(1, 50)))

# ---- [3] Prop 11.1 on sigma > 1: W has positive mean sum Lambda^2 log n / n^(2 sigma), so W is not identically 0 ----
sig = 2.0; n = NZ[NZ <= 3000]; a = LAM[n] * n ** (-sig); ln = np.log(n)
tt = np.arange(0.0, 4000.0, 0.05); acc = 0.0
for i in range(0, len(tt), 4000):
    T = tt[i:i + 4000][:, None] * ln[None, :]
    C, S = np.cos(T), np.sin(T)
    cc, gg = np.einsum('ij,j->i', C, a), np.einsum('ij,j->i', S, a); ct, gt = -np.einsum('ij,j->i', S, a * ln), np.einsum('ij,j->i', C, a * ln)
    acc += float(np.sum(cc * gt - gg * ct))
meanW = acc / len(tt); pred = float(np.sum(a * a * ln))
check("[3] sigma=2: time-average of W over [0,4000] = %.6f vs sum Lambda(n)^2 log n / n^4 = %.6f" % (meanW, pred), abs(meanW - pred) < 0.02 * pred)
f = 3 + np.cos(tt) + np.cos(math.sqrt(2) * tt)
check("[3] the sketch's lemma needs zero mean: 3 + cos t + cos(sqrt2 t) is almost periodic and never changes sign", f.min() > 0)
# the closed form used on the page: W = sum_{m,n} L(m)L(n) log n (mn)^-sigma cos(t(log m - log n))
sg, tg = 2.0, 7.3; nn = NZ[NZ <= 3000]; aa = LAM[nn] * nn.astype(float) ** (-sg); ll = np.log(nn)
Wser = float(np.sum(aa[:, None] * aa[None, :] * ll[None, :] * np.cos(tg * (ll[:, None] - ll[None, :]))))
Wan = float(cgW(sg, mpf(tg))[2])
check("[3] double-series closed form for W (truncated at n,m <= 3000) matches the analytic W at sigma=2, t=7.3 (%.8f vs %.8f; truncation tail ~1e-5)" % (Wser, Wan), abs(Wser - Wan) < 2e-5)
print("    => on sigma > 1 W is real-analytic with positive mean, hence not identically zero and with isolated zeros.")
print("       A positive mean does not rule out sign changes (see [6], sigma=2: W<0 at isolated points); the page's old")
print("       'dense sign changes' is incompatible with isolated zeros. Only log m != log n (m != n) is used, not independence of log p.")

# ---- [4] ch13: the local coefficient g_p ----
def gp_series(p, sig, t, K=400): return sum(math.log(p) * p ** (-k * sig) * math.sin(k * t * math.log(p)) for k in range(1, K))
def gp_sec133(p, sig, t): return math.log(p) * p ** -sig * math.sin(t * math.log(p)) / (1 - 2 * p ** -sig * math.cos(t * math.log(p)) + p ** (-2 * sig))
def gp_box(p, sig, t): return p ** -sig * math.sin(t * math.log(p)) / (1 - p ** (-2 * sig))
def im_local(p, sig, t):
    z = p ** complex(-sig, -t); return (math.log(p) * z / (1 - z)).imag
p, sig, t = 3, 1.3, 2.7
check("[4] sec 13.3 closed form equals the prime-power series sum_k log p p^(-k sigma) sin(k t log p) (%.6f)" % gp_sec133(p, sig, t),
      abs(gp_sec133(p, sig, t) - gp_series(p, sig, t)) < 1e-12)
check("[4] but Im(log p p^-s/(1-p^-s)) = %.6f = MINUS that: the displayed equality in sec 13.3 has the wrong sign" % im_local(p, sig, t),
      abs(im_local(p, sig, t) + gp_sec133(p, sig, t)) < 1e-12)
check("[4] header-box formula p^-sigma sin(t log p)/(1-p^(-2 sigma)) = %.6f does not equal g_p = %.6f" % (gp_box(p, sig, t), gp_sec133(p, sig, t)),
      abs(gp_box(p, sig, t) - gp_sec133(p, sig, t)) > 1e-3)
tot = sum(gp_sec133(int(q), 2.0, 20.0) for q in PRIMES); gref = float(cgW(2.0, 20.0)[1])
check("[4] sigma=2: sum over primes of g_p = g (%.8f vs %.8f)" % (tot, gref), abs(tot - gref) < 1e-5)
den0 = 1 - 2 * 2 ** -0.5 + 0.5; den1 = 1 - 2 * 2 ** -0.5 * math.cos(14.13 * math.log(2)) + 0.5
print("    Task 2: denominator of g_2 at sigma=0.5 is %.4f at t=0 and %.4f at t=14.13; g_2(0.5,14.13) = %.4f" % (den0, den1, gp_sec133(2, 0.5, 14.13)))
check("[4] Task 2: nothing happens to g_2 at the first zeta zero (no single Euler factor sees it; its poles are on sigma=0)", 0.05 < den1 < 4 and abs(gp_sec133(2, 0.5, 14.13)) < 2)

# ---- [5] the figures ----
def js_zeta(sig, t, N):                      # ch11.html lines 584-594: plain partial sum of n^-s
    n = np.arange(1, N + 1); return complex(np.sum(n ** -sig * np.cos(t * np.log(n))), -np.sum(n ** -sig * np.sin(t * np.log(n))))
g1 = 14.134725141734693
v = abs(js_zeta(0.5, g1, 300)); tr = abs(zeta(mpc(0.5, g1)))
check("[5] Fig 11.1 code at sigma=0.5, N=300, first zero: |partial sum| = %.3f while |zeta| = %.1e: the drawn curve does not pass through the origin" % (v, tr), v > 0.5 and tr < 1e-10)
dmin = min(abs(js_zeta(0.5, x, 300)) for x in np.arange(10, 30, 0.005))
print("    closest approach of the drawn sigma=0.5 curve to the origin for t in [10,30]: %.3f" % dmin)
def euler(sig, t, P):
    out = 1 + 0j
    for q in PRIMES[PRIMES <= P]: out /= (1 - int(q) ** complex(-sig, -t))
    return out
z7 = euler(1.0, 14.13, 17); zt = complex(zeta(mpc(1.0, 14.13)))
print("    Fig 13.1 default (sigma=1, t=14.13): 7-prime product = %.3f%+.3fi, zeta = %.3f%+.3fi" % (z7.real, z7.imag, zt.real, zt.imag))
e = [abs(euler(0.75, 14.13, P) - complex(zeta(mpc(0.75, 14.13)))) for P in (17, 1000, 100000)]
print("    sigma=0.75, t=14.13: |product - zeta| = %.3f, %.3f, %.3f for p<=17, 1e3, 1e5 (stops improving; the divergence is slow," % tuple(e))
print("      amplitude about P^(1-sigma)/(|1-s| log P), so this scale does not show it; recorded as not demonstrated here)")
z0 = float(zeta(mpf("0.75"))); pr = [euler(0.75, 0.0, P).real for P in (17, 1000, 100000)]
check("[5] slider range includes sigma=0.75, t=0: zeta = %.3f but the products are %.2f, %.2f, %.2f and growing: no convergence for sigma <= 1" % ((z0,) + tuple(pr)),
      z0 < 0 and pr[0] > 0 and pr[2] > pr[1] > pr[0])
e2 = [abs(euler(2.0, 14.13, P) - complex(zeta(mpc(2.0, 14.13)))) for P in (17, 1000, 100000)]
check("[5] control sigma=2: it does (errors %.1e, %.1e, %.1e)" % tuple(e2), e2[-1] < 1e-5)

# ---- [6] ch14: the Global Positivity condition, read as the page says: the sign of W ----
print("    W(sigma,t) sampled for t in [1,100), step 0.2:")
t1 = time.time(); res = {}
for sig in (0.10, 0.25, 0.49, 0.50, 0.51, 0.75, 0.99, 1.20, 2.00):
    vals = [float(cgW(sig, mpf(1) + mpf(k) / 5)[2]) for k in range(495)]
    res[sig] = vals
    print("      sigma=%.2f: W<0 at %3d of %d points, min %.4g, max %.4g" % (sig, sum(v < 0 for v in vals), len(vals), min(vals), max(vals)))
    sys.stdout.flush()
check("[6] left half 0<sigma<1/2: W takes both signs at every sampled sigma (no definite sign there)",
      all(min(res[s]) < 0 < max(res[s]) for s in (0.10, 0.25, 0.49)))
check("[6] on sigma=1/2: W does not degenerate; it is positive at every sample (min %.4f) and unbounded near zeros" % min(res[0.50]), min(res[0.50]) > 0)
check("[6] right half: W>0 at every sample for sigma=0.51 and 0.75, but W<0 at sigma=0.99 (min %.3f): positivity off the critical line fails for some 1/2<sigma<1 too" % min(res[0.99]),
      min(res[0.51]) > 0 and min(res[0.75]) > 0 and min(res[0.99]) < 0)
check("[6] sigma>1: W changes sign (as the page already says of this region)", min(res[1.20]) < 0 and min(res[2.00]) < 0)
c_, g_, W_ = cgW(0.25, mpf("59.35")); hh = mpf("1e-6")
ca, ga, _ = cgW(0.25, mpf("59.35") + hh); cb, gb, _ = cgW(0.25, mpf("59.35") - hh)
fd = c_ * (ga - gb) / (2 * hh) - g_ * (ca - cb) / (2 * hh)
check("[6] control: W at (0.25, 59.35) by formula %.5f and by finite differences %.5f agree" % (W_, fd), abs(W_ - fd) < 1e-4)
print("    heuristic reading (not checked here): near a zero rho = 1/2 + i gamma, -zeta'/zeta ~ -1/(s-rho), whose argument turns one way for sigma > 1/2")
print("    and the other way for sigma < 1/2; W = -|c - i g|^2 d/dt arg(c - i g), so W -> +inf on the right and -inf on the left.")
print("    (%.0f s)" % (time.time() - t1))
sys.exit(1 if fails else 0)
