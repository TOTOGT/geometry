#!/usr/bin/env python3
"""Fixtures for tools/terms.py. Run: python3 tools/test_terms.py

The vocabulary guard decides whether the corpus has absorbed a term that was
never its own, so the guard itself is checked here. Case 2 is CI run #247: the
corpus mentioning a disowned term in its own audit record, which the first form
of the checker read as a first use and failed the job on.
"""

import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
TERMS = os.path.join(HERE, 'terms.py')

REGISTRY = """\
# TERMS.md

- Structural Coherence Index (SCI)

---

## Disowned

- Harmonic Resonance Bands (HRB) @ CLAUDE.md
"""

MENTION = ("A Google AI Overview attributed \"Harmonic Resonance Bands (HRB)\""
           " to this corpus; the term occurs nowhere in it.\n")
USE = "<html><body><p>The lattice organises into Harmonic Resonance Bands (HRB).</p></body></html>\n"
DECLARED_USE = "Depth raises the Structural Coherence Index (SCI) throughout.\n"
NEW_COINAGE = "We define the Recursive Balance Field (RBF) as follows.\n"

# Every case carries a use of the declared term, so that a case testing
# something else does not also trip the STALE check and pass for the wrong
# reason.
CASES = [
    ("declared term used",              {},                              0, 'OK:'),
    ("disowned, mentioned where permitted (run #247)",
                                        {'CLAUDE.md': MENTION},          0, 'OK:'),
    ("disowned, absorbed into a chapter",
                                        {'CLAUDE.md': MENTION,
                                         'ch.html': USE},                1, 'DISOWNED TERM IN USE'),
    ("undeclared new coinage",          {'two.md': NEW_COINAGE},         1, 'UNDECLARED'),
    ("declared term vanished",          {'ch.md': 'nothing here\n'},     1, 'STALE'),
]


def run_case(files, keep_declared=True):
    d = tempfile.mkdtemp()
    try:
        with open(os.path.join(d, 'TERMS.md'), 'w', encoding='utf-8') as fh:
            fh.write(REGISTRY)
        if keep_declared and 'ch.md' not in files:
            with open(os.path.join(d, 'declared.md'), 'w', encoding='utf-8') as fh:
                fh.write(DECLARED_USE)
        for name, body in files.items():
            with open(os.path.join(d, name), 'w', encoding='utf-8') as fh:
                fh.write(body)
        p = subprocess.run([sys.executable, TERMS, '--check'], cwd=d,
                           capture_output=True, text=True)
        return p.returncode, p.stdout + p.stderr
    finally:
        shutil.rmtree(d)


def main():
    failures = 0
    for name, files, want_exit, needle in CASES:
        rc, out = run_case(files)
        ok = (rc == want_exit) and (needle in out)
        print("%-48s %s" % (name, "PASS" if ok else "FAIL"))
        if not ok:
            failures += 1
            print("   wanted exit %d and %r; got exit %d:" % (want_exit, needle, rc))
            for line in out.splitlines():
                print("   | " + line)
    print("\n%d/%d cases pass" % (len(CASES) - failures, len(CASES)))
    return 1 if failures else 0


if __name__ == '__main__':
    sys.exit(main())
