#!/usr/bin/env python3
"""Rung 3 of the reduction ladder (docs/verification-checklist.md).

A run's information content is its DELTA. A file that passed yesterday and passes
today contributes nothing and is not printed. Output is bounded; if it would grow
with the corpus, that is the bug.

Order is load-bearing: counts first, delta second, the decision LAST, because that
is where attention lands.

    python3 tools/verdict_summary.py [--day YYYY-MM-DD] [--against YYYY-MM-DD]
"""
import argparse, os, sys, datetime

ROOT = "tools/verify-audit"
GOOD = {"PASS", "PASS-AS-DECLARED"}
MAX_LISTED = 6


def load(day):
    p = os.path.join(ROOT, day, "verdicts.tsv")
    if not os.path.isfile(p):
        return None
    rows, head = {}, None
    for i, line in enumerate(open(p, encoding="utf-8")):
        f = line.rstrip("\n").split("\t")
        if i == 0:
            head = f; continue
        r = dict(zip(head, f))
        rows[r["path"]] = r
    return rows


def previous(day):
    days = sorted(d for d in os.listdir(ROOT)
                  if os.path.isfile(os.path.join(ROOT, d, "verdicts.tsv")) and d < day)
    return days[-1] if days else None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--day", default=datetime.date.today().isoformat())
    ap.add_argument("--against", default=None)
    a = ap.parse_args()

    now = load(a.day)
    if now is None:
        sys.exit("no verdicts.tsv for %s - run tools/verdict_table.py first" % a.day)
    base_day = a.against or previous(a.day)
    was = load(base_day) if base_day else None

    counts = {}
    for r in now.values():
        counts[r["verdict"]] = counts.get(r["verdict"], 0) + 1
    order = sorted(counts.items(), key=lambda kv: (kv[0] in GOOD, -kv[1]))

    out = []
    out.append("%s - %d files" % (a.day, len(now)))
    out.append("  " + "   ".join("%d %s" % (n, v) for v, n in order))

    # --- delta
    out.append("")
    if was is None:
        out.append("changed: no earlier table to compare against (%s is the baseline)" % a.day)
    else:
        new_bad, fixed, moved, appeared = [], [], [], []
        for p, r in now.items():
            o = was.get(p)
            if o is None:
                if r["verdict"] not in GOOD:
                    appeared.append(r)
                continue
            if o["verdict"] == r["verdict"] and o["sha256"] == r["sha256"]:
                continue
            if r["verdict"] not in GOOD and o["verdict"] in GOOD:
                new_bad.append((o, r))
            elif r["verdict"] in GOOD and o["verdict"] not in GOOD:
                fixed.append((o, r))
            else:
                moved.append((o, r))
        # A targeted run is not a shrunken corpus run. Comparing the two and
        # announcing "44 files dropped" is a true count under a false sentence.
        targeted = any(r.get("scope") == "targeted" for r in now.values())
        gone = [] if targeted else [p for p in was if p not in now]
        if targeted:
            out.append("targeted run: %d file(s); the other %d in %s were not re-checked"
                       % (len(now), max(0, len(was) - len(now)), base_day))

        if not (new_bad or fixed or moved or appeared or gone):
            out.append("changed since %s: nothing" % base_day)
        else:
            out.append("changed since %s:" % base_day)
            for label, items in (("REGRESSED", new_bad), ("fixed", fixed),
                                 ("moved", moved)):
                for o, r in items[:MAX_LISTED]:
                    out.append("  %-9s %s: %s -> %s" %
                               (label, os.path.basename(r["path"]), o["verdict"], r["verdict"]))
                if len(items) > MAX_LISTED:
                    out.append("  %-9s ... and %d more" % (label, len(items) - MAX_LISTED))
            for r in appeared[:MAX_LISTED]:
                out.append("  new       %s: %s" % (os.path.basename(r["path"]), r["verdict"]))
            if gone:
                out.append("  dropped   %d file(s) no longer in the table" % len(gone))

    # --- the decision, last
    out.append("")
    undeclared = [r for r in now.values() if r["verdict"] == "UNDECLARED-SORRY"]
    nostatus = [r for r in now.values() if r["verdict"] == "UNDECLARED-STATUS"]
    broken = [r for r in now.values()
              if r["verdict"] in ("AXIOM-VIOLATION", "PARSE-ERROR", "COUNT-MISMATCH",
                                  "DECLARED-MISMATCH")]
    if undeclared:
        out.append("DECIDE: %d file(s) admit a theorem nobody declared -" % len(undeclared))
        for r in undeclared[:MAX_LISTED]:
            out.append("        %s  %s" % (os.path.basename(r["path"]), r["note"][:80]))
    elif broken:
        out.append("DECIDE: %d file(s) the gate could not settle -" % len(broken))
        for r in broken[:MAX_LISTED]:
            out.append("        %-16s %s  %s" %
                       (r["verdict"], os.path.basename(r["path"]), r["note"][:60]))
    elif nostatus:
        out.append("DECIDE: %d file(s) admit theorems without a GATE-DECLARE line, so a new"
                   % len(nostatus))
        out.append("        undeclared sorry would arrive indistinguishable from these:")
        for r in nostatus[:MAX_LISTED]:
            out.append("        %s (%s admitted)" %
                       (os.path.basename(r["path"]), r["actual_sorries"]))
    else:
        out.append("DECIDE: nothing.")

    print("\n".join(out))


if __name__ == "__main__":
    main()
