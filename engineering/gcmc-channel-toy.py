"""Toy grand-canonical Monte Carlo (GCMC) of a lattice gas confined to a channel.
SCOPE: a METHOD CHECK, not a zeolite calculation. Sites on a w x L strip (periodic along L, walls at the
ends of w), nearest-neighbour attraction eps, chemical potential mu (all in units of kT=1).
No zeolite structure, force field, or pore size from any real material is used.
CONTROL: Metropolis GCMC mean occupancy is compared with exact enumeration of every state on a tiny
strip (w=2, L=4: 8 sites, 256 states). The check FAILS if the sampler has a wrong acceptance rule
(demonstrated below by a deliberately wrong rule that must be rejected).
"""
import itertools, math, random, sys

def neighbours(w, L):
    nb = {}
    for x in range(L):
        for y in range(w):
            s = x*w+y
            l = []
            l.append(((x+1) % L)*w+y); l.append(((x-1) % L)*w+y)
            if y+1 < w: l.append(x*w+y+1)
            if y-1 >= 0: l.append(x*w+y-1)
            nb[s] = list(dict.fromkeys(l))     # unique (handles L=2 wrap)
    return nb

def energy(occ, nb, eps):
    e = 0.0
    for s, o in enumerate(occ):
        if o:
            for t in nb[s]:
                if t > s and occ[t]: e -= eps
    return e

def exact_mean_occupancy(w, L, eps, mu):
    nb = neighbours(w, L); n = w*L
    Z = N = 0.0
    for occ in itertools.product((0, 1), repeat=n):
        k = sum(occ); wgt = math.exp(-energy(occ, nb, eps) + mu*k)
        Z += wgt; N += k*wgt
    return N/Z/n

def gcmc_mean_occupancy(w, L, eps, mu, sweeps=40000, seed=1, wrong=False):
    rnd = random.Random(seed); nb = neighbours(w, L); n = w*L
    occ = [0]*n; k = 0; acc = 0.0; cnt = 0
    for sweep in range(sweeps):
        for _ in range(n):
            s = rnd.randrange(n)
            nn = sum(occ[t] for t in nb[s])
            if occ[s] == 0:    # try insert: dlnW = eps*nn + mu
                d = eps*nn + mu
            else:              # try delete: dlnW = -(eps*nn + mu)
                d = -(eps*nn + mu)
            if wrong: d = abs(d)*0 + (eps*nn + mu)      # deliberately wrong: same sign for delete
            if d >= 0 or rnd.random() < math.exp(d):
                occ[s] ^= 1; k += 1 if occ[s] else -1
        if sweep > sweeps//10: acc += k/n; cnt += 1
    return acc/cnt

if __name__ == "__main__":
    eps = 1.0
    print("CONTROL: GCMC vs exact enumeration, w=2 L=4, eps=1 kT")
    ok = True
    for mu in (-3.0, -1.5, 0.0, 1.5):
        ex = exact_mean_occupancy(2, 4, eps, mu); mc = gcmc_mean_occupancy(2, 4, eps, mu)
        good = abs(ex-mc) < 0.01; ok &= good
        print(f"  mu={mu:+.1f}  exact={ex:.4f}  GCMC={mc:.4f}  {'PASS' if good else 'FAIL'}")
    # The wrong rule must be caught away from the particle-hole symmetric point (mu=-1.5 gives exactly 0.5
    # for any symmetric-looking sampler; the first version of this control tested only there and was vacuous).
    caught = True
    for mu in (-3.0, 0.0):
        bad = gcmc_mean_occupancy(2, 4, eps, mu, wrong=True); ex = exact_mean_occupancy(2, 4, eps, mu)
        c = abs(ex-bad) > 0.05; caught &= c
        print(f"  wrong-rule sampler at mu={mu:+.1f}: GCMC={bad:.4f} vs exact={ex:.4f}  {'CAUGHT (check can fail)' if c else 'NOT CAUGHT: check is vacuous'}")
    print("RESULT:", "ALL PASS" if ok and caught else "FAIL")
    if ok and caught:
        print("\nTOY RESULT (method demo only): mean occupancy vs channel width w, L=20, mu=-2.0, eps=1.0")
        for w in (1, 2, 3, 4):
            print(f"  w={w}  occupancy={gcmc_mean_occupancy(w, 20, 1.0, -2.0, sweeps=4000):.3f}")
