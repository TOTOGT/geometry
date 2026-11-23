# claim_check: how to rerun

Environment: Python 3 standard library only (written and run with the Python 3 version recorded below). No packages.

    python3 claim_check.py        # reads claims_input.json, writes ledger.json
    python3 negative_control.py   # alters printed numbers, expects the check to fail; prints CONTROL PASS

Expected: ledger.json has eight rows (C1, C2, C3a, C3b, C4, C5, C6, C7); the last line printed by negative_control.py is `CONTROL PASS: the checks fail when the printed numbers are wrong`.

Three separate review outcomes (do not merge them into one PASS):
1. Source fidelity: do the values in claims_input.json match arXiv:1711.05225 v3? Status: Table 1 and Section 4.1 key figures confirmed by one reviewer; the rest unchecked.
2. Computational reproducibility: do the scripts reproduce the ledger and catch the planted alteration? Status: a reviewer ran both scripts in a clean directory (Python 3.13.5): ledger.json matched byte for byte, and negative_control.py printed CONTROL PASS with exit code 0. This covers the two-command workflow and these inputs only.
3. Statistical interpretation: are the bootstrap comparison and its limits described correctly? Status: no statistician has reviewed it.
Python 3.13.18
