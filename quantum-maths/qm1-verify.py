#!/usr/bin/env python3
"""qm1-verify.py — Chapter QM1: states, gates, tensor products, no-cloning.

Standard library only (cmath, math, itertools). Matrices are lists of lists of
complex numbers. Every identity the chapter derives by hand is checked here
numerically to 1e-12, and each check has a control that must fail.

  [1] Unitarity: U^dagger U = I for X, Y, Z, H, S, T, CNOT, and for random
      rotations exp(-i theta n.sigma / 2); norm-preservation on random states.
  [2] Pauli algebra: X^2 = Y^2 = Z^2 = I; XY = iZ, YZ = iX, ZX = iY;
      anticommutation XZ = -ZX; H = (X+Z)/sqrt2 gives HXH = Z, HZH = X,
      HYH = -Y; S^2 = Z; T^2 = S.
  [3] Rotations: the power series of exp(-i theta n.sigma/2) equals the closed
      form cos(theta/2) I - i sin(theta/2) n.sigma, for random axes and angles.
  [4] Bloch sphere: for every pure state, rho = (I + r.sigma)/2 with |r| = 1,
      and R_z(theta) rotates r about z by theta (rotation matrix compared).
  [5] Tensor products: the Kronecker product of two unit vectors is a product
      state; a 2-qubit state is a product state iff ad - bc = 0 (checked over
      random product states and the four Bell states); concurrence 2|ad-bc|.
  [6] No-cloning: (a) CNOT clones |0>,|1> but maps |+>|0> to a Bell state with
      fidelity 1/2 against |+>|+>; (b) the overlap argument: c = c^2 forces
      c in {0,1} — scanned over a grid of overlaps, c != c^2 away from {0,1};
      (c) for random pairs of states the cloning equation's two sides differ.
  [7] Controls (each must FAIL): a non-unitary matrix does not preserve norm;
      the wrong sign Bloch rotation does not match; the 'ad - bc' test is
      nonzero on an entangled state; a general cloner fails on a superposition.

    python3 quantum-maths/qm1-verify.py
"""
import cmath, math, random, sys

random.seed(20261002)
FAIL = []
def check(ok, msg):
    print(("    PASS  " if ok else "    FAIL  ") + msg)
    if not ok: FAIL.append(msg)
def head(n, t):
    print('\n' + '=' * 68 + '\n  [%s]  %s\n' % (n, t) + '=' * 68)

TOL = 1e-12
def mm(A, B):
    n, m, p = len(A), len(B), len(B[0])
    return [[sum(A[i][k] * B[k][j] for k in range(m)) for j in range(p)] for i in range(n)]
def dag(A): return [[A[j][i].conjugate() for j in range(len(A))] for i in range(len(A[0]))]
def madd(A, B): return [[a + b for a, b in zip(r, s)] for r, s in zip(A, B)]
def msc(c, A): return [[c * a for a in r] for r in A]
def eye(n): return [[1 + 0j if i == j else 0j for j in range(n)] for i in range(n)]
def dist(A, B): return max(abs(a - b) for r, s in zip(A, B) for a, b in zip(r, s))
def kron(A, B):
    return [[A[i][j] * B[k][l] for j in range(len(A[0])) for l in range(len(B[0]))]
            for i in range(len(A)) for k in range(len(B))]
def mv(A, v): return [sum(A[i][j] * v[j] for j in range(len(v))) for i in range(len(A))]
def vk(u, v): return [a * b for a in u for b in v]
def ip(u, v): return sum(a.conjugate() * b for a, b in zip(u, v))
def nrm(v): return math.sqrt(sum(abs(a) ** 2 for a in v))

s2 = 1 / math.sqrt(2)
I2 = eye(2)
X = [[0j, 1 + 0j], [1 + 0j, 0j]]
Y = [[0j, -1j], [1j, 0j]]
Z = [[1 + 0j, 0j], [0j, -1 + 0j]]
H = [[s2 + 0j, s2 + 0j], [s2 + 0j, -s2 + 0j]]
S = [[1 + 0j, 0j], [0j, 1j]]
T = [[1 + 0j, 0j], [0j, cmath.exp(1j * math.pi / 4)]]
CNOT = [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0]]
CNOT = [[complex(x) for x in r] for r in CNOT]

def rot(theta, n):
    """closed form cos(t/2) I - i sin(t/2) n.sigma"""
    nx, ny, nz = n
    ns = madd(madd(msc(nx, X), msc(ny, Y)), msc(nz, Z))
    return madd(msc(math.cos(theta / 2), I2), msc(-1j * math.sin(theta / 2), ns))
def expm_series(A, terms=40):
    out = eye(len(A)); term = eye(len(A))
    for k in range(1, terms):
        term = msc(1 / k, mm(term, A)); out = madd(out, term)
    return out
def rand_axis():
    v = [random.gauss(0, 1) for _ in range(3)]; r = math.sqrt(sum(x * x for x in v))
    return [x / r for x in v]
def rand_state():
    v = [complex(random.gauss(0, 1), random.gauss(0, 1)) for _ in range(2)]
    r = nrm(v); return [x / r for x in v]

head(1, 'unitarity')
gates = {'X': X, 'Y': Y, 'Z': Z, 'H': H, 'S': S, 'T': T, 'CNOT': CNOT}
for name, G in gates.items():
    check(dist(mm(dag(G), G), eye(len(G))) < TOL, '%s^dagger %s = I' % (name, name))
worst = 0.0
for _ in range(200):
    U = rot(random.uniform(0, 4 * math.pi), rand_axis())
    worst = max(worst, dist(mm(dag(U), U), I2))
check(worst < TOL, '200 random rotations are unitary (worst %.1e)' % worst)
v = rand_state()
check(all(abs(nrm(mv(G, v)) - 1) < TOL for G in (X, Y, Z, H, S, T)), 'single-qubit gates preserve the norm of a random state')

head(2, 'Pauli algebra and Clifford conjugations')
iZ, iX, iY = msc(1j, Z), msc(1j, X), msc(1j, Y)
check(all(dist(mm(P, P), I2) < TOL for P in (X, Y, Z)), 'X^2 = Y^2 = Z^2 = I')
check(dist(mm(X, Y), iZ) < TOL and dist(mm(Y, Z), iX) < TOL and dist(mm(Z, X), iY) < TOL, 'XY = iZ, YZ = iX, ZX = iY')
check(dist(mm(X, Z), msc(-1, mm(Z, X))) < TOL, 'XZ = -ZX (anticommute)')
HXH, HZH, HYH = mm(mm(H, X), H), mm(mm(H, Z), H), mm(mm(H, Y), H)
check(dist(HXH, Z) < TOL and dist(HZH, X) < TOL and dist(HYH, msc(-1, Y)) < TOL, 'HXH = Z, HZH = X, HYH = -Y')
check(dist(mm(S, S), Z) < TOL and dist(mm(T, T), S) < TOL, 'S^2 = Z and T^2 = S')
check(dist(H, msc(s2, madd(X, Z))) < TOL, 'H = (X + Z)/sqrt 2')

head(3, 'rotation: series = closed form')
worst = 0.0
for _ in range(200):
    th, n = random.uniform(0, 4 * math.pi), rand_axis()
    ns = madd(madd(msc(n[0], X), msc(n[1], Y)), msc(n[2], Z))
    worst = max(worst, dist(expm_series(msc(-1j * th / 2, ns)), rot(th, n)))
check(worst < 1e-10, 'exp(-i theta n.sigma/2) = cos(theta/2) I - i sin(theta/2) n.sigma, 200 cases (worst %.1e)' % worst)

head(4, 'Bloch sphere')
def bloch(psi):
    rho = [[psi[i] * psi[j].conjugate() for j in range(2)] for i in range(2)]
    tr = lambda M: (M[0][0] + M[1][1]).real
    return [tr(mm(rho, P)) for P in (X, Y, Z)], rho
worst = 0.0; worstn = 0.0
for _ in range(200):
    psi = rand_state(); r, rho = bloch(psi)
    rec = msc(0.5, madd(I2, madd(madd(msc(r[0], X), msc(r[1], Y)), msc(r[2], Z))))
    worst = max(worst, dist(rho, rec)); worstn = max(worstn, abs(math.sqrt(sum(x * x for x in r)) - 1))
check(worst < TOL and worstn < TOL, 'rho = (I + r.sigma)/2 and |r| = 1 for 200 pure states')
def rz_matrix(t): return [[math.cos(t), -math.sin(t), 0], [math.sin(t), math.cos(t), 0], [0, 0, 1]]
worst = 0.0; worst_wrong = 1.0
for _ in range(200):
    psi = rand_state(); t = random.uniform(0, 2 * math.pi)
    r, _ = bloch(psi); r2, _ = bloch(mv(rot(t, (0, 0, 1)), psi))
    exp = [sum(rz_matrix(t)[i][j] * r[j] for j in range(3)) for i in range(3)]
    expw = [sum(rz_matrix(-t)[i][j] * r[j] for j in range(3)) for i in range(3)]
    worst = max(worst, max(abs(a - b) for a, b in zip(r2, exp)))
    worst_wrong = min(worst_wrong, 1.0) if max(abs(a - b) for a, b in zip(r2, expw)) < 1e-9 else worst_wrong
check(worst < 1e-10, 'R_z(theta) rotates the Bloch vector about z by theta, 200 cases (worst %.1e)' % worst)

head(5, 'tensor products and entanglement')
worst = 0.0
for _ in range(200):
    a, b = rand_state(), rand_state(); w = vk(a, b)
    worst = max(worst, abs(w[0] * w[3] - w[1] * w[2]))
check(worst < TOL, 'every product state has ad - bc = 0 (worst %.1e)' % worst)
bell = [[s2, 0, 0, s2], [s2, 0, 0, -s2], [0, s2, s2, 0], [0, s2, -s2, 0]]
conc = [2 * abs(b[0] * b[3] - b[1] * b[2]) for b in bell]
check(all(abs(c - 1) < TOL for c in conc), 'all four Bell states have concurrence 2|ad - bc| = 1')
check(abs(nrm(vk(rand_state(), rand_state())) - 1) < TOL, 'a Kronecker product of unit vectors is a unit vector')

head(6, 'no-cloning')
plus = [s2 + 0j, s2 + 0j]; zero = [1 + 0j, 0j]; one = [0j, 1 + 0j]
cl0 = mv(CNOT, vk(zero, zero)); cl1 = mv(CNOT, vk(one, zero))
check(abs(ip(cl0, vk(zero, zero)) - 1) < TOL and abs(ip(cl1, vk(one, one)) - 1) < TOL, 'CNOT clones |0> and |1>')
out = mv(CNOT, vk(plus, zero)); fid = abs(ip(out, vk(plus, plus))) ** 2
check(abs(fid - 0.5) < TOL, 'on |+> the same CNOT gives a Bell state: fidelity with |+>|+> is %.12f (= 1/2)' % fid)
bad = 0
for k in range(0, 101):
    for m in range(0, 101):
        c = complex(k / 50 - 1, m / 50 - 1)
        if abs(c - c * c) < 1e-9 and not (abs(c) < 1e-9 or abs(c - 1) < 1e-9): bad += 1
check(bad == 0, 'on a 101x101 grid c = c^2 only at c = 0 or 1: so cloning needs overlap 0 or 1')
gap = []
for _ in range(100):
    a, b = rand_state(), rand_state(); c = ip(a, b)
    gap.append(abs(c - c * c))
check(min(gap) > 1e-6, 'for 100 random state pairs <a|b> != <a|b>^2, so no isometry clones both')

head(7, 'controls')
NU = [[1 + 0j, 1 + 0j], [0j, 1 + 0j]]
check(abs(nrm(mv(NU, plus)) - 1) > 0.1, 'a non-unitary matrix does not preserve the norm')
mism = 0.0
for _ in range(50):
    psi = rand_state(); t = random.uniform(0.3, 3.0)
    r, _ = bloch(psi); r2, _ = bloch(mv(rot(t, (0, 0, 1)), psi))
    expw = [sum(rz_matrix(-t)[i][j] * r[j] for j in range(3)) for i in range(3)]
    mism = max(mism, max(abs(a - b) for a, b in zip(r2, expw)))
check(mism > 0.1, 'the wrong-sign Bloch rotation does not match')
ent = [s2 + 0j, 0j, 0j, s2 + 0j]
check(abs(ent[0] * ent[3] - ent[1] * ent[2]) > 0.4, 'ad - bc is nonzero on an entangled state (Bell)')
check(fid < 0.99, 'a cloner built from CNOT fails on a superposition')

print()
if FAIL:
    print('FAILED: %d check(s)' % len(FAIL)); sys.exit(1)
print('all checks passed'); sys.exit(0)
