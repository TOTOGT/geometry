#!/usr/bin/env python3
"""Verify Book XVII's elementary-row claims against the Lean files that close them.

Usage:  python3 book17/book17-claims-verify.py        (from the repository root)

Book XVII's index and chapter 1 each print a short list of facts about how a
total-function kernel behaves.  For one commit those lists carried the marker
[documented], which meant: read somewhere, not run here.  That marker is the
thing this book exists to object to, so it is now [VERIFIED], and this script
is what the word stands on.

It checks four things and returns non-zero if any fails:

  1. every claim string still appears on the page that is said to print it
     -- so a later edit to the prose cannot silently orphan a proof;
  2. every claim is paired with a theorem name that exists in the Lean file
     named beside it -- so the marker cannot outlive the proof;
  3. the Lean files hash to the bytes that were run;
  4. tools/axiom_gate.py passes on both saved #print axioms reports, at the
     expected theorem counts.

Point 3 is the one that does work.  The reports in book17/*.axioms.txt are
the output of a run that is over; re-reading them proves nothing about the
current .lean files unless the bytes are the same bytes.  The hashes below
were taken from the files the toolchain read.

Re-running the kernel itself needs the toolchain, and for Book17Mathlib.lean
it needs Mathlib at tag v4.33.0-rc1:

    lean book17/Book17Core.lean                  # no library required
    lake env lean .../Book17Mathlib.lean         # from a mathlib4 checkout
"""
import hashlib
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]

SHA = {
    "book17/Book17Core.lean":
        "0901b310ad6bc5a1f0dfae94f36150a648f5999eeb86eb3e9df6a4b8e11fcf32",
    "book17/Book17Mathlib.lean":
        "7d7a49f814795f37e552e727eb9e94d4d04393b395eb730c7b2a1bd0d81ea47a",
}

REPORTS = [
    ("book17/book17-core.axioms.txt", 12),
    ("book17/book17-mathlib.axioms.txt", 9),
]

# (page, exact string the page prints, lean file, theorem that closes it)
CLAIMS = [
    ("book17/ch01-the-names-it-already-has.html",
     "(3 : ℕ) - 5 = 0", "book17/Book17Core.lean", "nat_sub_truncates"),
    ("book17/ch01-the-names-it-already-has.html",
     "x / 0 = 0", "book17/Book17Core.lean", "nat_div_zero"),
    ("book17/ch01-the-names-it-already-has.html",
     "0<sup>0</sup> = 1", "book17/Book17Core.lean", "nat_zero_pow_zero"),
    ("book17/ch01-the-names-it-already-has.html",
     "√(&minus;1) = 0", "book17/Book17Mathlib.lean", "sqrt_neg_one"),
    ("book17/index.html",
     "natural subtraction truncates", "book17/Book17Core.lean",
     "nat_sub_truncates"),
    ("book17/index.html",
     "division by zero is defined", "book17/Book17Core.lean", "nat_div_zero"),
    ("book17/index.html",
     "has a value", "book17/Book17Core.lean", "nat_zero_pow_zero"),
    ("book17/index.html",
     "limits are filters", "book17/Book17Mathlib.lean",
     "tendsto_is_filter_le"),
    ("book17/index.html",
     "measurable-space instance with side conditions",
     "book17/Book17Mathlib.lean", "variance_is_total"),
]


def sha256(path):
    return hashlib.sha256((ROOT / path).read_bytes()).hexdigest()


def main():
    fail = []

    if "--rehash" in sys.argv:
        for path in SHA:
            print(f'    "{path}":\n        "{sha256(path)}",')
        return 0

    for page, text, leanfile, thm in CLAIMS:
        p = ROOT / page
        if not p.exists():
            fail.append(f"{page}: missing")
            continue
        if text not in p.read_text(encoding="utf-8"):
            fail.append(f"{page}: no longer prints {text!r}")
        lf = ROOT / leanfile
        if not lf.exists():
            fail.append(f"{leanfile}: missing")
            continue
        src = lf.read_text(encoding="utf-8")
        if not re.search(rf"^theorem {re.escape(thm)}\b", src, re.M):
            fail.append(f"{leanfile}: no theorem {thm} for {page} claim {text!r}")

    for path, want in SHA.items():
        if want is None:
            continue
        got = sha256(path)
        if got != want:
            fail.append(f"{path}: sha256 {got} != recorded {want}; "
                        f"re-run the kernel, then --rehash")

    for report, count in REPORTS:
        r = subprocess.run(
            [sys.executable, str(ROOT / "tools" / "axiom_gate.py"),
             str(ROOT / report), str(count)],
            capture_output=True, text=True)
        out = (r.stdout + r.stderr).strip()
        print(f"  {report}: {out}")
        if r.returncode != 0:
            fail.append(f"{report}: gate returned {r.returncode}")

    for f in fail:
        print(f"::error::{f}")
    if fail:
        return 1
    print(f"OK: {len(CLAIMS)} published claims, each paired with a theorem "
          f"that the kernel checked.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
