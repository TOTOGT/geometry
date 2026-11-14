"""Check of chIV-orthogonality.html Theorem 5.1 (iii)/(iv) and the Proof-1 prediction.

Prediction (section 5.3): for any realization with ||u_i w_i^T|| = 1/3 and (SH1),
sigma_min(A^(12)) = 2/3 exactly, where A_i = P^i + u_i w_i^T and
A^(12) = A_12 ... A_1, P the cyclic shift on R^12.

Realizations tested (all satisfy (SH1): u's mutually orthogonal, w's mutually
orthogonal, ||u_i|| = ||w_i|| = 3^(-1/2), so ||u_i w_i^T|| = 1/3; u_i = w_i, Phi = id):
  R1: u_i = w_i = e_i / sqrt(3)
  R2..R6: u_i = w_i = Q e_i / sqrt(3) for random orthogonal Q (seeded)

Also recounts (iv): rank of the Jacobian of the active constraint set
{<u_i,u_j>=0, <w_i,w_j>=0, i<j} at R1 with u and w INDEPENDENT (no duality),
and with duality u = Phi(w).
"""
import numpy as np

n = 12
P = np.zeros((n, n))
for i in range(n):
    P[(i + 1) % n, i] = 1.0

def sigma_min_of(us, ws):
    A = np.eye(n)
    for i in range(1, n + 1):
        Ai = np.linalg.matrix_power(P, i) + np.outer(us[i - 1], ws[i - 1])
        A = Ai @ A              # A^(12) = A_12 ... A_1 applied to A_1 first
    return np.linalg.svd(A, compute_uv=False).min()

s = 1 / np.sqrt(3)
E = np.eye(n) * s
print("R1 (u=w=e_i/sqrt3): sigma_min(A^(12)) = %.9f   (claim: 0.666666667)" % sigma_min_of(E, E))

rng = np.random.default_rng(20261114)
for t in range(5):
    Q, _ = np.linalg.qr(rng.standard_normal((n, n)))
    U = (Q * s).T   # rows u_i = s * Q e_i -> mutually orthogonal, norm s
    print("R%d (random orthogonal): sigma_min = %.9f" % (t + 2, sigma_min_of(U, U)))

# (iv) constraint count: number of independent scalar equations
pairs = [(i, j) for i in range(n) for j in range(i + 1, n)]
print("\npairs C(12,2) = %d; u-side + w-side = %d equations" % (len(pairs), 2 * len(pairs)))
u0 = E.copy(); w0 = E.copy()
# Jacobian of g_{ij} = <u_i, u_j> wrt all 144 u-coords, at R1 (independent u,w)
J = np.zeros((2 * len(pairs), 2 * n * n))
for r, (i, j) in enumerate(pairs):
    J[r, i * n:(i + 1) * n] = u0[j]; J[r, j * n:(j + 1) * n] = u0[i]
    J[len(pairs) + r, n * n + i * n:n * n + (i + 1) * n] = w0[j]
    J[len(pairs) + r, n * n + j * n:n * n + (j + 1) * n] = w0[i]
print("rank of constraint Jacobian, u and w independent: %d" % np.linalg.matrix_rank(J))
Jd = J[:len(pairs), :n * n] + J[len(pairs):, n * n:]   # duality u=w: same variables
print("rank with duality u_i = w_i (variables shared):   %d" % np.linalg.matrix_rank(Jd))
