#!/usr/bin/env bash
# disk-survey.sh — where the disk actually went.
#
#   bash ~/Desktop/geometry/tools/disk-survey.sh
#
# Claude can only see ~/Desktop, ~/geometry and ~/Desktop/DECS through the
# desktop bridge. Those are ~12 GB of a ~204 GB used disk. This runs where
# you are and shows the rest.

echo "=== volume ==="
df -h / | tail -1 | awk '{printf "  %s used of %s, %s free (%s)\n",$3,$2,$4,$5}'

echo
echo "=== home, top level, over 1 GB ==="
du -sh ~/* ~/.[!.]* 2>/dev/null | grep -E '^\s*[0-9.]+G' | sort -rh | head -25

echo
echo "=== regenerable build artefacts (safe to delete, never archive) ==="
for pat in .lake node_modules __pycache__ .venv venv .next dist build target .gradle; do
  found=$(find ~ -maxdepth 5 -name "$pat" -type d -not -path '*/.Trash/*' 2>/dev/null)
  [ -z "$found" ] && continue
  n=$(echo "$found" | wc -l | tr -d ' ')
  sz=$(echo "$found" | tr '\n' '\0' | xargs -0 du -sk 2>/dev/null | awk '{s+=$1} END{printf "%.1f", s/1048576}')
  printf "  %-14s %3s dir(s)  %6s GB\n" "$pat" "$n" "$sz"
done

echo
echo "=== Lean toolchains in ~/.elan (each 1.5-2.5 GB) ==="
if [ -d ~/.elan/toolchains ]; then
  du -sh ~/.elan/toolchains/* 2>/dev/null | sort -rh
  echo
  echo "  toolchains still declared by a project on this machine:"
  find ~ -maxdepth 4 -name lean-toolchain -not -path '*/.lake/*' -not -path '*/.Trash/*' 2>/dev/null \
    | xargs cat 2>/dev/null | sort -u | sed 's/^/    /'
  echo
  echo "  anything listed above but NOT declared below is orphaned:"
  echo "    elan toolchain uninstall <name>"
else
  echo "  (no ~/.elan)"
fi

echo
echo "=== caches worth knowing about ==="
for d in ~/Library/Caches ~/Library/Developer ~/Library/Application\ Support/Code ~/.npm ~/.cache; do
  [ -d "$d" ] && printf "  %-42s %s\n" "${d/#$HOME/~}" "$(du -sh "$d" 2>/dev/null | cut -f1)"
done
