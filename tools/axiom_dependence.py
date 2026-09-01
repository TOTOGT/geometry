#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Pablo Nogueira Grossi / G6 LLC
"""
axiom_dependence.py — which declarations rest on an axiom declared beside them.

    python3 tools/axiom_dependence.py            # the declared corpus roots
    python3 tools/axiom_dependence.py --json
    python3 tools/axiom_dependence.py PATH ...   # specific roots

WHAT THIS ANSWERS, AND WHAT IT DOES NOT

`#print axioms` (tools/axiom_gate.py) is the authoritative instrument: it asks the
kernel what a declaration actually depends on. It requires the file to ELABORATE.
Files that do not compile — wrong toolchain, removed Mathlib imports — are invisible
to it, and those are exactly the files where an unexamined axiom is most likely to
sit. AXLE/discreteDm3.lean is the case that motivated this tool: it imports
Mathlib.Init.Function, which no longer exists in Mathlib v4.32.0, so it cannot be
elaborated and cannot be gated, while its `collatz_converges` was published in the
theorem registry with a "proved" badge.

So this is a SOURCE-LEVEL scan, and it is deliberately crude:

  - it finds `axiom` / `private axiom` declarations by name, per file
  - it finds theorems and lemmas whose body mentions one of those names
  - it reports the body length, because a body of ~30 characters that names an
    axiom is a pass-through: the theorem asserts the axiom and nothing more

It cannot see axioms imported from another module, it does not resolve namespaces,
and a long body naming an axiom may well contain real work. Treat a hit as a
QUESTION — "what does this theorem add beyond the axiom?" — not as a verdict. The
short ones are the ones to read first.

WHY IT EXISTS. `sorry`-free is not proved, and an axiom is not a proof. A registry
that tiers declarations by "sorry-free in source" scores a one-line theorem invoking
an assumed conjecture identically to a real proof. This tool makes that population
countable so the tiering can name it.
"""
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOTS_FILE = os.path.join(HERE, 'corpus_roots.txt')
PREFIX = os.environ.get('AXDEP_PREFIX', os.path.expanduser('~'))
BARE = 80          # bodies at or under this many non-space chars are flagged bare

AXIOM = re.compile(r'^(?:private\s+)?axiom\s+([A-Za-z_][\w\'.]*)', re.M)
DECL = re.compile(
    r'^(?:private\s+|protected\s+|@\[[^\]]*\]\s*)*(theorem|lemma)\s+([A-Za-z_][\w\'.]*)'
    r'(.*?)(?=^\s*(?:@\[|/--|/-!|private\s|protected\s|theorem\s|lemma\s|def\s|'
    r'abbrev\s|instance\s|axiom\s|example\s|structure\s|inductive\s|end\s|namespace\s)|\Z)',
    re.M | re.S)


def read_roots():
    if not os.path.isfile(ROOTS_FILE):
        sys.exit(f'no roots file: {ROOTS_FILE}')
    out = []
    for line in open(ROOTS_FILE, encoding='utf-8'):
        line = line.split('#')[0].strip()
        if line:
            out.append(line)
    return out


def tracked_lean(root):
    r = subprocess.run(['git', '-C', root, 'ls-files', '*.lean'],
                       capture_output=True, text=True)
    return r.stdout.split() if r.returncode == 0 else []


def scan(paths):
    axioms_total, findings, files_seen, unreadable = 0, [], 0, []
    for root in paths:
        p = root.replace('~', PREFIX, 1) if root.startswith('~') else root
        if not os.path.isdir(os.path.join(p, '.git')):
            unreadable.append(root)
            continue
        for rel in tracked_lean(p):
            full = os.path.join(p, rel)
            try:
                src = open(full, encoding='utf-8', errors='ignore').read()
            except OSError:
                continue
            files_seen += 1
            names = sorted(set(AXIOM.findall(src)))
            axioms_total += len(names)
            if not names:
                continue
            for kind, decl, body in DECL.findall(src):
                tail = body.split(':=', 1)[-1] if ':=' in body else body
                used = [n for n in names if re.search(r'\b' + re.escape(n) + r'\b', body)]
                if used:
                    findings.append({
                        'file': f'{os.path.basename(p.rstrip("/"))}/{rel}',
                        'kind': kind, 'decl': decl, 'axioms': used,
                        'body_chars': len(re.sub(r'\s+', '', tail)),
                    })
    return axioms_total, findings, files_seen, unreadable


def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    paths = args or read_roots()
    axioms_total, findings, files_seen, unreadable = scan(paths)
    findings.sort(key=lambda f: (f['body_chars'], f['decl']))

    if '--json' in sys.argv:
        print(json.dumps({'axiom_declarations': axioms_total,
                          'files_scanned': files_seen,
                          'unreadable_roots': unreadable,
                          'findings': findings}, indent=2))
        return 0

    print(f'roots        : {len(paths)}   ({len(unreadable)} unreadable)')
    for u in unreadable:
        print(f'  UNREADABLE {u}   — totals below are not corpus totals')
    print(f'tracked .lean: {files_seen}')
    print(f'axiom declarations           : {axioms_total}')
    print(f'theorems/lemmas naming a local axiom : {len(findings)}')
    bare = [f for f in findings if f['body_chars'] <= BARE]
    print(f'  of which bare (body <= {BARE} chars, i.e. a pass-through): {len(bare)}')
    print()
    print(f'{"chars":>6}  {"declaration":<34}  {"rests on":<40}  file')
    print(f'{"-----":>6}  {"-"*34}  {"-"*40}  ----')
    for f in findings:
        mark = '*' if f['body_chars'] <= BARE else ' '
        print(f'{f["body_chars"]:>6}{mark} {f["decl"]:<34}  '
              f'{",".join(f["axioms"])[:40]:<40}  {f["file"]}')
    print()
    print('* = body is a pass-through; the declaration asserts the axiom and nothing more.')
    print('An unmarked row is a question, not a defect — read it before repeating it.')
    print('This is a source scan. The kernel gate is tools/axiom_gate.py, and it can only')
    print('see files that elaborate; the ones that do not are absent from both counts.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
