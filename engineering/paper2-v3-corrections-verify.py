#!/usr/bin/env python3
"""Check the four 'Changes in V3' corrections of Paper 2 (dm3_toy_model_v3.tex) against the system printed in its abstract
    rdot = r(1-r^2) + 2(r-1)e^{-z},  thetadot = 1,  zdot = r^2 - 2(r-1)^2 e^{-z}
and scan for the V2-era (early master_book) values. R24: runs before any sentence. R9: no file is changed."""
import os, re, sys
import numpy as np, sympy as sp
fails = []
def check(ok, msg):
    print('    %s  %s' % ('PASS' if ok else 'FLAG', msg))
    if not ok: fails.append(msg)
def head(n, t): print('\n[%d]  %s\n%s' % (n, t, '=' * 72))
r, z, rho, z0, t = sp.symbols('r z rho z0 t', real=True)
F = r * (1 - r**2) + 2 * (r - 1) * sp.exp(-z)
Fp = sp.simplify(sp.diff(F, r).subs(r, 1))

head(1, 'V3 correction (1): flow exponent e^{-4t} -> e^{-2t}')
print('    F_r(1,z) =', Fp, '; on Gamma zdot = 1, so z = z0 + t')
expo = sp.integrate(Fp.subs(z, z0 + t), (t, 0, t))
check(sp.simplify(sp.diff(expo, t).subs(t, 10**3).subs(z0, 0)) == -2 or abs(float(sp.diff(expo, t).subs({t: 50, z0: 0})) + 2) < 1e-9, 'late-time exponent rate is -2 (V3 right, V2 e^{-4t} wrong): d/dt of the exponent at t=50 is %.6f' % float(sp.diff(expo, t).subs({t: 50, z0: 0})))

head(2, 'V3 correction (2): Contact Hopf gamma* = e^{z0} -> 2 e^{z0}')
g = sp.symbols('gamma', positive=True)
lam = -2 + g * sp.exp(-z0)   # general gamma with baseline gamma = 2 reproducing the printed system (-2 + 2e^{-z})
check(sp.simplify(lam.subs(g, 2) - Fp.subs(z, z0)) == 0, 'the printed system is the gamma = 2 member of rho-dot = (-2 + gamma e^{-z}) rho')
check(sp.solve(lam, g)[0] == 2 * sp.exp(z0), 'lambda = 0 gives gamma* = %s (V3 right)' % sp.solve(lam, g)[0])
check(sp.solve(lam.subs(z0, 0), g)[0] == 2, 'at z0 = 0, gamma* = 2 = the paper\'s baseline gamma (V3 consistency check reproduced); V2 gave 1')

head(3, 'V3 correction (3): stationary density exp(-2(r-1)^2/s^2) -> exp(-4(r-1)^2/s^2)   *** NOT SUPPORTED ***')
def stat_var(zz, s0, n=400001):
    x = np.linspace(0.2, 1.8, n); dx = x[1] - x[0]
    Fx = x * (1 - x**2) + 2 * (x - 1) * np.exp(-zz)
    U = -np.cumsum(Fx) * dx
    lp = -2 * U / s0**2; lp -= lp.max(); w = np.exp(lp); w /= w.sum() * dx
    return (w * (x - 1)**2).sum() * dx
s0 = 0.05
print('    |F_r(1)| = 2(1 - e^{-z0}) <= 2 for every z0; V3 proof uses F ~ -4(r-1), which needs |F_r| = 4.')
for zz in (3, 10):
    v = stat_var(zz, s0)
    print('    z0=%-3g numerical stationary variance %.4e ; s0^2/4 = %.4e (V2 density) ; s0^2/8 = %.4e (V3 density)' % (zz, v, s0**2 / 4, s0**2 / 8))
v10 = stat_var(10, s0)
check(abs(v10 / (s0**2 / 4) - 1) < 0.02, 'at z0 = 10 the numerical variance equals s0^2/4 within 2%% (ratio %.4f): V2 formula is the z0->inf limit, V3 variance s0^2/8 is not reached' % (v10 / (s0**2 / 4)))
check(abs(v10 / (s0**2 / 8) - 1) > 0.5, 'and differs from V3\'s s0^2/8 by a factor %.2f' % (v10 / (s0**2 / 8)))
print('    OPEN (author): V3 may intend a different drift or noise scaling than the one printed; as printed, correction (3) is not supported.')
print('    V2\'s erf argument d/(s*sqrt2) does not match its own exp(-2x^2/s^2) either (that density gives erf(sqrt2*d/s)); so V2 had an error here too, and V3\'s 2d/s is right only if k = 4.')

head(4, 'where the V2-era and V3 values appear')
D = os.environ.get('EARLY_DIR', os.path.expanduser('~/Downloads'))
pats = {'V2 Hopf e^{z0}': r'gamma\^\*\s*=\s*e\^\{z_0\}', 'V2 density -2(r-1)^2': r'exp\(-2\(r-1\)\^2/\\sigma_0\^2\)', 'V3 density -4(r-1)^2': r'exp\(-4\(r-1\)\^2/\\sigma_0\^2\)'}
for f in ['master_book_FINAL_v2.tex', 'completePrincipia.tex', 'book321.tex', 'dm3_toy_model_v3.tex']:
    p = os.path.join(D, f)
    if not os.path.exists(p): continue
    s = open(p, errors='ignore').read()
    print('    %-26s ' % f + ', '.join('%s x%d' % (k, len(re.findall(v, s))) for k, v in pats.items()))
print('    repo: vol2-toymodel.html line 408 states the V3 density (variance sigma0^2/8); vol2-contact.html records the Hopf correction as "corrected in V4".')
head(5, 'the V1 deposit itself (Zenodo 19117400, byte-identical local copy) shows where the -4 came from')
import hashlib, subprocess, glob
V1 = {'f0037d1068b11cc9f31b3d43c7b57eb4': 'THE DM3 OPERATOR- EXPLICIT TOY MODEL  AND GLOBAL DYNAMICAL ANALYSIS (1).pdf'}
for md5, name in V1.items():
    path = os.path.join(D, name)
    if not os.path.exists(path): print('    (local V1 PDF not found; skipped)'); continue
    ok = hashlib.md5(open(path, 'rb').read()).hexdigest() == md5
    check(ok, 'local copy matches the md5 printed on the Zenodo record (%s)' % md5)
    txt = subprocess.run(['pdftotext', path, '-'], capture_output=True, text=True).stdout
    t1 = re.sub(r'\s+', ' ', txt)
    check('V\u0307 \u2248 \u22124(r \u2212 1)2 = \u22124V' in t1 or 'c = 4' in t1, 'V1 Axiom 4: Vdot ~ -4(r-1)^2 = -4V, so c = 4 (that is the decay rate of V = (r-1)^2, twice the rate of r-1)')
    check('F \u2248 \u22124(r \u2212 1)' in t1, 'V1 proof of the stationary density writes F ~ -4(r-1) (the V rate, not the drift rate 2)')
    check('exp(\u22122(r \u2212 1)2' in t1, 'yet V1 states rho ~ exp(-2(r-1)^2/s0^2), which IS what drift -2(r-1) gives')
print('    Reading: V1 had a slip in the proof line (-4 instead of -2) with the right final density; V3 changed the final density to match the slip.')
print('\n' + ('FLAGS: %d' % len(fails) if fails else 'all checks passed'))
