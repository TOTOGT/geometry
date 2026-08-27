#!/usr/bin/env python3
"""probe_consistency.py — the three counts around each kernel probe must agree.

Every tools/verify-*/ directory states its theorem count three times:

    probe_*.lean   the actual '#print axioms' lines        <- the truth
    run.sh         N=<k>, passed to axiom_gate.py          <- what the gate enforces
    README.md      'axioms.txt <k>' and the prose count    <- what a reader is told

The hardcoded N in run.sh is deliberate: deriving it from the probe would let a
theorem be dropped from the probe without failing anything, which is the exact
regression the gate exists to catch. The cost of hardcoding is drift, and drift
is what this script refuses.

    python3 tools/probe_consistency.py            # audit every verify-* dir
    python3 tools/probe_consistency.py --selftest # known-answer cases

Exit 0 clean, 1 drift found, 2 nothing to check (a silent pass on an empty
scan is how a check quietly stops checking).
"""
import os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

N_IN_RUNSH   = re.compile(r'^\s*N=(\d+)', re.M)
GATE_IN_MD   = re.compile(r'axiom_gate\.py\s+axioms\.txt\s+(\d+)')
PRINT_AXIOMS = re.compile(r'^\s*#print\s+axioms\s+\S', re.M)


def count_probe(text):
    """Number of live '#print axioms' lines. Lean line comments start with --."""
    n = 0
    for line in text.splitlines():
        s = line.strip()
        if s.startswith('--'):
            continue
        if re.match(r'#print\s+axioms\s+\S', s):
            n += 1
    return n


def check_dir(d):
    """Return a list of complaint strings for one verify-* directory."""
    out = []
    probes = [f for f in sorted(os.listdir(d)) if f.startswith('probe_') and f.endswith('.lean')]
    if not probes:
        return [f'{os.path.basename(d)}: no probe_*.lean']
    if len(probes) > 1:
        out.append(f'{os.path.basename(d)}: {len(probes)} probe files, expected 1: {probes}')
    probe = os.path.join(d, probes[0])
    truth = count_probe(open(probe, encoding='utf-8').read())
    name = os.path.basename(d)

    if truth == 0:
        out.append(f'{name}: probe names 0 theorems — the gate would pass on nothing')

    run = os.path.join(d, 'run.sh')
    if not os.path.exists(run):
        out.append(f'{name}: no run.sh')
    else:
        m = N_IN_RUNSH.search(open(run, encoding='utf-8').read())
        if not m:
            out.append(f'{name}: run.sh has no N=<k> line')
        elif int(m.group(1)) != truth:
            out.append(f'{name}: run.sh N={m.group(1)} but probe names {truth}')

    md = os.path.join(d, 'README.md')
    if os.path.exists(md):
        txt = open(md, encoding='utf-8').read()
        m = GATE_IN_MD.search(txt)
        if m and int(m.group(1)) != truth:
            out.append(f'{name}: README says gate count {m.group(1)} but probe names {truth}')
    return out


def audit(root=ROOT):
    base = os.path.join(root, 'tools')
    dirs = [os.path.join(base, d) for d in sorted(os.listdir(base))
            if d.startswith('verify-') and os.path.isdir(os.path.join(base, d))]
    problems = []
    for d in dirs:
        problems += check_dir(d)
    return dirs, problems


# --- known-answer tests -----------------------------------------------------
CASES = [
    ("#print axioms A.b\n#print axioms A.c\n", 2, "two plain lines"),
    ("-- #print axioms A.b\n#print axioms A.c\n", 1, "commented-out line does not count"),
    ("", 0, "empty probe counts zero, which the audit then rejects"),
    ("-- naming #print axioms in prose\n", 0, "mention inside a comment is not a probe"),
    ("#print axioms A.b\n\n\n#print axioms A.b\n", 2, "duplicate names still count twice"),
]


def selftest():
    bad = 0
    for text, want, why in CASES:
        got = count_probe(text)
        ok = got == want
        bad += not ok
        print(f'  {"ok  " if ok else "FAIL"}  {want:>2} == {got:<2}  {why}')
    return bad


if __name__ == '__main__':
    if '--selftest' in sys.argv:
        bad = selftest()
        print('selftest clean' if not bad else f'{bad} selftest case(s) failed')
        sys.exit(1 if bad else 0)

    dirs, problems = audit()
    if not dirs:
        print('no tools/verify-* directories found — nothing checked')
        sys.exit(2)
    print(f'{len(dirs)} probe director{"y" if len(dirs)==1 else "ies"} checked: '
          + ', '.join(os.path.basename(d) for d in dirs))
    if not problems:
        print('  clean — probe, run.sh and README agree in every one')
        sys.exit(0)
    for p in problems:
        print(f'  DRIFT  {p}')
    sys.exit(1)
