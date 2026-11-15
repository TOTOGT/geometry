#!/usr/bin/env python3
"""ch12_audit_check.py -- read-only checks complementing ch12_reflection_signcheck.py (audit 2026-11-15). mpmath."""
import sys, os, re, mpmath as mp
mp.mp.dps = 30
bad = 0
def ck(n, ok):
    global bad; bad += (not ok); print(('PASS ' if ok else 'FAIL ') + n)
lz = lambda s: mp.zeta(s, derivative=1)/mp.zeta(s)
chi = lambda s: mp.log(mp.pi) - mp.digamma(s/2)/2 - mp.digamma((1-s)/2)/2
# 1. Mathlib-form identity quoted in 12.7: Zlog(s) = -Zlog(1-s) + log(2pi) - psi(s) + (pi/2) tan(pi s/2)
pts = [mp.mpc(0.3, 0.7), mp.mpc(0.5, 7), mp.mpc(2.3, 5), mp.mpc(-0.4, 3), mp.mpc(1.7, -2)]
err = max(abs(lz(s) - (-lz(1-s) + mp.log(2*mp.pi) - mp.digamma(s) + mp.pi/2*mp.tan(mp.pi*s/2))) for s in pts)
ck('Mathlib form of the reflection identity holds (err %s)' % mp.nstr(err, 3), err < mp.mpf(10)**-20)
# 2. Same identity via chi'/chi (Result 12.1 / 12.2 combined): zeta'/zeta(s) = chi'/chi(s) - zeta'/zeta(1-s)
err2 = max(abs(lz(s) - (chi(s) - lz(1-s))) for s in pts)
ck('zeta\'/zeta(s) = chi\'/chi(s) - zeta\'/zeta(1-s) (err %s)' % mp.nstr(err2, 3), err2 < mp.mpf(10)**-20)
# 3. 'g(s,t)=g(1-s,t) holds identically on sigma=1/2 and on no other vertical line': Im chi'/chi
vals = {sg: [abs(mp.im(chi(mp.mpc(sg, t)))) for t in (0.7, 3, 9, 25)] for sg in (0.5, 0.3, 0.8, 1.1, 2.3)}
ck('Im chi\'/chi = 0 for all sampled t at sigma=1/2, nonzero at every sampled t for the other sigma',
   max(vals[0.5]) < mp.mpf(10)**-25 and all(min(v) > mp.mpf(10)**-6 for k, v in vals.items() if k != 0.5))
# 4. c(1/2,t) = theta'(t)
th = lambda t: mp.siegeltheta(t)
e4 = max(abs(-mp.re(lz(mp.mpc(0.5, t))) - mp.diff(th, t)) for t in (0.7, 3, 14.2, 50, 100))
ck('c(1/2,t) = -Re zeta\'/zeta(1/2+it) = theta\'(t) (err %s)' % mp.nstr(e4, 3), e4 < mp.mpf(10)**-18)
# 5. 'its integral along the wall counts the zeros': N(T) = theta/pi + 1 + S(T)
T = 50
N = sum(1 for k in range(1, 30) if mp.zetazero(k).imag < T)
smooth = th(T)/mp.pi + 1
ck('N(50)=%d; smooth part theta/pi+1 = %s; S(T) = %s != 0, so the smooth integral does not count zeros exactly' % (N, mp.nstr(smooth, 6), mp.nstr(N-smooth, 4)), abs(N-smooth) > 0.05)
# 6. Pole sign: g(1/2, gamma+delta) ~ -1/delta
g1 = mp.zetazero(1).imag
gv = mp.im(lz(mp.mpc(0.5, g1+mp.mpf('1e-3'))))
ck('g(1/2,gamma1+1e-3) = %s ~ -1000' % mp.nstr(gv, 8), abs(gv + 1000.08) < 0.01)
# 7. Lean file declaration counts
def count(p):
    if not os.path.isfile(p): return None
    return len(re.findall(r'^\s*(?:theorem|lemma)\s', open(p, encoding='utf-8', errors='replace').read(), re.M))
for p in ('book4/ZetaReflection.lean', 'book4/ZetaReflection.points.lean'):
    print('INFO', p, 'theorem/lemma declarations:', count(p))
print('NOTE hand argument, not computed: central-claim box states the contactomorphism as fact; Conjecture 12.2 and the status table call it open.')
print('NOTE hand argument, not computed: Mathlib PR #43252 and its merge date were not verified (no network check made).')
sys.exit(1 if bad else 0)
