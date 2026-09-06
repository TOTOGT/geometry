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

COUNTING AXIOMS, NOT JUST DECLARATIONS. The first version of this file filtered
on a grep for sorryAx and then threw the axiom list away. WP-73 §6 says why that
is the wrong shape twice over. Enumerating forbidden axioms cannot see
`Lean.ofReduceBool` or a `native_decide` axiom, so a declaration the kernel never
checked reads as audited; the permitted three are two lines and close the class
for good, including against whatever axiom nobody has thought of yet. And a
checker that counts only `depends on axioms: [...]` is blind to the other output
form — `does not depend on any axioms` — which is the STRONGEST result there is,
a proof resting on nothing, not even propext. WP-73 records a CI gate that
counted nine of twelve for exactly this reason and failed the job over its own
three best results.

So this file does not parse the reports itself. tools/axiom_gate.py already
rejoins Lean's wrapped pretty-printer lines, reads both output forms, and holds
the allowlist. Two tools with two parsers is two answers.

WHAT A ROW DOES NOT MEAN. "audited" here means: a gate report names declarations
belonging to this file, and every axiom on those lines is one of the permitted
three or there are none at all. It does not mean the file is correct, that its
statements say anything, or that the report is recent. The report's date is
printed for exactly that reason. Read the date.

THE TRIPLE IS NOT RECORDED, AND THAT IS A GAP. Verification is a property of
(artifact, toolchain, library) — WP-73 §2. A gate report on disk carries none of
the second and third: it is a list of names and axioms with a filesystem
timestamp. This ledger therefore cannot tell STALE from still-true, and does not
pretend to. CS/verify-stamp is the instrument that binds the triple; a row here
saying "kernel-audited" with an old date is an invitation to run it, not a
substitute for it.

MATCHING IS BY LAST NAME COMPONENT. Gate reports carry fully-qualified names
(`PolarTriadClosure.reach_even`); the census carries the bare declaration. A name
appearing in two files is reported as AMBIGUOUS rather than credited to either —
under-report, never over-report, the same direction as every other count here.
"""
import os, re, sys, glob, datetime, subprocess
from collections import defaultdict, Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import theorem_census as TC
import axiom_gate as AG

ROOT = HERE.parent
GATE_SHAPES = ['tools/verify-*/axioms*.txt', 'tools/axioms*.txt',
               # dated per-file reports written by `leancheck.sh --audit`,
               # so an overnight run raises Tier 1 without anyone typing a number
               'tools/verify-audit/*/*.axioms.txt']
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


def gate_records():
    """{bare declaration name: (axioms, report path, date)} over every gate report.

    Parsing is tools/axiom_gate.py's, not ours. A declaration resting on
    anything outside the permitted three is kept with its axiom list and
    classified UNTRUSTED downstream — never silently dropped, and never counted
    as audited.
    """
    found, unparsed = {}, []
    for root in corpus_roots() + [ROOT]:
        for shape in GATE_SHAPES:
            for rep in glob.glob(str(root / shape)):
                if SKIP.search(rep) or not os.path.exists(rep):
                    continue
                txt = open(rep, encoding='utf-8', errors='replace').read()
                date = datetime.date.fromtimestamp(os.path.getmtime(rep)).isoformat()
                label = os.path.relpath(rep, ROOT.parent)
                recs, unp = AG.parse(txt)
                unparsed += [(label, u) for u in unp]
                for name, ax in recs:
                    found.setdefault(name.split('.')[-1], (ax, label, date))
    return found, unparsed


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


PERMITTED = set(AG.DEFAULT_ALLOWED)


def classify(axioms):
    """'free' (rests on nothing), 'standard' (within the permitted three),
    or 'UNTRUSTED' (anything else — sorryAx, Lean.ofReduceBool, a native_decide
    axiom, or an axiom someone declared)."""
    if not axioms:
        return 'free'
    return 'standard' if set(axioms) <= PERMITTED else 'UNTRUSTED'


def main():
    gates, unparsed = gate_records()
    targets = lake_targets()
    owner = defaultdict(set)           # bare name -> files declaring it
    decls, declared_axioms = {}, {}
    for f in tracked_lean():
        src = TC.strip_comments((ROOT / f).read_text(errors='ignore'))
        names = [m.group(2).split('.')[-1] for m in TC.DECL.finditer(src)]
        decls[f] = names
        declared_axioms[f] = len(TC.AXIOM.findall(src))
        for n in names:
            owner[n].add(f)

    rows = []
    tot = Counter()
    for f, names in decls.items():
        hit = [n for n in names if n in gates and len(owner[n]) == 1]
        amb = [n for n in names if n in gates and len(owner[n]) > 1]
        kinds = Counter(classify(gates[n][0]) for n in hit)
        stem = f.stem
        in_target = stem in targets or any(str(f).startswith(t) for t in targets)
        rep, date = (gates[hit[0]][1], gates[hit[0]][2]) if hit else ('—', '—')
        audited = kinds['free'] + kinds['standard']
        if kinds['UNTRUSTED']:
            st = 'UNTRUSTED AXIOM'
        elif audited:
            st = 'kernel-audited'
        elif amb:
            st = 'ambiguous name'
        elif not in_target:
            st = 'OUTSIDE EVERY TARGET'
        else:
            st = 'declared, no gate'
        tot.update(kinds)
        tot['decls'] += len(names)
        tot['axiom_decls'] += declared_axioms[f]
        profile = ' · '.join(filter(None, [
            f"{kinds['free']} axiom-free" if kinds['free'] else '',
            f"{kinds['standard']} standard" if kinds['standard'] else '',
            f"**{kinds['UNTRUSTED']} untrusted**" if kinds['UNTRUSTED'] else '',
        ])) or '—'
        rows.append((str(f), len(names), audited, declared_axioms[f],
                     profile, st, rep, date))

    corpus_profile = Counter()
    for name, (ax, _, _) in gates.items():
        corpus_profile[tuple(sorted(ax)) or ('(none — axiom-free)',)] += 1

    toolchain = (ROOT / 'lean-toolchain').read_text().strip()
    ver = toolchain.split(':')[-1]
    today = datetime.date.today().isoformat()
    audited = tot['free'] + tot['standard']
    L = []
    L.append(f'# Lean {ver} ledger — geometry, measured {today}\n')
    L.append(f'Produced by `tools/toolchain_ledger.py`. Toolchain pinned: `{toolchain}`.\n')
    L.append('Nothing here is compiled by this tool. Each row reports whether a gate '
             "report already on disk names this file's declarations, and **what those "
             'declarations rest on**. Axiom reports are parsed by `tools/axiom_gate.py`, '
             'which holds the allowlist and rejoins Lean\'s wrapped output.\n')
    L.append(f'**{audited} of {tot["decls"]} tracked declarations in this repo have a '
             f'kernel record** — {tot["free"]} of them resting on no axiom at all, '
             f'{tot["standard"]} within the permitted three '
             f'(`propext`, `Classical.choice`, `Quot.sound`), '
             f'{tot["UNTRUSTED"]} outside them. '
             f'{tot["axiom_decls"]} explicit `axiom` declarations in this repo '
             '— an axiom is not a proof.\n')
    L.append('| file | decls | audited | `axiom` | rests on | status | report | dated |')
    L.append('|---|---:|---:|---:|---|---|---|---|')
    order = {'UNTRUSTED AXIOM': 0, 'kernel-audited': 1, 'ambiguous name': 2,
             'declared, no gate': 3, 'OUTSIDE EVERY TARGET': 4}
    for r in sorted(rows, key=lambda r: (order.get(r[5], 9), r[0])):
        L.append('| `{}` | {} | {} | {} | {} | {} | `{}` | {} |'.format(*r))
    L.append('')
    L.append('## Axiom profile across every gate report in the corpus\n')
    L.append('| declarations | rests on |')
    L.append('|---:|---|')
    for k, v in corpus_profile.most_common():
        L.append(f'| {v} | `{", ".join(k)}` |')
    L.append('')
    L.append('An axiom-free proof is the strongest result `#print axioms` can report, '
             'and a checker that counts only the `depends on axioms:` form cannot see '
             'it (WP-73 §6). Both forms are counted here.\n')
    if unparsed:
        L.append('## Report lines that did not parse\n')
        L.append('A line announcing axioms in a shape the gate cannot read is a finding, '
                 'never a silent skip.\n')
        for label, u in unparsed:
            L.append(f'- `{label}` — `{u}`')
        L.append('')
    L.append('`OUTSIDE EVERY TARGET` is the row to act on first: `lake build` never '
             'touches that file, so it can stop compiling and nothing will say so. '
             '`UNTRUSTED AXIOM` outranks it — a declaration resting on `sorryAx`, '
             '`Lean.ofReduceBool` or a `native_decide` axiom is disclosed, not audited.\n')
    L.append('Dates are file timestamps on the reports, not environment records. '
             'This ledger cannot tell STALE from still-true; `CS/verify-stamp` is the '
             'instrument that binds the triple.')
    out = '\n'.join(L)
    print(out)
    if '--write' in sys.argv:
        d = ROOT / 'docs' / f'lean-{ver.lstrip("v")}-ledger.md'
        d.write_text(out + '\n', encoding='utf-8')
        print(f'\nwrote {d.relative_to(ROOT)}', file=sys.stderr)


if __name__ == '__main__':
    main()
