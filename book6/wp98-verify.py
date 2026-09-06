#!/usr/bin/env python3
"""
wp98-verify.py — regenerates every corpus figure quoted in
Principia Orthogona, Book VI, WP-98, "A Measurement Science Without a Unit".

Repo rule: a published number must be regenerable by a tool. This paper's
argument is that a verification claim must carry the arguments it depends on,
so a paper making that argument with typed numbers would refute itself.

METHOD, and its limits. Every figure below is read out of the gate reports on
disk — the axioms.txt files that tools/verify-*/run.sh and
tools/leancheck.sh --audit write — and parsed by tools/axiom_gate.py, the same
allowlist the gates themselves use. Nothing here runs Lean. If a report is
stale, this script reproduces a stale number faithfully and cannot tell you so;
that is §4 of the paper, demonstrated on the paper.

Run:  python3 wp98-verify.py     (exits non-zero on any failure)
"""
import os, re, sys, glob, collections

GEOM = os.environ.get('GEOMETRY_ROOT', os.path.expanduser('~/Desktop/geometry'))
sys.path.insert(0, os.path.join(GEOM, 'tools'))
try:
    import axiom_gate as AG
except ImportError:
    sys.exit(f'tools/axiom_gate.py not found under {GEOM}. Set GEOMETRY_ROOT.')

FAIL = []


def check(label, got, want):
    ok = got == want
    print(("  OK   " if ok else "  FAIL ") + label + f"   got={got}  want={want}")
    if not ok:
        FAIL.append(label)


def roots():
    f = os.path.join(GEOM, 'tools', 'corpus_roots.txt')
    out = []
    for line in open(f, encoding='utf-8'):
        line = line.split('#')[0].strip()
        if line:
            out.append(os.path.expanduser(line))
    return out


SKIP = re.compile(r'(^|/)(_?to_delete|ml-evidence|\.lake)(/|$)')
SHAPES = ['tools/verify-*/axioms*.txt', 'tools/axioms*.txt',
          'tools/verify-audit/*/*.axioms.txt']


def tier1():
    """Distinct declarations with a kernel record, and their axiom profile.

    Allowlist, not a forbidden list — WP-73 §6. A declaration resting on
    anything outside the permitted three is counted as UNTRUSTED, never as
    audited, and a report line the gate cannot parse is a finding.
    """
    seen, profile, untrusted, unparsed, sources = {}, collections.Counter(), [], [], []
    allowed = set(AG.DEFAULT_ALLOWED)
    reports = []
    for r in roots():
        for shape in SHAPES:
            reports += glob.glob(os.path.join(r, shape))
    for rep in sorted(set(os.path.realpath(p) for p in reports)):
        if SKIP.search(rep):
            continue
        recs, unp = AG.parse(open(rep, encoding='utf-8', errors='replace').read())
        unparsed += [(rep, u) for u in unp]
        n = 0
        for name, ax in recs:
            if set(ax) <= allowed:
                if name not in seen:
                    seen[name] = rep
                    profile[tuple(sorted(ax)) or ('(none — axiom-free)',)] += 1
                n += 1
            else:
                untrusted.append((name, ax))
        if n:
            sources.append((os.path.relpath(rep, os.path.dirname(GEOM)), n))
    return seen, profile, untrusted, unparsed, sources


print("[1] Tier 1 — declarations with a kernel record, read from gate reports")
seen, profile, untrusted, unparsed, sources = tier1()
for path, n in sorted(sources, key=lambda s: -s[1]):
    print(f"       {n:4d}  {path}")
print()
check("distinct kernel-audited declarations", len(seen), 133 + 15)
check("declarations outside the permitted three", len(untrusted), 0)
check("report lines the gate could not parse", len(unparsed), 0)

print()
print("[2] Axiom profile — both output forms counted (WP-73 §6)")
for k, v in profile.most_common():
    print(f"       {v:4d}  {', '.join(k)}")
free = sum(v for k, v in profile.items() if k == ('(none — axiom-free)',))
# 11, corpus-wide. The paper first said 8, which is the geometry-only figure
# from tools/toolchain_ledger.py — a number carried from one scope to another
# without its scope. This script caught it, which is the paper's own argument
# arriving on the paper.
check("proofs resting on no axiom at all", free, 11)

print()
print("[3] The four classes caught in this corpus, 2026-09-05")
print("    Not recomputable — these are events, recorded in docs/audit-log.md.")
for c, what in [
    ("UNDERCOUNT",       "Tier 1 read 32 against a true 133; a glob missed vol1-proofs/tools/axioms.txt (82)"),
    ("NO EVIDENCE",      "leancheck.sh --audit wrote its probe to mktemp and rm -f'd it"),
    ("FORBIDDEN LIST",   "a grep for sorryAx in three separate places; the allowlist is two lines"),
    ("OVER-GENERALISED", "a published claim that was an artefact of choosing thirty sectors"),
]:
    print(f"       {c:18s} {what}")

print()
print("[4] The labour arithmetic of §8 — inputs stated, so the reader can move them")
POP = {  # approximate 2026 figures, millions; sources in §11
    'India': 1460, 'China': 1410,
    'United States': 342, 'European Union': 449, 'Japan': 123,
    'South Korea': 52, 'United Kingdom': 69,
}
IC = POP['India'] + POP['China']
BLOC = sum(POP[k] for k in ('United States', 'European Union', 'Japan',
                            'South Korea', 'United Kingdom'))
share = 0.30
trained = IC * share
print(f"       India + China                     {IC:,.0f} M")
print(f"       US + EU + Japan + Korea + UK      {BLOC:,.0f} M")
print(f"       30% of India + China              {trained:,.0f} M")
print(f"       as a fraction of the whole bloc   {trained / BLOC:.0%}")
check("30% of India+China exceeds the bloc's entire population", trained > BLOC, False)
check("fraction of the bloc's TOTAL population needed to match, rounded",
      round(trained / BLOC * 100), 83)
print("       Note: 30% of a total population holding a CS education exceeds total")
print("       tertiary attainment in every country that exists. This is a ratio, not")
print("       a forecast, and §8 says so.")

print()
if FAIL:
    print(f"FAILED: {len(FAIL)}")
    for f in FAIL:
        print("  -", f)
    raise SystemExit(1)
print("every corpus figure in WP-98 regenerated from reports on disk.")
