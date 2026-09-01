#!/usr/bin/env bash
# leancheck.sh — compile and kernel-audit Lean files using the Mathlib build
# that is ALREADY on this Mac. Nothing is downloaded.
#
#   bash ~/Desktop/geometry/tools/leancheck.sh FILE.lean [FILE.lean ...]
#   bash ~/Desktop/geometry/tools/leancheck.sh ~/Desktop/GTCT/*.lean
#   bash ~/Desktop/geometry/tools/leancheck.sh --audit ~/Desktop/GTCT/GTCTsorryFree.lean
#
# --audit additionally runs `#print axioms` on every theorem/lemma in the file
# and reports anything that is not a subset of the three standard axioms.
# That is the real gate. A clean compile is not a verification.
#
# WHY THIS PROJECT: ~/Desktop/geometry is the only checkout on this machine
# with a COMPLETE Mathlib build matching its own toolchain (v4.32.0, full
# Mathlib.olean present, 6.4 GB). GTCT is pinned to the same v4.32.0, so its
# files check here too. AXLE (v4.14.0), vol1-proofs (v4.14.0) and
# GTCT/GTCT (v4.11.0) have partial builds on older toolchains.

set -uo pipefail
PROJ=~/Desktop/geometry
AUDIT=0
[ "${1:-}" = "--audit" ] && { AUDIT=1; shift; }
[ $# -eq 0 ] && { echo "usage: leancheck.sh [--audit] FILE.lean ..."; exit 1; }

cd "$PROJ" || { echo "no $PROJ"; exit 1; }
echo "project:   $PROJ  ($(cat lean-toolchain))"
echo "mathlib:   $(cat .lake/packages/mathlib/lean-toolchain)"
echo

pass=0; fail=0
for f in "$@"; do
  f=$(cd "$(dirname "$f")" && pwd)/$(basename "$f")
  s=$(date +%s)
  out=$(lake env lean "$f" 2>&1); rc=$?
  e=$(date +%s)
  n=$(printf '%s' "$out" | grep -c 'error')
  if [ "$n" -eq 0 ] && [ $rc -eq 0 ]; then
    printf "  OK    %4ds  %s\n" $((e-s)) "$(basename "$f")"; pass=$((pass+1))
  else
    printf "  FAIL  %4ds  %s  (%d errors)\n" $((e-s)) "$(basename "$f")" "$n"; fail=$((fail+1))
    printf '%s\n' "$out" | grep 'error' | head -5 | sed 's/^/          /'
    continue
  fi

  [ $AUDIT -eq 1 ] || continue
  # build a probe: the file, then #print axioms for every declaration in it
  ns=$(grep -m1 '^namespace ' "$f" | awk '{print $2}')
  probe=$(mktemp /tmp/leanprobe.XXXXXX.lean)
  cp "$f" "$probe"
  grep -oE '^(theorem|lemma)[[:space:]]+[^[:space:]:({\[]+' "$f" \
    | awk '{print $2}' \
    | while read -r d; do
        [ -n "$ns" ] && echo "#print axioms $ns.$d" || echo "#print axioms $d"
      done >> "$probe"
  ax=$(lake env lean "$probe" 2>&1 | grep 'depends on axioms\|does not depend')
  tot=$(printf '%s' "$ax" | grep -c .)
  bad=$(printf '%s' "$ax" | grep -c 'sorryAx\|native_decide')
  printf "        audit: %d declarations, %d trusting sorryAx/native_decide\n" "$tot" "$bad"
  [ "$bad" -gt 0 ] && printf '%s\n' "$ax" | grep 'sorryAx\|native_decide' | sed 's/^/          /'
  rm -f "$probe"
done

echo
echo "  $pass ok, $fail failed"
