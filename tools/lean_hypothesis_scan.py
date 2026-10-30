#!/usr/bin/env python3
"""List, per Lean theorem, its hypotheses next to its conclusion, with R20 flags.

CLAUDE.md R20 names this as the instrument that did not exist: a clean `#print axioms` report does
not show that a theorem proves what its name says, and the failure modes below pass every gate the
corpus owns. This is a HEURISTIC text scan (no Lean needed). A flag is a reason to read the theorem,
not a verdict, and absence of a flag is not evidence the theorem is good.

Usage:  python3 tools/lean_hypothesis_scan.py FILE.lean [FILE2.lean ...]  [--all]   (--all lists unflagged too)

Flags
  SORRY        a `sorry` token in code (comments stripped)
  AXIOM        an `axiom` declaration (the conclusion is assumed)
  NATIVE       native_decide (adds a compiler axiom)
  BEGS         hypothesis text appears in the conclusion, or the proof is just `exact h` / `h` / `assumption`
               (the R20 shape: implication proved, antecedent not)
  NUMERALS     no binders and the conclusion mentions no identifiers except numerals and standard
               functions: it is arithmetic on constants, whatever the name says
  TRIVIAL      conclusion is True, a = a, P → P, or `∃ f, f x = e` closed by rfl
  NAME_EXCEEDS name contains a structural word (converge, unique, bijection, attractor, principle,
               stable, chaos, fold, lyapunov, theorem ...) AND the theorem carries NUMERALS or TRIVIAL
"""
import re, sys

STRUCT = re.compile(r"(converg|unique|bijec|attract|principle|stable|stabil|chaos|fold|lyapunov|"
                    r"catastroph|disaster|resolv|contract|embed|isomorph|equivalen|classif|exist|"
                    r"theorem|law|ladder|boundary|critical)", re.I)
STD = {"Real","exp","sqrt","log","sin","cos","abs","norm_num","Nat","Int","ℝ","ℕ","ℤ","ℚ","pi","π","Complex"}

def strip_comments(s):
    # remove block comments (including docstrings) and line comments; keep line structure
    out = []; i = 0; depth = 0; n = len(s)
    while i < n:
        if s.startswith("/-", i):
            depth += 1; i += 2; continue
        if depth and s.startswith("-/", i):
            depth -= 1; i += 2; continue
        if depth:
            out.append("\n" if s[i] == "\n" else " "); i += 1; continue
        if s.startswith("--", i):
            while i < n and s[i] != "\n": i += 1
            continue
        out.append(s[i]); i += 1
    return "".join(out)

def docstrings(s):
    d = {}
    for m in re.finditer(r"/--(.*?)-/\s*((?:@\[[^\]]*\]\s*)*(?:private\s+|protected\s+|noncomputable\s+)*(?:theorem|lemma|def|axiom)\s+(\S+))", s, re.S):
        d[m.group(3)] = " ".join(m.group(1).split())
    return d

DECL = re.compile(r"^(?:@\[[^\]]*\]\s*)*(?:private\s+|protected\s+|noncomputable\s+)*(theorem|lemma|axiom|def)\s+(\S+)", re.M)

def split_header(text):
    """text starts after the name. return (binders, conclusion, proof)."""
    depth = 0; i = 0; n = len(text)
    pairs = {"(": ")", "{": "}", "[": "]", "⟨": "⟩"}
    close = set(pairs.values()); stack = []
    colon = None
    while i < n:
        c = text[i]
        if c in pairs: stack.append(c)
        elif c in close and stack: stack.pop()
        elif c == ":" and not stack and text[i:i+2] != ":=":
            colon = i; break
        i += 1
    if colon is None: return text, "", ""
    binders = text[:colon]
    rest = text[colon+1:]
    j = rest.find(":=")
    if j < 0: return binders, rest, ""
    return binders, rest[:j], rest[j+2:]

def norm(x): return " ".join(x.split())

def analyze(path, show_all):
    raw = open(path, encoding="utf-8").read()
    docs = docstrings(raw)
    code = strip_comments(raw)
    heads = list(DECL.finditer(code))
    rows = []
    for k, m in enumerate(heads):
        kind, name = m.group(1), m.group(2)
        end = heads[k+1].start() if k+1 < len(heads) else len(code)
        body = code[m.end():end]
        flags = []
        if kind == "axiom": flags.append("AXIOM")
        if re.search(r"\bsorry\b", body): flags.append("SORRY")
        if "native_decide" in body: flags.append("NATIVE")
        if kind == "def":
            if flags: rows.append((name, kind, "", "", flags, docs.get(name, "")))
            continue
        binders, concl, proof = split_header(body)
        c = norm(concl); p = norm(proof)
        hyps = re.findall(r"\(\s*(h\w*)\s*:\s*([^()]*(?:\([^()]*\)[^()]*)*)\)", binders)
        hyp_txt = [(a, norm(b)) for a, b in hyps]
        premises = [norm(x) for x in re.split(r"→", c)[:-1]] if "→" in c else []
        # BEGS
        names = [a for a, _ in hyp_txt]
        short = re.sub(r"^by\s+", "", p)
        if names and (short in names or re.fullmatch(r"(exact|assumption|simpa using)\s*(" + "|".join(map(re.escape, names)) + r")?", short or "")):
            flags.append("BEGS")
        for _, t in hyp_txt:
            if len(t) > 6 and t in c:
                flags.append("BEGS"); break
        # numerals / trivial
        idents = set(re.findall(r"[A-Za-zα-ωΑ-Ω_][\w.']*", re.sub(r"\b\d+(\.\d+)?\b", "", c)))
        idents -= STD
        idents = {x for x in idents if x not in ("by","fun","at","in","then","else","if","and","or","not","true","false")}
        if not hyp_txt and not re.search(r"[∀∃]|fun ", c) and not idents and c:
            flags.append("NUMERALS")
        if re.fullmatch(r"True|⊤", c) or re.fullmatch(r"(.+?)\s*=\s*\1", c):
            flags.append("TRIVIAL")
        if re.search(r"∃\s*\w+\s*(?::[^,]*)?,\s*\w+\s+\w+\s*=", c) and re.search(r"rfl", p):
            flags.append("TRIVIAL")
        if premises and any(pr == norm(concl.split("→")[-1]) for pr in premises):
            flags.append("TRIVIAL")
        if ("NUMERALS" in flags or "TRIVIAL" in flags) and STRUCT.search(name) :
            flags.append("NAME_EXCEEDS")
        if flags or show_all:
            rows.append((name, kind, "; ".join(f"{a}: {b}" for a, b in hyp_txt)[:140], c[:170], sorted(set(flags)), docs.get(name, "")))
    return rows, len([h for h in heads if h.group(1) in ("theorem","lemma")])

if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    show_all = "--all" in sys.argv
    tot = 0; flagged = 0
    for path in args:
        rows, nthm = analyze(path, show_all)
        tot += nthm
        fl = [r for r in rows if r[4]]
        flagged += len(fl)
        print(f"\n## {path}  — {nthm} theorem/lemma declarations, {len(fl)} flagged")
        for name, kind, hy, c, flags, doc in rows:
            tag = ",".join(flags) if flags else "-"
            print(f"- `{name}` [{tag}]")
            if hy: print(f"    hyps: {hy}")
            if c: print(f"    concl: {c}")
            if doc and flags: print(f"    doc: {doc[:150]}")
    print(f"\nTOTAL: {tot} theorems/lemmas scanned, {flagged} flagged. Heuristic scan: read flagged theorems; unflagged is not verified.")
