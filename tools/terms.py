#!/usr/bin/env python3
"""Vocabulary guard. A coined term must be declared before it can be used.

Origin, 2026-08-22: a Google AI Overview described this corpus as using a
"Log-Psi Recurrence Operator" and "Harmonic Resonance Bands (HRB)". Neither
term occurs anywhere in the corpus. Confabulated vocabulary arrives in the
credible form -- an expansion followed by an acronym -- and prose is the one
layer here with no checker. This is that checker.

Same shape as Orthogenesis/Architecture/KNOWN_PLACEHOLDERS.txt: declare the
baseline, and fail on anything undeclared.

  python3 tools/terms.py            # report
  python3 tools/terms.py --check    # compare against TERMS.md, exit 1 on drift

USE AND MENTION, 2026-08-22 (second form)
-----------------------------------------
The first form skipped TERMS.md by name, because scanning the registry made
every declared term look like a use of that term. That was the right instinct
applied to one file instead of to the category. CI run #247 found the rest of
it: `CLAUDE.md` records why this checker exists, and to do so it names the
confabulated term. The guard read that as a first use of undeclared
vocabulary and failed the job -- the corpus was punished for writing down
that the term is not its own.

The distinction the guard was missing is use versus mention. A term can
appear in this corpus in two quite different ways:

  USE      the corpus adopts the term and builds on it
  MENTION  the corpus names the term in order to talk about it, most often
           to disown it

So TERMS.md now has two sections. The main list is vocabulary this corpus
uses. The `## Disowned` list is vocabulary attributed to this corpus from
outside that it does not use; each entry carries the files permitted to
mention it. A mention in one of those files is fine. The same term appearing
anywhere else is a *louder* failure than an ordinary undeclared term, because
it means a confabulation has been absorbed into the corpus -- the exact event
this checker was written to catch.
"""
import os, re, sys, html, collections

SKIP = {'.git', '.lake', '_to_delete', 'node_modules', '_archive'}
EXPAND = re.compile(r"\b([A-Z][A-Za-z0-9''-]+(?:[ -][A-Za-z0-9''-]+){1,4})\s*\(([A-Z]{2,6})\)")
TAG = re.compile(r'<[^>]+>')
REGISTRY = 'TERMS.md'


def files(root='.', include_registry=False):
    for dp, dn, fn in os.walk(root):
        dn[:] = [d for d in dn if d not in SKIP]
        for f in fn:
            # The registry is not corpus. Scanning it as corpus makes every
            # term it names look like a use of that term -- caught on this
            # tool's first run, when it flagged the very phrase quoted in
            # TERMS.md's own rationale.
            if f == REGISTRY and not include_registry:
                continue
            if f.endswith(('.html', '.md')):
                yield os.path.join(dp, f)


def text(p):
    try:
        s = open(p, encoding='utf-8', errors='replace').read()
    except Exception:
        return ''
    return html.unescape(TAG.sub(' ', s)) if p.endswith('.html') else s


def read_registry(path=REGISTRY):
    """Return (declared, disowned) where disowned maps term -> set(allowed files).

    A line under `## Disowned` has the form

        - Harmonic Resonance Bands (HRB) @ CLAUDE.md, docs/audit-log.md

    Everything after `@` is the list of files permitted to mention the term.
    """
    declared, disowned, in_disowned = set(), {}, False
    with open(path, encoding='utf-8') as fh:
        for line in fh:
            if line.startswith('#'):
                in_disowned = line.lower().lstrip('# ').startswith('disowned')
                continue
            if not line.strip().startswith('- '):
                continue
            body = line.split('#')[0].strip()[2:].strip()
            if in_disowned:
                term, _, allowed = body.partition('@')
                disowned[term.strip()] = {a.strip() for a in allowed.split(',') if a.strip()}
            else:
                declared.add(body)
    return declared, disowned


def expansion_of(term):
    """'Harmonic Resonance Bands (HRB)' -> 'Harmonic Resonance Bands'."""
    return re.sub(r'\s*\([A-Z]{2,6}\)\s*$', '', term).strip()


def main():
    defs = collections.defaultdict(set)      # "Expansion (ACRO)" -> files
    for p in files():
        for m in EXPAND.finditer(text(p)):
            defs['%s (%s)' % (m.group(1), m.group(2))].add(p.lstrip('./'))

    if '--check' not in sys.argv:
        once = {t: s for t, s in defs.items() if len(s) == 1}
        print('%d coined-term definitions, %d of them in exactly one file'
              % (len(defs), len(once)))
        print('\n--- defined in exactly one file (candidate imports / one-offs) ---')
        for t, s in sorted(once.items())[:40]:
            print('  %-58s %s' % (t[:58], sorted(s)[0]))
        return 0

    try:
        declared, disowned = read_registry()
    except FileNotFoundError:
        print('TERMS.md missing; run without --check to generate a baseline')
        return 1

    failed = False

    # A disowned term is not undeclared -- but it may only be MENTIONED, and
    # only where the registry says it may be.
    for term, allowed in sorted(disowned.items()):
        phrase = expansion_of(term)
        seen = set()
        for p in files(include_registry=True):
            if phrase in text(p):
                seen.add(p.lstrip('./'))
        intruders = sorted(seen - allowed - {REGISTRY})
        for p in intruders:
            print('::error::DISOWNED TERM IN USE  %s   %s' % (term, p))
            failed = True
        if intruders:
            print('::error::  This term was attributed to this corpus from outside and'
                  ' is not its vocabulary.')
            print('::error::  It may be mentioned only in: %s'
                  % (', '.join(sorted(allowed)) or '(nothing)'))
            print('::error::  Its appearance elsewhere means a confabulation has been'
                  ' absorbed. That is the event tools/terms.py exists to catch.')

    actual = set(defs)
    undeclared = sorted(actual - declared - set(disowned))
    stale = sorted(declared - actual)
    for t in undeclared:
        print('+ UNDECLARED  %s   %s' % (t, sorted(defs[t])[0]))
    for t in stale:
        print('- STALE       %s' % t)
    if undeclared or stale:
        print('::error::vocabulary baseline does not match TERMS.md')
        failed = True

    if failed:
        return 1
    print('OK: %d declared terms, all present; %d disowned terms, mentioned only'
          ' where declared.' % (len(declared), len(disowned)))
    return 0


if __name__ == '__main__':
    sys.exit(main())
