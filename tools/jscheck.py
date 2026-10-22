#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Pablo Nogueira Grossi / G6 LLC
"""
jscheck.py -- syntax-check every inline <script> in every HTML page.

WHY. On 2026-10-22 book4/chIV-field.html rendered on the live site with its
header, language bar and footer nav present and the entire chapter body
missing. Every check that exists in this repo passed on it: the file was
38,200 bytes, its divs balanced 36/36, `git diff origin/main` was empty, and
a fetch returned HTTP 200 with the right <title>.

The body of that chapter is not static HTML. It lives in a JS array
(`const PT = [...]`) and is injected into #contentA at load. One string
literal spanned six physical lines:

    document.head.insertAdjacentHTML('beforeend','<style>'+phaseCss+'
      .prov-add{...}
    </style>');

JavaScript does not allow a newline inside '...'. The parser threw
SyntaxError, so the WHOLE inline script -- renderer included -- never ran.
A page in that state is indistinguishable from a healthy one by any
file-level measure. Only parsing the script finds it.

Four more files carried the same class of defect, found by this check:
Book1.html (15 multi-line text:"..." literals, one per language array),
template-ebook-multilingual.html (unescaped inner double quotes), and
Enceladus.html / Enceladus-zenodo.html (CSS sitting inside <script>).

WHAT IT DOES. Extracts every inline <script> (ignoring those with src=) and
runs `node --check` on it. Reports each failure with the file, the block
index, and the line number translated back to the HTML file.

LIMITS, stated. `node --check` parses as a classic script: a block that is
legitimately an ES module (top-level import/export) will be reported as a
failure. None exists in this repo today; if one appears, exempt it here
rather than deleting the check. A block that parses is not thereby correct --
this finds syntax errors, not logic errors, and it cannot tell you whether a
renderer produced the right output.

USAGE
    python3 tools/jscheck.py              # whole repo from the repo root
    python3 tools/jscheck.py book4        # one subtree
Exit 0 if every block parses, 1 if any fails, 2 if node is not installed.
"""
import io, os, re, subprocess, sys

SKIP_DIRS = {".git", "node_modules", "_to_delete", ".lake", "build"}
SCRIPT_RE = re.compile(r'<script(?![^>]*\bsrc=)[^>]*>(.*?)</script>', re.S)


def blocks(path):
    """Yield (index, source, line_offset) for each inline script in a file."""
    try:
        text = io.open(path, encoding="utf-8").read()
    except (UnicodeDecodeError, OSError):
        return
    for i, m in enumerate(SCRIPT_RE.finditer(text)):
        src = m.group(1)
        if src.strip():
            yield i, src, text[:m.start(1)].count("\n") + 1


def main(root="."):
    if subprocess.run(["which", "node"], capture_output=True).returncode != 0:
        print("SKIP jscheck: node is not installed (needed for `node --check`)")
        return 2

    tmp = "/tmp/_jscheck_block.js"
    checked = failures = 0
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for fn in sorted(filenames):
            if not fn.endswith(".html"):
                continue
            path = os.path.join(dirpath, fn)
            for idx, src, offset in blocks(path):
                checked += 1
                io.open(tmp, "w", encoding="utf-8").write(src)
                r = subprocess.run(["node", "--check", tmp],
                                   capture_output=True, text=True)
                if r.returncode == 0:
                    continue
                failures += 1
                err = next((l for l in r.stderr.splitlines() if "Error" in l),
                           r.stderr.splitlines()[0] if r.stderr else "?")
                m = re.search(r'_jscheck_block\.js:(\d+)', r.stderr)
                where = ("%s:%d" % (path, offset + int(m.group(1)) - 1)
                         if m else path)
                print("FAIL %s  (inline script #%d)\n     %s"
                      % (where, idx, err.strip()[:160]))

    print("%s jscheck: %d inline scripts checked, %d failing"
          % ("FAIL" if failures else "PASS", checked, failures))
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else "."))
