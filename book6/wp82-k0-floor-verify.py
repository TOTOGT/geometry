#!/usr/bin/env python3
"""
wp82-k0-floor-verify.py

WP-82 records that "Mathlib has no K-theory, so Volume XI cannot have a
machine-checked core." Re-checked 2026-09-17 against the pinned checkout, that
sentence is true of the NAME and misleading about the CONTENT.

Source for the K-theory (input, not proved here):
  C. A. Weibel, The K-book: An Introduction to Algebraic K-theory,
  GSM 145, AMS 2013. Ch. I-II: K_0, group completion, projective modules.
  For a Dedekind domain R,  K_0(R) = Z (+) Pic(R), and for R = O_K the ring
  of integers of a number field, Pic(O_K) = Cl(K), the ideal class group.

Two blocks. [1] measures what the pinned Mathlib actually contains.
[2] computes class numbers from scratch, exactly, by counting reduced binary
quadratic forms -- the arithmetic that K_0(O_K) is built out of.

Standard library only.
"""

import os, subprocess, math
from decimal import Decimal as D, getcontext

FAIL = []
def check(name, ok, detail=""):
    print(("  PASS  " if ok else "  FAIL  ") + name + (("   " + detail) if detail else ""))
    if not ok: FAIL.append(name)

HERE = os.path.dirname(os.path.abspath(__file__))
MATHLIB = os.path.normpath(os.path.join(HERE, "..", ".lake", "packages", "mathlib", "Mathlib"))

print("[1] What the pinned Mathlib contains, measured rather than remembered.")
print()
if not os.path.isdir(MATHLIB):
    print("    Mathlib checkout not present at %s" % MATHLIB)
    print("    Block [1] SKIPPED -- it measures a checkout, and there is none.")
else:
    try:
        rev = subprocess.run(["git", "-C", os.path.dirname(MATHLIB), "log", "--oneline", "-1"],
                             capture_output=True, text=True, timeout=20).stdout.strip()
    except Exception:
        rev = "(git unavailable)"
    print("    checkout: %s" % rev)
    print()

    def count(term):
        n = 0
        for root, _, files in os.walk(MATHLIB):
            for f in files:
                if not f.endswith(".lean"): continue
                try:
                    with open(os.path.join(root, f), encoding="utf-8", errors="ignore") as fh:
                        if term in fh.read(): n += 1
                except OSError:
                    pass
        return n

    has_ktheory_dir = os.path.isdir(os.path.join(MATHLIB, "KTheory"))
    has_classnum_dir = os.path.isdir(os.path.join(MATHLIB, "NumberTheory", "ClassNumber"))
    nf_classnum = os.path.isfile(os.path.join(MATHLIB, "NumberTheory", "NumberField", "ClassNumber.lean"))
    rt_classgroup = os.path.isfile(os.path.join(MATHLIB, "RingTheory", "ClassGroup.lean"))

    print("      Mathlib/KTheory/                          %s" % ("present" if has_ktheory_dir else "ABSENT"))
    print("      Mathlib/NumberTheory/ClassNumber/         %s" % ("present" if has_classnum_dir else "ABSENT"))
    print("      Mathlib/NumberTheory/NumberField/ClassNumber.lean  %s" % ("present" if nf_classnum else "ABSENT"))
    print("      Mathlib/RingTheory/ClassGroup.lean        %s" % ("present" if rt_classgroup else "ABSENT"))
    print()
    for term in ("ClassGroup", "classNumber", "IsDedekindDomain", "FractionalIdeal", "Projective"):
        print("      files containing %-18s %4d" % (term, count(term)))
    print()

    check("WP-82's claim still holds on the name: there is no KTheory directory",
          not has_ktheory_dir)
    check("but the class group is present and named", rt_classgroup)
    check("and the class NUMBER of a number field is present", nf_classnum and has_classnum_dir)

    # The specific declarations that matter.
    want = {
        "NumberTheory/NumberField/ClassNumber.lean": [
            "noncomputable def classNumber",
            "classNumber_ne_zero",
            "classNumber_pos",
            "classNumber_eq_one_iff",
        ],
    }
    print("    Declarations found in Mathlib/NumberTheory/NumberField/ClassNumber.lean:")
    for path, names in want.items():
        full = os.path.join(MATHLIB, path)
        try:
            txt = open(full, encoding="utf-8", errors="ignore").read()
        except OSError:
            txt = ""
        for nm in names:
            here = nm in txt
            print("      %-32s %s" % (nm, "yes" if here else "no"))
            check("Mathlib declares %s" % nm, here)
    print()
    print("    classNumber_pos and classNumber_ne_zero are proved from Fintype.card,")
    print("    which means the FINITENESS of the class group is established, not")
    print("    assumed. That is the hard theorem in this area and it is done.")

print()
print("    THE CORRECTION. K_0(O_K) = Z (+) Cl(K) for a number field K (Weibel,")
print("    Ch. I-II). Mathlib holds Cl(K), its finiteness, classNumber, and the")
print("    criterion classNumber = 1 <-> the ring of integers is a PID. What it")
print("    does not hold is the DEFINITION of K_0 and the structure theorem")
print("    joining the two. That is a definition and a bridge lemma, not a field.")
print("    WP-82's sentence is right about the name and overstates the obstacle:")
print("    Volume XI's easiest machine-checked theorem is much closer than")
print("    'Mathlib has no K-theory' implies.")

# ----------------------------------------------------------------------------
print()
print("[2] The arithmetic K_0(O_K) is built out of, computed from scratch.")
print("    h(D) = the number of reduced binary quadratic forms (a,b,c) with")
print("    b^2 - 4ac = D,  |b| <= a <= c,  and b >= 0 when |b| = a or a = c.")
print("    Exact integer arithmetic, exhaustive, no tables.")
print()

def class_number(Dsc):
    """Form class number of a negative discriminant, by exhaustion."""
    assert Dsc < 0 and Dsc % 4 in (0, 1)
    h = 0
    amax = math.isqrt(-Dsc // 3)
    for a in range(1, amax + 1):
        for b in range(-a + 1, a + 1):
            num = b * b - Dsc
            if num % (4 * a): continue
            c = num // (4 * a)
            if c < a: continue
            if (abs(b) == a or a == c) and b < 0: continue
            h += 1
    return h

def disc_of(d):
    """Fundamental discriminant of Q(sqrt(-d)) for squarefree d > 0."""
    return -d if d % 4 == 3 else -4 * d

print("      d      disc      h(Q(sqrt(-d)))")
known = {1:1, 2:1, 3:1, 5:2, 6:2, 7:1, 10:2, 11:1, 13:2, 14:4, 15:2,
         19:1, 23:3, 26:6, 29:6, 31:3, 43:1, 47:5, 67:1, 163:1}
for d in sorted(known):
    Dd = disc_of(d); h = class_number(Dd)
    ok = (h == known[d])
    print("    %5d   %7d   %4d   %s" % (d, Dd, h, "" if ok else "<-- MISMATCH"))
    check("h(Q(sqrt(-%d))) = %d" % (d, known[d]), ok, "got %d" % h)

heegner = [d for d in range(1, 200) if all(d % (p*p) for p in range(2, 15))
           and class_number(disc_of(d)) == 1]
print()
print("    Class number one, d squarefree below 200, computed not looked up:")
print("      %s" % heegner)
check("the Heegner numbers come out exactly 1,2,3,7,11,19,43,67,163",
      heegner == [1, 2, 3, 7, 11, 19, 43, 67, 163], str(heegner))
print("    Baker, Heegner and Stark: that list is complete. There is no tenth.")

# ----------------------------------------------------------------------------
print()
print("[3] Why this corpus already had the floor without noticing.")
getcontext().prec = 60
def arctan_inv(m):
    m = D(m); t = D(0); term = 1/m; k = 0
    while True:
        add = term / (2*k+1)
        if add == 0: break
        t += add if k % 2 == 0 else -add
        term /= m*m; k += 1
    return t
PI = 16*arctan_inv(5) - 4*arctan_inv(239)

# A fixed threshold was tried first (1e-5) and failed at d = 43, where the gap
# is 2.2e-4. That threshold was a guess. What is actually true, and is the
# interesting statement, is that the gap SHRINKS with d across the class-number-
# one list -- the larger the discriminant, the better the integer approximation.
gaps = []
for d in (43, 67, 163):
    val = (PI * D(d).sqrt()).exp()
    frac = val - int(val)
    gap = min(frac, 1 - frac)
    gaps.append(gap)
    print("    e^(pi sqrt %3d) = %s" % (d, str(val)[:34]))
    print("                      distance to nearest integer  %.3e" % float(gap))
check("each of the three is within 1e-3 of an integer",
      all(g < D("1e-3") for g in gaps), "worst %.3e" % float(max(gaps)))
check("the approximation improves strictly with d: 43 > 67 > 163",
      gaps[0] > gaps[1] > gaps[2],
      "%.1e > %.1e > %.1e" % tuple(float(g) for g in gaps))
check("at d = 163 the gap is under 1e-12", gaps[2] < D("1e-12"),
      "%.3e" % float(gaps[2]))
print()
print("    That is class number one doing the work: h = 1 makes the singular")
print("    modulus rational, the j-invariant an integer, and e^(pi sqrt d) an")
print("    integer to many places. It is the SAME class-group arithmetic that")
print("    governs the Ramanujan-Weber class invariants G_n verified three days")
print("    ago in book7/ch-ramanujan-verify.py. Ramanujan tabulated units in")
print("    these fields by hand. Volume XI's floor is the group those units")
print("    live in, and the corpus has been standing on it since Vol VII.")

print()
if FAIL:
    print("FAILED: " + "; ".join(FAIL)); raise SystemExit(1)
print("All checks passed.")
print()
print("Recorded for WP-82: the admissibility verdict for Volume XI should be")
print("restated. Not 'no core is possible' but 'the core needs a definition of")
print("K_0 and one structure theorem, on top of arithmetic Mathlib already has")
print("machine-checked'. Whether anyone builds it is a separate question; that")
print("it cannot be built is no longer the reason not to.")
