"""ch12.html: sign convention for g, Result 12.1 and the pole value.

Lean (ZetaReflection.lean): Zlog = logDeriv zeta;  c = Re(-Zlog);  g = Im(Zlog) = Im(zeta'/zeta).
Result 12.1 (page): g(s,t) - g(1-s,t) = Im[(chi'/chi)(sigma+it)],
  (chi'/chi)(s) = log pi - psi(s/2)/2 - psi((1-s)/2)/2.
Page prose says c, g are 'the real and imaginary parts of -zeta'/zeta': true for c, opposite sign for g.
"""
import mpmath as mp
mp.mp.dps = 30
lz = lambda s: mp.zeta(s, derivative=1) / mp.zeta(s)
chi = lambda s: mp.log(mp.pi) - mp.digamma(s / 2) / 2 - mp.digamma((1 - s) / 2) / 2
pts = [(0.3, 0.7), (0.5, 7.0), (0.8, 3.0), (1.1, 12.0), (1.5, 18.0), (2.3, 25.0), (0.3, 25.0), (0.8, 0.7)]
worstL = worstP = 0
for sg, t in pts:
    s = mp.mpc(sg, t)
    g_lean = lambda a, b: mp.im(lz(mp.mpc(a, b)))            # Lean convention
    lhs = g_lean(sg, t) - g_lean(1 - sg, t)
    rhs = mp.im(chi(s))
    worstL = max(worstL, abs(lhs - rhs))
    g_prose = lambda a, b: mp.im(-lz(mp.mpc(a, b)))          # 'imaginary part of -zeta/zeta'
    worstP = max(worstP, abs((g_prose(sg, t) - g_prose(1 - sg, t)) - rhs))
print('Result 12.1, g = Im(zeta\'/zeta) (Lean):        max error over %d points = %s' % (len(pts), mp.nstr(worstL, 3)))
print('Result 12.1, g = Im(-zeta\'/zeta) (page prose):  max error over %d points = %s' % (len(pts), mp.nstr(worstP, 3)))
g1 = mp.im(mp.zetazero(1))
for d in (mp.mpf('1e-3'), mp.mpf('1e-4')):
    v = lz(mp.mpc(0.5, g1 + d))
    print('delta=%s: Im(zeta\'/zeta)=%s  Im(-zeta\'/zeta)=%s' % (d, mp.nstr(mp.im(v), 9), mp.nstr(-mp.im(v), 9)))
