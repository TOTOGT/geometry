#!/usr/bin/env python3
"""
erdos_catalog_crosscheck.py -- mechanical check: does anything this corpus has
actually proved intersect anything in Bloom/Tao's structured Erdos-problem
database?

WHY THIS EXISTS.  Book XXIX's mission statement says a thread opens only
where a named open problem meets a named, kernel-checked corpus result.
"Cross-check the Erdos catalog against the corpus's proven lemmas" was
proposed as Book XXIX section 3 before anyone had actually run it. This
script runs it.

SOURCE.  teorth/erdosproblems (github.com/teorth/erdosproblems), the
community database backing erdosproblems.com and the FrontierMath Erdos
benchmark. Pin used for this run: commit af83692edd2aee68d512e04fb7b9b9c175a29bb0,
2026-09-26. Clone it yourself to reproduce or refresh:
    git clone https://github.com/teorth/erdosproblems.git
Then: python3 erdos_catalog_crosscheck.py /path/to/erdosproblems

WHAT IT CHECKS.  data/problems.yaml carries 43 tags across 1221 problems
(593 open, as of the pinned commit). This script matches those tags, plus a
full-text grep of README.md (which lists every problem with its tags and a
short note), against a keyword fingerprint of what this corpus has actually
proved: the n-bonacci recurrence ladder and its growth bound, the hex/A2-root-
lattice quadratic form, discrete Gauss-Bonnet, and the dm3 dynamical-systems
vocabulary (limit cycle, contact geometry, attractor). It is a topic-overlap
check, not a proof-content check -- a zero here means "nothing in the catalog
is even filed under a subject this corpus works in," which is a real, useful,
and much cheaper thing to know than a false claim of relevance would be.

RESULT (this run, 2026-09-27): zero matches, on every keyword tried, across
the full tag taxonomy and the full README text. See book29/ch02 for the
write-up.
"""
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("Requires pyyaml: pip install pyyaml --break-system-packages", file=sys.stderr)
    sys.exit(2)

KEYWORDS = [
    # n-bonacci recurrence ladder (NbonacciLadder.lean, TribonacciLog.lean)
    "recurrence", "fibonacci", "tribonacci", "tetranacci", "pentanacci",
    "hexabonacci", "nbonacci", "skolem",
    # hex / A2 root lattice (HexForm.lean)
    "loeschian", "eisenstein integer", "hexagonal lattice", "triangular lattice",
    "honeycomb", "tiling", "polyomino",
    # discrete Gauss-Bonnet (GaussBonnet.lean)
    "gauss-bonnet", "gauss bonnet", "euler characteristic", "discrete curvature",
    "triangulation",
    # dm3 operator vocabulary (Book 3 / Book V)
    "dynamical system", "limit cycle", "contact geometry", "attractor",
    "whitney fold", "reeb",
]


def load_tags_and_text(repo):
    repo = Path(repo)
    problems = yaml.safe_load((repo / "data" / "problems.yaml").read_text(encoding="utf-8"))
    readme = (repo / "README.md").read_text(encoding="utf-8", errors="ignore")
    all_tags = sorted({t for p in problems for t in p.get("tags", [])})
    return problems, readme, all_tags


def main():
    repo = sys.argv[1] if len(sys.argv) > 1 else "erdosproblems"
    problems, readme, all_tags = load_tags_and_text(repo)
    open_count = sum(1 for p in problems if p.get("informal_status", {}).get("state") == "open")

    print(f"erdos_catalog_crosscheck: {len(problems)} problems loaded, "
          f"{open_count} open, {len(all_tags)} unique tags\n")

    any_hit = False
    for kw in KEYWORDS:
        tag_hits = [t for t in all_tags if kw in t.lower()]
        text_hits = len(re.findall(re.escape(kw), readme, re.I))
        if tag_hits or text_hits:
            any_hit = True
            print(f"[MATCH] '{kw}': tags={tag_hits} readme_mentions={text_hits}")

    if not any_hit:
        print("No keyword in the corpus fingerprint appears in any tag or in "
              "README.md, across all 1221 problems.")
        print("\nAll tags actually present in the catalog:")
        print(", ".join(all_tags))

    sys.exit(0)


if __name__ == "__main__":
    main()
