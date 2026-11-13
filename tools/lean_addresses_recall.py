#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Pablo Nogueira Grossi / G6 LLC
"""
lean_addresses_recall.py -- recall of tools/lean_addresses.py against a small hand-labelled gold set.

Book XIV ch 5 said recall was never measured for the four reading tools. This measures one more of them,
on docs/lean-addresses-gold.tsv: for every token labelled Y (it names a Lean file), does the tool's
NAME pattern pick the name up at that place? It reports the pattern as it was before the fix for
sentence-final names (OLD_NAME) and as it is now (NAME).

    python3 tools/lean_addresses_recall.py

Limits: one labeller (Claude), one sample of 150 candidates, files cited without the '.lean' extension
are invisible to the set, and the tool's job after matching (does the file exist?) is not tested here.
Standard library only.
"""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lean_addresses as la

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GOLD = os.path.join(ROOT, 'docs', 'lean-addresses-gold.tsv')
# the pattern before the fix: a name followed by a dot was rejected, so "see Ghost.lean." was never seen
OLD_NAME = re.compile(r'\b([A-Za-z][A-Za-z0-9_]*(?:[-_][A-Za-z0-9_]+)*\.lean)(?![-./\w])')


def fires(rx, ctx, token):
    i = ctx.find(token)
    if i < 0:
        return False
    return any(m.start() < i + len(token) and m.end() > i for m in rx.finditer(ctx))


def main():
    rows, stale = [], 0
    for line in open(GOLD, encoding='utf-8'):
        if line.startswith('#') or not line.strip():
            continue
        page, token, lab, ctx = line.rstrip('\n').split('\t', 3)
        if lab != 'Y':
            rows.append((page, token, lab, None, None))
            continue
        path = os.path.join(ROOT, page)
        text = re.sub(r'\s+', ' ', la.prose(path)) if os.path.exists(path) else ''
        if ctx not in text:
            stale += 1
            continue
        rows.append((page, token, lab, fires(OLD_NAME, ctx, token), fires(la.NAME, ctx, token)))
    Y = [r for r in rows if r[2] == 'Y']
    o, n = sum(1 for r in Y if r[3]), sum(1 for r in Y if r[4])
    print(f"gold tokens labelled Y: {len(Y)}")
    print(f"before the fix: pattern fires on {o} -> recall {o/len(Y):.2f}")
    print(f"now:            pattern fires on {n} -> recall {n/len(Y):.2f}")
    print(f"misses before the fix: {[r[1] for r in Y if not r[3]]}")
    print(f"labelled N: {sum(1 for r in rows if r[2]=='N')}, stale: {stale}")
    return 1 if stale else 0


if __name__ == '__main__':
    sys.exit(main())
