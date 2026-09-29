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
