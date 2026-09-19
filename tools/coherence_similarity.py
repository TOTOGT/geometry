#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Pablo Nogueira Grossi / G6 LLC
"""
coherence_similarity.py -- run the similarity test on the Coherence Bridge.

WHY. The bridge table says sixteen domains "instantiate the same contact normal
form with parameters (mu_max, omega, beta, kappa*)", and until 2026-09-18 two live
pages said they "are not analogies, they are exact mathematical identities."
Book XVII ch 1 found that one row of its translation table is a real identity with
a decision procedure attached: two matrices are SIMILAR exactly when they represent
one linear map in different bases (Hefferon p. 274). That is a test. This runs it.

THE TEST. Near Gamma each domain is a 2x2 linear system with eigenvalues
mu +- i*omega -- a spiral sink when mu < 0. For such matrices:

  (a) LINEAR SIMILARITY: similar iff the eigenvalue pairs agree. Same map,
      different basis.
  (b) SIMILARITY UP TO TIME-RESCALING: t -> c*t scales mu and omega together,
      so the invariant is the ratio mu/omega. This is the weakest reading under
      which "same normal form, different parameters" could still mean similar.
  (c) TOPOLOGICAL CONJUGACY: every 2D linear spiral sink is topologically
      conjugate to every other. [standard]

Rows are PARSED from book4/hub.html, not transcribed.

    python3 tools/coherence_similarity.py

Exit 0 always -- this reports a measurement, it does not gate.
"""
import math, os, re, sys

SRC = "book4/hub.html"

def parse(path):
    s = open(path, encoding="utf-8").read()
    out = []
    for m in re.finditer(r'<tr><td class="domain">(.*?)</td>(.*?)</tr>', s, re.S):
        name = re.sub(r"<[^>]*>", "", m.group(1)).strip()
        cells = [re.sub(r"<[^>]*>", "", c).strip()
                 for c in re.findall(r"<td[^>]*>(.*?)</td>", m.group(2), re.S)]
        if len(cells) < 2:
            continue
        out.append((name, cells[0], cells[1]))
    return out

def num(t):
    t = t.replace("−", "-").replace("–", "-").replace("×", "*").strip()
    if t in ("", "—", "-", "variable", "n/a"):
        return None
    m = re.fullmatch(r"2π/(\d+)", t) or re.fullmatch(r"2pi/(\d+)", t)
    if m:
        return 2 * math.pi / float(m.group(1))
    m = re.fullmatch(r"(-?[\d.]+)\s*\*\s*10⁻?([⁴⁵⁰-⁹\d-]+)", t)
    try:
        return float(t)
    except ValueError:
        pass
    m = re.match(r"(-?[\d.]+)[^\d]*10.*?(-?\d+)", t)
    if m:
        return float(m.group(1)) * 10 ** float(m.group(2))
    return None

def main():
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    path = os.path.join(root, SRC)
    rows = [(n, num(a), num(b)) for n, a, b in parse(path)]
    good = [(n, mu, w) for n, mu, w in rows if mu is not None and w is not None]
    print("  %d rows parsed from %s; %d carry both mu and omega\n" % (len(rows), SRC, len(good)))

    print("  %-34s %8s %12s %12s" % ("domain", "mu", "omega", "mu/omega"))
    for n, mu, w in good:
        print("  %-34s %8.4f %12.6g %12.4f" % (n[:34], mu, w, mu / w))
    for n, mu, w in rows:
        if mu is None or w is None:
            print("  %-34s %8s %12s %12s" % (n[:34], "-" if mu is None else "%.4f" % mu, "not numeric", "-"))

    print("\n  (a) LINEAR SIMILARITY -- eigenvalue pairs must agree exactly")
    pairs = [(a, b) for i, a in enumerate(good) for b in good[i + 1:]
             if abs(a[1] - b[1]) < 1e-12 and abs(a[2] - b[2]) < 1e-12]
    print("      similar pairs: %d of %d possible" % (len(pairs), len(good) * (len(good) - 1) // 2))

    print("\n  (b) UP TO TIME-RESCALING -- the invariant is mu/omega")
    rs = [(a, b, abs(a[1] / a[2] - b[1] / b[2])) for i, a in enumerate(good) for b in good[i + 1:]]
    exact = [p for p in rs if p[2] < 1e-9]
    close = sorted(rs, key=lambda p: p[2])[:3]
    print("      exact matches: %d of %d possible" % (len(exact), len(rs)))
    print("      closest three, none of them equal:")
    for a, b, d in close:
        print("        %-26s %-26s  |diff| = %.4f" % (a[0][:26], b[0][:26], d))

    print("\n  (c) TOPOLOGICAL CONJUGACY -- [standard]")
    sinks = [n for n, mu, w in good if mu < 0 and w > 0]
    print("      spiral sinks (mu < 0, omega > 0): %d of %d" % (len(sinks), len(good)))
    print("      Every 2D linear spiral sink is topologically conjugate to every other.")
    print("      So this property is shared, and is shared by ANY such system --")
    print("      it is not evidence of a common mechanism.")

    print("\n  READING")
    print("    Under the strict test the bridge has %d similar pairs." % len(pairs))
    print("    Under the most generous test that still means 'similar', it has %d." % len(exact))
    print("    What the rows do share is being spiral sinks, which is a class so")
    print("    wide that membership carries no information about mechanism.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
