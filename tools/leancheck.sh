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
# --audit NOW LEAVES AN ARTEFACT. Until 2026-09-05 the probe was written to a
# mktemp file, read for two counts, and `rm -f`d. So an overnight run over the
# whole corpus printed its results to a terminal and left nothing behind: the
# next morning the repository could not tell a file that had been audited from
# one that never had. That is the same shape as the July defect this repo
# exists to prevent -- a verification that happened and left no evidence is
# indistinguishable from one that did not happen. Reports now land in
#
#     tools/verify-audit/<YYYY-MM-DD>/<stem>.axioms.txt
#
# which is a gate-report shape tools/toolchain_ledger.py and the theorem
# registry already read, so an overnight run raises Tier 1 by construction.
# Override the directory with --out DIR.
#
# THE VERDICT IS tools/axiom_gate.py's. This script used to judge with
# `grep -c 'sorryAx\|native_decide'`. That is a forbidden list, and WP-73 §6
# gives the two ways a forbidden list is wrong: it cannot see an axiom nobody
# has thought of yet (Lean.ofReduceBool leaks straight through the name
# `native_decide`), and a checker counting only the `depends on axioms:` form
# is blind to `does not depend on any axioms`, which is the strongest result
# #print axioms can give. The gate enumerates the permitted three and reads
# both forms.
#
# WHY THIS PROJECT: ~/Desktop/geometry is the only checkout on this machine
# with a COMPLETE Mathlib build matching its own toolchain (v4.32.0, full
# Mathlib.olean present, 6.4 GB). GTCT is pinned to the same v4.32.0, so its
# files check here too. AXLE (v4.14.0), vol1-proofs (v4.14.0) and
# GTCT/GTCT (v4.11.0) have partial builds on older toolchains.

set -uo pipefail
PROJ=~/Desktop/geometry
AUDIT=0
FULL=0
OUTDIR=""
# Flags in any order, and repeated flags are harmless. The fixed-position form
# this replaced silently ignored --full when it followed --audit.
while [ $# -gt 0 ]; do
  case "${1:-}" in
    --audit) AUDIT=1; shift ;;
    --full)  FULL=1;  shift ;;
    --out)   OUTDIR="${2:-}"; shift 2 ;;
    *) break ;;
  esac
done
[ -z "$OUTDIR" ] && OUTDIR="$PROJ/tools/verify-audit/$(date +%F)"
[ $AUDIT -eq 1 ] && mkdir -p "$OUTDIR"
[ $# -eq 0 ] && { echo "usage: leancheck.sh [--audit] [--full] [--out DIR] FILE.lean ..."; exit 1; }

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
    # An error line is a LABEL; the part a reader can act on is underneath it.
    # `unsolved goals` prints the remaining goal on the following lines and
    # `type mismatch` prints both terms, and the previous form here --
    # `grep 'error' | head -5` -- kept only the lines carrying the word and
    # discarded every one of them. Measured 2026-09-08: two runs were spent
    # re-deriving a goal state the toolchain had already printed and this
    # script had already thrown away. An instrument must not discard its own
    # measurement. `--full` prints the untouched output.
    if [ $FULL -eq 1 ]; then
      printf '%s\n' "$out" | sed 's/^/          /'
    else
      printf '%s\n' "$out" | grep -A 14 -E 'error' | head -70 | sed 's/^/          /'
    fi
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
  rep="$OUTDIR/$(basename "${f%.lean}").axioms.txt"
  # Keep the wrapped continuation lines: axiom_gate.py rejoins them, and a
  # line-oriented grep here would truncate a long list exactly as CI run #245 did.
  lake env lean "$probe" 2>&1 | grep -E "^'|^ +[A-Za-z]" > "$rep"
  tot=$(grep -cE "^'" "$rep")
  if python3 "$PROJ/tools/axiom_gate.py" "$rep" "$tot" > "$rep.gate" 2>&1; then
    printf "        audit: %d declarations, all within the permitted three\n" "$tot"
  else
    printf "        audit: %d declarations — GATE REFUSED\n" "$tot"
    sed 's/^/          /' "$rep.gate"
  fi
  printf "        report: %s\n" "${rep#$PROJ/}"
  rm -f "$probe"
done

echo
if [ "$skip" -gt 0 ]; then
  echo "  $pass ok, $fail failed, $skip skipped (path did not resolve — not a compile result)"
else
  echo "  $pass ok, $fail failed"
fi
