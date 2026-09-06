#!/usr/bin/env bash
# The polar-polygon gate. From anywhere:
#     bash tools/verify-polar/run.sh
#
# HARVEST, DO NOT RE-ELABORATE. The three modules carry their own
# `#print axioms` blocks, so `lake build` already emits the audit. On a warm
# tree this is a replay of three targets, not a corpus rebuild. An earlier
# draft of this gate shipped a separate probe file that imported all three and
# re-ran the probe; that meant a second elaboration for a report the build had
# already produced -- and the probe's docstring sat above its `import`, so it
# did not parse. Both problems are gone with the probe.
set -uo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT" || exit 1
OUT="tools/verify-polar/axioms.txt"
MODS="PolarTriadClosure PolarPolygonCommonRefinement ChladniPolygon"

# N is the number of `#print axioms` lines the three modules themselves carry.
# Counted from the sources, so adding a theorem without adding its probe line
# leaves it out of Tier 1 -- under-report, never over-report.
N=0
for m in $MODS; do
  N=$(( N + $(grep -c '^#print axioms' "$m.lean") ))
done

command -v lake >/dev/null 2>&1 || { echo "lake not found (elan not on PATH)."; exit 127; }
echo "toolchain pinned : $(cat lean-toolchain)"
echo
echo "── 1/2  lake build (warm tree = replay) ────────────────────"
BUILD=$(lake build $MODS 2>&1); rc=$?
echo "$BUILD" | grep -E '^(ℹ|info: Build|Build)' | tail -3
[ "$rc" -ne 0 ] && { echo "$BUILD" | tail -20; echo "BUILD FAILED. Nothing below is meaningful."; exit 1; }

# Strip Lean's "file:line:col: " prefix so the file has the same shape as every
# other axioms.txt in the corpus: one `'Name' depends on ...` per line.
echo "$BUILD" | grep -oE "'[^']+' (depends on axioms: \[[^]]*\]|does not depend on any axioms)" > "$OUT"
echo
echo "── 2/2  axiom gate ($N expected) ───────────────────────────"
cat "$OUT"
got=$(wc -l < "$OUT" | tr -d ' ')
bad=$(grep -c sorryAx "$OUT")
echo
if [ "$got" -eq "$N" ] && [ "$bad" -eq 0 ]; then
  echo "GREEN — $got declarations, every one kernel-checked, no sorryAx."
  echo "        Arithmetic and symmetry only. Nothing here is a claim about Saturn."
  exit 0
fi
echo "RED — expected $N declarations, harvested $got, $bad trusting sorryAx."
echo "      A count that moved without a commit saying so is the thing this gate exists to catch."
exit 1
