#!/usr/bin/env python3
"""textual_conclusion_scan.py — the textual half of the conclusion check.

`conclusion_scan.lean` is the authoritative instrument. It works on elaborated
terms after `whnf`, so it sees a conclusion that *reduces* to `True` through a
definition, and it catches `∀ x ∈ S, x ∈ S := id` — the shape its own header
names as the one a textual sweep misses. **This file misses that shape too.**
It is named for its mechanism and not for the property, per `CONVENTIONS.md` §1:
a textual check standing in for a semantic one, and being believed, is the
failure that document was written to prevent.

What this file is for, and the only thing it is for: the semantic scan requires
the file to elaborate. Most of this corpus cannot be built without a Mathlib
fetch, so most of it has never been scanned at all. This reads source text with
comments stripped, so it reaches every `.lean` file in every repository whether
or not it compiles. Use it to find candidates; confirm them with the Lean scan
where the file builds.

    python3 tools/textual_conclusion_scan.py --corpus --tracked
    python3 tools/textual_conclusion_scan.py ~/Desktop/AXLE --tracked
    python3 tools/textual_conclusion_scan.py --selftest

CLASSES. Only the first three are defects; the last two are candidates whose
content lives where a parser cannot see it and need a human read.

  VACUOUS       conclusion is `True`. Nothing is claimed.
  TRUE-TAILED   `True` inside the statement — `∃ _ : Prop, True`, `P ∧ True`,
                `∀ x, True`. The wrapper is real; what it claims is not.
  REFLEXIVE     the statement is `x = x` up to whitespace and ascriptions.
  NUMERIC-ONLY  no variables bound: a closed arithmetic fact. Real, but its
                content is entirely in whether those numerals model what the
                prose says they model.
  IDLE-BINDER   a bound variable never appears in the conclusion. Often fine
                (section variables, instance arguments); sometimes a hypothesis
                that constrains nothing, which is what `stable_branch` was.

KNOWN LIMITS, stated because a scanner believed past its scope is the defect
above. The statement/proof split scans to the first top-level `:` and `:=` by
bracket depth, not by Lean's grammar. `True` appearing as a value inside an
anonymous constructor `⟨…, True, …⟩` is a structure field, not a vacuous
conjunct, and is excluded — that exclusion is itself a heuristic. Fixtures live
in `textual_conclusion_scan_fixtures.py` and run before any verdict is read.

Exit 1 if any VACUOUS, TRUE-TAILED or REFLEXIVE declaration is found.
"""
import os, re, sys
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from theorem_census import strip_comments, tracked_lean, read_roots_file, SKIP_DIRS

DECL = re.compile(
    r'^[ \t]*(?:@\[[^\]]*\][ \t]*)*'
    r'(?:private[ \t]+|protected[ \t]+|noncomputable[ \t]+|nonrec[ \t]+)*'
    r'(theorem|lemma)[ \t]+([A-Za-z_À-￿][^\s:({\[]*)', re.M)

OPEN, CLOSE = '([{⟨', ')]}⟩'
# type names and numerals are not variables
TYPEWORDS = {'Nat', 'Int', 'Real', 'Prop', 'Type', 'ℝ', 'ℕ', 'ℤ', 'ℚ', 'True', 'False'}
TRIVIAL_TACTICS = {'trivial', 'rfl', 'decide', 'norm_num', 'simp', 'native_decide'}


def split_decl(text):
    """(binders, statement, proof) for one declaration body, by bracket depth."""
    d, i, n = 0, 0, len(text)
    colon = assign = -1
    while i < n:
        c = text[i]
        if c in OPEN:
            d += 1
        elif c in CLOSE:
            d -= 1
        elif d == 0 and text.startswith(':=', i):
            assign = i
            break
        elif d == 0 and c == ':' and not text.startswith(':=', i):
            if colon < 0:
                colon = i
        i += 1
    if colon < 0:
        return text, '', ''
    stmt_end = assign if assign >= 0 else n
    return text[:colon], text[colon + 1:stmt_end].strip(), (
        text[assign + 2:].strip() if assign >= 0 else '')


def identifiers(s):
    return set(re.findall(r'[A-Za-z_][A-Za-z0-9_\'!?]*', s))


def binder_names(binders):
    """Names bound in (x y : T) / {x : T} / [inst : T] groups."""
    out = set()
    for m in re.finditer(r'[({\[⟨]([^:()\[\]{}⟨⟩]+):', binders):
        for w in m.group(1).split():
            if re.fullmatch(r"[A-Za-z_][A-Za-z0-9_']*", w):
                out.add(w)
    return out


def first_tactic(proof):
    p = proof.strip()
    if p.startswith('by'):
        p = p[2:].strip()
    p = p.split('\n')[0].strip().rstrip(';')
    return p.split()[0] if p else ''


ASCRIPTION = re.compile(r'\(\s*([^()\s:]+)\s*:\s*[^()]+\)')


def normalise(s):
    """Collapse whitespace and strip type ascriptions: `(2 : Nat)` -> `2`."""
    prev = None
    while prev != s:
        prev = s
        s = ASCRIPTION.sub(r'\1', s)
    return ' '.join(s.split())


def classify(name, binders, stmt, proof):
    flags = []
    s = ' '.join(stmt.split())
    ns = normalise(s)
    vacuous = ns == 'True'
    if vacuous:
        flags.append(('VACUOUS', 'conclusion is True'))
    m = re.fullmatch(r'(.+?)\s*=\s*(.+)', ns)
    if m and m.group(1).strip() == m.group(2).strip():
        flags.append(('REFLEXIVE', 'statement is x = x'))
    # `True` inside ⟨…⟩ is a structure field value, not a conjunct of the claim.
    outside_ctor = re.sub(r'⟨[^⟨⟩]*⟩', '', ns)
    if not vacuous and re.search(r'\bTrue\b', outside_ctor):
        flags.append(('TRUE-TAILED', 'True appears inside the statement: the '
                                     'quantifier or conjunct around it claims nothing'))
    ids = identifiers(ns) - TYPEWORDS
    if ns and not ids and not vacuous:
        flags.append(('NUMERIC-ONLY', 'closed arithmetic, tactic: %s' % (first_tactic(proof) or '?')))
    bound = binder_names(binders)
    idle = sorted(b for b in bound if b not in identifiers(ns))
    if idle and not vacuous:
        flags.append(('IDLE-BINDER', 'unused in conclusion: ' + ', '.join(idle)))
    return flags


def scan_file(path, repo, rel):
    src = strip_comments(open(path, encoding='utf-8', errors='replace').read())
    ms = list(DECL.finditer(src))
    rows = []
    for k, m in enumerate(ms):
        end = ms[k + 1].start() if k + 1 < len(ms) else len(src)
        body = src[m.end():end]
        binders, stmt, proof = split_decl(body)
        rows.append((m.group(2), repo, rel, classify(m.group(2), binders, stmt, proof),
                     ' '.join(stmt.split())[:70]))
    return rows


from textual_conclusion_scan_fixtures import CASES  # noqa: E402


def selftest():
    bad = 0
    for text, name, expect in CASES:
        rows = []
        ms = list(DECL.finditer(text))
        for k, m in enumerate(ms):
            end = ms[k + 1].start() if k + 1 < len(ms) else len(text)
            b, s, p = split_decl(text[m.end():end])
            rows.append((m.group(2), classify(m.group(2), b, s, p)))
        got = {c for _, fl in rows for c, _ in fl}
        ok = (expect in got) if expect else not got
        bad += not ok
        print('  %s  %-4s expect %-13s got %s' %
              ('ok  ' if ok else 'FAIL', name, expect or 'clean', sorted(got) or 'clean'))
    return bad


if __name__ == '__main__':
    argv = sys.argv[1:]
    if '--selftest' in argv:
        b = selftest()
        print('selftest clean' if not b else '%d case(s) failed' % b)
        sys.exit(1 if b else 0)

    tracked = '--tracked' in argv
    roots = []
    if '--corpus' in argv:
        roots = read_roots_file(os.path.join(HERE, 'corpus_roots.txt'))
    roots += [a for a in argv if not a.startswith('--')]
    roots = [r for r in roots if os.path.isdir(os.path.expanduser(r))] or ['.']

    allrows = []
    for root in roots:
        root = os.path.abspath(os.path.expanduser(root))
        repo = os.path.basename(root.rstrip('/'))
        keep = tracked_lean(root) if tracked else None
        if tracked and keep is None:
            print('warning: %s is not a git repo — skipped' % root, file=sys.stderr)
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
                allrows += scan_file(p, repo, rel)

    counts = defaultdict(int)
    hard = 0
    for cls in ('VACUOUS', 'TRUE-TAILED', 'REFLEXIVE', 'NUMERIC-ONLY', 'IDLE-BINDER'):
        rows = [r for r in allrows if any(c == cls for c, _ in r[3])]
        if not rows:
            continue
        print('\n== %s (%d) ==' % (cls, len(rows)))
        for name, repo, rel, fl, stmt in sorted(rows, key=lambda r: (r[1], r[2], r[0])):
            why = next(w for c, w in fl if c == cls)
            print('  %-38s %s/%s\n      %s   [%s]' % (name, repo, rel, stmt or '(unparsed)', why))
        counts[cls] = len(rows)
        if cls in ('VACUOUS', 'TRUE-TAILED', 'REFLEXIVE'):
            hard += len(rows)

    print('\n%d theorems scanned · ' % len(allrows) +
          ' · '.join('%s %d' % (k, counts[k]) for k in
                     ('VACUOUS', 'TRUE-TAILED', 'REFLEXIVE', 'NUMERIC-ONLY', 'IDLE-BINDER')))
    print('VACUOUS, TRUE-TAILED and REFLEXIVE are defects. The other two need a human read.')
    sys.exit(1 if hard else 0)
