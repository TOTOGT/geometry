"""
swarm_simulator.py  --  Version 3
=================================
Simulator for "The Swarm Simulator: A Dynamical Systems Model of Collective Intelligence
Using the TO/TOGT Operator Pipeline"  (Pablo Nogueira Grossi, G6 LLC, Newark NJ, 2026).

V3 changes (see CHANGES_SwarmSimulator_V3.md):
  * find_fixedpoint() returns the true fixed point of (I, C, M), which is (0, 0, 0). F_t = 1 + alpha t
    has no fixed point (SwarmSimulator.lean: diffuse_unbounded), so F is reported separately.
  * Contraction is stated on a ball: rho(R) = max(a, a c R, m) for decay, lambda(R) = max(a (1 + c R), m)
    for the Lipschitz constant (SwarmSimulator.lean: orbit_nrm_le, step_lipschitz_ball). There is no
    global Lipschitz constant (no_global_lipschitz).
  * Figure 2 plots the proved bound rho(R)^t ||X_0||, R = ||X_0||, instead of L^t ||X_0||.
  * Figure 3 maps the contraction RADIUS R* = (1 - a)/(a c), not L < 1.
  * Figure 4 uses two clusters that both satisfy the ball condition, and shows that they converge to the
    SAME fixed point, 0, at different rates. (V2 used parameter sets with L = 2.41 and 1.93.)

Usage:
  python swarm_simulator.py            # figures into ./figures
  python swarm_simulator.py --check    # numerical checks of the facts the Lean file proves (no plotting)
Dependencies: numpy, matplotlib (figures only).
Zenodo V1: 10.5281/zenodo.19208284 - V2: 10.5281/zenodo.20230613 - AXLE: https://github.com/TOTOGT/AXLE
"""
import os
import sys
import numpy as np


class SwarmParams:
    """Parameters (Definitions 3.1-3.4). a, c, m are the constants the proofs use:
         a = f_types * f_agents * (1 - eta)        I_{t+1} = a I_t
         c = 1 / (1 + D)                            C_{t+1} = C_t * I_{t+1} * c
         m = (1 + beta * reuse) * avg_quality       M_{t+1} = m M_t
    """
    def __init__(self, type_quality=0.65, agent_quality=0.80, noise=0.20, drag=1.50,
                 beta=0.10, reuse=0.50, avg_quality=0.22, alpha=0.02):
        self.type_quality, self.agent_quality, self.noise = type_quality, agent_quality, noise
        self.drag, self.beta, self.reuse = drag, beta, reuse
        self.avg_quality, self.alpha = avg_quality, alpha
        self.a = type_quality * agent_quality * (1 - noise)
        self.c = 1.0 / (1.0 + drag)
        self.m = (1 + beta * reuse) * avg_quality
        # the paper's printed constants
        self.LI = self.a
        self.LC = self.LI / (1 + drag)
        self.LM = self.m
        self.L = self.LI + self.LC + self.LM

    def rho(self, R):
        """Decay factor on the ball ||X||_1 <= R (orbit_nrm_le)."""
        return max(self.a, self.a * self.c * R, self.m)

    def lam(self, R):
        """Lipschitz constant on the ball (step_lipschitz_ball)."""
        return max(self.a * (1 + self.c * R), self.m)

    def radius(self):
        """Largest R with lambda(R) < 1: R* = (1 - a)/(a c), provided m < 1 and a < 1."""
        if self.a >= 1 or self.m >= 1:
            return 0.0
        return (1 - self.a) / (self.a * self.c) if self.a > 0 else float("inf")

    def __repr__(self):
        return (f"SwarmParams(a={self.a:.4f}, c={self.c:.4f}, m={self.m:.4f}; printed L={self.L:.4f}; "
                f"contraction radius R*={self.radius():.4f})")


def step(state, p, t):
    """One step: (I, C, M, F) -> (I', C', M', F')."""
    I, C, M, F = state
    In = I * p.type_quality * p.agent_quality * (1 - p.noise)
    return (In, C * In / (1 + p.drag), M * (1 + p.beta * p.reuse) * p.avg_quality, 1 + p.alpha * t)


def evolve(state0, p, T):
    traj = np.zeros((T + 1, 4))
    traj[0] = state0
    s = state0
    for t in range(1, T + 1):
        s = step(s, p, t)
        traj[t] = s
    return traj


def find_fixedpoint(p, T=200):
    """Fixed point of the (I, C, M) part: (0, 0, 0) whenever it exists in the ball (fixed_point_zero).
    F is not a fixed coordinate: it is returned as its value at time T, for information only."""
    return (0.0, 0.0, 0.0, 1 + p.alpha * (T - 1))


def l1(x):
    return float(sum(abs(v) for v in x[:3]))


# ------------------------------------------------------------------ numerical checks of the Lean facts
def run_checks():
    p = SwarmParams()
    ok = True

    def check(name, cond):
        nonlocal ok
        print(("PASS  " if cond else "FAIL  ") + name)
        ok &= bool(cond)

    check("a, c, m = 0.416, 0.4, 0.231 (default_radius, printed_bound_fails use these exactly)",
          abs(p.a - 0.416) < 1e-12 and abs(p.c - 0.4) < 1e-12 and abs(p.m - 0.231) < 1e-12)
    check("printed L = 0.8134 < 1", abs(p.L - 0.8134) < 1e-12 and p.L < 1)
    check("contraction radius R* = 3.5096 (default_radius: lambda(3.5) < 1 < lambda(4))",
          abs(p.radius() - 3.50962) < 1e-4 and p.lam(3.5) < 1 < p.lam(4.0))
    # orbit_nrm_le on random starts inside the ball
    rng = np.random.default_rng(2026)
    bad = 0
    for _ in range(2000):
        R = rng.uniform(0.1, 6.0)
        v = rng.random(3) + 1e-9
        v = v / v.sum() * R * rng.uniform(0.0, 1.0)
        s = (v[0], v[1], v[2], 0.0)
        r0 = l1(s)
        rr = p.rho(R)
        if rr > 1:
            continue
        for t in range(1, 40):
            s = step(s, p, t)
            if l1(s) > rr ** t * r0 * (1 + 1e-9) + 1e-300:
                bad += 1
                break
    check("orbit_nrm_le: ||X_t|| <= rho(R)^t ||X_0|| on 2000 random starts (R up to 6, rho <= 1)", bad == 0)
    # paper_bound for ||X0|| <= 1
    bad = 0
    for _ in range(2000):
        v = rng.random(3)
        v = v / v.sum() * rng.uniform(0.0, 1.0)
        s = (v[0], v[1], v[2], 0.0)
        r0 = l1(s)
        for t in range(1, 40):
            s = step(s, p, t)
            if l1(s) > p.L ** t * r0 * (1 + 1e-9) + 1e-300:
                bad += 1
                break
    check("paper_bound: the printed bound L^t ||X_0|| holds for ||X_0|| <= 1 (2000 random starts)", bad == 0)
    # printed bound fails from (100, 10, 1)
    s = step((100.0, 10.0, 1.0, 0.0), p, 1)
    check("printed_bound_fails: from (100, 10, 1) one step gives 208.231 > L * 111 = 90.2874",
          abs(l1(s) - 208.231) < 1e-9 and l1(s) > p.L * 111)
    # no global Lipschitz constant: grow C, the ratio grows without bound
    ratios = []
    for C0 in (1.0, 10.0, 100.0, 1000.0):
        X = (1.0, C0, 0.0, 0.0); Y = (0.0, C0, 0.0, 0.0)
        A = step(X, p, 1); B = step(Y, p, 1)
        ratios.append(l1(tuple(a - b for a, b in zip(A, B))) / 1.0)
    check("no_global_lipschitz: the ratio ||G(X)-G(Y)|| / ||X-Y|| grows without bound with C: "
          + ", ".join(f"{r:.2f}" for r in ratios), ratios == sorted(ratios) and ratios[-1] > 100)
    tr = evolve((1.0, 1.0, 1.0, 0.0), p, 200)
    check("diffuse_unbounded: F_100 = 3.0, F_200 = 5.0 (no fixed point in F)",
          abs(tr[100, 3] - 3.0) < 1e-12 and abs(tr[200, 3] - 5.0) < 1e-12)
    # two_clusters: two clusters that satisfy the ball condition share the fixed point 0
    pA = SwarmParams(type_quality=0.70, agent_quality=0.80, noise=0.10, drag=1.0, beta=0.10, reuse=0.50, avg_quality=0.30)
    pB = SwarmParams(type_quality=0.55, agent_quality=0.75, noise=0.15, drag=2.0, beta=0.20, reuse=0.60, avg_quality=0.25)
    R = 2.0
    check(f"two_clusters: A (a={pA.a:.3f}) and B (a={pB.a:.3f}) both have rho({R}) < 1: "
          f"{pA.rho(R):.3f}, {pB.rho(R):.3f}", pA.rho(R) < 1 and pB.rho(R) < 1)
    endA = evolve((1.0, 0.5, 0.5, 0.0), pA, 300)[-1][:3]
    endB = evolve((1.0, 0.5, 0.5, 0.0), pB, 300)[-1][:3]
    check("two_clusters: both converge to (0, 0, 0)", max(np.abs(endA)) < 1e-50 and max(np.abs(endB)) < 1e-50)
    print("\n" + ("ALL CHECKS PASS" if ok else "SOME CHECKS FAILED"))
    return ok


# ------------------------------------------------------------------ figures
def figures():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    NAVY, GOLD, TEAL, RED, GREY = "#1a2744", "#c9a84c", "#1a6b5a", "#c0392b", "#7f8c8d"
    plt.rcParams.update({"font.family": "serif", "font.size": 11, "figure.dpi": 150})
    out = "figures"
    os.makedirs(out, exist_ok=True)

    def save(name):
        for ext in ("pdf", "png"):
            plt.savefig(os.path.join(out, f"{name}.{ext}"), bbox_inches="tight", dpi=150)
        plt.close()
        print("  saved", name)

    p = SwarmParams()
    print(p)
    # fig 1: state evolution
    T = 60
    tr = evolve((1.0, 1.0, 1.0, 0.0), p, T)
    fig, axes = plt.subplots(2, 2, figsize=(10, 7))
    for ax, col, lab, colr in zip(axes.flat, range(4), ["I (shared intent)", "C (coordination)",
                                                        "M (type propagation)", "F (diffusion)"],
                                  [NAVY, TEAL, GOLD, RED]):
        ax.plot(np.arange(T + 1), tr[:, col], color=colr, lw=2)
        ax.set_title(lab); ax.set_xlabel("t"); ax.grid(True, alpha=0.2)
        if col < 3:
            ax.set_yscale("log")
    fig.suptitle("I, C, M decay to 0 (log scale); F = 1 + alpha t grows without bound", fontsize=12)
    plt.tight_layout(); save("fig1_state_evolution")

    # fig 2: the proved bound rho(R)^t ||X0||, R = ||X0||
    fig, ax = plt.subplots(figsize=(8, 5))
    for X0, colr in zip([(2.0, 0.5, 1.5), (0.3, 1.8, 0.4), (1.5, 1.5, 0.8)], [NAVY, TEAL, GOLD]):
        R = sum(X0)
        tr = evolve((*X0, 0.0), p, T)
        ax.semilogy([l1(tr[t]) for t in range(T + 1)], color=colr, lw=2, label=f"X0={X0}")
        ax.semilogy([p.rho(R) ** t * R for t in range(T + 1)], "--", color=colr, lw=1, alpha=0.8)
    ax.set_xlabel("t"); ax.set_ylabel("||X_t||_1")
    ax.set_title("Decay to 0 and the proved bound rho(R)^t ||X_0|| (dashed), R = ||X_0||")
    ax.legend(fontsize=9); ax.grid(True, alpha=0.2)
    save("fig2_convergence")

    # fig 3: contraction radius R* = (1-a)/(a c) over noise and type quality
    noise = np.linspace(0.0, 0.5, 200); tq = np.linspace(0.5, 1.0, 200)
    N, TQ = np.meshgrid(noise, tq)
    a = TQ * 0.88 * (1 - N); c = 1 / (1 + 0.5)
    Rs = np.where(a < 1, (1 - a) / (a * c), np.nan)
    fig, ax = plt.subplots(figsize=(6.5, 5))
    cf = ax.contourf(noise, tq, np.clip(Rs, 0, 12), levels=24, cmap="viridis")
    plt.colorbar(cf, ax=ax, label="contraction radius R* = (1 - a)/(a c)")
    ax.set_xlabel("noise eta"); ax.set_ylabel("type quality f_types")
    ax.set_title("Contraction holds on the ball ||X||_1 < R*\n(agent quality 0.88, drag D = 0.5)")
    save("fig3_contraction_region")

    # fig 4: two clusters, same fixed point
    pA = SwarmParams(type_quality=0.70, agent_quality=0.80, noise=0.10, drag=1.0, beta=0.10, reuse=0.50, avg_quality=0.30)
    pB = SwarmParams(type_quality=0.55, agent_quality=0.75, noise=0.15, drag=2.0, beta=0.20, reuse=0.60, avg_quality=0.25)
    fig, ax = plt.subplots(figsize=(8, 5))
    for pp, colr, nm in ((pA, NAVY, "cluster A"), (pB, RED, "cluster B")):
        tr = evolve((1.0, 0.5, 0.5, 0.0), pp, 80)
        ax.semilogy([max(l1(tr[t]), 1e-300) for t in range(81)], color=colr, lw=2,
                    label=f"{nm}: a={pp.a:.3f}, rho(2)={pp.rho(2.0):.3f}")
    ax.set_xlabel("t"); ax.set_ylabel("||X_t||_1")
    ax.set_title("Two clusters that satisfy the ball condition: same fixed point (0), different rates")
    ax.legend(fontsize=9); ax.grid(True, alpha=0.2)
    save("fig4_multi_orbit")


if __name__ == "__main__":
    if "--check" in sys.argv:
        sys.exit(0 if run_checks() else 1)
    figures()
    print("done. Numerical checks: python swarm_simulator.py --check")
