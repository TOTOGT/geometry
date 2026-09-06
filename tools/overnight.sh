#!/usr/bin/env bash
# overnight.sh — the run order in CLAUDE.md, as something that runs.
#
#   bash tools/overnight.sh            # the whole corpus, priority order
#   bash tools/overnight.sh --dry-run  # print the order and stop
#
# WHY THIS EXISTS. "The overnight job" was a prose section in CLAUDE.md
# addressed to whichever session had the machine. Nothing scheduled it, nothing
# recorded whether it had run, and the last attempt left
# ~/Desktop/leanaudit-2026-09-01.log at zero bytes. A run order a human has to
# re-read and re-type each night is not a job.
#
# This is a DRIVER, not a checker. Every verdict here is tools/leancheck.sh's,
# whose verdict is in turn tools/axiom_gate.py's. Nothing new judges anything.
#
# WHAT IT LEAVES BEHIND, which is the point:
#   tools/verify-audit/<date>/<stem>.axioms.txt   one gate report per file
#   tools/verify-audit/<date>/run.log             the full transcript
#   tools/verify-audit/<date>/order.txt           what it tried, in order
# Those are the shape tools/toolchain_ledger.py and the theorem registry read,
# so the morning after a run the ledger reflects it without anyone typing.
#
# PRIORITY ORDER, from the 2026-08-30 handoff, highest value first:
#   1. files with no `import` line — most have never been elaborated by
#      anything. NOT ALL: PolarTriadClosure and PolarPolygonCommonRefinement
#      import nothing because they need nothing, and both compile. Zero-import
#      is a heuristic for "never checked", not a proof of it.
#   2. files containing `sorry` — triage before proving; the handoff records
#      three GTCT theorems and three AXLE axioms that were FALSE, not merely
#      unproved.
#   3. everything else tracked.
#
# DO NOT run `lake exe cache get`. Six sessions did, and left 30 GB of
# duplicate builds. Mathlib v4.32.0 is already at .lake.
set -uo pipefail
PROJ=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
DATE=$(date +%F)
OUT="$PROJ/tools/verify-audit/$DATE"
DRY=0
[ "${1:-}" = "--dry-run" ] && DRY=1
mkdir -p "$OUT"

# Roots are declared, never discovered — tools/corpus_roots.txt, the same file
# leanscan.sh, the registry and the ledger read. A root that cannot be read is
# reported, not skipped: a run over five roots of eleven is a different
# measurement, not a smaller one.
#
# BASH 3.2. macOS ships bash 3.2.57 as /bin/bash and has since 2007, for
# licensing reasons that are not going to change. `mapfile`/`readarray` is
# bash 4, so the first version of this line died on the machine it was written
# for with "mapfile: command not found" — and then, under `set -u`, took the
# whole run down with "ROOTS[@]: unbound variable". Anything written here has
# to run under 3.2 or it does not run at all.
ROOTS=()
while IFS= read -r _line; do
  [ -n "$_line" ] && ROOTS+=("$_line")
done < <(sed 's/#.*//' "$PROJ/tools/corpus_roots.txt" | sed 's/[[:space:]]*$//' | grep .)
[ ${#ROOTS[@]} -eq 0 ] && { echo "no roots in tools/corpus_roots.txt — nothing to run"; exit 1; }

: > "$OUT/order.txt"
for r in ${ROOTS[@]+"${ROOTS[@]}"}; do
  d="${r/#\~/$HOME}"
  [ -d "$d/.git" ] || { echo "UNREADABLE ROOT: $d" | tee -a "$OUT/order.txt"; continue; }
  ( cd "$d" && git ls-files '*.lean' ) | while read -r f; do
      p="$d/$f"; [ -f "$p" ] || continue
      body=$(sed 's|--.*||' "$p")
      if ! grep -qE '^[[:space:]]*import[[:space:]]' "$p"; then pri=1
      elif printf '%s' "$body" | grep -qw sorry;            then pri=2
      else                                                       pri=3; fi
      printf '%d\t%s\n' "$pri" "$p"
    done >> "$OUT/order.txt"
done
sort -s -k1,1n "$OUT/order.txt" -o "$OUT/order.txt"

n=$(grep -c $'^[0-9]\t' "$OUT/order.txt")
echo "corpus: $n tracked .lean files across ${#ROOTS[@]} declared roots"
echo "shell: bash ${BASH_VERSION:-unknown}"
for p in 1 2 3; do
  printf "  priority %d: %d files\n" "$p" "$(grep -c "^$p"$'\t' "$OUT/order.txt")"
done
echo "reports → tools/verify-audit/$DATE/"
[ "$DRY" -eq 1 ] && { echo; echo "--dry-run: nothing compiled."; exit 0; }

echo
i=0
grep $'^[0-9]\t' "$OUT/order.txt" | cut -f2 | while read -r f; do
  i=$((i+1))
  rep="$OUT/$(basename "${f%.lean}").axioms.txt"
  # Resumable on purpose. An overnight run gets interrupted — a closed lid, a
  # full disk — and re-running from the top would spend the night redoing the
  # cheap files it already did.
  [ -s "$rep" ] && { printf "[%4d/%4d] skip (done today) %s\n" "$i" "$n" "$f"; continue; }
  printf "[%4d/%4d] %s\n" "$i" "$n" "$f"
  bash "$PROJ/tools/leancheck.sh" --out "$OUT" --audit "$f" 2>&1
done | tee -a "$OUT/run.log"

echo | tee -a "$OUT/run.log"
echo "== summary ==" | tee -a "$OUT/run.log"
# Counted with find, not with a glob piped to xargs. On an empty directory a
# glob stays literal and `xargs grep -l` runs grep with no file arguments,
# which reads stdin -- a summary line that can hang is worse than no summary.
nrep=$(find "$OUT" -name '*.axioms.txt' 2>/dev/null | wc -l | tr -d ' ')
nbad=$(find "$OUT" -name '*.gate' -exec grep -l '::error::' {} + 2>/dev/null | wc -l | tr -d ' ')
printf "  reports written : %s\n" "$nrep" | tee -a "$OUT/run.log"
printf "  gate refusals   : %s\n" "$nbad" | tee -a "$OUT/run.log"
echo | tee -a "$OUT/run.log"
echo "next: python3 tools/toolchain_ledger.py --write" | tee -a "$OUT/run.log"
