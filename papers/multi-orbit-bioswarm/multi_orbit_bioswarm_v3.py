"""
multi_orbit_bioswarm_v3.py  --  Version 3 companion to
"Biological Transitions as Multi-Agent Realisations of the Generative Operator Pipeline in TO/TOGT:
 A Fruit-Fly Connectome Toy Model"  (Pablo Nogueira Grossi, G6 LLC, Newark NJ, 2026).

The four operators C, K, F, U are imported unchanged from the V2 code, multi_orbit_bioswarm.py.
V3 measures what the swarm does instead of plotting |s|^2, which U fixes at 1:
  * for each coupling alpha: how many different end states 40 random starts reach, and whether each run
    settles (period 1), cycles (period p > 1) or does neither within the step budget;
  * how fast a run reaches its own end state.

Usage:
  python multi_orbit_bioswarm_v3.py            # figures and scan_v3.csv into ./figures
  python multi_orbit_bioswarm_v3.py --check    # the numerical checks quoted in the paper (no plotting)
Dependencies: numpy (matplotlib for figures).
"""
import csv, importlib.util, os, sys
from collections import Counter
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
_spec = importlib.util.spec_from_file_location("bio_v2", os.path.join(HERE, "multi_orbit_bioswarm.py"))
_bio = importlib.util.module_from_spec(_spec); sys.modules["bio_v2"] = _bio; _spec.loader.exec_module(_bio)
C, K, F, U = _bio.C_compress, _bio.K_clip, _bio.F_fold, _bio.U_unfold


def G(s, nb, alpha, b=0.1):
    return U(F(K(C(s), b), nb, alpha))


def run(N, alpha, T, seed):
    rng = np.random.default_rng(seed)
    S = [rng.uniform(-1, 1, 2) for _ in range(N)]
    hist = [np.array(S)]
    for _ in range(T):
        S = [G(S[i], S[(i + 1) % N], alpha) for i in range(N)]
        hist.append(np.array(S))
    return hist


def period(hist, pmax=40, tol=1e-9):
    for p in range(1, pmax):
        if np.abs(hist[-1 - p] - hist[-1]).max() < tol:
            return p
    return None


def scan(alpha, N=8, seeds=40, T=400):
    ends, pers = set(), []
    for seed in range(seeds):
        h = run(N, alpha, T, seed)
        ends.add(tuple(np.round(h[-1].ravel(), 4)))
        pers.append(period(h))
    c = Counter(pers)
    return {"alpha": alpha, "distinct": len(ends), "settle": c.get(1, 0),
            "cycle": sum(v for k, v in c.items() if k not in (1, None)), "neither": c.get(None, 0),
            "periods": dict(c)}


def run_checks():
    ok = True

    def check(name, cond):
        nonlocal ok
        print(("PASS  " if cond else "FAIL  ") + name)
        ok &= bool(cond)

    x, y, nb = np.array([1.0, 0.999]), np.array([0.999, 1.0]), np.array([0.6, 0.8])
    check("C jumps: inputs 0.002 apart go 1.32 apart under G at alpha = 0.3",
          abs(np.abs(G(x, nb, 0.3) - G(y, nb, 0.3)).sum() - 1.3203) < 1e-3)
    lim = set()
    for s0 in [(1, 0), (-1, 0), (0, 1), (0, -1), (0.3, 0.2), (-0.2, 0.9), (0.1, -0.7), (-0.5, -0.4)]:
        s = np.array(s0, float)
        for _ in range(50):
            s = G(s, s, 0.0)
        lim.add(tuple(np.round(s, 6)))
    check("alpha = 0: one agent has exactly 4 fixed points, (+-1, 0.1)/sqrt(1.01) and (0.1, +-1)/sqrt(1.01)", len(lim) == 4)
    S = run(12, 0.5, 6, 1)[-1]
    check("U fixes |s|^2 = 1 for every agent (noise-free)", np.allclose((S ** 2).sum(1), 1.0, atol=1e-12))
    r = {a: scan(a) for a in (0.0, 0.3, 0.4, 0.45, 0.5, 0.7, 0.9)}
    check("alpha in {0, 0.3}: 40 of 40 runs settle, to 40 different end states",
          all(r[a]["settle"] == 40 and r[a]["distinct"] == 40 for a in (0.0, 0.3)))
    check("alpha = 0.4: all 40 runs settle", r[0.4]["settle"] == 40)
    r42 = scan(0.42); r41 = scan(0.41)
    check("alpha = 0.41: all 40 runs settle; alpha = 0.42: 4 runs cycle with period 24",
          r41["settle"] == 40 and r42["periods"].get(24, 0) == 4)
    check("alpha = 0.45: cycles are present (period 16); in this sample the first appear at 0.42 (period 24)", r[0.45]["periods"].get(16, 0) > 0)
    check("alpha = 0.5: more runs cycle than settle", r[0.5]["cycle"] > r[0.5]["settle"])
    check("alpha >= 0.7: some runs neither settle nor repeat within 400 steps",
          r[0.7]["neither"] > 0 and r[0.9]["neither"] > 0)
    rat = []
    for seed in range(200):
        h = run(8, 0.3, 60, seed)
        fin = h[-1]
        rat.append(np.linalg.norm(h[6] - fin, axis=1).mean() / np.linalg.norm(h[0] - fin, axis=1).mean())
    check("alpha = 0.3: after 6 steps each run is within 1.5% of its own end state (200 runs)", max(rat) < 0.015)
    print("\n" + ("ALL CHECKS PASS" if ok else "SOME CHECKS FAILED"))
    return ok


def figures(out="figures"):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    os.makedirs(out, exist_ok=True)
    plt.rcParams.update({"font.family": "serif", "font.size": 11, "figure.dpi": 150})
    alphas = [round(0.05 * k, 2) for k in range(20)]
    rows = [scan(a) for a in alphas]
    with open(os.path.join(out, "scan_v3.csv"), "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["alpha", "distinct", "settle", "cycle", "neither", "periods"])
        w.writeheader()
        for r in rows:
            w.writerow(r)
    fig, ax = plt.subplots(1, 2, figsize=(11, 4.2))
    a = np.array(alphas)
    st = np.array([r["settle"] for r in rows]); cy = np.array([r["cycle"] for r in rows]); ne = np.array([r["neither"] for r in rows])
    ax[0].bar(a, st, width=0.04, color="#1a6b5a", label="settles (period 1)")
    ax[0].bar(a, cy, width=0.04, bottom=st, color="#c9a84c", label="cycles (period > 1)")
    ax[0].bar(a, ne, width=0.04, bottom=st + cy, color="#c0392b", label="neither, within 400 steps")
    ax[0].axvline(0.5, ls="--", color="#1a2744", lw=1)
    ax[0].set_xlabel("coupling alpha"); ax[0].set_ylabel("runs (of 40)"); ax[0].legend(fontsize=8, loc="lower left")
    ax[0].set_title("What each run does (N = 8, noise-free)")
    ax[1].plot(a, [r["distinct"] for r in rows], "o-", color="#1a2744")
    ax[1].axvline(0.5, ls="--", color="#1a2744", lw=1)
    ax[1].set_xlabel("coupling alpha"); ax[1].set_ylabel("different end states (of 40 runs)")
    ax[1].set_title("Multistability"); ax[1].set_ylim(0, 42); ax[1].grid(True, alpha=0.2)
    plt.tight_layout()
    for ext in ("pdf", "png"):
        plt.savefig(os.path.join(out, f"fig2_attractor_scan.{ext}"), bbox_inches="tight")
    plt.close()
    fig, ax = plt.subplots(figsize=(7.5, 4.5))
    for seed, col in zip(range(5), ["#1a2744", "#1a6b5a", "#c9a84c", "#c0392b", "#7f8c8d"]):
        h = run(8, 0.3, 30, seed)
        fin = h[-1]
        d = [max(np.linalg.norm(h[t] - fin, axis=1).mean(), 1e-17) for t in range(31)]
        ax.semilogy(range(31), d, color=col, lw=1.8)
    ax.axvline(6, ls=":", color="grey")
    ax.set_xlabel("step t"); ax.set_ylabel("mean distance to the run's own end state")
    ax.set_title("alpha = 0.3: five runs, five different end states, each reached fast")
    ax.grid(True, alpha=0.2)
    for ext in ("pdf", "png"):
        plt.savefig(os.path.join(out, f"fig3_settling.{ext}"), bbox_inches="tight")
    plt.close()
    for r in rows:
        print(r)


if __name__ == "__main__":
    if "--check" in sys.argv:
        sys.exit(0 if run_checks() else 1)
    figures()
