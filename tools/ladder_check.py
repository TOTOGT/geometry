#!/usr/bin/env python3
"""Refuse a floor-ladder row whose three addresses disagree.

Usage:  python3 tools/ladder_check.py          (from the repository root)
        python3 tools/ladder_check.py --rehash

WHY THIS FILE EXISTS

On 2026-09-19 the shift-index proof was committed to `book11/` because
`docs/math-placement-map.md` gives Volume XI the role "the algebraic floor".
The file's own header then said "Volume XI". Both were wrong: rung 33 is
Volume XXXIII, and XI's subject is number fields and class groups, not an
index computation on a free module. Nothing in the repository objected. The
author did.

That is the failure this tool is aimed at, and it is worth naming precisely,
because it is not a reasoning failure. A session that has read a thousand
lines of this corpus will still put a file in the wrong volume, and the next
session will read the wrong volume and build on it. The repository cannot rely
on any session remembering where things go. It has to be able to say no.

So a rung's address is written in THREE independent places and this script
fails unless all three agree:

  1. the `volume` column of docs/floor-ladder.tsv
  2. the directory the file actually sits in  (book33/... -> XXXIII)
  3. the volume the .lean file declares in its own header

One of those can drift by accident. Three cannot drift the same way at once.

It also checks what the Book XVII verifier checks, for the same reason: the
saved `#print axioms` report proves nothing about a `.lean` file that has
changed since, so the recorded sha256 must match the bytes on disk, and
tools/axiom_gate.py must pass at the recorded theorem count.

A row with an empty `volume` is UNASSIGNED and is reported as such rather than
guessed at. Unassigned is a legitimate state. Guessed is not.
"""
import hashlib
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
LADDER = ROOT / "docs" / "floor-ladder.tsv"

NUM = [(1000,"M"),(900,"CM"),(500,"D"),(400,"CD"),(100,"C"),(90,"XC"),(50,"L"),
       (40,"XL"),(10,"X"),(9,"IX"),(5,"V"),(4,"IV"),(1,"I")]


def roman(n: int) -> str:
    out = ""
    for v, s in NUM:
        while n >= v:
            out += s
            n -= v
    return out


def unroman(s: str):
    vals = {"I":1,"V":5,"X":10,"L":50,"C":100,"D":500,"M":1000}
    if not s or any(c not in vals for c in s):
        return None
    total, prev = 0, 0
    for c in reversed(s):
        v = vals[c]
        total += -v if v < prev else v
        prev = max(prev, v)
    return total if roman(total) == s else None


def rows():
    lines = LADDER.read_text(encoding="utf-8").rstrip("\n").split("\n")
    head = lines[0].split("\t")
    for ln in lines[1:]:
        if ln.strip():
            yield dict(zip(head, ln.split("\t")))


def sha256(p: pathlib.Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main() -> int:
    fail, unassigned, ok = [], [], 0
    rehash = "--rehash" in sys.argv
    updated = []

    for r in rows():
        rung = r.get("rung", "?")
        rel = r.get("file", "").strip()
        vol = r.get("volume", "").strip()
        tag = f"rung {rung}"

        if r.get("status", "").startswith("not written"):
            if rel and (ROOT / rel).exists():
                fail.append(f"{tag}: marked 'not written' but {rel} exists")
            unassigned.append(f"{tag}: not written yet")
            updated.append(r)
            continue

        p = ROOT / rel
        if not rel or not p.exists():
            fail.append(f"{tag}: file {rel!r} does not exist")
            updated.append(r)
            continue

        # --- address 1 vs 2: the directory the file sits in
        m = re.match(r"book(\d+)/", rel)
        dir_vol = roman(int(m.group(1))) if m else None

        # --- address 3: the volume the file declares in its own header
        head = p.read_text(encoding="utf-8", errors="replace")[:2000]
        hm = re.search(r"Volume\s+([IVXLCDM]+)\b", head)
        file_vol = hm.group(1) if hm else None

        if not vol:
            unassigned.append(f"{tag}: {rel} has no volume in the ladder")
            if dir_vol or file_vol:
                fail.append(
                    f"{tag}: ladder says UNASSIGNED but the file claims "
                    f"{file_vol or dir_vol} — assign it or stop claiming it")
        else:
            if unroman(vol) is None:
                fail.append(f"{tag}: volume {vol!r} is not a roman numeral")
            if dir_vol and dir_vol != vol:
                fail.append(f"{tag}: ladder says {vol}, directory says {dir_vol} ({rel})")
            if file_vol and file_vol != vol:
                fail.append(f"{tag}: ladder says {vol}, the file's header says {file_vol}")
            if not file_vol:
                fail.append(f"{tag}: {rel} does not name its volume in its header")
            if dir_vol and unroman(vol) is not None and str(unroman(vol)) != m.group(1):
                fail.append(f"{tag}: directory book{m.group(1)} vs volume {vol}")

        # --- the proof still is what it was
        want = r.get("sha256", "").strip()
        got = sha256(p)
        if rehash:
            r["sha256"] = got
        elif want and want != got:
            fail.append(f"{tag}: {rel} sha256 {got[:12]}… != recorded {want[:12]}…; "
                        f"re-run the kernel, then --rehash")
        elif not want:
            fail.append(f"{tag}: no sha256 recorded for {rel}")

        rep = r.get("report", "").strip()
        n = r.get("theorems", "").strip()
        if rep and n:
            rp = ROOT / rep
            if not rp.exists():
                fail.append(f"{tag}: report {rep} missing")
            else:
                res = subprocess.run(
                    [sys.executable, str(ROOT / "tools" / "axiom_gate.py"), str(rp), n],
                    capture_output=True, text=True)
                out = (res.stdout + res.stderr).strip()
                print(f"  {tag:8s} {rel:34s} {out}")
                if res.returncode != 0:
                    fail.append(f"{tag}: gate failed on {rep}")
                else:
                    ok += 1
        else:
            fail.append(f"{tag}: no report/theorem count recorded")
        updated.append(r)

    if rehash:
        head = list(rows().__next__().keys()) if updated else []
        head = list(updated[0].keys())
        LADDER.write_text(
            "\t".join(head) + "\n"
            + "\n".join("\t".join(r.get(h, "") for h in head) for r in updated) + "\n",
            encoding="utf-8")
        print("ladder rehashed")
        return 0

    for u in unassigned:
        print(f"  UNASSIGNED  {u}")
    for f in fail:
        print(f"::error::{f}")
    if fail:
        return 1
    print(f"OK: {ok} rung(s) verified; {len(unassigned)} unassigned or unwritten. "
          f"Every written rung agrees with its directory and its own header.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
