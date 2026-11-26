"""Minimal executable example: legal admissibility A vs practical accessibility B.
TOY MODEL. All numbers are illustrative parameters, not law and not data.
Run: python3 legal_transition_demo.py   (deterministic, no dependencies)
"""
from itertools import product

# ---- system: states, legal transitions (time-windowed), cost (money), lag (days) ----
# legal[(r)] = (src, dst, window_start, window_end)   step may start at day t with ws <= t < we
LEGAL = {
    "file_motion":   ("Detained", "MotionFiled", 0, 4),      # must start before day 4
    "hearing":       ("MotionFiled", "BailSet", 0, 30),
    "post_bail":     ("BailSet", "Released", 0, 30),
    "waiver_req":    ("Detained", "WaiverGranted", 0, 4),    # means-tested fee/bail waiver (ROR-like)
    "waiver_release":("WaiverGranted", "Released", 0, 30),
}
LAG = {"file_motion": 1, "hearing": 3, "post_bail": 0, "waiver_req": 2, "waiver_release": 0}

def cost(r, params):
    return {"file_motion": params["filing"], "hearing": 0, "post_bail": params["bail"],
            "waiver_req": 0, "waiver_release": 0}[r]

def eligible(r, money, params):
    # means test: waiver only for those with money <= threshold. Non-monotone in money.
    if r == "waiver_req":
        return money <= params["means_threshold"]
    return True

def steps(state, t):
    return [r for r, (s, d, ws, we) in LEGAL.items() if s == state and ws <= t < we]

def admissible_paths(start, t0, horizon=30):
    """A: all legal paths ignoring resources and eligibility."""
    out = []
    def go(s, t, path):
        out.append((tuple(path), s, t))
        for r in steps(s, t):
            t2 = t + LAG[r]
            if t2 <= horizon:
                go(LEGAL[r][1], t2, path + [r])
    go(start, t0, [])
    return out

def accessible_paths(start, t0, money, params, horizon=30):
    """B: legal paths executable by an agent holding `money` (pays costs, passes means tests)."""
    out = []
    def go(s, t, m, path):
        out.append((tuple(path), s, t))
        for r in steps(s, t):
            c = cost(r, params)
            if c <= m and eligible(r, m, params):
                t2 = t + LAG[r]
                if t2 <= horizon:
                    go(LEGAL[r][1], t2, m - c, path + [r])
    go(start, t0, money, [])
    return out

def reach(paths, goal):
    return any(s == goal for (_, s, _) in paths)

P = {"filing": 20, "bail": 500, "means_threshold": 50}

if __name__ == "__main__":
    A = admissible_paths("Detained", 0)
    # (1) B subset of A for every resource level
    for m in [0, 10, 20, 100, 520, 1000]:
        B = accessible_paths("Detained", 0, m, P)
        assert set(B) <= set(A), m
    # (2) remedy available (in A) but obstructed (not in B) for low money without waiver eligibility
    assert reach(A, "Released")
    B0 = accessible_paths("Detained", 0, 100, P)      # money 100 > threshold 50, < 520
    assert not reach(B0, "Released")                   # obstructed: admissible but inaccessible
    O = set(A) - set(B0)
    assert len(O) > 0
    # (3) monotonicity holds on the sub-model WITHOUT means test (free disposal)
    P_nomeans = dict(P, means_threshold=-1)
    prev = set()
    for m in range(0, 700, 10):
        cur = set(accessible_paths("Detained", 0, m, P_nomeans))
        assert prev <= cur, m
        prev = cur
    # (4) monotonicity FAILS with a means-tested remedy: a poorer agent reaches a path a richer one cannot
    p_poor = set(accessible_paths("Detained", 0, 40, P))   # eligible for waiver
    p_mid = set(accessible_paths("Detained", 0, 100, P))   # not eligible, cannot pay bail
    assert reach(list(p_poor), "Released") and not reach(list(p_mid), "Released")
    assert not (p_poor <= p_mid)
    # (5) threshold (obstruction distance) to unlock release by payment: smallest money m* with Released in B
    # (searched over the ordinary payment route; waiver excluded by setting threshold below 0)
    mstar = next(m for m in range(0, 2000) if reach(accessible_paths("Detained", 0, m, P_nomeans), "Released"))
    assert mstar == P["filing"] + P["bail"]
    # (6) temporal obstruction: starting after the window closes removes the remedy from A itself
    A_late = admissible_paths("Detained", 4)
    assert not reach(A_late, "Released")
    # (7) finite-difference marginal value of liquidity (discrete 'price'), step function not a derivative
    V = lambda m: 1 if reach(accessible_paths("Detained", 0, m, P_nomeans), "Released") else 0
    jumps = [m for m in range(1, 2000) if V(m) != V(m - 1)]
    assert jumps == [mstar]
    print("all checks pass; unlock threshold m* =", mstar, "; obstruction set size at m=100:", len(O))
