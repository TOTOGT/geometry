#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Pablo Nogueira Grossi / G6 LLC
"""
book28/ch03-verify.py -- every number and quotation on book28/ch03-the-winding-number.html. Run first (R24).
    python3 book28/ch03-verify.py [--downloads DIR]
  [1] Zois, 18 Lectures on K-Theory (arXiv:1008.1346v1), Part II Lecture 2: the sentences quoted, by PDF page
  [1b] two more witnesses to Ind T_f = -wn(f) (Blackadar; the unattributed Chapter 10 draft), and the other Noether
  [1c] F. Noether, Math. Ann. 82 (1921), pp. 42-63: the scan, by OCR -- now held, see docs/audit-log.md 2026-09-28
  [2] winding numbers of eleven symbols, two ways: the argument around the circle, and roots inside the disc
  [3] Zois Prop. 1 on polynomial symbols: T_f T_g - T_fg has finite rank, the same at every truncation (exact)
  [4] Zois Thm. 1, Ind T_f = -wn(f), observed on the same eleven symbols from N x N sections (numerical)
  [5] Mathlib at the pinned revision: what the bridge would need, and what is there
  [HONESTY]
"""
import json, os, re, subprocess, sys
from fractions import Fraction
from pathlib import Path
import numpy as np
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
squash = lambda s: re.sub(r"\s+", "", s.replace("-\n", "")).lower()

print("[1] Zois, 18 Lectures on K-Theory, Part II Lecture 2")
Z = subprocess.run(["pdftotext", "-layout", str(dl() / "18 LECTURES ON K-THEORY.pdf"), "-"],
                   stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True).stdout.split("\f")
QS = [(63, "Lecture 2 (Index of Toeplitz Operators, Winding Number and K-Homology)"),
      (63, "the Hardy space, namely the functions with only positive Fourier coefficients"),
      (64, "is called the Hardy projection"),
      (64, "(hence the Hardy projection is non-local but not very far from being local)"),
      (64, "Then the Toeplitz operator Tf : H 2 (S 1 ) →"),
      (64, "Proposition 1. Tf Tg − Tf g is compact."),
      (65, "Corollary 1. If f ∈ C(S 1 ) is invertible, then Tf is Fredholm."),
      (65, "Key Question: What is the index of Tf ?"),
      (65, "the winding number, denoted wn(f ), of f is the only topological invariant of such maps"),
      (65, "IndTf = −wn(f )"),
      (65, "Each homotopy class contains a representative z m and we just check what the answer is on this representative"),
      (65, "Thus Tz is the unilateral shift with index −1"),
      (66, "The above data define an odd K-cycle for the space X, namely an element of K −1 (X)"),
      (66, "This suggests that K-cycles should generate a ”dual” to K-Theory, namely K-Homology"),
      (67, "definition of K-cycle a la Connes in Noncommutative Geometry")]
for pg, q in QS:
    check(f'Zois p.{pg}: "{q[:62]}"', squash(q) in squash(Z[pg - 1]))
check("Zois cites no paper of F. Noether (the 1921 source is read directly in [1c])",
      "noether" not in " ".join(Z).lower())

print("[1b] two more witnesses, and the other Noether")
def pdfp(name): return subprocess.run(["pdftotext", "-layout", str(dl() / name), "-"], stdout=subprocess.PIPE,
                                      stderr=subprocess.DEVNULL, text=True).stdout.split("\f")
BL = pdfp("K-THEORY FOR OPERATOR ALGEBRAS Bruce Blackadar.pdf")
check('Blackadar PDF p.263 (printed 249), Ex. 24.1.2(a): "The Index Theorem then says that Inda (Df ) = −(winding number of f )"',
      squash("The Index Theorem then says that Inda (Df ) = −(winding number of f )") in squash(BL[262]))
check('Blackadar calls it the odd-dimensional case: "in the odd" … "and even-dimensional cases respectively"',
      squash("illustrate the typical content of the Index Theorem in the odd") in squash(BL[262])
      and squash("and even-dimensional cases respectively") in squash(BL[262]))
C10 = pdfp("CHAPTER 10 K-theory.pdf")
check('Chapter 10 (unattributed draft, held) PDF p.11: "the index of A is given by the winding number of the determinant of the symbol"',
      squash("the index of A is given by the winding number of the determinant of the symbol") in squash(C10[10]))
check('…and its proof is marked unfinished: "Proof. ****Expand"', squash("Proof. ****Expand") in squash(C10[10]))
EMMY = ["Vladimir M. Ristić Noether's Theorem.pdf", "Noether’s Theorem Is Not So Simple.pdf", "EMMY NOETHER (1882 - 1935) .pdf",
        "Colloquium- A Century of Noether’s Theorem.pdf", "On the wonderfulness of Noether’s theorems, 100 years later, and Routh reduction.pdf"]
E_ = " ".join(" ".join(pdfp(f)) for f in EMMY)
check("the five 'Noether's theorem' texts held are Emmy Noether's 1918 theorem: '1918' throughout, 'Fritz' nowhere, 'Toeplitz' nowhere",
      E_.count("1918") >= 20 and "Fritz" not in E_ and "Toeplitz" not in E_, f"1918 x{E_.count('1918')}")

CK = pdfp("Cooke_The History of Mathematics.pdf")
check('Cooke, History of Mathematics (3rd ed. 2013), p. 412 (PDF 440): "her brother Fritz (1884–1941), who was also a mathematician"',
      squash("her brother Fritz (1884–1941), who was also a mathematician") in squash(CK[439]) and CK[439].lstrip().startswith("412"))
check('…and Emmy was "the eldest child of the distinguished mathematician Max Noether"',
      squash("the eldest child of the distinguished mathematician Max Noether") in squash(CK[439]))

print("[1c] F. Noether, Math. Ann. 82 (1921), pp. 42-63: the scan, by OCR")
import shutil, tempfile, hashlib
MA = dl() / "Titel- Mathematische Annalen Jahr- 1921.pdf"
if not (shutil.which("tesseract") and shutil.which("pdftoppm")):
    print("  needs tesseract and pdftoppm:  brew install tesseract poppler"); sys.exit(2)
tmp = Path(tempfile.mkdtemp())
def ocr(scan):                               # scan n holds printed page n - 6
    subprocess.run(["pdftoppm", "-r", "200", "-gray", "-png", "-f", str(scan), "-l", str(scan), str(MA), str(tmp / f"s{scan}")], check=True)
    return subprocess.run(["tesseract", str(next(tmp.glob(f"s{scan}*.png"))), "-"], capture_output=True, text=True).stdout
S = {n: squash(ocr(n)) for n in (48, 49, 57, 58, 61)}
check("the volume is Mathematische Annalen 82 (Göttingen digitisation PPN235181684_0082)",
      "PPN235181684_0082" in subprocess.run(["pdftotext", "-l", "1", str(MA), "-"], capture_output=True, text=True).stdout)
NQ = [(48, 42, "Fritz Noether in Karlsruhe"),
      (48, 42, "Die folgende Mitteilung beschäftigt sich mit linearen Integral"),
      (49, 43, "Anzahl der Reihen und der Kolonnen"),
      (49, 43, "die Differenz eine bestimmte und explizit angebbare"),
      (48, 42, "Theorie der Gezeiten"),
      (48, 42, "Hydrodynamik schwach reibender"),
      (57, 51, "Die Differenz der homogenen"),
      (58, 52, "Index"),
      (61, 55, "Die Differenz der homogenen"),
      (61, 55, "Dabei ist n der Index"),
      (61, 55, "Index die Hälfte einer ungeraden Zahl")]
def ascii_(s): return s.replace("ä", "a").replace("ü", "u").replace("ö", "o")
for scan, pg, q in NQ:
    ok = squash(q) in S[scan] or ascii_(squash(q)) in ascii_(S[scan])
    check(f'Noether p.{pg} (scan {scan}): "{q}"', ok)
check("Satz I and Satz II are both on the OCR'd pages", "satzi." in S[57] and "satzii." in S[61])
img = ROOT / "book28/img/noether-1921-satz-ii.png"
check("book28/img/noether-1921-satz-ii.png is the crop of p. 55 shown on the page",
      hashlib.sha256(img.read_bytes()).hexdigest().startswith("366db397cc22b653"))

print("[2] winding numbers, two ways")
def fromroots(rs, lo):                     # z^lo * prod (z - r)
    c = np.poly(rs)[::-1]; return {i + lo: complex(v) for i, v in enumerate(c)}
SYM = [("z", {1: 1}), ("z³", {3: 1}), ("z⁻²", {-2: 1}), ("2 + z", {0: 2, 1: 1}), ("1 + 2z", {0: 1, 1: 2}),
       ("z⁻¹ + 3 + z/4", {-1: 1, 0: 3, 1: .25}), ("z⁻¹ + z/4", {-1: 1, 1: .25}),
       ("(z−.3)(z−.5)(z−3)/z", fromroots([.3, .5, 3], -1)),
       ("(z−.2)(z+.4i)(z−2)(z−5)/z²", fromroots([.2, .4j, 2, 5], -2)),
       ("(z−.2)(z−.4)(z−.6)(z−3)/z", fromroots([.2, .4, .6, 3], -1)),
       ("(z−.5)(z−2)/z³", fromroots([.5, 2], -3))]
def wn_arg(c, M=8192):
    z = np.exp(2j * np.pi * np.arange(M) / M); f = sum(v * z ** k for k, v in c.items())
    return round(float(np.angle(np.roll(f, -1) / f).sum() / (2 * np.pi))), float(np.abs(f).min())
def wn_roots(c):
    m = -min(min(c), 0); p = np.zeros(max(c) + m + 1, complex)
    for k, v in c.items(): p[k + m] = v
    r = np.roots(p[::-1]); return int((abs(r) < 1).sum()) - m
WN = {}
for name, c in SYM:
    a, mn = wn_arg(c); b = wn_roots(c); WN[name] = a
    check(f"wn({name}) = {a:+d}  (argument) = roots inside − pole order", a == b and mn > 0.05, f"min |f| on circle {mn:.3f}")
check("the eleven symbols cover winding numbers −2 … +3", set(WN.values()) == {-2, -1, 0, 1, 2, 3})

print("[3] Zois Prop. 1 on integer polynomial symbols: rank of T_f T_g − T_fg (exact)")
def mul(f, g):
    h = {}
    for a, x in f.items():
        for b, y in g.items(): h[a + b] = h.get(a + b, 0) + x * y
    return h
def rank(M):
    M = [[Fraction(x) for x in row] for row in M]; r = 0
    for c in range(len(M[0])):
        p = next((i for i in range(r, len(M)) if M[i][c] != 0), None)
        if p is None: continue
        M[r], M[p] = M[p], M[r]
        for i in range(len(M)):
            if i != r and M[i][c] != 0:
                q = M[i][c] / M[r][c]; M[i] = [a - q * b for a, b in zip(M[i], M[r])]
        r += 1
    return r
def defect(f, g, N):                       # (T_f T_g - T_fg) on e_0..e_{N-1}, the true infinite product
    L = N + max(max(g), 0) + max(-min(f), 0) + 2
    fg = mul(f, g)
    return [[sum(f.get(i - l, 0) * g.get(l - j, 0) for l in range(L)) - fg.get(i - j, 0) for j in range(N)] for i in range(N)]
PAIRS = [("z", "z⁻¹", {1: 1}, {-1: 1}), ("z⁻¹", "z", {-1: 1}, {1: 1}), ("z²", "z⁻²", {2: 1}, {-2: 1}),
         ("1 + z", "2 + z⁻¹", {0: 1, 1: 1}, {0: 2, -1: 1}), ("z⁻² + z", "3 + z²", {-2: 1, 1: 1}, {0: 3, 2: 1}),
         ("z⁻¹ − z", "z⁻¹ + z³", {-1: 1, 1: -1}, {-1: 1, 3: 1})]
RK = {}
for fn, gn, f, g in PAIRS:
    rs = [rank(defect(f, g, N)) for N in (12, 24, 36)]; RK[(fn, gn)] = rs[0]
    check(f"rank(T_[{fn}] T_[{gn}] − T_[fg]) = {rs[0]} at N = 12, 24, 36", len(set(rs)) == 1, str(rs))
check("T_z T_z⁻¹ − I has rank 1 and T_z⁻¹ T_z − I rank 0: ch 1's Sₖ∘Bₖ ≠ id and Bₖ∘Sₖ = id",
      RK[("z", "z⁻¹")] == 1 and RK[("z⁻¹", "z")] == 0)

print("[4] Ind T_f from N x N sections (numerical): kernel vs cokernel, told apart by where they live")
def ind(c, N=160):
    A = np.array([[c.get(i - j, 0) for j in range(N)] for i in range(N)], complex)
    U, s, Vh = np.linalg.svd(A); small = np.where(s < 1e-8 * s.max())[0]
    ker = sum(1 for i in small if (np.abs(Vh[i]) ** 2)[:N // 2].sum() > .5)   # near e_0: survives N -> inf
    cok = sum(1 for i in small if (np.abs(U[:, i]) ** 2)[:N // 2].sum() > .5)
    return ker, cok, len(small)
rows = []
for name, c in SYM:
    k, q, n = ind(c); rows.append((name, WN[name], k, q, k - q))
    check(f"T_[{name}]: {n} small singular values; ker {k}, coker {q}; index {k - q:+d} = −wn", k - q == -WN[name] and n == abs(WN[name]))

print("[5] Mathlib at the pinned revision")
man = json.loads((ROOT / "lake-manifest.json").read_text())
rev = next(p["rev"] for p in man["packages"] if p["name"] == "mathlib")
ML = ROOT / ".lake/packages/mathlib"
def gg(*pat): return subprocess.run(["git", "-C", str(ML), "grep", *pat, rev, "--", "Mathlib"],
                                   capture_output=True, text=True).stdout
check("the checkout is the manifest's revision",
      subprocess.run(["git", "-C", str(ML), "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip() == rev, rev[:12])
CENSUS = [("LinearMap.index (the algebraic index)", r"^public def index : ℤ", True),
          ("IsCompactOperator", r"^def IsCompactOperator", True),
          ("circleIntegral", r"def circleIntegral", True),
          ("a Fredholm operator (def / structure / class)", r"^(public )?(noncomputable )?(def|structure|class|abbrev) \S*[Ff]redholm", False),
          ("a winding number", r"[Ww]inding", False),
          ("a Hardy space H²", r"[Hh]ardy[ _]?[Ss]pace|HardySpace", False),
          ("a Toeplitz operator", r"[Tt]oeplitz[ _]?[Oo]perator|ToeplitzOp", False),
          ("the Calkin algebra", r"Calkin", False)]
for label, pat, want in CENSUS:
    hits = [l for l in gg("-En", pat).splitlines() if l]
    check(f"{'has' if want else 'lacks'} {label}", bool(hits) == want, f"{len(hits)} hits")
todo = gg("-n", "TODO: once mathlib has Fredholm operators")
check("Banach.lean: '-- TODO: once mathlib has Fredholm operators, generalise the next four lemmas accordingly'",
      "Mathlib/Analysis/Normed/Operator/Banach.lean" in todo, todo.split(":")[2] if todo else "")
toe = gg("-n", "Toeplitz")
check("the only 'Toeplitz' in Mathlib is the Hellinger–Toeplitz theorem (2 places)",
      len(toe.splitlines()) == 2 and toe.count("Hellinger--Toeplitz") == 2)

print("[HONESTY]")
print("  Noether (1921) IS held (updated 2026-09-28): [1c] above quotes it directly, by OCR, from the")
print("  Goettingen scan of Math. Ann. 82. Zois himself does not cite it -- his own theorem statement")
print("  ([1]) is quoted from his notes of Roe's 1995 lectures, whose proof is a sketch (homotopy to")
print("  z^m, then the shift), and that sketch is not verified against Noether's own 1921 argument.")
print("  [2] and [4] are floating point: [4] reads the index off N x N sections (N = 160) by where the")
print("  near-null singular vectors sit, which is an observation on eleven symbols, not a proof. [3]")
print("  is exact. [5] is a text search at the pinned revision; 'lacks' means no declaration matched")
print("  the pattern.")
print(f"\n{len(FAIL)} FAIL" + (": " + ", ".join(FAIL) if FAIL else ""))
sys.exit(1 if FAIL else 0)
