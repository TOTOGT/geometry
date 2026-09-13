#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Check that the scheduled checks actually ran.

A workflow that says it runs weekly is a claim. Like every other claim in this
corpus it needs an address: a dated receipt something can read. Without one,
"the audit runs on Tuesdays" is `pratijna` without `hetu`, and its silent
expiry is `kalatita` - true when written, expired unnoticed.

This reads the cron out of each workflow, reads the receipts in
docs/ci-receipts.tsv, and reports any workflow whose newest receipt is older
than its own cadence allows. It needs no network and no credentials, so it can
be run from anywhere by anyone - which is the point: enforcement that depends
on one account being awake is not enforcement.

    python3 tools/cadence_check.py [--grace 1.6] [--strict]

--strict exits 1 when a workflow is overdue. Default exits 0 and reports, so it
can be added to a pipeline before the receipts exist without breaking it.
"""
import argparse, datetime, io, os, re, sys

WF_DIR = ".github/workflows"
RECEIPTS = "docs/ci-receipts.tsv"
DAY = 86400.0


def cron_period_days(expr):
    """Coarse cadence in days. Only the shapes this repo actually uses."""
    f = expr.split()
    if len(f) != 5:
        return None
    mi, ho, dom, mon, dow = f
    if dow != "*" and dom == "*":
        n = len([x for x in re.split(r"[,]", dow) if x.strip()])
        if "-" in dow:
            a, b = dow.split("-")[:2]
            try:
                n = (int(b) - int(a)) % 7 + 1
            except ValueError:
                n = 1
        return 7.0 / max(1, n)
    if dom == "*" and dow == "*":
        if ho.startswith("*/"):
            return int(ho[2:]) / 24.0
        if ho == "*":
            return 1.0 / 24.0
        return 1.0
    return 30.0


def workflows():
    out = []
    if not os.path.isdir(WF_DIR):
        return out
    for fn in sorted(os.listdir(WF_DIR)):
        if not fn.endswith((".yml", ".yaml")):
            continue
        t = io.open(os.path.join(WF_DIR, fn), encoding="utf-8", errors="replace").read()
        nm = re.search(r"^name:\s*(.+)$", t, re.M)
        crons = re.findall(r"^\s*-\s*cron:\s*['\"]?([^'\"#\n]+?)['\"]?\s*(?:#.*)?$", t, re.M)
        if crons:
            out.append((fn, (nm.group(1).strip() if nm else fn), [c.strip() for c in crons]))
    return out


def receipts():
    seen = {}
    if not os.path.isfile(RECEIPTS):
        return seen
    for i, line in enumerate(io.open(RECEIPTS, encoding="utf-8")):
        if i == 0 or not line.strip():
            continue
        f = line.rstrip("\n").split("\t")
        if len(f) < 2:
            continue
        try:
            when = datetime.datetime.strptime(f[0][:19], "%Y-%m-%dT%H:%M:%S")
        except ValueError:
            continue
        key = f[1]
        if key not in seen or when > seen[key][0]:
            seen[key] = (when, f)
    return seen


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--grace", type=float, default=1.6,
                    help="multiple of the cadence tolerated before overdue")
    ap.add_argument("--strict", action="store_true")
    a = ap.parse_args()

    now = datetime.datetime.utcnow()
    rec, rows, overdue, unproven = receipts(), [], 0, 0
    for fn, name, crons in workflows():
        period = min(p for p in (cron_period_days(c) for c in crons) if p) if crons else None
        got = rec.get(fn) or rec.get(name)
        if not got:
            rows.append((fn, period, None, "NO RECEIPT EVER"))
            unproven += 1
            continue
        age = (now - got[0]).total_seconds() / DAY
        state = "ok"
        if period and age > period * a.grace:
            state = "OVERDUE by %.1fd" % (age - period)
            overdue += 1
        rows.append((fn, period, age, state))

    print("%-28s %8s %8s  %s" % ("workflow", "every", "last", "state"))
    for fn, period, age, state in rows:
        print("%-28s %7s %8s  %s" % (
            fn[:28],
            ("%.1fd" % period) if period else "-",
            ("%.1fd" % age) if age is not None else "never",
            state))
    print("\n%d scheduled workflow(s); %d overdue; %d have never left a receipt"
          % (len(rows), overdue, unproven))
    if unproven:
        print("A workflow with no receipt is not evidence that it ran. It is evidence")
        print("that nothing here can tell whether it ran, which is the same thing a")
        print("page saying 'machine-checked' with no gate file is.")
    if a.strict and (overdue or unproven):
        sys.exit(1)


if __name__ == "__main__":
    main()
