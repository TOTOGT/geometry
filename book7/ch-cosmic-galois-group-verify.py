#!/usr/bin/env python3
"""Regression and numerical checks for book7/ch-cosmic-galois-group.html  (revision 2).

Usage:  python3 ch-cosmic-galois-group-verify.py [--k4] [--hi]
        --k4  run the (expensive, inconclusive) quasi-Monte-Carlo K4 period estimate
        --hi  also run the Bessel moments at 80 digits (slow)

Statuses
  PASS          a valid assertion passed its test
  REJECTED      a deliberately FALSE assertion was correctly rejected (a successful negative control)
  FAIL          a valid assertion failed, or a false assertion was ACCEPTED  -> exit code 1
  INFO          printed value, no verdict
  INCONCLUSIVE  evidence too weak to decide; never counted as a pass
  SKIP          test not executed

Mapping to the chapter (HTML):
  block 1  Part II   A2 closed form, Proposition 1
  block 2  Part IV   Bessel moments (NUMERICAL; source fidelity NOT checked, see [SOURCES])
  block 3  Part VII  Propositions 2, 3 (+3b projectors), 4  -- finite-r REGRESSION tests, not proofs;
                     the general proofs are in the chapter
  block 4  Part VII  Props 5-6 and the counterexamples (r=1, r=2, F(s)=(s-1/2)^2-1/16)
  block 5  Part III  K4: exact spanning-tree count (always); period estimate (opt-in, inconclusive)

[HONESTY] Nothing here tests the Riemann hypothesis or any zero location. Numerical agreement is not a proof.
[SOURCES] Source audit (2026-11-25), read through a summarising fetch tool, so equation numbers/pages are as reported and
should be confirmed in the PDFs: BBBG arXiv:0801.0891 (c_{3,1}: Sec 3.2/eq (63)/Table 1; c_{4,1}: Sec 4.3/eq (67);
int t I0 K0^4 = s_{5,1}: eq (95), a CONJECTURE there, checked to 1200 digits; theta form of C: eq (93)); Zhou arXiv:1706.08308
Thm 2.2.2 proves it (also credited to Bloch-Kerr-Vanhove, Samart); Schnetz arXiv:0801.2856 Example 2.8 / Table 4: P_3 = 6 zeta(3),
stated for the COMPLETED graph K5 whose decompletion is K4 (identification not read in the source).
"""
import itertools, random, sys, time, platform
from fractions import Fraction as Fr
import mpmath
from mpmath import mp, mpf, mpc, zeta, pi, log, quad, besselk, besseli, inf, gamma, sqrt, log10

T0 = time.time()
cnt = dict(PASS=0, REJECTED=0, FAIL=0, INFO=0, INCONCLUSIVE=0, SKIP=0)
def say(status, name, info=""):
    cnt[status] += 1
    print(f"{status:<12} {name}" + (f"  [{info}]" if info else ""))
def pos(name, ok, info=""): say("PASS" if ok else "FAIL", name, info)
def neg(name, false_claim_holds, info=""):
    """negative control: the claim is deliberately false; if our machinery accepts it, that is a FAIL."""
    say("FAIL" if false_claim_holds else "REJECTED", "CONTROL " + name, info)

# ---------------------------------------------------------------- 1. two-loop QED coefficient
mp.dps = 30
C4 = mpf(197)/144 + pi**2/12 + mpf(3)/4*zeta(3) - pi**2/2*log(2)
REF = mpf("-0.328478965579193784")   # value of the closed form itself, reproduced at higher precision below
mp.dps = 50
C4hi = mpf(197)/144 + pi**2/12 + mpf(3)/4*zeta(3) - pi**2/2*log(2)
mp.dps = 30
pos("A2 closed form value agrees between 30- and 50-digit evaluation", abs(C4 - C4hi) < mpf("1e-28"), str(C4)[:22])
pos("A2 closed form = -0.328478965579193...", abs(C4 - REF) < mpf("1e-15"), "this checks the formula's value, not the diagram calculation")
pos("pi^2/12 == zeta(2)/2", abs(pi**2/12 - zeta(2)/2) < mpf("1e-28"))
pos("pi^2/2 == 3 zeta(2)  (Proposition 1)", abs(pi**2/2 - 3*zeta(2)) < mpf("1e-28"))
neg("A2 with the zeta(3) sign flipped equals the same value", abs((mpf(197)/144 + pi**2/12 - mpf(3)/4*zeta(3) - pi**2/2*log(2)) - C4) < mpf("1e-6"))

# ---------------------------------------------------------------- 2. Bessel moments (NUMERICAL)
def moments(dps, pts):
    mp.dps = dps
    K = lambda n, k: quad(lambda t: t**k*besselk(0, t)**n, pts)
    c41 = K(4, 1); c31 = K(3, 1)
    j = quad(lambda t: t*besseli(0, t)*besselk(0, t)**4, pts)
    L3 = (zeta(2, mpf(1)/3) - zeta(2, mpf(2)/3))/9          # L(chi_-3, 2) via Hurwitz zeta
    Cc = gamma(mpf(1)/15)*gamma(mpf(2)/15)*gamma(mpf(4)/15)*gamma(mpf(8)/15)/(240*sqrt(5)*pi**2)
    c51 = K(5, 1)
    return dict(d41=abs(c41 - 7*zeta(3)/8), d31=abs(c31 - mpf(3)/4*L3), dj=abs(j - pi**2*Cc),
                c51=c51, pC=pi**2*Cc, vals=(c41, c31, j))
def digits(d, cap): return float(cap) if d == 0 else (float(-log10(d)) if d < 1 else 0.0)   # difference exactly 0 at working precision => agreement to the cap
levels = [30, 50] + ([80] if "--hi" in sys.argv else [])
PTS_A = [0, 1, 5, 20, inf]; PTS_B = [0, mpf(1)/2, 2, 10, 40, inf]
base = None
for dps in levels:
    r = moments(dps, PTS_A); rb = moments(dps, PTS_B)
    for key, label in (("d41", "c_{4,1} = 7 zeta(3)/8"), ("d31", "c_{3,1} = (3/4) L(chi_-3,2)"), ("dj", "int t I0 K0^4 = pi^2 C")):
        meas = digits(r[key], dps)
        ok = meas >= dps - 10                   # require agreement to within 10 digits of the working precision
        pos(f"{label} at {dps} digits", ok, f"measured agreement ~{meas:.0f} digits; NUMERICAL")
    stab = max(abs(a - b) for a, b in zip(r["vals"], rb["vals"]))
    pos(f"integration-interval stability at {dps} digits", stab < mpf(10)**(-(dps - 10)), f"max change {mpmath.nstr(stab,3)}")
    if dps == levels[-1]: base = r
# omitted tail: integrand t*I0*K0^4 <= t*e^t*(pi/(2t))^2*e^{-4t}... bound tail beyond T by explicit integral of a majorant
mp.dps = 30
Tcut = mpf(60)
maj = lambda t: t*besseli(0, t)*besselk(0, t)**4
tail = quad(maj, [Tcut, 2*Tcut, inf])
# rigorous majorant: I0(t) <= e^t and K0(t) <= sqrt(pi/(2t)) e^{-t}  =>  t I0 K0^4 <= (pi^2/4) e^{-3t}/t, so tail <= pi^2 e^{-3T}/(12 T)
bound = pi**2*mpmath.exp(-3*Tcut)/(12*Tcut)
pos("tail of int t I0 K0^4 beyond t=60 lies below the rigorous majorant pi^2 e^{-3T}/(12T)", tail <= bound, f"computed tail {mpmath.nstr(tail,3)} <= bound {mpmath.nstr(bound,3)} (the integral above uses an infinite endpoint, not 60)")
# sanity of the two ingredient inequalities at sample points
pos("I0(t) <= e^t and K0(t) <= sqrt(pi/(2t)) e^{-t} at sample points t=0.01..60", all(besseli(0,t) <= mpmath.exp(t) and besselk(0,t) <= sqrt(pi/(2*t))*mpmath.exp(-t) for t in [mpf('0.01'),mpf('0.1'),1,2,5,10,30,60]), "spot check of the inequalities proved in the chapter")
# theta-series form of C (Bailey-Borwein-Broadhurst-Glasser, as reported) equals the Gamma-product form
Cth = (pi/16)*(1 - 1/sqrt(5))*(1 + 2*mpmath.nsum(lambda n: mpmath.exp(-n**2*pi*sqrt(15)), [1, inf]))**4
Cgam = gamma(mpf(1)/15)*gamma(mpf(2)/15)*gamma(mpf(4)/15)*gamma(mpf(8)/15)/(240*sqrt(5)*pi**2)
pos("theta-series form of C equals the Gamma-product form (30 digits)", abs(Cth - Cgam) < mpf("1e-28"), "reconciles the two normalisations quoted in the literature")
neg("int t K0^5 = pi^2 C (a misremembered pairing)", base["c51"] - base["pC"] < mpf("1e-10") and abs(base["c51"] - base["pC"]) < mpf("1e-10"),
    f"int t K0^5 = {mpmath.nstr(base['c51'],10)} vs pi^2 C = {mpmath.nstr(base['pC'],10)}")
neg("c_{3,1} = L(chi_-3,2) (wrong factor)", abs(base["vals"][1] - (zeta(2, mpf(1)/3) - zeta(2, mpf(2)/3))/9) < mpf("1e-6"))
say("INFO", "Bessel identities: literature status and exact equation numbers NOT verified by this script")

# ---------------------------------------------------------------- 3. reversal-reflection algebra (exact)
mp.dps = 30
random.seed(1)
def rnd(r): return tuple(Fr(random.randint(-20, 20), random.randint(1, 7)) for _ in range(r))
def R(s): return tuple(1 - x for x in reversed(s))
def matmul(A, B): return [[sum(A[i][k]*B[k][j] for k in range(len(B))) for j in range(len(B[0]))] for i in range(len(A))]
def eye(r): return [[Fr(int(i == j)) for j in range(r)] for i in range(r)]
def Jm(r): return [[Fr(int(j == r-1-i)) for j in range(r)] for i in range(r)]
def lin(a, A, b, B): return [[a*x + b*y for x, y in zip(ra, rb)] for ra, rb in zip(A, B)]
def rank(M):
    M = [row[:] for row in M]; rk = 0; rows = len(M); cols = len(M[0])
    for c in range(cols):
        p = next((i for i in range(rk, rows) if M[i][c] != 0), None)
        if p is None: continue
        M[rk], M[p] = M[p], M[rk]
        for i in range(rows):
            if i != rk and M[i][c] != 0:
                f = M[i][c]/M[rk][c]; M[i] = [a - f*b for a, b in zip(M[i], M[rk])]
        rk += 1
    return rk
RMAX = 12
for r in range(1, RMAX+1):
    I = eye(r); J = Jm(r); A = lin(-1, J, 0, I)
    Pp = lin(Fr(1,2), I, Fr(-1,2), J)     # (I-J)/2 : projector onto the +1 eigenspace of A=-J (fixed space)
    Pm = lin(Fr(1,2), I, Fr(1,2), J)      # (I+J)/2 : projector onto the -1 eigenspace
    ok2 = all(R(R(s)) == s for s in (rnd(r) for _ in range(100))) and matmul(J, J) == I
    pos(f"Prop 2: R^2 = id, J^2 = I (r={r})", ok2)
    pos(f"Prop 3b: P+^2=P+, P-^2=P-, P+P-=0, P++P-=I (r={r})",
        matmul(Pp, Pp) == Pp and matmul(Pm, Pm) == Pm and all(x == 0 for row in matmul(Pp, Pm) for x in row) and lin(1, Pp, 1, Pm) == I)
    pos(f"Prop 3b: A P+ = P+, A P- = -P- (r={r})", matmul(A, Pp) == Pp and matmul(A, Pm) == lin(-1, Pm, 0, I))
    dp, dm = rank(Pp), rank(Pm)
    pos(f"Prop 3: computed dim(+1)=floor(r/2), dim(-1)=ceil(r/2) (r={r})", dp == r//2 and dm == (r+1)//2, f"{dp},{dm}")
    ker = r - rank(lin(1, A, -1, I))      # dimension of ker(A - I), computed independently of the projector
    pos(f"Prop 3: dim ker(A-I) = rank P+ (r={r})", ker == dp)
    # fixed-point construction
    m = r//2; s = [None]*r; free = [Fr(random.randint(-9, 9), 3) for _ in range(m)]
    for i in range(m): s[i] = free[i]; s[r-1-i] = 1 - free[i]
    if r % 2: s[m] = Fr(1, 2)
    pos(f"Prop 3: constructed point with floor(r/2) free parameters is fixed (r={r})", R(tuple(s)) == tuple(s))
    # Prop 4 both directions
    ok4 = True
    for k in range(1, r+1):
        for _ in range(25):
            u = list(rnd(r)); u[k-1] += k - sum(u[:k])             # u in H_k : s1+..+sk = k
            ok4 &= (sum(R(tuple(u))[r-k:]) == 0)
            w = list(rnd(r)); w[r-1] -= sum(w[r-k:])               # w in H'_k : s_{r-k+1}+..+s_r = 0
            ok4 &= (sum(R(tuple(w))[:k]) == k)
    pos(f"Prop 4: R maps H_k onto H'_k and H'_k onto H_k, all k (r={r})", ok4)
# negative controls on the COMPUTED dimensions
wrong = [r for r in (1, 3, 5, 7, 9, 11) if rank(lin(Fr(1,2), eye(r), Fr(-1,2), Jm(r))) == (r+1)//2]
neg("computed dim of the fixed space equals ceil(r/2) for some odd r", bool(wrong), f"offending r: {wrong}")
neg("P+ is not idempotent for r=5 (negation of the verified fact)", matmul(lin(Fr(1,2), eye(5), Fr(-1,2), Jm(5)), lin(Fr(1,2), eye(5), Fr(-1,2), Jm(5))) != lin(Fr(1,2), eye(5), Fr(-1,2), Jm(5)))
neg("R(s)=s has solutions with s_1+s_r != 1 (r=4)", any(R(p) == p and p[0]+p[3] != 1 for p in (rnd(4) for _ in range(3000))))

# ---------------------------------------------------------------- 4. counterexamples to 'symmetry confines zeros'
F = lambda s: (s - mpf(1)/2)**2 - mpf(1)/16
pts = [mpc(random.uniform(-3, 3), random.uniform(-9, 9)) for _ in range(50)]
pos("F(s)=(s-1/2)^2-1/16:  F(1-s)=F(s)", all(abs(F(1-s) - F(s)) < mpf("1e-25") for s in pts))
pos("F(s)=(s-1/2)^2-1/16:  F(conj s)=conj F(s)", all(abs(F(s.conjugate()) - F(s).conjugate()) < mpf("1e-25") for s in pts))
exactF = lambda s: (s - Fr(1, 2))**2 - Fr(1, 16)
pos("F has zeros exactly 1/4 and 3/4 (exact rational arithmetic)", exactF(Fr(1, 4)) == 0 and exactF(Fr(3, 4)) == 0)
pos("both zeros lie in 0<Re<1 and off Re=1/2", all(0 < z < 1 and z != Fr(1, 2) for z in (Fr(1, 4), Fr(3, 4))))
neg("a zero of F has real part 1/2", any(z == Fr(1, 2) for z in (Fr(1, 4), Fr(3, 4))))
g = lambda s: s*(1 - s)
pos("r=1: s(1-s) is invariant; its zeros 0,1 are not the fixed point 1/2", abs(g(mpf('0.3')) - g(1-mpf('0.3'))) < mpf("1e-28") and g(0) == 0 and g(1) == 0)
f2 = lambda a, b: a - b
q = (mpc(1, 2), mpc(-3, .5))
pos("r=2: f=s1-s2 is R-invariant", abs(f2(*q) - f2(1 - q[1], 1 - q[0])) < mpf("1e-25"))
z0 = (mpc(0.3, 2), mpc(0.3, 2))
pos("r=2: zero (0.3+2i,0.3+2i) of f is not on Fix(R): s1+s2 != 1", f2(*z0) == 0 and abs(z0[0] + z0[1] - 1) > 0.1)
p = mpc(0.5, 14.1347)
pos("critical-line point is fixed by s->1-conj(s)", (1 - p.conjugate()) == p)
neg("critical-line point is fixed by s->1-s", (1 - p) == p)
say("INFO", "these examples refute an inference from SYMMETRY ALONE; they are not statements about RH or about xi")

# ---------------------------------------------------------------- 5. K4
E4 = [(0,1),(0,2),(0,3),(1,2),(1,3),(2,3)]
def conn(sub):
    par = list(range(4))
    def f(a):
        while par[a] != a: a = par[a]
        return a
    for i in sub:
        a, b = E4[i]; par[f(a)] = f(b)
    return len({f(v) for v in range(4)}) == 1
trees = [t for t in itertools.combinations(range(6), 3) if conn(t)]
def det(M):
    M = [row[:] for row in M]; n = len(M); d = Fr(1)
    for c in range(n):
        p = next((i for i in range(c, n) if M[i][c] != 0), None)
        if p is None: return Fr(0)
        if p != c: M[c], M[p] = M[p], M[c]; d = -d
        d *= M[c][c]
        for i in range(c+1, n):
            f = M[i][c]/M[c][c]; M[i] = [a - f*b for a, b in zip(M[i], M[c])]
    return d
L = [[Fr(0)]*4 for _ in range(4)]
for a, b in E4: L[a][a] += 1; L[b][b] += 1; L[a][b] -= 1; L[b][a] -= 1
pos("K4: exact enumeration gives 16 spanning trees", len(trees) == 16)
pos("K4: matrix-tree theorem (reduced Laplacian determinant) gives 16", det([row[1:] for row in L[1:]]) == 16)
pos("K4: Cayley n^(n-2) = 16 for n=4", 4**2 == 16)
pos("K4: 4 stars + 12 paths", sum(1 for t in trees if any(sum(1 for i in t if v in E4[i]) == 3 for v in range(4))) == 4)
if "--k4" in sys.argv:
    try:
        import numpy as np
        from scipy.stats import qmc
        comp = [sorted(set(range(6)) - set(t)) for t in trees]      # Psi = sum over trees of the product of the 3 edges OFF the tree
        vals = []
        for seed in range(8):
            u = np.clip(qmc.Sobol(6, scramble=True, seed=seed).random_base2(20), 1e-15, 1)
            x = -np.log(u); x /= x.sum(1, keepdims=True)             # Dirichlet(1,..,1): uniform on the 5-simplex, volume 1/5! = 1/120
            Ps = sum(x[:, a]*x[:, b]*x[:, c] for a, b, c in comp)
            vals.append((1/Ps**2).mean()/120)
        m, e = float(np.mean(vals)), float(np.std(vals)/np.sqrt(len(vals)))
        ref = float(6*zeta(3)); sig = (m - ref)/e if e else float('nan')
        say("INCONCLUSIVE", "K4 period estimate vs 6 zeta(3) (literature value, source not checked)",
            f"estimate {m:.4f}, spread of 8 scrambled-Sobol replicates {e:.4f} (NOT a rigorous error bound), reference {ref:.4f}, discrepancy {sig:+.1f} replicate-spreads")
    except Exception as ex:
        say("SKIP", "K4 period estimate (numpy/scipy unavailable)", str(ex))
else:
    say("SKIP", "K4 period estimate (opt-in: pass --k4); previous runs were INCONCLUSIVE")
say("INFO", "K4 period 6 zeta(3): primary source not checked; graph-polynomial convention and projective measure as in the chapter text")

# ---------------------------------------------------------------- summary
el = time.time() - T0
print("\n--- summary ---")
print("  ".join(f"{k}={v}" for k, v in cnt.items()))
print(f"positive tests passed: {cnt['PASS']}; negative controls correctly rejected: {cnt['REJECTED']}; inconclusive: {cnt['INCONCLUSIVE']}; skipped: {cnt['SKIP']}")
print(f"python {platform.python_version()}, mpmath {mpmath.__version__}", end="")
try:
    import numpy, scipy; print(f", numpy {numpy.__version__}, scipy {scipy.__version__}", end="")
except Exception: pass
print(f"; elapsed {el:.1f}s; exit {1 if cnt['FAIL'] else 0}")
print("[HONESTY] Finite-r checks are regression tests, not proofs for arbitrary r. Numerical agreement is not a literature proof.\n"
      "Nothing here bears on the Riemann hypothesis, any zero location, or the unread sources listed in [SOURCES].")
sys.exit(1 if cnt["FAIL"] else 0)
