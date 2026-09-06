#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Pablo Nogueira Grossi / G6 LLC
"""
toolchain_ledger.py — which files in this repo have a v4.32.0 kernel record.

    python3 tools/toolchain_ledger.py            # print the ledger
    python3 tools/toolchain_ledger.py --write    # also write docs/lean-4.32-ledger.md

WHY THIS EXISTS AND WHAT IT DOES NOT DUPLICATE

  tools/theorem_census.py  counts declarations. It cannot tell you whether any
                           of them was ever elaborated.
  tools/leanscan.sh        reports the root set and the never-imported files.
                           It is corpus-wide and does not go per declaration.
  tools/leancheck.sh       compiles and audits. It reports to a terminal, and a
                           terminal scrolls. Yesterday's pass leaves no artefact.
  tools/verify-*/run.sh    each writes an axioms.txt. That is the artefact — but
                           there is no view that says which FILES those reports
                           between them cover.

This is that view, and only that view. It compiles nothing and runs no Lean.
It reads the gate reports that already exist and answers one question per file:
is there a kernel record for this file's declarations, or is there not.

WHY IT MATTERS HERE. geometry is the only checkout in the corpus with a complete
v4.32.0 Mathlib build (CLAUDE.md, the four-toolchain table). Work migrating in
from AXLE (v4.14.0) or from a tree with no toolchain at all gets re-done here.
A file that lands in this repo, compiles once by hand, and never enters a gate
is indistinguishable a month later from a file that was never run. The whole
point of the tiered vocabulary — written / sorry-free / kernel-audited — is that
the third tier is evidenced. This is where you see which files have that evidence.

WHAT A ROW DOES NOT MEAN. "audited" here means: a gate report names declarations
belonging to this file, with no sorryAx on those lines. It does not mean the file
is correct, that its statements say anything, or that the report is recent. The
report's date is printed for exactly that reason. Read the date.

MATCHING IS BY LAST NAME COMPONENT. Gate reports carry fully-qualified names
(`PolarTriadClosure.reach_even`); the census carries the bare declaration. A name
appearing in two files is reported as AMBIGUOUS rather than credited to either —
under-report, never over-report, the same direction as every other count here.
"""
import os, re, sys, glob, datetime, subprocess
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import theorem_census as TC

ROOT = HERE.parent
GATE_SHAPES = ['tools/verify-*/axioms*.txt', 'tools/axioms*.txt']
SKIP = re.compile(r'(^|/)(_?to_delete|ml-evidence|\.lake)(/|$)')


def corpus_roots():
    """Declared, not discovered — the same file leanscan.sh and the registry read."""
    f = HERE / 'corpus_roots.txt'
    out = []
    if f.exists():
        for line in f.read_text(encoding='utf-8').splitlines():
            line = line.split('#')[0].strip()
            if line:
                out.append(Path(os.path.expanduser(line)))
    return out


def gate_names():
    """{bare declaration name: (report path, date)} over every gate report in the corpus.

    A report line carrying sorryAx contributes nothing: admitted is disclosed,
    not audited.
    """
    found = {}
    for root in corpus_roots() + [ROOT]:
        for shape in GATE_SHAPES:
            for rep in glob.glob(str(root / shape)):
                if SKIP.search(rep) or not os.path.exists(rep):
                    continue
                txt = open(rep, encoding='utf-8', errors='replace').read()
                date = datetime.date.fromtimestamp(os.path.getmtime(rep)).isoformat()
                for line in txt.splitlines():
                    m = re.match(r"'([^']+)' (depends on axioms|does not depend)", line)
                    if m and 'sorryAx' not in line:
                        found.setdefault(m.group(1).split('.')[-1],
                                         (os.path.relpath(rep, ROOT.parent), date))
    return found


def lake_targets():
    """Names declared as lean_lib in lakefile.lean. A file outside every target
    is never built, so it rots without anyone being told."""
    lf = ROOT / 'lakefile.lean'
    if not lf.exists():
        return set()
    return set(re.findall(r'^\s*lean_lib\s+([A-Za-z_][\w.]*)', lf.read_text(encoding='utf-8'), re.M))


def tracked_lean():
    out = subprocess.run(['git', 'ls-files', '*.lean'], cwd=ROOT,
                         capture_output=True, text=True)
    return sorted(Path(p) for p in out.stdout.split('\n') if p.strip())


def main():
    gates = gate_names()
    targets = lake_targets()
    owner = defaultdict(set)           # bare name -> files declaring it
    decls = {}
    for f in tracked_lean():
        src = TC.strip_comments((ROOT / f).read_text(errors='ignore'))
        names = [m.group(2).split('.')[-1] for m in TC.DECL.finditer(src)]
        decls[f] = names
        for n in names:
            owner[n].add(f)

    rows, tot_a, tot_d = [], 0, 0
    for f, names in decls.items():
        aud = [n for n in names if n in gates and len(owner[n]) == 1]
        amb = [n for n in names if n in gates and len(owner[n]) > 1]
        stem = f.stem
        in_target = stem in targets or any(str(f).startswith(t) for t in targets)
        rep, date = (gates[aud[0]] if aud else ('—', '—'))
        if aud:
            st = 'kernel-audited'
        elif amb:
            st = 'ambiguous name'
        elif not in_target:
            st = 'OUTSIDE EVERY TARGET'
        else:
            st = 'declared, no gate'
        tot_a += len(aud)
        tot_d += len(names)
        rows.append((str(f), len(names), len(aud), st, rep, date))

    toolchain = (ROOT / 'lean-toolchain').read_text().strip()
    today = datetime.date.today().isoformat()
    L = []
    L.append(f'# Lean {toolchain.split(":")[-1]} ledger — geometry, measured {today}\n')
    L.append(f'Produced by `tools/toolchain_ledger.py`. Toolchain pinned: `{toolchain}`.\n')
    L.append('Nothing here is compiled by this tool. Each row reports whether a gate '
             'report already on disk names this file\'s declarations. **Read the date '
             'column** — a stale report is a record of a past run, not of the file as '
             'it stands.\n')
    L.append(f'**{tot_a} of {tot_d} tracked declarations in this repo have a kernel record.**\n')
    L.append('| file | decls | audited | status | report | dated |')
    L.append('|---|---:|---:|---|---|---|')
    for r in sorted(rows, key=lambda r: (r[3] != 'kernel-audited', r[0])):
        L.append('| `{}` | {} | {} | {} | `{}` | {} |'.format(*r))
    L.append('')
    L.append('`OUTSIDE EVERY TARGET` is the row to act on first: `lake build` never '
             'touches that file, so it can stop compiling and nothing will say so.')
    out = '\n'.join(L)
    print(out)
    if '--write' in sys.argv:
        d = ROOT / 'docs' / f'lean-{toolchain.split(":")[-1].lstrip("v")}-ledger.md'
        d.write_text(out + '\n', encoding='utf-8')
        print(f'\nwrote {d.relative_to(ROOT)}', file=sys.stderr)


if __name__ == '__main__':
    main()
