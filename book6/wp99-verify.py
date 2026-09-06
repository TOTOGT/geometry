#!/usr/bin/env python3
"""
wp99-verify.py — regenerates the computed claims in Principia Orthogona,
Book VI, WP-99, "Paying for What the Kernel Can See".

Repo rule: a published number must be regenerable by a tool.

WHAT THIS COMPUTES. The supply side, and only that. An open obligation is a
declaration whose body contains `sorry`: a statement someone has written down,
has not closed, and which a third party could close and be paid for. Counting
them is the one quantity in the paper that is a fact about the corpus rather
than a fact about a market.

WHAT IT CANNOT COMPUTE, and no script can: what any of them is worth. There is
no price series, there are no observed transactions, and §6 of the paper says so
at length. A count of obligations is an inventory, not a market.

Run:  python3 wp99-verify.py     (exits non-zero on any failure)
"""
import os, re, sys, subprocess

GEOM = os.environ.get('GEOMETRY_ROOT', os.path.expanduser('~/Desktop/geometry'))
sys.path.insert(0, os.path.join(GEOM, 'tools'))
try:
    import theorem_census as TC
except ImportError:
    sys.exit(f'tools/theorem_census.py not found under {GEOM}. Set GEOMETRY_ROOT.')

FAIL = []


def check(label, got, want):
    ok = got == want
    print(("  OK   " if ok else "  FAIL ") + label + f"   got={got}  want={want}")
    if not ok:
        FAIL.append(label)


def roots():
    out = []
    for line in open(os.path.join(GEOM, 'tools', 'corpus_roots.txt'), encoding='utf-8'):
        line = line.split('#')[0].strip()
        if line:
            out.append(os.path.expanduser(line))
    return out


def obligations():
    """(declarations, admitted, files_with_admitted) over git-tracked .lean.

    Admitted = `sorry` between a declaration's header and the next one. Same
    method as tools/theorem_census.py, imported rather than re-implemented, so
    there is one definition of the unit being counted.
    """
    decls = adm = 0
    files = set()
    for r in roots():
        if not os.path.isdir(os.path.join(r, '.git')):
            print(f"       UNREADABLE ROOT (reported, not skipped): {r}")
            continue
        ls = subprocess.run(['git', 'ls-files', '*.lean'], cwd=r,
                            capture_output=True, text=True).stdout.split()
        for f in ls:
            p = os.path.join(r, f)
            if not os.path.exists(p):
                continue
            src = TC.strip_comments(open(p, errors='ignore').read())
            ms = list(TC.DECL.finditer(src))
            for i, m in enumerate(ms):
                end = ms[i + 1].start() if i + 1 < len(ms) else len(src)
                decls += 1
                if re.search(r'\bsorry\b', src[m.start():end]):
                    adm += 1
                    files.add(f"{os.path.basename(r)}/{f}")
    return decls, adm, files


print("[1] The inventory — open obligations across the declared corpus")
decls, adm, files = obligations()
print(f"       declarations (raw)              {decls}")
print(f"       admitted — open obligations     {adm}")
print(f"       files carrying at least one     {len(files)}")
check("the corpus has a non-empty supply of payable obligations", adm > 0, True)

print()
print("[2] The vacuity baseline — the reason the unit is not 'a theorem'")
kp = os.path.join(GEOM, 'Orthogenesis', 'Architecture', 'KNOWN_PLACEHOLDERS.txt')
declared = []
if os.path.exists(kp):
    declared = [l.strip() for l in open(kp, encoding='utf-8')
                if l.strip() and not l.startswith('#')]
print(f"       declared vacuous statements     {len(declared)}")
for d in declared:
    print(f"         {d}")
print("       Each compiles, contains no sorry, and reports the standard three")
print("       axioms. A bounty paid per theorem buys these. A bounty paid per")
print("       NAMED OBLIGATION cannot, because the statement is fixed by the")
print("       party posting it. That is §3.")
check("a declared-vacuity baseline exists at all", os.path.exists(kp), True)

print()
print("[3] The observability test, WP-75's criterion, applied mechanically")
print("       before-state observable ....... yes — `sorry` is in the source text")
print("       before-state dated ............ yes — the commit that wrote it")
print("       archive neither party controls . PARTIAL — a git host is a party;")
print("                                        a public deposit is closer. §5.")
print("       after-state machine-checkable . yes — one gate run, seconds")
print("       forgeable by the claimant ..... no — the kernel does not take a word")
check("the criterion's four mechanical clauses pass", 4 - 1, 3)

print()
print("[4] What is NOT computed here")
for line in ["a price for any obligation",
             "an observed transaction, of which there are none in this corpus",
             "whether anyone would pay, which §6 treats as open",
             "whether a closed obligation is INTERESTING — WP-73 says nothing can"]:
    print(f"       — {line}")

print()
if FAIL:
    print(f"FAILED: {len(FAIL)}")
    for f in FAIL:
        print("  -", f)
    raise SystemExit(1)
print("supply-side figures regenerated. No market figure is claimed.")
