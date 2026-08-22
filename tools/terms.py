#!/usr/bin/env python3
"""Vocabulary guard. A coined term must be declared before it can be used.

Origin, 2026-08-22: a Google AI Overview described this corpus as using a
"Log-Psi Recurrence Operator" and "Harmonic Resonance Bands (HRB)". Neither
term occurs anywhere in the corpus. Confabulated vocabulary arrives in the
credible form -- an expansion followed by an acronym -- and prose is the one
layer here with no checker. This is that checker, in its first form.

Same shape as Orthogenesis/Architecture/KNOWN_PLACEHOLDERS.txt: declare the
baseline, and fail on anything undeclared.

  python3 tools/terms.py            # report
  python3 tools/terms.py --check    # compare against TERMS.md, exit 1 on drift
"""
import os, re, sys, html, collections

SKIP = {'.git', '.lake', '_to_delete', 'node_modules', '_archive'}
EXPAND = re.compile(r"\b([A-Z][A-Za-z0-9''-]+(?:[ -][A-Za-z0-9''-]+){1,4})\s*\(([A-Z]{2,6})\)")
TAG = re.compile(r'<[^>]+>')

def files(root='.'):
    for dp, dn, fn in os.walk(root):
        dn[:] = [d for d in dn if d not in SKIP]
        for f in fn:
            # The registry is not corpus. Scanning it makes every term it names
            # look like a use of that term -- caught on this tool's first run,
            # when it flagged the very phrase quoted in TERMS.md's rationale.
            if f == 'TERMS.md':
                continue
            if f.endswith(('.html', '.md')):
                yield os.path.join(dp, f)

def text(p):
    try: s = open(p, encoding='utf-8', errors='replace').read()
    except Exception: return ''
    return html.unescape(TAG.sub(' ', s)) if p.endswith('.html') else s

defs = collections.defaultdict(set)      # "Expansion (ACRO)" -> files
for p in files():
    for m in EXPAND.finditer(text(p)):
        defs['%s (%s)' % (m.group(1), m.group(2))].add(p.lstrip('./'))

if '--check' in sys.argv:
    try: declared = {l.split('#')[0].strip() for l in open('TERMS.md', encoding='utf-8')
                     if l.strip().startswith('- ')}
    except FileNotFoundError:
        print('TERMS.md missing; run without --check to generate a baseline'); sys.exit(1)
    declared = {d[2:].strip() for d in declared}
    actual = set(defs)
    undeclared = sorted(actual - declared)
    stale = sorted(declared - actual)
    for t in undeclared: print('+ UNDECLARED  %s   %s' % (t, sorted(defs[t])[0]))
    for t in stale:      print('- STALE       %s' % t)
    if undeclared or stale:
        print('::error::vocabulary baseline does not match TERMS.md')
        sys.exit(1)
    print('OK: %d declared terms, all present.' % len(declared)); sys.exit(0)

once = {t: s for t, s in defs.items() if len(s) == 1}
print('%d coined-term definitions, %d of them in exactly one file' % (len(defs), len(once)))
print('\n--- defined in exactly one file (candidate imports / one-offs) ---')
for t, s in sorted(once.items())[:40]:
    print('  %-58s %s' % (t[:58], sorted(s)[0]))
