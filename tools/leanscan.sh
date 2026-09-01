#!/usr/bin/env bash
# leanscan.sh — the instrument behind docs/leanscan-<date>.md
#
#   bash ~/Desktop/geometry/tools/leanscan.sh
#
# Prints two things and computes nothing else:
#   1. the root set, with each repo's lean-toolchain and whether it matches the
#      reference build
#   2. priority 1 — tracked .lean files with zero `import` lines, which have
#      therefore never been elaborated against any environment
#
# THE ROOT SET IS NOT DISCOVERED, IT IS DECLARED. It comes from
# tools/corpus_roots.txt and from nowhere else. A first draft of this tool globbed
# ~/Desktop for directories containing .git and de-duplicated by remote, keeping
# whichever checkout came first. Shell glob order put `geometry-backup-jul5/` ahead
# of `geometry/`, so the backup was counted as canonical and the live repo was
# reported as its duplicate — the exact double-count that corpus_roots.txt exists to
# prevent, reproduced by the tool written to measure it. Roots change by editing that
# file, which is the one place a change to a published total is visible.
#
# A root that cannot be read is REPORTED, never skipped silently: a total computed
# over five of eleven roots is not a smaller total, it is a different measurement.
#
# This tool does NOT compile anything. Compiling is tools/leancheck.sh, and the gate
# there is `#print axioms`, not a clean build.

set -uo pipefail
HERE=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
ROOTS_FILE=${LEANSCAN_ROOTS:-$HERE/corpus_roots.txt}
REF=${LEANSCAN_REF:-$HOME/Desktop/geometry}
# LEANSCAN_PREFIX rewrites the ~ in corpus_roots.txt; used when the folders are
# mounted somewhere other than the home directory. Empty means "use $HOME".
PREFIX=${LEANSCAN_PREFIX:-$HOME}

[ -f "$ROOTS_FILE" ] || { echo "no roots file: $ROOTS_FILE"; exit 1; }
ref_tc=$(cat "$REF/lean-toolchain" 2>/dev/null || echo "unknown")
echo "roots:           $ROOTS_FILE"
echo "reference build: $REF ($ref_tc)"
echo "measured:        $(date +%F)"
echo

roots=$(sed 's/#.*//' "$ROOTS_FILE" | sed 's/[[:space:]]*$//' | grep -v '^$')

printf "%-34s %6s  %-26s %s\n" ROOT LEAN TOOLCHAIN "CHECKABLE vs $ref_tc"
printf "%-34s %6s  %-26s %s\n" ---- ---- --------- ---------
total=0; unreachable=0; reachable=""
while read -r r; do
  p=${r/#\~/$PREFIX}
  if [ ! -d "$p/.git" ]; then
    printf "%-34s %6s  %-26s %s\n" "$r" "-" "UNREACHABLE" "not read — see note below"
    unreachable=$((unreachable+1)); continue
  fi
  n=$( (cd "$p" && git ls-files '*.lean' 2>/dev/null | wc -l | tr -d ' ') )
  tc=$(cat "$p/lean-toolchain" 2>/dev/null || echo "none")
  if [ "$tc" = "$ref_tc" ]; then ck="yes"; else ck="no"; fi
  [ "$n" = "0" ] && ck="—"
  printf "%-34s %6s  %-26s %s\n" "$r" "$n" "$tc" "$ck"
  total=$((total+n)); reachable="$reachable $p"
done <<< "$roots"
echo "  tracked .lean over the roots that were read: $total"
[ "$unreachable" -gt 0 ] && echo "  $unreachable root(s) UNREACHABLE — this total is not the corpus total"
echo

echo "priority 1 — tracked .lean with zero import lines:"
: > /tmp/leanscan-noimports.txt
for p in $reachable; do
  base=$(basename "$p")
  (cd "$p" && git ls-files '*.lean' 2>/dev/null) | while read -r f; do
    [ -f "$p/$f" ] || continue
    [ "$(grep -c '^import ' "$p/$f")" -eq 0 ] && echo "$base/$f" >> /tmp/leanscan-noimports.txt
  done
done
sort -o /tmp/leanscan-noimports.txt /tmp/leanscan-noimports.txt
sed 's/^/  /' /tmp/leanscan-noimports.txt
echo "  total: $(wc -l < /tmp/leanscan-noimports.txt | tr -d ' ')   (also at /tmp/leanscan-noimports.txt)"
echo

echo "checkable subset — pass these to leancheck.sh --audit:"
for p in $reachable; do
  tc=$(cat "$p/lean-toolchain" 2>/dev/null || echo "none")
  [ "$tc" = "$ref_tc" ] || continue
  grep "^$(basename "$p")/" /tmp/leanscan-noimports.txt | sed 's/^/    /'
done
