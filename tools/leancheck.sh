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

# Resolve every argument to an absolute path BEFORE cd-ing into the project.
# This used to happen inside the loop, AFTER `cd "$PROJ"`, so a relative
# argument resolved against ~/Desktop/geometry instead of the caller's
# directory. On 2026-08-30 that turned a 252-file run into 252 identical
# "cd: 3M: No such file or directory" errors, reported in the summary as
# "0 ok, 252 failed" — a path bug wearing the costume of a mathematical one.
# Unresolvable paths are now counted separately and can never be read as
# compile failures again.
FILES=(); skip=0
for _a in "$@"; do
  case "$_a" in
    /*) FILES+=("$_a") ;;
    *)  _d=$(cd "$(dirname "$_a")" 2>/dev/null && pwd) || _d=""
        if [ -n "$_d" ]; then FILES+=("$_d/$(basename "$_a")")
        else echo "  SKIP        $_a  (no such path, from $(pwd))"; skip=$((skip+1)); fi ;;
  esac
done
for _f in ${FILES[@]+"${FILES[@]}"}; do
  [ -f "$_f" ] || { echo "  SKIP        $_f  (not a file)"; skip=$((skip+1)); }
done
FILES=($(for _f in ${FILES[@]+"${FILES[@]}"}; do [ -f "$_f" ] && printf '%s\n' "$_f"; done))
[ ${#FILES[@]} -eq 0 ] && { echo; echo "  0 ok, 0 failed, $skip skipped — nothing resolved, check the paths"; exit 1; }

cd "$PROJ" || { echo "no $PROJ"; exit 1; }
echo "project:   $PROJ  ($(cat lean-toolchain))"
echo "mathlib:   $(cat .lake/packages/mathlib/lean-toolchain)"
echo

pass=0; fail=0
for f in "${FILES[@]}"; do
  s=$(date +%s)
  out=$(lake env lean "$f" 2>&1); rc=$?
  e=$(date +%s)
  n=$(printf '%s' "$out" | grep -c 'error')
  if [ "$n" -eq 0 ] && [ $rc -eq 0 ]; then
    printf "  OK    %4ds  %s\n" $((e-s)) "$(basename "$f")"; pass=$((pass+1))
  else
    if [ "$n" -eq 0 ]; then
      # rc != 0 with no error lines means the toolchain never ran (missing lake,
      # wrong toolchain), not that the file is broken. Say so, or the next reader
      # counts it as a mathematical failure the way the 2026-08-30 log invited.
      printf "  FAIL  %4ds  %s  (toolchain did not run — rc=%d, no error output)\n" $((e-s)) "$(basename "$f")" "$rc"
    else
      printf "  FAIL  %4ds  %s  (%d errors)\n" $((e-s)) "$(basename "$f")" "$n"
    fi
    fail=$((fail+1))
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
if [ "$skip" -gt 0 ]; then
  echo "  $pass ok, $fail failed, $skip skipped (path did not resolve — not a compile result)"
else
  echo "  $pass ok, $fail failed"
fi
