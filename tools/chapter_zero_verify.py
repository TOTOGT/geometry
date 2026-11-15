#!/usr/bin/env python3
"""chapter_zero_verify.py — recompute the numbers behind the VERIFIED rows of docs/definitions.md
and check that each generated Chapter 0 page matches what tools/chapter_zero.py would write now.

  python3 tools/chapter_zero_verify.py            all books
  python3 tools/chapter_zero_verify.py --book 4
Pure Python (no scipy). Exit 1 on any failure. R24: the page says VERIFIED only because this ran first.
"""
import argparse, hashlib, math, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import chapter_zero as cz

FAIL = []
def check(ok, msg):
    print(("  PASS  " if ok else "  FAIL  ") + msg)
    if not ok: FAIL.append(msg)

def rk4(f, r, z, dt):
    k1 = f(r, z); k2 = f(r + dt/2*k1[0], z + dt/2*k1[1])
    k3 = f(r + dt/2*k2[0], z + dt/2*k2[1]); k4 = f(r + dt*k3[0], z + dt*k3[1])
    return (r + dt/6*(k1[0] + 2*k2[0] + 2*k3[0] + k4[0]), z + dt/6*(k1[1] + 2*k2[1] + 2*k3[1] + k4[1]))

def toy(r, z):                         # dm3 toy model, epsilon = 2 (Book 4 ch10)
    e = math.exp(-z)
    return (r*(1 - r*r) + 2*(r - 1)*e, r*r - 2*(r - 1)**2*e)

def converges(r0, z0=0.0, dt=2e-3, T=30.0):
    r, z = r0, z0
    for _ in range(int(T/dt)):
        r, z = rk4(toy, r, z, dt)
        if r < 1e-4 or z < -30: return False
    return abs(r - 1) < 1e-3

def math_checks():
    print("[1] numbers behind the VERIFIED rows")
    rs = 2*math.cos(3*math.pi/7)
    check(abs(rs**3 - rs**2 - 2*rs + 1) < 1e-12, f"saddle r_s = 2cos(3π/7) = {rs:.6f} solves r³ − r² − 2r + 1 = 0")
    # tau = sqrt(c/kappa), V = lam*rho^2 with rho_dot = -2 rho  => c = 4, kappa_noise = lam
    for lam in (0.5, 1, 2, 4):
        check(abs(math.sqrt(4/lam)*math.sqrt(lam) - 2) < 1e-12, f"τ·√λ = 2 at λ = {lam}  (τ → τ/√λ)")
    check(abs(math.sqrt(4/1) - 2) < 1e-12, "V = ρ²: c = 4, κ_noise = 1, τ = 2")
    check(abs(math.sqrt(4/0.5) - 2*math.sqrt(2)) < 1e-12, "W = ½ρ²: τ = 2√2 ≈ 2.83")
    check(abs(2/(2*(1 + 2)) - 1/3) < 1e-15 and abs(2/(2*(1 + 3)) - 1/4) < 1e-15, "ε₀ = 1/3 iff sup‖Hess V‖ = 2 (H = 3 gives 1/4)")
    lo, hi = 0.5, 1.0
    for _ in range(28):
        m = (lo + hi)/2
        if converges(m): hi = m
        else: lo = m
    check(abs(hi - 0.77594058) < 2e-4, f"r* = {hi:.6f} at z(0)=0 (Book 4 ch10 certifies 0.77594058)")
    check(1 - hi < 1/3, f"displacement 1 − r* = {1-hi:.4f} < ε₀ = 1/3: the Gronwall disc crosses the fold inward")
    check(not converges(0.70) and converges(0.80), "r0 = 0.70 escapes, r0 = 0.80 converges (inside the Gronwall gap 0.667–0.776)")

# Four other generators add boxes to every chapter page (subject_tags, gold_standard, run_yourself, crossref); each has its own
# --check. This verifier compares only what chapter_zero.py owns, so those regions are removed first -- but only if they are
# exactly the expected regions: right count, begin/end alternating, nothing nested, no stray marker, and no chapter content
# (heading or table) inside a region. Anything else is reported as a problem and the page fails; nothing is silently excluded.
BOX_COUNTS = {"subject": 2, "gss": 1, "run": 1, "related": 1}   # regions per chapter page (subject: head meta + body tags)
MARK = re.compile(r"<!--(/?)po-([A-Za-z0-9_-]+)-->")
def strip_boxes(src):
    problems, regions, open_at = [], [], {}
    for m in MARK.finditer(src):
        end, name = bool(m.group(1)), m.group(2)
        if name not in BOX_COUNTS:
            problems.append(f"unknown marker {m.group(0)}"); continue
        if open_at:
            other = next(iter(open_at))
            if not end or name != other:
                problems.append(f"{m.group(0)} inside an open {other} region"); continue
        if not end:
            if name in open_at: problems.append(f"nested {m.group(0)}")
            open_at[name] = m.start()
        else:
            if name not in open_at: problems.append(f"{m.group(0)} without a begin marker"); continue
            start = open_at.pop(name); stop = m.end()
            inner = src[start:stop]
            if re.search(r"<(h1|h2|table)\b", inner, re.I): problems.append(f"{name} region contains chapter content (heading or table)")
            regions.append((name, start, stop))
    for name, start in open_at.items(): problems.append(f"po-{name} begin marker has no end marker")
    for name, want in BOX_COUNTS.items():
        have = sum(1 for r in regions if r[0] == name)
        if have != want: problems.append(f"po-{name}: {have} region(s), expected {want}")
    out, pos = [], 0
    for name, start, stop in sorted(regions, key=lambda r: r[1]):
        out.append(src[pos:start]); pos = stop
        if src[pos:pos + 1] == "\n": pos += 1
    out.append(src[pos:])
    return "".join(out), problems

def page_checks(books):
    print("[2] generated pages match definitions.md")
    md = open(cz.SRC, encoding="utf-8").read(); sha = hashlib.sha1(md.encode()).hexdigest()[:10]
    sections = cz.parse(md)
    strip = lambda s: re.sub(r"Generated \d{4}-\d{2}-\d{2}", "Generated DATE", s)
    for n in books:
        d = cz.BOOKS[n][0]; p = os.path.join(cz.ROOT, d, "ch00-definitions.html")
        if not os.path.exists(p): check(False, f"{d}/ch00-definitions.html is missing"); continue
        have = open(p, encoding="utf-8").read()
        body, problems = strip_boxes(have)
        for pr in problems: check(False, f"{d}/ch00-definitions.html box markers: {pr}")
        check(not problems, f"{d}/ch00-definitions.html has exactly the expected generator boxes, well formed")
        check(not problems and strip(body) == strip(cz.render(n, sections, sha)), f"{d}/ch00-definitions.html is current (sha1 {sha})")

if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("--book", type=int); a = ap.parse_args()
    math_checks(); page_checks([a.book] if a.book else sorted(cz.BOOKS))
    print("\nALL CHECKS PASSED" if not FAIL else f"\n{len(FAIL)} FAILED")
    sys.exit(1 if FAIL else 0)
