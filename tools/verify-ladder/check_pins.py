#!/usr/bin/env python3
"""Fail unless lean-toolchain, the committed lake-manifest.json and (if present) the checked-out Mathlib all match
tools/verify-ladder/pins.txt. Usage: check_pins.py   (run from the repository root)"""
import json, os, subprocess, sys
root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
pins = dict(l.strip().split('=', 1) for l in open(os.path.join(root, 'tools/verify-ladder/pins.txt')) if '=' in l and not l.startswith('#'))
bad = []
tc = open(os.path.join(root, 'lean-toolchain')).read().strip()
print('lean-toolchain      :', tc, '(expected %s)' % pins['toolchain'])
if tc != pins['toolchain']: bad.append('lean-toolchain differs from pins.txt')
man = json.load(open(os.path.join(root, 'lake-manifest.json')))
pk = {p['name']: p for p in man['packages']}
mrev = pk.get('mathlib', {}).get('rev')
print('manifest mathlib rev:', mrev, '(expected %s)' % pins['mathlib_rev'])
if mrev != pins['mathlib_rev']: bad.append('lake-manifest.json mathlib rev differs from pins.txt')
d = os.path.join(root, '.lake/packages/mathlib')
if os.path.isdir(d):
    r = subprocess.run(['git', '-C', d, 'rev-parse', 'HEAD'], capture_output=True, text=True)
    got = r.stdout.strip()
    print('resolved mathlib rev:', got or '(unreadable: %s)' % r.stderr.strip())
    if got != pins['mathlib_rev']: bad.append('resolved Mathlib checkout differs from pins.txt')
else:
    print('resolved mathlib rev: .lake/packages/mathlib not present'); bad.append('Mathlib not resolved (run lake build / lake exe cache get first)')
for b in bad: print('::error::' + b)
sys.exit(1 if bad else 0)
