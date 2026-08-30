#!/usr/bin/env bash
# lean-disk.sh — find every Mathlib build on this Mac, and reclaim the dead ones.
#
#   bash ~/Desktop/geometry/tools/lean-disk.sh          # report only (default)
#   bash ~/Desktop/geometry/tools/lean-disk.sh --yes    # actually delete
#
# Deletes ONLY .lake build directories. Never touches a .lean source, a repo,
# or anything under git. Every .lake here is regenerable with `lake exe cache get`.

KEEP=~/Desktop/geometry          # the one complete, matched, current build
DROP=(
  ~/geometry                     # stale duplicate checkout; complete v4.32.0 build
  ~/Desktop/orthogenesis         # v4.33.0-rc1; its 10 sources are byte-identical to geometry's
  ~/Desktop/vol1-proofs          # v4.14.0, partial, no Mathlib.olean
  ~/Desktop/AXLE                 # v4.14.0, partial, no Mathlib.olean
  ~/Desktop/GTCT/GTCT            # v4.11.0, partial, tarball extract
)

echo "=== Mathlib builds on this Mac ==="
tot=0
for d in "$KEEP" "${DROP[@]}"; do
  p="$d/.lake"
  [ -d "$p" ] || continue
  sz=$(du -sk "$p" 2>/dev/null | cut -f1)
  tc=$(cat "$d/lean-toolchain" 2>/dev/null || echo '?')
  full=$([ -f "$p/packages/mathlib/.lake/build/lib/lean/Mathlib.olean" ] && echo complete || echo partial)
  mark=$([ "$d" = "$KEEP" ] && echo "KEEP" || echo "drop")
  printf "  %-4s %-32s %-28s %-8s %6.1f GB\n" "$mark" "${d/#$HOME/~}" "$tc" "$full" "$(echo "$sz/1048576"|bc -l)"
  [ "$d" != "$KEEP" ] && tot=$((tot+sz))
done
printf "\n  reclaimable: %.1f GB\n" "$(echo "$tot/1048576"|bc -l)"
echo "  free now:    $(df -h ~ | tail -1 | awk '{print $4}')"

if [ "${1:-}" != "--yes" ]; then
  echo
  echo "  Report only. Re-run with --yes to delete the five 'drop' trees."
  echo "  Nothing but .lake directories will be removed."
  exit 0
fi

echo
for d in "${DROP[@]}"; do
  [ -d "$d/.lake" ] || continue
  echo "  removing $d/.lake"
  rm -rf "$d/.lake"
done
echo
echo "  free now: $(df -h ~ | tail -1 | awk '{print $4}')"
echo
echo "  To rebuild any of them later, in that repo:  lake exe cache get"
echo "  Note: ~/Desktop/orthogenesis/JacobianCounterexample.lean is the one"
echo "  source there with no copy in geometry. Its .lake goes; the file stays."
