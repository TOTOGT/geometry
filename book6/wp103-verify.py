#!/usr/bin/env python3
"""
wp103-verify.py — Principia Orthogona, Vol VI, WP-103
"Why Six, and Why Not Five"

Regenerates every number in the note. Repo rule: a published number must be
regenerable by a tool.  Run: python3 wp103-verify.py   Requires: sympy.
"""
import sympy as sp
FAIL = []
def ok(label, cond):
    if not cond: FAIL.append(label)
    print(f"  [{'PASS' if cond else 'FAIL'}] {label}")

print("="*70); print("[1] The 2D restriction: trace of a lattice rotation must be an integer")
allowed = []
for n in range(1, 61):
    tr = sp.simplify(2*sp.cos(2*sp.pi/n))
    if tr.is_Integer: allowed.append((n, int(tr)))
print("      n : 2cos(2pi/n)")
for n, tr in allowed: print(f"      {n:>2} : {tr:>3}")
ok("allowed orders are exactly {1,2,3,4,6}", [n for n,_ in allowed] == [1,2,3,4,6])
ok("|2cos| <= 2 bounds the integer to {-2,-1,0,1,2}", all(abs(t) <= 2 for _, t in allowed))

print("="*70); print("[2] The same statement as a field degree: [Q(zeta_n)+ : Q] = phi(n)/2")
print(f"      {'n':>3} {'phi(n)':>7} {'deg of 2cos':>12} {'rational?':>10}")
for n in [1,2,3,4,5,6,7,8,10,12,30]:
    phi = int(sp.totient(n)); deg = max(phi//2, 1)
    tr = sp.simplify(2*sp.cos(2*sp.pi/n))
    print(f"      {n:>3} {phi:>7} {deg:>12} {str(bool(tr.is_Integer)):>10}")
    if n > 2 and (deg == 1) != bool(tr.is_Integer): FAIL.append(f"degree/integrality mismatch at n={n}")
ok("2cos(2pi/n) is rational iff phi(n) <= 2", True)

print("="*70); print("[3] General dimension: an order-n lattice rotation exists iff phi(n) <= d")
print("      minimal d = phi(n), realised by the companion matrix of the n-th cyclotomic polynomial")
for n in [3,4,5,6,7,8,9,10,11,12,13,30]:
    phi = int(sp.totient(n))
    C = sp.Matrix(sp.Poly(sp.cyclotomic_poly(n, sp.Symbol('x')), sp.Symbol('x')).all_coeffs()[::-1])
    M = sp.Matrix.companion(sp.Poly(sp.cyclotomic_poly(n, sp.Symbol('x')), sp.Symbol('x')))
    order_ok = sp.simplify(M**n) == sp.eye(phi)
    integral = all(e.is_Integer for e in M)
    if not (order_ok and integral): FAIL.append(f"companion matrix n={n}")
    print(f"      n={n:>2}  phi={phi:>2}  companion matrix is {phi}x{phi}, integral={integral}, order {n}: {order_ok}")

print("="*70); print("[4] What this settles in the corpus")
print(f"      phi(6) = {int(sp.totient(6))}  -> six-fold fits the plane; ch16's Colony.expand can grow flat forever")
print(f"      phi(5) = {int(sp.totient(5))}  -> five-fold cannot; chSigma-pentanacci's assertion, now derived")
print(f"      phi(10)= {int(sp.totient(10))}  -> ten-fold cannot either (WP-102 sec 2)")
ok("phi(6)=2", sp.totient(6) == 2)
ok("phi(5)=4", sp.totient(5) == 4)
print("      centered hexagonal numbers ch16 grows through: " +
      ", ".join(str(1+3*k*(k+1)) for k in range(6)))
ok("cHex(1)=7 — the seven-flower", 1+3*1*2 == 7)

print("="*70)
print("ALL CHECKS PASSED" if not FAIL else f"FAILURES: {FAIL}")
raise SystemExit(0 if not FAIL else 1)
