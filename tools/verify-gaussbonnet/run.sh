#!/usr/bin/env bash
# Local equivalent of the CI gate step. Run from the repo root.
set -u
PROBE=tools/verify-gaussbonnet/probe_gb.lean
set +e
lake env lean "$PROBE" > /tmp/gb.txt 2>&1
rc=$?
set -e
echo "----- discrete Gauss-Bonnet: axiom report -----"
cat /tmp/gb.txt
echo "-----------------------------------------------"
if [ "$rc" -ne 0 ]; then
  echo "probe failed to elaborate (exit $rc)" >&2
  exit 1
fi
python3 tools/axiom_gate.py /tmp/gb.txt 8
