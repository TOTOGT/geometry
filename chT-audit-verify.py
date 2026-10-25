#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""chT-audit-verify.py - audit script for chT-tubulin.html (Book 3, Chapter T).

[A] arithmetic the chapter relies on (PASS = the audit's numbers hold; they are the
    reasons the page was relabelled).  [B] regression guards: PASS = audited wording in place.
Stdlib only.  Run: python3 chT-audit-verify.py
Principia Orthogona - Book 3 - G6 LLC - CC BY-NC-ND 4.0
"""
import html as H, math, re, sys
from pathlib import Path
PAGE = Path(__file__).resolve().parent / "chT-tubulin.html"
FAIL = []
def check(label, ok, detail=""):
    print(f"    {'PASS' if ok else 'FAIL'}  {label}" + (f"   {detail}" if detail else ""))
    if not ok: FAIL.append(label)

print("[A] arithmetic behind the audit")
phi = (1+5**.5)/2
check("beta = 0.382 is phi^-2 (0.38197), not phi^-1 (0.61803)", abs(0.382-phi**-2) < 5e-4 and abs(0.382-1/phi) > 0.2,
      f"phi^-2={phi**-2:.5f} phi^-1={1/phi:.5f}")
bend, L = math.radians(12), 8.2      # ~12 deg per heterodimer; heterodimer repeat ~8.2 nm (approximate)
kappa = bend/L
check("stated derivation (12 deg over ~8 nm) gives about 0.026 /nm, not 3.42 /nm", abs(kappa-0.0255) < 0.001 and 3.42/kappa > 100,
      f"{kappa:.4f} /nm; page value is {3.42/kappa:.0f}x larger")
check("3.42 /nm is a 0.29 nm radius of curvature; 2.81 /nm is 0.36 nm", abs(1/3.42-0.292) < 1e-3 and abs(1/2.81-0.356) < 1e-3)
check("microtubule wall (radius 12.5 nm) curvature is 0.08 /nm, 35-43x below the tabulated values", abs(1/12.5-0.08) < 1e-12 and 35 < 2.81/0.08 < 44 and 3.42/0.08 > 42)
check("omega = 0.077 /s gives a period of 81.6 s (page: ~80 s), self-consistent only", abs(2*math.pi/0.077-81.6) < 0.1)
check("12 nm / 13 = 0.923 nm, the P1 'prediction' (appears to be standard 3-start geometry)", abs(12/13-0.923) < 1e-3)
check("six Clay problems remain unsolved -> US$6 million, not 7 (Collatz has no Clay prize)", 6*1 == 6)
print("    NOTE  the 8.2 nm heterodimer repeat and the 12 nm 3-start pitch are standard figures from memory,")
print("          not checked against the cited cryo-EM papers.")

print("[B] page regression guards")
raw = PAGE.read_text(encoding="utf-8")
txt = re.sub(r"\s+", " ", H.unescape(re.sub(r"<[^>]+>", " ", re.sub(r"(?s)<(style|script).*?</\1>", "", raw))))
has = lambda x: x in txt
def guard(label, gone, here):
    check(label, all(not has(g) for g in gone) and all(has(h) for h in here))
guard("Theorem T.1 relabelled an unproved proposition", ["Theorem T.1 — Morphology is Computation"], ["Proposition T.1 (unproved)"])
guard("Table T.2 no longer 'computed'; no 'not a fit, it is a prediction'", ["Computed contact normal form parameters", "The contact normal form is not a fit. It is a prediction."], ["Stated contact normal form parameters (unverified)", "treat Table T.2 as unverified"])
guard("beta corrected to phi^-2", ["agrees with the inverse golden ratio"], ["equals φ⁻² (0.3820)"])
guard("Lean sketch flagged as not a verified mechanisation; dz - b dtheta + mu drho not contact", ["are fully discharged against Mathlib4."], ["this sketch is not a verified mechanisation", "α ∧ dα = 0"])
guard("sales claim corrected (6 Clay problems, none proved)", ["seven million dollars", "working drafts on all seven"], ["none is a proof"])
guard("age claim softened", ["for 500 million years", "more than 500 million years ago"], ["over 500 million years"])
print()
print(f"checks failed: {len(FAIL)}")
sys.exit(1 if FAIL else 0)
