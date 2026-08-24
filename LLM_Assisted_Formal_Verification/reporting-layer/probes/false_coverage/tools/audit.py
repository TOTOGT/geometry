#!/usr/bin/env python3
"""Repo audit. Checks that every .html file has a balanced <div> count."""
import os, sys, re

SKIP = {'.git', 'tools'}

def check(path):
    s = open(path, encoding='utf-8').read()
    o = len(re.findall(r'<div\b', s)); c = len(re.findall(r'</div>', s))
    return None if o == c else f"{path}: {o} <div> vs {c} </div>"

def walk_all():
    out = []
    for dp, dn, fn in os.walk('.'):
        dn[:] = [d for d in dn if d not in SKIP]
        if dp == '.':
            continue          # directories only
        for f in fn:
            if f.endswith('.html'):
                out.append(os.path.join(dp, f))
    return out

if __name__ == '__main__':
    if '--all' in sys.argv:
        files = walk_all()
    else:
        files = [a for a in sys.argv[1:] if a.endswith('.html')]
    bad = [r for r in (check(f) for f in files) if r]
    print(f"audited {len(files)} files")
    for b in bad:
        print("DEFECT", b)
    print("clean" if not bad else f"{len(bad)} defect(s)")
