#!/usr/bin/env python3
"""regen_scoped.py -- regenerate or check ONE book's Chapter 0 page through the complete generator sequence.

  python3 tools/regen_scoped.py --book 4 --write    chapter_zero, then the four box generators, each scoped to the page
  python3 tools/regen_scoped.py --book 4 --check    run every scoped --check plus the chapter verifier; exit 1 if any fails

Steps (page = <bookdir>/ch00-definitions.html):
  1 chapter_zero.py --check --book N | --write --book N
  2 subject_tags.py, 3 gold_standard.py, 4 run_yourself.py, 5 crossref.py   each with --page PAGE (and --write in write mode)
  6 <bookdir>/ch00-verify.py   (content check; box markers must be exactly the expected four generator regions)
Every command and its exit status is printed. Nothing is skipped: a missing step or non-zero status fails the run.
In --write mode the same checks are run afterwards, so a write that leaves any step stale also fails.
"""
import argparse, os, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import chapter_zero as cz

def run(cmd, label, results):
    r = subprocess.run(cmd, capture_output=True, text=True)
    tail = (r.stdout.strip().splitlines() or [""])[-1][:150]
    print(f"[{'ok' if r.returncode == 0 else 'FAIL'}] exit {r.returncode}  {label}\n       $ {' '.join(('python3' if c == sys.executable else (os.path.relpath(c) if c.startswith('/') else c)) for c in cmd)}\n       {tail}")
    results.append((label, r.returncode))
    return r.returncode

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--book", type=int, required=True)
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--write", action="store_true"); g.add_argument("--check", action="store_true")
    a = ap.parse_args()
    d = cz.BOOKS[a.book][0]; page = f"{d}/ch00-definitions.html"
    T = os.path.join(cz.ROOT, "tools"); py = sys.executable; res = []
    gens = ["subject_tags", "gold_standard", "run_yourself", "crossref"]
    if a.write:
        run([py, os.path.join(T, "chapter_zero.py"), "--write", "--book", str(a.book)], "write chapter_zero", res)
        for g_ in gens:
            run([py, os.path.join(T, g_ + ".py"), "--write", "--page", page], f"write {g_}", res)
    run([py, os.path.join(T, "chapter_zero.py"), "--check", "--book", str(a.book)], "check chapter_zero", res)
    for g_ in gens:
        run([py, os.path.join(T, g_ + ".py"), "--page", page], f"check {g_} (scoped)", res)
    run([py, os.path.join(cz.ROOT, d, "ch00-verify.py")], "chapter verifier", res)
    want = 1 + len(gens) + 1
    ran = sum(1 for l, _ in res if l.startswith("check") or l == "chapter verifier")
    bad = [l for l, c in res if c != 0]
    print(f"\n{ran} of {want} checks ran; " + ("FAILED: " + ", ".join(bad) if bad else "all passed") + f"  ({page})")
    sys.exit(1 if bad or ran != want else 0)

if __name__ == "__main__":
    main()
