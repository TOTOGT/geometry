#!/usr/bin/env bash
# The polar-polygon gate. From anywhere:
#     bash tools/verify-polar/run.sh
#
# Covers the three modules written for the hexagon/decagon question:
# PolarTriadClosure (triad arithmetic), PolarPolygonCommonRefinement (the
# negative result: sixfold AND tenfold together force a constant), and
# ChladniPolygon (the nodal-set statements the SBM page displays).
set -uo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT" || exit 1
PROBE="tools/verify-polar/probe_polar.lean"
OUT="tools/verify-polar/axioms.txt"
# Anchored on purpose. The unanchored grep that verify-book8/run.sh uses also
# matches the probe's own docstring, so N there is inflated by the prose.
N=$(grep -c '^#print axioms' "$PROBE")

command -v lake >/dev/null 2>&1 || {
  echo "lake not found. Install elan first:"
  echo "  curl -sSfL https://raw.githubusercontent.com/leanprover/elan/master/elan-init.sh | sh"
  exit 127; }

echo "toolchain pinned : $(cat lean-toolchain)"
echo

echo "── 1/3  lake build ─────────────────────────────────────────"
lake build PolarTriadClosure PolarPolygonCommonRefinement ChladniPolygon || {
  echo "BUILD FAILED — the Lean does not compile. Nothing below is meaningful."; exit 1; }

echo
echo "── 2/3  kernel axiom probe ($N declarations) ───────────────"
lake env lean "$PROBE" > "$OUT" 2>&1
rc=$?
cat "$OUT"
[ "$rc" -ne 0 ] && { echo; echo "PROBE FAILED TO ELABORATE (exit $rc)."; exit 1; }

echo
echo "── 3/3  axiom gate ─────────────────────────────────────────"
python3 tools/axiom_gate.py "$OUT" "$N"
gate=$?

echo
if [ "$gate" -eq 0 ]; then
  echo "GREEN — $N declarations, every one kernel-checked, no sorryAx."
  echo "        Arithmetic and symmetry only. Nothing here is a claim about Saturn."
else
  echo "RED — the gate refused. Read the report above."
fi
exit $gate
