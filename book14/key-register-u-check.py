#!/usr/bin/env python3
"""Key Register follow-up (HANDOFF item 4, 2026-09-29): what the pages behind the three
extra U glosses actually say. Reuses tools/key_register.py's own page set, gloss regex and
Omega test, so the counts are the register's, not a re-implementation. Read-only."""
import importlib.util, os, re
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sp = importlib.util.spec_from_file_location('kr', os.path.join(ROOT, 'tools', 'key_register.py'))
kr = importlib.util.module_from_spec(sp); sp.loader.exec_module(kr)
T = {f: kr.text(f) for f in kr.pages()}
omega = {f for f, t in T.items() if all(w.search(t) for w in kr.OMEGA_WORDS)}
rx = re.compile(r'(?<![A-Za-z0-9_])U\s*(?:—|–|-|=|:|\()\s*(?i:the\s+|a\s+|o\s+)?([A-Za-zçãõéêíóúàÀ-Ú]+)')
print(f"page set: {len(T)} pages; Omega-test pages (name Genesis and Logos): {len(omega)}")
use = {s: set() for s in kr.SENSES['U']}
for s, ws in kr.SENSES['U'].items():
    for f, t in T.items():
        if any(m.group(1).lower() in ws for m in rx.finditer(t)):
            use[s].add(f)
for s, fs in use.items():
    o = sorted(f for f in fs if f in omega)
    print(f"{s}: {len(fs)} pages; on Omega-test pages: {len(o)}; not: {sorted(fs - omega)}")
both = lambda a, b: sorted(use[a] & use[b])
print("pages using unfolding AND universal:", both('unfolding', 'universal'))
print("pages using unfolding AND unification:", both('unfolding', 'unification'))
print("pages using unfolding AND union:", both('unfolding', 'union'))
print("pages using union AND (C/K/F compression/threshold/fold) key words in the same U-gloss page:",
      [f for f in sorted(use['union']) if re.search(r'\bC\s*[—:=]\s*compress', T[f])])

# ---- part 2 (2026-09-29): where the series itself DEFINES U. Read the definitions, not just the glosses.
import zipfile
print("\n[part 2] definitions of U inside the corpus")
vol1 = kr.text('book1/vol1-mathematics.html')
m = re.search(r'Definition 3\.4\s*·\s*Unfolding Operator.{0,200}', vol1)
print("Vol I (book1/vol1-mathematics.html) Def 3.4:", m.group(0)[:150] if m else 'NOT FOUND')
gcm = kr.text('gcm-framework.html')
m1 = re.search(r'Unfolding U:.{0,90}', gcm); m2 = re.search(r'Definition 3\.1 — Unification Operator.{0,300}', gcm)
print("gcm-framework.html table row:", m1.group(0) if m1 else 'NOT FOUND')
print("gcm-framework.html Def 3.1  :", m2.group(0)[:230] if m2 else 'NOT FOUND')
print("  same page also says:", re.search(r'the U-operator is the unification map[^.]*', gcm).group(0))
om = kr.text('omega/ch-fourfold.html'); m3 = re.search(r'Definition 5\.4 — Union.{0,140}', om)
print("omega/ch-fourfold.html Def 5.4:", m3.group(0) if m3 else 'NOT FOUND')
g_t = re.search(r'\\tau_\{12\}\s*=.{0,75}', gcm); o_t = re.search(r'τ₁₂\s*=\s*√.{0,32}', om)
print("  tau12, GCM page  :", g_t.group(0) if g_t else 'NOT FOUND')
print("  tau12, Omega page:", o_t.group(0) if o_t else 'NOT FOUND')
p = os.path.expanduser('~/Downloads/GCM-Institutional-Edition.docx')
if not os.path.exists(p): p = os.path.expanduser('~/mnt/Downloads/GCM-Institutional-Edition.docx')
if os.path.exists(p):
    x = zipfile.ZipFile(p).read('word/document.xml').decode('utf8')
    P = [re.sub(r'<[^>]+>', '', q).strip() for q in x.split('</w:p>')]; P = [q for q in P if q]
    a = max(i for i, q in enumerate(P) if 'Appendix A: Unified Lexicon' in q)
    for i in range(a, a + 60):
        if re.match(r'(Metric|Lie derivative|Reeb|Unfolding|Boundary) ', P[i]):
            print(f"  Institutional Ed. App. A: {P[i]} -> {P[i+2][:110]}")
else:
    print("  GCM-Institutional-Edition.docx not found: SKIP")
prel = kr.text('prelude.html'); m = re.search(r'\(a\) The operators:.{0,330}', prel)
print("prelude.html (Book 3) audit note:", m.group(0) if m else 'NOT FOUND')
print("Book 3 'residue/hysteresis' reading of U:", [f for f in sorted(T) if re.search(r'\bU\s*(?:\(residue|—\s*when the driver is reversed)', T[f])])
print("Book 3 'scale' reading of U:", [f for f in sorted(T) if re.search(r'\bU\s*(?:\(Scale\)|=\s*the scale-invariant|—\s*the recognition of the same structure)', T[f])])

# ---- part 3 (2026-09-29): the founding papers. Vol I, Vol II, dm3 Operator = author's Downloads copies (matched to
# Zenodo 19117400 by filename and byte size only); the GCM paper = its web edition gcm-framework.html (DOI ...20230610).
import glob, hashlib, subprocess
def pdf(pattern):
    for d in (os.path.expanduser('~/Downloads'), os.path.expanduser('~/mnt/Downloads')):
        for f in sorted(glob.glob(os.path.join(d, pattern))):
            return ' '.join(subprocess.run(['pdftotext', f, '-'], capture_output=True, text=True).stdout.split()), hashlib.md5(open(f, 'rb').read()).hexdigest()
    return None, None
print("\n[part 3] founding papers (Zenodo v1 bundle 10.5281/zenodo.19117400; md5s as listed on zenodo.org/records/20230610, 2026-09-29)")
for label, pat, md5, needles in [
    ("Vol I", "Principia Orthogona Volume One-*Nogueira Grossi 2026*.pdf", "e7390cd722654fc680c8cba4f5462e7a",
     ["Definition 3.4 (Unfolding Map). The unfolding operator U", "Gradient flow to Γsyn via U3",
      "The full dm3 grammar g → L → R → U extends this sequence by adding multi-orbit coherence, resonance detection, and categorical unification"]),
    ("Vol II", "Principia Orthogona Volume Two Grossi2026*.pdf", "53431c95f5dfe549ab07869276a929e1",
     ["Gradient flow to Γ via U3", "Every operator (g-, L-, R-, U -, B-operators)"]),
    ("dm3 Operator", "THE DM3 OPERATOR- EXPLICIT TOY MODEL*GLOBAL DYNAMICAL ANALYSIS*.pdf", "f0037d1068b11cc9f31b3d43c7b57eb4",
     ["3.4.1. U1 : pushout. Unified state space", "3.4.2. U2 : translation", "3.4.3. U3 : synthesis", "τ12 = min(τ1 , τ2 )"]),
    ("GCM paper", "GENERATIVE CONTACT MECHANICS-*STRUCTURED LIMIT CYCLES*.pdf", "bea3bf9092305c692cf0d3e9cdb0cbf3",
     ["4.4. U -operators: unification", "Definition 4.27 (U1, U2, U3)", "U3 = exp(−∇dg(·, Γsyn)2)", "τ12 ≤ min(τi)"])]:
    t, h = pdf(pat)
    if t is None:
        print(f"{label}: not in ~/Downloads: SKIP (Zenodo md5 {md5}). Read only in the Zenodo viewer on 2026-09-29, NOT script-verified.")
        continue
    print(f"{label}: md5 {'MATCHES Zenodo' if h == md5 else 'DIFFERS from Zenodo (' + h + ')'}")
    for n in needles: print(f"   {'FOUND  ' if n in t else 'MISSING'} {n}")
    if label == "Vol I": print("   'universal' as an operator name (U — Universal / U: universal):", bool(re.search(r'U\s*[—:-]\s*[Uu]niversal', t)))
m = re.search(r'Theorem B · Unification and Noise Tolerance.{0,330}', gcm)
print("GCM web edition Theorem B:", m.group(0)[:330] if m else 'NOT FOUND')
print("GCM web edition Theorem D lists the algebra as:", (re.search(r'operator algebra \\\(\(([^)]*)\)', gcm) or [None, 'NOT FOUND'])[1] if False else re.search(r'dm³ operator algebra \\\(\(G, U, F, K, C\)\\\)', gcm) is not None)
print("GCM web edition DOI on page:", sorted(set(re.findall(r'10\.5281/zenodo\.\d+', gcm)))[:6])
