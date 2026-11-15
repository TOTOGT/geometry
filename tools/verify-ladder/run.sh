#!/usr/bin/env bash
# Compile and axiom-check LadderBound.lean and LadderRung.lean. CI runs this same script (verify-proofs.yml).
#     bash tools/verify-ladder/run.sh [LOGDIR]        default LOGDIR: tools/verify-ladder/logs
# Runs every step even after a failure (so the logs are complete), preserves each exit status in LOGDIR/status.tsv,
# and exits non-zero if any step failed. Needs: elan/lake, Mathlib resolved from the committed lake-manifest.json
# (locally: `lake exe cache get`; in CI the preceding `lake build` step does it).
set -uo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"; cd "$ROOT" || exit 1
OUT="${1:-tools/verify-ladder/logs}"; mkdir -p "$OUT"
command -v lake >/dev/null 2>&1 || { echo "lake not found; install elan first"; exit 127; }
: > "$OUT/status.tsv"; FAIL=0
rec() { printf '%s\t%s\n' "$1" "$2" >> "$OUT/status.tsv"; echo "[$([ "$2" -eq 0 ] && echo ok || echo FAIL)] exit $2  $1"; [ "$2" -eq 0 ] || FAIL=1; }

{ echo "commit: $(git rev-parse HEAD 2>/dev/null)"; echo "toolchain pin: $(cat lean-toolchain)"; lean --version; lake --version
  sha256sum LadderBound.lean LadderRung.lean lakefile.lean lake-manifest.json tools/axiom_gate.py 2>/dev/null || shasum -a 256 LadderBound.lean LadderRung.lean lakefile.lean lake-manifest.json tools/axiom_gate.py; } > "$OUT/environment.txt" 2>&1
cat "$OUT/environment.txt"

python3 tools/verify-ladder/check_pins.py > "$OUT/pins.log" 2>&1; rec "pins (toolchain, manifest, resolved Mathlib)" $?; cat "$OUT/pins.log"

lake build LadderBound LadderRung > "$OUT/lake-build.log" 2>&1; rec "lake build LadderBound LadderRung (targets)" $?; tail -3 "$OUT/lake-build.log"

lake env lean LadderBound.lean > "$OUT/LadderBound.compile.log" 2>&1; rec "lake env lean LadderBound.lean" $?
python3 tools/axiom_gate.py "$OUT/LadderBound.compile.log" 6 > "$OUT/LadderBound.gate.log" 2>&1; rec "axiom gate LadderBound (6 theorems)" $?; cat "$OUT/LadderBound.gate.log"

lake env lean LadderRung.lean > "$OUT/LadderRung.compile.log" 2>&1; rec "lake env lean LadderRung.lean" $?
python3 tools/axiom_gate.py "$OUT/LadderRung.compile.log" 3 > "$OUT/LadderRung.gate.log" 2>&1; rec "axiom gate LadderRung (3 theorems)" $?; cat "$OUT/LadderRung.gate.log"

lake env lean tools/verify-ladder/probe_ladder.lean > "$OUT/probe.log" 2>&1; rec "lake env lean probe_ladder.lean (via the library targets)" $?
python3 tools/axiom_gate.py "$OUT/probe.log" 9 > "$OUT/probe.gate.log" 2>&1; rec "axiom gate probe (9 theorems)" $?; cat "$OUT/probe.gate.log"

echo; if [ "$FAIL" -eq 0 ]; then echo "GREEN: both files compile, 6 + 3 theorems, no sorryAx, axioms within the allowlist, pins match."
else echo "RED: see $OUT/status.tsv and the logs beside it."; fi
exit $FAIL
