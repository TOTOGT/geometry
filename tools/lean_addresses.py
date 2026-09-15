#!/usr/bin/env python3
"""lean_addresses.py — every .lean file named in prose must exist somewhere.

decl_resolve.py already checks that a cited declaration resolves at the path
cited. It takes a claims.json that nobody ever built, so it had never been run
across the corpus. This is the rung below it: the cheapest possible check,
requiring no hand-written input at all — does the FILE exist, anywhere, under
any of the roots the reader could plausibly be sent to?

A page that names a file which exists in no repository is making a claim whose
address resolves nowhere. It is not wrong about the mathematics. It is
unfalsifiable, which is worse, because a reader who goes looking cannot come
back with a verdict either way.

    python3 tools/lean_addresses.py ~/Desktop/geometry --roots ~/Desktop/AXLE ~/Desktop/GTCT
    python3 tools/lean_addresses.py --selftest

FINDINGS:

  DANGLING   the page names <X>.lean; no root contains a file of that name.
  CASE_ONLY  a file of that name exists under a different case. It opens on a
             macOS checkout and 404s on GitHub and on any Linux clone, so the
             page is right for its author and wrong for every reader.

Names are matched on the basename only, deliberately loosely: a hit here means
"something by that name exists and decl_resolve can take over", not "the path
is right". A miss is therefore a hard miss — no case, no directory, no repo.

Text inside <style>, <script> and HTML tags is stripped before matching, because
CSS selectors like `pre.lean-block` and `b.lean` otherwise read as filenames.
That is not a hypothetical: the first run of this check reported nine of them.

Declared examples — a filename a page names precisely in order to show what a
bad citation looks like — are exempted in EXEMPT below, by (page, name) pair.
A blanket name exemption would hide a real dangling citation elsewhere.

Exit 0 clean, 1 findings, 2 nothing checked.
"""
import os, re, sys

SKIP_DIRS = {'.lake', 'lake-packages', '.git', 'node_modules', '__pycache__'}
STYLE = re.compile(r'<(style|script)\b.*?</\1>', re.S | re.I)
TAG = re.compile(r'<[^>]+>')
NAME = re.compile(r'\b([A-Za-z][A-Za-z0-9_]*(?:[-_][A-Za-z0-9_]+)*\.lean)(?![-./\w])')

# (page relpath, cited name) pairs that are deliberate illustrations, or a file
# the page is instructing the READER to create rather than citing as evidence.
EXEMPT = {
    ('docs/defect-ledger.html', 'XXXXXX.lean'),
    ('course-16weeks.html', 'claim.lean'),
    # named on the page precisely to report that they resolve nowhere
    ('chDis-disaster.html', 'CatastropheF.lean'),
    ('chDis-disaster.html', 'ChaosMu.lean'),
    ('chDis-disaster.html', 'DisasterTheory.lean'),
    ('_archive/course-16weeks-source.html', 'claim.lean'),
}


def existing_names(roots):
    """basename -> [paths]. Every .lean file under every root."""
    out = {}
    for root in roots:
        root = os.path.abspath(os.path.expanduser(root))
        for dp, dns, fns in os.walk(root):
            dns[:] = [d for d in dns if d not in SKIP_DIRS]
            for f in fns:
                if f.endswith('.lean'):
                    out.setdefault(f, []).append(os.path.join(dp, f))
    return out


def prose(path):
    t = open(path, encoding='utf-8', errors='replace').read()
    return TAG.sub(' ', STYLE.sub(' ', t))


def scan(site, have):
    lower = {k.lower(): k for k in have}
    site = os.path.abspath(os.path.expanduser(site))
    findings = []
    pages = 0
    for dp, dns, fns in os.walk(site):
        dns[:] = [d for d in dns if d not in SKIP_DIRS]
        for f in sorted(fns):
            if not f.endswith('.html'):
                continue
            rel = os.path.relpath(os.path.join(dp, f), site)
            pages += 1
            for name in sorted(set(NAME.findall(prose(os.path.join(dp, f))))):
                if name in have or (rel, name) in EXEMPT:
                    continue
                alt = lower.get(name.lower())
                findings.append(('CASE_ONLY' if alt else 'DANGLING', rel, name, alt or ''))
    return pages, findings


SELFTEST = [
    # (page body, expected dangling names)
    ('<p>see Real.lean</p>', []),
    ('<p>see Ghost.lean</p>', ['Ghost.lean']),
    ('<style>pre.lean-block{color:red}</style><p>ok</p>', []),
    ('<p class="lean-kw">Ghost.lean</p>', ['Ghost.lean']),
    ('<a href="x.html" class="lean">Real.lean</a>', []),
    ('<p>run it on live.lean-lang.org</p>', []),
    ('<p>see real.lean</p>', ['real.lean']),
]


def selftest():
    import tempfile, shutil
    tmp = tempfile.mkdtemp()
    src, site = os.path.join(tmp, 'src'), os.path.join(tmp, 'site')
    os.makedirs(src); os.makedirs(site)
    open(os.path.join(src, 'Real.lean'), 'w').write('theorem t : True := trivial\n')
    have = existing_names([src])
    bad = 0
    for i, (body, want) in enumerate(SELFTEST):
        p = os.path.join(site, f'p{i}.html')
        open(p, 'w').write(body)
        _, F = scan(site, have)
        got = sorted(n for k, r, n, x in F if r == f'p{i}.html')
        ok = got == sorted(want)
        bad += not ok
        print(f'  {"ok  " if ok else "FAIL"}  case {i}: {got or ["clean"]}'
              f'   expected {sorted(want) or ["clean"]}')
        os.remove(p)
    shutil.rmtree(tmp)
    return bad


if __name__ == '__main__':
    if '--selftest' in sys.argv:
        bad = selftest()
        print('selftest clean' if not bad else f'{bad} case(s) failed')
        sys.exit(1 if bad else 0)
    argv = sys.argv[1:]
    if '--roots' in argv:
        i = argv.index('--roots')
        site, roots = argv[0], argv[i + 1:]
    else:
        site, roots = (argv[0] if argv else '.'), []
    roots = [site] + roots
    have = existing_names(roots)
    if not have:
        print('no .lean files found under any root — nothing checked')
        sys.exit(2)
    pages, F = scan(site, have)
    print(f'{pages} pages scanned against {len(have)} .lean files in {len(roots)} root(s)')
    if not F:
        print('  clean — every .lean file named in prose exists')
        sys.exit(0)
    by = {}
    for kind, rel, name, extra in F:
        by.setdefault((kind, name, extra), []).append(rel)
    nd = sum(1 for k, n, x in by if k == 'DANGLING')
    nc = len(by) - nd
    print(f'  {nd} names resolve nowhere, {nc} resolve only under another case;'
          f' {len(F)} citations in all\n')
    for kind in ('DANGLING', 'CASE_ONLY'):
        for (k, name, extra), pgs in sorted(
                by.items(), key=lambda kv: (-len(kv[1]), kv[0][1])):
            if k != kind:
                continue
            tail = f'  [on disk: {extra}]' if extra else ''
            print(f'  {k:<9} {name:<34} {len(pgs):>2}  {", ".join(sorted(pgs))}{tail}')
    sys.exit(1)
