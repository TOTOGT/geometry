#!/usr/bin/env bash
# Run the same check CI runs, locally. From anywhere:
#     bash tools/verify-book8/run.sh
set -uo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT" || exit 1
PROBE="tools/verify-book8/probe_book8.lean"
OUT="tools/verify-book8/axioms.txt"
N=4                                    # theorems named in the probe
                                       # counted by: grep -c '#print axioms' "$PROBE"

command -v lake >/dev/null 2>&1 || {
  echo "lake not found. Install elan first:"
  echo "  curl -sSfL https://raw.githubusercontent.com/leanprover/elan/master/elan-init.sh | sh"
  exit 127; }

echo "toolchain pinned : $(cat lean-toolchain)"
lean --version || true
echo

echo "── 1/3  lake build OrthogonalWitness ───────────────────────"
lake build OrthogonalWitness || {
  echo "BUILD FAILED — the Lean does not compile. Nothing below is meaningful."; exit 1; }

echo
echo "── 2/3  kernel axiom probe ─────────────────────────────────"
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
  echo "GREEN — $N theorems, every one kernel-checked, no sorryAx, axioms within the allowlist."
  echo "        Scalar identities only. The tensor pullback is sympy, not kernel."
else
  echo "RED — the gate refused. Read the report above: either a theorem is admitted"
  echo "      (sorryAx), an axiom is outside the allowlist, or the count moved."
fi
exit $gate
