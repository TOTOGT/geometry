#!/usr/bin/env python3
"""
wordcount_scan.py — count the words a reader actually reads.

WHY THIS EXISTS
---------------
Publishers, grant forms and cover notes ask for a length. A length quoted from
memory is a claim about a moment, and this corpus grows weekly. This recomputes
it from the files.

WHAT IT COUNTS
--------------
Visible prose only. <script>, <style>, <nav>, <footer> and HTML comments are
stripped before counting, so navigation chrome and licence boilerplate -- which
repeat on every page -- are not counted 48 times. Where a page has a <main>
element, only <main> is counted; otherwise the whole <body>.

Redirect stubs (<meta http-equiv="refresh">) are skipped: they have no prose.

Usage
-----
    python3 tools/wordcount_scan.py omega          # one directory
    python3 tools/wordcount_scan.py                # whole repository, by folder
    python3 tools/wordcount_scan.py omega --per-file
    python3 tools/wordcount_scan.py omega --json out.json
    python3 tools/wordcount_scan.py --self-test    # known-answer cases

An instrument that can examine nothing must fail when it examines nothing.
This one exits 2 on a scan of zero documents rather than printing "0 words".
"""

import argparse, glob, html as _html, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKIP = (".lake/", "_to_delete/", "to_delete/", "_archive/", "node_modules/", ".git/")
REDIRECT = re.compile(r'<meta\s+http-equiv=["\']refresh["\']', re.I)


def visible_words(src):
    src = re.sub(r"<!--.*?-->", " ", src, flags=re.S)
    src = re.sub(r"<(script|style|nav|footer)\b.*?</\1>", " ", src, flags=re.S | re.I)
    m = re.search(r"<main\b[^>]*>(.*?)</main>", src, flags=re.S | re.I)
    if m:
        src = m.group(1)
    else:
        b = re.search(r"<body\b[^>]*>(.*?)</body>", src, flags=re.S | re.I)
        src = b.group(1) if b else src
    text = _html.unescape(re.sub(r"<[^>]+>", " ", src))
    return len([w for w in re.split(r"\s+", text) if w.strip(".,;:—–-·|")])


SELF_TEST = [
    ("plain body", "<html><body><p>one two three four five</p></body></html>", 5),
    ("main wins", "<body><p>ignored here</p><main><p>a b c</p></main></body>", 3),
    ("chrome stripped",
     "<body><nav><a>Home</a></nav><main><p>x y</p></main><footer>c 2026 all rights</footer></body>", 2),
    ("script and comment stripped",
     "<body><main><script>var a=1;b=2</script><!-- note here --><p>only these words count</p></main></body>", 4),
    ("entities", "<body><main><p>caf&eacute; na&iuml;ve &amp; co</p></main></body>", 4),
]


def self_test():
    bad = 0
    for name, doc, want in SELF_TEST:
        got = visible_words(doc)
        ok = got == want
        bad += not ok
        print("  %-28s %3d  expected %3d   %s" % (name, got, want, "ok" if ok else "** WRONG **"))
    print("  %d/%d cases correct" % (len(SELF_TEST) - bad, len(SELF_TEST)))
    return bad


def scan(root, sub=None):
    base = os.path.join(root, sub) if sub else root
    rows = []
    for f in sorted(glob.glob(os.path.join(base, "**", "*.html"), recursive=True)):
        rel = os.path.relpath(f, root).replace(os.sep, "/")
        if any(k in rel for k in SKIP):
            continue
        try:
            s = open(f, encoding="utf-8", errors="replace").read()
        except OSError:
            continue
        if REDIRECT.search(s):
            continue
        rows.append({"file": rel, "words": visible_words(s)})
    return rows


def main(argv):
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("subdir", nargs="?")
    ap.add_argument("--root", default=ROOT)
    ap.add_argument("--per-file", action="store_true")
    ap.add_argument("--json", metavar="PATH")
    ap.add_argument("--self-test", action="store_true")
    a = ap.parse_args(argv[1:])

    print("wordcount_scan.py -- known-answer cases")
    if self_test():
        print("::error::the counter is wrong. Nothing below can be trusted.")
        return 2
    if a.self_test:
        return 0
    print()

    rows = scan(a.root, a.subdir)
    if not rows:
        print("::error::wordcount_scan.py read 0 documents. Check the path.")
        return 2

    total = sum(r["words"] for r in rows)
    if a.per_file:
        for r in sorted(rows, key=lambda r: -r["words"]):
            print("  %8s  %s" % (format(r["words"], ","), r["file"]))
        print()
    else:
        folders = {}
        for r in rows:
            k = r["file"].split("/")[0] if "/" in r["file"] else "(root)"
            folders.setdefault(k, [0, 0])
            folders[k][0] += r["words"]
            folders[k][1] += 1
        for k in sorted(folders, key=lambda k: -folders[k][0]):
            w, n = folders[k]
            print("  %10s words  %3d pages  %s" % (format(w, ","), n, k))
        print()

    print("  %s words across %d pages%s"
          % (format(total, ","), len(rows), (" in " + a.subdir) if a.subdir else ""))
    if a.json:
        json.dump({"total": total, "pages": len(rows), "rows": rows},
                  open(a.json, "w", encoding="utf-8"), indent=2)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
