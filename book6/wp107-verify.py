#!/usr/bin/env python3
"""
wp107-verify.py  --  regenerates every COMPUTED number in
book6/wp107-the-statement-was-not-theirs.html.

WP-107 audits the STATEMENT layer of OpenAI's Navier-Stokes / Euler release: not
whether the proofs are right, but whether the Prop being proved is the Clay
problem or something narrower that resembles it.  Its answer is structural -- the
Navier-Stokes challenge statement is Google DeepMind's, copied unmodified, so the
claimant could not have narrowed it.  That answer is a diff, and a diff is exactly
the kind of claim a reader should not have to take on trust.

  [1] provenance -- each ComparatorChallenges reference file names its upstream;
      the Navier-Stokes one pins a 40-hex commit, the Euler one does not;
  [2] normalised code-line counts, upstream vs the copy;
  [3] the unified diff: its length, and that every changed line is a DELETION,
      and that what was deleted is exactly the two positive alternatives (A)
      and (B) with their `sorry` placeholders;
  [4] the inherited definitions, byte-identical after the adaptations the copy's
      own header declares (attributes, and `local` on notation) are normalised;
  [5] the repo-wide escape search: sorry / admit / native_decide / axiom;
  [6] THE ASYMMETRY.  The Euler challenge file is NOT a copy -- its header says
      "adapted", it specialises rather than transcribes, and it links `main`
      rather than a commit.  So §3's structural argument covers Navier-Stokes and
      does NOT extend to Euler.  This block is why the script is worth having:
      it turns §7's "the Euler side is unaudited" into a specific finding.

Blocks [1]-[4] need only two files and fetch them over HTTPS.  Blocks [5]-[6]
need the OpenAI repository; pass --repo PATH to a checkout, or the script reports
them SKIPPED rather than guessing.

    git clone --depth 1 https://github.com/openai/NavierStokesAndEuler.git
    python3 wp107-verify.py --repo NavierStokesAndEuler

Requires only the standard library.  Exits 1 on any failure.
"""

import argparse
import difflib
import os
import re
import sys
import urllib.request

FAIL = []
SKIP = []

DM_COMMIT = "8bf45ed70d48b2b2a501de9c00b26bfa38c573ee"
DM_RAW = ("https://raw.githubusercontent.com/google-deepmind/formal-conjectures/"
          + DM_COMMIT + "/FormalConjectures/Millenium/NavierStokes.lean")
OA_RAW = ("https://raw.githubusercontent.com/openai/NavierStokesAndEuler/"
          "main/ComparatorChallenges/NavierStokes.lean")

CH_NS = os.path.join("ComparatorChallenges", "NavierStokes.lean")
CH_EU = os.path.join("ComparatorChallenges", "Euler.lean")


def check(label, got, want, note=None):
    ok = (got == want)
    print("  %s %-52s got=%s  want=%s" % ("OK  " if ok else "FAIL", label, got, want))
    if note:
        for line in note.split("\n"):
            print("       " + line)
    if not ok:
        FAIL.append(label)
    return ok


def skip(label, why):
    print("  SKIP %-52s %s" % (label, why))
    SKIP.append(label)


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "wp107-verify"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read().decode("utf-8")


# --------------------------------------------------------------- normalisation

def strip_block_comments(src):
    """Remove /- ... -/ regions, nesting-aware.  Covers /-! and /-- as well."""
    out, i, depth = [], 0, 0
    while i < len(src):
        if src.startswith("/-", i):
            depth += 1
            i += 2
            continue
        if src.startswith("-/", i) and depth:
            depth -= 1
            i += 2
            continue
        if depth == 0:
            out.append(src[i])
        i += 1
    return "".join(out)


# Exactly the page's declared strip list, and nothing beyond it: comments and
# docstrings (handled above), attributes, imports, open/namespace scaffolding,
# notation, and blank lines.  `variable {n : ℕ}` is deliberately RETAINED -- it
# binds the dimension in every definition below it and is therefore statement
# content, not scaffolding.  Dropping it is what turns 80/72 into 79/71.
DROP = ("import ", "open ", "namespace ", "end ", "@[", "attribute ",
        "notation", "local notation")


def code_lines(src):
    """The comparable content of a Lean file: no comments, docstrings, imports,
    attributes, namespace/section scaffolding, notation, or blank lines.  Every
    remaining line is stripped of leading indentation, because the copy reflows
    continuation lines and indentation is not content."""
    keep = []
    for ln in strip_block_comments(src).split("\n"):
        t = ln.strip()
        if not t or t == "open" or t == "end" or t.startswith("--"):
            continue
        if any(t.startswith(p) for p in DROP):
            continue
        keep.append(t)
    return keep


DECL = (r"^(?:noncomputable\s+)?(?:def|abbrev|structure|class|theorem|lemma|"
        r"instance)\s+([A-Za-z_][A-Za-z0-9_']*)")


def declarations(src):
    """Map name -> the declaration's own text: the keyword line plus its indented
    continuation, with blank lines dropped.  Deliberately EXCLUDES the attribute
    and notation lines that sit around a declaration, because those are what the
    copy's header says were adapted.  Excluding them is a normalisation and is
    reported as one -- see block [4]."""
    L = src.split("\n")
    out = {}
    for i, ln in enumerate(L):
        m = re.match(DECL, ln)
        if not m:
            continue
        j = i + 1
        while j < len(L) and (not L[j].strip() or L[j][:1] in " \t"):
            if not L[j].strip() and j + 1 < len(L) and L[j + 1][:1] not in " \t":
                break
            j += 1
        out.setdefault(m.group(1), "\n".join(x for x in L[i:j] if x.strip()))
    return out


# ------------------------------------------------------------------ the checks

ap = argparse.ArgumentParser()
ap.add_argument("--repo", help="path to a checkout of openai/NavierStokesAndEuler")
ap.add_argument("--upstream", help="local copy of DeepMind's NavierStokes.lean")
ap.add_argument("--copy", help="local copy of the OpenAI challenge file")
args = ap.parse_args()

print()
print("[0] inputs")
try:
    if args.upstream:
        up = open(args.upstream, encoding="utf-8").read()
        print("       upstream from %s" % args.upstream)
    else:
        up = fetch(DM_RAW)
        print("       upstream fetched at commit %s" % DM_COMMIT[:7])
    if args.copy:
        oa = open(args.copy, encoding="utf-8").read()
    elif args.repo:
        oa = open(os.path.join(args.repo, CH_NS), encoding="utf-8").read()
    else:
        oa = fetch(OA_RAW)
    print("       copy: %s" % (args.copy or (args.repo and CH_NS) or "fetched at main"))
except Exception as e:                                    # noqa: BLE001
    print("  FAIL could not obtain the two statement files: %s" % e)
    print("\nFAILED: inputs")
    sys.exit(1)

# ------------------------------------------------------------------------- [1]
print()
print("[1] provenance, as each file states it")
check("copy's header names DeepMind's file", "formal-conjectures" in oa, True)
check("copy's header pins the 40-hex commit", DM_COMMIT in oa, True,
      "A pinned commit is what makes block [2] reproducible. The Euler\n"
      "challenge file does not have one -- block [6].")
check("copy declares what it adapted",
      all(w in oa for w in ("imports", "attributes", "notation")), True,
      "'imports, metadata attributes, namespace, and local notation are\n"
      "adapted'. That is a checkable claim, and block [4] checks it.")
check("copy declares the retained placeholders", "challenge placeholders" in oa
      or "intentional" in oa, True)

# ------------------------------------------------------------------------- [2]
print()
print("[2] normalised code-line counts")
A, B = code_lines(up), code_lines(oa)
check("upstream code lines", len(A), 80)
check("copy code lines", len(B), 72,
      "NOTE. The page as first published read 71 here. The count is 72 and the\n"
      "page carries a dated correction. The substantive claim -- deletions only,\n"
      "and only of (A) and (B) -- is unaffected and is block [3].")
check("the copy is a strict subset of upstream", set(B) <= set(A), True,
      "No line of the copy is absent from upstream. Whatever else the copy is,\n"
      "it introduces no statement text of its own.")

# ------------------------------------------------------------------------- [3]
print()
print("[3] the unified diff")
diff = list(difflib.unified_diff(A, B, "upstream", "openai", lineterm=""))
check("unified diff length (default context n=3)", len(diff), 17)
changed = [d for d in diff if d[:1] in "+-" and not d.startswith(("---", "+++"))]
check("every changed line is a deletion",
      sorted({d[0] for d in changed}), ["-"],
      "This is the whole audit in one assertion. An addition here would mean the\n"
      "claimant had written statement text, and the structural argument of §3\n"
      "would collapse into a line-by-line reading.")
check("deleted lines", len(changed), 8)
deleted = "\n".join(d[1:] for d in changed)
check("deletion is theorem (A)", "navier_stokes_existence_and_smoothness_R3" in deleted, True)
check("deletion is theorem (B)", "navier_stokes_existence_and_smoothness_periodic" in deleted, True)
check("and their placeholders", deleted.count("sorry"), 2)
check("the two BREAKDOWN theorems survive in the copy",
      sum(1 for l in B if l.startswith("theorem navier_stokes_breakdown")), 2,
      "(C) on R^3 and (D) on the torus -- the alternatives being claimed. They\n"
      "are DeepMind's own sorry-ed challenges, discharged elsewhere in the repo.")
check("no breakdown theorem was touched",
      any("breakdown" in d for d in changed), False)

# ------------------------------------------------------------------------- [4]
print()
print("[4] the inherited definitions, byte for byte")
print("       Compared as declaration text only: the keyword line and its indented")
print("       continuation. Attribute lines and the `local` on notation are excluded,")
print("       because those are the adaptations the header declares. Excluding them")
print("       is a normalisation, and pretending otherwise would be the move this")
print("       corpus refuses -- so it is named here rather than buried.")
NAMES = ["divergence", "IsOnePeriodic",
         "InitialVelocityCondition", "InitialVelocityConditionDecay",
         "InitialVelocityConditionPeriodic",
         "ForceCondition", "ForceConditionDecay", "ForceConditionPeriodic",
         "NavierStokesExistenceAndSmoothness",
         "NavierStokesExistenceAndSmoothnessRn",
         "NavierStokesExistenceAndSmoothnessPeriodic"]
DA, DB = declarations(up), declarations(oa)
same, total_bytes = 0, 0
for n in NAMES:
    a, b = DA.get(n), DB.get(n)
    if a is not None and a == b:
        same += 1
        total_bytes += len(a.encode())
    else:
        print("       DIFFERS: %s" % n)
check("declarations byte-identical", same, len(NAMES),
      "%d of %d, %d bytes. The page named nine; there are eleven, the two extra\n"
      "being the Periodic variants of the initial-velocity and force conditions."
      % (same, len(NAMES), total_bytes))
check("the negated solution notion is among them",
      DA.get("NavierStokesExistenceAndSmoothnessRn") ==
      DB.get("NavierStokesExistenceAndSmoothnessRn"), True,
      "This is the one that decides §2. Strengthening the solution notion would\n"
      "weaken the negation and make (C) into something narrower. It is unchanged.")

# ------------------------------------------------------------------------- [5]
print()
print("[5] the repo-wide escape search")
if not args.repo:
    skip("escape search", "no --repo given")
    skip("file and line census", "no --repo given")
else:
    files = []
    for dp, dn, fn in os.walk(args.repo):
        if ".git" in dp.split(os.sep):
            continue
        files += [os.path.join(dp, f) for f in fn if f.endswith(".lean")]
    files.sort()
    refs = {os.path.normpath(os.path.join(args.repo, CH_NS)),
            os.path.normpath(os.path.join(args.repo, CH_EU))}
    pats = {"sorry": r"\bsorry\b", "admit": r"\badmit\b",
            "native_decide": r"\bnative_decide\b", "axiom": r"^\s*axiom\s+"}
    lines, hits = 0, {k: [] for k in pats}
    for p in files:
        s = open(p, encoding="utf-8", errors="replace").read()
        lines += s.count("\n") + (1 if s and not s.endswith("\n") else 0)
        if os.path.normpath(p) in refs:
            continue
        for k, rx in pats.items():
            for m in re.finditer(rx, s, re.M):
                hits[k].append((p, s[:m.start()].count("\n") + 1))
    check("Lean files", len(files), 2486)
    check("Lean lines", lines, 616276)
    for k in ("sorry", "admit", "native_decide", "axiom"):
        check("%s, outside the reference files" % k, len(hits[k]), 0,
              None if hits[k] else None)
    print("       NOTE. The page excludes 'the challenge reference file', singular.")
    print("       There are two, and the Euler one carries the only two `sorry`s in")
    print("       the repository. The page carries a dated correction. Excluding")
    print("       both is the same rationale, not a wider one: each says in its own")
    print("       header that its placeholders are intentional.")
    print("       This is a statement about SOURCE TEXT. It is not a build, not a")
    print("       type-check, and not an axiom report.")

# ------------------------------------------------------------------------- [6]
print()
print("[6] the asymmetry -- and why §3 does not cover Euler")
if not args.repo:
    skip("Euler provenance", "no --repo given")
else:
    try:
        eu = open(os.path.join(args.repo, CH_EU), encoding="utf-8").read()
    except OSError as e:                                   # noqa: BLE001
        eu = ""
        print("       could not read %s: %s" % (CH_EU, e))
    if eu:
        check("Euler challenge names the same upstream FILE",
              "formal-conjectures" in eu and "NavierStokes.lean" in eu, True)
        check("Euler challenge pins NO commit", DM_COMMIT in eu, False,
              "It links `main`, a moving target. The Navier-Stokes comparison in\n"
              "block [2] is reproducible; an equivalent comparison for Euler is\n"
              "not, because there is no stated version to compare against.")
        check("Euler challenge says 'adapted', not 'copied'",
              "Adapted from" in eu or "adapted from" in eu, True)
        check("and it SPECIALISES rather than transcribes",
              "specialized" in eu or "specialised" in eu, True,
              "'the whole-space breakdown alternative specialized to zero\n"
              "viscosity and zero external force.' A specialisation is authored.")
        check("Euler statement text is NOT a subset of upstream",
              set(code_lines(eu)) <= set(A), False,
              "THE FINDING. §3's argument is that the claimant could not have\n"
              "narrowed the target because they did not write it. That holds for\n"
              "Navier-Stokes and does not hold here: the Euler challenge Prop was\n"
              "written by the claimant. It may be perfectly faithful -- nothing\n"
              "here says it is not -- but it is a statement that has to be read,\n"
              "not a provenance that can be checked. §7 marks the Euler side OPEN;\n"
              "this block says what specifically is open about it.")
        check("Euler placeholders are declared intentional",
              "intentional" in eu, True)

# ---------------------------------------------------------------------- verdict
print()
if SKIP:
    print("SKIPPED (no --repo): " + ", ".join(SKIP))
if FAIL:
    print("FAILED: " + ", ".join(FAIL))
    sys.exit(1)
print("ALL CHECKS PASSED" + (" (partial -- see SKIPPED)" if SKIP else ""))
