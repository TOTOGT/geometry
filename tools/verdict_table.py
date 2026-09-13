#!/usr/bin/env python3
"""Rung 2 of the reduction ladder (docs/verification-checklist.md).

Reads a verify-audit day directory and emits ONE ROW PER FILE, fixed fields,
no prose. Reads only artifacts already on disk; never invokes Lean.

    python3 tools/verdict_table.py [--day YYYY-MM-DD] [--out PATH]

Verdict set is CLOSED. An open set is prose again.
"""
import argparse, hashlib, os, re, sys, datetime

PERMITTED = {"propext", "Classical.choice", "Quot.sound"}
NON_KERNEL = {"Lean.ofReduceBool", "Lean.trustCompiler"}

DECL_RE  = re.compile(r"^'(?P<name>.+?)' (?:depends on axioms: \[(?P<ax>.*)\]|does not depend on any axioms)\s*$")
# Incumbent convention, already in the corpus:
#   -- EXPECTED under `--audit`:  18 declarations, 0 trusting sorryAx
# Preferred extension, because counts cannot catch a swap (one closed, one opened):
#   -- GATE-DECLARE: sorries = name_a, name_b      (or `none`)
DECLARE_RE  = re.compile(r"GATE-DECLARE:\s*sorries\s*=\s*(?P<v>.+?)\s*$", re.M)
EXPECTED_RE = re.compile(r"EXPECTED under.{0,20}?:\s*(?P<d>\d+)\s+declarations,\s*(?P<s>\d+)\s+trusting\s+sorryAx")

FIELDS = ["project","path","sha256","toolchain","verdict",
          "declared_sorries","actual_sorries","declarations","expected_decls","scope","note"]

MAPS = []           # (from, to) prefix remaps, so a desk-absolute path resolves on any host
SEARCH_ROOTS = []   # used only when the day directory has no order.txt


def localise(p):
    for a, b in MAPS:
        if p.startswith(a):
            return b + p[len(a):]
    return p


def sha12(p):
    try:
        h = hashlib.sha256()
        with open(p, "rb") as fh:
            for b in iter(lambda: fh.read(1 << 16), b""):
                h.update(b)
        return h.hexdigest()[:12]
    except OSError:
        return "-"


def toolchain_of(p):
    d = os.path.dirname(os.path.abspath(p))
    while d and d != "/":
        t = os.path.join(d, "lean-toolchain")
        if os.path.isfile(t):
            try:
                return open(t).read().strip().replace("leanprover/lean4:", ""), os.path.basename(d)
            except OSError:
                break
        d = os.path.dirname(d)
    return "-", "-"


def declaration_of(src):
    """What the file says about itself. Absence is its own verdict, never a guess.

    Returns (named_set_or_None, expected_sorry_count_or_None, expected_decls_or_None).
    """
    try:
        txt = open(src, encoding="utf-8", errors="replace").read()
    except OSError:
        return None, None, None
    named = None
    m = DECLARE_RE.search(txt)
    if m:
        v = m.group("v").strip()
        named = set() if v.lower() in ("none", "-", "()") else {
            x.strip() for x in re.split(r"[,\s]+", v) if x.strip()}
    nsorry = ndecl = None
    e = EXPECTED_RE.search(txt)
    if e:
        ndecl, nsorry = int(e.group("d")), int(e.group("s"))
    return named, nsorry, ndecl


def parse_axioms(path):
    decls, sorry_decls, violators, bad, nonkernel = {}, set(), set(), [], set()
    # `#print axioms` wraps a long axiom list across lines; rejoin before parsing.
    joined, buf = [], None
    for raw in open(path, encoding="utf-8", errors="replace"):
        raw = raw.rstrip("\n")
        if buf is not None:
            buf += " " + raw.strip()
            if "]" in raw:
                joined.append(buf); buf = None
            continue
        if not raw.lstrip().startswith("'"):
            continue          # elaborator noise, not a declaration report
        t = raw.strip()
        if "[" in t and "]" not in t:
            buf = t
        else:
            joined.append(t)
    if buf is not None:
        joined.append(buf)

    for line in joined:
        m = DECL_RE.match(line)
        if not m:
            bad.append(line[:70]); continue
        name = m.group("name")
        ax = {a.strip() for a in (m.group("ax") or "").split(",") if a.strip()}
        decls[name] = ax
        if "sorryAx" in ax:
            sorry_decls.add(name)
        nonkernel |= (ax & NON_KERNEL)
        out = ax - PERMITTED - {"sorryAx"} - NON_KERNEL
        if out:
            violators |= out
    return decls, sorry_decls, violators, bad, nonkernel


def slug_to_path(day_dir):
    """order.txt carries the full path each slug came from."""
    mapping, order = {}, os.path.join(day_dir, "order.txt")
    if not os.path.isfile(order):
        return mapping
    for line in open(order, encoding="utf-8", errors="replace"):
        line = line.strip()
        if not line or "UNREADABLE" in line:
            continue
        p = line.split("\t")[-1].strip()
        if not p.endswith(".lean"):
            continue
        stem = os.path.basename(p)[:-5]
        mapping.setdefault(stem, []).append(p)
    return mapping


def scan_fallback(stem, search_roots):
    """No order.txt (a targeted leancheck run writes none): find the stem on disk."""
    hits = []
    for root in search_roots:
        if not os.path.isdir(root):
            continue
        for dirpath, dirnames, filenames in os.walk(root):
            dirnames[:] = [d for d in dirnames
                           if d not in (".lake", ".git", "_to_delete", "node_modules")]
            if stem + ".lean" in filenames:
                hits.append(os.path.join(dirpath, stem + ".lean"))
    return hits


def resolve(slug, mapping):
    """Slug is either <stem> (old) or <project>__<stem> (new)."""
    proj = None
    stem = slug
    if "__" in slug:
        proj, stem = slug.split("__", 1)
    cands = [localise(c) for c in mapping.get(stem, [])]
    if not cands:
        cands = scan_fallback(stem, SEARCH_ROOTS)
        if proj:
            narrowed = [c for c in cands if ("/%s/" % proj) in c or
                        os.path.basename(os.path.dirname(c)) == proj]
            if narrowed:
                cands = narrowed
    if proj:
        narrowed = [c for c in cands if ("/%s/" % proj) in c]
        if narrowed:
            cands = narrowed
    if len(cands) == 1:
        return cands[0], ""
    if not cands:
        return "", "no path in order.txt"
    return cands[0], "AMBIGUOUS: %d copies share this name" % len(cands)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--day", default=datetime.date.today().isoformat())
    ap.add_argument("--root", default="tools/verify-audit")
    ap.add_argument("--out", default=None)
    ap.add_argument("--map", action="append", default=[],
                    help="FROM=TO path prefix remap; repeatable")
    a = ap.parse_args()

    for m in a.map:
        f, _, t = m.partition("=")
        if f and t:
            MAPS.append((f, t))
    auto = os.path.join(os.path.expanduser("~"), "mnt", "Desktop")
    if not MAPS and os.path.isdir(auto):
        MAPS.append(("/Users/pablogrossi/Desktop", auto))

    base = MAPS[0][1] if MAPS else os.path.dirname(os.path.abspath("."))
    for d in ("geometry", "GTCT", "AXLE"):
        SEARCH_ROOTS.append(os.path.join(base, d))

    day_dir = os.path.join(a.root, a.day)
    if not os.path.isdir(day_dir):
        sys.exit("no such day directory: %s" % day_dir)

    mapping = slug_to_path(day_dir)
    scope = "corpus" if os.path.isfile(os.path.join(day_dir, "order.txt")) else "targeted"
    rows = []
    for fn in sorted(os.listdir(day_dir)):
        if not fn.endswith(".axioms.txt"):
            continue
        slug = fn[:-len(".axioms.txt")]
        src, note = resolve(slug, mapping)
        decls, sorries, violators, bad, nonkernel = parse_axioms(os.path.join(day_dir, fn))
        named, exp_sorry, exp_decls = declaration_of(src) if src else (None, None, None)
        declared = named
        if declared is None and exp_sorry is not None:
            declared = "count:%d" % exp_sorry
        tc, proj = toolchain_of(src) if src else ("-", "-")

        def add(n):
            return (note + "; " if note else "") + n

        if bad:
            verdict = "PARSE-ERROR"; note = add("unreadable declaration line: " + bad[0])
        elif violators:
            verdict = "AXIOM-VIOLATION"; note = add("outside permitted: " + ",".join(sorted(violators)))
        elif exp_decls is not None and exp_decls != len(decls):
            verdict = "COUNT-MISMATCH"
            note = add("file expects %d declarations, report has %d" % (exp_decls, len(decls)))
        elif not sorries:
            verdict = "PASS"
        elif named is None and exp_sorry is None:
            verdict = "UNDECLARED-STATUS"
            note = add("no GATE-DECLARE line; add one naming its open obligations")
        elif named is not None:
            if named == sorries:
                verdict = "PASS-AS-DECLARED"
            elif sorries - named:
                verdict = "UNDECLARED-SORRY"; note = add("not declared: " + ",".join(sorted(sorries - named)))
            else:
                verdict = "DECLARED-MISMATCH"; note = add("declared but absent: " + ",".join(sorted(named - sorries)))
        elif exp_sorry == len(sorries):
            verdict = "PASS-AS-DECLARED"
            note = add("declared by count only; a swap would not be caught - prefer GATE-DECLARE")
        else:
            verdict = "UNDECLARED-SORRY"
            note = add("file expects %d admitted, report has %d" % (exp_sorry, len(sorries)))

        if nonkernel and verdict in ("PASS", "PASS-AS-DECLARED"):
            note = (note + "; " if note else "") + "NOT a kernel check: " + ",".join(sorted(nonkernel))

        rows.append({
            "project": proj, "path": src or ("?" + slug), "sha256": sha12(src) if src else "-",
            "toolchain": tc, "verdict": verdict,
            "declared_sorries": ("-" if declared is None else
                                 declared if isinstance(declared, str) else str(len(declared))),
            "actual_sorries": str(len(sorries)), "declarations": str(len(decls)),
            "expected_decls": "-" if exp_decls is None else str(exp_decls),
            "scope": scope,
            "note": note or "-",
        })

    out = a.out or os.path.join(day_dir, "verdicts.tsv")
    with open(out, "w", encoding="utf-8") as fh:
        fh.write("\t".join(FIELDS) + "\n")
        for r in rows:
            fh.write("\t".join(r[k] for k in FIELDS) + "\n")
    print("%s: %d rows" % (out, len(rows)))


if __name__ == "__main__":
    main()
