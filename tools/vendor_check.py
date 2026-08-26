#!/usr/bin/env python3
"""
vendor_check.py — refuse to ship a drifted copy of a shared instrument.

WHY THIS EXISTS
---------------
On 2026-08-25 the vacuity scanner was ported from the Volume I bundle into
this repository. Within the hour, `isTriviallyInhabited` existed in FOUR files
with TWO spellings, and the two spellings were not introduced by the port --
the Volume I bundle's own `vacuity.lean` and `vacuity_fixtures.lean` already
disagreed with each other, and the port copied one from each.

Nothing was wrong yet. Both spellings were semantically identical. That is
exactly the state in which this defect is invisible: a duplicated instrument
does not announce itself until someone fixes a bug in one copy and the other
three keep the bug.

`tools/axiom_gate.py` was written for the same reason, one layer up. Its
docstring records CI run #245, where a shell pipeline copied into two workflow
steps carried one defect in two places, failed for the right theorem, and
printed the wrong reason. The lesson generalised: an instrument that exists in
more than one copy needs a mechanism that makes drift impossible to ship, not
a convention that makes it impolite.

WHAT IT CHECKS
--------------
For each entry in tools/vendor_manifest.json, the CORE of the file -- comments
and blank lines stripped, trailing whitespace removed -- is hashed and compared
to the recorded digest. Comments are excluded deliberately: a vendored copy
SHOULD carry a different header explaining where it came from and what it is
scoped to. What must not differ is the logic.

A vendored copy in another repository is checked by running this file there
with --manifest pointing at its own manifest, whose digests name this
repository as canonical.

WHAT IT DOES NOT CHECK
----------------------
That the canonical copy is correct. Nothing here validates behaviour -- that is
what the fixtures files are for. This tool only guarantees that every copy is
the SAME copy. A wrong instrument, faithfully vendored everywhere, passes.

Usage
-----
    python3 tools/vendor_check.py                  # verify against manifest
    python3 tools/vendor_check.py --update         # rewrite digests (review the diff)
    python3 tools/vendor_check.py --manifest PATH
"""

import argparse
import hashlib
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_MANIFEST = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "vendor_manifest.json")

# Comment syntax by extension. A language whose comments we cannot strip is a
# language we refuse to hash, rather than one we hash badly: a false OK here is
# worse than an error, because it reads as a verified match.
COMMENTS = {
    ".lean": {"block": (r"/-", r"-/"), "line": "--"},
    ".py":   {"block": None,           "line": "#"},
    ".sh":   {"block": None,           "line": "#"},
}


def core(path, marker=None):
    """Return the comment-free, whitespace-normalised body of a file.

    With `marker`, return only the region between
    `BEGIN SHARED BLOCK <marker>` and `END SHARED BLOCK <marker>`. Markers are
    comments, so the region is extracted BEFORE comments are stripped.

    A file that declares no such block, when one is expected, is an error and
    not an empty match. A silently empty region hashes to a stable value and
    would report every copy as identical -- a detector that did not run looks
    exactly like a detector that found nothing.
    """
    ext = os.path.splitext(path)[1]
    if ext not in COMMENTS:
        raise ValueError(
            "no comment syntax registered for %r -- add it to COMMENTS "
            "rather than hashing the file with its comments included" % ext)
    rule = COMMENTS[ext]
    src = open(path, encoding="utf-8").read()

    if marker:
        m = re.search(r"BEGIN SHARED BLOCK\s+" + re.escape(marker) +
                      r".*?\n(.*?)\S*\s*END SHARED BLOCK\s+" + re.escape(marker),
                      src, re.S)
        if not m:
            raise ValueError("no SHARED BLOCK %r in this file" % marker)
        src = m.group(1)

    if rule["block"]:
        open_tok, close_tok = rule["block"]
        src = re.sub(open_tok + r".*?" + close_tok, "", src, flags=re.S)

    out = []
    for line in src.splitlines():
        marker_tok = rule["line"]
        idx = line.find(marker_tok)
        if idx != -1:
            before = line[:idx]
            if before.count('"') % 2 == 0:
                line = before
        line = line.rstrip()
        if line.strip():
            out.append(line)
    return "\n".join(out) + "\n"


def digest(path, marker=None):
    return hashlib.sha256(core(path, marker).encode("utf-8")).hexdigest()


def main(argv):
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--manifest", default=DEFAULT_MANIFEST)
    ap.add_argument("--update", action="store_true",
                    help="rewrite the digests from the files on disk")
    ap.add_argument("--root", default=None,
                    help="repository root the manifest's paths are relative to "
                         "(default: the manifest's grandparent directory)")
    args = ap.parse_args(argv[1:])

    if not os.path.exists(args.manifest):
        print("::error::no manifest at %s" % args.manifest)
        return 1

    man = json.load(open(args.manifest, encoding="utf-8"))
    base = os.path.abspath(args.root) if args.root else \
        os.path.dirname(os.path.dirname(os.path.abspath(args.manifest)))
    bad, checked = [], 0

    for name, entry in sorted(man.get("instruments", {}).items()):
        for copy in entry["copies"]:
            path = os.path.join(base, copy)
            if not os.path.exists(path):
                bad.append((name, copy, "MISSING", ""))
                continue
            try:
                got = digest(path, entry.get("shared_block"))
            except ValueError as e:
                bad.append((name, copy, "UNHASHABLE", str(e)))
                continue
            checked += 1
            if args.update:
                entry["sha256"] = got
            elif got != entry["sha256"]:
                bad.append((name, copy, "DRIFTED", got))

    if args.update:
        json.dump(man, open(args.manifest, "w", encoding="utf-8"),
                  indent=2, sort_keys=True)
        print("digests rewritten for %d file(s) -- review the diff before committing"
              % checked)
        return 0

    print("vendor_check: %d file(s) hashed against %s"
          % (checked, os.path.basename(args.manifest)))

    # A run that hashed nothing is not a clean run. Without this, an empty
    # manifest -- or one whose paths all resolve wrong -- prints a summary and
    # returns 0, and a green step means the checker never looked at anything.
    # This tool exists because instruments drift silently; it must not be able
    # to pass silently itself.
    if checked == 0:
        print("::error::vendor_check hashed 0 files. An empty check is not a "
              "passing check -- verify the manifest paths and --root.")
        return 1

    if not bad:
        print("  all %d copies identical to canonical" % checked)
        return 0

    for name, copy, why, detail in bad:
        if why == "DRIFTED":
            print("::error::%s: %s has drifted from canonical (%s)"
                  % (name, copy, man["instruments"][name]["canonical"]))
            print("         recorded %s" % man["instruments"][name]["sha256"][:16])
            print("         found    %s" % detail[:16])
            print("         Fix the CANONICAL copy, re-vendor, then --update.")
            print("         Do not --update to silence a real difference.")
        else:
            print("::error::%s: %s %s %s" % (name, copy, why, detail))
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
