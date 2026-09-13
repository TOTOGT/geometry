#!/usr/bin/env bash
# clear-stale-lock.sh — remove a stale .git/index.lock, and refuse to remove a live one.
#
#   bash tools/clear-stale-lock.sh                    # the repos below
#   bash tools/clear-stale-lock.sh ~/Desktop/AXLE     # or named ones
#   bash tools/clear-stale-lock.sh --check            # report only, remove nothing
#
# WHY THIS EXISTS. Git takes .git/index.lock before writing the index and removes
# it afterwards. If the process dies in between -- a crash, a killed terminal, a
# sandbox that can create the file but not unlink it -- the lock outlives its
# owner, and from then on every `git add` and `git commit` in that repository
# fails. The failure is loud at the moment you hit it and silent in aggregate:
# nothing tells you that work has stopped reaching the history, so it accumulates.
#
# Measured twice:
#   AXLE      lock from 2026-09-09 00:15:48, found 2026-09-13. Four days of
#             commits did not happen; three journal files sat staged-in-intent
#             and untracked in fact.
#   geometry  lock from 2026-09-13 04:41, found the same day at 14:39. Five
#             changesets were blocked behind a zero-byte file.
#
# THE ONE RULE. A lock with a live git process behind it is NOT stale, and
# removing it can corrupt the index of a running operation. This script checks
# for that process first and exits rather than guess. That check is the only
# reason this file exists instead of `rm -f`.

set -u
CHECK=0
REPOS=()
for a in "$@"; do
  case "$a" in
    --check) CHECK=1 ;;
    *) REPOS+=("$a") ;;
  esac
done
[ ${#REPOS[@]} -eq 0 ] && REPOS=("$HOME/Desktop/geometry" "$HOME/Desktop/AXLE" "$HOME/Desktop/dnls" "$HOME/geometry")

# A live git process anywhere on this machine is enough to stop us. The lock
# names no owner, so we cannot tell which repository a running git belongs to,
# and the conservative reading is the only safe one.
live=$(pgrep -a git 2>/dev/null | grep -v 'clear-stale-lock' || true)
if [ -n "$live" ]; then
  echo "A git process is running. Not touching any lock."
  printf '%s\n' "$live" | sed 's/^/  /'
  exit 1
fi

found=0; cleared=0
for r in "${REPOS[@]}"; do
  lock="$r/.git/index.lock"
  [ -e "$lock" ] || continue
  found=$((found+1))
  age=$(( ( $(date +%s) - $(stat -f %m "$lock" 2>/dev/null || stat -c %Y "$lock") ) / 60 ))
  size=$(stat -f %z "$lock" 2>/dev/null || stat -c %s "$lock")
  printf '%s\n  lock present: %s bytes, %s minutes old\n' "$r" "$size" "$age"
  if [ "$CHECK" -eq 1 ]; then
    echo "  --check: left in place"
    continue
  fi
  if rm -f "$lock"; then
    echo "  removed"; cleared=$((cleared+1))
    ( cd "$r" && git status -sb 2>&1 | head -1 | sed 's/^/  /' )
  else
    echo "  COULD NOT REMOVE -- the filesystem refused the unlink, not git."
    echo "  A sandboxed session without delete rights will see exactly this."
  fi
done

if [ "$found" -eq 0 ]; then
  echo "No stale locks in: ${REPOS[*]}"
else
  echo
  echo "  $found found, $cleared cleared"
fi
