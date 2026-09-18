#!/bin/sh
# Re-derive the axiom report for Volume XI's floor and gate it.
#
# The header of VolXI_K0_Floor.lean makes a claim about that file's axioms.
# A claim in a header is prose. This makes it a check.
#
#   run from the repo root:  sh book6/lean/VolXI_K0_Floor-verify.sh
#
# Exit 0 iff the file elaborates AND the one theorem it exports depends only on
# [propext, Classical.choice, Quot.sound] -- in particular, not on sorryAx.
#
# Classical.choice is PERMITTED here and the reason is specific, not a shrug:
# the proof ends in `AddLocalization.addEquivOfQuotient`, which is noncomputable,
# over a localization, which is a quotient. The choice is Mathlib's construction,
# not this argument's. If that stops being true the allowlist should shrink, not
# the claim.
#
# LIMITS OF THIS CHECK.
#   - It pins nothing about WHICH Mathlib. The pinned checkout is 81a5d257c8 on
#     toolchain v4.32.0 and lake resolves that from lake-manifest.json; this
#     script trusts that resolution and does not verify it.
#   - It checks one declaration. The file's other declarations are `example`s
#     and carry no names, so `#print axioms` cannot reach them; they are covered
#     only by the file elaborating at all.
#   - It does not check that the theorem says what the prose says it says.

set -e
EXPECTED="book6/lean/VolXI_K0_Floor.axioms.txt"
ACTUAL="$(mktemp)"
trap 'rm -f "$ACTUAL"' EXIT

lake env lean book6/lean/VolXI_K0_Floor.lean > "$ACTUAL" 2>&1

if ! diff -u "$EXPECTED" "$ACTUAL"; then
  echo "FAIL: axiom report differs from the recorded one."
  echo "      Any error or warning line also lands here -- the file must be silent"
  echo "      apart from its one #print axioms line."
  exit 1
fi

echo "OK: VolXI_K0_Floor.lean elaborates silently and its axiom report is unchanged."
echo "    [propext, Classical.choice, Quot.sound] -- no sorryAx."
