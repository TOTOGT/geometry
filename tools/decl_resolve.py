#!/usr/bin/env python3
"""decl_resolve.py — every declaration named in prose must resolve, at the path cited.

The rule is in CLAUDE.md (2026-08-27). This is the tool that enforces it, so that a
paper, badge or README naming a Lean declaration can be checked instead of trusted.

    python3 tools/decl_resolve.py claims.json ~/Desktop/AXLE
    python3 tools/decl_resolve.py --selftest

claims.json is a list of {"file": "...", "decl": "...", "line": 123 (optional),
"claim": "T" (optional)} — the citations as written in the prose, verbatim, including
whatever case and spelling the prose used. That is the point: the tool compares the
citation against the filesystem, so the citation must not be cleaned up first.

FINDINGS, in decreasing severity:

  MISSING_FILE   no file at that path under any case
  MISSING_DECL   file resolves, declaration not declared in it
  CASE_MISMATCH  file exists under a different case. Works on macOS, 404s on a Linux
                 checkout and on GitHub. THIS TOOL EXISTS BECAUSE OF THIS CASE:
                 a hand-written `find -name 'AXLE_v8*'` missed `AXLE_V8.lean` and
                 reported a real declaration as absent. AXLE's own lakefile header
                 records the same defect (roots=["Finite"] vs finite.lean).
  LINE_OFF       declaration found, but not within 6 lines of the cited line number
  NOT_A_THEOREM  cited as a theorem/lemma but declared as def/abbrev/axiom/structure.
                 A `def` is a definition. It is not evidence of anything.
  UNBUILT        the file is in no lakefile target, so nothing ever elaborates it.
                 An unelaborated declaration is a name, not a theorem.

Exit 0 clean, 1 findings, 2 nothing checked.
"""
import os, re, sys, json

KINDS = r'(theorem|lemma|def|abbrev|instance|structure|axiom|noncomputable def)'
DECL = re.compile(
    r'^[ \t]*(?:@\[[^\]]*\][ \t]*)*'
    r'(?:private[ \t]+|protected[ \t]+|nonrec[ \t]+)*'
    r'(?:(noncomputable)[ \t]+)?'
    r'(theorem|lemma|def|abbrev|instance|structure|axiom)[ \t]+'
    r"([^\s:({\[]+)")
PROOF_KINDS = {'theorem', 'lemma'}
SKIP_DIRS = {'.lake', 'lake-packages', '.git', 'node_modules', '__pycache__'}


def index_files(root):
    """lowercased relpath -> actual relpath. Case-insensitive path resolution."""
    idx = {}
    for dp, dns, fns in os.walk(root):
        dns[:] = [d for d in dns if d not in SKIP_DIRS]
        for f in fns:
            if f.endswith('.lean'):
                rel = os.path.relpath(os.path.join(dp, f), root)
                idx.setdefault(rel.lower(), rel)
    return idx


def index_decls(path):
    """name -> [(line, kind)] for one file. Comments are NOT stripped here on
    purpose: a declaration commented out is a declaration that does not exist,
    and we want it reported as MISSING_DECL, not silently matched."""
    out = {}
    depth = 0
    for i, line in enumerate(open(path, encoding='utf-8', errors='replace'), 1):
        s = line
        # crude block-comment tracking, enough to skip /- ... -/ regions
        if depth:
            depth += s.count('/-') - s.count('-/')
            if depth < 0:
                depth = 0
            continue
        if '/-' in s and '-/' not in s:
            depth = 1
            continue
        if s.lstrip().startswith('--'):
            continue
        m = DECL.match(s)
        if m:
            kind = m.group(2)
            out.setdefault(m.group(3), []).append((i, kind))
    return out


def lakefile_roots(root):
    """Module roots declared in lakefile.toml / lakefile.lean, lowercased."""
    roots = set()
    for name in ('lakefile.toml', 'lakefile.lean'):
        p = os.path.join(root, name)
        if not os.path.exists(p):
            continue
        txt = open(p, encoding='utf-8', errors='replace').read()
        for m in re.finditer(r'roots\s*[:=]+\s*\[([^\]]*)\]', txt):
            for r in re.findall(r'"([^"]+)"', m.group(1)):
                roots.add(r.lower())
        for m in re.finditer(r'lean_lib\s+([A-Za-z_][\w.]*)', txt):
            roots.add(m.group(1).lower())
    return roots


def module_of(rel):
    return os.path.splitext(rel)[0].replace(os.sep, '.').lower()


def check(claims, root):
    root = os.path.abspath(os.path.expanduser(root))
    files = index_files(root)
    roots = lakefile_roots(root)
    findings = []
    cache = {}
    for c in claims:
        cited, decl = c['file'], c['decl']
        actual = files.get(cited.lower())
        if actual is None:
            findings.append(('MISSING_FILE', cited, decl, ''))
            continue
        if actual != cited:
            findings.append(('CASE_MISMATCH', cited, decl, f'on disk: {actual}'))
        if actual not in cache:
            cache[actual] = index_decls(os.path.join(root, actual))
        idx = cache[actual]
        if decl not in idx:
            findings.append(('MISSING_DECL', actual, decl, ''))
            continue
        hits = idx[decl]
        kinds = {k for _, k in hits}
        if c.get('claim', '').upper() == 'T' and not (kinds & PROOF_KINDS):
            findings.append(('NOT_A_THEOREM', actual, decl,
                             f'declared as {"/".join(sorted(kinds))}'))
        ln = c.get('line')
        if ln and not any(abs(a - ln) <= 6 for a, _ in hits):
            findings.append(('LINE_OFF', actual, decl,
                             f'cited L{ln}, found L{",L".join(str(a) for a, _ in hits)}'))
        mod = module_of(actual)
        if roots and not any(mod == r or mod.startswith(r + '.') for r in roots):
            findings.append(('UNBUILT', actual, decl, 'in no lakefile target'))
    return findings


SELFTEST = [
    # (filename on disk, file as cited, decl, claim, expected finding or None)
    ('Widget.lean', 'Widget.lean', 'foo_pos', 'T', None),
    ('AXLE_V8.lean', 'AXLE_v8.lean', 'eta_def', '', 'CASE_MISMATCH'),
    ('Widget.lean', 'Nope.lean', 'foo_pos', '', 'MISSING_FILE'),
    ('Widget.lean', 'Widget.lean', 'absent_thm', '', 'MISSING_DECL'),
    ('Widget.lean', 'Widget.lean', 'a_definition', 'T', 'NOT_A_THEOREM'),
    ('Widget.lean', 'Widget.lean', 'commented_out', '', 'MISSING_DECL'),
]


def selftest():
    import tempfile, shutil
    tmp = tempfile.mkdtemp()
    body = ('theorem foo_pos : True := trivial\n'
            'def a_definition : Nat := 1\n'
            'def eta_def : Nat := 1\n'
            '-- theorem commented_out : True := trivial\n')
    for name in ('Widget.lean', 'AXLE_V8.lean'):
        open(os.path.join(tmp, name), 'w').write(body)
    open(os.path.join(tmp, 'lakefile.toml'), 'w').write('roots = ["Widget", "AXLE_V8"]\n')
    bad = 0
    for disk, cited, decl, claim, want in SELFTEST:
        got = check([{'file': cited, 'decl': decl, 'claim': claim}], tmp)
        kinds = [g[0] for g in got]
        ok = (want in kinds) if want else (not kinds)
        bad += not ok
        print(f'  {"ok  " if ok else "FAIL"}  {cited}::{decl} -> {kinds or ["clean"]}'
              f'   expected {want or "clean"}')
    shutil.rmtree(tmp)
    return bad


if __name__ == '__main__':
    if '--selftest' in sys.argv:
        bad = selftest()
        print('selftest clean' if not bad else f'{bad} case(s) failed')
        sys.exit(1 if bad else 0)
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    if len(args) != 2:
        print(__doc__.strip().splitlines()[0]); print('usage: decl_resolve.py claims.json <repo-root>')
        sys.exit(2)
    claims = json.load(open(args[0], encoding='utf-8'))
    if not claims:
        print('claims file is empty — nothing checked'); sys.exit(2)
    F = check(claims, args[1])
    print(f'{len(claims)} citations checked against {args[1]}')
    if not F:
        print('  clean — every declaration resolves at the path cited'); sys.exit(0)
    order = ['MISSING_FILE', 'MISSING_DECL', 'CASE_MISMATCH', 'NOT_A_THEOREM', 'LINE_OFF', 'UNBUILT']
    for k in order:
        for kind, f, d, extra in F:
            if kind == k:
                print(f'  {kind:<14} {f}::{d}  {extra}')
    sys.exit(1)
