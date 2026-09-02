#!/usr/bin/env python3
"""
lexeme_census.py — count a lexeme and its paradigm across the whole corpus.

WHY THIS EXISTS
---------------
WP-94 publishes per-million rates and countability profiles for six lexemes.
A rate quoted from memory is a claim about a moment. This recomputes it, and
prints the denominator it used, so any published figure can be checked and so
the scope of a figure is never lost again (see WP-94 §7, which corrects a rate
that was right for one repository and published as if it covered the corpus).

WHAT IT COUNTS
--------------
Visible prose in git-tracked files, across the roots in tools/corpus_roots.txt.
HTML chrome (<script> <style> <nav> <footer>, comments) is stripped and <main>
preferred where present, matching tools/wordcount_scan.py. Extensions counted:
.html .htm .md .txt .tex .lean. A word is an alphabetic token. Redirect stubs
are skipped.

Singular and plural are counted as SEPARATE figures: `n` never includes the
plural. `axiom` has more plural tokens than singular ones, and collapsing them
would hide exactly the fact WP-94 §2 is about.

Usage
-----
    python3 tools/lexeme_census.py                 # the WP-94 six
    python3 tools/lexeme_census.py sorry:sorries lemma:lemmata
    python3 tools/lexeme_census.py --per-repo      # break the rate down by root
    python3 tools/lexeme_census.py --concordance grammar

An instrument that can examine nothing must fail when it examines nothing:
exits 2 on a scan of zero documents rather than printing a rate of 0.
"""
import argparse, collections, html as _html, os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOTS_FILE = os.path.join(HERE, "corpus_roots.txt")
EXT = (".html", ".htm", ".md", ".txt", ".tex", ".lean")
REDIRECT = re.compile(r'<meta\s+http-equiv=["\']refresh["\']', re.I)
TOK = re.compile(r"[A-Za-z][A-Za-z'’-]*")
FUNCTION_MOD = {
    "the", "this", "that", "these", "those", "his", "her", "its", "their", "our",
    "your", "whose", "same", "full", "more", "most", "not", "old", "new", "own",
    "one", "two", "three", "any", "some", "all", "each", "every", "no", "such",
    "and", "but", "for", "with", "from", "into", "than", "then", "else", "only",
    "very", "much", "less", "least", "both", "other", "another", "first", "last",
    "single", "whole", "entire", "above", "below", "here", "there", "what",
    "which", "when", "where", "was", "were", "are", "has", "had", "have", "been",
    "ational",
}
DEFAULT = ["sorry:sorries", "axiom:axioms", "proof:proofs",
           "conjecture:conjectures", "gap:gaps", "grammar:grammars"]
NUM = r"(?:\d+|zero|one|two|three|four|five|six|seven|eight|nine|ten)"
DET_SG = r"(?:a|an|the|this|that|another|each|every|one)"
DET_PL = r"(?:the|these|those|several|many|few|all|some|no|any|remaining|outstanding|two|three)"


def _resolve(path):
    """corpus_roots.txt records paths as they are on the author's machine
    (~/Desktop/...). Some environments mount the same trees one level down
    (~/mnt/Desktop/...). Try the literal path first, then the mounted one, so
    the same roots file works from either side without being edited."""
    home = os.path.expanduser("~")
    p = os.path.expanduser(path)
    if os.path.isdir(p):
        return p
    if p.startswith(home + os.sep):
        rel = p[len(home) + 1:]
        parts = rel.split(os.sep)
        # ~/Desktop/AXLE -> ~/mnt/Desktop/AXLE, and deeper trees that are
        # mounted by a shorter name: ~/Documents/Claude/Projects/io-clone
        # -> ~/mnt/Projects/io-clone -> ~/mnt/io-clone.
        for k in range(len(parts)):
            alt = os.path.join(home, "mnt", *parts[k:])
            if os.path.isdir(alt):
                return alt
    return None


def roots():
    out, missing = [], []
    for line in open(ROOTS_FILE, encoding="utf-8"):
        line = line.split("#")[0].strip()
        if not line:
            continue
        r = _resolve(line)
        (out.append(r) if r else missing.append(line))
    if missing:
        print("lexeme_census: roots not found on this machine, EXCLUDED from the "
              "denominator — any rate printed below is for a partial corpus:",
              file=sys.stderr)
        for m in missing:
            print(f"    {m}", file=sys.stderr)
        print(file=sys.stderr)
    return out


def visible(src, is_html):
    if not is_html:
        return src
    if REDIRECT.search(src):
        return ""
    src = re.sub(r"<!--.*?-->", " ", src, flags=re.S)
    src = re.sub(r"<(script|style|nav|footer)\b.*?</\1>", " ", src, flags=re.S | re.I)
    m = re.search(r"<main\b[^>]*>(.*?)</main>", src, flags=re.S | re.I)
    if m:
        src = m.group(1)
    else:
        b = re.search(r"<body\b[^>]*>(.*?)</body>", src, flags=re.S | re.I)
        src = b.group(1) if b else src
    return _html.unescape(re.sub(r"<[^>]+>", " ", src))


def documents(root):
    try:
        out = subprocess.run(["git", "-C", root, "ls-files"],
                             capture_output=True, text=True, timeout=300)
    except Exception:
        return
    for rel in out.stdout.splitlines():
        if not rel.endswith(EXT):
            continue
        try:
            src = open(os.path.join(root, rel), encoding="utf-8", errors="replace").read()
        except Exception:
            continue
        text = visible(src, rel.endswith((".html", ".htm")))
        if text.strip():
            yield rel, text


def profile(text, sg, pl):
    return {
        "n":       len(re.findall(rf"\b{sg}\b", text, re.I)),
        "pl":      len(re.findall(rf"\b{pl}\b", text, re.I)),
        "num+":    len(re.findall(rf"\b{NUM}\s+(?:{sg}|{pl})\b", text, re.I)),
        "det+sg":  len(re.findall(rf"\b{DET_SG}\s+{sg}\b", text, re.I)),
        "det+pl":  len(re.findall(rf"\b{DET_PL}\s+{pl}\b", text, re.I)),
        "N+X":     len(re.findall(rf"\b[A-Za-z][A-Za-z-]{{2,}}\s+{sg}\b", text, re.I)),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("lexemes", nargs="*", default=DEFAULT,
                    help="singular:plural pairs, e.g. sorry:sorries")
    ap.add_argument("--per-repo", action="store_true")
    ap.add_argument("--concordance", metavar="LEMMA")
    args = ap.parse_args()
    pairs = [l.split(":") if ":" in l else (l, l + "s") for l in (args.lexemes or DEFAULT)]

    per_repo, corpus, words, docs = {}, [], 0, 0
    for root in roots():
        name = os.path.basename(root)
        rw, rt = 0, []
        for rel, text in documents(root):
            docs += 1
            rw += len(TOK.findall(text))
            rt.append(text)
        per_repo[name] = ("\n".join(rt), rw)
        corpus.append("\n".join(rt))
        words += rw

    if docs == 0:
        sys.exit("lexeme_census: scanned zero documents — refusing to print a rate")

    text = "\n".join(corpus)
    print(f"documents         : {docs:,}")
    print(f"denominator       : {words:,} alphabetic word tokens (tracked, visible prose)\n")
    hdr = f"{'lexeme':<12}{'sg':>8}{'per M':>10}{'pl':>7}{'num+':>7}{'det+sg':>8}{'det+pl':>8}{'N+X':>7}"
    print(hdr); print("-" * len(hdr))
    for sg, pl in pairs:
        p = profile(text, sg, pl)
        print(f"{sg:<12}{p['n']:>8,}{p['n']/(words/1e6):>10.1f}{p['pl']:>7,}"
              f"{p['num+']:>7,}{p['det+sg']:>8,}{p['det+pl']:>8,}{p['N+X']:>7,}")

    if args.per_repo:
        print("\nPER REPOSITORY (a single corpus-wide rate is a mixture — report components)")
        for sg, pl in pairs:
            print(f"\n  {sg}")
            for name, (t, w) in sorted(per_repo.items(), key=lambda kv: -kv[1][1]):
                if not w:
                    continue
                n = len(re.findall(rf"\b{sg}\b", t, re.I))
                print(f"    {name:<14}{w:>10,} words{n:>8,}{n/(w/1e6):>10.1f}/M")

    if args.concordance:
        lem = args.concordance
        pat = re.compile(rf"\b{lem}(?:s|'s|’s)?\b", re.I)
        mods = collections.Counter()
        for m in pat.finditer(text):
            a, b = max(0, m.start() - 90), min(len(text), m.end() + 90)
            ctx = re.sub(r"\s+", " ", text[a:b]).strip()
            print("    ..." + ctx + "...")
        for m in re.finditer(rf"\b([A-Za-z][A-Za-z-]{{2,}})\s+{lem}\b", text, re.I):
            mods[m.group(1).lower()] += 1
        # Determiners, quantifiers and the like sit in the same slot as a real
        # modifier but do not individuate: "the grammar" names no kind. They are
        # reported separately rather than dropped, because the ratio between the
        # two is the point -- a type noun individuates by CONTENT modifier.
        content = collections.Counter({w: n for w, n in mods.items() if w not in FUNCTION_MOD})
        func = sum(n for w, n in mods.items() if w in FUNCTION_MOD)
        print(f"\n  X + {lem}: {sum(mods.values())} tokens total")
        print(f"    content modifiers : {sum(content.values())} tokens, "
              f"{len(content)} types, {sum(1 for v in content.values() if v == 1)} hapax")
        print(f"    function words    : {func} tokens "
              f"(determiners/quantifiers, listed but not counted as individuating)")
        for w, n in content.most_common(30):
            print(f"    {n:>4}  {w} {lem}")


if __name__ == "__main__":
    main()
