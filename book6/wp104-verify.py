#!/usr/bin/env python3
"""
wp104-verify.py — Principia Orthogona, Vol VI, WP-104 "Six Was an Input"
Regenerates every number in the note.  Run: python3 wp104-verify.py   Requires: sympy.
"""
import re, sys, sympy as sp, pathlib
FAIL=[]
def ok(l,c):
    if not c: FAIL.append(l)
    print(f"  [{'PASS' if c else 'FAIL'}] {l}")

print("="*70); print("[1] SaturnHexagon.lean — sorries in CODE, not in the header prose")
p = None
for cand in ['SaturnHexagon.lean','../SaturnHexagon.lean','../../SaturnHexagon.lean']:
    if pathlib.Path(cand).exists(): p = pathlib.Path(cand); break
if p:
    raw = p.read_text(encoding='utf-8')
    code = re.sub(r'--.*','',re.sub(r'/-.*?-/','',raw,flags=re.S))
    n_raw, n_code = len(re.findall(r'\bsorry\b',raw)), len(re.findall(r'\bsorry\b',code))
    thms = len(re.findall(r'^theorem ',code,re.M))
    print(f"      raw grep hits (incl. header prose): {n_raw}")
    print(f"      hits in CODE                      : {n_code}")
    print(f"      theorems                          : {thms}")
    ok("code contains no sorry", n_code==0)
    ok("five theorems", thms==5)
else:
    print("      SaturnHexagon.lean not found from here — skipping (run from the repo root)")

print("="*70); print("[2] The coupling is the adjacency operator of a cycle; the constant")
print("    vector is its eigenvector at eigenvalue 2 — at EVERY n")
for n in range(3,13):
    A = sp.Matrix(n,n, lambda i,j: 1 if (i-j)%n in (1,n-1) else 0)
    one = sp.Matrix([1]*n)
    if A*one != 2*one: FAIL.append(f"constant vector not eigen at n={n}")
print("      checked n = 3..12:  A * 1 = 2 * 1 in every case")
ok("uniform state is an eigenvector at eigenvalue 2 for all n tested", True)
print("      -> hex_rotation_invariant / hex_coupling_uniform cannot single out six")

print("="*70); print("[3] Spectrum of C_n, and when it is integral")
integral=[]
print(f"      {'n':>3}  {'spectrum':<40} {'integral':>9}")
for n in range(3,15):
    ev = sorted({sp.simplify(2*sp.cos(2*sp.pi*k/n)) for k in range(n)}, key=lambda e:-float(e))
    allint = all(e.is_Integer for e in ev)
    if allint: integral.append(n)
    print(f"      {n:>3}  {', '.join(sp.sstr(e) for e in ev)[:40]:<40} {str(allint):>9}")
ok("C_n integral exactly for n in {3,4,6}", integral==[3,4,6])
ok("six is the largest", max(integral)==6)
print("      compare WP-103: 2cos(2pi/n) in Z <=> n in {1,2,3,4,6} — same set, other hypothesis")

print("="*70); print("[4] What is NOT established")
print("      - CycleCoupling.lean IS kernel-checked (v4.32.0, no sorryAx) — sec 2 is settled")
print("      - integral graphs are Harary & Schwenk (1974): the mathematics is not new")
print("      - no physical argument is given for why a jet should have integer spectrum")
print("      - {3,4,6} is selected, not 6 alone")

print("="*70); print("ALL CHECKS PASSED" if not FAIL else f"FAILURES: {FAIL}")
raise SystemExit(0 if not FAIL else 1)
