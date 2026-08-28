#!/usr/bin/env python3
"""declaration_scan.py — does a declaration named in prose exist where it is claimed?

The rule (CLAUDE.md, 2026-08-27): every declaration named in prose must resolve.
A deposit that lists fifteen theorems by name has made fifteen checkable claims;
this is the tool that checks them, so that a reader is not asked to trust a list.

    python3 tools/declaration_scan.py tools/deposits/<name>.txt --corpus --tracked
    python3 tools/declaration_scan.py --names GenerativeOp,gronwall_radius --corpus --tracked
    python3 tools/declaration_scan.py ... --print-axioms   # emit the kernel-gate lines

WHAT RESOLUTION IS AND IS NOT. Resolving means: a declaration with that name is
declared, in a git-tracked file, in a repository in the corpus. It does NOT mean
the declaration is proved, that its statement says what the prose says it says, or
that it elaborates. A name that resolves to a `def` is reported as a def, because
prose that calls it a theorem is then wrong. A name that resolves to an `axiom` is
reported as an axiom, which is the opposite of a proof.

A dotted name (`UnfoldOp.stable_branch`) is matched exactly if possible, and
otherwise by its final component, reported as SHORT — Lean namespaces are not
parsed here, so a short match is a lead, not a confirmation.

Exit 0 only if every name resolves to a theorem/lemma with no `sorry` in its body.
Exit 1 otherwise. This is a gate: a deposit's claim list either holds or it does not.
"""
import os, re, sys, subprocess
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from theorem_census import strip_comments, tracked_lean, read_roots_file, SKIP_DIRS

ANY = re.compile(
    r'^[ \t]*(?:@\[[^\]]*\][ \t]*)*'
    r'(?:private[ \t]+|protected[ \t]+|noncomputable[ \t]+|nonrec[ \t]+)*'
    r'(theorem|lemma|axiom|def|instance|abbrev)[ \t]+([A-Za-z_À-￿][^\s:({\[]*)', re.M)


def index(roots, tracked):
    """name -> [(kind, repo, relpath, has_sorry)]"""
    idx = defaultdict(list)
    for root in roots:
        root = os.path.abspath(os.path.expanduser(root))
        repo = os.path.basename(root.rstrip('/'))
        keep = tracked_lean(root) if tracked else None
        if tracked and keep is None:
            print(f'warning: {root} is not a git repo — skipped', file=sys.stderr)
            continue
        for dp, dns, fns in os.walk(root):
            dns[:] = [d for d in dns if d not in SKIP_DIRS]
            for f in sorted(fns):
                if not f.endswith('.lean'):
                    continue
                p = os.path.join(dp, f)
                rel = os.path.relpath(p, root)
                if keep is not None and rel not in keep:
                    continue
                s = strip_comments(open(p, encoding='utf-8', errors='replace').read())
                ms = list(ANY.finditer(s))
                for k, m in enumerate(ms):
                    end = ms[k + 1].start() if k + 1 < len(ms) else len(s)
                    body = s[m.start():end]
                    idx[m.group(2)].append(
                        (m.group(1), repo, rel, bool(re.search(r'\bsorry\b', body))))
    return idx


def resolve(name, idx):
    if name in idx:
        return 'EXACT', idx[name]
    short = name.split('.')[-1]
    if short != name and short in idx:
        return 'SHORT', idx[short]
    return 'MISSING', []


def selftest():
    from declaration_scan_fixtures import CASES
    bad = 0
    for idx, name, expect, why in CASES:
        how, hits = resolve(name, idx)
        ok = how == expect
        bad += not ok
        kind = '/'.join(sorted({h[0] for h in hits})) or '—'
        print('  %s  %-26s %-8s kind %-8s %s' %
              ('ok  ' if ok else 'FAIL', name, how, kind, why))
    return bad


if __name__ == '__main__':
    argv = sys.argv[1:]
    if '--selftest' in argv:
        b = selftest()
        print('selftest clean' if not b else '%d case(s) failed' % b)
        sys.exit(1 if b else 0)
    tracked = '--tracked' in argv
    names = []
    for i, a in enumerate(argv):
        if a == '--names':
            names += [x.strip() for x in argv[i + 1].split(',') if x.strip()]
    files = [a for a in argv if not a.startswith('--')
             and os.path.isfile(os.path.expanduser(a)) and not a.endswith('.lean')]
    for f in files:
        names += read_roots_file(f)
    seen = set()
    names = [n for n in names if not (n in seen or seen.add(n))]
    if not names:
        print('no declaration names given', file=sys.stderr); sys.exit(2)

    roots = []
    if '--corpus' in argv:
        roots = read_roots_file(os.path.join(HERE, 'corpus_roots.txt'))
    roots += [a for a in argv if a.startswith('/') or a.startswith('~')]
    roots = [r for r in roots if os.path.isdir(os.path.expanduser(r))] or ['.']

    idx = index(roots, tracked)
    bad, resolved = 0, []
    print(f'{"declaration":<34} {"how":<8} {"kind":<9} {"sorry":<6} where')
    for n in names:
        how, hits = resolve(n, idx)
        if not hits:
            print(f'{n:<34} {"MISSING":<8} {"—":<9} {"—":<6} NOT FOUND IN CORPUS')
            bad += 1
            continue
        kinds = {h[0] for h in hits}
        sorried = any(h[3] for h in hits)
        kind = '/'.join(sorted(kinds))
        where = '; '.join(f'{h[1]}/{h[2]}' for h in hits[:3])
        if len(hits) > 3:
            where += f' (+{len(hits)-3} more)'
        flag = 'YES' if sorried else 'no'
        print(f'{n:<34} {how:<8} {kind:<9} {flag:<6} {where}')
        if kinds - {'theorem', 'lemma'} or sorried or how == 'SHORT':
            bad += 1
        else:
            resolved.append((n, hits[0]))

    print(f'\n{len(names)} named · {len(names)-bad} clean · {bad} needing attention')
    if '--print-axioms' in argv and resolved:
        print('\n-- kernel gate: paste into a Lean file that imports these modules,')
        print('-- then `lake env lean` it. Resolution is not proof; this is the check.')
        for n, h in resolved:
            print(f'#print axioms {n}   -- {h[1]}/{h[2]}')
    sys.exit(1 if bad else 0)
