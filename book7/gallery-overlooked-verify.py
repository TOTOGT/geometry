#!/usr/bin/env python3
"""Re-audit the overlooked-mathematicians gallery against this repository.

Usage:  python3 book7/gallery-overlooked-verify.py

The gallery page makes counting claims -- five of nineteen have a chapter here,
two entries fail its own premise, two tags do not match, two formula slots
carry someone else's work. Counting claims rot: a chapter gets written and the
page still says fourteen are missing.

So the card data lives in `gallery-overlooked-data.tsv`, verbatim as supplied,
and this script recomputes every count from it, re-checks each declared chapter
path against the filesystem, and fails if the page has stopped printing what
the data says.

It also looks for the opposite failure -- a card marked "no chapter" for whom a
chapter has since appeared. That is the good outcome and it still has to fail
the script, because a page that under-reports its own corpus is wrong in the
direction nobody checks.
"""
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
TSV = ROOT / "book7" / "gallery-overlooked-data.tsv"
PAGE = ROOT / "book7" / "gallery-overlooked.html"

# A surname or distinctive token to hunt for when a card claims no chapter.
HUNT = {
    "Aryabhata": "aryabhata", "Liu Hui": "liu-hui", "Brahmagupta": "brahmagupta",
    "Virahanka": "virahanka", "Al-Khwarizmi": "khwarizmi", "Al-Biruni": "biruni",
    "Bhaskara II": "bhaskara", "Al-Karaji": "karaji",
    "Abu'l-Wafa al-Buzjani": "buzjani", "Gangesa Upadhyaya": "gangesa",
    "Narayana Pandita": "narayana", "Jamshid al-Kashi": "kashi",
    "Seki Takakazu": "seki", "Shinichi Mochizuki": "mochizuki",
}


def rows():
    lines = TSV.read_text(encoding="utf-8").rstrip("\n").split("\n")
    head = lines[0].split("\t")
    for ln in lines[1:]:
        yield dict(zip(head, (ln.split("\t") + [""] * len(head))[:len(head)]))


def main():
    if not TSV.exists():
        print("::error::%s is missing" % TSV.relative_to(ROOT))
        return 1
    fail = []
    rs = list(rows())

    have = [r for r in rs if r["chapter"]]
    none = [r for r in rs if not r["chapter"]]
    flags = {}
    for r in rs:
        if r["flag"]:
            flags.setdefault(r["flag"], []).append(r["name"])

    print("  cards                     : %d" % len(rs))
    print("  with a chapter in this repo: %d" % len(have))
    print("  without                    : %d" % len(none))
    for k in sorted(flags):
        print("  flagged %-14s: %d  %s" % (k, len(flags[k]), ", ".join(flags[k])))

    # every declared chapter path must resolve from book7/
    for r in have:
        p = (ROOT / "book7" / r["chapter"]).resolve()
        if not p.exists():
            fail.append("%s: chapter %s does not exist" % (r["name"], r["chapter"]))

    # a card claiming no chapter, for whom one has appeared, is a stale page
    appeared = []
    for r in none:
        tok = HUNT.get(r["name"])
        if not tok:
            continue
        hits = []
        for d in ("book7", "omega", "book9"):
            base = ROOT / d
            if not base.is_dir():
                continue
            hits += [q.relative_to(ROOT).as_posix() for q in base.glob("*.html")
                     if tok in q.name.lower() and "gallery-overlooked" not in q.name]
        if hits:
            appeared.append((r["name"], hits))
    for n, h in appeared:
        fail.append("%s is marked 'no chapter' but %s exists -- update the TSV" % (n, h))

    if not PAGE.exists():
        fail.append("%s is missing" % PAGE.relative_to(ROOT))
    else:
        flat = " ".join(re.sub(r"<[^>]+>", " ",
                 re.sub(r"<script.*?</script>|<style.*?</style>", " ",
                        PAGE.read_text(encoding="utf-8"), flags=re.S)).split())
        checks = {
            "the card count": "nineteen",
            "the chapter count": "Five of nineteen",
            "the missing count": "fourteen",
        }
        for label, s in checks.items():
            if s.lower() not in flat.lower():
                fail.append("the page no longer states %s (%r)" % (label, s))
        # one status marker per card, and each count must agree with the
        # data rather than with the other.
        raw = PAGE.read_text(encoding="utf-8")
        n_none = raw.count('class="gchap gnone"')
        n_have = raw.count('class="gchap"')
        print("  page renders: %d 'no chapter', %d 'chapter ok'" % (n_none, n_have))
        if n_none != len(none):
            fail.append("page shows %d 'no chapter' markers; the data says %d" % (n_none, len(none)))
        if n_have != len(have):
            fail.append("page shows %d 'chapter ok' markers; the data says %d" % (n_have, len(have)))

    for f in fail:
        print("::error::" + f)
    if fail:
        return 1
    print("gallery audit recomputed from the card data; the page agrees with it.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
