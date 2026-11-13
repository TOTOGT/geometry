#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Pablo Nogueira Grossi / G6 LLC
"""
book26/ch19-verify.py -- book26/ch19-a-toy-for-cycles-with-several-stable-states.html (Template B): a work sample, a
two-node model with several stable states, a bimodality test with stated failure conditions, and a measured power limit.
  [1] structure: hero, nav, sections in order, Sources footer; no script, form, network or storage code
  [2] RUN: tools/multistability_toy.py is run; it must print '0 FAIL', and every number typed on the page must appear
      in its output (thresholds, correlation, verdicts, BIC gains, D values, satellite table, power shares)
  [3] the four failure conditions M1-M4 are stated
  [4] honesty: no finding, agreement, review or experience claimed; no individual named; limits present
  [5] controls: each check family is run on a page with the matching statement removed and must fail   [HONESTY]
Standard library only (the toy needs numpy). Takes about 15 s.
"""
import re, subprocess, sys, html as _h
from pathlib import Path
HERE = Path(__file__).resolve().parent
PAGE = HERE / "ch19-a-toy-for-cycles-with-several-stable-states.html"
TOY = HERE.parent / "tools" / "multistability_toy.py"
FAIL = []
def check(label, ok, detail=""):
    print(("PASS " if ok else "FAIL ") + label + (f"  -- {detail}" if detail else ""))
    if not ok: FAIL.append(label)
raw = PAGE.read_text(encoding="utf-8")
def visible(r):
    t = re.sub(r"<(script|style)[^>]*>.*?</\1>", "", r, flags=re.S)
    t = re.sub(r"<[^>]+>", " ", t)
    return re.sub(r"\s+", " ", _h.unescape(t))
def body(r): return visible(r.split('<footer id="sources"', 1)[0])

p = subprocess.run([sys.executable, str(TOY)], capture_output=True, text=True, timeout=300)
OUT = re.sub(r"[ \t]+", " ", p.stdout)
check("[2] toy runs and prints 0 FAIL", p.returncode == 0 and "0 FAIL" in p.stdout, f"rc={p.returncode}")

# numbers typed on the page, each of which must be in the toy's output as a whole token
NUMS = ["0.828", "0.879", "13934.5", "5.65", "-29.7", "0.64", "3996.1", "0.00",
        "492", "1671", "0.390", "1220", "0.053", "575", "1147", "0.040", "1077", "0.162", "687", "0.014",
        "0.98", "0.59", "0.17", "0.02"]
def c_numbers(page_txt):
    res = []
    for n in NUMS:
        in_out = re.search(r"(?<![\d.])" + re.escape(n) + r"(?![\d])", OUT) is not None
        n_page = n.replace("-", "−") if n.startswith("-") else n
        on_page = (n in page_txt) or (n_page in page_txt)
        res.append((f"number {n} in toy output and on page", in_out and on_page))
    return res
FAILS_TXT = ["M1.", "M2.", "M3.", "M4.", "at least 80%", "no more than 5%"]
LIMITS = ["Any finding about a real economy", "several stable states", "That the test works on real data",
          "Care, investment or any motive", "Anything about Newark or New York", "Any experience in dynamical systems",
          "Any agreement, interest or review", "Anything after the date written"]
CLAIMS = [r"\bwe found\b", r"\bresults show\b", r"\bdemonstrates? that\b", r"\bproved\b", r"(?<!no one at the university )\bhas agreed\b",
          r"\bis interested\b", r"\bhas approved\b", r"\bour experience\b", r"\bI have worked\b"]
def c_struct(r):
    ids = re.findall(r'<section id="([a-z]+)"', r)
    return [("hero", 'class="hero"' in r), ("nav", 'class="pillars"' in r),
            ("sections in order", ids == ["intro","model","test","results","power","next","limits","updates","cross","checked"]),
            ("Sources footer", 'id="sources"' in r),
            ("no script/form/network/storage", not re.search(r"<script|<form|fetch\(|XMLHttpRequest|localStorage|sessionStorage", r))]
def c_fail(t): return [(f"failure condition {f}", f in t) for f in FAILS_TXT]
def c_honest(t):
    res = [("states no one has seen it", "No one at the university has seen this page" in t),
           ("states no claim about a real economy", "It makes no claim about any real economy" in t),
           ("no real data used", "no data from anywhere" in t)]
    res += [(f"no claim phrase {c}", not re.search(c, t, flags=re.I)) for c in CLAIMS]
    res += [(f"limit present: {l}", l in t) for l in LIMITS]
    return res
def run(tag, results):
    for l, o in results: check(f"{tag} {l}", o)

bt = body(raw)
run("[1]", c_struct(raw)); run("[2]", c_numbers(bt)); run("[3]", c_fail(bt)); run("[4]", c_honest(bt))
for l in sorted(set(re.findall(r'href="([^"#:]+\.html)"', raw))):
    check(f"[1] link resolves: {l}", ((HERE.parent / l[len("/geometry/"):]) if l.startswith("/geometry/") else (HERE / l)).exists())

print("== [5] controls (each must FAIL on a damaged page)")
def ctl(label, results_fn, damage):
    d = damage(raw); res = results_fn(d)
    check(f"[5] control: {label}", any(not o for _, o in res))
ctl("numbers fail when a number is altered", lambda r: c_numbers(body(r)), lambda r: r.replace("13934.5", "13934.9"))
ctl("failure conditions fail when M4 removed", lambda r: c_fail(body(r)), lambda r: r.replace("M4.", "X."))
ctl("honesty fails when the 'no one has seen it' line is removed", lambda r: c_honest(body(r)), lambda r: r.replace("No one at the university has seen this page", "Seen"))
ctl("honesty fails with an agreement claim added", lambda r: c_honest(body(r)), lambda r: r.replace("<section id=\"limits\">", "<p>The group has approved this.</p><section id=\"limits\">"))
ctl("structure fails when a section is removed", c_struct, lambda r: r.replace('<section id="power">', '<section id="powerX">'))

print(f"{len(FAIL)} FAIL"); sys.exit(1 if FAIL else 0)
