#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Pablo Nogueira Grossi / G6 LLC
"""
book18/ch01-verify.py -- every number and quotation on book18/ch01-a-ratio-not-a-rate.html.
Run first (R24). The index's thesis for this chapter -- Leibniz's notation composes and
Newton's does not -- was written before either text was held. This script tests it.

    python3 book18/ch01-verify.py [--downloads DIR]

  [1] the held texts: ledger rows and hashes
  [2] Leibniz 1684, as reproduced in facsimile by Dunham (p. 22): the substitution sentence
  [3] Newton, Method of Fluxions (Colson 1736): dotted letters (§60, p. 20), the rule of
      Prob. I (p. 21), composition by an auxiliary fluent (Ex. 5, §12, p. 24), moments (§13-18)
  [4] Dunham on notation: Laplace's "very happy notation" (p. 22); dx as a tool (p. 24)
  [5] one composite, y = (x^2 + 1)^3, done both ways; and Newton's scheme as forward mode
  [HONESTY]
"""
import hashlib, os, re, subprocess, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
FAIL = []
def check(label, ok, detail=""):
    print(("PASS " if ok else "FAIL ") + label + (f"  -- {detail}" if detail else ""))
    if not ok: FAIL.append(label)
def dl():
    if "--downloads" in sys.argv: return Path(sys.argv[sys.argv.index("--downloads") + 1])
    for c in ("~/mnt/Downloads", "~/Downloads"):
        p = Path(os.path.expanduser(c))
        if p.is_dir(): return p
DL = dl()
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
flat = lambda s: re.sub(r"\s+", " ", s)
def pages(n):
    try: return subprocess.run(["pdftotext", "-layout", str(DL / n), "-"], capture_output=True, text=True, timeout=170).stdout.split("\f")
    except Exception: return None

print("[1] held")
NEW, DUN, RUM, GIF = "methodoffluxions00newt.pdf", "THE_CALCULUS_GALLERY_Masterpieces_from_Newton_to_Lebesgue.pdf", "RumelhartDE1986.pdf", "novamethodus-stoudt.gif"
led = (ROOT / "docs/floor-texts.tsv").read_text(encoding="utf-8")
for n in (NEW, DUN):
    h = sha(DL / n)
    check(f"{n} is a ledger row and hashes to it", h in led and n in led, h[:16])
check("Stoudt's scan of the Nova Methodus page (image, not ledgered) hashes as recorded", sha(DL / GIF).startswith("b4ed0136669f0e1b"))
check("Rumelhart 1986 (4 pp, under the ledger's page floor) hashes as recorded", sha(DL / RUM).startswith("1f7b0339d34bb6da"))

print("[2] Leibniz 1684, Dunham's facsimile (p. 22)")
D = pages(DUN)
d22 = flat(D[36]); d24 = flat(D[38])
check("the page is Dunham p. 22 and carries the 1684 facsimile", d22.strip().startswith("22 CHAPTER 2") and "first paper on differential calculus (1684)" in d22)
check("'Jam recta aliqua pro arbitrio assumta vocetur dx': dx is an arbitrary line", "pro arbitrio aifumta" in d22)
check("'In arbitrio enim est vel formulam, ut xv, vel compendio pro ea literam, ut y, adhibere'", "In arbitrio enim eft vel formulam" in d22 and "compendio pro ea" in d22)
check("'x et dx eodem modo in hoc calculo tractari, ut y et dy, vel aliam literam indeterminatam cum sua differentiali'", "eodem modo in hoc calculo" in d22 and "indeterminatam cum fua differentiali" in d22)
check("'non dari semper regressum a differentiali Aequatione, nisi cum quadam cautione'", "regrelfum a differentiali" in d22 and "cautio" in d22)

print("[3] Newton, Method of Fluxions (Colson 1736)")
N = pages(NEW)
n5 = flat(N[4])
check("title page: translated by John Colson", "THE METHOD of FLUXIONS" in n5 and "CO L SON" in n5)
n20, n21, n24, n25 = (flat(N[i]) for i in (43, 44, 47, 48))
check("§60 (p. 20): fluents are the final letters v, x, y, z", "call Fluents, or" in n20 and "final Letters of the" in n20)
check("§59 (p. 20): one equable fluxion stands in for Time", "by way of Analogy, it may not improperly receive" in n20)
check("Prob. I (p. 21): from the relation of the fluents, the relation of their fluxions", "to determine the Relation of their Fluxions" in n21)
check("Ex. 1 (p. 21): the answer is a proportion of fluxions, x-dot : y-dot :: ...", "which Equation gives the Relation between the Fluxions" in n21)
check("Ex. 5 (§12, p. 24): an auxiliary fluent z, its relation, then 'substitute this Value'", "Ex. 5" in n24 and "Value inftead of it" in n24)
check("§13-14 (p. 24): moments are velocity times an indefinitely small o", "The Moments of flowing Quantities" in n24 and "indefinitely fmall" in n24)
check("§17-18 (p. 25): terms multiplied by o 'will be nothing in respect of the rest. Therefore I reject them'", "Therefore I" in n25 and "reject" in n25)

print("[4] Dunham")
check("p. 22: Laplace's 'a very happy notation'", 'a very happy notation' in d22)
check("p. 24: the infinitely small used as 'a tool that has advantages for the purpose of the calculation'", "a tool that has advantages for the purpose of the calcula" in d24)

print("[5] one composite, both ways: y = (x^2 + 1)^3 at x = 1.2")
x = 1.2
# Leibniz: z = x^2 + 1 is a letter standing for a formula; dy = 3 z^2 dz, dz = 2x dx
z = x * x + 1
leib = 3 * z * z * (2 * x)
# Newton: two relations among fluents, y - z^3 = 0 and z - x^2 - 1 = 0; Prob. I gives
# y' - 3 z^2 z' = 0 and z' - 2 x x' = 0; take x' = 1 (x flows equably, as Time) and solve
xd = 1.0
zd = 2 * x * xd
yd = 3 * z * z * zd
check("Leibniz's substitution and Newton's auxiliary fluent give the same dy/dx", abs(leib - yd / xd) < 1e-12, f"{leib:.6f}")
h = 1e-6
check("and a central difference agrees", abs(leib - (((x+h)**2+1)**3 - ((x-h)**2+1)**3) / (2*h)) < 1e-5)
# Newton's scheme: every quantity carries its velocity w.r.t. one equable flow, seeded x' = 1.
class Fl:
    def __init__(s, v, d): s.v, s.d = v, d
    def __add__(s, o): o = o if isinstance(o, Fl) else Fl(o, 0.0); return Fl(s.v + o.v, s.d + o.d)
    def __mul__(s, o): o = o if isinstance(o, Fl) else Fl(o, 0.0); return Fl(s.v * o.v, s.v * o.d + s.d * o.v)
X = Fl(x, 1.0); Z = X * X + 1; Y = Z * Z * Z
check("carried as (value, fluxion) pairs with x' = 1, the rule is forward-mode arithmetic", abs(Y.d - leib) < 1e-9, f"{Y.d:.6f}")
chain_depth = 2
print(f"     Newton: {chain_depth} relations, {chain_depth} fluxion equations, then elimination")
print(f"     Leibniz: {chain_depth} substitutions, dy = 3z^2 dz = 3z^2 (2x dx)")

print("""
[HONESTY]
[2] reads Dunham's facsimile of the 1684 Acta page through its OCR layer, which spells
the long s as f; matches are made on fragments that survived. The clearer reprint page
scanned by G. Stoudt (IUP) was read by eye for this page and is hashed in [1] as the copy on this desk (the transfer to this machine re-encoded
it from GIF87a to GIF89a, so its hash differs from the file as downloaded); its edition
is not identified on the scan. Latin translations on the page are this chapter's own.
[3] reads Colson's 1736 English translation, not Newton's Latin manuscript of 1671; the
dotted letters are Colson's printing, checked by eye on p. 20 (OCR drops the dots).
[5] checks that the two procedures agree on one composite and that Newton's scheme,
written as arithmetic on (value, fluxion) pairs, is forward mode. That is a structural
identity, not a claim about what Newton intended.
""")
print(f"{len(FAIL)} FAIL")
sys.exit(1 if FAIL else 0)
